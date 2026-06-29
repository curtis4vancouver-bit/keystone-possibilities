import json
import urllib.request
import urllib.parse
import os
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
FILE_ID = "12OtPIWE4thqqpUX9mCL0uipiQZwF-vcaIFpUKSBEfns"

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

def export_doc(access_token, file_id):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text/plain"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        safe_print(f"Failed to export Google Doc {file_id}: {e}")
        return None

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        safe_print(f"Credentials not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    safe_print(f"Fetching Google Doc content for ID: {FILE_ID}...")
    doc_content = export_doc(access_token, FILE_ID)
    if doc_content:
        safe_print("Content loaded successfully!")
        # Let's save a copy locally under scratch
        local_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\gmail_gemini_brain_context.txt"
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(doc_content)
        safe_print(f"Saved locally to {local_path}")
        
        # Display the first 1000 characters
        safe_print("\n--- Preview of Document (First 2000 chars) ---")
        safe_print(doc_content[:2000])
        safe_print("---------------------------------------------")
    else:
        safe_print("Could not retrieve document content.")

if __name__ == "__main__":
    main()
