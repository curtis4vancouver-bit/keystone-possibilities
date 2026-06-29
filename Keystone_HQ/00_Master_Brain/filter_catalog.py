import sys

try:
    with open('docker_mcp_catalog.txt', 'r', encoding='utf-16') as f:
        lines = f.readlines()
except UnicodeError:
    with open('docker_mcp_catalog.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

servers = []
current = {}
for line in lines:
    line = line.strip()
    if line.startswith('Title:'):
        current['title'] = line[6:].strip()
    elif line.startswith('Description:'):
        current['desc'] = line[12:].strip()
    elif line.startswith('Tools:'):
        servers.append(current)
        current = {}

keywords = ['youtube', 'seo', 'audio', 'notion', 'slack', 'mail', 'social', 'crm', 'postgres', 'neo4j', 'redis', 'rag', 'memory', 'browser']

count = 0
for s in servers:
    title = s.get('title', '').lower()
    desc = s.get('desc', '').lower()
    if any(k in title or k in desc for k in keywords):
        try:
            print(f"--- {s.get('title')} ---")
            desc_clean = s.get('desc').encode('ascii', 'ignore').decode('ascii')
            print(f"{desc_clean}\n")
            count += 1
        except Exception:
            pass

if count == 0:
    print("No servers found matching keywords.")
