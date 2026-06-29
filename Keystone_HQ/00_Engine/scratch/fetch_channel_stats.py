import os
import sys
import json
import logging

# Set working directory to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from youtube_api_manager import YouTubeAPIManager

logging.basicConfig(level=logging.WARNING)

# We use the OAC token file because it successfully refreshes and authenticates.
# Since channel statistics are public, we can query any channel ID using this single authenticated service.
TOKEN_FILE = os.path.join(PROJECT_ROOT, "youtube_token_oac.json")
if not os.path.exists(TOKEN_FILE):
    TOKEN_FILE = os.path.join(PROJECT_ROOT, "youtube_token.json")

CHANNELS = {
    "Keystone Possibilities": "UCu8gdU_R8XE2RvcttGa3drg",
    "Keystone Protocols": "UCxURlqMNhAtxUTpdXmlOYaw",
    "Keystone Recomposition (OAC)": "UCMn1f9DTF_iybKmv5WlTm9Q"
}

print("============================================================")
print("     FETCHING LIVE KEYSTONE YOUTUBE CHANNEL METRICS (VIA PUBLIC QUERY)")
print("============================================================")

stats_report = {}

try:
    manager = YouTubeAPIManager(token_file=TOKEN_FILE)
    if not manager.youtube:
        print("[-] Failed to authenticate YouTube API manager.")
        sys.exit(1)
        
    for ch_name, ch_id in CHANNELS.items():
        try:
            result = manager.youtube.channels().list(
                part="snippet,statistics",
                id=ch_id
            ).execute()
            
            if not result.get("items"):
                print(f"[-] {ch_name}: Channel not found via API ({ch_id})")
                continue
                
            ch_data = result["items"][0]
            stats = ch_data["statistics"]
            snippet = ch_data["snippet"]
            
            sub_count = stats.get("subscriberCount", "0")
            view_count = stats.get("viewCount", "0")
            video_count = stats.get("videoCount", "0")
            
            print(f"[+] {ch_name}:")
            print(f"    - Subscribers: {int(sub_count):,}" if sub_count.isdigit() else f"    - Subscribers: {sub_count}")
            print(f"    - Total Views: {int(view_count):,}" if view_count.isdigit() else f"    - Views: {view_count}")
            print(f"    - Video Count: {int(video_count):,}" if video_count.isdigit() else f"    - Videos: {video_count}")
            print(f"    - Channel ID:  {ch_id}")
            print()
            
            stats_report[ch_name] = {
                "channel_id": ch_id,
                "title": snippet.get("title"),
                "subscribers": sub_count,
                "views": view_count,
                "videos": video_count
            }
        except Exception as ex:
            print(f"[-] {ch_name}: Error fetching stats for ID {ch_id} - {ex}")
            
except Exception as e:
    print(f"[-] Fatal auth error: {e}")

# Save results
output_file = os.path.join(PROJECT_ROOT, "scratch", "live_youtube_stats.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(stats_report, f, indent=2, ensure_ascii=False)

print(f"Done. Detailed stats saved to scratch/live_youtube_stats.json")
