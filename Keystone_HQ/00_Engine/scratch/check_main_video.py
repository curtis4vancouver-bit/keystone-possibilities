import sys
import os
import json

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

def check_video(video_id, token_file):
    print(f"\n=== Checking Video {video_id} using {token_file} ===")
    if not os.path.exists(token_file):
        print(f"Token file {token_file} does not exist.")
        return
        
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            print("Failed to initialize service.")
            return
            
        videos_response = manager.youtube.videos().list(
            part="snippet,status",
            id=video_id
        ).execute()
        
        items = videos_response.get("items", [])
        if items:
            item = items[0]
            print(f"  Found video!")
            print(f"  Channel ID: {item['snippet']['channelId']}")
            print(f"  Channel Title: {item['snippet'].get('channelTitle', 'N/A')}")
            print(f"  Title: {item['snippet']['title']}")
            print(f"  Privacy: {item['status']['privacyStatus']}")
        else:
            print("  Video not found with this token.")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    os.chdir(SCRIPT_DIR)
    check_video("UoFQmlKo5Uc", "youtube_token.json")
    check_video("UoFQmlKo5Uc", "youtube_token_oac.json")
