from qdrant_client import QdrantClient, models

def test_scroll():
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "keystone_unified"
    
    # We know that possibilities namespace panics when we scroll it.
    # Let's test with_payload=False, with_vectors=False
    print("Testing scroll with_payload=False, with_vectors=False on 'possibilities'...")
    try:
        res, next_offset = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value="possibilities")
                    )
                ]
            ),
            limit=10,
            with_payload=False,
            with_vectors=False
        )
        print(f"Success! Retrieved {len(res)} points.")
        for point in res:
            print(f"  Point ID: {point.id}")
    except Exception as e:
        print(f"Failed: {e}")

    # Let's test with_payload=True, with_vectors=False
    print("\nTesting scroll with_payload=True, with_vectors=False on 'possibilities'...")
    try:
        res, next_offset = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value="possibilities")
                    )
                ]
            ),
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        print(f"Success! Retrieved {len(res)} points.")
    except Exception as e:
        print(f"Failed: {e}")

    # Let's test with_payload=False, with_vectors=True
    print("\nTesting scroll with_payload=False, with_vectors=True on 'possibilities'...")
    try:
        res, next_offset = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value="possibilities")
                    )
                ]
            ),
            limit=10,
            with_payload=False,
            with_vectors=True
        )
        print(f"Success! Retrieved {len(res)} points.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_scroll()
