import json

data = open(r'C:\Users\Curtis\.gemini\antigravity\brain\123af895-a55b-41b0-bc08-417dda0b4305\.system_generated\steps\1119\output.txt', encoding='utf-8').read()
parsed = json.loads(data)
for o in parsed['orphans']:
    print(o['name'])
print(f"---")
print(f"Returned: {parsed['returned']}, Total: {parsed['total']}")
