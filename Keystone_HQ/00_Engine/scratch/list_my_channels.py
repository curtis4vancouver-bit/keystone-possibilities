import sys
import os
import json

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

def list_channels_for_token(name, token_file):
    print(f"\n=== Channels for {name} ({token_file}) ===")
    if not os.path.exists(token_file):
        print(f"Token file {token_file} does not exist.")
        return
        
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            print("Failed to initialize service.")
            return
            
        # Get all channels the authenticated user has access to
        channels_response = manager.youtube.channels().list(
            part="snippet,contentDetails",
            mine=True
        ).execute()
        
        for ch in channels_response.get("items", []):
            print(f"  - Channel ID: {ch['id']}")
            print(f"    Title: {ch['snippet']['title']}")
            print(f"    Custom URL: {ch['snippet'].get('customUrl', 'N/A')}")
            
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    os.chdir(SCRIPT_DIR)
    list_channels_for_token("Default Token", "youtube_token.json")
    list_channels_for_token("OAC Token", "youtube_token_oac.json")
