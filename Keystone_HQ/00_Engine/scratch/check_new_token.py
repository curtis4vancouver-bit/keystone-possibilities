import os
import sys
import json
import logging

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Set standard output encoding to utf-8 in python to prevent CP1252 crash
sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    token_file = "youtube_token.json"
    if not os.path.exists(token_file):
        logger.error(f"{token_file} does not exist!")
        return

    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Failed to build YouTube service.")
            return

        channels_response = manager.youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()

        if channels_response.get("items"):
            channel = channels_response["items"][0]
            title = channel["snippet"]["title"]
            channel_id = channel["id"]
            logger.info(f"✅ Success! Token is active.")
            logger.info(f"Connected Channel: {title} ({channel_id})")
        else:
            logger.error("No channel found for these credentials.")
    except Exception as e:
        logger.error(f"Error checking token: {str(e)}")

if __name__ == "__main__":
    main()
