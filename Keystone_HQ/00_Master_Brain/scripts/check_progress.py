from qdrant_client import QdrantClient
c = QdrantClient(url='http://localhost:6333')
total = 0
has = 0
offset = None
for batch in range(5):
    pts, offset = c.scroll('keystone_unified', limit=100, offset=offset, with_vectors=True)
    total += len(pts)
    has += sum(1 for p in pts if 'fast-sparse-splade_pp_en_v1' in (p.vector or {}))
    if offset is None:
        break
pct = has * 100 // total if total else 0
est = has * 14915 // total if total else 0
print(f"Sampled {total} points: {has}/{total} have sparse ({pct}%)")
print(f"Estimated progress: ~{est}/14915 points done")
