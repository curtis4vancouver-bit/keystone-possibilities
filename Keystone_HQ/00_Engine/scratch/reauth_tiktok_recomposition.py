import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PARENT_DIR)
import json
import urllib.parse
import urllib.request
import webbrowser
import threading
import time
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

# Reconfigure output to utf-8
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8080
callback_data = {}

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path.startswith("/callback"):
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            code = query_params.get("code", [None])[0]
            state = query_params.get("state", [None])[0]
            
            if code:
                callback_data["code"] = code
                callback_data["state"] = state
                
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>TikTok Auth Success</title>
                    <style>
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                            background-color: #0c0c0e;
                            color: #e0e0e4;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }
                        .container {
                            text-align: center;
                            background-color: #141417;
                            padding: 50px 40px;
                            border-radius: 16px;
                            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
                            border: 1px solid #c5a880;
                            max-width: 480px;
                        }
                        h1 { color: #c5a880; font-size: 24px; margin-top: 0; margin-bottom: 16px; font-weight: 600; letter-spacing: 0.5px; }
                        p { font-size: 15px; line-height: 1.6; color: #a0a0ab; margin-bottom: 24px; }
                        .success-badge {
                            background-color: rgba(197, 168, 128, 0.1);
                            color: #c5a880;
                            padding: 6px 14px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 700;
                            letter-spacing: 1.5px;
                            display: inline-block;
                            margin-bottom: 20px;
                            border: 1px solid rgba(197, 168, 128, 0.3);
                            text-transform: uppercase;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="success-badge">Authorization Intercepted</div>
                        <h1>TikTok Content Engine</h1>
                        <p>Your secure TikTok authorization code has been successfully captured!</p>
                        <p>You can safely close this browser window now.</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authorization failed: No secure callback code found.")
            
            threading.Thread(target=lambda: self.server.shutdown()).start()
        else:
            self.send_response(404)
            self.end_headers()

def run_local_server(use_ssl=False):
    server = HTTPServer(('0.0.0.0', PORT), OAuthCallbackHandler)
    if use_ssl:
        cert_path = "cert.pem"
        key_path = "key.pem"
        # Since cryptography might not be in stdlib, let's look for dynamic self-signed cert creation
        from social_oauth_manager import generate_self_signed_cert
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            generate_self_signed_cert(cert_path, key_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        server.socket = context.wrap_socket(server.socket, server_side=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()

def http_post_form(url, payload):
    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'KeystoneApp/2.0'}
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        sys.stdout.write("ERROR: social_tokens.json not found.\n")
        return
        
    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    tiktok = tokens.get("recomposition", {}).get("tiktok", {})
    client_key = tiktok.get("client_key")
    client_secret = tiktok.get("client_secret")
    
    if not client_key or not client_secret:
        sys.stdout.write("ERROR: TikTok client_key or client_secret not found in social_tokens.json.\n")
        return
        
    sys.stdout.write("Loaded TikTok App Credentials from social_tokens.json.\n")
    sys.stdout.write("Preparing TikTok authorization with 'video.publish' scope.\n\n")
    
    # We will use localtest.me HTTPS because TikTok requires HTTPS redirect URIs in production
    redirect_uri = f"https://localtest.me:{PORT}/callback"
    scopes = "user.info.basic,video.upload,video.publish"
    state = "tiktok_state_recomposition_" + str(int(time.time()))
    
    auth_params = {
        'client_key': client_key,
        'scope': scopes,
        'redirect_uri': redirect_uri,
        'state': state,
        'response_type': 'code'
    }
    auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(auth_params)
    
    sys.stdout.write(f"Starting secure local redirect server at https://localtest.me:8080/callback...\n")
    sys.stdout.write("Note: If you see a 'Connection not private' warning in your browser,\n")
    sys.stdout.write("click 'Advanced' and choose 'Proceed to localtest.me (unsafe)'.\n\n")
    
    callback_data.clear()
    server_thread = threading.Thread(target=lambda: run_local_server(use_ssl=True))
    server_thread.start()
    
    sys.stdout.write(f"AUTH_URL: {auth_url}\n")
    sys.stdout.write("Opening browser authorization page...\n")
    webbrowser.open(auth_url)
    
    server_thread.join()
    
    # Clean up certs
    for temp_file in ["cert.pem", "key.pem"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
                
    code = callback_data.get("code")
    if not code:
        sys.stdout.write("ERROR: Authorization code not retrieved.\n")
        return
        
    sys.stdout.write("\nExchanging Authorization Code for fresh Access Tokens...\n")
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        'client_key': client_key,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    
    try:
        resp = http_post_form(token_url, payload)
        
        tiktok["access_token"] = resp["access_token"]
        tiktok["refresh_token"] = resp.get("refresh_token", tiktok.get("refresh_token"))
        tiktok["expires_in"] = resp.get("expires_in", 86400)
        tiktok["refresh_expires_in"] = resp.get("refresh_expires_in", 31536000)
        tiktok["acquired_at"] = int(time.time())
        
        tokens["recomposition"]["tiktok"] = tiktok
        
        with open(tokens_file, "w", encoding="utf-8") as f:
            json.dump(tokens, f, indent=4)
            
        sys.stdout.write("\nSUCCESS: TikTok credentials updated with 'video.publish' scope!\n")
    except Exception as e:
        sys.stdout.write(f"\nERROR during TikTok token exchange: {str(e)}\n")

if __name__ == "__main__":
    main()
