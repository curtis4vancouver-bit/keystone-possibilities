import json
import urllib.request
import urllib.parse
import os
import datetime
import base64
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
OUTPUT_FILE = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\gmail_results.txt"

# Force output to handle encoding cleanly
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

def refresh_token(creds):
    safe_print("Refreshing OAuth2 token...")
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
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            access_token = res_data["access_token"]
            expires_in = res_data.get("expires_in", 3600)
            
            # Calculate new expiry time
            new_expiry = (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).isoformat()
            
            creds["token"] = access_token
            creds["expiry"] = new_expiry
            
            # Write back
            with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
                json.dump(creds, f, indent=2)
            
            safe_print(f"Token refreshed successfully! Expires at: {new_expiry}")
            return access_token
    except Exception as e:
        safe_print(f"Failed to refresh token: {e}")
        raise e

def call_gmail_api(access_token, endpoint, params=None):
    url = endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        safe_print(f"API call to {url} failed: {e}")
        return None

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        safe_print(f"Credentials file not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    
    query = "Hydro"
    safe_print(f"\nSearching Gmail with query: '{query}'...")
    
    search_res = call_gmail_api(
        access_token,
        "https://www.googleapis.com/gmail/v1/users/me/messages",
        {"q": query, "maxResults": 15}
    )
    
    if not search_res or "messages" not in search_res:
        safe_print("No messages found matching the query. Trying a broader search for 'license' or 'certificate'...")
        search_res = call_gmail_api(
            access_token,
            "https://www.googleapis.com/gmail/v1/users/me/messages",
            {"q": "license certificate", "maxResults": 15}
        )
        
    if not search_res or "messages" not in search_res:
        safe_print("Still no messages found. Listing the 15 most recent emails instead to see what is there...")
        search_res = call_gmail_api(
            access_token,
            "https://www.googleapis.com/gmail/v1/users/me/messages",
            {"maxResults": 15}
        )
        
    if not search_res or "messages" not in search_res:
        safe_print("No emails found in the account.")
        return
        
    safe_print(f"Found {len(search_res['messages'])} messages. Fetching details...\n")
    
    out_lines = []
    
    for msg_meta in search_res["messages"]:
        msg_id = msg_meta["id"]
        msg = call_gmail_api(access_token, f"https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}")
        if not msg:
            continue
            
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "(Unknown Sender)")
        date = next((h["value"] for h in headers if h["name"].lower() == "date"), "(Unknown Date)")
        
        snippet = msg.get("snippet", "")
        
        # Let's get body content if possible
        body = ""
        parts = payload.get("parts", [])
        if not parts and payload.get("body", {}).get("data"):
            body_data = payload["body"]["data"]
            body = base64.urlsafe_b64decode(body_data.encode("UTF-8")).decode("UTF-8", errors="ignore")
        else:
            # Recursively find body
            def get_text_body(part_list):
                for p in part_list:
                    mime = p.get("mimeType", "")
                    if mime == "text/plain" and p.get("body", {}).get("data"):
                        return base64.urlsafe_b64decode(p["body"]["data"].encode("UTF-8")).decode("UTF-8", errors="ignore")
                    elif p.get("parts"):
                        b = get_text_body(p["parts"])
                        if b: return b
                return ""
            body = get_text_body(parts)
            
        out_lines.append("-" * 80)
        out_lines.append(f"FROM:    {sender}")
        out_lines.append(f"SUBJECT: {subject}")
        out_lines.append(f"DATE:    {date}")
        out_lines.append(f"SNIPPET: {snippet}")
        if body:
            out_lines.append("\nBODY:")
            out_lines.append(body)
        out_lines.append("-" * 80 + "\n")
        
        # Safe print short snippet to console
        safe_print(f"FROM: {sender} | SUBJECT: {subject}")
        safe_print(f"Snippet: {snippet[:150]}")
        safe_print("-" * 50)

    # Write full output in UTF-8
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    safe_print(f"\nWritten all {len(search_res['messages'])} full emails to {OUTPUT_FILE} successfully!")

if __name__ == "__main__":
    main()
