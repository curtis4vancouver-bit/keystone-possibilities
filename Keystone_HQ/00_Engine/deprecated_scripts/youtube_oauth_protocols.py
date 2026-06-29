import os
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Set standard output encoding to utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 
          'https://www.googleapis.com/auth/youtube']

CLIENT_ID = "911189793704-0dhnkc0g3f7tlq197ujal3o1ie0e2nk8.apps.googleusercontent.com"
CLIENT_SECRET = "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"

client_config = {
    "web": {
        "client_id": CLIENT_ID,
        "project_id": "semiotic-ion-458504-e9",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": CLIENT_SECRET,
        "redirect_uris": ["http://localhost:8080/"]
    }
}

with open("temp_secrets_protocols.json", "w") as f:
    json.dump(client_config, f)

print("Starting YouTube Authentication Flow for KEYSTONE PROTOCOLS...")
print("A browser window will open. Please log in, choose the CORRECT channel (Keystone Protocols), and click 'Allow'.")
print("IMPORTANT: Make sure to check ALL permission boxes (Upload videos, View YouTube Account).")

try:
    flow = InstalledAppFlow.from_client_secrets_file("temp_secrets_protocols.json", SCOPES)
    # Use run_local_server to handle the redirect back
    creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')
    
    with open("youtube_token_protocols.json", "w") as token:
        token.write(creds.to_json())
    print("\nSUCCESS: Token saved to youtube_token_protocols.json!")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
finally:
    if os.path.exists("temp_secrets_protocols.json"):
        os.remove("temp_secrets_protocols.json")
