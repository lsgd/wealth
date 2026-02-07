# VIAC Integration Setup

This guide explains how to set up the VIAC integration for the Wealth Tracker application.

## Overview

[VIAC](https://www.viac.ch) is a Swiss digital pension provider offering low-cost Pillar 3a (retirement savings) accounts. This integration fetches your portfolio balance and positions using their web API.

## Requirements

- VIAC account
- Login credentials (email and password)

## Important Notes

- **No 2FA for web login**: Unlike some other services, VIAC typically doesn't require 2FA for web-based authentication
- **Session-based**: Each sync creates a new session
- **CHF currency**: VIAC accounts are denominated in Swiss Francs

## Step 1: Get Your VIAC Credentials

Use your existing VIAC login credentials:
- Email address used to register
- Password

## Step 2: Add VIAC Account to Wealth Tracker

### Via API:

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "VIAC Pillar 3a",
    "broker_code": "viac",
    "account_type": "retirement",
    "currency": "CHF",
    "credentials": {
      "username": "your-email@example.com",
      "password": "your-password"
    }
  }'
```

Replace:
- `your-email@example.com` with your VIAC login email
- `your-password` with your password

### Via Frontend:

1. Navigate to **Accounts** → **Add Account**
2. Select **VIAC** as the broker
3. Enter your login email
4. Enter your password
5. Click **Add Account**

## Step 3: Sync Your Account

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/sync/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

The sync will fetch your current portfolio value and positions.

## What Data is Fetched

| Data | Description |
|------|-------------|
| **Total Value** | Current portfolio value |
| **Currency** | CHF (Swiss Francs) |
| **Positions** | Individual ETF holdings (if available) |
| **Asset Allocation** | Breakdown by asset class |

## Account Types

VIAC supports different types of Pillar 3a accounts:

- **VIAC Invest** - Investment-focused retirement savings
- **VIAC Savings** - Bank deposit-based retirement savings

The integration works with all VIAC account types.

## Investment Strategies

VIAC offers various investment strategies with different risk profiles:

| Strategy | Equity Allocation |
|----------|------------------|
| Global 20 | 20% stocks |
| Global 40 | 40% stocks |
| Global 60 | 60% stocks |
| Global 80 | 80% stocks |
| Global 100 | 100% stocks |

The integration fetches your actual holdings regardless of strategy.

## Sync Frequency

You can sync your VIAC account as often as needed. The balance reflects the most recent valuation available from VIAC.

## Troubleshooting

### "Invalid credentials"

- Verify your email and password are correct
- Try logging in via the VIAC website to confirm credentials work
- Check if your account is locked

### "Failed to initialize session"

- VIAC may be experiencing issues
- Try again in a few minutes
- Check if you can log in via their website

### "Access denied" or 2FA required

If VIAC has enabled 2FA for your account:
- The integration may not work until 2FA is completed
- Contact support if you need assistance

### Empty positions

- VIAC may not expose detailed holdings via their web API
- Balance (total value) should still be available
- Positions are extracted if the API provides them

## Security Considerations

1. **Credentials are encrypted** at rest using Fernet encryption
2. **No API tokens** - username/password are required for each session
3. **HTTPS only** - all communication is encrypted in transit
4. **Session cleanup** - sessions are closed after each sync

## Privacy Note

VIAC is regulated by FINMA (Swiss Financial Market Supervisory Authority) and follows Swiss banking secrecy laws. Your data remains protected under Swiss law.

## API Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `GET /` | Initialize session, get CSRF token |
| `POST /external-login/public/authentication/password/check/` | Authenticate |
| `GET /rest/web/wealth/summary` | Get portfolio value |
| `GET /rest/web/portfolio/{id}/positions` | Get holdings (if available) |

## Sources

- [VIAC Website](https://www.viac.ch)
- [VIAC App](https://app.viac.ch)
