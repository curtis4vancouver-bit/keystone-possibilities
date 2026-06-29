"""
Keystone YouTube Manager MCP v2.0
Full channel management: list, update metadata, change privacy, bulk operations.
"""
import os
import sys
import io

# Fix CWD: ensure we're in the script's directory for relative imports and token file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Legacy Windows encoding overrides (TextIOWrapper/utf-8) removed to prevent Python 3.14 I/O closed file errors.

from mcp.server.fastmcp import FastMCP
from youtube_api_manager import YouTubeAPIManager
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

mcp = FastMCP("YouTube Manager")

# Cache for channel managers to avoid re-authenticating on every call
_managers = {}

# Channel → Token mapping: which token file authenticates which channel
# CRITICAL: Getting this wrong uploads to the WRONG channel!
# This is the SINGLE SOURCE OF TRUTH for token routing.
CHANNEL_TOKEN_MAP = {
    "possibilities": "youtube_token_possibilities.json",
    "protocols": "youtube_token.json",
    "recomposition": "youtube_token_oac.json",
    "oac": "youtube_token_oac.json",
}

CHANNELS = {
    "possibilities": "UCu8gdU_R8XE2RvcttGa3drg",   # Construction brand
    "protocols": "UCxURlqMNhAtxUTpdXmlOYaw",        # Protocols channel
    "recomposition": "UCMn1f9DTF_iybKmv5WlTm9Q",    # Health/wellness brand (OAC)
    "oac": "UCMn1f9DTF_iybKmv5WlTm9Q",              # Alias for recomposition (legacy)
}

def get_manager(channel: str = "oac") -> YouTubeAPIManager:
    """Returns the YouTubeAPIManager instance for the given channel.
    Uses CHANNEL_TOKEN_MAP for correct token routing.
    Auto-evicts stale cached managers when the token file has been updated."""
    global _managers
    # Normalize channel name
    if channel == "recomposition":
        channel = "oac"
        
    # Resolve token path
    token_filename = CHANNEL_TOKEN_MAP.get(channel)
    if not token_filename:
        token_filename = f"youtube_token_{channel}.json"
    token_path = os.path.join(SCRIPT_DIR, token_filename)
    
    if not os.path.exists(token_path):
        legacy_path = os.path.join(SCRIPT_DIR, "youtube_token.json")
        if os.path.exists(legacy_path):
            token_path = legacy_path
        else:
            return None

    # Cache-bust: evict if manager exists but its youtube service is broken,
    # or if the token file on disk is newer than when we cached it.
    if channel in _managers:
        mgr = _managers[channel]
        needs_refresh = False
        # Check if youtube service is dead
        if not mgr.youtube:
            needs_refresh = True
        # Check if token file changed since we cached (mtime comparison)
        elif hasattr(mgr, '_token_mtime'):
            try:
                current_mtime = os.path.getmtime(token_path)
                if current_mtime > mgr._token_mtime:
                    needs_refresh = True
            except OSError:
                pass
        if needs_refresh:
            del _managers[channel]

    if channel not in _managers:
        mgr = YouTubeAPIManager(token_file=token_path)
        # Tag with the mtime of the token file so we can detect changes later
        try:
            mgr._token_mtime = os.path.getmtime(token_path)
        except OSError:
            mgr._token_mtime = 0
        _managers[channel] = mgr
        
    return _managers[channel]

def get_youtube(channel: str = "oac"):
    """Returns the YouTube API service for the given channel."""
    mgr = get_manager(channel)
    return mgr.youtube if mgr else None

@mcp.tool()
def list_channel_videos(channel: str = "oac", max_results: int = 50) -> str:
    """
    Lists all videos on a Keystone channel with their privacy status, view counts, and metadata.
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        max_results: Max videos to return (default 50, max 200)
    """
    yt = get_youtube(channel)
    if not yt:
        return "ERROR: YouTube API not authenticated. Run youtube_oauth.py first."
    
    ch_id = CHANNELS.get(channel)
    if not ch_id:
        return f"ERROR: Unknown channel '{channel}'. Use: possibilities, protocols, oac"
    
    uploads_playlist = "UU" + ch_id[2:]
    videos = []
    next_page = None
    fetched = 0
    
    while fetched < max_results:
        batch_size = min(50, max_results - fetched)
        try:
            result = yt.playlistItems().list(
                part="snippet,status,contentDetails",
                playlistId=uploads_playlist,
                maxResults=batch_size,
                pageToken=next_page
            ).execute()
            
            for item in result.get("items", []):
                vid = item["snippet"]
                status = item.get("status", {})
                video_id = vid.get("resourceId", {}).get("videoId", "?")
                videos.append({
                    "video_id": video_id,
                    "title": vid.get("title", "Untitled"),
                    "privacy": status.get("privacyStatus", "unknown"),
                    "published": vid.get("publishedAt", "?")[:10],
                    "description_preview": (vid.get("description", "")[:100] + "...") if vid.get("description") else ""
                })
                fetched += 1
            
            next_page = result.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            return f"ERROR listing videos: {e}"
    
    return json.dumps({"channel": channel, "channel_id": ch_id, "total": len(videos), "videos": videos}, indent=2, ensure_ascii=False)


@mcp.tool()
def get_video_details(video_id: str, channel: str = "protocols") -> str:
    """
    Gets full details for a specific video including description, tags, statistics, and status.
    Args:
        video_id: The YouTube video ID
        channel: 'possibilities', 'protocols', or 'oac' (determines which token to use)
    """
    yt = get_youtube(channel)
    if not yt:
        return "ERROR: YouTube API not authenticated."
    
    try:
        result = yt.videos().list(
            part="snippet,status,statistics,contentDetails",
            id=video_id
        ).execute()
        
        if not result.get("items"):
            return f"ERROR: Video {video_id} not found."
        
        item = result["items"][0]
        return json.dumps({
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "tags": item["snippet"].get("tags", []),
            "category_id": item["snippet"]["categoryId"],
            "privacy": item["status"]["privacyStatus"],
            "publish_at": item["status"].get("publishAt"),
            "made_for_kids": item["status"].get("madeForKids"),
            "views": item["statistics"].get("viewCount", "0"),
            "likes": item["statistics"].get("likeCount", "0"),
            "comments": item["statistics"].get("commentCount", "0"),
            "duration": item["contentDetails"]["duration"],
            "published": item["snippet"]["publishedAt"]
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"ERROR: {e}"


@mcp.tool()
def update_video_metadata(video_id: str, title: str = None, description: str = None, tags: list = None, category_id: str = None, channel: str = "protocols") -> str:
    """
    Updates metadata for an existing YouTube video.
    Args:
        video_id: The YouTube ID of the video to update.
        title: New title (optional).
        description: New description (optional).
        tags: New list of tags (optional).
        category_id: New category ID (optional).
        channel: 'possibilities', 'protocols', or 'recomposition' (determines which token to use).
    """
    try:
        mgr = get_manager(channel)
        if not mgr:
            return f"ERROR: YouTube API not authenticated for channel '{channel}'."
        response = mgr.update_video_metadata(video_id, title, description, tags, category_id)
        if response:
            return f"Success! Metadata updated for Video ID: {video_id}"
        return f"Failed to update metadata for Video ID: {video_id}."
    except Exception as e:
        return f"Error updating metadata: {str(e)}"


@mcp.tool()
def set_video_privacy(video_id: str, privacy: str, channel: str = "protocols") -> str:
    """
    Changes the privacy status of a video.
    Args:
        video_id: The YouTube video ID
        privacy: 'public', 'unlisted', or 'private'
        channel: 'possibilities', 'protocols', or 'oac' (determines which token to use)
    """
    yt = get_youtube(channel)
    if not yt:
        return "ERROR: YouTube API not authenticated."
    
    if privacy not in ("public", "unlisted", "private"):
        return f"ERROR: Invalid privacy '{privacy}'. Use: public, unlisted, private"
    
    try:
        # Get current video data
        result = yt.videos().list(
            part="snippet,status",
            id=video_id
        ).execute()
        
        if not result.get("items"):
            return f"ERROR: Video {video_id} not found."
        
        item = result["items"][0]
        old_privacy = item["status"]["privacyStatus"]
        
        # Update privacy
        status_body = {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": item["status"].get("madeForKids", False)
        }
        if "containsSyntheticMedia" in item["status"]:
            status_body["containsSyntheticMedia"] = item["status"]["containsSyntheticMedia"]
            
        update_result = yt.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": status_body
            }
        ).execute()
        
        return f"Success! Video {video_id} privacy changed: {old_privacy} -> {privacy}"
    except Exception as e:
        return f"ERROR changing privacy: {e}"


@mcp.tool()
def get_channel_info(channel: str = "oac") -> str:
    """
    Gets channel info including description, subscriber count, and branding settings.
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
    """
    yt = get_youtube(channel)
    if not yt:
        return "ERROR: YouTube API not authenticated."
    
    ch_id = CHANNELS.get(channel)
    if not ch_id:
        return f"ERROR: Unknown channel '{channel}'. Use: possibilities, protocols, oac"
    
    try:
        result = yt.channels().list(
            part="snippet,statistics,brandingSettings,contentDetails",
            id=ch_id
        ).execute()
        
        if not result.get("items"):
            return f"ERROR: Channel not found."
        
        ch = result["items"][0]
        branding = ch.get("brandingSettings", {})
        
        return json.dumps({
            "channel_id": ch_id,
            "title": ch["snippet"]["title"],
            "description": ch["snippet"].get("description", ""),
            "subscribers": ch["statistics"].get("subscriberCount", "hidden"),
            "total_views": ch["statistics"]["viewCount"],
            "video_count": ch["statistics"]["videoCount"],
            "keywords": branding.get("channel", {}).get("keywords", ""),
            "country": branding.get("channel", {}).get("country", ""),
            "uploads_playlist": ch["contentDetails"]["relatedPlaylists"]["uploads"]
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"ERROR: {e}"


@mcp.tool()
def upload_video(file_path: str, title: str, description: str, tags: list, channel: str = "possibilities", category_id: str = "27", privacy_status: str = "private") -> str:
    """
    Uploads a video to a specific YouTube channel with the provided metadata.
    
    CRITICAL ROUTING:
    - 'possibilities' → Construction content (Keystone Possibilities channel)
    - 'recomposition' → Health/wellness content (Keystone Recomposition channel)  
    - 'protocols' → Protocol content (Protocols channel)
    
    Args:
        file_path: Absolute path to the video file.
        title: Title of the video.
        description: Description of the video.
        tags: List of tags for the video.
        channel: 'possibilities', 'recomposition', or 'protocols'. MUST match video content!
        category_id: YouTube Category ID (default 27 for Education).
        privacy_status: 'public', 'unlisted', or 'private'.
    """
    # Validate channel
    if channel not in CHANNELS:
        return f"ERROR: Unknown channel '{channel}'. Use: possibilities, recomposition, protocols"
    
    # Route to correct token based on channel
    token_filename = CHANNEL_TOKEN_MAP.get(channel)
    if not token_filename:
        return f"ERROR: Token mapping not found for channel: {channel}"
    
    token_file = os.path.join(SCRIPT_DIR, token_filename)
    channel_name = f"Keystone {channel.capitalize()} ({token_filename})"
    
    if not os.path.exists(token_file):
        return f"ERROR: Token file not found: {token_file}. Run youtube_oauth.py first."
    
    try:
        upload_manager = YouTubeAPIManager(token_file=token_file)
        if not upload_manager.youtube:
            return f"ERROR: Authentication failed for {channel_name}."
        
        response = upload_manager.upload_video(
            file_path=file_path,
            title=title,
            description=description,
            tags=tags,
            category_id=category_id,
            privacy_status=privacy_status
        )
        
        if response:
            video_id = response.get('id')
            return (
                f"Success! Video uploaded to {channel_name}.\n"
                f"Video ID: {video_id}\n"
                f"Channel: {channel} ({CHANNELS[channel]})\n"
                f"URL: https://youtube.com/watch?v={video_id}\n"
                f"Privacy: {privacy_status}"
            )
        return f"Upload failed for channel {channel}. Check logs."
    except Exception as e:
        return f"Error during upload to {channel_name}: {str(e)}"


@mcp.tool()
def bulk_update_descriptions(channel: str, template: str, append: bool = False) -> str:
    """
    Updates descriptions for ALL videos on a channel using a template.
    Use {title} placeholder for the video title. If append=True, adds to existing description.
    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        template: Description template text. Use {title} for video title placeholder.
        append: If True, appends template to existing description. If False, replaces.
    """
    yt = get_youtube(channel)
    if not yt:
        return "ERROR: YouTube API not authenticated."
    
    ch_id = CHANNELS.get(channel)
    if not ch_id:
        return f"ERROR: Unknown channel '{channel}'."
    
    uploads_playlist = "UU" + ch_id[2:]
    updated = 0
    errors = []
    next_page = None
    
    while True:
        try:
            result = yt.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist,
                maxResults=50,
                pageToken=next_page
            ).execute()
            
            for item in result.get("items", []):
                video_id = item["snippet"]["resourceId"]["videoId"]
                title = item["snippet"]["title"]
                
                try:
                    # Get full video details
                    vid_result = yt.videos().list(
                        part="snippet",
                        id=video_id
                    ).execute()
                    
                    if vid_result.get("items"):
                        snippet = vid_result["items"][0]["snippet"]
                        desc_text = template.replace("{title}", title)
                        
                        if append:
                            existing = snippet.get("description", "")
                            # Don't append if template content already exists
                            if desc_text not in existing:
                                snippet["description"] = existing + "\n\n" + desc_text
                            else:
                                continue
                        else:
                            snippet["description"] = desc_text
                        
                        yt.videos().update(
                            part="snippet",
                            body={"id": video_id, "snippet": snippet}
                        ).execute()
                        updated += 1
                except Exception as e:
                    errors.append(f"{video_id}: {e}")
            
            next_page = result.get("nextPageToken")
            if not next_page:
                break
        except Exception as e:
            return f"ERROR: {e}"
    
    result = f"Updated {updated} videos on {channel}."
    if errors:
        result += f" Errors ({len(errors)}): " + "; ".join(errors[:5])
    return result


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
