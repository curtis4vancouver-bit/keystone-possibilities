import os
import sys
import json
import urllib.parse
import urllib.request
import webbrowser
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Reconfigure output to utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}/callback"
CLIENT_ID = "1004714315742024"
CLIENT_SECRET = "57ca3100e6a28799d666db6b20e1a8be"

callback_data = {}

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path.startswith("/callback"):
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            code = query_params.get("code", [None])[0]
            
            if code:
                callback_data["code"] = code
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
                        h1 { color: #c5a880; font-size: 24px; margin-top: 0; margin-bottom: 16px; font-weight: 600; }
                        p { font-size: 15px; color: #a0a0ab; line-height: 1.6; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Meta Authorization Captured</h1>
                        <p>Code received successfully! You can close this browser tab and return to the terminal.</p>
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

def run_local_server():
    server = HTTPServer(('0.0.0.0', PORT), OAuthCallbackHandler)
    server.serve_forever()

def load_tokens():
    token_path = "social_tokens.json"
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    token_path = "social_tokens.json"
    with open(token_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4)
    print(f"\n[OK] Tokens saved successfully to {token_path}")
    sys.stdout.flush()

def http_get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'KeystoneApp/2.0'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    print("=================================================================")
    print("       Keystone Recomposition Meta OAuth Re-authorization        ")
    print("=================================================================")
    print("1. Starts a local server at port 8080")
    print("2. Formulates the authorization URL with 'auth_type=rerequest'")
    print("3. Opens your default web browser to log in to Facebook")
    print("-----------------------------------------------------------------")
    print("🔑 CRITICAL ACTION DURING LOGIN FLOW:")
    print("Make sure to click 'Edit Settings' in the Facebook dialog and")
    print("actively check the 'Keystone Recomposition' Page and your Instagram")
    print("Business account. Ensure previously connected pages remain checked.")
    print("=================================================================\n")
    sys.stdout.flush()

    server_thread = threading.Thread(target=run_local_server)
    server_thread.start()
    
    scopes = "public_profile,instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement,pages_manage_posts"
    state = "meta_state_recomposition_" + str(int(time.time()))
    
    auth_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scopes,
        'response_type': 'code',
        'auth_type': 'rerequest'  # FORCES Meta to display the Page selection UI!
    }
    auth_url = "https://www.facebook.com/v20.0/dialog/oauth?" + urllib.parse.urlencode(auth_params)
    
    print("Starting secure authentication interceptor...")
    print(f"Opening authorization URL: {auth_url}\n")
    sys.stdout.flush()
    
    webbrowser.open(auth_url)
    
    # Wait for callback to complete and server to shut down
    server_thread.join()
    
    code = callback_data.get("code")
    if not code:
        print("\n❌ Error: No authorization code received.")
        sys.stdout.flush()
        return
        
    print("\n[OK] Received OAuth Authorization Code.")
    print("Exchanging code for short-lived user access token...")
    sys.stdout.flush()
    
    short_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&client_secret={CLIENT_SECRET}&code={code}"
    
    try:
        short_tokens = http_get_json(short_token_url)
        short_token = short_tokens["access_token"]
        
        print("[OK] Acquired short-lived access token.")
        print("Exchanging for long-lived access token (60-day lifespan)...")
        sys.stdout.flush()
        
        long_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&fb_exchange_token={short_token}"
        long_tokens = http_get_json(long_token_url)
        long_token = long_tokens["access_token"]
        
        print("[OK] Acquired long-lived access token.")
        
        # Save tokens under recomposition brand Meta key
        all_tokens = load_tokens()
        if "recomposition" not in all_tokens:
            all_tokens["recomposition"] = {}
        all_tokens["recomposition"]["meta"] = {
            "app_id": CLIENT_ID,
            "app_secret": CLIENT_SECRET,
            "user_access_token": long_token,
            "expires_in": long_tokens.get("expires_in", 5184000),
            "acquired_at": int(time.time())
        }
        
        save_tokens(all_tokens)
        
        # Immediate verification call
        print("\n========================================================")
        print("🔍 IMMEDIATE TOKEN PAGES VERIFICATION:")
        print("========================================================")
        sys.stdout.flush()
        
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={long_token}"
        pages_data = http_get_json(pages_url)
        pages = pages_data.get("data", [])
        
        print(f"Connected Pages found under the new token: {len(pages)}")
        for idx, p in enumerate(pages, 1):
            name = p.get("name")
            pid = p.get("id")
            print(f"  Page {idx}: '{name}' (ID: {pid})")
            
            # Check IG
            try:
                page_token = p["access_token"]
                ig_url = f"https://graph.facebook.com/v20.0/{pid}?fields=instagram_business_account&access_token={page_token}"
                ig_data = http_get_json(ig_url)
                ig_acct = ig_data.get("instagram_business_account", {})
                ig_id = ig_acct.get("id")
                print(f"    Linked Instagram Account ID: {ig_id}")
            except Exception as ig_err:
                print(f"    Failed to query Instagram: {str(ig_err)}")
        print("========================================================\n")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"\n❌ Error during Meta token exchange: {str(e)}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
