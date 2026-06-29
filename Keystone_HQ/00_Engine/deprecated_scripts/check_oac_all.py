"""Check if all OAC unlisted videos are now visible via API."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

OAC_ID = "UCMn1f9DTF_iybKmv5WlTm9Q"
uploads = "UU" + OAC_ID[2:]

# Get channel stats first
stats = yt.channels().list(part="statistics", id=OAC_ID).execute()
reported = stats["items"][0]["statistics"]["videoCount"]
print(f"Channel reports: {reported} total videos\n")

# Pull ALL videos from uploads playlist (paginated)
all_videos = []
next_page = None
page = 0
while True:
    page += 1
    r = yt.playlistItems().list(
        part="snippet,status",
        playlistId=uploads,
        maxResults=50,
        pageToken=next_page
    ).execute()
    
    batch = r.get("items", [])
    all_videos.extend(batch)
    print(f"Page {page}: Got {len(batch)} videos (total so far: {len(all_videos)})")
    
    next_page = r.get("nextPageToken")
    if not next_page:
        break

# Count by privacy
pub = unl = priv = 0
for v in all_videos:
    p = v.get("status", {}).get("privacyStatus", "?")
    if p == "public": pub += 1
    elif p == "unlisted": unl += 1
    elif p == "private": priv += 1

print(f"\n{'='*60}")
print(f"  TOTAL VISIBLE: {len(all_videos)}")
print(f"  Public: {pub} | Unlisted: {unl} | Private: {priv}")
print(f"  Channel reports: {reported}")
print(f"{'='*60}")

# List all with privacy status
for i, v in enumerate(all_videos, 1):
    s = v["snippet"]
    p = v.get("status", {}).get("privacyStatus", "?")
    icon = {"public": "🟢", "unlisted": "🟡", "private": "🔴"}.get(p, "❓")
    title = s.get("title", "?")
    vid_id = s.get("resourceId", {}).get("videoId", "?")
    print(f"  {i:3}. {icon} [{p[:3].upper()}] {title[:60]} ({vid_id})")
