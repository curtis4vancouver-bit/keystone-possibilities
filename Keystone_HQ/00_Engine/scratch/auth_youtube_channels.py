import os
import sys
import json
import logging
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Standard scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]

CLIENT_ID = "911189793704-0dhnkc0g3f7tlq197ujal3o1ie0e2nk8.apps.googleusercontent.com"
CLIENT_SECRET = "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"

CHANNELS = {
    "possibilities": "UCu8gdU_R8XE2RvcttGa3drg",   # Construction brand
    "protocols": "UCxURlqMNhAtxUTpdXmlOYaw",        # Protocols channel
    "recomposition": "UCMn1f9DTF_iybKmv5WlTm9Q",    # Health/wellness brand
    "oac": "UCMn1f9DTF_iybKmv5WlTm9Q",              # Alias for recomposition
}

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

def main():
    parser = argparse.ArgumentParser(description="Authenticate YouTube Channels specifically.")
    parser.add_argument("--channel", required=True, choices=["possibilities", "protocols", "recomposition", "oac"],
                        help="The channel context to authenticate.")
    args = parser.parse_args()

    channel = args.channel
    expected_channel_id = CHANNELS[channel]
    
    # Map token filenames
    token_files = {
        "possibilities": "youtube_token_possibilities.json",
        "protocols": "youtube_token_protocols.json",
        "recomposition": "youtube_token_oac.json",
        "oac": "youtube_token_oac.json"
    }
    
    token_file = token_files[channel]
    
    # Determine login hint and directions
    login_hint = "curtis4vancouver@gmail.com"
    if channel in ["recomposition", "oac"]:
        directions = (
            "1. Sign in with: curtis4vancouver@gmail.com\n"
            "2. Pick 'KeyStone Recomposition' channel (119 subs)\n"
            "3. Allow all permissions"
        )
    elif channel == "possibilities":
        directions = (
            "1. Sign in with: curtis4vancouver@gmail.com\n"
            "2. Pick '@KeystonePossibilities' channel\n"
            "3. Allow all permissions"
        )
    else:  # protocols
        directions = (
            "1. Sign in with: curtis4vancouver@gmail.com\n"
            "2. Pick 'Keystone Protocols' channel (Note: Protocol videos will be routed to Recomposition channel!)\n"
            "3. Allow all permissions"
        )

    # Write temp client secret file
    temp_secrets = f"temp_secrets_{channel}.json"
    with open(temp_secrets, "w") as f:
        json.dump(client_config, f)

    print("=" * 60)
    print(f"  YOUTUBE OAUTH AUTHENTICATION: {channel.upper()}")
    print("=" * 60)
    print()
    print("IMPORTANT DIRECTIONS:")
    print(directions)
    print()

    try:
        flow = InstalledAppFlow.from_client_secrets_file(temp_secrets, SCOPES)
        
        # Get the URL manually first so we can print it before starting the server
        flow.redirect_uri = "http://localhost:8080/"
        auth_url, _ = flow.authorization_url(
            prompt='select_account consent'
        )
        
        print("Starting local callback server on port 8080...")
        print(f"AUTH_URL: {auth_url}")
        sys.stdout.flush() # Make sure URL is printed immediately
        
        # Run the server and block until callback is received
        creds = flow.run_local_server(
            port=8080,
            authorization_prompt_message=f"Opening browser for {channel} authentication...",
            prompt='select_account consent'
        )
        
        # Save credentials to target token file
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            
        print(f"\n[OK] YouTube token saved to {token_file}!")
        
        # Verify the channel
        youtube = build("youtube", "v3", credentials=creds)
        result = youtube.channels().list(part="snippet,statistics", mine=True).execute()
        
        authenticated_channel_title = "Unknown"
        authenticated_channel_id = "Unknown"
        
        if result.get("items"):
            ch = result["items"][0]
            authenticated_channel_title = ch['snippet']['title']
            authenticated_channel_id = ch['id']
            print(f"\n  Authenticated as: {authenticated_channel_title} ({authenticated_channel_id})")
            
            if authenticated_channel_id == expected_channel_id:
                print("  [OK] SUCCESS - Authenticated channel matches target channel!")
            else:
                print(f"  [WARNING] Channel ID mismatch! Expected: {expected_channel_id}, got: {authenticated_channel_id}")
                print(f"  You may have selected the wrong channel ({authenticated_channel_title}).")
                print("  Please re-run this script and select the correct channel!")
        else:
            print("\n  [WARNING] No channel details returned. Verify your selections.")
            
    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {str(e)}")
    finally:
        if os.path.exists(temp_secrets):
            try:
                os.remove(temp_secrets)
            except Exception:
                pass

if __name__ == "__main__":
    main()
