import os
import sys
import json
import urllib.request
import math
import time

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

def api_post_json(url: str, payload: dict, headers: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={**headers, "Content-Type": "application/json; charset=UTF-8"}
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise Exception(f"HTTP {e.code}: {e.reason} - {err_body}")

def put_chunk(url: str, headers: dict, data: bytes) -> int:
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as res:
            return res.status
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        raise Exception(f"HTTP {e.code}: {e.reason} - {err_body}")

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        print("ERROR: social_tokens.json not found.")
        sys.exit(1)
        
    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    tiktok_info = tokens.get("recomposition", {}).get("tiktok", {})
    access_token = tiktok_info.get("access_token")
    if not access_token:
        print("ERROR: No TikTok access token found under recomposition.")
        sys.exit(1)
        
    video_path = r"C:\Users\Curtis\Desktop\short 2.mov"
    if not os.path.exists(video_path):
        print(f"ERROR: Video not found at {video_path}")
        sys.exit(1)
        
    file_size = os.path.getsize(video_path)
    # Target chunk size: 10MB (10,485,760 bytes)
    chunk_size = 10 * 1024 * 1024
    total_chunks = math.floor(file_size / chunk_size)
    if total_chunks == 0:
        total_chunks = 1
    
    # Beautiful, YMYL-compliant description matching SCRIPT_003
    title = "CJC-1295 vs. Tesamorelin: Visceral Belly Fat Battle! ⚠️🧬 #KeystoneRecomposition #VisceralFat #PeptideScience #MenOver40 #CJC1295 #Tesamorelin #Squamish"
    video_cover_timestamp_ms = 10000
    
    print("1. Initializing TikTok video FILE_UPLOAD request to INBOX (DRAFT)...")
    init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "post_info": {
            "title": title,
            "video_cover_timestamp_ms": video_cover_timestamp_ms
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks
        }
    }
    
    try:
        res = api_post_json(init_url, payload, headers)
        data = res.get("data", {})
        publish_id = data.get("publish_id")
        upload_url = data.get("upload_url")
        
        if not upload_url:
            print("ERROR: Failed to obtain upload_url from initialization.")
            sys.exit(1)
            
        print(f"Upload session initialized successfully!")
        print(f"Publish ID: {publish_id}")
        print(f"Total chunks to upload: {total_chunks} ({file_size / (1024*1024):.2f} MB total)")
        
        # 2. Upload chunks sequentially
        print("\n2. Starting sequential chunked binary transfer...")
        with open(video_path, "rb") as f:
            for i in range(total_chunks):
                first_byte = i * chunk_size
                if i == total_chunks - 1:
                    # Last chunk gets all remaining bytes
                    chunk_data = f.read()
                else:
                    chunk_data = f.read(chunk_size)
                
                last_byte = first_byte + len(chunk_data) - 1
                
                chunk_headers = {
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(chunk_data)),
                    "Content-Range": f"bytes {first_byte}-{last_byte}/{file_size}"
                }
                
                print(f"  Uploading chunk {i+1}/{total_chunks} (bytes {first_byte}-{last_byte}, size: {len(chunk_data)})...")
                status = put_chunk(upload_url, chunk_headers, chunk_data)
                
                if status not in (200, 201, 204, 206):
                    print(f"  ERROR: Chunk {i+1} upload failed with status {status}")
                    sys.exit(1)
                    
        print("\n🎉 SUCCESS: Video successfully uploaded directly as a draft to TikTok Recomposition!")
        print(f"Verify on your TikTok mobile app under your Inbox/Draft Notifications!")
        
    except Exception as e:
        print(f"ERROR: TikTok upload failed: {str(e)}")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
