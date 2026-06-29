import sys
import os

SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

video_id = "LB_ewKqGOsE"
playlist_id = "PL6-D6_RxzlhgaZ5SDa_KHqVA3WCWFKjbf"

new_description = (
    "Building a custom home in Squamish, North Vancouver, or Whistler? The permits aren't the only thing delayed—new growth charges "
    "and structural shifts are squeezing custom builds across the Sea-to-Sky corridor. Here is how high-end project management "
    "keeps your build moving when municipal backlogs freeze the site.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🏗️ KEYSTONE POSSIBILITIES — Luxury Construction & Project Management\n"
    "🔬 Health & Protocols → https://www.youtube.com/@KeystoneProtocols\n"
    "🎵 Focus Music for Builders → https://www.youtube.com/@KeyStoneRecomposition\n"
    "🌐 Website → https://www.keystonepossibilities.ca\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "#squamish #northvancouver #whistler #construction #vancouverbuilder #customhome #projectmanagement #keystonepossibilities #shorts"
)

manager = YouTubeAPIManager(token_file=os.path.join(SCRIPT_DIR, "youtube_token.json"))

if not manager.youtube:
    print("Error: Could not initialize YouTube API Manager.")
    sys.exit(1)

print(f"=== Updating Metadata for Video: {video_id} ===")
# Update description and hashtags
update_result = manager.update_video_metadata(
    video_id=video_id,
    description=new_description
)

if update_result:
    print("SUCCESS: Video description updated successfully.")
else:
    print("FAILED: Video description update failed.")

print(f"=== Adding Video {video_id} to Playlist: {playlist_id} ===")
try:
    playlist_item_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    pl_result = manager.youtube.playlistItems().insert(
        part="snippet",
        body=playlist_item_body
    ).execute()
    print(f"SUCCESS: Video added to playlist! Playlist Item ID: {pl_result.get('id')}")
except Exception as e:
    print(f"FAILED to add to playlist: {e}")
