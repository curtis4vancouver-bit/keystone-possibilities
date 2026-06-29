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

    video_id = "rzxpWi2yBLQ"
    correct_playlist_id = "PL22ZXw2RiZLSsJbrHT_R70D_xACSTV1f6" # Builder Blueprint Shorts
    redundant_playlist_id = "PL22ZXw2RiZLQo4zUwtlx89Ey1jzI4z67T" # Keystone Protocols Shorts

    # 1. Add video to the correct, pre-existing playlist
    try:
        logger.info(f"Adding video {video_id} to the correct existing playlist '{correct_playlist_id}'...")
        body = {
            "snippet": {
                "playlistId": correct_playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
        response = manager.youtube.playlistItems().insert(
            part="snippet",
            body=body
        ).execute()
        logger.info(f"✅ Successfully added video to 'Builder Blueprint Shorts'! Item ID: {response.get('id')}")
    except Exception as e:
        logger.error(f"Failed to add video to correct playlist: {str(e)}")

    # 2. Delete the redundant playlist we accidentally created
    try:
        logger.info(f"Deleting the redundant empty playlist '{redundant_playlist_id}' to clean up the channel...")
        manager.youtube.playlists().delete(id=redundant_playlist_id).execute()
        logger.info(f"✅ Successfully deleted the redundant playlist '{redundant_playlist_id}'!")
    except Exception as e:
        logger.error(f"Failed to delete redundant playlist: {str(e)}")

if __name__ == "__main__":
    main()
