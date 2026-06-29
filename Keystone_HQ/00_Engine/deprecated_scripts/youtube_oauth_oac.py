"""
YouTube OAuth — Authenticate for the Recomposition channel (OAC Brand Account).
All channels are under: curtis4vancouver@gmail.com

Run this script, and when the browser opens:
1. Sign in with curtis4vancouver@gmail.com
2. If it asks which channel, pick KeyStone Recomposition
3. Click 'Allow' on all permissions
"""
import os
import sys
import io
import json

# Legacy TextIOWrapper removed — causes Python 3.14 crashes
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]

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

print("=" * 60)
print("  YOUTUBE OAC OWNER AUTHENTICATION")
print("=" * 60)
print()
print("A browser will open. IMPORTANT:")
print("  1. Sign in with: curtis4vancouver@gmail.com")
print("  2. Select the Recomposition channel if asked")
print("  4. Click 'Allow' for all permissions")
print()

try:
    flow = InstalledAppFlow.from_client_secrets_file("temp_secrets.json", SCOPES)
    # Force re-consent and hint at the correct account
    creds = flow.run_local_server(
        port=8080,
        prompt='consent',
        access_type='offline',
        authorization_prompt_message="Opening browser for Recomposition channel auth...",
        login_hint="curtis4vancouver@gmail.com"
    )
    
    with open("youtube_token_oac.json", "w") as token:
        token.write(creds.to_json())
    print("\n[OK] OAC Token saved to youtube_token_oac.json!")
    
    # Test the new token
    from googleapiclient.discovery import build
    youtube = build("youtube", "v3", credentials=creds)
    
    # Check which channel this token is for
    result = youtube.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    for ch in result.get("items", []):
        print(f"\n  Authenticated as: {ch['snippet']['title']} ({ch['id']})")
        print(f"  Videos: {ch['statistics']['videoCount']}")
        
        # Check uploads playlist for unlisted videos
        uploads = ch['contentDetails']['relatedPlaylists']['uploads']
        pl = youtube.playlistItems().list(part="status", playlistId=uploads, maxResults=1).execute()
        total = pl.get("pageInfo", {}).get("totalResults", 0)
        print(f"  Total playlist items (inc. unlisted): {total}")
        
        if ch['id'] == "UCMn1f9DTF_iybKmv5WlTm9Q":
            print("  [OK] CORRECT - This is the OAC channel!")
        else:
            print(f"  [WARNING] Not the OAC. You selected: {ch['snippet']['title']}")
            print("  Re-run and select the correct channel from curtis4vancouver@gmail.com")
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
finally:
    if os.path.exists("temp_secrets.json"):
        os.remove("temp_secrets.json")
