import re
import os

LEAD_LIST_MD = r"C:\Users\Curtis\.gemini\antigravity\knowledge\sea_to_sky_realtor_leads\artifacts\agent_email_list.md"
TRACKER_FILE = r"C:\Users\Curtis\.gemini\antigravity\knowledge\outreach_campaign\artifacts\campaign_tracker.md"

def parse_leads(file_path):
    leads = []
    # Match markdown table row like: | 1 | Alexandra Smith | asmith@myseatosky.com | RE/MAX Sea to Sky | Whistler |
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
            # Find all emails in tracker
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
            for email in emails:
                contacted_emails.add(email.lower().strip())
    return contacted_emails

def main():
    leads = parse_leads(LEAD_LIST_MD)
    contacted = parse_tracker_emails(TRACKER_FILE)
    
    print(f"Total leads in list: {len(leads)}")
    print(f"Total contacted emails in tracker: {len(contacted)}")
    
    pending = []
    for lead in leads:
        if lead["email"].lower().strip() not in contacted:
            pending.append(lead)
            
    print(f"Pending leads: {len(pending)}")
    print("\nNext 12 pending leads:")
    for i, lead in enumerate(pending[:12], 1):
        print(f"{i}. {lead['name']} ({lead['email']}) - {lead['brokerage']} | {lead['location']}")

if __name__ == "__main__":
    main()
