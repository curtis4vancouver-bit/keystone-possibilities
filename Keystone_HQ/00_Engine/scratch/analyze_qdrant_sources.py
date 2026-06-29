from qdrant_client import QdrantClient, models

def analyze_all_sources_per_tenant():
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "keystone_unified"
    
    namespaces = ["possibilities", "music", "protocol_brand", "content_pipeline", "general", "local_seo", "webmaster"]
    
    print("Fetching points per tenant (limit=15000 per tenant, bypassing offsets)...")
    
    data = {}
    total_loaded = 0
    
    for ns in namespaces:
        try:
            print(f"Loading namespace '{ns}'...")
            res, next_offset = client.scroll(
                collection_name=collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns)
                        )
                    ]
                ),
                limit=15000,
                with_payload=True,
                with_vectors=False,
                offset=None
            )
            
            data[ns] = {}
            for point in res:
                p = point.payload or {}
                source = p.get("source") or p.get("path") or p.get("filename") or "unknown_source"
                data[ns][source] = data[ns].get(source, 0) + 1
            
            print(f"  Loaded {len(res)} points for '{ns}'. Next offset would be: {next_offset}")
            total_loaded += len(res)
            
        except Exception as e:
            print(f"  Error loading namespace '{ns}': {e}")
            
    print(f"\nTotal points successfully analyzed: {total_loaded}")
    
    print("\n==================================================")
    print("DETAILED QDRANT VECTOR SOURCE ANALYSIS")
    print("==================================================")
    
    total_unique_docs = 0
    for tenant, sources in sorted(data.items()):
        tenant_total = sum(sources.values())
        print(f"\nNamespace: '{tenant}' (Total vectors: {tenant_total})")
        print(f"Unique source documents: {len(sources)}")
        total_unique_docs += len(sources)
        
        # Sort sources by chunk count descending
        sorted_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
        print("Top 15 documents by chunk count:")
        for doc, count in sorted_sources[:15]:
            print(f"  - {count:4d} chunks | {doc}")
        if len(sorted_sources) > 15:
            print(f"  - ... and {len(sorted_sources) - 15} more files")
            
    print("\n==================================================")
    print(f"Grand Total Unique Source Documents: {total_unique_docs}")
    print(f"Grand Total Vectors (Chunks): {total_loaded}")
    print("==================================================")

if __name__ == "__main__":
    analyze_all_sources_per_tenant()
