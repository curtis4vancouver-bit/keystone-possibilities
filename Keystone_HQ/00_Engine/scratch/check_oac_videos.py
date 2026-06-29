import os
import sys
import json
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    token_file = "youtube_token_oac.json"
    if not os.path.exists(token_file):
        logger.error("youtube_token_oac.json not found.")
        return
        
    manager = YouTubeAPIManager(token_file=token_file)
    if not manager.youtube:
        return
        
    try:
        channels_response = manager.youtube.channels().list(
            part="snippet,contentDetails",
            mine=True
        ).execute()
        
        channel_title = channels_response["items"][0]["snippet"]["title"]
        uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        logger.info(f"OAC Channel Title: {channel_title}")
        logger.info(f"OAC Uploads playlist ID: {uploads_playlist_id}")
        
        playlist_items_response = manager.youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=10
        ).execute()
        
        logger.info("OAC Recent Uploads:")
        for item in playlist_items_response.get("items", []):
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            published_at = item["snippet"]["publishedAt"]
            logger.info(f"- Title: {title} | Video ID: {video_id} | Published: {published_at}")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
