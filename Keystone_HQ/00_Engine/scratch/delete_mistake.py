import os
import sys
import json
import logging

# Ensure CWD is correct
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    token_file = "youtube_token.json"
    if not os.path.exists(token_file):
        logger.error(f"Token file {token_file} does not exist.")
        return

    logger.info("Initializing YouTubeAPIManager with youtube_token.json...")
    manager = YouTubeAPIManager(token_file=token_file)
    if not manager.youtube:
        logger.error("Failed to initialize YouTube Data API client.")
        return

    # 1. Identify which channel this is
    try:
        channels_response = manager.youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()
        
        if channels_response.get("items"):
            channel = channels_response["items"][0]
            title = channel["snippet"]["title"]
            channel_id = channel["id"]
            logger.info(f"Connected Channel: {title} ({channel_id})")
        else:
            logger.error("No channel found for these credentials.")
            return
    except Exception as e:
        logger.error(f"Failed to identify channel: {str(e)}")
        return

    # 2. Delete the specific video if it was uploaded here
    video_id = "-abkt0cDDY4"
    logger.info(f"Attempting to delete video {video_id} from channel '{title}'...")
    try:
        # Check if video exists first
        video_details = manager.youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if video_details.get("items"):
            video_title = video_details["items"][0]["snippet"]["title"]
            logger.info(f"Found video: '{video_title}'. Proceeding with deletion...")
            manager.youtube.videos().delete(id=video_id).execute()
            logger.info(f"✅ SUCCESS: Deleted video '{video_title}' ({video_id}) from {title}!")
        else:
            logger.warning(f"Video {video_id} was not found on YouTube or you don't have access. It might already be deleted.")
    except Exception as e:
        logger.error(f"Failed to delete video: {str(e)}")

if __name__ == "__main__":
    main()
