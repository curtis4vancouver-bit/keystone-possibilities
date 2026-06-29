from qdrant_client import QdrantClient

def list_collections():
    client = QdrantClient(url="http://localhost:6333")
    try:
        collections = client.get_collections().collections
        print("Existing collections in Qdrant:")
        for c in collections:
            info = client.get_collection(collection_name=c.name)
            print(f"  - {c.name}: {info.points_count} points")
    except Exception as e:
        print(f"Error listing collections: {e}")

if __name__ == "__main__":
    list_collections()
