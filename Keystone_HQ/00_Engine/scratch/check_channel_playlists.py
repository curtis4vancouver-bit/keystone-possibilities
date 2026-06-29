import sys
import os
import json

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

def main():
    manager = YouTubeAPIManager(token_file=os.path.join(SCRIPT_DIR, "youtube_token.json"))
    if not manager.youtube:
        print("Error: Could not initialize YouTube API Manager.")
        sys.exit(1)
        
    print("=== Listing Playlists for Authenticated Channel ===")
    try:
        playlists_response = manager.youtube.playlists().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        ).execute()
        
        items = playlists_response.get("items", [])
        print(f"Found {len(items)} playlists:")
        for idx, pl in enumerate(items, 1):
            snippet = pl["snippet"]
            details = pl["contentDetails"]
            print(f"{idx}. [{pl['id']}] Title: {snippet['title']} (Videos: {details.get('itemCount', 0)})")
            
    except Exception as e:
        print(f"Error fetching playlists: {e}")

if __name__ == "__main__":
    main()
