"""Quick test: verify dual-token routing works for all 3 channels."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from youtube_api_manager import YouTubeAPIManager

manager = YouTubeAPIManager(token_file=os.path.join(SCRIPT_DIR, "youtube_token.json"))
OAC_TOKEN = os.path.join(SCRIPT_DIR, "youtube_token_oac.json")
_oac_youtube = None

def get_youtube(channel="oac"):
    global _oac_youtube
    if channel == "oac" and os.path.exists(OAC_TOKEN):
        if _oac_youtube is None:
            creds = Credentials.from_authorized_user_file(OAC_TOKEN)
            _oac_youtube = build("youtube", "v3", credentials=creds)
        return _oac_youtube
    return manager.youtube

CHANNELS = {
    "possibilities": "UCu8gdU_R8XE2RvcttGa3drg",
    "protocols": "UCxURlqMNhAtxUTpdXmlOYaw",
    "oac": "UCMn1f9DTF_iybKmv5WlTm9Q",
}

for name, ch_id in CHANNELS.items():
    yt = get_youtube(name)
    result = yt.channels().list(part="snippet,statistics", id=ch_id).execute()
    ch = result["items"][0]
    uploads = "UU" + ch_id[2:]
    pl = yt.playlistItems().list(part="status", playlistId=uploads, maxResults=1).execute()
    total = pl.get("pageInfo", {}).get("totalResults", 0)
    print(f"  {name:15s} | {ch['snippet']['title']:30s} | public: {ch['statistics']['videoCount']:>3s} | total (inc unlisted): {total}")

print("\n[OK] All 3 channels accessible via dual-token routing!")
