"""Test whether Qdrant SEARCH queries (as opposed to SCROLL) work fine across all namespaces,
including the corrupted ones. The corruption might only affect full-collection scrolling,
not HNSW-indexed similarity search."""

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

def test_search_all_namespaces():
    client = QdrantClient(url="http://localhost:6333")
    embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    
    query = "construction project management Bill 44"
    query_vec = list(embed_model.embed([query]))[0].tolist()
    
    namespaces = ["possibilities", "music", "protocol_brand", "content_pipeline", "general", "local_seo", "webmaster"]
    
    for ns in namespaces:
        try:
            results = client.query_points(
                collection_name="keystone_unified",
                query=query_vec,
                using="fast-bge-small-en-v1.5",
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns)
                        )
                    ]
                ),
                limit=3,
                with_payload=True,
            )
            count = len(results.points)
            if count > 0:
                top_score = results.points[0].score
                top_source = results.points[0].payload.get("source", "?")
                print(f"  {ns}: OK ({count} results, top score={top_score:.3f}, source={top_source[:60]})")
            else:
                print(f"  {ns}: OK (0 results)")
        except Exception as e:
            err_str = str(e)[:100]
            print(f"  {ns}: FAILED ({err_str})")

if __name__ == "__main__":
    print("Testing vector SEARCH (not scroll) across all namespaces...")
    test_search_all_namespaces()
