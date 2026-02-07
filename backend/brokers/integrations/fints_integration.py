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

# FinTS/HBCI error code translations
FINTS_ERROR_MESSAGES = {
    '900': 'Invalid TAN code. Please check and try again.',
    '9000': 'Invalid TAN code. Please check and try again.',
    '9010': 'TAN has expired. Please restart the authentication process.',
    '9050': 'TAN mechanism is locked. Please contact your bank.',
    '9210': 'Invalid credentials. Please check your username and PIN.',
    '9800': 'Dialog initialization failed. Please try again.',
    '9900': 'Authentication failed. Please check your credentials.',
    '9910': 'Session expired. Please restart the authentication process.',
    '9920': 'Too many failed attempts. Please try again later.',
    '9930': 'Account locked. Please contact your bank.',
    '9931': 'PIN locked. Please contact your bank.',
    '9941': 'TAN required but not provided.',
    '9942': 'Invalid TAN format.',
}


def _translate_fints_error(error: Exception) -> str:
    """Translate FinTS error codes to user-friendly messages."""
    error_str = str(error).strip()

    # Check if it's a pure error code (just digits)
    if error_str.isdigit():
        return FINTS_ERROR_MESSAGES.get(error_str, f'Bank error ({error_str}). Please try again.')

    # Check if error contains a known code
    for code, message in FINTS_ERROR_MESSAGES.items():
        if code in error_str:
            return message

    # Return original error if no translation found, but clean it up
    if len(error_str) < 100:
        return f'Bank error: {error_str}'
    return 'An error occurred during authentication. Please try again.'


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

            # Log all available mechanisms with details
            logger.warning(f"FinTS: Available TAN mechanisms: {mechs}")
            if isinstance(mechs, dict):
                for key, mech in mechs.items():
                    mech_name = getattr(mech, 'name', 'unknown') if hasattr(mech, 'name') else str(mech)
                    is_decoupled = getattr(mech, 'decoupled', False) if hasattr(mech, 'decoupled') else False
                    logger.warning(f"FinTS: Mechanism {key}: {mech_name}, decoupled={is_decoupled}")

            # Build list of mechanism keys
            mech_keys = list(mechs.keys()) if isinstance(mechs, dict) else [str(m) for m in mechs]

            # Prefer decoupled TAN mechanisms (push notification, no manual entry needed)
            # Common decoupled TAN mechanism IDs: 940 (PushTAN), 942, 944
            selected_mechanism = None
            for preferred in ['940', '942', '944', '920', '921']:
                if preferred in mech_keys:
                    selected_mechanism = preferred
                    break

            if selected_mechanism:
                logger.warning(f"FinTS: Selecting decoupled TAN mechanism: {selected_mechanism}")
                self._client.set_tan_mechanism(selected_mechanism)
            elif mech_keys:
                # Fallback to first available mechanism
                selected_mechanism = mech_keys[0]
                logger.warning(f"FinTS: No decoupled TAN found, using first mechanism: {selected_mechanism}")
                self._client.set_tan_mechanism(selected_mechanism)

            # Start the session
            self._client.__enter__()

            # Check if 2FA is required
            if isinstance(self._client.init_tan_response, NeedTANResponse):
                tan_resp = self._client.init_tan_response

                # Log all attributes of the TAN response for debugging
                tan_attrs = [attr for attr in dir(tan_resp) if not attr.startswith('_')]
                logger.warning(f"FinTS: TAN response attributes: {tan_attrs}")

                # Check decoupled status
                is_decoupled = getattr(tan_resp, 'decoupled', False)
                challenge_text = getattr(tan_resp, 'challenge', None)

                logger.warning(f"FinTS: TAN response - decoupled={is_decoupled}, challenge={challenge_text[:100] if challenge_text else None}")

                # Also check if the selected mechanism is typically decoupled
                # Mechanisms 940, 942, 944 are usually decoupled (PushTAN)
                if selected_mechanism in ['940', '942', '944']:
                    logger.warning(f"FinTS: Selected mechanism {selected_mechanism} is typically decoupled, forcing decoupled=True")
                    is_decoupled = True

                if is_decoupled:
                    # Poll for app approval (decoupled TAN) — up to 5 minutes
                    logger.info("Waiting for banking app approval...")
                    max_attempts = 60  # 5 min at 5s intervals
                    for attempt in range(max_attempts):
                        result = self._client.send_tan(tan_resp, None)
                        if not isinstance(result, NeedTANResponse):
                            self._authenticated = True
                            logger.info("App approval received.")
                            return AuthResult(success=True)
                        tan_resp = result
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

                    # Extract all available challenge data
                    challenge_text = getattr(tan_resp, 'challenge', None)
                    challenge_html = getattr(tan_resp, 'challenge_html', None)

                    # For photoTAN/chipTAN, the image data can be in various attributes
                    challenge_hhduc = getattr(tan_resp, 'challenge_hhduc', None)
                    challenge_matrix = getattr(tan_resp, 'challenge_matrix', None)
                    challenge_raw = getattr(tan_resp, 'challenge_raw', None)

                    logger.warning(f"TAN challenge - text: {bool(challenge_text)}, html: {bool(challenge_html)}, hhduc: {bool(challenge_hhduc)}, matrix: {bool(challenge_matrix)}, raw: {bool(challenge_raw)}")

                    # If we have matrix data (photoTAN image), convert to displayable format
                    if challenge_matrix:
                        import base64
                        logger.warning(f"PhotoTAN: challenge_matrix type={type(challenge_matrix)}, len={len(challenge_matrix) if hasattr(challenge_matrix, '__len__') else 'N/A'}")

                        # Extract image data - challenge_matrix can be:
                        # - bytes: raw image data
                        # - str: base64 encoded
                        # - tuple: (mime_type, image_data)
                        img_data = None
                        mime_type = 'image/png'

                        if isinstance(challenge_matrix, tuple) and len(challenge_matrix) >= 2:
                            # Tuple format: (mime_type, image_data)
                            mime_type = challenge_matrix[0] or 'image/png'
                            img_data = challenge_matrix[1]
                            logger.warning(f"PhotoTAN: tuple format - mime={mime_type}, data_type={type(img_data)}")
                        elif isinstance(challenge_matrix, bytes):
                            img_data = challenge_matrix
                        elif isinstance(challenge_matrix, str):
                            # Already base64 encoded
                            img_base64 = challenge_matrix
                            challenge_html = f'<div class="phototan-challenge"><p>{challenge_text or "Scan this code with your banking app:"}</p><img src="data:image/png;base64,{img_base64}" alt="PhotoTAN" style="max-width: 250px; margin: 10px auto; display: block;" /></div>'
                            logger.warning("PhotoTAN: Using challenge_matrix image (string)")
                            img_data = None  # Already handled

                        # Convert bytes to base64 if we have raw data
                        if img_data is not None:
                            if isinstance(img_data, bytes):
                                img_base64 = base64.b64encode(img_data).decode('utf-8')
                                challenge_html = f'<div class="phototan-challenge"><p>{challenge_text or "Scan this code with your banking app:"}</p><img src="data:{mime_type};base64,{img_base64}" alt="PhotoTAN" style="max-width: 250px; margin: 10px auto; display: block;" /></div>'
                                logger.warning(f"PhotoTAN: Using challenge_matrix image (bytes, {len(img_data)} bytes)")
                            elif isinstance(img_data, str):
                                # img_data is already base64
                                challenge_html = f'<div class="phototan-challenge"><p>{challenge_text or "Scan this code with your banking app:"}</p><img src="data:{mime_type};base64,{img_data}" alt="PhotoTAN" style="max-width: 250px; margin: 10px auto; display: block;" /></div>'
                                logger.warning("PhotoTAN: Using challenge_matrix image (string from tuple)")

                    # Fallback to HHD UC data if no matrix
                    elif challenge_hhduc:
                        # HHD UC is typically used for flicker code TAN generators
                        challenge_html = f'<div class="phototan-challenge"><p>{challenge_text or "Use your TAN generator:"}</p><p class="form-hint">HHD UC Code: {challenge_hhduc}</p></div>'
                        logger.warning("PhotoTAN: Using challenge_hhduc data")

                    return AuthResult(
                        success=False,
                        requires_2fa=True,
                        two_fa_type='tan',
                        session_data={'decoupled': False},
                        challenge_data={
                            'challenge': challenge_text,
                            'challenge_html': challenge_html,
                            'challenge_hhduc': challenge_hhduc,
                            'challenge_matrix': bool(challenge_matrix),  # Just indicate if present
                        }
                    )

            self._authenticated = True
            return AuthResult(success=True)

        except Exception as e:
            logger.exception("FinTS authentication failed")
            return AuthResult(
                success=False,
                error_message=_translate_fints_error(e)
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
                error_message=_translate_fints_error(e)
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
