import sys
import os
import json

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

def test_token(name, token_file):
    print(f"\n=== Testing {name} ({token_file}) ===")
    if not os.path.exists(token_file):
        print(f"Token file {token_file} does not exist.")
        return
        
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            print("Failed to initialize service.")
            return
            
        # Get channel details
        ch_resp = manager.youtube.channels().list(
            part="snippet,contentDetails",
            mine=True
        ).execute()
        
        if ch_resp.get("items"):
            item = ch_resp["items"][0]
            print(f"  Channel ID: {item['id']}")
            print(f"  Title: {item['snippet']['title']}")
            
            # List playlists
            playlists_resp = manager.youtube.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=50
            ).execute()
            print(f"  Playlists ({len(playlists_resp.get('items', []))}):")
            for pl in playlists_resp.get("items", []):
                print(f"    - [{pl['id']}] {pl['snippet']['title']} ({pl['contentDetails'].get('itemCount', 0)} videos)")
        else:
            print("  No channels found for this token.")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    os.chdir(SCRIPT_DIR)
    test_token("Default Token", "youtube_token.json")
    test_token("OAC Token", "youtube_token_oac.json")
