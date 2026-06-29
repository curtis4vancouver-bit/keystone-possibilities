"""
Keystone YouTube OAuth — Unified Authentication for ALL 3 Channels
All channels are under the master email: curtis4vancouver@gmail.com

Usage:
    python youtube_oauth_all.py                    # Re-auth ALL 3 channels
    python youtube_oauth_all.py possibilities      # Re-auth just Possibilities
    python youtube_oauth_all.py protocols           # Re-auth just Protocols  
    python youtube_oauth_all.py recomposition       # Re-auth just Recomposition
"""
import os
import sys
import json

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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Channel configuration — the SINGLE SOURCE OF TRUTH for token routing
CHANNEL_CONFIG = {
    "possibilities": {
        "token_file": "youtube_token_possibilities.json",
        "channel_id": "UCu8gdU_R8XE2RvcttGa3drg",
        "display_name": "Keystone Possibilities (Construction)",
        "login_hint": "curtis4vancouver@gmail.com",
    },
    "protocols": {
        "token_file": "youtube_token_protocols.json",
        "channel_id": "UCxURlqMNhAtxUTpdXmlOYaw",
        "display_name": "Keystone Protocols (Clinical Science)",
        "login_hint": "curtis4vancouver@gmail.com",
    },
    "recomposition": {
        "token_file": "youtube_token_oac.json",
        "channel_id": "UCMn1f9DTF_iybKmv5WlTm9Q",
        "display_name": "Keystone Recomposition (Wellness/Music)",
        "login_hint": "curtis4vancouver@gmail.com",
    },
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


def authenticate_channel(channel_name: str) -> bool:
    """Authenticate a single channel and save token with refresh_token."""
    config = CHANNEL_CONFIG[channel_name]
    token_path = os.path.join(SCRIPT_DIR, config["token_file"])
    
    print(f"\n{'='*60}")
    print(f"  AUTHENTICATING: {config['display_name']}")
    print(f"  Token file: {config['token_file']}")
    print(f"  Expected Channel ID: {config['channel_id']}")
    print(f"{'='*60}")
    print()
    print("  A browser will open. IMPORTANT:")
    print(f"  1. Sign in with: {config.get('login_hint')}")
    print(f"  2. Select the channel: {config['display_name'].split('(')[0].strip()}")
    print("  3. Click 'Allow' for ALL permissions")
    print("  4. Check ALL scope boxes if prompted")
    print()
    
    temp_file = os.path.join(SCRIPT_DIR, f"_temp_secrets_{channel_name}.json")
    
    try:
        with open(temp_file, "w") as f:
            json.dump(client_config, f)
        
        flow = InstalledAppFlow.from_client_secrets_file(temp_file, SCOPES)
        
        # CRITICAL: access_type='offline' + prompt='consent' = refresh_token
        # Without access_type='offline', Google will NOT give us a refresh_token
        # Without prompt='consent', Google may skip the consent screen on re-auth
        # and return only an access_token (no refresh_token)
        creds = flow.run_local_server(
            port=8080,
            prompt='consent',
            access_type='offline',
            authorization_prompt_message=f"Opening browser for {config['display_name']}...",
            login_hint=config.get("login_hint")
        )
        
        # Verify we got a refresh token
        if not creds.refresh_token:
            print("\n  ⚠️  WARNING: No refresh_token received!")
            print("  This token will expire and NOT auto-renew.")
            print("  Try revoking app access at https://myaccount.google.com/permissions")
            print("  then re-run this script.")
        else:
            print("\n  ✅ Refresh token obtained — token will auto-renew!")
        
        # Save the token
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        print(f"  ✅ Token saved to {config['token_file']}")
        
        # Verify the token works and points to the right channel
        from googleapiclient.discovery import build
        youtube = build("youtube", "v3", credentials=creds)
        result = youtube.channels().list(part="snippet,statistics", mine=True).execute()
        
        if result.get("items"):
            ch = result["items"][0]
            actual_id = ch["id"]
            actual_name = ch["snippet"]["title"]
            
            print(f"\n  Authenticated as: {actual_name} ({actual_id})")
            print(f"  Videos: {ch['statistics'].get('videoCount', '?')}")
            print(f"  Subscribers: {ch['statistics'].get('subscriberCount', 'hidden')}")
            
            if actual_id == config["channel_id"]:
                print(f"  ✅ CORRECT CHANNEL — matches expected ID")
                return True
            else:
                print(f"\n  ❌ WRONG CHANNEL!")
                print(f"  Expected: {config['channel_id']}")
                print(f"  Got:      {actual_id}")
                print(f"  The token was saved but points to the WRONG channel.")
                print(f"  Re-run and select the correct channel in the browser.")
                return False
        else:
            print("\n  ⚠️  Could not verify channel (mine=True returned empty)")
            print("  Token saved — may work for Brand Account operations.")
            return True
            
    except Exception as e:
        print(f"\n  ❌ ERROR: {str(e)}")
        return False
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    
    if target == "all":
        channels_to_auth = list(CHANNEL_CONFIG.keys())
    elif target in CHANNEL_CONFIG:
        channels_to_auth = [target]
    else:
        print(f"Unknown channel: {target}")
        print(f"Valid options: {', '.join(CHANNEL_CONFIG.keys())}, all")
        sys.exit(1)
    
    print("=" * 60)
    print("  KEYSTONE YOUTUBE MULTI-CHANNEL AUTHENTICATOR")
    print(f"  Master Email: curtis4vancouver@gmail.com")
    print(f"  Channels to authenticate: {', '.join(channels_to_auth)}")
    print("=" * 60)
    
    results = {}
    for channel in channels_to_auth:
        results[channel] = authenticate_channel(channel)
        if len(channels_to_auth) > 1 and channel != channels_to_auth[-1]:
            input("\n  Press ENTER to continue to the next channel...")
    
    # Summary
    print("\n" + "=" * 60)
    print("  AUTHENTICATION SUMMARY")
    print("=" * 60)
    for channel, success in results.items():
        config = CHANNEL_CONFIG[channel]
        status = "✅ SUCCESS" if success else "❌ FAILED"
        token_path = os.path.join(SCRIPT_DIR, config["token_file"])
        has_refresh = False
        if os.path.exists(token_path):
            with open(token_path) as f:
                data = json.load(f)
                has_refresh = bool(data.get("refresh_token"))
        refresh_status = "✅ auto-renew" if has_refresh else "⚠️ NO refresh (will expire)"
        print(f"  {channel:15s} | {status} | {refresh_status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
