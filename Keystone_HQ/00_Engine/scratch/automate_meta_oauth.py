import os
import json
import urllib.parse
import urllib.request
import threading
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

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
                    <title>Meta Auth Success</title>
                    <style>
                        body {
                            font-family: system-ui, sans-serif;
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
                        p { font-size: 15px; color: #a0a0ab; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Meta Authorization Captured</h1>
                        <p>Code received! Exchanging for token now...</p>
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
    server = HTTPServer(('localhost', PORT), OAuthCallbackHandler)
    print("Local HTTP Server started on port 8080. Awaiting Meta callback...")
    sys.stdout.flush()
    server.serve_forever()

def load_tokens():
    token_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "social_tokens.json")
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    token_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "social_tokens.json")
    with open(token_path, "w") as f:
        json.dump(tokens, f, indent=4)
    print(f"Tokens saved successfully to {token_path}")
    sys.stdout.flush()

def http_get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'KeystoneApp/2.0'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    server_thread = threading.Thread(target=run_local_server)
    server_thread.start()
    
    # Print the Meta authorization URL for reference
    scopes = "public_profile,instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement,pages_manage_posts"
    state = "meta_state_keystone_" + str(int(time.time()))
    auth_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scopes,
        'response_type': 'code'
    }
    auth_url = "https://www.facebook.com/v20.0/dialog/oauth?" + urllib.parse.urlencode(auth_params)
    print(f"OAUTH_URL:{auth_url}")
    sys.stdout.flush()
    
    server_thread.join()
    
    code = callback_data.get("code")
    if not code:
        print("Error: No code received.")
        sys.stdout.flush()
        return
        
    print("Exchanging code for short-lived token...")
    sys.stdout.flush()
    short_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&client_secret={CLIENT_SECRET}&code={code}"
    
    try:
        short_tokens = http_get_json(short_token_url)
        short_token = short_tokens["access_token"]
        
        print("Exchanging for long-lived access token...")
        sys.stdout.flush()
        long_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&fb_exchange_token={short_token}"
        long_tokens = http_get_json(long_token_url)
        long_token = long_tokens["access_token"]
        
        all_tokens = load_tokens()
        all_tokens["meta"] = {
            "app_id": CLIENT_ID,
            "app_secret": CLIENT_SECRET,
            "user_access_token": long_token,
            "expires_in": long_tokens.get("expires_in", 5184000),
            "acquired_at": int(time.time())
        }
        save_tokens(all_tokens)
        print("META_AUTH_SUCCESS")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error during Meta token exchange: {str(e)}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
