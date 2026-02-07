# Wealth Tracker Backend

Django REST Framework backend for the Wealth Tracker application.

## Architecture

### Apps

#### `accounts`
User authentication and profiles.

- **Models**: `UserProfile`
- **Endpoints**: `/api/auth/*`, `/api/profile/`

#### `brokers`
Broker definitions and integrations.

- **Models**: `Broker`
- **Endpoints**: `/api/brokers/`
- **Integrations**: `brokers/integrations/`

#### `portfolio`
Financial accounts, snapshots, and positions.

- **Models**: `FinancialAccount`, `AccountSnapshot`, `PortfolioPosition`
- **Endpoints**: `/api/accounts/`, `/api/wealth/*`

#### `exchange_rates`
Currency conversion service.

- **Models**: `ExchangeRate`
- **Endpoints**: `/api/exchange-rates/`
- **Service**: Frankfurter API integration

### Core Utilities

#### `core/encryption.py`
Fernet-based encryption for storing broker credentials securely.

```python
from core.encryption import encrypt_credentials, decrypt_credentials

# Encrypt
encrypted = encrypt_credentials({'username': 'user', 'pin': '1234'})

# Decrypt
credentials = decrypt_credentials(encrypted)
```

## Data Models

### UserProfile
```python
user: User (OneToOne)
base_currency: str  # EUR, USD, CHF, GBP
auto_sync_enabled: bool
sync_frequency_hours: int
```

### Broker
```python
code: str           # dkb, commerzbank, etc.
name: str
integration_type: str  # fints, rest, graphql
bank_identifier: str   # BLZ for German banks
fints_server: str
api_base_url: str
credential_schema: dict  # JSON schema for required credentials
```

### FinancialAccount
```python
user: User
broker: Broker
name: str
account_identifier: str  # IBAN or account number
account_type: str        # checking, savings, brokerage, retirement
currency: str
encrypted_credentials: bytes
status: str              # active, inactive, error, pending_auth
is_manual: bool
```

### AccountSnapshot
```python
account: FinancialAccount
balance: Decimal
currency: str
balance_base_currency: Decimal  # Converted amount
exchange_rate_used: Decimal
snapshot_date: date
snapshot_source: str  # auto, manual, import
raw_data: dict        # Full broker response
```

### PortfolioPosition
```python
snapshot: AccountSnapshot
symbol: str
isin: str
name: str
quantity: Decimal
price_per_unit: Decimal
market_value: Decimal
currency: str
cost_basis: Decimal
asset_class: str  # equity, fixed_income, cash, etc.
```

### ExchangeRate
```python
from_currency: str
to_currency: str
rate: Decimal
rate_date: date
source: str  # frankfurter
```

## Broker Integrations

### Base Interface

All broker integrations implement `BrokerIntegrationBase`:

```python
class BrokerIntegrationBase(ABC):
    def authenticate(self) -> AuthResult
    def complete_2fa(self, auth_code, session_data) -> AuthResult
    def get_accounts(self) -> List[AccountInfo]
    def get_balance(self, account_identifier) -> BalanceInfo
    def get_positions(self, account_identifier) -> List[PositionInfo]
    def close()
```

### FinTS Integration

For German banks (DKB, Commerzbank):

```python
from brokers.integrations import get_broker_integration

integration = get_broker_integration(broker, credentials)
auth_result = integration.authenticate()

if auth_result.requires_2fa:
    # Wait for app approval or get TAN
    auth_result = integration.complete_2fa(tan_code, session_data)

accounts = integration.get_accounts()
balance = integration.get_balance(account.iban)
integration.close()
```

### Adding New Brokers

1. Create integration class in `brokers/integrations/`:

```python
# brokers/integrations/new_broker.py
from .base import BrokerIntegrationBase, AuthResult, AccountInfo, BalanceInfo

class NewBrokerIntegration(BrokerIntegrationBase):
    def authenticate(self) -> AuthResult:
        # Implement authentication
        pass

    def complete_2fa(self, auth_code, session_data) -> AuthResult:
        # Implement 2FA if needed
        pass

    def get_accounts(self) -> List[AccountInfo]:
        # Fetch account list
        pass

    def get_balance(self, account_identifier) -> BalanceInfo:
        # Fetch balance
        pass
```

2. Register in factory (`brokers/integrations/__init__.py`):

```python
def get_broker_integration(broker, credentials):
    if broker.code == 'new_broker':
        from .new_broker import NewBrokerIntegration
        return NewBrokerIntegration(credentials)
```

3. Add broker fixture in `brokers/fixtures/initial_brokers.json`

4. Load fixture: `python manage.py loaddata initial_brokers`

## API Authentication

Uses JWT (JSON Web Tokens) via `djangorestframework-simplejwt`.

```bash
# Get tokens
POST /api/auth/login/
{"username": "user", "password": "pass"}
# Returns: {"access": "...", "refresh": "..."}

# Use access token
GET /api/accounts/
Authorization: Bearer <access_token>

# Refresh token
POST /api/auth/refresh/
{"refresh": "<refresh_token>"}
```

## Management Commands

```bash
# Run migrations
python manage.py migrate

# Load broker fixtures
python manage.py loaddata initial_brokers

# Create superuser
python manage.py createsuperuser

# Shell with auto-imports
python manage.py shell

# Check for issues
python manage.py check
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test brokers
python manage.py test portfolio

# With coverage
coverage run manage.py test
coverage report
```
