# Keystone YouTube API Manager (Multiplexer Stub)
# This is a lightweight stub so the MCP Multiplexer can import youtube_mcp.py
# without crashing when google-auth / google-api-python-client are missing
# or when token files aren't present. It mirrors the full manager at:
#   youtube_api_manager.py (project root)
#
# TODO: Replace this stub with a proper import path or symlink to the
#       canonical youtube_api_manager.py once the Multiplexer path
#       routing is fixed. Alternatively, install the required Google
#       packages in the Multiplexer venv and copy the real file.

import os
import json
import logging

logger = logging.getLogger(__name__)


class YouTubeAPIManager:
    """Stub implementation of the YouTube API Manager.

    Provides the same interface as the real manager so youtube_mcp.py
    can instantiate it without import errors. All API calls return
    None or placeholder values.

    TODO: Route imports to the canonical youtube_api_manager.py at the
          project root, or install google-auth + google-api-python-client
          in the Multiplexer environment and copy the real file here.
    """

    def __init__(self, token_file="youtube_token.json"):
        self.token_file = token_file
        self.youtube = self._authenticate()

    def _authenticate(self):
        """Attempt to authenticate with Google OAuth2.

        Falls back to a stub service object if the required Google
        packages or token files are unavailable.
        """
        if not os.path.exists(self.token_file):
            logger.warning(
                f"[YT STUB] Token file {self.token_file} not found. "
                "Running in stub mode."
            )
            return None

        try:
            # Try the real authentication path
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request

            with open(self.token_file, "r") as f:
                creds_data = json.load(f)

            creds = Credentials(
                token=creds_data.get("token"),
                refresh_token=creds_data.get("refresh_token"),
                token_uri=creds_data.get("token_uri"),
                client_id=creds_data.get("client_id"),
                client_secret=creds_data.get("client_secret"),
                scopes=creds_data.get("scopes"),
            )

            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired YouTube token...")
                creds.refresh(Request())
                with open(self.token_file, "w") as token:
                    token.write(creds.to_json())

            logger.info("Successfully authenticated with YouTube Data API v3.")
            return build("youtube", "v3", credentials=creds)

        except ImportError:
            logger.warning(
                "[YT STUB] google-auth or google-api-python-client not "
                "installed. Running in stub mode — API calls will return None."
            )
            return None
        except Exception as e:
            logger.warning(
                f"[YT STUB] Authentication failed: {e}. Running in stub mode."
            )
            return None

    def upload_video(
        self,
        file_path,
        title,
        description,
        tags,
        category_id="27",
        privacy_status="private",
    ):
        """Uploads a video to YouTube.

        TODO: Requires real google-api-python-client MediaFileUpload.
        """
        if not self.youtube:
            logger.error("[YT STUB] Cannot upload — running in stub mode.")
            return None
        # If we have a real youtube service, delegate to it
        try:
            from googleapiclient.http import MediaFileUpload

            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": category_id,
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False,
                },
            }
            if privacy_status in ("private", "unlisted"):
                body["status"]["containsSyntheticMedia"] = True
            ext = os.path.splitext(file_path)[1].lower()
            mimetype = "video/mp4" if ext == ".mp4" else "video/quicktime"
            media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
            request = self.youtube.videos().insert(
                part="snippet,status", body=body, media_body=media
            )
            response = request.execute()
            logger.info(f"Upload Complete! Video ID: {response.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return None

    def update_video_metadata(
        self, video_id, title=None, description=None, tags=None, category_id=None
    ):
        """Updates metadata for an existing video.

        TODO: Requires real YouTube API service.
        """
        if not self.youtube:
            logger.error("[YT STUB] Cannot update — running in stub mode.")
            return None
        try:
            resp = self.youtube.videos().list(id=video_id, part="snippet").execute()
            if not resp.get("items"):
                return None
            snippet = resp["items"][0]["snippet"]
            if title:
                snippet["title"] = title
            if description:
                snippet["description"] = description
            if tags is not None:
                snippet["tags"] = tags
            if category_id:
                snippet["categoryId"] = category_id
            return (
                self.youtube.videos()
                .update(part="snippet", body={"id": video_id, "snippet": snippet})
                .execute()
            )
        except Exception as e:
            logger.error(f"Failed to update metadata: {e}")
            return None

    def set_thumbnail(self, video_id, image_path):
        """Uploads a custom thumbnail for a video.

        TODO: Requires real YouTube API service.
        """
        if not self.youtube:
            logger.error("[YT STUB] Cannot set thumbnail — running in stub mode.")
            return None
        try:
            from googleapiclient.http import MediaFileUpload

            return (
                self.youtube.thumbnails()
                .set(videoId=video_id, media_body=MediaFileUpload(image_path))
                .execute()
            )
        except Exception as e:
            logger.error(f"Failed to set thumbnail: {e}")
            return None
