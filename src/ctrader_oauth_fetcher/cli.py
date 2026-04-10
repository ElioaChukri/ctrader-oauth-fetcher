import time
import argparse
import webbrowser
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
from urllib.request import urlopen
from urllib.error import HTTPError


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--client-id", required=True, help="Client ID used to authorize the application"
    )
    parser.add_argument(
        "--client-secret",
        required=True,
        help="Client Secret used to authorize the application",
    )
    parser.add_argument(
        "--scope",
        default="trading",
        help="The scope of the permissions to authorize for the application. Must be one of 'accounts' or 'trading'",
    )
    parser.add_argument(
        "--redirect-uri",
        default="http://localhost:8080",
        help="Redirect URI registered with your application. Defaults to http://localhost:8080",
    )
    args = parser.parse_args()

    if args.scope not in ["accounts", "trading"]:
        eprint("Invalid scope. Must be one of 'accounts' or 'trading'")
        sys.exit(1)

    auth_code = None
    auth_error = None

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal auth_code, auth_error
            params = parse_qs(urlparse(self.path).query)
            if "error" in params:
                auth_error = params["error"][0]
            elif "code" in params:
                auth_code = params["code"][0]
            else:
                auth_error = "No code or error returned in redirect"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization complete. You can close this tab.")

        def log_message(self, format: str, *args):
            pass

    auth_url = (
        f"https://id.ctrader.com/my/settings/openapi/grantingaccess/"
        f"?client_id={args.client_id}"
        f"&redirect_uri={args.redirect_uri}"
        f"&scope={args.scope}"
        f"&product=web"
    )

    parsed = urlparse(args.redirect_uri)
    host = parsed.hostname
    port = parsed.port or 80

    opened = webbrowser.open(auth_url)
    if not opened:
        print(f"Could not open browser. Visit this URL manually:\n{auth_url}")
    else:
        print("Browser opened. Complete the authorization in your browser.")

    print("Waiting for authorization...")
    HTTPServer((host, int(port)), Handler).handle_request()

    if auth_error:
        eprint(f"Authorization failed: {auth_error}")
        sys.exit(1)

    print("Authorization code received. Exchanging for tokens...")
    url_params = urlencode(
        {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": args.redirect_uri,
            "client_id": args.client_id,
            "client_secret": args.client_secret,
        }
    )

    try:
        with urlopen(
            f"https://openapi.ctrader.com/apps/token?{url_params}"
        ) as response:
            tokens = json.loads(response.read())
    except HTTPError as e:
        body = e.read().decode()
        eprint(f"Token exchange failed ({e.code}): {body}")
        sys.exit(1)

    expires_at = time.time() + tokens["expiresIn"]

    print("Tokens received successfully.\n")
    print(f"Access token:  {tokens['accessToken']}")
    print(f"Refresh token: {tokens['refreshToken']}")
    print(f"Expires in:    {tokens['expiresIn']} seconds")
    print(f"Expires at:    {int(expires_at)} (epoch time)")
