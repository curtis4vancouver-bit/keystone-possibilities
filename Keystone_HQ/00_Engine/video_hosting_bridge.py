"""
Keystone Video Hosting Bridge
Uploads local video/image files to Google Cloud Storage and returns a public URL.
Used by social_publisher.py to provide publicly accessible media URLs for TikTok and Instagram APIs.

Usage:
    # As a module:
    from video_hosting_bridge import upload_to_gcs
    public_url = upload_to_gcs("C:\\Users\\Curtis\\Desktop\\short 22.mov")

    # As CLI:
    python video_hosting_bridge.py "C:\\Users\\Curtis\\Desktop\\short 22.mov"
    python video_hosting_bridge.py "C:\\path\\to\\thumbnail.jpg" --subfolder images
"""

import os
import sys
import time
import uuid
import json
import mimetypes
import argparse

# Reconfigure stdout to UTF-8 for Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── Configuration ────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "scratch" else SCRIPT_DIR

GCS_KEY_PATH = os.path.join(ROOT_DIR, "scratch", "gcs_key.json")
if not os.path.exists(GCS_KEY_PATH):
    GCS_KEY_PATH = os.path.join(SCRIPT_DIR, "gcs_key.json")

BUCKET_NAME = "semiotic-ion-458504-e9-brand-brain-bucket"
DEFAULT_SUBFOLDER = "social_media"  # Videos stored under gs://bucket/social_media/

# Signed URL expiry (hours). TikTok/IG need time to fetch the video.
SIGNED_URL_EXPIRY_HOURS = 48

# ── Core Functions ───────────────────────────────────────────────────────────

def _get_gcs_client():
    """Returns an authenticated GCS client using the service account key."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCS_KEY_PATH
    from google.cloud import storage
    return storage.Client()


def _detect_content_type(file_path: str) -> str:
    """Detects MIME type from file extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type

    ext = os.path.splitext(file_path)[1].lower()
    ext_map = {
        ".mov": "video/quicktime",
        ".mp4": "video/mp4",
        ".m4v": "video/mp4",
        ".avi": "video/x-msvideo",
        ".mkv": "video/x-matroska",
        ".webm": "video/webm",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return ext_map.get(ext, "application/octet-stream")


def upload_to_catbox(file_path: str) -> str:
    """Uploads a local file to Catbox.moe and returns the direct public URL."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Uploading {os.path.basename(file_path)} to Catbox.moe fallback...")
    url = "https://catbox.moe/user/api.php"
    
    with open(file_path, "rb") as f:
        file_content = f.read()

    filename = os.path.basename(file_path)
    mime_type = _detect_content_type(file_path)

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    parts = []
    
    parts.append(f"--{boundary}".encode('utf-8'))
    parts.append('Content-Disposition: form-data; name="reqtype"'.encode('utf-8'))
    parts.append(''.encode('utf-8'))
    parts.append('fileupload'.encode('utf-8'))
    
    parts.append(f"--{boundary}".encode('utf-8'))
    parts.append(f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"'.encode('utf-8'))
    parts.append(f'Content-Type: {mime_type}'.encode('utf-8'))
    parts.append(''.encode('utf-8'))
    parts.append(file_content)
    
    parts.append(f"--{boundary}--".encode('utf-8'))
    body = b"\r\n".join(parts)
    
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    import urllib.request
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req) as res:
        public_url = res.read().decode('utf-8').strip()
        if public_url.startswith("https://files.catbox.moe/"):
            print(f"Catbox Upload Success: {public_url}")
            return public_url
        else:
            raise Exception(f"Catbox upload failed. Response: {public_url}")


def upload_to_gcs(
    local_file_path: str,
    subfolder: str = DEFAULT_SUBFOLDER,
    custom_filename: str = None,
    make_public: bool = False
) -> str:
    """
    Uploads a local file to Google Cloud Storage and returns a URL.

    Args:
        local_file_path: Absolute path to the local video or image file.
        subfolder: GCS subfolder (default: 'social_media').
        custom_filename: Optional override for the GCS blob name.
        make_public: If True, makes the blob publicly readable (no signed URL needed).
                     If False (default), generates a 48-hour signed URL.

    Returns:
        A public or signed URL string that TikTok/Instagram APIs can pull from.

    Raises:
        FileNotFoundError: If the local file doesn't exist.
        Exception: On GCS upload failure.
    """
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"File not found: {local_file_path}")

    file_size = os.path.getsize(local_file_path)
    if file_size == 0:
        raise ValueError(f"File is empty (0 bytes): {local_file_path}")

    # Generate a unique filename to prevent collisions
    original_name = os.path.basename(local_file_path)
    name_base, ext = os.path.splitext(original_name)
    # Sanitize: replace spaces with underscores, lowercase
    safe_name = name_base.replace(" ", "_").lower()
    timestamp = int(time.time())
    unique_id = uuid.uuid4().hex[:8]

    if custom_filename:
        blob_name = f"{subfolder}/{custom_filename}"
    else:
        blob_name = f"{subfolder}/{safe_name}_{timestamp}_{unique_id}{ext.lower()}"

    content_type = _detect_content_type(local_file_path)

    print(f"Uploading: {original_name} ({file_size / (1024*1024):.1f} MB)")
    print(f"Content-Type: {content_type}")
    print(f"Destination: gs://{BUCKET_NAME}/{blob_name}")

    # Upload
    try:
        client = _get_gcs_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name)
        blob.content_type = content_type

        # Use resumable upload for files > 5MB
        if file_size > 5 * 1024 * 1024:
            print("Using resumable upload (file > 5MB)...")
            blob.upload_from_filename(local_file_path, content_type=content_type, timeout=600)
        else:
            blob.upload_from_filename(local_file_path, content_type=content_type)

        print("Upload complete.")

        # Generate URL
        if make_public:
            blob.make_public()
            public_url = blob.public_url
            print(f"Public URL: {public_url}")
            return public_url
        else:
            # Generate a signed URL (48 hours default)
            from datetime import timedelta
            signed_url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=SIGNED_URL_EXPIRY_HOURS),
                method="GET"
            )
            print(f"Signed URL (expires in {SIGNED_URL_EXPIRY_HOURS}h): {signed_url[:80]}...")
            return signed_url
    except Exception as e:
        print(f"⚠️ GCS Upload failed ({str(e)}). Falling back to Catbox.moe...")
        try:
            return upload_to_catbox(local_file_path)
        except Exception as fallback_error:
            print(f"❌ Fallback to Catbox.moe also failed: {str(fallback_error)}")
            raise e


def list_hosted_media(subfolder: str = DEFAULT_SUBFOLDER, limit: int = 20) -> list:
    """Lists recently uploaded media files in GCS."""
    client = _get_gcs_client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=f"{subfolder}/", max_results=limit))

    results = []
    for blob in blobs:
        results.append({
            "name": blob.name,
            "size_mb": round(blob.size / (1024 * 1024), 2) if blob.size else 0,
            "content_type": blob.content_type,
            "created": str(blob.time_created) if blob.time_created else "unknown",
        })
    return results


def cleanup_old_media(subfolder: str = DEFAULT_SUBFOLDER, older_than_days: int = 7) -> int:
    """Deletes media files older than the specified number of days to save storage."""
    client = _get_gcs_client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=f"{subfolder}/"))

    from datetime import datetime, timezone, timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
    deleted = 0

    for blob in blobs:
        if blob.time_created and blob.time_created < cutoff:
            print(f"Deleting old media: {blob.name} (created {blob.time_created})")
            blob.delete()
            deleted += 1

    print(f"Cleaned up {deleted} old media files.")
    return deleted


# ── CLI Interface ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload media to GCS for TikTok/Instagram publishing")
    parser.add_argument("file", nargs="?", help="Path to the local video or image file")
    parser.add_argument("--subfolder", default=DEFAULT_SUBFOLDER, help="GCS subfolder (default: social_media)")
    parser.add_argument("--public", action="store_true", help="Make file publicly readable (no signed URL)")
    parser.add_argument("--list", action="store_true", help="List recently hosted media files")
    parser.add_argument("--cleanup", type=int, metavar="DAYS", help="Delete media older than N days")
    parser.add_argument("--filename", type=str, help="Custom filename for the uploaded file")

    args = parser.parse_args()

    if args.list:
        media = list_hosted_media(args.subfolder)
        if media:
            print(f"\nHosted media in gs://{BUCKET_NAME}/{args.subfolder}/:")
            for item in media:
                print(f"  {item['name']} ({item['size_mb']} MB, {item['content_type']})")
        else:
            print("No media files found.")
    elif args.cleanup is not None:
        cleanup_old_media(args.subfolder, args.cleanup)
    elif args.file:
        url = upload_to_gcs(args.file, args.subfolder, custom_filename=args.filename, make_public=args.public)
        print(f"\nRESULT URL: {url}")
    else:
        parser.print_help()
