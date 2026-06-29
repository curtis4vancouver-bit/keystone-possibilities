import json
import urllib.request
import urllib.parse
import os
import datetime
import uuid

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
RESUME_HTML_PATH = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\wayne_resume.html"

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
        print(f"Credentials not found at {CREDENTIALS_PATH}")
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
    
    # Make request to Drive v3 API files endpoint with uploadType=multipart
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink"
    req = urllib.request.Request(url, data=body_data, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    
    print("Uploading resume and converting to Google Doc...")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print("Successfully created Google Doc!")
            print(f"File Name: {res.get('name')}")
            print(f"File ID:   {res.get('id')}")
            print(f"Link:      {res.get('webViewLink')}")
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    main()
