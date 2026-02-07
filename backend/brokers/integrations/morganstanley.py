"""
Morgan Stanley at Work integration.

Morgan Stanley at Work is a platform for employee stock plans and equity compensation.
This integration uses their internal web API and GraphQL endpoints.

Authentication flow:
1. Get initial cookies from /solium/servlet/userLogin.do
2. Login with account number and password (form-based)
3. Extract JWT token from response
4. Use GraphQL API to fetch portfolio data

Note: This integration may require 2FA depending on account settings.
"""
import logging
import re
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


class MorganStanleyIntegration(BrokerIntegrationBase):
    """
    Integration for Morgan Stanley at Work (employee stock plans).

    Requires:
    - account_number (employee/participant ID)
    - password
    """

    BASE_URL = "https://atwork.morganstanley.com"
    GRAPHQL_URL = "https://atwork.morganstanley.com/graphql"

    def __init__(self, credentials: Dict[str, Any]):
        super().__init__(credentials)
        self.account_number = credentials.get('account_number') or credentials.get('username')
        self.password = credentials.get('password')
        self.employee_id = credentials.get('employee_id')
        self._session = requests.Session()
        self._setup_session()
        self._authenticated = False
        # Support direct JWT token (bypasses login - recommended due to bot detection)
        self._jwt_token: Optional[str] = credentials.get('jwt_token')
        self._portfolio_data: Optional[Dict] = None

        # If JWT token provided, we're already authenticated
        if self._jwt_token and self.employee_id:
            self._authenticated = True
            logger.info("Morgan Stanley: Using provided JWT token and employee ID")

    def _setup_session(self):
        """Configure session with required headers."""
        self._session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Ch-Ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        })

    def _get_initial_cookies(self) -> bool:
        """Fetch initial cookies and login page."""
        try:
            response = self._session.get(
                f"{self.BASE_URL}/solium/servlet/userLogin.do",
                timeout=30
            )
            response.raise_for_status()

            # Store the page content for CSRF token extraction if needed
            self._login_page = response.text

            return True
        except Exception as e:
            logger.error(f"Failed to get initial cookies: {e}")
            return False

    def _extract_csrf_token(self) -> Optional[str]:
        """Extract CSRF token from login page if present."""
        if not hasattr(self, '_login_page'):
            return None

        # Look for hidden form fields with CSRF-like names
        patterns = [
            r'name="TO_[^"]+"\s+value="([^"]+)"',
            r'name="_csrf"\s+value="([^"]+)"',
            r'name="csrf_token"\s+value="([^"]+)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, self._login_page)
            if match:
                return match.group(1)

        return None

    def authenticate(self) -> AuthResult:
        """
        Authenticate with Morgan Stanley at Work.

        Supports two modes:
        1. JWT token + employee ID (recommended - bypasses bot detection)
        2. Account number + password (may fail due to bot detection)
        """
        # If JWT token already provided, we're authenticated
        if self._jwt_token and self.employee_id:
            self._authenticated = True
            logger.info("Morgan Stanley: Already authenticated via JWT token")
            return AuthResult(success=True)

        # Fall back to username/password login (may fail due to bot detection)
        if not self.account_number or not self.password:
            return AuthResult(
                success=False,
                error_message="JWT token and employee ID are required. "
                             "Log in via browser, open DevTools > Network, find a /graphql request, "
                             "and copy the 'authorization' and 'employeeId' headers."
            )

        # Get initial cookies
        if not self._get_initial_cookies():
            return AuthResult(
                success=False,
                error_message="Failed to initialize session with Morgan Stanley."
            )

        return self._do_login()

    def _do_login(self) -> AuthResult:
        """Perform the actual login with credentials."""
        try:
            # Build form data matching the browser request
            form_data = {
                'state': '',
                'lang': '',
                'browserwidth': '1452',
                'browserheight': '429',
                'screenwidth': '1512',
                'screenheight': '982',
                'requested_lang': 'en',
                'login_method': 'account_number',
                'account_number': self.account_number,
                'account_number_dummy': self.account_number,
                'password': self.password,
                'password_dummy': '',
                'remember': 'true',
            }

            # Add CSRF token if found (format: TO_xxxx=value)
            csrf_token = self._extract_csrf_token()
            if csrf_token:
                # The token name varies - try to find it
                token_match = re.search(r'name="(TO_[^"]+)"', self._login_page)
                if token_match:
                    form_data[token_match.group(1)] = csrf_token

            # Add fingerprints (simplified versions - Morgan Stanley may require these)
            # These are complex browser fingerprints; using minimal placeholders
            form_data['ms_rsa_footprint'] = 'version%3D3.5.1_4'
            form_data['symantec_device_fingerprint'] = ''

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cache-Control': 'max-age=0',
                'Origin': self.BASE_URL,
                'Referer': f"{self.BASE_URL}/solium/servlet/userLogin.do",
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
            }

            logger.info(f"Morgan Stanley login attempt to {self.BASE_URL}/solium/servlet/userLogin.do")
            logger.debug(f"Morgan Stanley form data keys: {list(form_data.keys())}")

            response = self._session.post(
                f"{self.BASE_URL}/solium/servlet/userLogin.do",
                data=form_data,
                headers=headers,
                timeout=30,
                allow_redirects=True
            )

            logger.info(f"Morgan Stanley login response: status={response.status_code}, url={response.url}")
            logger.info(f"Morgan Stanley cookies after login: {[(c.name, c.domain) for c in self._session.cookies]}")
            logger.info(f"Morgan Stanley response headers: {dict(response.headers)}")

            # Store dashboard page for JWT extraction attempts
            self._dashboard_page = response.text

            # Log response snippet for debugging
            logger.warning(f"Morgan Stanley response body (first 2000 chars): {response.text[:2000]}")

            # Save full HTML for debugging
            try:
                with open('/tmp/ms_dashboard.html', 'w') as f:
                    f.write(response.text)
                logger.warning(f"Morgan Stanley: Saved full HTML ({len(response.text)} bytes) to /tmp/ms_dashboard.html")
            except Exception as e:
                logger.warning(f"Morgan Stanley: Failed to save HTML: {e}")

            # Look for embedded JSON data or participant info in the full page
            import json as json_module
            # Search for JSON objects in script tags
            script_data_patterns = [
                r'var\s+(\w+)\s*=\s*(\{[^;]+\});',  # var name = {...};
                r'window\.(\w+)\s*=\s*(\{[^;]+\});',  # window.name = {...};
                r'data-config=["\'](\{[^"\']+\})["\']',  # data-config="{...}"
            ]
            for pattern in script_data_patterns:
                for match in re.finditer(pattern, response.text[:50000]):
                    try:
                        var_name = match.group(1) if match.lastindex >= 1 else 'unknown'
                        json_str = match.group(2) if match.lastindex >= 2 else match.group(1)
                        data = json_module.loads(json_str)
                        logger.info(f"Morgan Stanley embedded data '{var_name}': {list(data.keys()) if isinstance(data, dict) else type(data)}")
                        # Check for useful fields
                        if isinstance(data, dict):
                            for key in ['token', 'jwt', 'authorization', 'participantId', 'employeeId', 'userId', 'accountId']:
                                if key in data:
                                    logger.info(f"Morgan Stanley found {key} in embedded data: {str(data[key])[:100]}")
                    except Exception:
                        pass

            # Look for participant ID in various formats
            participant_patterns = [
                r'participantId["\s:=]+["\']?(\d+)',
                r'participant_id["\s:=]+["\']?(\d+)',
                r'accountId["\s:=]+["\']?(\d+)',
                r'userId["\s:=]+["\']?(\d+)',
                r'employeeId["\s:=]+["\']?(\d+)',
            ]
            for pattern in participant_patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    logger.info(f"Morgan Stanley found ID via pattern '{pattern[:30]}': {match.group(1)}")

            # Check for successful login
            if response.status_code == 200:
                # Look for JWT token in response or cookies
                jwt_token = self._extract_jwt_token(response)

                if jwt_token:
                    self._jwt_token = jwt_token
                    self._authenticated = True

                    # Try to extract employee ID from token
                    self._extract_employee_id_from_jwt()

                    return AuthResult(success=True)

                # Check if 2FA is required
                if 'two-factor' in response.text.lower() or 'verification' in response.text.lower() or 'mfa' in response.url.lower():
                    logger.info("Morgan Stanley 2FA required")
                    return AuthResult(
                        success=False,
                        requires_2fa=True,
                        two_fa_type='app',
                        error_message="Two-factor authentication required. Please complete 2FA in your browser first."
                    )

                # Check for device registration page
                if 'device' in response.text.lower() and 'register' in response.text.lower():
                    logger.info("Morgan Stanley device registration required")
                    return AuthResult(
                        success=False,
                        requires_2fa=True,
                        two_fa_type='device',
                        error_message="Device registration required. Please complete registration in your browser first."
                    )

                # Check for login errors - look for specific error messages
                error_patterns = [
                    r'(invalid\s+(?:account|password|credentials))',
                    r'(incorrect\s+(?:account|password|credentials))',
                    r'(login\s+failed)',
                    r'(authentication\s+failed)',
                ]
                for pattern in error_patterns:
                    match = re.search(pattern, response.text, re.IGNORECASE)
                    if match:
                        logger.error(f"Morgan Stanley login error detected: {match.group(1)}")
                        logger.error(f"Morgan Stanley response snippet: {response.text[:1000]}")
                        return AuthResult(
                            success=False,
                            error_message=f"Login failed: {match.group(1)}"
                        )

                # If we got here but no JWT, login may have partially succeeded
                # Try to get JWT from a token endpoint
                jwt_token = self._try_get_jwt_from_session()
                if jwt_token:
                    self._jwt_token = jwt_token
                    self._extract_employee_id_from_jwt()
                    self._authenticated = True
                    logger.info("Morgan Stanley: Obtained JWT from session endpoint")
                    return AuthResult(success=True)

                # Try to access the dashboard to confirm login worked
                if self._verify_login():
                    self._authenticated = True
                    # Even without JWT, we might be able to use session cookies
                    logger.warning("Morgan Stanley: Login succeeded but no JWT token obtained. GraphQL calls may fail.")
                    return AuthResult(success=True)

                return AuthResult(
                    success=False,
                    error_message="Login appeared to succeed but session not established."
                )

            else:
                return AuthResult(
                    success=False,
                    error_message=f"Login failed with status {response.status_code}"
                )

        except requests.RequestException as e:
            logger.error(f"Login request failed: {e}")
            return AuthResult(
                success=False,
                error_message=f"Connection error: {str(e)}"
            )

    def _extract_jwt_token(self, response) -> Optional[str]:
        """Extract JWT token from response."""
        # Check cookies
        for cookie in self._session.cookies:
            logger.debug(f"Morgan Stanley cookie: {cookie.name}={cookie.value[:50] if len(cookie.value) > 50 else cookie.value}...")
            if 'jwt' in cookie.name.lower() or 'token' in cookie.name.lower() or 'auth' in cookie.name.lower():
                if cookie.value.startswith('eyJ'):  # JWT header
                    logger.info(f"Found JWT token in cookie: {cookie.name}")
                    return cookie.value

        # Check response headers
        auth_header = response.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            logger.info("Found JWT token in Authorization header")
            return auth_header[7:]
        elif auth_header.startswith('eyJ'):
            logger.info("Found JWT token in Authorization header (no Bearer prefix)")
            return auth_header

        # Check response body for token
        token_patterns = [
            r'"authorization":\s*"(eyJ[^"]+)"',
            r'"token":\s*"(eyJ[^"]+)"',
            r'"jwt":\s*"(eyJ[^"]+)"',
            r'authorization["\']:\s*["\']?(eyJ[^"\']+)',
            r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',  # Raw JWT pattern
        ]

        for pattern in token_patterns:
            match = re.search(pattern, response.text, re.IGNORECASE)
            if match:
                token = match.group(1) if match.lastindex else match.group(0)
                logger.info(f"Found JWT token in response body via pattern: {pattern[:30]}...")
                return token

        # Log a snippet of the response for debugging
        logger.warning(f"No JWT token found. Response snippet: {response.text[:500]}...")
        return None

    def _extract_employee_id_from_jwt(self):
        """Extract employee ID from JWT token payload."""
        if not self._jwt_token:
            return

        try:
            import base64
            import json

            # JWT format: header.payload.signature
            parts = self._jwt_token.split('.')
            if len(parts) >= 2:
                # Decode payload (add padding if needed)
                payload = parts[1]
                padding = 4 - len(payload) % 4
                if padding != 4:
                    payload += '=' * padding

                decoded = base64.urlsafe_b64decode(payload)
                data = json.loads(decoded)

                # Look for employee ID in common fields
                for field in ['sub', 'employeeId', 'employee_id', 'userId', 'user_id']:
                    if field in data:
                        self.employee_id = str(data[field])
                        break

        except Exception as e:
            logger.debug(f"Could not extract employee ID from JWT: {e}")

    def _try_get_jwt_from_session(self) -> Optional[str]:
        """Try to get JWT token from session/auth endpoints after login."""
        # List of potential endpoints that might return a JWT
        token_endpoints = [
            '/solium/servlet/mobileAuth.do',
            '/solium/api/auth/token',
            '/solium/api/session',
            '/solium/servlet/getToken.do',
            '/solium/servlet/apiToken.do',
            '/api/auth/token',
            '/api/v1/auth/token',
            '/oauth/token',
        ]

        for endpoint in token_endpoints:
            try:
                logger.debug(f"Trying token endpoint: {endpoint}")
                response = self._session.get(
                    f"{self.BASE_URL}{endpoint}",
                    timeout=10
                )
                logger.debug(f"Token endpoint {endpoint}: status={response.status_code}")
                if response.status_code == 200:
                    # Check for JWT in response
                    try:
                        data = response.json()
                        logger.debug(f"Token endpoint {endpoint} JSON keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
                        # Look for token in various fields
                        for field in ['token', 'jwt', 'authorization', 'access_token', 'accessToken', 'authToken', 'id_token']:
                            if field in data and str(data[field]).startswith('eyJ'):
                                logger.info(f"Found JWT in {endpoint} response field: {field}")
                                # Also extract employee ID if present
                                if not self.employee_id:
                                    for eid_field in ['employeeId', 'employee_id', 'userId', 'user_id', 'sub', 'participantId']:
                                        if eid_field in data:
                                            self.employee_id = str(data[eid_field])
                                            break
                                return data[field]
                    except Exception:
                        pass
                    # Check raw response for JWT pattern
                    match = re.search(r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', response.text)
                    if match:
                        logger.info(f"Found JWT in {endpoint} response body")
                        return match.group(0)
            except Exception as e:
                logger.debug(f"Failed to get JWT from {endpoint}: {e}")
                continue

        # Try POST to token endpoint (some require POST)
        try:
            response = self._session.post(
                f"{self.BASE_URL}/solium/api/auth/token",
                json={},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            logger.debug(f"POST /solium/api/auth/token: status={response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    for field in ['token', 'jwt', 'authorization', 'access_token', 'accessToken']:
                        if field in data and str(data[field]).startswith('eyJ'):
                            logger.info(f"Found JWT via POST token endpoint")
                            return data[field]
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"POST token endpoint failed: {e}")

        # Try the GWT module load - sometimes tokens are in bootstrap data
        try:
            response = self._session.get(
                f"{self.BASE_URL}/solium/participant/participant.nocache.js",
                timeout=10
            )
            if response.status_code == 200:
                # Look for bootstrap data or config with tokens
                match = re.search(r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', response.text)
                if match:
                    logger.info("Found JWT in GWT bootstrap")
                    return match.group(0)
        except Exception:
            pass

        # Try extracting from the dashboard page JavaScript/embedded data
        pages_to_search = []
        if hasattr(self, '_dashboard_page'):
            pages_to_search.append(('dashboard', self._dashboard_page))
        if hasattr(self, '_login_page'):
            pages_to_search.append(('login', self._login_page))

        for page_name, page in pages_to_search:
            # Look for JWT in script tags or data attributes
            patterns = [
                (r'authToken["\']?\s*[:=]\s*["\']?(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', 'authToken'),
                (r'token["\']?\s*[:=]\s*["\']?(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', 'token'),
                (r'jwt["\']?\s*[:=]\s*["\']?(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', 'jwt'),
                (r'authorization["\']?\s*[:=]\s*["\']?(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', 'authorization'),
                (r'Bearer\s+(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', 'Bearer'),
                (r'"accessToken"\s*:\s*"(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)"', 'accessToken'),
            ]
            for pattern, name in patterns:
                match = re.search(pattern, page, re.IGNORECASE)
                if match:
                    token = match.group(1)
                    logger.info(f"Found JWT in {page_name} page via {name} pattern")
                    return token

            # Also try to extract employee/participant ID
            if not self.employee_id:
                id_patterns = [
                    r'"participantId"\s*:\s*"?(\d+)"?',
                    r'"employeeId"\s*:\s*"?(\d+)"?',
                    r'"userId"\s*:\s*"?(\d+)"?',
                    r'"sub"\s*:\s*"?(\d+)"?',
                    r'participantId=(\d+)',
                ]
                for pattern in id_patterns:
                    match = re.search(pattern, page)
                    if match:
                        self.employee_id = match.group(1)
                        logger.info(f"Found employee ID in {page_name} page: {self.employee_id}")
                        break

        return None

    def _verify_login(self) -> bool:
        """Verify login by accessing a protected endpoint and extract data."""
        try:
            response = self._session.get(
                f"{self.BASE_URL}/solium/servlet/participantHome.do",
                timeout=30
            )
            # If we get redirected to login, we're not authenticated
            if 'userLogin' in response.url:
                return False

            # Store this page too for data extraction
            self._home_page = response.text
            logger.info(f"Morgan Stanley participantHome page length: {len(response.text)}")

            # Try to find account value or balance in the page
            value_patterns = [
                r'Total\s+Value[:\s]*\$?([\d,]+\.?\d*)',
                r'Portfolio\s+Value[:\s]*\$?([\d,]+\.?\d*)',
                r'Account\s+Value[:\s]*\$?([\d,]+\.?\d*)',
                r'Market\s+Value[:\s]*\$?([\d,]+\.?\d*)',
                r'class="[^"]*value[^"]*"[^>]*>\s*\$?([\d,]+\.?\d*)',
                r'availableValue["\s:]+(\d+\.?\d*)',
                r'"amount":\s*(\d+\.?\d*)',
            ]
            for pattern in value_patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    logger.info(f"Morgan Stanley found value via pattern: {match.group(0)[:100]}")

            # Try alternative endpoints that might return JSON
            json_endpoints = [
                '/solium/servlet/getParticipantSummary.do',
                '/solium/servlet/getAccountSummary.do',
                '/solium/api/participant/summary',
                '/solium/api/portfolio/summary',
            ]
            for endpoint in json_endpoints:
                try:
                    resp = self._session.get(f"{self.BASE_URL}{endpoint}", timeout=10)
                    logger.debug(f"Morgan Stanley {endpoint}: status={resp.status_code}, content-type={resp.headers.get('content-type', 'unknown')}")
                    if resp.status_code == 200:
                        content_type = resp.headers.get('content-type', '')
                        if 'json' in content_type:
                            logger.info(f"Morgan Stanley JSON endpoint found: {endpoint}")
                            try:
                                data = resp.json()
                                logger.info(f"Morgan Stanley JSON data keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
                                # Check for JWT or useful data
                                if isinstance(data, dict):
                                    for key in ['token', 'jwt', 'authorization', 'totalValue', 'portfolioValue', 'balance']:
                                        if key in data:
                                            logger.info(f"Morgan Stanley found {key}: {str(data[key])[:100]}")
                            except Exception:
                                pass
                except Exception as e:
                    logger.debug(f"Morgan Stanley endpoint {endpoint} failed: {e}")

            return True
        except Exception as e:
            logger.error(f"Morgan Stanley verify login failed: {e}")
            return False

    def complete_2fa(
        self,
        auth_code: Optional[str],
        session_data: Dict[str, Any]
    ) -> AuthResult:
        """
        Complete 2FA if required.

        Morgan Stanley uses various 2FA methods. This may need to be
        completed through the browser first.
        """
        return AuthResult(
            success=False,
            error_message="2FA must be completed through the Morgan Stanley website. "
                         "Please log in via browser first, then try syncing again."
        )

    def _graphql_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query."""
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Origin': self.BASE_URL,
            'Accept': 'application/json',
        }

        # JWT token without Bearer prefix (per actual browser request)
        if self._jwt_token:
            headers['authorization'] = self._jwt_token

        if self.employee_id:
            headers['employeeId'] = self.employee_id

        payload = {
            'operationName': None,
            'variables': variables or {},
            'query': query
        }

        logger.info(f"Morgan Stanley GraphQL query to {self.GRAPHQL_URL}")
        logger.debug(f"Morgan Stanley GraphQL headers: {list(headers.keys())}")
        logger.debug(f"Morgan Stanley GraphQL payload: {payload}")

        response = self._session.post(
            self.GRAPHQL_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        logger.info(f"Morgan Stanley GraphQL response: status={response.status_code}")
        if response.status_code != 200:
            logger.error(f"Morgan Stanley GraphQL error: {response.text[:500]}")

        response.raise_for_status()

        return response.json()

    def get_accounts(self) -> List[AccountInfo]:
        """Fetch list of accounts from Morgan Stanley."""
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        # For Morgan Stanley at Work, typically one account per employee
        accounts = [
            AccountInfo(
                identifier=self.account_number or self.employee_id or 'main',
                name='Morgan Stanley at Work',
                account_type='brokerage',
                currency='USD'
            )
        ]

        return accounts

    def get_balance(self, account_identifier: str) -> BalanceInfo:
        """
        Fetch account balance using GraphQL.

        Returns the total portfolio value (availableValue + unavailableValue).
        """
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        try:
            query = """
            query {
                portfolio {
                    availableValue {
                        amount
                        currency
                    }
                    unavailableValue {
                        amount
                        currency
                    }
                }
            }
            """

            data = self._graphql_query(query, {'cumulative': True})
            self._portfolio_data = data

            portfolio = data.get('data', {}).get('portfolio', {})

            available = portfolio.get('availableValue', {})
            unavailable = portfolio.get('unavailableValue', {})

            # Only count vested (available) value - unvested shares aren't truly owned yet
            available_amount = Decimal(str(available.get('amount', 0)))
            unavailable_amount = Decimal(str(unavailable.get('amount', 0)))

            currency = available.get('currency', 'USD') or unavailable.get('currency', 'USD')

            return BalanceInfo(
                balance=available_amount,  # Only vested/available value
                currency=currency,
                balance_date=date.today(),
                available_balance=available_amount,
                raw_data={
                    'vestedValue': float(available_amount),
                    'unvestedValue': float(unavailable_amount),
                    'currency': currency
                }
            )

        except requests.RequestException as e:
            logger.error(f"Failed to fetch balance: {e}")
            raise RuntimeError(f"Failed to fetch portfolio balance: {str(e)}")

    def get_positions(self, account_identifier: str) -> List[PositionInfo]:
        """
        Fetch portfolio positions using GraphQL.

        Fetches stock grants, options, and other holdings.
        """
        if not self._authenticated:
            result = self.authenticate()
            if not result.success:
                raise RuntimeError(result.error_message)

        positions = []

        try:
            # Query for holdings/grants
            query = """
            query {
                holdings {
                    symbol
                    name
                    quantity
                    currentPrice {
                        amount
                        currency
                    }
                    marketValue {
                        amount
                        currency
                    }
                    costBasis {
                        amount
                        currency
                    }
                    grantType
                    vestingStatus
                }
            }
            """

            data = self._graphql_query(query)
            holdings = data.get('data', {}).get('holdings', [])

            for holding in holdings:
                if holding:
                    positions.append(self._parse_holding(holding))

        except Exception as e:
            logger.warning(f"Failed to fetch positions via holdings query: {e}")

            # Try alternative query
            try:
                query = """
                query {
                    stockGrants {
                        symbol
                        grantName
                        vestedShares
                        unvestedShares
                        currentPrice
                        vestedValue
                        grantType
                    }
                }
                """

                data = self._graphql_query(query)
                grants = data.get('data', {}).get('stockGrants', [])

                for grant in grants:
                    if grant:
                        positions.append(self._parse_grant(grant))

            except Exception as e2:
                logger.warning(f"Failed to fetch positions via grants query: {e2}")

        return positions

    def _parse_holding(self, holding: Dict) -> PositionInfo:
        """Parse a holding into PositionInfo."""
        current_price = holding.get('currentPrice', {})
        market_value = holding.get('marketValue', {})
        cost_basis = holding.get('costBasis', {})

        quantity = holding.get('quantity', 0)
        price = current_price.get('amount', 0) if current_price else 0
        value = market_value.get('amount', 0) if market_value else 0
        cost = cost_basis.get('amount') if cost_basis else None

        # Determine asset class based on grant type
        grant_type = holding.get('grantType', '').upper()
        if 'OPTION' in grant_type:
            asset_class = 'equity'  # Stock options
        elif 'RSU' in grant_type or 'STOCK' in grant_type:
            asset_class = 'equity'
        else:
            asset_class = 'equity'

        return PositionInfo(
            symbol=holding.get('symbol', ''),
            name=holding.get('name', holding.get('grantName', '')),
            quantity=Decimal(str(quantity)),
            price_per_unit=Decimal(str(price)),
            market_value=Decimal(str(value)),
            currency=current_price.get('currency', 'USD') if current_price else 'USD',
            cost_basis=Decimal(str(cost)) if cost else None,
            asset_class=asset_class
        )

    def _parse_grant(self, grant: Dict) -> PositionInfo:
        """Parse a stock grant into PositionInfo."""
        vested = grant.get('vestedShares', 0)
        price = grant.get('currentPrice', 0)
        value = grant.get('vestedValue', 0)

        return PositionInfo(
            symbol=grant.get('symbol', ''),
            name=grant.get('grantName', ''),
            quantity=Decimal(str(vested)),
            price_per_unit=Decimal(str(price)),
            market_value=Decimal(str(value)),
            currency='USD',
            asset_class='equity'
        )

    def close(self):
        """Close the session."""
        if self._session:
            try:
                # Try to logout
                self._session.get(
                    f"{self.BASE_URL}/solium/servlet/userLogout.do",
                    timeout=10
                )
            except Exception:
                pass
            self._session.close()
            self._session = None
        self._authenticated = False
        self._jwt_token = None
        self._portfolio_data = None
