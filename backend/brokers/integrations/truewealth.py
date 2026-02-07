"""
TrueWealth integration.

TrueWealth is a Swiss robo-advisor that doesn't offer a public API.
This integration uses their internal web API endpoints.

Authentication flow:
1. Get initial cookies from /api/public/authCheck
2. Login with username, password, and optional TOTP token
3. Use session to fetch portfolio data

Note: This integration requires 2FA (TOTP) for login.
"""
import logging
import uuid
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests

from .base import (
    AccountInfo,
    AuthResult,
    BalanceInfo,
    BrokerIntegrationBase,
    PositionInfo,
)

logger = logging.getLogger(__name__)


class TrueWealthIntegration(BrokerIntegrationBase):
    """
    Integration for TrueWealth Swiss robo-advisor.

    Requires:
    - username (login ID)
    - password
    - totp_secret or token (one-time TOTP code)
    - portfolio_id (optional, will be discovered if not provided)
    """

    BASE_URL = "https://app.truewealth.ch"
    CLIENT_VERSION = "v499.0.0"

    def __init__(self, credentials: Dict[str, Any]):
        super().__init__(credentials)
        self.username = credentials.get('username')
        self.password = credentials.get('password')
        self.portfolio_id = credentials.get('portfolio_id')
        self._session = requests.Session()
        self._setup_session()
        self._authenticated = False
        # Use user-provided XSRF token or default (tokens don't expire)
        self._xsrf_token: Optional[str] = credentials.get('xsrf_token') or '6Z4VTEX76FGI3DM5HEBUWVRYHTGMYWBJ'
        self._portfolios: List[Dict] = []

    def _setup_session(self):
        """Configure session with required headers."""
        self._session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-Client-Version': self.CLIENT_VERSION,
            'X-Correlation-Id': str(uuid.uuid4())[:8],
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })

    def _get_initial_cookies(self) -> bool:
        """Fetch initial cookies including XSRF token."""
        try:
            # First visit the login page to establish session
            response = self._session.get(
                f"{self.BASE_URL}/app/login?lang=en",
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                },
                timeout=30
            )
            logger.info(f"TrueWealth login page: status={response.status_code}, content-length={len(response.text)}")

            # Log all response headers to understand what's being set
            logger.debug(f"TrueWealth login page headers: {dict(response.headers)}")

            # Only search for XSRF token if we don't already have one (hardcoded)
            if not self._xsrf_token:
                # Try to extract XSRF token from HTML if embedded in page
                import re
                xsrf_match = re.search(r'name=["\']_csrf["\'][^>]*value=["\']([^"\']+)["\']', response.text)
                if xsrf_match:
                    self._xsrf_token = xsrf_match.group(1)
                    logger.info(f"TrueWealth XSRF token found in HTML")
                else:
                    # Try alternative pattern
                    xsrf_match = re.search(r'XSRF-TOKEN["\s:]+["\']([^"\']+)["\']', response.text)
                    if xsrf_match:
                        self._xsrf_token = xsrf_match.group(1)
                        logger.info(f"TrueWealth XSRF token found in HTML (alt pattern)")

                # Log all cookies received
                logger.info(f"TrueWealth cookies after login page: {[(c.name, c.value[:20] + '...' if len(c.value) > 20 else c.value) for c in self._session.cookies]}")
                for cookie in self._session.cookies:
                    if 'XSRF' in cookie.name.upper() or 'CSRF' in cookie.name.upper() or 'TOKEN' in cookie.name.upper():
                        self._xsrf_token = cookie.value
                        logger.info(f"TrueWealth XSRF token found in cookie: {cookie.name}")

            # Then call authCheck - this may set additional cookies
            response = self._session.get(
                f"{self.BASE_URL}/api/public/authCheck",
                headers={
                    'Accept': 'application/json, text/plain, */*',
                    'Referer': f"{self.BASE_URL}/app/login?lang=en",
                    'X-Client-Version': self.CLIENT_VERSION,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                timeout=30
            )
            logger.info(f"TrueWealth authCheck: status={response.status_code}, body={response.text[:100] if response.text else '(empty)'}")

            # Check cookies again after authCheck (only if we don't have a token)
            if not self._xsrf_token:
                logger.info(f"TrueWealth cookies after authCheck: {[(c.name, c.value[:20] + '...' if len(c.value) > 20 else c.value) for c in self._session.cookies]}")
                for cookie in self._session.cookies:
                    if 'XSRF' in cookie.name.upper() or 'CSRF' in cookie.name.upper() or 'TOKEN' in cookie.name.upper():
                        self._xsrf_token = cookie.value
                        logger.info(f"TrueWealth XSRF token found after authCheck: {cookie.name}")

            if not self._xsrf_token:
                logger.warning("No XSRF token found - will try login without it")
            else:
                logger.info(f"Using XSRF token: {self._xsrf_token[:10]}...")

            return True
        except Exception as e:
            logger.error(f"Failed to get initial cookies: {e}")
            return False

    def authenticate(self) -> AuthResult:
        """
        Authenticate with TrueWealth.

        Requires username, password, and TOTP token or TOTP secret.
        If TOTP secret is provided, generates the code automatically.
        """
        if not self.username or not self.password:
            return AuthResult(
                success=False,
                error_message="Username and password are required."
            )

        # Get initial cookies
        if not self._get_initial_cookies():
            return AuthResult(
                success=False,
                error_message="Failed to initialize session with TrueWealth."
            )

        # Check if we have a TOTP token (user-provided OTP code)
        totp_token = self.credentials.get('token') or self.credentials.get('totp_token')

        # If no direct token, try to generate from secret
        if not totp_token:
            totp_secret = self.credentials.get('totp_secret')
            if totp_secret:
                try:
                    import pyotp
                    totp = pyotp.TOTP(totp_secret)
                    totp_token = totp.now()
                    logger.warning(f"Generated TOTP code from secret: {totp_token}")
                except Exception as e:
                    logger.error(f"Failed to generate TOTP code: {e}")
                    return AuthResult(
                        success=False,
                        error_message=f"Invalid TOTP secret: {e}"
                    )
        else:
            logger.warning(f"Using user-provided OTP token: {totp_token}")

        if not totp_token:
            # Need 2FA token
            return AuthResult(
                success=False,
                requires_2fa=True,
                two_fa_type='totp',
                session_data={'xsrf_token': self._xsrf_token},
                error_message="TOTP authentication code required."
            )

        return self._do_login(totp_token)

    def _do_login(self, totp_token: str) -> AuthResult:
        """Perform the actual login with credentials and TOTP."""
        try:
            # Build headers matching exact browser request from truewealth.txt
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9,de;q=0.8',
                'content-type': 'application/json; charset=utf-8',
                'dnt': '1',
                'origin': self.BASE_URL,
                'priority': 'u=1, i',
                'referer': f"{self.BASE_URL}/app/login?lang=en",
                'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-client-version': self.CLIENT_VERSION,
                'x-correlation-id': str(uuid.uuid4())[:8],
                'x-requested-with': 'XMLHttpRequest',
            }

            if self._xsrf_token:
                headers['x-xsrf-token'] = self._xsrf_token
                # Also set XSRF token as cookie with __Host- prefix (required by TrueWealth)
                self._session.cookies.set(
                    '__Host-XSRF-Token',
                    self._xsrf_token,
                    domain='app.truewealth.ch',
                    path='/'
                )
                logger.warning(f"Set __Host-XSRF-Token cookie: {self._xsrf_token[:10]}...")

            # TrueWealth login payload
            login_payload = {
                'loginId': self.username,
                'password': self.password,
                'token': totp_token,
            }

            logger.info(f"TrueWealth login attempt to {self.BASE_URL}/api/auth/login")
            logger.info(f"TrueWealth XSRF token: {self._xsrf_token[:20] + '...' if self._xsrf_token and len(self._xsrf_token) > 20 else self._xsrf_token}")
            logger.info(f"TrueWealth cookies before login: {[(c.name, c.domain) for c in self._session.cookies]}")

            # Try the login request
            response = self._session.post(
                f"{self.BASE_URL}/api/auth/login",
                json=login_payload,
                headers=headers,
                timeout=30
            )

            # Log detailed response info
            logger.info(f"TrueWealth login response: status={response.status_code}")
            logger.info(f"TrueWealth response cookies: {[(c.name, c.domain) for c in response.cookies]}")

            if response.status_code in (200, 204):
                self._authenticated = True
                # Try to discover portfolios
                self._discover_portfolios()
                return AuthResult(success=True)

            elif response.status_code == 401:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('message', 'Invalid credentials or TOTP code.')
                return AuthResult(
                    success=False,
                    error_message=error_msg
                )

            elif response.status_code == 403:
                return AuthResult(
                    success=False,
                    requires_2fa=True,
                    two_fa_type='totp',
                    error_message="Invalid or expired TOTP code. Please try again."
                )

            else:
                # Log response for debugging
                logger.error(f"TrueWealth login failed: status={response.status_code}")
                logger.error(f"TrueWealth response headers: {dict(response.headers)}")
                logger.error(f"TrueWealth response body: {response.text[:500] if response.text else '(empty)'}")

                # Check for common issues
                if response.status_code == 400:
                    # 400 can mean: missing fields, invalid format, CSRF issue, or blocked request
                    if not response.text or response.text == '':
                        error_msg = "Login rejected (400 with empty body). TrueWealth may be blocking automated requests or requiring additional headers."
                    else:
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('message', error_data.get('error', str(error_data)))
                        except Exception:
                            error_msg = f"Login failed: {response.text[:200]}"
                elif response.status_code == 429:
                    error_msg = "Rate limited. Please wait before trying again."
                else:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('message', error_data.get('error', f"Login failed with status {response.status_code}"))
                    except Exception:
                        error_msg = response.text[:200] if response.text else f"Login failed with status {response.status_code}"

                return AuthResult(
                    success=False,
                    error_message=error_msg
                )

        except requests.RequestException as e:
            logger.error(f"TrueWealth login request failed: {e}")
            return AuthResult(
                success=False,
                error_message=f"Connection error: {str(e)}"
            )

    def complete_2fa(
        self,
        auth_code: Optional[str],
        session_data: Dict[str, Any]
    ) -> AuthResult:
        """Complete 2FA by providing the TOTP code."""
        if not auth_code:
            return AuthResult(
                success=False,
                error_message="TOTP code is required."
            )

        # Restore session data
        if session_data.get('xsrf_token'):
            self._xsrf_token = session_data['xsrf_token']

        # Re-initialize cookies if needed
        if not self._xsrf_token:
            self._get_initial_cookies()

        return self._do_login(auth_code)

    def _discover_portfolios(self):
        """Discover available portfolios after login.

        Uses the customer-fee-schedules endpoint which returns portfolio IDs.
        Response format: [{"portfolioId": 677155, ...}, ...]
        """
        try:
            response = self._session.get(
                f"{self.BASE_URL}/api/user/fees/customer-fee-schedules",
                headers={
                    'Referer': f"{self.BASE_URL}/app/overview",
                    'X-XSRF-Token': self._xsrf_token or '',
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"TrueWealth fee schedules response: {data}")

                if isinstance(data, list):
                    # Extract portfolio IDs from fee schedules
                    # Format: [{"portfolioId": 677155, ...}, ...]
                    self._portfolios = []
                    seen_ids = set()
                    for item in data:
                        portfolio_id = item.get('portfolioId')
                        if portfolio_id and portfolio_id not in seen_ids:
                            seen_ids.add(portfolio_id)
                            self._portfolios.append({
                                'portfolioId': portfolio_id,
                                'id': portfolio_id,
                                'name': f'TrueWealth Portfolio {portfolio_id}',
                                'currency': 'CHF'
                            })
                    logger.info(f"Discovered {len(self._portfolios)} TrueWealth portfolios")

        except Exception as e:
            logger.warning(f"Failed to discover portfolios: {e}")

    def get_accounts(self) -> List[AccountInfo]:
        """Fetch list of portfolios as accounts."""
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        if not self._portfolios:
            self._discover_portfolios()

        accounts = []
        for portfolio in self._portfolios:
            portfolio_id = str(portfolio.get('id', portfolio.get('portfolioId', '')))
            accounts.append(AccountInfo(
                identifier=portfolio_id,
                name=portfolio.get('name', f'TrueWealth Portfolio {portfolio_id}'),
                account_type='brokerage',
                currency=portfolio.get('currency', 'CHF')
            ))

        # If no portfolios found but we have a configured portfolio_id, use that
        if not accounts and self.portfolio_id:
            accounts.append(AccountInfo(
                identifier=self.portfolio_id,
                name='TrueWealth Portfolio',
                account_type='brokerage',
                currency='CHF'
            ))

        return accounts

    def get_balance(self, account_identifier: str) -> BalanceInfo:
        """
        Fetch portfolio balance (net value).

        Uses the performanceSummary endpoint which returns portfolioItem.netValue.
        """
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        try:
            response = self._session.get(
                f"{self.BASE_URL}/api/portfolios/{account_identifier}/performanceSummary",
                headers={
                    'Referer': f"{self.BASE_URL}/app/overview",
                    'X-XSRF-Token': self._xsrf_token or '',
                },
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Extract net value from portfolioItem
            portfolio_item = data.get('portfolioItem', data)
            net_value = portfolio_item.get('netValue', 0)
            currency = portfolio_item.get('currency', 'CHF')

            # Try to get the date
            balance_date = date.today()
            if 'date' in data:
                try:
                    from datetime import datetime
                    balance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass

            return BalanceInfo(
                balance=Decimal(str(net_value)),
                currency=currency,
                balance_date=balance_date,
                raw_data=data
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch balance: {e}")
            raise RuntimeError(f"Failed to fetch portfolio balance: {str(e)}")

    def get_positions(self, account_identifier: str) -> List[PositionInfo]:
        """
        Fetch portfolio positions/holdings.

        Uses the portfolio details endpoint.
        """
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        positions = []

        try:
            # Try to get detailed holdings
            response = self._session.get(
                f"{self.BASE_URL}/api/portfolios/{account_identifier}/holdings",
                headers={
                    'Referer': f"{self.BASE_URL}/app/overview",
                    'X-XSRF-Token': self._xsrf_token or '',
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                holdings = data if isinstance(data, list) else data.get('holdings', [])

                for holding in holdings:
                    positions.append(self._parse_holding(holding))

        except Exception as e:
            logger.warning(f"Failed to fetch positions: {e}")

        return positions

    def _parse_holding(self, holding: Dict) -> PositionInfo:
        """Parse a holding into PositionInfo."""
        quantity = holding.get('quantity', holding.get('units', 0))
        price = holding.get('price', holding.get('pricePerUnit', 0))
        market_value = holding.get('marketValue', holding.get('value', 0))

        # Determine asset class
        asset_type = holding.get('assetClass', holding.get('type', '')).lower()
        asset_class_map = {
            'equity': 'equity',
            'stock': 'equity',
            'bond': 'fixed_income',
            'fixed income': 'fixed_income',
            'cash': 'cash',
            'real estate': 'real_estate',
            'commodity': 'commodity',
            'gold': 'commodity',
        }
        asset_class = asset_class_map.get(asset_type, 'other')

        return PositionInfo(
            symbol=holding.get('symbol', holding.get('ticker', '')),
            name=holding.get('name', holding.get('description', '')),
            isin=holding.get('isin'),
            quantity=Decimal(str(quantity)),
            price_per_unit=Decimal(str(price)),
            market_value=Decimal(str(market_value)),
            currency=holding.get('currency', 'CHF'),
            cost_basis=Decimal(str(holding['costBasis'])) if holding.get('costBasis') else None,
            asset_class=asset_class
        )

    def supports_historical_data(self) -> bool:
        """TrueWealth provides performance history."""
        return True

    def get_historical_balances(
        self,
        account_identifier: str,
        start_date: date,
        end_date: date
    ) -> List[BalanceInfo]:
        """
        Fetch historical balances from TrueWealth performance history.
        """
        from datetime import datetime

        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                return []

        try:
            # Try performance history endpoint
            response = self._session.get(
                f"{self.BASE_URL}/api/portfolios/{account_identifier}/performance/history",
                params={
                    'from': start_date.isoformat(),
                    'to': end_date.isoformat(),
                },
                headers={
                    'Referer': f"{self.BASE_URL}/app/overview",
                    'X-XSRF-Token': self._xsrf_token or '',
                },
                timeout=30
            )

            if response.status_code != 200:
                # Try alternative endpoint
                response = self._session.get(
                    f"{self.BASE_URL}/api/portfolios/{account_identifier}/chart",
                    params={
                        'startDate': start_date.isoformat(),
                        'endDate': end_date.isoformat(),
                    },
                    headers={
                        'Referer': f"{self.BASE_URL}/app/overview",
                        'X-XSRF-Token': self._xsrf_token or '',
                    },
                    timeout=30
                )

            if response.status_code != 200:
                logger.debug(f"TrueWealth historical data not available: {response.status_code}")
                return []

            data = response.json()
            historical = []

            # Parse response - common formats: [{date, value}, ...] or {dates: [], values: []}
            if isinstance(data, list):
                for entry in data:
                    entry_date = entry.get('date') or entry.get('timestamp')
                    entry_value = entry.get('value') or entry.get('netValue') or entry.get('totalValue')
                    if entry_date and entry_value:
                        try:
                            if isinstance(entry_date, str):
                                bal_date = datetime.strptime(entry_date[:10], '%Y-%m-%d').date()
                            else:
                                bal_date = date.fromtimestamp(entry_date / 1000)  # ms timestamp
                            historical.append(BalanceInfo(
                                balance=Decimal(str(entry_value)),
                                currency='CHF',
                                balance_date=bal_date
                            ))
                        except (ValueError, TypeError):
                            continue
            elif isinstance(data, dict):
                dates = data.get('dates', [])
                values = data.get('values', data.get('netValues', []))
                for d, v in zip(dates, values):
                    try:
                        if isinstance(d, str):
                            bal_date = datetime.strptime(d[:10], '%Y-%m-%d').date()
                        else:
                            bal_date = date.fromtimestamp(d / 1000)
                        historical.append(BalanceInfo(
                            balance=Decimal(str(v)),
                            currency='CHF',
                            balance_date=bal_date
                        ))
                    except (ValueError, TypeError):
                        continue

            logger.info(f"TrueWealth: Found {len(historical)} historical entries")
            return historical

        except Exception as e:
            logger.warning(f"Failed to fetch TrueWealth historical data: {e}")
            return []

    def close(self):
        """Close the session."""
        if self._session:
            try:
                # Try to logout
                self._session.post(
                    f"{self.BASE_URL}/api/auth/logout",
                    headers={'X-XSRF-Token': self._xsrf_token or ''},
                    timeout=10
                )
            except Exception:
                pass
            self._session.close()
            self._session = None
        self._authenticated = False
        self._xsrf_token = None
