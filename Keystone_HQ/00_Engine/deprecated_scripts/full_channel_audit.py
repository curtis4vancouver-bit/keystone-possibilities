"""Full audit of all 3 Keystone YouTube channels — list every video with privacy status."""
import sys
import io
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

from youtube_api_manager import YouTubeAPIManager
import json

manager = YouTubeAPIManager(token_file="youtube_token.json")
if not manager.youtube:
    print("FATAL: No auth")
    exit(1)

CHANNELS = {
    "Keystone Possibilities": "UCu8gdU_R8XE2RvcttGa3drg",
    "Keystone Protocols": "UCxURlqMNhAtxUTpdXmlOYaw",
    "KeyStone Recomposition (OAC)": "UCMn1f9DTF_iybKmv5WlTm9Q",
}

full_report = {}

for ch_name, ch_id in CHANNELS.items():
    print(f"\n{'='*60}")
    print(f"  {ch_name} ({ch_id})")
    print(f"{'='*60}")
    
    # Get uploads playlist ID (UC -> UU)
    uploads_playlist = "UU" + ch_id[2:]
    
    videos = []
    next_page = None
    
    while True:
        try:
            playlist_items = manager.youtube.playlistItems().list(
                part="snippet,status,contentDetails",
                playlistId=uploads_playlist,
                maxResults=50,
                pageToken=next_page
            ).execute()
            
            for item in playlist_items.get("items", []):
                vid = item["snippet"]
                status = item.get("status", {})
                privacy = status.get("privacyStatus", "unknown")
                video_id = vid.get("resourceId", {}).get("videoId", "?")
                title = vid.get("title", "Untitled")
                published = vid.get("publishedAt", "?")
                
                videos.append({
                    "id": video_id,
                    "title": title,
                    "privacy": privacy,
                    "published": published[:10] if published != "?" else "?"
                })
            
            next_page = playlist_items.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            print(f"  ERROR: {e}")
            break
    
    # Count by privacy status
    public_count = sum(1 for v in videos if v["privacy"] == "public")
    private_count = sum(1 for v in videos if v["privacy"] == "private")
    unlisted_count = sum(1 for v in videos if v["privacy"] == "unlisted")
    
    print(f"  Total: {len(videos)} | Public: {public_count} | Private: {private_count} | Unlisted: {unlisted_count}")
    print()
    
    for v in videos:
        icon = {"public": "🟢", "private": "🔴", "unlisted": "🟡"}.get(v["privacy"], "⚪")
        print(f"  {icon} [{v['privacy']:>8}] {v['title'][:70]} ({v['id']}) {v['published']}")
    
    full_report[ch_name] = {
        "channel_id": ch_id,
        "total": len(videos),
        "public": public_count,
        "private": private_count,
        "unlisted": unlisted_count,
        "videos": videos
    }

# Save full report as JSON for programmatic use
with open("channel_audit_report.json", "w", encoding="utf-8") as f:
    json.dump(full_report, f, indent=2, ensure_ascii=False)

print(f"\n\nFull report saved to channel_audit_report.json")
