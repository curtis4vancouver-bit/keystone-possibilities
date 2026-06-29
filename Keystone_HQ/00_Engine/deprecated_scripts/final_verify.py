"""Get correct handles for Protocols and Possibilities channels."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

# Get CORRECT Protocols channel info
print("=== PROTOCOLS CHANNEL ===")
result = yt.channels().list(part="snippet,statistics,brandingSettings", id="UCxURlqMNhAtxUTpdXmlOYaw").execute()
ch = result["items"][0]
print(f"  Title: {ch['snippet']['title']}")
print(f"  Handle: {ch['snippet'].get('customUrl', 'NOT SET')}")
print(f"  Subs: {ch['statistics']['subscriberCount']}")
print(f"  Videos: {ch['statistics']['videoCount']}")

# Get Possibilities channel - check if there's a better handle
print("\n=== POSSIBILITIES CHANNEL ===")
result = yt.channels().list(part="snippet,statistics,brandingSettings", id="UCu8gdU_R8XE2RvcttGa3drg").execute()
ch = result["items"][0]
print(f"  Title: {ch['snippet']['title']}")
print(f"  Handle: {ch['snippet'].get('customUrl', 'NOT SET')}")
print(f"  Subs: {ch['statistics']['subscriberCount']}")
print(f"  Videos: {ch['statistics']['videoCount']}")

# Get OAC
print("\n=== OAC CHANNEL ===")
result = yt.channels().list(part="snippet,statistics", id="UCMn1f9DTF_iybKmv5WlTm9Q").execute()
ch = result["items"][0]
print(f"  Title: {ch['snippet']['title']}")
print(f"  Handle: {ch['snippet'].get('customUrl', 'NOT SET')}")
print(f"  Subs: {ch['statistics']['subscriberCount']}")
print(f"  Videos: {ch['statistics']['videoCount']}")

# Get ALL Protocols videos
print("\n=== ALL PROTOCOLS VIDEOS ===")
uploads = "UU" + "UCxURlqMNhAtxUTpdXmlOYaw"[2:]
result = yt.playlistItems().list(part="snippet,status", playlistId=uploads, maxResults=50).execute()
for item in result.get("items", []):
    vid = item["snippet"]
    video_id = vid["resourceId"]["videoId"]
    privacy = item.get("status", {}).get("privacyStatus", "?")
    print(f"  [{privacy[:3].upper()}] {vid['title'][:65]} ({video_id})")

# Test write access on a Protocols video
print("\n=== TESTING WRITE ACCESS ON PROTOCOLS ===")
test_vid = "DW-VXf2GXk0"
try:
    detail = yt.videos().list(part="snippet,status", id=test_vid).execute()
    if detail["items"]:
        v = detail["items"][0]
        print(f"  ✅ CAN READ: {v['snippet']['title'][:50]}")
        print(f"  Tags: {v['snippet'].get('tags', [])}")
        print(f"  Description (first 200 chars):")
        print(f"  {v['snippet'].get('description', '')[:200]}")
        
        # Try a dry-run write (update with same data to test permissions)
        snippet = v["snippet"]
        try:
            yt.videos().update(
                part="snippet",
                body={
                    "id": test_vid,
                    "snippet": {
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "tags": snippet.get("tags", []),
                        "categoryId": snippet["categoryId"]
                    }
                }
            ).execute()
            print(f"  ✅ CAN WRITE! Full update access confirmed!")
        except Exception as e:
            print(f"  ❌ CANNOT WRITE: {e}")
except Exception as e:
    print(f"  ❌ ERROR: {e}")
