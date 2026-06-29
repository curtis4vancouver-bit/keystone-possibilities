import os
import sys
import json

# Add the 00_Master_Brain to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_BRAIN_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(MASTER_BRAIN_DIR)

try:
    from youtube_api_manager import YouTubeAPIManager
except ImportError as e:
    print(f"Error importing YouTubeAPIManager: {e}")
    sys.exit(1)

def get_latest_video_stats():
    token_file = os.path.join(MASTER_BRAIN_DIR, "youtube_token.json")
    if not os.path.exists(token_file):
        print(f"Token file not found: {token_file}")
        return

    manager = YouTubeAPIManager(token_file=token_file)
    if not manager.youtube:
        print("Failed to authenticate with YouTube API.")
        return

    try:
        # Get channel's uploaded videos playlist
        channels_response = manager.youtube.channels().list(
            mine=True,
            part="contentDetails,statistics,snippet"
        ).execute()

        if not channels_response.get("items"):
            print("No channel found for authenticated user.")
            return

        channel = channels_response["items"][0]
        uploads_playlist_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_title = channel["snippet"]["title"]
        print(f"Channel: {channel_title}")

        # Get the latest video from uploads
        playlist_response = manager.youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part="snippet",
            maxResults=3
        ).execute()

        if not playlist_response.get("items"):
            print("No videos found in uploads playlist.")
            return

        print("\n--- Latest Videos ---")
        for item in playlist_response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            published_at = item["snippet"]["publishedAt"]

            # Get video statistics
            video_response = manager.youtube.videos().list(
                id=video_id,
                part="statistics"
            ).execute()

            if video_response.get("items"):
                stats = video_response["items"][0]["statistics"]
                views = stats.get("viewCount", "0")
                likes = stats.get("likeCount", "0")
                comments = stats.get("commentCount", "0")
                
                print(f"\nTitle: {title}")
                print(f"Published: {published_at}")
                print(f"Views: {views} | Likes: {likes} | Comments: {comments}")
                print(f"Link: https://youtube.com/shorts/{video_id}")
            else:
                print(f"Could not fetch stats for {video_id}")

    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    get_latest_video_stats()
