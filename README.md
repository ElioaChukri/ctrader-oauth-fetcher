# ctrader-oauth-fetcher

A command-line utility for obtaining OAuth tokens from the cTrader Open API. This tool automates the OAuth 2.0 authorization code flow, handling browser-based authorization and token exchange.

## Requirements

- Python 3.14+
- A cTrader Open API application (client ID and secret)

## Usage

Run directly without installation using uvx:

```bash
uvx ctrader-oauth-fetcher --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

With all options:

```bash
ctrader-oauth-fetcher \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --scope trading \
  --redirect-uri http://localhost:8080
```

### Options

| Option            | Required | Default                 | Description                               |
|-------------------|----------|-------------------------|-------------------------------------------|
| `--client-id`     | Yes      | -                       | OAuth application client ID               |
| `--client-secret` | Yes      | -                       | OAuth application client secret           |
| `--scope`         | No       | `trading`               | Permission scope: `trading` or `accounts` |
| `--redirect-uri`  | No       | `http://localhost:8080` | OAuth callback URL                        |

### Scopes

- `trading` - Full trading permissions (place orders, manage positions)
- `accounts` - Read-only access to account information

## How It Works

1. The tool constructs an authorization URL and opens it in your default browser
2. A local HTTP server starts to listen for the OAuth callback
3. After you authorize the application in your browser, cTrader redirects back to the local server
4. The tool exchanges the authorization code for access and refresh tokens
5. Tokens are displayed in the terminal

## Output

On success, the tool outputs the token response:

```
Tokens received successfully.

Access token:  <TOKEN>
Refresh token: <TOKEN>
Expires in:    <SECONDS> seconds
Expires at:    <UNIX-EPOCH> (epoch time)
```

## Getting cTrader API Credentials

1. Go to [cTrader Open API](https://openapi.ctrader.com/)
2. Register or log in to your account
3. Create a new application
4. Note your client ID and client secret

## License

MIT License - see [LICENSE](LICENSE) for details.