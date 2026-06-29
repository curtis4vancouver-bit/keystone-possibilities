import sys
import os
import json

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

def list_videos(name, token_file):
    print(f"\n=== Videos for {name} ({token_file}) ===")
    if not os.path.exists(token_file):
        print(f"Token file {token_file} does not exist.")
        return
        
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            print("Failed to initialize service.")
            return
            
        my_channels = manager.youtube.channels().list(
            part="contentDetails",
            mine=True
        ).execute()
        
        if my_channels.get("items"):
            uploads_playlist = my_channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            playlist_items = manager.youtube.playlistItems().list(
                part="snippet,status",
                playlistId=uploads_playlist,
                maxResults=50
            ).execute()
            
            print(f"Uploads count: {len(playlist_items.get('items', []))}")
            for item in playlist_items.get("items", []):
                vid = item["snippet"]
                status = item.get("status", {})
                print(f"  - [{vid['resourceId']['videoId']}] [{status.get('privacyStatus','?')}] {vid['title']}")
        else:
            print("No channels found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    os.chdir(SCRIPT_DIR)
    list_videos("Keystone Possibilities", "youtube_token.json")
    list_videos("KeyStone Recomposition", "youtube_token_oac.json")
