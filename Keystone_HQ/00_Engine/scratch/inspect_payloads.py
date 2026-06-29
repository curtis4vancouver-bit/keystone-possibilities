import json
from pathlib import Path

payload_file = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\sync_doc_payloads.json")
with open(payload_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for doc_id, info in data.items():
    print(f"Doc ID: {doc_id}")
    print(f"  Name: {info['name']}")
    print(f"  Length: {len(info['content'])} characters")
