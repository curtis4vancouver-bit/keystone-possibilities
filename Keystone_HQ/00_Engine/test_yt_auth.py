"""Quick test: verify YouTube API auth and list all 3 Keystone channels using their respective token files."""
import os
import json
from youtube_api_manager import YouTubeAPIManager

TOKENS = {
    "possibilities": "youtube_token_possibilities.json",
    "protocols": "youtube_token.json",
    "recomposition": "youtube_token_oac.json"
}

CHANNELS = {
    "possibilities": "UCu8gdU_R8XE2RvcttGa3drg",
    "protocols": "UCxURlqMNhAtxUTpdXmlOYaw",
    "recomposition": "UCMn1f9DTF_iybKmv5WlTm9Q"
}

print("=== YouTube API Multi-Token Verification ===")

for name, token_file in TOKENS.items():
    print(f"\n--- Testing {name.upper()} (Token: {token_file}) ---")
    if not os.path.exists(token_file):
        print(f"  WARNING: Token file {token_file} does not exist. Trying legacy fallback youtube_token.json")
        token_file = "youtube_token.json"
        if not os.path.exists(token_file):
            print("  ERROR: No token file found.")
            continue
            
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            print("  ERROR: Failed to initialize YouTube service.")
            continue
            
        # Get authorized channel info
        res = manager.youtube.channels().list(part="snippet", mine=True).execute()
        if res.get("items"):
            ch = res["items"][0]
            print(f"  SUCCESS! Authenticated to channel: '{ch['snippet']['title']}' (ID: {ch['id']})")
            expected_id = CHANNELS[name]
            if ch['id'] == expected_id:
                print("  MATCH OK: Channel matches expected ID.")
            else:
                print(f"  ❌ MISMATCH: Expected {expected_id}, but token is for {ch['id']}.")
        else:
            print("  WARNING: No channels found (mine=True returned empty). Checking explicit ID lookup...")
            res2 = manager.youtube.channels().list(part="snippet", id=CHANNELS[name]).execute()
            if res2.get("items"):
                ch = res2["items"][0]
                print(f"  FOUND by ID: '{ch['snippet']['title']}' (ID: {ch['id']})")
            else:
                print(f"  ERROR: Channel ID {CHANNELS[name]} not found or not authorized.")
    except Exception as e:
        print(f"  ERROR testing token: {e}")
