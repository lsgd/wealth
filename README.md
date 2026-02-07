# Wealth Tracker

A personal wealth tracking application that aggregates account balances from multiple financial institutions and provides portfolio analytics.

## Features

- **Multi-broker support**: Connect to German banks via FinTS (DKB, Commerzbank), Interactive Brokers, and other brokers
- **Automated sync**: Fetch account balances automatically with 2FA support
- **Currency conversion**: Automatic conversion to your base currency using Frankfurter API
- **Historical tracking**: Store balance snapshots over time for growth visualization
- **Portfolio breakdown**: View wealth by broker, currency, or account type
- **Secure credential storage**: Fernet encryption for stored credentials

## Project Structure

```
wealth/
├── backend/                 # Django REST API
│   ├── accounts/           # User profiles and authentication
│   ├── brokers/            # Broker definitions and integrations
│   │   └── integrations/   # FinTS, REST API implementations
│   ├── portfolio/          # Financial accounts and snapshots
│   ├── exchange_rates/     # Currency conversion service
│   └── core/               # Shared utilities (encryption)
├── frontend/               # React + TypeScript (Vite)
├── exchange-rates/         # Standalone exchange rate scripts
└── venv/                   # Python virtual environment
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (already installed)
pip install -r requirements.txt

# Navigate to backend
cd backend

# Run migrations
python manage.py migrate

# Load initial broker data
python manage.py loaddata initial_brokers

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Get current user |

### User Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile/` | Get user profile |
| PATCH | `/api/profile/` | Update profile (base currency, etc.) |

### Brokers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/brokers/` | List available brokers |
| GET | `/api/brokers/{code}/` | Get broker details |

### Financial Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/` | List user's accounts |
| POST | `/api/accounts/` | Create/link new account |
| GET | `/api/accounts/{id}/` | Get account details |
| PATCH | `/api/accounts/{id}/` | Update account |
| DELETE | `/api/accounts/{id}/` | Delete account |
| POST | `/api/accounts/{id}/sync/` | Trigger balance sync |
| POST | `/api/accounts/{id}/auth/` | Complete 2FA |

### Snapshots

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/{id}/snapshots/` | Get account history |
| POST | `/api/accounts/{id}/snapshots/` | Add manual snapshot |

### Wealth Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/wealth/summary/` | Current total wealth |
| GET | `/api/wealth/history/?days=30` | Historical timeline |
| GET | `/api/wealth/breakdown/?by=broker` | Breakdown by category |

### Exchange Rates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exchange-rates/?date=2024-01-01` | Get rates for date |
| POST | `/api/exchange-rates/sync/` | Fetch latest rates |

## Supported Brokers

| Broker | Status | Integration Type | Notes |
|--------|--------|------------------|-------|
| DKB | ✅ Active | FinTS | German bank, 2FA via app |
| Commerzbank | ✅ Active | FinTS | German bank, 2FA via app |
| Interactive Brokers | ✅ Active | REST | Flex Web Service (recommended) or Gateway, see [setup guide](docs/IBKR_SETUP.md) |
| Manual Entry | ✅ Active | - | For accounts without API |
| Morgan Stanley | ✅ Active | GraphQL | Employee stock plans (at Work), see [setup guide](docs/MORGANSTANLEY_SETUP.md) |
| True Wealth | ✅ Active | REST | Swiss robo-advisor, requires TOTP, see [setup guide](docs/TRUEWEALTH_SETUP.md) |
| VIAC | ✅ Active | REST | Swiss pension (Pillar 3a), see [setup guide](docs/VIAC_SETUP.md) |

## Usage Examples

### Register and Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "email": "user@example.com", "password": "securepass123", "password_confirm": "securepass123", "base_currency": "EUR"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "securepass123"}'
```

### Add a DKB Account

```bash
# Get JWT token first, then:
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DKB Girokonto",
    "broker_code": "dkb",
    "account_identifier": "DE89370400440532013000",
    "account_type": "checking",
    "currency": "EUR",
    "credentials": {
      "username": "your-dkb-username",
      "pin": "your-dkb-pin"
    }
  }'
```

### Sync Account Balance

```bash
# Initiate sync (may require 2FA)
curl -X POST http://localhost:8000/api/accounts/1/sync/ \
  -H "Authorization: Bearer <your-token>"

# If 2FA required, approve in banking app, then call again
# or for TAN-based auth:
curl -X POST http://localhost:8000/api/accounts/1/auth/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"auth_code": "123456"}'
```

### View Wealth Summary

```bash
curl http://localhost:8000/api/wealth/summary/ \
  -H "Authorization: Bearer <your-token>"
```

### Add an Interactive Brokers Account

IBKR supports two methods: Flex Web Service (recommended) or Client Portal Gateway. See [IBKR Setup Guide](docs/IBKR_SETUP.md) for detailed instructions.

**Using Flex Web Service (recommended):**
```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Interactive Brokers",
    "broker_code": "ibkr",
    "account_identifier": "U1234567",
    "account_type": "brokerage",
    "currency": "USD",
    "credentials": {
      "token": "your-flex-token",
      "query_id": "123456"
    }
  }'
```

**Using Client Portal Gateway:**
```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Interactive Brokers",
    "broker_code": "ibkr",
    "account_identifier": "U1234567",
    "account_type": "brokerage",
    "currency": "USD",
    "credentials": {
      "gateway_url": "https://localhost:5000"
    }
  }'
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, defaults to SQLite)
DATABASE_URL=postgres://user:pass@localhost/wealth

# Credential encryption key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
CREDENTIAL_ENCRYPTION_KEY=your-fernet-key-here

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Generate Encryption Key

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

## Development

### Running Tests

```bash
cd backend
python manage.py test
```

### Django Admin

Access the admin interface at `http://localhost:8000/admin/` after creating a superuser.

### Database

- **Development**: SQLite (default)
- **Production**: PostgreSQL recommended (set `DATABASE_URL`)

## Security Notes

- Credentials are encrypted using Fernet symmetric encryption
- JWT tokens expire after 60 minutes (refresh tokens last 7 days)
- Never commit `.env` files or credentials to version control
- The encryption key must be kept secure and backed up

## License

Private - All rights reserved
