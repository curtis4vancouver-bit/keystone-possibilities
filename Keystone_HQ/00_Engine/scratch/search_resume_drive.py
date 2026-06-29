import json
import urllib.request
import urllib.parse
import os
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"

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

def search_drive(access_token):
    url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode({
        "q": "name contains 'Resume' or name contains 'resume' or name contains 'Stevenson'",
        "orderBy": "modifiedTime desc",
        "fields": "files(id, name, mimeType, modifiedTime, webViewLink)",
        "pageSize": 10
    })
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode("utf-8"))
        return res.get("files", [])

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Credentials not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    print("Searching for Resume files on Google Drive (sorted by modifiedTime desc)...")
    files = search_drive(access_token)
    for f in files:
        print(f"- Name: {f['name']}")
        print(f"  ID: {f['id']}")
        print(f"  Modified: {f['modifiedTime']}")
        print(f"  MimeType: {f['mimeType']}")
        print(f"  Link: {f['webViewLink']}")
        print("")

if __name__ == "__main__":
    main()
