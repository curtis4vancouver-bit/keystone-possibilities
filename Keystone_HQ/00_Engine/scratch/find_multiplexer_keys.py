import json

with open(r"C:\Users\Curtis\.gemini\antigravity\brain\c47c6452-cc70-4117-9f16-571f8aabc598\.system_generated\steps\1265\output.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys in output.txt:")
for k in data.keys():
    print(f" - {k} ({len(data[k])} tools)")
