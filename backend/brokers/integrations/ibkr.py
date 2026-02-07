"""
Interactive Brokers (IBKR) Client Portal API integration.

This integration connects to the IBKR Client Portal Gateway, which must be
running locally on the user's machine. The gateway handles authentication
with IBKR servers.

Requirements:
- IBKR Pro account (Lite accounts not supported)
- Client Portal Gateway running locally
- Java 8 update 192+ or OpenJDK 11+

See: https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/
"""
import logging
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import ConnectionError, Timeout

from .base import (
    AccountInfo,
    AuthResult,
    BalanceInfo,
    BrokerIntegrationBase,
    PositionInfo,
)

logger = logging.getLogger(__name__)


class IBKRIntegration(BrokerIntegrationBase):
    """
    Integration for Interactive Brokers via Client Portal Gateway.

    The Client Portal Gateway must be running locally and the user must
    have authenticated via the gateway's web interface before using this
    integration.

    Default gateway URL: https://localhost:5000
    """

    # Asset class mapping from IBKR to our standard classes
    ASSET_CLASS_MAP = {
        'STK': 'equity',
        'OPT': 'equity',  # Options
        'FUT': 'commodity',  # Futures
        'CASH': 'cash',
        'BOND': 'fixed_income',
        'FUND': 'equity',  # Mutual funds
        'ETF': 'equity',
        'WAR': 'equity',  # Warrants
        'CRYPTO': 'crypto',
    }

    def __init__(
        self,
        credentials: Dict[str, Any],
        gateway_url: str = 'https://localhost:5000'
    ):
        """
        Initialize IBKR integration.

        Args:
            credentials: Dict with optional 'gateway_url' override
            gateway_url: Base URL for Client Portal Gateway
        """
        super().__init__(credentials)
        self.gateway_url = credentials.get('gateway_url', gateway_url)
        self._session = requests.Session()
        # Disable SSL verification for local gateway (self-signed cert)
        self._session.verify = False
        self._accounts_cache: Optional[List[Dict]] = None
        self._authenticated = False

        # Suppress SSL warnings for local gateway
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Make a request to the Client Portal Gateway."""
        url = f"{self.gateway_url}/v1/api{endpoint}"
        try:
            response = self._session.request(method, url, timeout=30, **kwargs)
            return response
        except ConnectionError:
            raise ConnectionError(
                "Cannot connect to IBKR Client Portal Gateway. "
                "Please ensure the gateway is running at " + self.gateway_url
            )
        except Timeout:
            raise Timeout("Request to IBKR Gateway timed out")

    def authenticate(self) -> AuthResult:
        """
        Check authentication status with the gateway.

        The actual authentication happens via the gateway's web interface.
        This method verifies that the user has already authenticated.
        """
        try:
            # Check authentication status
            response = self._request('GET', '/iserver/auth/status')

            if response.status_code != 200:
                return AuthResult(
                    success=False,
                    error_message=f"Gateway returned status {response.status_code}"
                )

            data = response.json()
            authenticated = data.get('authenticated', False)
            connected = data.get('connected', False)

            if authenticated and connected:
                self._authenticated = True
                # Tickle to keep session alive
                self._request('POST', '/tickle')
                return AuthResult(success=True)

            # Not authenticated - user needs to log in via gateway
            if not authenticated:
                return AuthResult(
                    success=False,
                    requires_2fa=True,
                    two_fa_type='gateway',
                    error_message=(
                        "Please authenticate via the Client Portal Gateway web interface "
                        f"at {self.gateway_url}"
                    ),
                    challenge_data={
                        'gateway_url': self.gateway_url,
                        'instructions': (
                            "1. Open the gateway URL in your browser\n"
                            "2. Log in with your IBKR credentials\n"
                            "3. Complete any 2FA challenges\n"
                            "4. Return here and retry the sync"
                        )
                    }
                )

            return AuthResult(
                success=False,
                error_message="Gateway connected but not authenticated"
            )

        except ConnectionError as e:
            return AuthResult(
                success=False,
                error_message=str(e)
            )
        except Exception as e:
            logger.exception("IBKR authentication check failed")
            return AuthResult(
                success=False,
                error_message=f"Authentication check failed: {str(e)}"
            )

    def complete_2fa(
        self,
        auth_code: Optional[str],
        session_data: Dict[str, Any]
    ) -> AuthResult:
        """
        For IBKR, 2FA is handled via the gateway web interface.
        This method simply re-checks authentication status.
        """
        return self.authenticate()

    def _ensure_authenticated(self):
        """Ensure we have an authenticated session."""
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(
                    result.error_message or "Not authenticated with IBKR"
                )

    def get_accounts(self) -> List[AccountInfo]:
        """Fetch list of accounts from IBKR."""
        self._ensure_authenticated()

        response = self._request('GET', '/portfolio/accounts')

        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch accounts: {response.status_code} - {response.text}"
            )

        accounts_data = response.json()
        self._accounts_cache = accounts_data

        accounts = []
        for acc in accounts_data:
            account_id = acc.get('id') or acc.get('accountId')
            account_type = acc.get('type', 'brokerage').lower()

            # Map IBKR account types
            if 'ira' in account_type.lower():
                mapped_type = 'retirement'
            else:
                mapped_type = 'brokerage'

            accounts.append(AccountInfo(
                identifier=account_id,
                name=acc.get('accountAlias') or acc.get('accountTitle') or account_id,
                account_type=mapped_type,
                currency=acc.get('currency', 'USD')
            ))

        return accounts

    def get_balance(self, account_identifier: str) -> BalanceInfo:
        """
        Fetch account balance/summary from IBKR.

        Returns the Net Liquidation Value as the balance.
        """
        self._ensure_authenticated()

        # Fetch account summary/ledger
        response = self._request(
            'GET',
            f'/portfolio/{account_identifier}/ledger'
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch balance: {response.status_code} - {response.text}"
            )

        ledger_data = response.json()

        # The ledger contains balances by currency
        # We want the base currency total (usually in 'BASE' key)
        base_data = ledger_data.get('BASE', {})

        # Net Liquidation Value is the total account value
        net_liq = base_data.get('netliquidationvalue', 0)
        available = base_data.get('availablefunds', 0)
        currency = base_data.get('currency', 'USD')

        # If no BASE, try to find the primary currency
        if not base_data:
            for curr, data in ledger_data.items():
                if isinstance(data, dict) and 'netliquidationvalue' in data:
                    net_liq = data.get('netliquidationvalue', 0)
                    available = data.get('availablefunds', 0)
                    currency = data.get('currency', curr)
                    break

        return BalanceInfo(
            balance=Decimal(str(net_liq)),
            currency=currency,
            balance_date=date.today(),
            available_balance=Decimal(str(available)) if available else None,
            raw_data=ledger_data
        )

    def get_positions(self, account_identifier: str) -> List[PositionInfo]:
        """Fetch all positions for an account."""
        self._ensure_authenticated()

        # First, invalidate cache to get fresh positions
        self._request('POST', f'/portfolio/{account_identifier}/positions/invalidate')

        # Fetch positions (paginated, page 0)
        response = self._request(
            'GET',
            f'/portfolio/{account_identifier}/positions/0'
        )

        if response.status_code != 200:
            if response.status_code == 404:
                return []  # No positions
            raise RuntimeError(
                f"Failed to fetch positions: {response.status_code} - {response.text}"
            )

        positions_data = response.json()
        positions = []

        for pos in positions_data:
            if not pos:
                continue

            # Extract position data
            conid = pos.get('conid')
            quantity = pos.get('position', 0)

            # Skip zero positions
            if quantity == 0:
                continue

            market_value = pos.get('mktValue', 0)
            market_price = pos.get('mktPrice', 0)
            avg_cost = pos.get('avgCost', 0)
            currency = pos.get('currency', 'USD')

            # Asset class mapping
            asset_class_raw = pos.get('assetClass', 'STK')
            asset_class = self.ASSET_CLASS_MAP.get(asset_class_raw, 'other')

            positions.append(PositionInfo(
                symbol=pos.get('contractDesc', '') or pos.get('ticker', ''),
                name=pos.get('name', '') or pos.get('contractDesc', ''),
                quantity=Decimal(str(abs(quantity))),
                price_per_unit=Decimal(str(market_price)),
                market_value=Decimal(str(abs(market_value))),
                currency=currency,
                isin=None,  # IBKR uses conid, not ISIN
                cost_basis=Decimal(str(abs(avg_cost * quantity))) if avg_cost else None,
                asset_class=asset_class
            ))

        return positions

    def get_pnl(self, account_identifier: str) -> Dict[str, Any]:
        """Get profit/loss information for the account."""
        self._ensure_authenticated()

        response = self._request('GET', '/iserver/account/pnl/partitioned')

        if response.status_code != 200:
            return {}

        return response.json()

    def tickle(self):
        """
        Keep the session alive.
        Should be called every few minutes to prevent timeout.
        """
        try:
            self._request('POST', '/tickle')
        except Exception as e:
            logger.warning(f"Tickle failed: {e}")

    def close(self):
        """Close the session."""
        if self._session:
            try:
                # Optionally log out (uncomment if needed)
                # self._request('POST', '/logout')
                self._session.close()
            except Exception:
                pass
            finally:
                self._session = None
                self._authenticated = False
