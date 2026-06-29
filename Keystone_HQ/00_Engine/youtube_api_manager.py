import os
import sys
import io
import json
import logging

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Legacy Windows encoding override removed to prevent Python 3.14 I/O closed file errors.

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class YouTubeAPIManager:
    def __init__(self, token_file="youtube_token.json"):
        self.token_file = token_file
        self.youtube = self._authenticate()
        
    def _authenticate(self):
        """Load the master token and build the YouTube API service."""
        if not os.path.exists(self.token_file):
            logger.error(f"Token file {self.token_file} not found. Please run youtube_oauth.py first.")
            return None
            
        with open(self.token_file, "r") as f:
            creds_data = json.load(f)
            
        creds = Credentials(
            token=creds_data.get("token"),
            refresh_token=creds_data.get("refresh_token"),
            token_uri=creds_data.get("token_uri"),
            client_id=creds_data.get("client_id"),
            client_secret=creds_data.get("client_secret"),
            scopes=creds_data.get("scopes")
        )
        
        # Auto-refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired YouTube token...")
            creds.refresh(Request())
            # Save the refreshed token
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
                
        logger.info("Successfully authenticated with YouTube Data API v3.")
        return build("youtube", "v3", credentials=creds)
        
    def upload_video(self, file_path, title, description, tags, category_id="27", privacy_status="private"):
        """
        Uploads a video to YouTube with the provided metadata.
        """
        if not self.youtube:
            logger.error("YouTube service is not initialized.")
            return None
            
        if not os.path.exists(file_path):
            logger.error(f"Video file not found: {file_path}")
            return None
            
        logger.info(f"Preparing to upload: {file_path}")
        logger.info(f"Title: {title}")
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": False
            }
        }
        if privacy_status in ("private", "unlisted"):
            body["status"]["containsSyntheticMedia"] = True
        
        # Determine mimetype based on extension
        ext = os.path.splitext(file_path)[1].lower()
        mimetype = "video/mp4" if ext == ".mp4" else "video/quicktime"
        
        media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
        
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = None
        try:
            logger.info("Starting upload... This may take a while depending on file size.")
            response = request.execute()
            logger.info(f"✅ Upload Complete! Video ID: {response.get('id')}")
            return response
        except Exception as e:
            logger.error(f"❌ Upload failed: {str(e)}")
            return None

    def update_video_metadata(self, video_id, title=None, description=None, tags=None, category_id=None):
        """
        Updates metadata for an existing video.
        """
        if not self.youtube:
            return None
            
        # First, fetch the existing snippet
        try:
            videos_list_response = self.youtube.videos().list(
                id=video_id,
                part="snippet"
            ).execute()
            
            if not videos_list_response.get("items"):
                logger.error(f"Video {video_id} not found.")
                return None
                
            snippet = videos_list_response["items"][0]["snippet"]
            
            # Update only provided fields
            if title: snippet["title"] = title
            if description: snippet["description"] = description
            if tags is not None: snippet["tags"] = tags
            if category_id: snippet["categoryId"] = category_id
            
            # Perform update
            update_request = self.youtube.videos().update(
                part="snippet",
                body={
                    "id": video_id,
                    "snippet": snippet
                }
            )
            response = update_request.execute()
            logger.info(f"✅ Metadata updated for Video ID: {video_id}")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to update metadata: {str(e)}")
            return None

    def set_thumbnail(self, video_id, image_path):
        """Uploads a custom thumbnail for a video."""
        if not self.youtube:
            return None
        if not os.path.exists(image_path):
            logger.error(f"Thumbnail not found: {image_path}")
            return None
            
        try:
            logger.info(f"Uploading thumbnail {image_path} for video {video_id}...")
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(image_path)
            )
            response = request.execute()
            logger.info(f"✅ Thumbnail updated for Video ID: {video_id}")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to set thumbnail: {str(e)}")
            return None

if __name__ == "__main__":
    # Test initialization
    manager = YouTubeAPIManager()
