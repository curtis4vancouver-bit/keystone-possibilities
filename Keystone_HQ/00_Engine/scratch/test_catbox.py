import os
import sys
import logging
import urllib.request
import urllib.parse
import mimetypes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def upload_to_catbox(file_path):
    """Uploads a local file to Catbox.moe and returns the direct public URL."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None

    logger.info(f"Uploading {file_path} to Catbox.moe...")
    url = "https://catbox.moe/user/api.php"
    
    # Read file content
    with open(file_path, "rb") as f:
        file_content = f.read()

    filename = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "video/quicktime"

    # Construct multipart/form-data boundary
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    # Form fields
    parts = []
    
    # Field: reqtype
    parts.append(f"--{boundary}".encode('utf-8'))
    parts.append('Content-Disposition: form-data; name="reqtype"'.encode('utf-8'))
    parts.append(''.encode('utf-8'))
    parts.append('fileupload'.encode('utf-8'))
    
    # Field: fileToUpload
    parts.append(f"--{boundary}".encode('utf-8'))
    parts.append(f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"'.encode('utf-8'))
    parts.append(f'Content-Type: {mime_type}'.encode('utf-8'))
    parts.append(''.encode('utf-8'))
    parts.append(file_content)
    
    parts.append(f"--{boundary}--".encode('utf-8'))
    
    # Join parts with CRLF
    body = b"\r\n".join(parts)
    
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        req = urllib.request.Request(url, data=body, headers=headers)
        with urllib.request.urlopen(req) as res:
            public_url = res.read().decode('utf-8').strip()
            if public_url.startswith("https://files.catbox.moe/"):
                logger.info(f"✅ Success! Direct URL: {public_url}")
                return public_url
            else:
                logger.error(f"Catbox upload failed. Response: {public_url}")
                return None
    except Exception as e:
        logger.error(f"Error during Catbox upload: {str(e)}")
        return None

def main():
    file_path = r"C:\Users\Curtis\Desktop\short 21.mov"
    public_url = upload_to_catbox(file_path)
    if public_url:
        print(f"\nPublic URL obtained: {public_url}")
    else:
        print("\nFailed to obtain public URL.")

if __name__ == "__main__":
    main()
