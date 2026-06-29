"""
Batch link orphans into the graph via graphthulhu link_pages API calls.
Generates a list of MCP calls to execute.
"""
import json

# Read the orphan list
data = open(r'C:\Users\Curtis\.gemini\antigravity\brain\123af895-a55b-41b0-bc08-417dda0b4305\.system_generated\steps\1119\output.txt', encoding='utf-8').read()
parsed = json.loads(data)

# For each orphan, determine its parent _INDEX
calls = []
for o in parsed['orphans']:
    name = o['name']  # e.g. Research_Archives/04_YT_Analytics/filename
    parts = name.rsplit('/', 1)
    if len(parts) == 2:
        parent_dir = parts[0]
        from_page = f"{parent_dir}/_INDEX"
    else:
        from_page = "Research_Archives/_INDEX"
    
    calls.append({
        "from": from_page,
        "to": name
    })

# Save for reference
with open('scripts/_link_calls.json', 'w', encoding='utf-8') as f:
    json.dump(calls, f, indent=2)

print(f"Generated {len(calls)} link calls")
print("First 5:")
for c in calls[:5]:
    print(f"  {c['from']} -> {c['to']}")
