import os
import sys
import time

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP
import yt_dlp
import google.generativeai as genai

# Initialize the FastMCP server
mcp = FastMCP("Video Analyzer (Eyes and Ears)")

# Try to configure API key from environment, or use a default placeholder if running in test
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@mcp.tool()
def analyze_competitor_video(url: str, prompt: str) -> str:
    """
    Downloads a web video (YouTube, etc.), uploads it to the Gemini Multimodal API for 1fps visual and native audio analysis, and returns the insights.
    Args:
        url: The URL of the video.
        prompt: Specific questions to ask about the video's content, editing style, or strategy.
    """
    if not os.environ.get("GEMINI_API_KEY"):
        return "Error: GEMINI_API_KEY environment variable is not set. Please set it to run this tool."
        
    # By using 'best[height<=720]/best', we grab a format that has both video and audio pre-merged.
    # This bypasses the need for ffmpeg to merge them, which is perfect since ffmpeg is missing.
    ydl_opts = {
        'format': 'best[height<=720]/best',
        'outtmpl': 'temp_video_%(id)s.%(ext)s',
        'quiet': True,
    }
    
    filename = None
    try:
        print(f"Downloading {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        print(f"Downloaded to {filename}. Uploading to Gemini...")
        
        # Upload to Gemini File API
        video_file = genai.upload_file(path=filename)
        
        # Wait for Processing (Critical Step)
        max_wait = 180 # Wait up to 3 minutes
        elapsed = 0
        while video_file.state.name == "PROCESSING" and elapsed < max_wait:
            time.sleep(5)
            elapsed += 5
            video_file = genai.get_file(video_file.name)
            
        if video_file.state.name == "FAILED":
            raise ValueError("Gemini video processing failed.")
        elif video_file.state.name == "PROCESSING":
            raise ValueError("Gemini video processing timed out after 3 minutes.")
            
        print(f"File active. Running inference...")
        
        # Run Inference using 1.5 Pro
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content([video_file, prompt])
        
        # Cleanup remote file
        try:
            genai.delete_file(video_file.name)
        except Exception as e:
            print(f"Warning: Failed to delete remote file: {e}")
            
        return response.text
        
    except Exception as e:
        return f"Error analyzing video: {str(e)}"
    finally:
        # Cleanup local file
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Warning: Failed to delete local file {filename}: {e}")

if __name__ == "__main__":
    mcp.run()
