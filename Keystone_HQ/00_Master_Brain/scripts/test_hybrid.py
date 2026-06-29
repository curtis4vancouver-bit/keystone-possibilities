"""Test hybrid search (dense+sparse RRF) vs dense-only to show the improvement."""
import sys, time
sys.path.insert(0, r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Qdrant_Brain')

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"
SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"
COLLECTION = "keystone_unified"

print("Loading models...")
embed = TextEmbedding(EMBED_MODEL)
sparse_embed = SparseTextEmbedding(SPARSE_MODEL)
client = QdrantClient(url="http://localhost:6333")

# Test queries that stress keyword matching (where hybrid shines)
test_queries = [
    ("BPC-157 dosing protocol", "protocol_brand"),
    ("BCBC Ministerial Order BA 2024 03", "possibilities"),
    ("SES single egress stair code", "possibilities"),
]

for query, namespace in test_queries:
    print(f"\n{'='*70}")
    print(f"QUERY: {query}")
    print(f"NAMESPACE: {namespace}")
    print(f"{'='*70}")
    
    q_filter = models.Filter(
        must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value=namespace))]
    )
    
    # Dense-only search
    t0 = time.time()
    query_vec = list(embed.embed([query]))[0].tolist()
    dense_results = client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        using=VECTOR_NAME,
        limit=5,
        query_filter=q_filter,
    ).points
    dense_time = time.time() - t0
    
    # Hybrid search (dense + sparse + RRF)
    t0 = time.time()
    sparse_result = list(sparse_embed.embed([query]))[0]
    sparse_query = models.SparseVector(
        indices=sparse_result.indices.tolist(),
        values=sparse_result.values.tolist(),
    )
    hybrid_results = client.query_points(
        collection_name=COLLECTION,
        prefetch=[
            models.Prefetch(query=query_vec, using=VECTOR_NAME, limit=10, filter=q_filter),
            models.Prefetch(query=sparse_query, using=SPARSE_VECTOR_NAME, limit=10, filter=q_filter),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=5,
        with_payload=True,
    ).points
    hybrid_time = time.time() - t0
    
    print(f"\n  DENSE-ONLY ({dense_time*1000:.0f}ms):")
    for i, r in enumerate(dense_results[:3]):
        src = r.payload.get('source', '?')
        doc = r.payload.get('document', '')[:90].replace('\n', ' ')
        print(f"    {i+1}. [{r.score:.3f}] {src}: {doc}")
    
    print(f"\n  HYBRID RRF ({hybrid_time*1000:.0f}ms):")
    for i, r in enumerate(hybrid_results[:3]):
        src = r.payload.get('source', '?')
        doc = r.payload.get('document', '')[:90].replace('\n', ' ')
        print(f"    {i+1}. [{r.score:.4f}] {src}: {doc}")
    
    # Check if different results surfaced
    dense_sources = [r.payload.get('source','') for r in dense_results[:3]]
    hybrid_sources = [r.payload.get('source','') for r in hybrid_results[:3]]
    if dense_sources != hybrid_sources:
        new_sources = set(hybrid_sources) - set(dense_sources)
        if new_sources:
            print(f"\n  ** HYBRID SURFACED NEW RESULTS: {new_sources}")
        else:
            print(f"\n  ** HYBRID REORDERED RESULTS")
    else:
        print(f"\n  -> Same top 3 (both methods agree)")

print("\n\nDone!")
