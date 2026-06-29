import sys
import os

sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
from youtube_api_manager import YouTubeAPIManager

def fix_spotify():
    video_id = "ohMgTNrlz0Y"
    mgr = YouTubeAPIManager(token_file=r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token.json")
    
    videos_list_response = mgr.youtube.videos().list(id=video_id, part="snippet").execute()
    snippet = videos_list_response["items"][0]["snippet"]
    
    old_desc = snippet["description"]
    new_desc = old_desc.replace(
        "https://open.spotify.com/artist/WayneStevenson", 
        "https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y"
    )
    
    if old_desc != new_desc:
        snippet["description"] = new_desc
        mgr.youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": snippet
            }
        ).execute()
        print("Spotify link fixed on live video!")
    else:
        print("No change needed.")

fix_spotify()
