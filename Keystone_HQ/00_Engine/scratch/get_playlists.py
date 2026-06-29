import sys
import os

sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
from youtube_api_manager import YouTubeAPIManager

mgr = YouTubeAPIManager(token_file=r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token.json")

req = mgr.youtube.playlists().list(part="snippet", mine=True, maxResults=50)
res = req.execute()

print("Playlists found:")
for item in res.get("items", []):
    print(f"- {item['snippet']['title']}: {item['id']}")
