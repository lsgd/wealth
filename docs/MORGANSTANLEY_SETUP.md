# Morgan Stanley Integration Setup

This guide explains how to set up the Morgan Stanley integration for the Wealth Tracker application.

## Overview

[Morgan Stanley at Work](https://atwork.morganstanley.com) is a platform for employee stock plans, equity compensation, and financial benefits. This integration fetches your portfolio value and stock holdings using their web API and GraphQL endpoints.

## Requirements

- Morgan Stanley at Work account (employee stock plan participant)
- Account number (participant ID)
- Password

## Important Notes

- **Employee Stock Plans**: This integration is designed for Morgan Stanley at Work, not regular Morgan Stanley brokerage accounts
- **2FA may be required**: Depending on your account settings, you may need to complete 2FA through the website first
- **Session-based**: Each sync creates a new authenticated session

## Supported Features

| Feature | Supported |
|---------|-----------|
| Portfolio Value | ✅ Yes |
| Available/Unvested Split | ✅ Yes |
| Stock Holdings | ✅ Yes |
| Stock Options | ✅ Yes |
| RSUs | ✅ Yes |
| ESPP | ✅ Yes |

## Step 1: Get Your Account Number

Your account number (participant ID) can be found:

1. On your Morgan Stanley at Work welcome page
2. In account statements
3. In the URL when logged in (often in the format of a numeric ID)

## Step 2: Add Morgan Stanley Account to Wealth Tracker

### Via API:

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morgan Stanley Stock Plan",
    "broker_code": "morganstanley",
    "account_type": "brokerage",
    "currency": "USD",
    "credentials": {
      "account_number": "12345678901",
      "password": "your-password"
    }
  }'
```

Replace:
- `12345678901` with your participant/account number
- `your-password` with your password

### Via Frontend:

1. Navigate to **Accounts** → **Add Account**
2. Select **Morgan Stanley** as the broker
3. Enter your account/participant number
4. Enter your password
5. Click **Add Account**

## Step 3: Complete 2FA (If Required)

If your account has 2FA enabled:

1. Log in to [Morgan Stanley at Work](https://atwork.morganstanley.com) in your browser
2. Complete the 2FA verification
3. Keep the session active
4. Run the sync in Wealth Tracker

The integration will attempt to use the authenticated session.

## Step 4: Sync Your Account

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/sync/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

## What Data is Fetched

| Data | Description |
|------|-------------|
| **Available Value** | Vested shares that can be sold |
| **Unavailable Value** | Unvested shares (RSUs, options not yet exercisable) |
| **Total Value** | Combined portfolio value |
| **Holdings** | Individual stock grants and positions |
| **Currency** | USD (Morgan Stanley accounts are typically in USD) |

## Understanding Your Portfolio

### Available vs Unavailable Value

- **Available Value**: Shares you can sell immediately (vested RSUs, exercised options)
- **Unavailable Value**: Shares subject to vesting schedules

### Grant Types

| Type | Description |
|------|-------------|
| RSU | Restricted Stock Units - shares granted that vest over time |
| Stock Options | Right to purchase shares at a set price |
| ESPP | Employee Stock Purchase Plan shares |
| Performance Shares | Shares tied to performance metrics |

## Troubleshooting

### "Invalid account number or password"

- Verify your account number is correct
- Ensure you're using the right password
- Try logging in via the website to confirm credentials

### "Two-factor authentication required"

- Log in to Morgan Stanley at Work in your browser
- Complete the 2FA verification
- Try syncing again while the browser session is active

### "Login appeared to succeed but session not established"

- The site may have changed its authentication flow
- Try logging in via browser first, then sync
- Clear cookies and try again

### Empty positions

- Your account may not have any stock grants yet
- Check the website to verify your holdings
- The GraphQL query may need adjustment for your specific plan

## Security Considerations

1. **Credentials are encrypted** at rest using Fernet encryption
2. **JWT tokens** are extracted for API calls but not persisted
3. **HTTPS only** - all communication is encrypted in transit
4. **Session cleanup** - sessions are closed after each sync

## Technical Details

### Authentication Flow

1. GET `/solium/servlet/userLogin.do` - Fetch login page and cookies
2. POST `/solium/servlet/userLogin.do` - Submit credentials
3. Extract JWT token from response
4. Use token for GraphQL API calls

### GraphQL API

The integration uses Morgan Stanley's GraphQL endpoint at `/graphql` with queries like:

```graphql
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
```

## API Endpoints Used

| Endpoint | Description |
|----------|-------------|
| `GET /solium/servlet/userLogin.do` | Login page, cookies |
| `POST /solium/servlet/userLogin.do` | Authentication |
| `POST /graphql` | Portfolio and holdings data |
| `GET /solium/servlet/userLogout.do` | Logout |

## Sources

- [Morgan Stanley at Work](https://atwork.morganstanley.com)
