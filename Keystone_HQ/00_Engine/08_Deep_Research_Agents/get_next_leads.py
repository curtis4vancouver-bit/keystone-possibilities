import re
import os

LEAD_LIST_MD = r"C:\Users\Curtis\.gemini\antigravity\knowledge\sea_to_sky_realtor_leads\artifacts\agent_email_list.md"
TRACKER_FILE = r"C:\Users\Curtis\.gemini\antigravity\knowledge\outreach_campaign\artifacts\campaign_tracker.md"

with open(LEAD_LIST_MD, 'r', encoding='utf-8') as f:
    content = f.read()

leads = []
pattern = re.compile(r'\|\s*\d+\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|')
for match in pattern.finditer(content):
    if '@' in match.group(2):
        leads.append(match.group(2).strip())

contacted = set()
if os.path.exists(TRACKER_FILE):
    with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
        contacted = set([e.lower() for e in re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', f.read())])

pending = [l for l in leads if l.lower() not in contacted]
print(pending[:12])
