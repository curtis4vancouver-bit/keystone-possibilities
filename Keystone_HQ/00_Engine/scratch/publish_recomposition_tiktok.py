import os
import sys
import json
import urllib.request
import time

def api_post_json(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={**headers, "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise Exception(f"HTTP {e.code}: {e.reason} - {err_body}")

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        sys.stdout.write("ERROR: social_tokens.json not found.\n")
        sys.exit(1)
        
    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    tiktok_info = tokens.get("recomposition", {}).get("tiktok", {})
    access_token = tiktok_info.get("access_token")
    if not access_token:
        sys.stdout.write("ERROR: No TikTok access token found under recomposition.\n")
        sys.exit(1)
        
    title = "The Silent GLP-1 Muscle Leak! #GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #PeptideProtocols #MenOver40 #LongevityBuilder #SquamishWellness #KeystoneProtocols #Biohacking"
    
    # 41.96s total, last 2s contains DaVinci thumbnail, so select 41500 ms (41.5 seconds)
    video_cover_timestamp_ms = 41500
    video_url = "https://files.catbox.moe/c00r5n.mov"
    
    sys.stdout.write(f"Initiating TikTok video publish request...\n")
    sys.stdout.write(f"Title: {title}\n")
    sys.stdout.write(f"Video URL: {video_url}\n")
    sys.stdout.write(f"Cover Frame Offset: {video_cover_timestamp_ms} ms (41.5 seconds)\n\n")
    
    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "post_info": {
            "title": title,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "video_cover_timestamp_ms": video_cover_timestamp_ms
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url
        }
    }
    
    try:
        res = api_post_json(init_url, payload, headers)
        data = res.get("data", {})
        publish_id = data.get("publish_id")
        
        sys.stdout.write("SUCCESS: Queued TikTok Video upload!\n")
        sys.stdout.write(f"TikTok Publish ID: {publish_id}\n")
        
    except Exception as e:
        sys.stdout.write(f"ERROR TikTok upload failed: {str(e)}\n")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
