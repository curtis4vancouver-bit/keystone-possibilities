import json
import urllib.request
import urllib.parse
import os
import datetime
import uuid
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
RESUME_HTML_PATH = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\wayne_resume.html"
FILE_ID = "1oGf_cwalgjAy3xW0aEDpl-V4fK3KKS-ok5k2cqhCKts"

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

def refresh_token(creds):
    data = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        creds["token_uri"],
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        access_token = res_data["access_token"]
        creds["token"] = access_token
        with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2)
        return access_token

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        safe_print(f"Credentials not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    
    with open(RESUME_HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Boundary for multipart request
    boundary = f"----{uuid.uuid4().hex}"
    
    # Metadata part
    metadata = {
        "name": "Wayne Stevenson - Resume",
        "mimeType": "application/vnd.google-apps.document"
    }
    metadata_json = json.dumps(metadata)
    
    # Construct multipart request body
    body_parts = []
    
    # Part 1: Metadata
    body_parts.append(f"--{boundary}".encode("utf-8"))
    body_parts.append(b"Content-Type: application/json; charset=UTF-8")
    body_parts.append(b"")
    body_parts.append(metadata_json.encode("utf-8"))
    
    # Part 2: Media (HTML file)
    body_parts.append(f"--{boundary}".encode("utf-8"))
    body_parts.append(b"Content-Type: text/html; charset=UTF-8")
    body_parts.append(b"")
    body_parts.append(html_content.encode("utf-8"))
    
    # End boundary
    body_parts.append(f"--{boundary}--".encode("utf-8"))
    
    # Join parts with CRLF
    body_data = b"\r\n".join(body_parts)
    
    # Make request to Drive v3 API files endpoint to update the existing Google Doc
    url = f"https://www.googleapis.com/upload/drive/v3/files/{FILE_ID}?uploadType=multipart&fields=id,name,webViewLink"
    req = urllib.request.Request(url, data=body_data, method="PATCH")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    
    safe_print(f"Updating existing Google Doc (ID: {FILE_ID}) with latest resume...")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            safe_print("Successfully updated Google Doc!")
            safe_print(f"File Name: {res.get('name')}")
            safe_print(f"File ID:   {res.get('id')}")
            safe_print(f"Link:      {res.get('webViewLink')}")
    except Exception as e:
        safe_print(f"Upload failed: {e}")
        # Print response body if available for better debugging
        if hasattr(e, 'read'):
            try:
                error_body = e.read().decode('utf-8')
                safe_print(f"Error details: {error_body}")
            except Exception:
                pass

if __name__ == "__main__":
    main()
