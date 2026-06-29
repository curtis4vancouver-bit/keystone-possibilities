from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
import os

client = QdrantClient(url="http://localhost:6333")
ops_file = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\_redistribute_ops.json"

with open(ops_file, "r", encoding="utf-8") as f:
    ops = json.load(f)

target_keywords = {}
for op in ops:
    ns = op["target_namespace"]
    if ns not in target_keywords:
        target_keywords[ns] = []
    target_keywords[ns].append(op["query"].lower())

print("Starting scan of 'general' namespace...")
offset = None
moved_counts = {ns: 0 for ns in target_keywords}
total_scanned = 0

while True:
    records, next_offset = client.scroll(
        collection_name="keystone_unified",
        limit=500,
        with_payload=True,
        with_vectors=False,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id",
                    match=models.MatchValue(value="general")
                )
            ]
        ),
        offset=offset
    )
    
    total_scanned += len(records)
    for record in records:
        content = record.payload.get("document", "")
        if not content:
            content = str(record.payload)
        content_lower = content.lower()
        source = record.payload.get("source", "").lower()
        
        # Search both document text and source name
        search_text = content_lower + " " + source

        new_tenant = None
        # We only assign one tenant. First match wins.
        for target, keywords in target_keywords.items():
            if any(k in search_text for k in keywords):
                new_tenant = target
                break
        
        if new_tenant:
            client.set_payload(
                collection_name="keystone_unified",
                payload={"tenant_id": new_tenant},
                points=[record.id]
            )
            moved_counts[new_tenant] += 1
            
    if next_offset is None:
        break
    offset = next_offset

print(f"Scanned {total_scanned} vectors.")
for ns, count in moved_counts.items():
    print(f"Moved to {ns}: {count}")
print(f"Total moved: {sum(moved_counts.values())}")
