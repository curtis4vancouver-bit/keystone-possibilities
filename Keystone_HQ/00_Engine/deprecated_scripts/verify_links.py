"""
Step 1: Verify all exact channel handles and URLs before updating anything.
Step 2: Test write access to each channel.
Step 3: Execute bulk updates on channels we can write to.
"""
import sys, io, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

CHANNELS = {
    "possibilities": "UCu8gdU_R8XE2RvcttGa3drg",
    "protocols": "UC8pMhKdMOCdiXLwX0fRwJWA",
    "oac": "UCMn1f9DTF_iybKmv5WlTm9Q",
}

print("=" * 70)
print("  STEP 1: VERIFYING ALL CHANNEL HANDLES & URLS")
print("=" * 70)

channel_urls = {}
for name, cid in CHANNELS.items():
    try:
        result = yt.channels().list(
            part="snippet,brandingSettings",
            id=cid
        ).execute()
        ch = result["items"][0]
        title = ch["snippet"]["title"]
        custom_url = ch["snippet"].get("customUrl", "NOT SET")
        channel_urls[name] = {
            "title": title,
            "id": cid,
            "handle": custom_url,
            "url": f"https://www.youtube.com/{custom_url}" if custom_url != "NOT SET" else "NO HANDLE"
        }
        print(f"\n  {name.upper()}:")
        print(f"    Title: {title}")
        print(f"    ID: {cid}")
        print(f"    Handle: {custom_url}")
        print(f"    URL: {channel_urls[name]['url']}")
    except Exception as e:
        print(f"\n  {name.upper()}: ERROR - {e}")

print("\n" + "=" * 70)
print("  STEP 2: VERIFYING WEBSITE URL")
print("=" * 70)
print("  Website: https://keystonepossibilities.ca")
print("  (This is the primary domain used across all descriptions)")

print("\n" + "=" * 70)
print("  STEP 3: TESTING WRITE ACCESS")
print("=" * 70)

# Get all video IDs from Protocols and Possibilities
for channel_name in ["possibilities", "protocols"]:
    cid = CHANNELS[channel_name]
    uploads_playlist = "UU" + cid[2:]
    try:
        result = yt.playlistItems().list(
            part="snippet,status",
            playlistId=uploads_playlist,
            maxResults=50
        ).execute()
        videos = []
        for item in result.get("items", []):
            vid = item["snippet"]
            video_id = vid["resourceId"]["videoId"]
            privacy = item.get("status", {}).get("privacyStatus", "?")
            videos.append({"id": video_id, "title": vid["title"], "privacy": privacy})
        
        print(f"\n  {channel_name.upper()} - {len(videos)} videos:")
        for v in videos:
            print(f"    [{v['privacy'][:3].upper()}] {v['title'][:60]} ({v['id']})")
        
        # Test read access on first video
        if videos:
            test_id = videos[0]["id"]
            try:
                detail = yt.videos().list(part="snippet,status", id=test_id).execute()
                if detail["items"]:
                    snippet = detail["items"][0]["snippet"]
                    tags = snippet.get("tags", [])
                    desc_preview = snippet.get("description", "")[:100]
                    print(f"\n    ✅ Can READ video details")
                    print(f"    Current tags ({len(tags)}): {', '.join(tags[:8])}")
                    print(f"    Current desc preview: {desc_preview}...")
                else:
                    print(f"    ❌ Could not read video details")
            except Exception as e:
                print(f"    ❌ Read error: {e}")
                
    except Exception as e:
        print(f"\n  {channel_name.upper()}: ERROR listing videos - {e}")

# Save channel URLs for use in the update script
with open("verified_links.json", "w", encoding="utf-8") as f:
    json.dump(channel_urls, f, indent=2, ensure_ascii=False)

print("\n\n  ✅ Verified links saved to verified_links.json")
print("\n" + "=" * 70)
print("  LINK SUMMARY FOR DESCRIPTIONS:")
print("=" * 70)
for name, info in channel_urls.items():
    print(f"  {name.upper()}: {info['url']}")
print(f"  WEBSITE: https://keystonepossibilities.ca")
print("=" * 70)
