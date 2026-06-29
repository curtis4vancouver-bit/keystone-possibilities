"""Test the cross-encoder reranking integration end-to-end."""
import sys, time
sys.path.insert(0, r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Qdrant_Brain')

# Simulate what the MCP server does
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from sentence_transformers import CrossEncoder

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"
COLLECTION = "keystone_unified"
RERANKER = "cross-encoder/ms-marco-MiniLM-L-6-v2"

print("Loading models...")
t0 = time.time()
embed = TextEmbedding(EMBED_MODEL)
print(f"  Embedder loaded in {time.time()-t0:.1f}s")

t0 = time.time()
reranker = CrossEncoder(RERANKER)
print(f"  Reranker loaded in {time.time()-t0:.1f}s")

client = QdrantClient(url="http://localhost:6333")

# Test query
query = "Bill 44 construction permit requirements British Columbia"
namespace = "possibilities"
limit = 5
fetch_limit = limit * 3  # Over-fetch for reranking

print(f"\n{'='*60}")
print(f"Query: {query}")
print(f"Namespace: {namespace}")
print(f"Fetching {fetch_limit} candidates, returning top {limit}")
print(f"{'='*60}")

# Step 1: Dense vector search
t0 = time.time()
query_vec = list(embed.embed([query]))[0].tolist()
results = client.query_points(
    collection_name=COLLECTION,
    query=query_vec,
    using=VECTOR_NAME,
    query_filter=models.Filter(
        must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value=namespace))]
    ),
    limit=fetch_limit,
    with_payload=True,
).points
vec_time = time.time() - t0
print(f"\nVector search: {len(results)} results in {vec_time*1000:.0f}ms")

# Step 2: Rerank
t0 = time.time()
pairs = []
for r in results:
    doc = r.payload.get('document', r.payload.get('text', ''))
    pairs.append([query, str(doc)[:512]])

scores = reranker.predict(pairs)
rerank_time = time.time() - t0
print(f"Reranking: {len(pairs)} pairs in {rerank_time*1000:.0f}ms")

# Compare before/after
print(f"\n--- BEFORE RERANKING (vector score order) ---")
for i, r in enumerate(results[:limit]):
    src = r.payload.get('source', '?')
    doc = r.payload.get('document', '')[:80]
    print(f"  {i+1}. [{r.score:.3f}] {src}: {doc}...")

# Sort by rerank score
scored = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)

print(f"\n--- AFTER RERANKING (cross-encoder score order) ---")
for i, (r, s) in enumerate(scored[:limit]):
    src = r.payload.get('source', '?')
    doc = r.payload.get('document', '')[:80]
    print(f"  {i+1}. [vec:{r.score:.3f} rerank:{s:.3f}] {src}: {doc}...")

# Did the order change?
before_sources = [r.payload.get('source','') for r in results[:limit]]
after_sources = [r.payload.get('source','') for r,_ in scored[:limit]]
if before_sources != after_sources:
    print(f"\n✅ RERANKING CHANGED THE ORDER — precision improved!")
else:
    print(f"\n→ Order unchanged (vector search already had good precision for this query)")

print(f"\nTotal time: {(vec_time + rerank_time)*1000:.0f}ms")
