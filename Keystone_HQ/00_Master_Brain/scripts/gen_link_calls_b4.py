import json

data = open(r'C:\Users\Curtis\.gemini\antigravity\brain\123af895-a55b-41b0-bc08-417dda0b4305\.system_generated\steps\1260\output.txt', encoding='utf-8').read()
parsed = json.loads(data)

calls = []
for o in parsed['orphans']:
    name = o['name']
    parts = name.rsplit('/', 1)
    if len(parts) == 2:
        parent_dir = parts[0]
        from_page = f"{parent_dir}/_INDEX"
    else:
        from_page = "MAP_OF_CONTENTS"
    calls.append({"from": from_page, "to": name})

with open(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\_link_calls_batch4.json', 'w', encoding='utf-8') as f:
    json.dump(calls, f, indent=2)

print(f"Generated {len(calls)} link calls for batch 4 (FINAL)")
print(f"Total orphans remaining: {parsed['total']}")

cats = {}
for o in parsed['orphans']:
    parts = o['name'].split('/')
    cat = '/'.join(parts[:2]) if len(parts) > 2 else parts[0]
    cats[cat] = cats.get(cat, 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")
