import json
import urllib.request
import urllib.parse
import os
import datetime
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"

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
        # Save back
        with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2)
        return access_token

def call_drive_api(access_token, params=None):
    url = "https://www.googleapis.com/drive/v3/files"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        safe_print(f"Credentials file not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    
    # 1. Search for files containing Gemini or Brain
    safe_print("Searching Google Drive for files containing 'Gemini' or 'Brain'...")
    params = {
        "q": "name contains 'Gemini' or name contains 'Brain' or name contains 'Keystone'",
        "orderBy": "modifiedTime desc",
        "pageSize": 30,
        "fields": "files(id, name, mimeType, modifiedTime, webViewLink)"
    }
    
    res = call_drive_api(access_token, params)
    files = res.get("files", [])
    safe_print(f"Found {len(files)} matching files:")
    for f in files:
        safe_print(f"- {f['name']} ({f['mimeType']})")
        safe_print(f"  Modified: {f['modifiedTime']}")
        safe_print(f"  Link: {f['webViewLink']}")
        safe_print("")
        
    # 2. List the 20 most recently modified files overall
    safe_print("\nListing the 20 most recently modified files overall...")
    params_recent = {
        "orderBy": "modifiedTime desc",
        "pageSize": 20,
        "fields": "files(id, name, mimeType, modifiedTime, webViewLink)"
    }
    res_recent = call_drive_api(access_token, params_recent)
    files_recent = res_recent.get("files", [])
    for f in files_recent:
        safe_print(f"- {f['name']} ({f['mimeType']})")
        safe_print(f"  Modified: {f['modifiedTime']}")
        safe_print(f"  Link: {f['webViewLink']}")
        safe_print("")

if __name__ == "__main__":
    main()
