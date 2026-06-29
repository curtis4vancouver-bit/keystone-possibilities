import os
import sys
import json
import urllib.parse
import urllib.request
import webbrowser
import threading
import time
import ssl
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Reconfigure output to utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}/callback"
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
                    <title>Keystone Auth Success</title>
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
                        <h1>Keystone Content Engine</h1>
                        <p>Your Recomposition Meta authorization code has been successfully captured!</p>
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

def run_local_server():
    server = HTTPServer(('0.0.0.0', PORT), OAuthCallbackHandler)
    try:
        server.serve_forever()
    finally:
        server.server_close()

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        print("ERROR: social_tokens.json not found.")
        return

    with open(tokens_file, "r") as f:
        tokens = json.load(f)

    meta_possibilities = tokens.get("possibilities", {}).get("meta", {})
    client_id = meta_possibilities.get("app_id")
    client_secret = meta_possibilities.get("app_secret")

    if not client_id or not client_secret:
        print("ERROR: App ID or App Secret not found in possibilities meta config.")
        return

    print("Loaded App Credentials from social_tokens.json.")
    print("Preparing Meta authorization specifically for 'recomposition' brand context.")
    
    scopes = "public_profile,instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement,pages_manage_posts"
    state = "meta_state_recomposition_" + str(int(time.time()))
    
    auth_params = {
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scopes,
        'response_type': 'code'
    }
    auth_url = "https://www.facebook.com/v20.0/dialog/oauth?" + urllib.parse.urlencode(auth_params)
    
    print("\nStarting local authentication server...")
    callback_data.clear()
    server_thread = threading.Thread(target=run_local_server)
    server_thread.start()
    
    print("Opening browser authorization page...")
    print(f"AUTH_URL: {auth_url}")
    print("Please make sure to select both 'Keystone Recomposition' and your Instagram account!")
    webbrowser.open(auth_url)
    
    server_thread.join()
    
    code = callback_data.get("code")
    if not code:
        print("ERROR: Authorization code not retrieved.")
        return
        
    print("\nExchanging code for Short-Lived Access Token...")
    short_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={client_id}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&client_secret={client_secret}&code={code}"
    
    try:
        req = urllib.request.Request(short_token_url)
        with urllib.request.urlopen(req) as res:
            short_tokens = json.loads(res.read().decode('utf-8'))
            
        short_token = short_tokens["access_token"]
        
        print("Exchanging for Long-Lived Access Token (60-day lifespan)...")
        long_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={short_token}"
        
        long_req = urllib.request.Request(long_token_url)
        with urllib.request.urlopen(long_req) as res:
            long_tokens = json.loads(res.read().decode('utf-8'))
            
        long_token = long_tokens["access_token"]
        
        # Save tokens
        tokens["recomposition"]["meta"] = {
            "app_id": client_id,
            "app_secret": client_secret,
            "user_access_token": long_token,
            "expires_in": long_tokens.get("expires_in", 5184000),
            "acquired_at": int(time.time())
        }
        
        with open(tokens_file, "w") as f:
            json.dump(tokens, f, indent=4)
            
        print("\nSUCCESS: Recomposition Meta credentials saved to social_tokens.json!")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
