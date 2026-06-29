"""
Deep OAC Access Test — Find all private health videos and test management access.
The OAC is likely a Brand Account channel, so we need special handling.
"""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

OAC_CHANNEL_ID = "UCMn1f9DTF_iybKmv5WlTm9Q"

print("=== TEST 1: List ALL channels this account manages ===")
try:
    result = yt.channels().list(part="snippet,contentDetails,statistics", mine=True, maxResults=50).execute()
    for ch in result.get("items", []):
        print(f"  Channel: {ch['snippet']['title']} ({ch['id']})")
        print(f"    Uploads playlist: {ch['contentDetails']['relatedPlaylists']['uploads']}")
        print(f"    Videos: {ch['statistics']['videoCount']}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== TEST 2: Get OAC channel details with contentDetails ===")
try:
    result = yt.channels().list(part="snippet,contentDetails,statistics", id=OAC_CHANNEL_ID).execute()
    for ch in result.get("items", []):
        print(f"  Channel: {ch['snippet']['title']} ({ch['id']})")
        uploads = ch['contentDetails']['relatedPlaylists'].get('uploads', 'NOT FOUND')
        print(f"  Uploads playlist: {uploads}")
        print(f"  Total video count: {ch['statistics']['videoCount']}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== TEST 3: Search for ALL videos on managed channels (optimized) ===")
try:
    # Fetch uploads playlists for all mine=True channels and list videos
    ch_result = yt.channels().list(part="snippet,contentDetails", mine=True, maxResults=50).execute()
    for ch in ch_result.get("items", []):
        ch_title = ch["snippet"]["title"]
        uploads_playlist = ch['contentDetails']['relatedPlaylists']['uploads']
        print(f"  Channel: {ch_title} -> Uploads Playlist: {uploads_playlist}")
        pl_result = yt.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist,
            maxResults=10
        ).execute()
        for item in pl_result.get("items", []):
            vid = item["snippet"]
            vid_id = vid.get("resourceId", {}).get("videoId", "?")
            print(f"    - {vid['title'][:60]} ({vid_id})")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== TEST 4: List OAC videos with uploads playlist (optimized) ===")
try:
    all_ids = []
    next_page = None
    uploads_playlist = "UU" + OAC_CHANNEL_ID[2:]
    while True:
        result = yt.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist,
            maxResults=50,
            pageToken=next_page
        ).execute()
        for item in result.get("items", []):
            vid_id = item["snippet"].get("resourceId", {}).get("videoId", "?")
            all_ids.append(vid_id)
            vid = item["snippet"]
            print(f"  {vid['title'][:65]} ({vid_id})")
        next_page = result.get("nextPageToken")
        if not next_page:
            break
    print(f"\n  Total found via uploads playlist: {len(all_ids)}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== TEST 5: Use OAC uploads playlist directly ===")
try:
    # Try both UU construction and the contentDetails approach
    uploads_playlist = "UU" + OAC_CHANNEL_ID[2:]
    print(f"  Playlist ID: {uploads_playlist}")
    
    all_videos = []
    next_page = None
    while True:
        result = yt.playlistItems().list(
            part="snippet,status,contentDetails",
            playlistId=uploads_playlist,
            maxResults=50,
            pageToken=next_page
        ).execute()
        for item in result.get("items", []):
            vid = item["snippet"]
            status = item.get("status", {})
            privacy = status.get("privacyStatus", "unknown")
            video_id = vid.get("resourceId", {}).get("videoId", "?")
            all_videos.append({"id": video_id, "privacy": privacy, "title": vid.get("title", "?")})
        next_page = result.get("nextPageToken")
        if not next_page:
            break
    
    pub = sum(1 for v in all_videos if v["privacy"] == "public")
    priv = sum(1 for v in all_videos if v["privacy"] == "private")
    unl = sum(1 for v in all_videos if v["privacy"] == "unlisted")
    print(f"  Total: {len(all_videos)} | Public: {pub} | Private: {priv} | Unlisted: {unl}")
    
    for v in all_videos:
        icon = {"public": "P", "private": "X", "unlisted": "U"}.get(v["privacy"], "?")
        print(f"  [{icon}] {v['title'][:70]} ({v['id']})")
        
except Exception as e:
    print(f"  ERROR: {e}")

print("\n=== TEST 6: Get OAC video count from channel stats ===")
try:
    result = yt.channels().list(part="statistics", id=OAC_CHANNEL_ID).execute()
    stats = result["items"][0]["statistics"]
    print(f"  Channel reports {stats['videoCount']} total videos (API sees {len(all_videos)} via playlist)")
    print(f"  Hidden count = {int(stats['videoCount']) - len(all_videos)}")
except Exception as e:
    print(f"  ERROR: {e}")

# Save all discovered video IDs for later use
with open("oac_video_ids.json", "w", encoding="utf-8") as f:
    json.dump(all_videos, f, indent=2, ensure_ascii=False)
print("\nSaved to oac_video_ids.json")
