import json
import urllib.request
import urllib.parse
import os
import datetime
import base64
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
        return res_data["access_token"]

def call_gmail_api(access_token, endpoint, params=None):
    url = endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Credentials not found at {CREDENTIALS_PATH}")
        return
        
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    
    print(f"Listing 10 most recent emails...")
    
    search_res = call_gmail_api(
        access_token,
        "https://www.googleapis.com/gmail/v1/users/me/messages",
        {"maxResults": 10}
    )

        
    if not search_res or "messages" not in search_res:
        print("No emails found.")
        return
        
    for msg_meta in search_res["messages"]:
        msg_id = msg_meta["id"]
        msg = call_gmail_api(access_token, f"https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}")
        if not msg:
            continue
            
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "(Unknown)")
        date = next((h["value"] for h in headers if h["name"].lower() == "date"), "(Unknown)")
        
        snippet = msg.get("snippet", "")
        print(f"\n=====================================")
        print(f"FROM: {sender}\nDATE: {date}\nSUBJECT: {subject}\nSNIPPET: {snippet}")
        print("=====================================")
        
        # Get body
        parts = payload.get("parts", [])
        body = ""
        if not parts and payload.get("body", {}).get("data"):
            body_data = payload["body"]["data"]
            body = base64.urlsafe_b64decode(body_data.encode("UTF-8")).decode("UTF-8", errors="ignore")
        else:
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
            
        if body:
            print("BODY DETAILS:")
            # Print first 1500 chars of body
            print(body[:2000])
            break

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
