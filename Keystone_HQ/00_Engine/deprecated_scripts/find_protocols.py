"""Find the correct Protocols channel ID by searching."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

# Search for "Keystone Protocols" channel
print("=== Searching for Keystone Protocols channel ===")
result = yt.search().list(
    part="snippet",
    q="Keystone Protocols GLP-1",
    type="channel",
    maxResults=10
).execute()

for item in result.get("items", []):
    ch = item["snippet"]
    print(f"  Channel: {ch['channelTitle']} ({item['id']['channelId']})")
    print(f"    Desc: {ch.get('description', '')[:80]}")

# Also try searching for a known Protocols video
print("\n=== Searching for known Protocols video titles ===")
result = yt.search().list(
    part="snippet",
    q="GLP-1 Changed My Life Wolverine Stack Keystone",
    type="video",
    maxResults=5
).execute()

for item in result.get("items", []):
    vid = item["snippet"]
    print(f"  Video: {vid['title'][:60]}")
    print(f"    Channel: {vid['channelTitle']} ({vid['channelId']})")
    print(f"    Video ID: {item['id']['videoId']}")

# Try known video IDs from Protocols
print("\n=== Checking known Protocols video IDs ===")
known_protocol_ids = ["DW-VXf2GXk0", "c--naKpO5_M", "3giPCEFfVTY", "NLTSFHhT9cc", "zFUwRvTI7EU", "pBB4W2kOgQM", "PwQqt6U0kdo", "d9wBAZgZx7E", "ynSo4eOaIeU"]
for vid_id in known_protocol_ids[:3]:
    try:
        detail = yt.videos().list(part="snippet,status", id=vid_id).execute()
        if detail["items"]:
            v = detail["items"][0]
            print(f"  {v['snippet']['title'][:50]}")
            print(f"    Channel: {v['snippet']['channelTitle']} ({v['snippet']['channelId']})")
            print(f"    Privacy: {v['status']['privacyStatus']}")
            print(f"    Tags: {v['snippet'].get('tags', [])[:5]}")
    except Exception as e:
        print(f"  {vid_id}: ERROR - {e}")
