import os
import json
import urllib.parse
import urllib.request
import webbrowser
import threading
import time
import sys
import ssl
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Reconfigure stdout to use UTF-8 to prevent Windows console encoding crashes with emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# Cryptography imports for self-signed certificates
try:
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

# Local callback server configuration
PORT = 8080
REDIRECT_URI = f"http://localhost:{PORT}/callback"

# Global dictionary to store captured code
callback_data = {}

def generate_self_signed_cert(cert_path="cert.pem", key_path="key.pem"):
    if not CRYPTOGRAPHY_AVAILABLE:
        raise ImportError("The 'cryptography' package is required but not installed.")
        
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate certificate subject & issuer (self-signed)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Keystone"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localtest.me"),
    ])
    
    # Build certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        # Valid for 30 days
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localtest.me"),
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())
    
    # Write private key file
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
        
    # Write certificate file
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging server requests to terminal to keep UI clean
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
                        <p>Your secure authorization code has been successfully captured by the local background pipeline.</p>
                        <p>You can safely close this browser window now and return to the command line to finalize token registration.</p>
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
            
            # Spin off server shutdown call to allow request thread to complete cleanly
            threading.Thread(target=lambda: self.server.shutdown()).start()
        else:
            self.send_response(404)
            self.end_headers()

def run_local_server(use_ssl=False):
    # Bind to 0.0.0.0 to handle wildcard loopback resolution (localtest.me resolves to 127.0.0.1)
    server = HTTPServer(('0.0.0.0', PORT), OAuthCallbackHandler)
    
    if use_ssl:
        cert_path = "cert.pem"
        key_path = "key.pem"
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            print("🔑 Generating self-signed SSL certificate for localtest.me...")
            generate_self_signed_cert(cert_path, key_path)
            
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        print(f"🔒 Secure local redirect server listening at https://localtest.me:{PORT}/callback")
    else:
        print(f"🔓 Local redirect server listening at http://localhost:{PORT}/callback")
        
    try:
        server.serve_forever()
    finally:
        server.server_close()

def load_tokens():
    tokens = {}
    if os.path.exists("social_tokens.json"):
        try:
            with open("social_tokens.json", "r") as f:
                tokens = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Could not parse social_tokens.json: {str(e)}")
            return {"possibilities": {}, "recomposition": {}}
            
    # Ensure brand sections exist
    if "possibilities" not in tokens:
        tokens["possibilities"] = {}
    if "recomposition" not in tokens:
        tokens["recomposition"] = {}
        
    # Migrate flat old format to brand nested format
    migrated = False
    for flat_key in ["linkedin", "meta", "tiktok"]:
        if flat_key in tokens:
            tokens["possibilities"][flat_key] = tokens.pop(flat_key)
            migrated = True
            
    if migrated:
        print("\n🔄 MIGRATION: Old flat tokens detected in social_tokens.json and migrated to 'possibilities' brand context.")
        save_tokens_silent(tokens)
        
    return tokens

def save_tokens(tokens):
    with open("social_tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)
    print("\n✅ SUCCESS: Social Media credentials updated in social_tokens.json!")

def save_tokens_silent(tokens):
    with open("social_tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)

def select_brand_context():
    while True:
        print("\nSelect Brand Context for this session:")
        print("1. Keystone Possibilities (possibilities)")
        print("2. KeyStone Recomposition (recomposition)")
        print("3. Keystone Protocol (inherits from recomposition)")
        choice = input("Select an option (1-3): ").strip()
        if choice == '1':
            return "possibilities"
        elif choice in ['2', '3']:
            if choice == '3':
                print("ℹ️ Note: Protocol brand inherits Recomposition tokens.")
            return "recomposition"
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

def http_post_form(url, payload):
    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'KeystoneApp/2.0'}
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def http_get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'KeystoneApp/2.0'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def authenticate_linkedin():
    print("\n--- LinkedIn Integration ---\n")
    brand = select_brand_context()
    print("\nPre-requisite: Add 'http://localhost:8080/callback' as an Authorized Redirect URL in LinkedIn Developer Console.")
    client_id = input("Enter LinkedIn Client ID: ").strip()
    client_secret = input("Enter LinkedIn Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Error: Both Client ID and Client Secret are required.")
        return

    # Scopes needed for OpenID Connect + feed posting
    scopes = "openid profile email w_member_social"
    state = f"linkedin_state_{brand}_" + str(int(time.time()))
    
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': scopes
    }
    auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode(auth_params)
    
    print("\nStarting local authentication server...")
    callback_data.clear()
    server_thread = threading.Thread(target=run_local_server)
    server_thread.start()
    
    print(f"Opening browser authorization page...")
    webbrowser.open(auth_url)
    
    # Wait for the background thread callback server to shut down
    server_thread.join()
    
    code = callback_data.get("code")
    if not code:
        print("❌ Error: Authorization code not retrieved.")
        return
        
    print("\nExchanging Authorization Code for Access Tokens...")
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        tokens = http_post_form(token_url, payload)
        
        # Save tokens
        all_tokens = load_tokens()
        all_tokens[brand]["linkedin"] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "access_token": tokens["access_token"],
            "expires_in": tokens.get("expires_in", 5184000), # Default 60 days
            "acquired_at": int(time.time())
        }
        save_tokens(all_tokens)
    except Exception as e:
        print(f"❌ Error during token exchange: {str(e)}")

def authenticate_meta():
    print("\n--- Meta Integration (Facebook Pages & Instagram Business) ---\n")
    brand = select_brand_context()
    print("\nPre-requisite: Add 'http://localhost:8080/callback' as a Valid OAuth Redirect URI in Meta Developer Console.")
    client_id = input("Enter Meta App ID (Client ID): ").strip()
    client_secret = input("Enter Meta App Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Error: Both App ID and App Secret are required.")
        return

    # Request essential scopes for posting to Pages & Instagram Accounts
    scopes = "public_profile,instagram_basic,instagram_content_publish,pages_show_list,pages_read_engagement,pages_manage_posts"
    state = f"meta_state_{brand}_" + str(int(time.time()))
    
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
    
    print(f"Opening browser authorization page...")
    webbrowser.open(auth_url)
    
    server_thread.join()
    
    code = callback_data.get("code")
    if not code:
        print("❌ Error: Authorization code not retrieved.")
        return
        
    print("\nExchanging code for Short-Lived Access Token...")
    short_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={client_id}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&client_secret={client_secret}&code={code}"
    
    try:
        short_tokens = http_get_json(short_token_url)
        short_token = short_tokens["access_token"]
        
        print("Exchanging for Long-Lived Access Token (60-day lifespan)...")
        long_token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={client_id}&client_secret={client_secret}&fb_exchange_token={short_token}"
        long_tokens = http_get_json(long_token_url)
        long_token = long_tokens["access_token"]
        
        # Save tokens
        all_tokens = load_tokens()
        all_tokens[brand]["meta"] = {
            "app_id": client_id,
            "app_secret": client_secret,
            "user_access_token": long_token,
            "expires_in": long_tokens.get("expires_in", 5184000),
            "acquired_at": int(time.time())
        }
        save_tokens(all_tokens)
        
        print("\n💡 NOTE: You can now query your connected Pages and Instagram accounts")
        print("using the acquired User Access Token to automate publishing!")
    except Exception as e:
        print(f"❌ Error during Meta token exchange: {str(e)}")

def authenticate_tiktok():
    print("\n--- TikTok Integration ---\n")
    brand = select_brand_context()
    
    # We can detect if a tunnel is active or let the user input the redirect URI
    default_uri = f"https://localtest.me:{PORT}/callback"
    print(f"Standard Local Redirect URI: {default_uri}")
    print("If you are using a secure tunnel (e.g. ngrok or localhost.run), enter your public HTTPS callback URL.")
    tiktok_redirect_uri = input(f"Enter Redirect URI [{default_uri}]: ").strip()
    if not tiktok_redirect_uri:
        tiktok_redirect_uri = default_uri
        
    client_key = input("Enter TikTok Client Key: ").strip()
    client_secret = input("Enter TikTok Client Secret: ").strip()
    
    if not client_key or not client_secret:
        print("❌ Error: Both Client Key and Client Secret are required.")
        return

    scopes = "user.info.basic,video.upload,video.publish"
    state = f"tiktok_state_{brand}_" + str(int(time.time()))
    
    auth_params = {
        'client_key': client_key,
        'scope': scopes,
        'redirect_uri': tiktok_redirect_uri,
        'state': state,
        'response_type': 'code'
    }
    auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(auth_params)
    
    # Determine if local server needs SSL
    # If the redirect URI starts with https://localhost or https://localtest.me, we need local SSL.
    # If it's a public tunnel (like lhr.life or ngrok), the tunnel handles SSL termination, so local server runs HTTP (no SSL)!
    use_ssl = False
    if tiktok_redirect_uri.startswith("https://") and ("localhost" in tiktok_redirect_uri or "localtest.me" in tiktok_redirect_uri):
        use_ssl = True
        
    print(f"\nStarting local redirect server (SSL={'Enabled' if use_ssl else 'Disabled'})...")
    if use_ssl:
        print("⚠️  IMPORTANT: Since we are using a self-signed SSL certificate for local HTTPS:")
        print("   When the browser redirects to the callback page, you will see a 'Connection not private' warning.")
        print("   Please click 'Advanced' and then 'Proceed to localtest.me (unsafe)' to complete authentication.")
    else:
        print("🔒 Secure tunnel connection detected (SSL handled by tunnel).")
        print("   No browser certificate warnings will be shown!")
        
    callback_data.clear()
    server_thread = threading.Thread(target=lambda: run_local_server(use_ssl=use_ssl))
    server_thread.start()
    
    print(f"\nOpening browser authorization page...")
    webbrowser.open(auth_url)
    
    server_thread.join()
    
    # Cleanup certificate files to keep working directory clean
    for temp_file in ["cert.pem", "key.pem"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                pass
                
    code = callback_data.get("code")
    if not code:
        print("❌ Error: Authorization code not retrieved.")
        return
        
    print("\nExchanging Authorization Code for Access Tokens...")
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        'client_key': client_key,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': tiktok_redirect_uri
    }
    
    try:
        tokens = http_post_form(token_url, payload)
        
        # Save tokens
        all_tokens = load_tokens()
        all_tokens[brand]["tiktok"] = {
            "client_key": client_key,
            "client_secret": client_secret,
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "expires_in": tokens.get("expires_in", 86400), # Typically 24 hours
            "refresh_expires_in": tokens.get("refresh_expires_in", 31536000), # Typically 1 year
            "acquired_at": int(time.time())
        }
        save_tokens(all_tokens)
    except Exception as e:
        print(f"❌ Error during TikTok token exchange: {str(e)}")

def main():
    while True:
        print("\n==============================================")
        print("   Keystone Multi-Platform OAuth Integrator")
        print("==============================================")
        print("1. Authenticate LinkedIn")
        print("2. Authenticate Meta (Facebook / Instagram)")
        print("3. Authenticate TikTok")
        print("4. View Active Social Tokens")
        print("5. Exit")
        print("==============================================")
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            authenticate_linkedin()
        elif choice == '2':
            authenticate_meta()
        elif choice == '3':
            authenticate_tiktok()
        elif choice == '4':
            all_tokens = load_tokens()
            print("\n--- Active Integration Profiles ---")
            for brand_key in ["possibilities", "recomposition"]:
                brand_name = "Keystone Possibilities" if brand_key == "possibilities" else "KeyStone Recomposition / Protocol"
                print(f"\n[{brand_name}]")
                brand_tokens = all_tokens.get(brand_key, {})
                if not brand_tokens:
                    print("  • No active profiles authenticated.")
                else:
                    for platform, data in brand_tokens.items():
                        acquired_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['acquired_at']))
                        print(f"  • {platform.upper()}: Authenticated (Acquired: {acquired_str})")
        elif choice == '5':
            print("\nExiting. Stay Hardcore.")
            break
        else:
            print("\n❌ Invalid choice. Please select from options 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Goodbye.")
        sys.exit(0)
