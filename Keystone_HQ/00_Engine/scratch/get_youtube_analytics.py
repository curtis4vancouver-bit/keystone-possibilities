"""Fetch live YouTube analytics (views, likes, comments, duration) for all uploaded videos on the Keystone Protocols channel."""
import os
import sys
import io
import json
import logging
from datetime import datetime

# Setup absolute paths to import from Master Brain
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_iso8601_duration(duration_str):
    """Simple parser for ISO 8601 duration format (e.g. PT8M20S, PT43S)"""
    import re
    # Match patterns like PT1H2M3S or PT43S
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration_str)
    if not match:
        return 0
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def run_analytics():
    # Target channel details
    CHANNEL_NAME = "Keystone Protocols"
    CHANNEL_ID = "UCxURlqMNhAtxUTpdXmlOYaw"
    UPLOADS_PLAYLIST = "UUxURlqMNhAtxUTpdXmlOYaw"
    
    # Initialize the API Manager with the Protocols token
    logger.info("Initializing YouTube API Manager...")
    # Use the protocols token in the parent folder
    token_path = os.path.join(PARENT_DIR, "youtube_token.json")
    manager = YouTubeAPIManager(token_file=token_path)
    
    if not manager.youtube:
        logger.error("Failed to authenticate YouTube API service.")
        return
        
    logger.info("Retrieving all video uploads...")
    videos_list = []
    next_page = None
    
    while True:
        try:
            playlist_items = manager.youtube.playlistItems().list(
                part="snippet,status,contentDetails",
                playlistId=UPLOADS_PLAYLIST,
                maxResults=50,
                pageToken=next_page
            ).execute()
            
            for item in playlist_items.get("items", []):
                snippet = item["snippet"]
                video_id = snippet.get("resourceId", {}).get("videoId")
                title = snippet.get("title", "Untitled")
                published = snippet.get("publishedAt", "?")
                
                videos_list.append({
                    "id": video_id,
                    "title": title,
                    "published": published[:10] if published != "?" else "?"
                })
                
            next_page = playlist_items.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            logger.error(f"Error fetching uploads playlist: {e}")
            break
            
    if not videos_list:
        logger.warning("No uploads found on the channel.")
        return
        
    logger.info(f"Found {len(videos_list)} videos. Fetching detailed statistics...")
    
    # Group video IDs into batches of 50 for the videos().list API call
    video_ids = [v["id"] for v in videos_list]
    detailed_videos = {}
    
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        ids_str = ",".join(batch)
        try:
            stats_response = manager.youtube.videos().list(
                id=ids_str,
                part="statistics,contentDetails,snippet"
            ).execute()
            
            for item in stats_response.get("items", []):
                v_id = item["id"]
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                content_details = item.get("contentDetails", {})
                
                v_title = snippet.get("title", "Untitled")
                duration_raw = content_details.get("duration", "PT0S")
                duration_sec = parse_iso8601_duration(duration_raw)
                
                # Format duration to MM:SS
                min_part = duration_sec // 60
                sec_part = duration_sec % 60
                duration_formatted = f"{min_part}:{sec_part:02d}"
                
                # Check if it's likely a Short (9:16 vertical and < 60s)
                description = snippet.get("description", "")
                tags = snippet.get("tags", [])
                is_short = (duration_sec <= 60) or ("#shorts" in v_title.lower()) or ("#short" in v_title.lower()) or ("#shorts" in description.lower())
                
                detailed_videos[v_id] = {
                    "id": v_id,
                    "title": v_title,
                    "published": snippet.get("publishedAt", "")[:10], # Use exact publish date
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "duration_sec": duration_sec,
                    "duration": duration_formatted,
                    "type": "Short" if is_short else "Long-Form",
                    "tags": tags
                }
        except Exception as e:
            logger.error(f"Error fetching stats batch: {e}")
            
    # Merge statistics back into the initial list
    final_videos = []
    for v in videos_list:
        v_id = v["id"]
        if v_id in detailed_videos:
            v_data = detailed_videos[v_id]
            v.update(v_data)
            final_videos.append(v)
            
    # Sort videos by published date descending (newest first)
    final_videos.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    # Calculate channel totals
    total_views = sum(v["views"] for v in final_videos)
    total_likes = sum(v["likes"] for v in final_videos)
    total_comments = sum(v["comments"] for v in final_videos)
    long_count = sum(1 for v in final_videos if v["type"] == "Long-Form")
    shorts_count = sum(1 for v in final_videos if v["type"] == "Short")
    
    # Structure full report
    report = {
        "channel_name": CHANNEL_NAME,
        "channel_id": CHANNEL_ID,
        "timestamp": datetime.now().isoformat(),
        "totals": {
            "total_videos": len(final_videos),
            "long_form_count": long_count,
            "shorts_count": shorts_count,
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments
        },
        "videos": final_videos
    }
    
    # Save JSON report
    report_json_path = os.path.join(SCRIPT_DIR, "youtube_analytics_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    # Generate beautifully formatted Markdown report
    md_path = os.path.join(SCRIPT_DIR, "youtube_analytics_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 📊 KEYSTONE PROTOCOLS — YOUTUBE ANALYTICS DIGEST\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n")
        f.write(f"**Channel:** {CHANNEL_NAME} ({CHANNEL_ID})\n\n")
        
        f.write(f"## 📈 Channel Totals\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|---|---|\n")
        f.write(f"| **Total Videos Uploaded** | {len(final_videos)} |\n")
        f.write(f"| ├— *Long-Form (16:9)* | {long_count} |\n")
        f.write(f"| └— *Shorts (9:16)* | {shorts_count} |\n")
        f.write(f"| **Cumulative Views** | {total_views:,} |\n")
        f.write(f"| **Cumulative Likes** | {total_likes:,} |\n")
        f.write(f"| **Cumulative Comments** | {total_comments:,} |\n\n")
        
        f.write(f"## 🏆 Top Performing Videos (by Views)\n")
        sorted_by_views = sorted(final_videos, key=lambda x: x["views"], reverse=True)
        f.write(f"| Rank | Title | Format | Views | Likes | Comments | Published |\n")
        f.write(f"|---|---|---|---|---|---|---|\n")
        for idx, v in enumerate(sorted_by_views[:5], 1):
            f.write(f"| #{idx} | **{v['title']}** | `{v['type']}` | {v['views']:,} | {v['likes']:,} | {v['comments']:,} | {v['published']} |\n")
            
        f.write(f"\n## 🎬 Upload Timeline & Serialized Pacing\n")
        f.write(f"Here is the complete chronological log of uploads, enabling us to track script continuity and series sequencing:\n\n")
        
        f.write(f"| Date | Format | Title | Duration | Views | Likes | Video ID |\n")
        f.write(f"|---|---|---|---|---|---|---|\n")
        for v in final_videos:
            format_emoji = "📺" if v["type"] == "Long-Form" else "📱"
            f.write(f"| {v['published']} | {format_emoji} `{v['type']}` | {v['title']} | {v['duration']} | {v['views']:,} | {v['likes']:,} | [{v['id']}](https://youtube.com/watch?v={v['id']}) |\n")
            
    print(f"\n=============================================")
    print(f"   {CHANNEL_NAME} LIVE ANALYTICS DIGEST")
    print(f"=============================================")
    print(f"  Total Videos: {len(final_videos)} (Long: {long_count} | Shorts: {shorts_count})")
    print(f"  Total Views:  {total_views:,}")
    print(f"  Total Likes:  {total_likes:,}")
    print(f"  Total Comments: {total_comments:,}")
    print(f"\nSaved JSON: {report_json_path}")
    print(f"Saved Markdown: {md_path}")
    print(f"=============================================")

if __name__ == "__main__":
    run_analytics()
