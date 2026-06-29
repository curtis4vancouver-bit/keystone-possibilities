from qdrant_client import QdrantClient
c = QdrantClient(url='http://localhost:6333')
pts = c.scroll(collection_name='keystone_unified', limit=3, with_vectors=True)[0]
for p in pts:
    vec = p.vector or {}
    has_dense = 'fast-bge-small-en-v1.5' in vec
    has_sparse = 'fast-sparse-splade_pp_en_v1' in vec
    print(f'Point {p.id}: dense={has_dense}, sparse={has_sparse}, vector_keys={list(vec.keys())}')
