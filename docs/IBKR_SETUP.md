# Interactive Brokers (IBKR) Integration Setup

This guide explains how to set up the Interactive Brokers integration for the Wealth Tracker application.

## Overview

The Wealth Tracker supports **two methods** for connecting to Interactive Brokers:

| Method | Best For | Data Freshness | Setup Complexity |
|--------|----------|----------------|------------------|
| **Flex Web Service** | Individual retail users | Daily (end of day) | Easy - just token + query ID |
| **Client Portal Gateway** | Real-time data needs | Real-time | Moderate - requires local gateway |

**Recommendation**: Most users should use the **Flex Web Service** method. It's simpler to set up and doesn't require running any local software.

---

## Method 1: Flex Web Service (Recommended)

The Flex Web Service allows you to fetch account data using a token and pre-configured query. Data is updated daily at market close.

### Requirements

- Any IBKR account (Pro or Lite)
- Flex Web Service access (enabled by default for most accounts)

### Step 1: Enable Flex Web Service

1. Log in to [IBKR Client Portal](https://www.interactivebrokers.com/portal)
2. Navigate to **Settings** → **Reporting** → **Flex Queries**
3. If not already enabled, click **Enable Flex Web Service**

### Step 2: Generate a Flex Token

1. In the Flex Queries section, find **Flex Web Service Token**
2. Click **Create** or **Regenerate**
3. Copy and save the token securely
4. Note: Tokens are valid for up to 1 year

### Step 3: Create a Flex Query

1. Click **Create** under Activity Flex Queries
2. Configure the query with these sections:

**Query Name**: `WealthTracker` (or any name you prefer)

**Date Period**: Last 7 Calendar Days (or your preference)

**Sections to Include**:
- ✅ Account Information
- ✅ Cash Report
- ✅ Open Positions
- ✅ Equity Summary (Net Asset Value)

**Delivery Configuration**:
- Format: XML
- Include header and trailer records: Yes

3. Save the query
4. Note the **Query ID** (visible in the query list)

### Step 4: Add IBKR Account to Wealth Tracker

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Interactive Brokers",
    "broker_code": "ibkr",
    "account_identifier": "U1234567",
    "account_type": "brokerage",
    "currency": "USD",
    "credentials": {
      "token": "your-flex-token-here",
      "query_id": "123456"
    }
  }'
```

Replace:
- `U1234567` with your IBKR account ID
- `your-flex-token-here` with your Flex token
- `123456` with your Query ID

### Step 5: Sync Your Account

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/sync/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

The sync will fetch your latest Flex report and update positions and balances.

### Flex Web Service Limitations

- Data is updated once daily at market close
- Reports may take a few seconds to generate
- Historical data limited to configured date range
- Token expires after 1 year (regenerate as needed)

### Troubleshooting Flex Web Service

**"Invalid token" error**:
- Token may have expired - regenerate in Client Portal
- Ensure you copied the full token without extra spaces

**"Invalid query" error**:
- Verify the Query ID is correct
- Ensure the query is an Activity Flex Query (not Trade Confirmation)

**Empty positions**:
- Check that "Open Positions" is enabled in your query
- Verify your account has positions

---

## Method 2: Client Portal Gateway

The Client Portal Gateway provides real-time data access but requires running a local Java application.

### Requirements

- **IBKR Pro account** (Lite accounts have limited API access)
- **Java Runtime**: Java 8 update 192+ or OpenJDK 11+
- **Client Portal Gateway**: Downloaded from IBKR

### Step 1: Download the Client Portal Gateway

1. Go to the [IBKR API Solutions page](https://www.interactivebrokers.com/en/trading/ib-api.php)
2. Scroll to "Client Portal API"
3. Click "Download Client Portal Gateway"
4. Extract the downloaded ZIP file

The extracted folder will contain:
```
clientportal/
├── bin/
│   └── run.sh (or run.bat on Windows)
├── root/
│   └── conf.yaml
└── ...
```

### Step 2: Configure the Gateway

Edit `root/conf.yaml`:

```yaml
# Listen port (default: 5000)
listenPort: 5000

# SSL configuration (recommended to keep enabled)
listenSsl: true

# IP whitelist
ips:
  allow:
    - 127.0.0.1
    - 0.0.0.0

# Account IDs (optional - leave empty to allow all)
accountIds: []
```

### Step 3: Start the Gateway

**macOS/Linux:**
```bash
cd clientportal
./bin/run.sh root/conf.yaml
```

**Windows:**
```cmd
cd clientportal
bin\run.bat root\conf.yaml
```

### Step 4: Authenticate

1. Open `https://localhost:5000` in your browser
2. Accept the self-signed certificate warning
3. Log in with your IBKR credentials
4. Complete 2FA (mobile app, SMS, or security device)
5. You'll see "Client login succeeds"

### Step 5: Add IBKR Account to Wealth Tracker

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer <your-jwt-token>" \
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

### Step 6: Sync Your Account

Ensure the gateway is running and authenticated, then:

```bash
curl -X POST http://localhost:8000/api/accounts/<account-id>/sync/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Session Management

- Sessions last up to **24 hours**
- Sessions timeout after **6 minutes** of inactivity
- Re-authenticate when session expires or gateway restarts

### Running Gateway as a Service

**macOS (launchd):**

Create `~/Library/LaunchAgents/com.ibkr.gateway.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ibkr.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/clientportal/bin/run.sh</string>
        <string>/path/to/clientportal/root/conf.yaml</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.ibkr.gateway.plist
```

**Linux (systemd):**

Create `/etc/systemd/system/ibkr-gateway.service`:
```ini
[Unit]
Description=IBKR Client Portal Gateway
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/clientportal
ExecStart=/path/to/clientportal/bin/run.sh /path/to/clientportal/root/conf.yaml
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable ibkr-gateway
sudo systemctl start ibkr-gateway
```

### Gateway Troubleshooting

**"Cannot connect to gateway"**:
```bash
curl -k https://localhost:5000/v1/api/iserver/auth/status
```

**"Not authenticated"**:
Open `https://localhost:5000` and log in again.

**Rate limiting**:
- Global: 10 requests/second
- Portfolio: 1 request/5 seconds
- Penalty box: 15 minutes if exceeded

---

## What Data is Fetched

Both methods fetch:

| Data | Description |
|------|-------------|
| **Net Liquidation Value** | Total account value |
| **Cash Balances** | Cash in each currency |
| **Positions** | Holdings with quantities and market values |
| **Cost Basis** | Original purchase cost (if available) |

### Supported Asset Types

- Stocks (STK)
- ETFs
- Options (OPT)
- Futures (FUT)
- Bonds (BOND)
- Mutual Funds (FUND)
- Crypto (if enabled)
- CFDs

---

## Security Considerations

1. **Flex Token**: Store securely - treat like a password
2. **Gateway**: Never expose to the internet - localhost only
3. **Credentials**: IBKR username/password are never stored by Wealth Tracker
4. **SSL**: Keep SSL enabled on the gateway

---

## API Reference

### Flex Web Service Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /SendRequest` | Request Flex report generation |
| `GET /GetStatement` | Retrieve generated report |

Base URL: `https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService`

### Client Portal Gateway Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /iserver/auth/status` | Check authentication status |
| `POST /tickle` | Keep session alive |
| `GET /portfolio/accounts` | List accounts |
| `GET /portfolio/{accountId}/ledger` | Get account balances |
| `GET /portfolio/{accountId}/positions/0` | Get positions |

---

## Sources

- [IBKR Flex Web Service Guide](https://www.interactivebrokers.com/campus/ibkr-api-page/flex-web-service/)
- [IBKR Trading API Solutions](https://www.interactivebrokers.com/en/trading/ib-api.php)
- [Client Portal API Documentation](https://interactivebrokers.github.io/cpwebapi/)
- [Web API v1.0 Documentation](https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/)
