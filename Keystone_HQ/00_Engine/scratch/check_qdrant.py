from qdrant_client import QdrantClient, models

def check_qdrant_types():
    client = QdrantClient(url="http://localhost:6333")
    
    try:
        # Check overall points count
        info = client.get_collection(collection_name="keystone_unified")
        print(f"Total points: {info.points_count}")
        
        # Count points with type == 'obsidian_note'
        res_obsidian = client.count(
            collection_name="keystone_unified",
            count_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="type",
                        match=models.MatchValue(value="obsidian_note")
                    )
                ]
            )
        )
        print(f"Obsidian notes: {res_obsidian.count} vectors")
        
        # Count points with type != 'obsidian_note' (or no type field)
        res_other = client.count(
            collection_name="keystone_unified",
            count_filter=models.Filter(
                must_not=[
                    models.FieldCondition(
                        key="type",
                        match=models.MatchValue(value="obsidian_note")
                    )
                ]
            )
        )
        print(f"Other types (including pre-existing): {res_other.count} vectors")
        
        # Print a sample of non-obsidian note vectors
        scroll_res = client.scroll(
            collection_name="keystone_unified",
            scroll_filter=models.Filter(
                must_not=[
                    models.FieldCondition(
                        key="type",
                        match=models.MatchValue(value="obsidian_note")
                    )
                ]
            ),
            limit=20,
            with_payload=True,
            with_vectors=False
        )
        print("\nSample sources for other (non-obsidian note) vectors:")
        sources = set()
        for point in scroll_res[0]:
            p = point.payload or {}
            source = p.get("source") or p.get("path") or p.get("file")
            tenant = p.get("tenant_id")
            type_val = p.get("type")
            created = p.get("created_at")
            print(f"  - Tenant: {tenant} | Type: {type_val} | Source: {source} | Created: {created}")
            
    except Exception as e:
        print(f"Error querying Qdrant: {e}")

if __name__ == "__main__":
    check_qdrant_types()
