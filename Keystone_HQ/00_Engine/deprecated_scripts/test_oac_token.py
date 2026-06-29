"""Test new OAC token — check which channel it authenticated as and if we can see unlisted videos."""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load OAC token
creds = Credentials.from_authorized_user_file("youtube_token_oac.json")
youtube = build("youtube", "v3", credentials=creds)

# Test 1: What channel does mine=True return?
print("=== TEST 1: mine=True channel ===")
result = youtube.channels().list(part="snippet,statistics", mine=True).execute()
for ch in result.get("items", []):
    print(f"  Channel: {ch['snippet']['title']}")
    print(f"  ID: {ch['id']}")
    print(f"  Videos: {ch['statistics']['videoCount']}")

# Test 2: Can we list OAC videos by channel ID (optimized)?
OAC_ID = "UCMn1f9DTF_iybKmv5WlTm9Q"
print(f"\n=== TEST 2: List OAC videos by uploads playlist (optimized) ===")
uploads_playlist = "UU" + OAC_ID[2:]
result = youtube.playlistItems().list(
    part="snippet", playlistId=uploads_playlist, maxResults=5
).execute()
print(f"  Found {result.get('pageInfo',{}).get('totalResults',0)} videos via uploads playlist")
for item in result.get("items", []):
    print(f"  - {item['snippet']['title']}")

# Test 3: Can we see unlisted videos? Try listing ALL including unlisted
print(f"\n=== TEST 3: Channel stats for OAC ===")
result = youtube.channels().list(part="statistics,contentDetails", id=OAC_ID).execute()
for ch in result.get("items", []):
    print(f"  Total videos (public count): {ch['statistics']['videoCount']}")
    uploads_playlist = ch['contentDetails']['relatedPlaylists']['uploads']
    print(f"  Uploads playlist: {uploads_playlist}")
    
    # Try to list from uploads playlist (should include unlisted)
    pl_result = youtube.playlistItems().list(
        part="snippet,status", playlistId=uploads_playlist, maxResults=50
    ).execute()
    total = pl_result.get("pageInfo", {}).get("totalResults", 0)
    print(f"  Playlist items visible: {total}")
    
    statuses = {}
    for item in pl_result.get("items", []):
        status = item.get("status", {}).get("privacyStatus", "unknown")
        statuses[status] = statuses.get(status, 0) + 1
        if status != "public":
            print(f"  >> NON-PUBLIC: [{status}] {item['snippet']['title'][:60]}")
    
    print(f"\n  Privacy breakdown: {statuses}")

print("\n=== DONE ===")
