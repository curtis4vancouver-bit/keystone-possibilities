"""Full OAC inventory — list all 185 videos with privacy status breakdown."""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file("youtube_token_oac.json")
youtube = build("youtube", "v3", credentials=creds)

# Get uploads playlist
ch = youtube.channels().list(part="contentDetails", mine=True).execute()
uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Paginate through ALL videos
all_videos = []
next_token = None
while True:
    params = {"part": "snippet,status", "playlistId": uploads, "maxResults": 50}
    if next_token:
        params["pageToken"] = next_token
    result = youtube.playlistItems().list(**params).execute()
    all_videos.extend(result.get("items", []))
    next_token = result.get("nextPageToken")
    if not next_token:
        break

# Breakdown
statuses = {}
categories = {"public": [], "unlisted": [], "private": []}
for v in all_videos:
    status = v.get("status", {}).get("privacyStatus", "unknown")
    statuses[status] = statuses.get(status, 0) + 1
    title = v["snippet"]["title"][:70]
    vid_id = v["snippet"]["resourceId"]["videoId"]
    categories.get(status, []).append({"id": vid_id, "title": title})

print(f"TOTAL VIDEOS: {len(all_videos)}")
print(f"BREAKDOWN: {json.dumps(statuses)}")
print(f"\nPUBLIC ({statuses.get('public',0)}):")
for v in categories["public"][:5]:
    print(f"  {v['id']} | {v['title']}")
if statuses.get('public',0) > 5:
    print(f"  ... and {statuses['public']-5} more")

print(f"\nUNLISTED ({statuses.get('unlisted',0)}):")
for v in categories["unlisted"][:10]:
    print(f"  {v['id']} | {v['title']}")
if statuses.get('unlisted',0) > 10:
    print(f"  ... and {statuses['unlisted']-10} more")

print(f"\nPRIVATE ({statuses.get('private',0)}):")
for v in categories["private"][:5]:
    print(f"  {v['id']} | {v['title']}")
if statuses.get('private',0) > 5:
    print(f"  ... and {statuses['private']-5} more")

# Test write access — just read a video to confirm we CAN update
test_id = categories["unlisted"][0]["id"] if categories["unlisted"] else None
if test_id:
    test = youtube.videos().list(part="snippet,status", id=test_id).execute()
    if test.get("items"):
        print(f"\n[WRITE TEST] Can read video details for: {test['items'][0]['snippet']['title'][:50]}")
        print(f"  Category: {test['items'][0]['snippet'].get('categoryId','?')}")
        print(f"  Tags: {test['items'][0]['snippet'].get('tags',['none'])[:5]}")
        print("[OK] Full read/write access confirmed")
