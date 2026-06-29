"""Full system status report."""
from qdrant_client import QdrantClient
import json

c = QdrantClient(url='http://localhost:6333')
info = c.get_collection('keystone_unified')

print("=== QDRANT VECTOR BRAIN ===")
print(f"Points: {info.points_count}")
print(f"Status: {info.status}")
print(f"Segments: {info.segments_count}")

hnsw = info.config.hnsw_config
print(f"HNSW: m={hnsw.m}, ef_construct={hnsw.ef_construct}")
print(f"Quantization: {info.config.quantization_config}")

dense_cfg = info.config.params.vectors
sparse_cfg = info.config.params.sparse_vectors
print(f"Dense vectors: {list(dense_cfg.keys()) if isinstance(dense_cfg, dict) else 'single'}")
print(f"Sparse vectors: {list(sparse_cfg.keys()) if sparse_cfg else 'None'}")

# Check sparse coverage
sample = c.scroll('keystone_unified', limit=100, with_vectors=True)[0]
has_sparse = sum(1 for p in sample if 'fast-sparse-splade_pp_en_v1' in (p.vector or {}))
print(f"Sparse coverage (sample): {has_sparse}/100")

# Namespace distribution
print("\n=== NAMESPACE DISTRIBUTION ===")
tenant_counts = {}
offset = None
while True:
    pts, offset = c.scroll('keystone_unified', limit=250, offset=offset, with_payload=True, with_vectors=False)
    if not pts:
        break
    for p in pts:
        tid = p.payload.get('tenant_id', 'unknown')
        tenant_counts[tid] = tenant_counts.get(tid, 0) + 1
    if offset is None:
        break

for tid in sorted(tenant_counts.keys(), key=lambda k: tenant_counts[k], reverse=True):
    pct = tenant_counts[tid] * 100 // info.points_count
    bar = '#' * (pct // 2)
    print(f"  {tid:20s}: {tenant_counts[tid]:6d} ({pct:2d}%) {bar}")
print(f"  {'TOTAL':20s}: {sum(tenant_counts.values()):6d}")
