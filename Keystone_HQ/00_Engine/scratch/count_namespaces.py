from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
counts = {}
offset = None

import sys
while True:
    print(f"Scrolling with offset: {offset}...")
    try:
        records, offset = client.scroll(
            collection_name="keystone_unified",
            limit=500,
            with_payload=["tenant_id"],
            with_vectors=False,
            offset=offset
        )
    except Exception as e:
        print(f"Error scrolling: {e}", file=sys.stderr)
        break
    
    print(f"Retrieved {len(records)} records. Next offset: {offset}")
    for r in records:
        if r.payload:
            tid = r.payload.get("tenant_id", "unknown")
        else:
            tid = "unknown"
        counts[tid] = counts.get(tid, 0) + 1
    if offset is None or len(records) == 0:
        break

print("Tenant counts:")
for k, v in sorted(counts.items()):
    print(f"  - {k}: {v} vectors")
print(f"Total: {sum(counts.values())}")
