"""
FinTS integration for German banks (DKB, Commerzbank).
"""
import logging
from datetime import date
from decimal import Decimal
from time import sleep
from typing import Any, Dict, List, Optional

from fints.client import FinTS3PinTanClient, NeedTANResponse

from .base import (
    AccountInfo,
    AuthResult,
    BalanceInfo,
    BrokerIntegrationBase,
)

logger = logging.getLogger(__name__)


class FinTSIntegration(BrokerIntegrationBase):
    """Integration for German banks using FinTS protocol."""

    # FinTS product ID for this application
    PRODUCT_ID = 'literal:os.environ.get('FINTS_PRODUCT_ID', '')'

    def __init__(
        self,
        credentials: Dict[str, Any],
        bank_identifier: str,
        fints_server: str
    ):
        super().__init__(credentials)
        self.bank_identifier = bank_identifier
        self.fints_server = fints_server
        self._client: Optional[FinTS3PinTanClient] = None
        self._accounts = None
        self._authenticated = False

    def authenticate(self) -> AuthResult:
        """Initialize FinTS client and start authentication."""
        try:
            self._client = FinTS3PinTanClient(
                product_id=self.PRODUCT_ID,
                bank_identifier=self.bank_identifier,
                server=self.fints_server,
                user_id=self.credentials.get('username'),
                pin=self.credentials.get('pin'),
            )

            # Fetch available TAN mechanisms
            self._client.fetch_tan_mechanisms()
            mechs = self._client.get_tan_mechanisms()
            logger.info(f"Available TAN mechanisms: {mechs}")

            # Prefer decoupled TAN (app-based approval, mechanism 940)
            mech_keys = list(mechs.keys()) if isinstance(mechs, dict) else [str(m) for m in mechs]
            if '940' in mech_keys:
                self._client.set_tan_mechanism('940')
            elif mech_keys:
                # Use the first available mechanism
                self._client.set_tan_mechanism(mech_keys[0])

            # Start the session
            self._client.__enter__()

            # Check if 2FA is required
            if isinstance(self._client.init_tan_response, NeedTANResponse):
                is_decoupled = getattr(
                    self._client.init_tan_response, 'decoupled', False
                )

                if is_decoupled:
                    # Poll for app approval (decoupled TAN) — up to 5 minutes
                    logger.info("Waiting for banking app approval...")
                    max_attempts = 60  # 5 min at 5s intervals
                    for attempt in range(max_attempts):
                        result = self._client.send_tan(
                            self._client.init_tan_response, None
                        )
                        if not isinstance(result, NeedTANResponse):
                            self._authenticated = True
                            logger.info("App approval received.")
                            return AuthResult(success=True)
                        self._client.init_tan_response = result
                        logger.debug(
                            f"Waiting for app approval... ({attempt + 1}/{max_attempts})"
                        )
                        sleep(5)

                    return AuthResult(
                        success=False,
                        error_message='2FA approval timeout (5 min). Please approve in your banking app and retry.'
                    )
                else:
                    # Manual TAN entry required — return to frontend
                    return AuthResult(
                        success=False,
                        requires_2fa=True,
                        two_fa_type='tan',
                        session_data={'decoupled': False},
                        challenge_data={
                            'challenge': getattr(
                                self._client.init_tan_response, 'challenge', None
                            ),
                            'challenge_html': getattr(
                                self._client.init_tan_response, 'challenge_html', None
                            ),
                        }
                    )

            self._authenticated = True
            return AuthResult(success=True)

        except Exception as e:
            logger.exception("FinTS authentication failed")
            return AuthResult(
                success=False,
                error_message=str(e)
            )

    def complete_2fa(
        self,
        auth_code: Optional[str],
        session_data: Dict[str, Any]
    ) -> AuthResult:
        """Complete 2FA authentication."""
        if not self._client:
            return AuthResult(
                success=False,
                error_message="No active session. Call authenticate() first."
            )

        try:
            tan_response = self._client.init_tan_response

            if session_data.get('decoupled'):
                # Poll for app approval (decoupled TAN)
                max_attempts = 120  # 2 minutes timeout
                for attempt in range(max_attempts):
                    result = self._client.send_tan(tan_response, None)
                    if not isinstance(result, NeedTANResponse):
                        self._authenticated = True
                        return AuthResult(success=True)
                    logger.debug(f"Waiting for app approval... ({attempt + 1}/{max_attempts})")
                    sleep(1)

                return AuthResult(
                    success=False,
                    error_message='2FA approval timeout. Please approve in your banking app.'
                )
            else:
                # Submit TAN code
                if not auth_code:
                    return AuthResult(
                        success=False,
                        error_message='TAN code required for this authentication method.'
                    )
                self._client.send_tan(tan_response, auth_code)
                self._authenticated = True
                return AuthResult(success=True)

        except Exception as e:
            logger.exception("2FA completion failed")
            return AuthResult(
                success=False,
                error_message=str(e)
            )

    def get_accounts(self) -> List[AccountInfo]:
        """Fetch SEPA accounts from the bank."""
        if not self._client or not self._authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        # Small delay to ensure connection is ready
        sleep(2)

        sepa_accounts = self._client.get_sepa_accounts()
        self._accounts = sepa_accounts  # Cache for balance lookup

        accounts = []
        for acc in sepa_accounts:
            accounts.append(AccountInfo(
                identifier=acc.iban,
                name=getattr(acc, 'account_name', '') or acc.iban,
                account_type='checking',
                currency='EUR'
            ))

        return accounts

    def get_balance(self, account_identifier: str) -> BalanceInfo:
        """Fetch balance for a specific account."""
        if not self._client or not self._authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        if not self._accounts:
            self.get_accounts()

        # Find the account by IBAN
        account = None
        for acc in self._accounts:
            if acc.iban == account_identifier:
                account = acc
                break

        if not account:
            raise ValueError(f"Account {account_identifier} not found")

        balance = self._client.get_balance(account)

        # Extract balance amount
        amount = balance.amount.amount if hasattr(balance.amount, 'amount') else balance.amount
        currency = getattr(balance, 'currency', 'EUR')

        return BalanceInfo(
            balance=Decimal(str(amount)),
            currency=currency,
            balance_date=date.today(),
            raw_data={'fints_balance': str(balance)}
        )

    def close(self):
        """Close FinTS session."""
        if self._client:
            try:
                self._client.__exit__(None, None, None)
            except Exception as e:
                logger.warning(f"Error closing FinTS session: {e}")
            finally:
                self._client = None
                self._authenticated = False
