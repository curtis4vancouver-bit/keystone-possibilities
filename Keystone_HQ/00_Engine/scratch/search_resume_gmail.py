import json
import urllib.request
import urllib.parse
import os
import datetime
import base64
import sys

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
OUTPUT_FILE = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\resume_gmail_results.txt"

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
        expires_in = res_data.get("expires_in", 3600)
        creds["token"] = access_token
        creds["expiry"] = (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).isoformat()
        with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2)
        return access_token

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
    
    queries = ["resume", "Wayne Stevenson resume", "Wayne Carpenter", "from:curtis4vancouver"]
    search_res = None
    for query in queries:
        print(f"Searching with query: '{query}'...")
        res = call_gmail_api(
            access_token,
            "https://www.googleapis.com/gmail/v1/users/me/messages",
            {"q": query, "maxResults": 10}
        )
        if res and "messages" in res:
            search_res = res
            print(f"Found {len(res['messages'])} messages with query '{query}'.")
            break
            
    if not search_res or "messages" not in search_res:
        print("No messages found in standard searches. Listing the 20 most recent emails...")
        search_res = call_gmail_api(
            access_token,
            "https://www.googleapis.com/gmail/v1/users/me/messages",
            {"maxResults": 20}
        )
        
    if not search_res or "messages" not in search_res:
        print("No emails found.")
        return
        
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
        
        body = ""
        parts = payload.get("parts", [])
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
            
        out_lines.append("-" * 80)
        out_lines.append(f"MESSAGE ID: {msg_id}")
        out_lines.append(f"FROM:       {sender}")
        out_lines.append(f"SUBJECT:    {subject}")
        out_lines.append(f"DATE:       {date}")
        out_lines.append(f"SNIPPET:    {snippet}")
        if body:
            out_lines.append("\nBODY:")
            out_lines.append(body)
        
        # Check if there are attachments and list them
        attachments = []
        if parts:
            for p in parts:
                filename = p.get("filename", "")
                if filename:
                    attachments.append((filename, p.get("body", {}).get("attachmentId", "")))
        if attachments:
            out_lines.append("\nATTACHMENTS:")
            for filename, att_id in attachments:
                out_lines.append(f" - {filename} (ID: {att_id})")
                
        out_lines.append("-" * 80 + "\n")
        
        print(f"Fetched: {subject} | Date: {date}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"\nWritten all results to {OUTPUT_FILE} successfully!")

if __name__ == "__main__":
    main()
