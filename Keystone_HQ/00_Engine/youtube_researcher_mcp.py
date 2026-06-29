import os
import sys
import io

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Legacy Windows encoding override (TextIOWrapper/utf-8) removed to prevent Python 3.14 I/O closed file errors.

from mcp.server.fastmcp import FastMCP
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import json

# Initialize the FastMCP server
mcp = FastMCP("YouTube Deep Researcher")

@mcp.tool()
def get_video_metadata(url: str) -> str:
    """
    Extracts deep backend metadata from a YouTube video including viral tags, upload date, views, likes, and full description.
    Args:
        url: The full YouTube video URL.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'dumpjson': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "view_count": info.get("view_count"),
                "like_count": info.get("like_count"),
                "tags": info.get("tags", []),
                "description": info.get("description")
            }
            return json.dumps(metadata, indent=2)
    except Exception as e:
        return f"Error extracting metadata: {str(e)}"

@mcp.tool()
def get_video_transcript(video_id: str) -> str:
    """
    Extracts the full spoken transcript/script of a YouTube video so the AI can analyze the hook, pacing, and how they wrote it.
    Args:
        video_id: The 11-character YouTube video ID (e.g., dQw4w9WgXcQ).
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id)
        full_text = " ".join([t.text for t in transcript_data])
        return full_text
    except Exception as e:
        return f"Error extracting transcript (video may not have captions enabled): {str(e)}"

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
