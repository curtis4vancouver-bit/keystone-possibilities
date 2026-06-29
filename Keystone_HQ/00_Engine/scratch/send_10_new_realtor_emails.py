import json
import urllib.request
import urllib.parse
import os
import datetime
import base64
import sys
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
LEAD_LIST_MD = r"C:\Users\Curtis\.gemini\antigravity\knowledge\sea_to_sky_realtor_leads\artifacts\agent_email_list.md"
TRACKER_FILE = r"C:\Users\Curtis\.gemini\antigravity\knowledge\outreach_campaign\artifacts\campaign_tracker.md"
TEMPLATE_PATH = r"C:\Users\Curtis\.gemini\antigravity\knowledge\realtor_email_flyer\artifacts\project_manager_email_template.html"

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

def refresh_token(creds):
    safe_print("[GMAIL] Refreshing OAuth2 token...")
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
            new_expiry = (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).isoformat()
            
            creds["token"] = access_token
            creds["expiry"] = new_expiry
            
            with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
                json.dump(creds, f, indent=2)
            
            safe_print(f"[GMAIL] Token refreshed successfully! Expires at: {new_expiry}")
            return access_token
    except Exception as e:
        safe_print(f"[GMAIL] Failed to refresh token: {e}")
        raise e

def send_gmail_api(access_token, from_email, to_email, subject, html_content):
    message = MIMEMultipart('alternative')
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    
    part = MIMEText(html_content, 'html', 'utf-8')
    message.attach(part)
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"
    data = json.dumps({"raw": raw_message}).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except Exception as e:
        safe_print(f"[GMAIL] Failed to send email to {to_email}: {e}")
        return None

def parse_leads(file_path):
    leads = []
    pattern = re.compile(r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    num = match.group(1).strip()
                    name = match.group(2).strip()
                    email = match.group(3).strip()
                    brokerage = match.group(4).strip()
                    location = match.group(5).strip()
                    if "@" in email:
                        leads.append({
                            "name": name,
                            "email": email,
                            "brokerage": brokerage,
                            "location": location
                        })
    return leads

def parse_tracker_emails(file_path):
    contacted_emails = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
            for email in emails:
                contacted_emails.add(email.lower().strip())
    return contacted_emails

def append_to_tracker(tracker_path, lead):
    date_str = datetime.date.today().strftime("%B %d, %Y") # e.g. "May 24, 2026"
    new_line = f"| {date_str} | {lead['name']} | Realtor - {lead['location']} | {lead['email']} | Project Manager Luxury Flyer | SENT | Wait 5 days for reply |\n"
    
    try:
        with open(tracker_path, "a", encoding="utf-8") as f:
            f.write(new_line)
        safe_print(f"[TRACKER] Appended {lead['email']} to tracker.")
    except Exception as e:
        safe_print(f"[TRACKER] Failed to append {lead['email']} to tracker: {e}")

def main():
    if not os.path.exists(CREDENTIALS_PATH):
        safe_print(f"[ERROR] Credentials file not found at {CREDENTIALS_PATH}")
        return
    if not os.path.exists(LEAD_LIST_MD):
        safe_print(f"[ERROR] Lead list file not found at {LEAD_LIST_MD}")
        return
    if not os.path.exists(TEMPLATE_PATH):
        safe_print(f"[ERROR] Template file not found at {TEMPLATE_PATH}")
        return
    if not os.path.exists(TRACKER_FILE):
        safe_print(f"[ERROR] Tracker file not found at {TRACKER_FILE}")
        return

    # Load credentials
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    from_email = "curtis4vancouver@gmail.com"
    
    # Load HTML template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        base_template = f.read()
        
    # Get pending leads
    leads = parse_leads(LEAD_LIST_MD)
    contacted = parse_tracker_emails(TRACKER_FILE)
    
    pending = [lead for lead in leads if lead["email"].lower().strip() not in contacted]
    
    targets = pending[:10]
    safe_print(f"[GMAIL] Found {len(pending)} pending leads. Sending next {len(targets)} emails...\n")
    
    if not targets:
        safe_print("[GMAIL] No pending leads left to email!")
        return

    for lead in targets:
        name = lead["name"]
        first_name = name.split(" ")[0].strip()
        email = lead["email"]
        brokerage = lead["brokerage"]
        location = lead["location"]
        
        subject = f"Project Management & Developer Support in Squamish/Whistler — {brokerage}"
        
        # Build premium personalized introductory text
        personalized_greeting = (
            f"<p style=\"font-size:14px;color:#C9A84C;text-align:left;margin-top:0;font-family:Arial,sans-serif;\">Hi {first_name},</p>"
            f"<p style=\"font-size:14px;color:#999999;text-align:left;line-height:1.8;font-family:Arial,sans-serif;\">"
            f"As a real estate advisor with <strong>{brokerage}</strong> in <strong>{location}</strong>, I wanted to reach out. "
            f"When your clients purchase a fixer-upper or plan a custom luxury build in the corridor, having an engineering-grade local Project Manager protects their investment, ensures Step Code compliance, and frees up your time to focus on listing inventory. "
            f"Keystone Possibilities provides elite, flat-fee Project Management services to oversee builds from initial zoning and permits to final occupancy.</p>"
        )
        
        # Replace the generic intro in the minified template with our personalized intro
        generic_p_tag = '<p style="margin:18px auto 0 auto;max-width:440px;font-size:14px;color:#999999;line-height:1.8;">When your clients buy a property that needs a complete overhaul, they need a trusted partner. Keystone Possibilities provides elite Project Management services to oversee luxury builds and renovations from permits to completion.</p>'
        
        html_content = base_template.replace(generic_p_tag, personalized_greeting)
        
        # Send via API
        safe_print(f"[SENDING] To: {name} ({email}) | Subject: {subject}...")
        send_result = send_gmail_api(access_token, from_email, email, subject, html_content)
        
        if send_result:
            safe_print(f"[SUCCESS] Email sent successfully to {email}! Message ID: {send_result.get('id')}")
            append_to_tracker(TRACKER_FILE, lead)
        else:
            safe_print(f"[FAILED] Failed to send email to {email}")
            
    safe_print("\n[GMAIL] Outreach campaign chunk completed successfully!")

if __name__ == "__main__":
    main()
