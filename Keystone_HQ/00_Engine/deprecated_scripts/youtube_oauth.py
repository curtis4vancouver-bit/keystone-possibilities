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

with open("temp_secrets.json", "w") as f:
    json.dump(client_config, f)

channel = sys.argv[1] if len(sys.argv) > 1 else "oac"
token_filename = f"youtube_token_{channel}.json"

print(f"Starting YouTube Authentication Flow for channel: {channel}")
print("A browser window will open. Please log in, choose the CORRECT channel, and click 'Allow'.")

try:
    flow = InstalledAppFlow.from_client_secrets_file("temp_secrets.json", SCOPES)
    # Force consent to ensure we get a refresh token
    creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')
    
    with open(token_filename, "w") as token:
        token.write(creds.to_json())
    print(f"\nSUCCESS: YouTube Token saved to {token_filename}!")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
finally:
    if os.path.exists("temp_secrets.json"):
        os.remove("temp_secrets.json")
