import os
import sys
import json
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Reconfigure output to utf-8
sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    token_file = "youtube_token.json"
    manager = YouTubeAPIManager(token_file=token_file)
    if not manager.youtube:
        return
        
    try:
        channels_response = manager.youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()
        
        channel_title = channels_response["items"][0]["snippet"]["title"]
        logger.info(f"Checking playlists for target channel: {channel_title}")
        
        playlists_response = manager.youtube.playlists().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        ).execute()
        
        logger.info("Found Playlists:")
        items = playlists_response.get("items", [])
        if not items:
            logger.info("No playlists found on this channel using mine=True.")
        else:
            for item in items:
                playlist_id = item["id"]
                title = item["snippet"]["title"]
                item_count = item["contentDetails"]["itemCount"]
                logger.info(f"- Playlist Title: '{title}' | ID: {playlist_id} | Video Count: {item_count}")
                
    except Exception as e:
        logger.error(f"Error listing playlists: {str(e)}")

if __name__ == "__main__":
    main()
