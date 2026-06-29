import sys
import os

sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
from youtube_api_manager import YouTubeAPIManager

def check_token(filename):
    print(f"\nChecking token: {filename}")
    mgr = YouTubeAPIManager(token_file=filename)
    if not mgr.youtube:
        print("Failed to initialize.")
        return
    try:
        req = mgr.youtube.channels().list(part="snippet", mine=True)
        res = req.execute()
        if res.get("items"):
            print("Channel Name:", res["items"][0]["snippet"]["title"])
            print("Channel ID:", res["items"][0]["id"])
        else:
            print("No channel found.")
    except Exception as e:
        print(f"Error: {e}")

check_token(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token.json")
check_token(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token_oac.json")
