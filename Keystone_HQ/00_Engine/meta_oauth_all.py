"""
Keystone Meta OAuth — Unified Authentication & Verification for Facebook & Instagram Pages
All accounts are under the master email: curtis4vancouver@gmail.com

Usage:
    python meta_oauth_all.py
"""
import os
import sys
import json
import time
import urllib.parse
import urllib.request
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Reconfigure stdout to use UTF-8 to prevent Windows console encoding crashes with emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}/callback"

# Global dict to hold callback data
callback_data = {}

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging to keep terminal clean
        return

    def do_GET(self):
        if self.path.startswith("/callback"):
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            code = query_params.get("code", [None])[0]
            error = query_params.get("error", [None])[0]
            error_description = query_params.get("error_description", [None])[0]
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            if code:
                callback_data["code"] = code
                html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Keystone Meta Auth Success</title>
                    <style>
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
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
                        <h1>Keystone Meta Integration</h1>
                        <p>Your secure Meta authorization code has been successfully captured by the local background pipeline.</p>
                        <p>You can safely close this browser window now and return to the terminal to complete token verification.</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
            else:
                callback_data["error"] = error or "unknown"
                callback_data["error_description"] = error_description or "Unknown error"
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Keystone Meta Auth Failed</title>
                    <style>
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                            background-color: #0c0c0e;
                            color: #e0e0e4;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }}
                        .container {{
                            text-align: center;
                            background-color: #141417;
                            padding: 50px 40px;
                            border-radius: 16px;
                            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
                            border: 1px solid #ff5555;
                            max-width: 480px;
                        }}
                        h1 {{ color: #ff5555; font-size: 24px; margin-top: 0; margin-bottom: 16px; font-weight: 600; }}
                        p {{ font-size: 15px; line-height: 1.6; color: #a0a0ab; margin-bottom: 24px; }}
                        .error-badge {{
                            background-color: rgba(255, 85, 85, 0.1);
                            color: #ff5555;
                            padding: 6px 14px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 700;
                            letter-spacing: 1.5px;
                            display: inline-block;
                            margin-bottom: 20px;
                            border: 1px solid rgba(255, 85, 85, 0.3);
                            text-transform: uppercase;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="error-badge">Authorization Failed</div>
                        <h1>Meta Authentication Error</h1>
                        <p>Error: {error}</p>
                        <p>Description: {error_description}</p>
                        <p>Please close this browser window and check the terminal logs.</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
            
            # Shut down server after handling request
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

def load_tokens() -> dict:
    if os.path.exists("social_tokens.json"):
        with open("social_tokens.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"possibilities": {}, "recomposition": {}}

def save_tokens(tokens):
    with open("social_tokens.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)
    print("\n✅ SUCCESS: Saved Meta user access token to social_tokens.json!")

def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "KeystoneOAuth/2.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def main():
    print("=" * 70)
    print("  KEYSTONE META (FACEBOOK + INSTAGRAM) UNIFIED AUTHENTICATOR")
    print("=" * 70)
    
    # 1. Load active config
    tokens = load_tokens()
    
    # Extract app credentials from current possibilities meta context as master config
    poss_meta = tokens.get("possibilities", {}).get("meta", {})
    app_id = poss_meta.get("app_id", "1004714315742024")
    app_secret = poss_meta.get("app_secret", "57ca3100e6a28799d666db6b20e1a8be")
    
    print(f"Using Meta App ID: {app_id}")
    print(f"Using Redirect URI: {REDIRECT_URI}")
    
    # Essential scopes for both Facebook page updates and Instagram Business publishing
    scopes = [
        "public_profile",
        "instagram_basic",
        "instagram_content_publish",
        "pages_show_list",
        "pages_read_engagement",
        "pages_manage_posts"
    ]
    
    auth_params = {
        "client_id": app_id,
        "redirect_uri": REDIRECT_URI,
        "scope": ",".join(scopes),
        "response_type": "code",
        "state": f"keystone_meta_{int(time.time())}"
    }
    
    auth_url = "https://www.facebook.com/v20.0/dialog/oauth?" + urllib.parse.urlencode(auth_params)
    
    print("\nStarting local background HTTP server...")
    callback_data.clear()
    server_thread = threading.Thread(target=run_local_server)
    server_thread.start()
    
    print("Opening browser for authorization...")
    print("IMPORTANT: Log in as 'Curtis Stevenson' and authorize ALL pages & Instagram accounts.")
    webbrowser.open(auth_url)
    
    # Wait for callback server to stop
    server_thread.join()
    
    if "error" in callback_data:
        print(f"\n❌ Error returned from Meta: {callback_data['error']}")
        print(f"Description: {callback_data['error_description']}")
        return
        
    code = callback_data.get("code")
    if not code:
        print("\n❌ Error: No authorization code captured. Server shutdown.")
        return
        
    print("\nExchanging Authorization Code for Short-Lived Access Token...")
    short_token_url = (
        f"https://graph.facebook.com/v20.0/oauth/access_token?"
        f"client_id={app_id}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&client_secret={app_secret}&code={code}"
    )
    
    try:
        short_res = http_get_json(short_token_url)
        short_token = short_res["access_token"]
        print("✅ Obtained short-lived User Access Token.")
        
        print("\nExchanging for Long-Lived User Access Token (60 days)...")
        long_token_url = (
            f"https://graph.facebook.com/v20.0/oauth/access_token?"
            f"grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_token}"
        )
        long_res = http_get_json(long_token_url)
        long_token = long_res["access_token"]
        expires_in = long_res.get("expires_in", 5184000)
        print("✅ Obtained long-lived User Access Token.")
        
        # 2. Update tokens in memory
        for brand in ["possibilities", "recomposition"]:
            if brand not in tokens:
                tokens[brand] = {}
            tokens[brand]["meta"] = {
                "app_id": app_id,
                "app_secret": app_secret,
                "user_access_token": long_token,
                "expires_in": expires_in,
                "acquired_at": int(time.time())
            }
        
        # Save tokens
        save_tokens(tokens)
        
        # 3. Verify access to pages and print rich report
        print("\n" + "="*70)
        print("  VERIFYING LIVE API CONTEXTS & CHANNELS")
        print("="*70)
        
        # Retrieve user profile
        try:
            user_url = f"https://graph.facebook.com/v20.0/me?fields=id,name&access_token={long_token}"
            user_data = http_get_json(user_url)
            print(f"👤 Authenticated User: {user_data.get('name')} (ID: {user_data.get('id')})")
        except Exception as e:
            print(f"❌ Failed to fetch user profile: {e}")
            
        # Retrieve connected pages
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={long_token}"
        try:
            pages_res = http_get_json(pages_url)
            pages = pages_res.get("data", [])
            print(f"\n🔍 Found {len(pages)} Facebook Pages connected to this user:")
            
            # The page mappings expected by Keystone
            expected_pages = {
                "166025896601563": "Keystone Possibilities",
                "898671469990393": "KeyStone Recomposition"
            }
            
            for page in pages:
                page_id = page.get("id")
                page_name = page.get("name")
                page_token = page.get("access_token")
                
                status_label = "⚠️ UNKNOWN/OTHER"
                if page_id in expected_pages:
                    status_label = f"✅ KEYSTONE MATCH ({expected_pages[page_id]})"
                    
                print(f"  • Page: {page_name:30s} | ID: {page_id:15s} | {status_label}")
                
                # Check for connected Instagram Business accounts
                try:
                    ig_url = f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
                    ig_res = http_get_json(ig_url)
                    ig_account = ig_res.get("instagram_business_account", {})
                    ig_id = ig_account.get("id")
                    
                    if ig_id:
                        print(f"    └─ Instagram Business Account Linked! ID: {ig_id}")
                    else:
                        print(f"    └─ ❌ No linked Instagram Business Account found.")
                except Exception as e:
                    print(f"    └─ ❌ Error checking Instagram link: {e}")
            
            # Check if any expected page is missing
            found_ids = [p.get("id") for p in pages]
            missing = [name for id_, name in expected_pages.items() if id_ not in found_ids]
            if missing:
                print(f"\n⚠️ WARNING: The following required Facebook Pages were not authorized:")
                for m in missing:
                    print(f"  • {m}")
                print("Make sure you authorized all requested pages during login.")
            else:
                print(f"\n✅ All required Facebook Pages and Instagram profiles are fully authorized and active!")
                
        except Exception as e:
            print(f"❌ Failed to query pages: {e}")
            
    except Exception as e:
        print(f"\n❌ Error during token exchange or verification: {e}")

if __name__ == "__main__":
    main()
