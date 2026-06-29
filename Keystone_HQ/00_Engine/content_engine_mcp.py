"""
Keystone Content Engine MCP v1.0
Cross-channel content management, SEO keyword sync, content calendar, and analytics.
Works across all 3 YouTube channels + WordPress blog.
"""
import os
import sys
import io
import json
import time
import logging
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# ── CRITICAL: MCP STDOUT GUARD ──────────────────────────────────────
# Suppress httpx/MCP loggers that print request logs to stdout,
# which corrupts the JSON-RPC protocol with non-JSON text.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("mcp").setLevel(logging.WARNING)
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)

from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

try:
    from mcp_error_handler import safe_mcp_tool
except ImportError:
    # Fallback if execution environment differs
    def safe_mcp_tool(func): return func

mcp = FastMCP("Keystone Content Engine")

# ── Token Management ──────────────────────────────────────────────
# Per-channel token files — matches CHANNEL_TOKEN_MAP in youtube_mcp.py
CHANNEL_TOKEN_FILES = {
    "possibilities": os.path.join(SCRIPT_DIR, "youtube_token_possibilities.json"),
    "protocols": os.path.join(SCRIPT_DIR, "youtube_token.json"),
    "oac": os.path.join(SCRIPT_DIR, "youtube_token_oac.json"),
}
_yt_cache = {}

CHANNELS = {
    "possibilities": {"id": "UCu8gdU_R8XE2RvcttGa3drg", "niche": "construction", "handle": "@KeystonePossibilities"},
    "protocols":     {"id": "UCxURlqMNhAtxUTpdXmlOYaw", "niche": "health",       "handle": "@KeystoneProtocols"},
    "oac":           {"id": "UCMn1f9DTF_iybKmv5WlTm9Q", "niche": "music",        "handle": "@KeyStoneRecomposition"},
}

# Master keyword sets per channel
MASTER_KEYWORDS = {
    "possibilities": [
        "luxury construction Vancouver", "custom home builder", "project management Vancouver",
        "BC builder", "luxury renovation", "North Shore construction", "West Vancouver homes",
        "construction project manager", "Keystone Possibilities", "luxury home builder BC",
        "Vancouver renovation contractor", "custom build Vancouver"
    ],
    "protocols": [
        "GLP-1 muscle loss", "BPC-157 peptide", "men over 40 fitness", "peptide protocol",
        "tirzepatide muscle", "Wolverine Stack", "TB-500 recovery", "GHK-Cu skin",
        "testosterone optimization", "body recomposition over 40", "Keystone Protocols",
        "peptide stacking", "GLP-1 side effects", "men's health over 40"
    ],
    "oac": [
        "deep house", "atmospheric deep house", "workout music", "focus music",
        "healing frequencies", "study music", "deep house mix 2026", "electronic music",
        "Keystone Recomposition", "ambient deep house", "meditation music",
        "binaural beats music", "gym motivation music"
    ],
}

# Cross-channel links (for description footers)
CROSS_LINKS = {
    "possibilities": (
        "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏗️ KEYSTONE POSSIBILITIES — Luxury Construction & Project Management\n"
        "🔬 Health & Protocols → https://www.youtube.com/@KeystoneProtocols\n"
        "🎵 Focus Music for Builders → https://www.youtube.com/@KeyStoneRecomposition\n"
        "🌐 Website → https://www.keystonepossibilities.com\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
    "protocols": (
        "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔬 KEYSTONE PROTOCOLS — GLP-1, Peptides & Men's Health Over 40\n"
        "⚠️ Not medical advice. Consult your physician before starting any protocol.\n"
        "🏗️ Construction & PM → https://www.youtube.com/@KeystonePossibilities\n"
        "🎵 Workout & Focus Music → https://www.youtube.com/@KeyStoneRecomposition\n"
        "🌐 Blog → https://keystonerecomposition.com\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
    "oac": (
        "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎵 KEYSTONE RECOMPOSITION — Deep House for Focus, Flow & Recovery\n"
        "Available on Spotify, Apple Music, Amazon Music & YouTube Music\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
}


def _get_youtube(channel_key):
    """Get YouTube API client for the specified channel using per-channel tokens."""
    if channel_key not in CHANNELS:
        return None
    if channel_key not in _yt_cache:
        token_path = CHANNEL_TOKEN_FILES.get(channel_key)
        if not token_path or not os.path.exists(token_path):
            return None
        creds = Credentials.from_authorized_user_file(token_path)
        _yt_cache[channel_key] = build("youtube", "v3", credentials=creds, cache_discovery=False)
    return _yt_cache[channel_key]


def _get_all_videos(channel_key, max_results=500):
    """Fetch all videos from a channel's uploads playlist."""
    yt = _get_youtube(channel_key)
    ch_id = CHANNELS[channel_key]["id"]
    uploads = "UU" + ch_id[2:]
    videos = []
    next_page = None
    while len(videos) < max_results:
        result = yt.playlistItems().list(
            part="snippet,status", playlistId=uploads,
            maxResults=min(50, max_results - len(videos)), pageToken=next_page
        ).execute()
        for item in result.get("items", []):
            vid = item["snippet"]
            videos.append({
                "video_id": vid.get("resourceId", {}).get("videoId"),
                "title": vid.get("title", ""),
                "privacy": item.get("status", {}).get("privacyStatus", "unknown"),
                "published": vid.get("publishedAt", "")[:10],
            })
        next_page = result.get("nextPageToken")
        if not next_page:
            break
    return videos


# ── TOOL 1: Full Empire Status ──────────────────────────────────
@mcp.tool()
@safe_mcp_tool
def empire_status() -> str:
    """
    Returns a complete status report of all 3 Keystone YouTube channels
    including video counts, privacy breakdowns, and last upload dates.
    """
    report = {"timestamp": datetime.now().isoformat(), "channels": {}}
    for key, ch in CHANNELS.items():
        yt = _get_youtube(key)
        if not yt:
            report["channels"][key] = {"error": "No API access"}
            continue
        r = yt.channels().list(part="snippet,statistics,contentDetails", id=ch["id"]).execute()
        if not r.get("items"):
            continue
        item = r["items"][0]
        uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
        pl = yt.playlistItems().list(part="status", playlistId=uploads, maxResults=1).execute()
        total = pl.get("pageInfo", {}).get("totalResults", 0)
        # Get latest video
        latest = yt.playlistItems().list(part="snippet", playlistId=uploads, maxResults=1).execute()
        last_upload = "none"
        if latest.get("items"):
            last_upload = latest["items"][0]["snippet"].get("publishedAt", "unknown")[:10]
        report["channels"][key] = {
            "name": item["snippet"]["title"],
            "handle": ch["handle"],
            "subscribers": item["statistics"].get("subscriberCount", "hidden"),
            "public_videos": int(item["statistics"]["videoCount"]),
            "total_videos": total,
            "unlisted": total - int(item["statistics"]["videoCount"]),
            "total_views": item["statistics"]["viewCount"],
            "niche": ch["niche"],
            "last_upload": last_upload,
        }
    return json.dumps(report, indent=2, ensure_ascii=False)


# ── TOOL 2: SEO Keyword Audit ──────────────────────────────────
@mcp.tool()
@safe_mcp_tool
def seo_keyword_audit(channel: str = "all") -> str:
    """
    Audits tags/keywords across all videos on a channel (or all channels).
    Returns which master keywords are present, missing, and tag frequency analysis.
    Args:
        channel: 'possibilities', 'protocols', 'oac', or 'all'
    """
    channels_to_check = [channel] if channel != "all" else list(CHANNELS.keys())
    report = {}
    for ch_key in channels_to_check:
        yt = _get_youtube(ch_key)
        if not yt:
            report[ch_key] = {"error": "No API access"}
            continue
        videos = _get_all_videos(ch_key)
        public_vids = [v for v in videos if v["privacy"] != "private"]
        master_kw = MASTER_KEYWORDS.get(ch_key, [])
        tag_freq = {}
        videos_missing_tags = []
        videos_with_cross_links = 0
        
        # Batch video details in groups of 50 to optimize API quota and execution speed
        for i in range(0, len(public_vids), 50):
            batch_vids = public_vids[i:i+50]
            batch_ids = ",".join(v["video_id"] for v in batch_vids)
            try:
                detail = yt.videos().list(part="snippet", id=batch_ids).execute()
                for item in detail.get("items", []):
                    snippet = item.get("snippet", {})
                    tags = snippet.get("tags", [])
                    desc = snippet.get("description", "")
                    title = snippet.get("title", "")
                    
                    if not tags:
                        videos_missing_tags.append(title[:50])
                    for t in tags:
                        t_lower = t.lower()
                        tag_freq[t_lower] = tag_freq.get(t_lower, 0) + 1
                    # Check cross-links
                    if "youtube.com/@" in desc or "keystonepossibilities.com" in desc or "keystonerecomposition.com" in desc:
                        videos_with_cross_links += 1
            except Exception as e:
                print(f"Error fetching batch: {str(e)}")
        # Check which master keywords appear
        kw_coverage = {}
        for kw in master_kw:
            kw_lower = kw.lower()
            found = sum(1 for t, c in tag_freq.items() if kw_lower in t)
            kw_coverage[kw] = found
        missing_kw = [k for k, v in kw_coverage.items() if v == 0]
        top_tags = sorted(tag_freq.items(), key=lambda x: -x[1])[:15]
        report[ch_key] = {
            "total_videos_checked": len(videos),
            "videos_missing_tags": len(videos_missing_tags),
            "videos_with_cross_links": videos_with_cross_links,
            "master_keyword_coverage": f"{len(master_kw) - len(missing_kw)}/{len(master_kw)}",
            "missing_keywords": missing_kw[:10],
            "top_15_tags": [{"tag": t, "count": c} for t, c in top_tags],
            "videos_needing_tags": videos_missing_tags[:5],
        }
    return json.dumps(report, indent=2, ensure_ascii=False)


# ── TOOL 3: Sync Cross-Channel Links ──────────────────────────
@mcp.tool()
@safe_mcp_tool
def sync_cross_links(channel: str, dry_run: bool = True) -> str:
    """
    Ensures all videos on a channel have the standard cross-channel link footer
    in their descriptions. Appends the footer if missing.
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        dry_run: If True, shows what would change without making changes.
    """
    yt = _get_youtube(channel)
    if not yt:
        return f"ERROR: No API access for {channel}"
    footer = CROSS_LINKS.get(channel, "")
    if not footer:
        return f"ERROR: No footer template for {channel}"
    videos = _get_all_videos(channel)
    would_update = []
    updated = []
    skipped = []
    for v in videos:
        if v["privacy"] == "private":
            continue
        detail = yt.videos().list(part="snippet,status", id=v["video_id"]).execute()
        if not detail.get("items"):
            continue
        snippet = detail["items"][0]["snippet"]
        desc = snippet.get("description", "")
        # Check if footer already exists (check for the separator)
        if "━━━━━━━━" in desc:
            skipped.append(v["title"][:40])
            continue
        if dry_run:
            would_update.append(v["title"][:50])
        else:
            snippet["description"] = desc + footer
            yt.videos().update(part="snippet", body={"id": v["video_id"], "snippet": snippet}).execute()
            updated.append(v["title"][:50])
            time.sleep(0.5)  # Rate limiting

    result = {
        "channel": channel,
        "dry_run": dry_run,
        "already_have_footer": len(skipped),
    }
    if dry_run:
        result["would_update"] = len(would_update)
        result["preview"] = would_update[:10]
    else:
        result["updated"] = len(updated)
        result["updated_titles"] = updated[:10]
    return json.dumps(result, indent=2, ensure_ascii=False)


# ── TOOL 4: Inject Master Tags ────────────────────────────────
@mcp.tool()
@safe_mcp_tool
def inject_master_tags(channel: str, dry_run: bool = True) -> str:
    """
    Ensures all videos on a channel have the master keyword set in their tags.
    Merges with existing tags (doesn't replace).
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        dry_run: If True, previews without making changes.
    """
    yt = _get_youtube(channel)
    if not yt:
        return f"ERROR: No API access for {channel}"
    master_tags = MASTER_KEYWORDS.get(channel, [])
    if not master_tags:
        return f"ERROR: No master tags for {channel}"
    videos = _get_all_videos(channel)
    results = {"channel": channel, "dry_run": dry_run, "updated": 0, "skipped": 0, "details": []}
    for v in videos:
        if v["privacy"] == "private":
            continue
        detail = yt.videos().list(part="snippet", id=v["video_id"]).execute()
        if not detail.get("items"):
            continue
        snippet = detail["items"][0]["snippet"]
        existing = set(t.lower() for t in snippet.get("tags", []))
        to_add = [t for t in master_tags if t.lower() not in existing]
        if not to_add:
            results["skipped"] += 1
            continue
        if dry_run:
            results["details"].append({"title": v["title"][:40], "missing_tags": len(to_add), "sample": to_add[:3]})
        else:
            new_tags = list(snippet.get("tags", [])) + to_add
            # YouTube tag limit is 500 chars total
            total_chars = sum(len(t) for t in new_tags)
            while total_chars > 480 and new_tags:
                removed = new_tags.pop()
                total_chars -= len(removed)
            snippet["tags"] = new_tags
            yt.videos().update(part="snippet", body={"id": v["video_id"], "snippet": snippet}).execute()
            results["updated"] += 1
            time.sleep(0.5)
    if dry_run:
        results["would_update"] = len(results["details"])
        results["details"] = results["details"][:10]
    return json.dumps(results, indent=2, ensure_ascii=False)


# ── TOOL 5: Content Calendar ──────────────────────────────────
@mcp.tool()
@safe_mcp_tool
def content_calendar(weeks_ahead: int = 4) -> str:
    """
    Generates a content calendar for the next N weeks based on the publishing schedule:
    - Protocols: Tuesday & Thursday 5:30 AM PT
    - Possibilities: Monday 6:00 AM PT
    - OAC: Friday (music releases)
    Shows what's due, what's published, and gaps.
    Args:
        weeks_ahead: Number of weeks to plan (default 4)
    """
    today = datetime.now()
    schedule = []
    for week in range(weeks_ahead):
        week_start = today + timedelta(weeks=week, days=-today.weekday())
        mon = week_start
        tue = week_start + timedelta(days=1)
        thu = week_start + timedelta(days=3)
        fri = week_start + timedelta(days=4)
        week_num = f"Week {week + 1} ({mon.strftime('%b %d')} - {(mon + timedelta(days=6)).strftime('%b %d')})"
        slots = [
            {"day": "Monday", "date": mon.strftime("%Y-%m-%d"), "channel": "possibilities", "type": "Construction/PM Long-form", "status": "planned"},
            {"day": "Tuesday", "date": tue.strftime("%Y-%m-%d"), "channel": "protocols", "type": "Health/Peptide Long-form", "time": "5:30 AM PT", "status": "planned"},
            {"day": "Thursday", "date": thu.strftime("%Y-%m-%d"), "channel": "protocols", "type": "Health/GLP-1 Short or Long-form", "time": "5:30 AM PT", "status": "planned"},
            {"day": "Friday", "date": fri.strftime("%Y-%m-%d"), "channel": "oac", "type": "Music Release / Mix", "status": "planned"},
        ]
        # Mark past dates
        for slot in slots:
            slot_date = datetime.strptime(slot["date"], "%Y-%m-%d")
            if slot_date < today:
                slot["status"] = "past"
        schedule.append({"week": week_num, "slots": slots})
    return json.dumps({"calendar": schedule, "total_slots": weeks_ahead * 4}, indent=2, ensure_ascii=False)


# ── TOOL 6: NotebookLM Prep ──────────────────────────────────
@mcp.tool()
@safe_mcp_tool
def notebooklm_prep() -> str:
    """
    Packages all Research Archives and Master Brain docs into a manifest
    for upload to Google NotebookLM. Returns file paths and sizes.
    """
    archives_dir = os.path.join(SCRIPT_DIR, "Master_Docs", "Research_Archives")
    master_dir = os.path.join(SCRIPT_DIR, "Master_Docs")
    files = []
    # Research Archives
    if os.path.isdir(archives_dir):
        for f in sorted(os.listdir(archives_dir)):
            if f.endswith(".md"):
                fp = os.path.join(archives_dir, f)
                size_kb = os.path.getsize(fp) / 1024
                files.append({"file": f, "path": fp, "size_kb": round(size_kb, 1), "category": "research_archive"})
    # Master docs (top level)
    if os.path.isdir(master_dir):
        for f in sorted(os.listdir(master_dir)):
            fp = os.path.join(master_dir, f)
            if f.endswith(".md") and os.path.isfile(fp):
                size_kb = os.path.getsize(fp) / 1024
                files.append({"file": f, "path": fp, "size_kb": round(size_kb, 1), "category": "master_doc"})
    total_kb = sum(f["size_kb"] for f in files)
    return json.dumps({
        "total_files": len(files),
        "total_size_kb": round(total_kb, 1),
        "notebooklm_limit": "50 sources per notebook, 500K words per source",
        "instruction": "Upload these files to notebooklm.google.com. Create one notebook per category or one master notebook.",
        "files": files
    }, indent=2, ensure_ascii=False)


# ── TOOL 7: Cross-Channel Analytics ──────────────────────────
@mcp.tool()
@safe_mcp_tool
def channel_analytics(channel: str = "all") -> str:
    """
    Pulls view counts, engagement metrics, and top-performing videos for a channel.
    Args:
        channel: 'possibilities', 'protocols', 'oac', or 'all'
    """
    channels_to_check = [channel] if channel != "all" else list(CHANNELS.keys())
    report = {}
    for ch_key in channels_to_check:
        yt = _get_youtube(ch_key)
        if not yt:
            continue
        videos = _get_all_videos(ch_key)
        public_vids = [v for v in videos if v["privacy"] == "public"]
        # Get stats for public videos
        video_stats = []
        for i in range(0, len(public_vids), 50):
            batch_ids = ",".join(v["video_id"] for v in public_vids[i:i+50])
            stats = yt.videos().list(part="statistics,snippet", id=batch_ids).execute()
            for item in stats.get("items", []):
                video_stats.append({
                    "title": item["snippet"]["title"][:60],
                    "views": int(item["statistics"].get("viewCount", 0)),
                    "likes": int(item["statistics"].get("likeCount", 0)),
                    "comments": int(item["statistics"].get("commentCount", 0)),
                })
        # Sort by views
        video_stats.sort(key=lambda x: -x["views"])
        total_views = sum(v["views"] for v in video_stats)
        total_likes = sum(v["likes"] for v in video_stats)
        report[ch_key] = {
            "total_public_videos": len(public_vids),
            "total_views": total_views,
            "total_likes": total_likes,
            "avg_views_per_video": round(total_views / max(len(video_stats), 1)),
            "top_5_videos": video_stats[:5],
            "lowest_5_videos": video_stats[-5:] if len(video_stats) > 5 else [],
        }
    return json.dumps(report, indent=2, ensure_ascii=False)


# ── TOOL 8: Generate Video Package ────────────────────────────
@mcp.tool()
@safe_mcp_tool
def generate_video_package(channel: str, topic: str, target_keywords: list = None) -> str:
    """
    Generates a complete video upload package: optimized title options, description
    with cross-links, tags from master keyword set + custom, and scheduling recommendation.
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        topic: The video topic/subject
        target_keywords: Optional additional keywords to include
    """
    master_tags = MASTER_KEYWORDS.get(channel, [])
    custom_tags = target_keywords or []
    all_tags = list(set(master_tags + custom_tags))
    # Trim to 500 char limit
    total_chars = sum(len(t) for t in all_tags)
    while total_chars > 480 and all_tags:
        all_tags.pop()
        total_chars = sum(len(t) for t in all_tags)
    schedule_map = {
        "protocols": {"days": "Tuesday or Thursday", "time": "5:30 AM PT"},
        "possibilities": {"days": "Monday", "time": "6:00 AM PT"},
        "oac": {"days": "Friday", "time": "12:00 PM PT"},
    }
    footer = CROSS_LINKS.get(channel, "")
    package = {
        "channel": channel,
        "topic": topic,
        "title_options": [
            f"{topic} | What Men Over 40 Need to Know" if channel == "protocols" else topic,
            f"The Truth About {topic}" if channel == "protocols" else f"{topic} | Keystone Possibilities",
            f"{topic} — Full Breakdown" if channel == "protocols" else topic,
        ],
        "description_template": f"[HOOK — 2 sentences about {topic}]\n\n[BODY — key points]\n\n[TIMESTAMPS]\n0:00 — Introduction\n0:30 — [Section 1]\n...\n{footer}",
        "tags": all_tags,
        "tag_count": len(all_tags),
        "category_id": "27" if channel == "protocols" else "22" if channel == "possibilities" else "10",
        "schedule": schedule_map.get(channel, {}),
        "checklist": [
            "Hook in first 5 seconds (face to camera)",
            "Thumbnail: high contrast, 3-4 words max",
            "Description: timestamps + cross-links + disclaimer",
            "Tags: master keywords + topic-specific",
            "End screen: subscribe + next video",
            "Cards: link to related video at key moment",
        ],
    }
    return json.dumps(package, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    transport = "stdio"
    port = 8000
    if len(sys.argv) > 1:
        if sys.argv[1] in ("sse", "streamable-http", "stdio"):
            transport = sys.argv[1]
        if len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                pass
                
    if transport == "sse":
        mcp.settings.port = port
        mcp.run(transport="sse")
    else:
        mcp.run(transport=transport)
