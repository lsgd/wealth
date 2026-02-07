# True Wealth Integration Setup

This guide explains how to set up the True Wealth integration for the Wealth Tracker application.

## Overview

[True Wealth](https://www.truewealth.ch) is a Swiss robo-advisor offering low-cost ETF portfolios. This integration fetches your portfolio balance and positions using their web API.

## Requirements

- True Wealth account
- Two-factor authentication (TOTP) enabled on your account
- Authenticator app (Google Authenticator, Authy, 1Password, etc.)

## Important Notes

- **2FA Required**: True Wealth requires TOTP authentication for every login
- **Session-based**: Each sync requires providing a fresh TOTP code
- **No persistent token**: Unlike some brokers, True Wealth doesn't offer API tokens

## Step 1: Enable 2FA on Your Account

If you haven't already:

1. Log in to [True Wealth](https://app.truewealth.ch)
2. Go to **Settings** → **Security**
3. Enable **Two-Factor Authentication**
4. Scan the QR code with your authenticator app
5. Confirm with a code from your app

## Step 2: Find Your Portfolio ID (Optional)

The integration can auto-discover your portfolios, but if you have multiple portfolios and want to specify one:

1. Log in to True Wealth
2. Navigate to your portfolio
3. The URL will contain your portfolio ID: `https://app.truewealth.ch/app/portfolio/XXXXXX`
4. Note this number (e.g., `677155`)

## Step 3: Add True Wealth Account to Wealth Tracker

### Via API:

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "True Wealth",
    "broker_code": "truewealth",
    "account_identifier": "677155",
    "account_type": "brokerage",
    "currency": "CHF",
    "credentials": {
      "username": "your-email@example.com",
      "password": "your-password",
      "token": "123456"
    }
  }'
```

Replace:
- `677155` with your portfolio ID (or leave empty for auto-discovery)
- `your-email@example.com` with your True Wealth login email
- `your-password` with your password
- `123456` with a current TOTP code from your authenticator

### Via Frontend:

1. Navigate to **Accounts** → **Add Account**
2. Select **True Wealth** as the broker
3. Enter your login email
4. Enter your password
5. Enter a TOTP code from your authenticator
6. Optionally enter your portfolio ID
7. Click **Add Account**

## Step 4: Sync Your Account

Each sync requires a fresh TOTP code:

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/sync/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"token": "123456"}'
```

If the sync returns `pending_auth`, provide a new TOTP code:

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/auth/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"auth_code": "654321"}'
```

## What Data is Fetched

| Data | Description |
|------|-------------|
| **Net Value** | Total portfolio value |
| **Currency** | Portfolio currency (typically CHF) |
| **Positions** | Individual holdings (ETFs, cash) |
| **Cost Basis** | Original investment amount (if available) |

## Sync Frequency

Due to the TOTP requirement, automated background syncing is limited. Options:

1. **Manual sync**: Trigger sync manually when needed, providing a TOTP code
2. **TOTP automation**: If you have programmatic access to your TOTP secret, you can automate code generation

### Using TOTP Secret (Advanced)

If you have your TOTP secret (the key shown when setting up 2FA), you can store it:

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "True Wealth",
    "broker_code": "truewealth",
    "account_identifier": "677155",
    "account_type": "brokerage",
    "currency": "CHF",
    "credentials": {
      "username": "your-email@example.com",
      "password": "your-password",
      "totp_secret": "JBSWY3DPEHPK3PXP"
    }
  }'
```

**Security Warning**: Storing your TOTP secret reduces security. Only do this if you understand the risks.

## Troubleshooting

### "Invalid credentials or TOTP code"

- Verify your email and password are correct
- Ensure the TOTP code is current (not expired)
- Check that your system clock is accurate (TOTP is time-based)

### "Failed to initialize session"

- True Wealth may be experiencing issues
- Try again in a few minutes
- Check if you can log in via their website

### "Portfolio not found"

- Verify your portfolio ID is correct
- Try without specifying a portfolio ID (auto-discovery)

### Empty positions

- True Wealth may not expose detailed holdings via their API
- Balance (net value) should still be available

## Security Considerations

1. **Credentials are encrypted** at rest using Fernet encryption
2. **TOTP codes expire** after 30 seconds - syncs must be quick
3. **No API tokens** - username/password are required for each session
4. **HTTPS only** - all communication is encrypted in transit

## API Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `GET /api/public/authCheck` | Initialize session, get XSRF token |
| `POST /api/auth/login` | Authenticate with credentials + TOTP |
| `GET /api/portfolios` | List available portfolios |
| `GET /api/portfolios/{id}/performanceSummary` | Get portfolio net value |
| `GET /api/portfolios/{id}/holdings` | Get portfolio positions |

## Sources

- [True Wealth Website](https://www.truewealth.ch)
