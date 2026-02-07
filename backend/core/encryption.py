import json
import os

from cryptography.fernet import Fernet
from django.conf import settings


def get_encryption_key() -> bytes:
    """Get the encryption key from settings or environment."""
    key = getattr(settings, 'CREDENTIAL_ENCRYPTION_KEY', None)
    if not key:
        key = os.environ.get('CREDENTIAL_ENCRYPTION_KEY')
    if not key:
        # Generate a key for development (not for production!)
        key = Fernet.generate_key()
        print("WARNING: Generated temporary encryption key. Set CREDENTIAL_ENCRYPTION_KEY in production.")
    if isinstance(key, str):
        key = key.encode()
    return key


def encrypt_credentials(data: dict) -> bytes:
    """Encrypt credentials dictionary to bytes."""
    f = Fernet(get_encryption_key())
    json_data = json.dumps(data).encode()
    return f.encrypt(json_data)


def decrypt_credentials(encrypted_data: bytes) -> dict:
    """Decrypt bytes to credentials dictionary."""
    if not encrypted_data:
        return {}
    f = Fernet(get_encryption_key())
    decrypted = f.decrypt(encrypted_data)
    return json.loads(decrypted.decode())
