import time
from qdrant_client import QdrantClient
from qdrant_client.http import models

def main():
    print("Connecting to Qdrant...")
    client = QdrantClient(url="http://localhost:6333")
    collection_name = "keystone_unified"

    if not client.collection_exists(collection_name):
        print(f"Error: Collection '{collection_name}' does not exist.")
        return

    # Check initial config
    info = client.get_collection(collection_name)
    print(f"Current collection status: {info.status}")
    print(f"Points count: {info.points_count}")

    print("\n[STEP 1] Applying TurboQuant 4-bit compression & storing vectors on disk...")
    try:
        client.update_collection(
            collection_name=collection_name,
            vectors_config={
                "fast-bge-small-en-v1.5": models.VectorParamsDiff(
                    on_disk=True  # Store full-precision vectors on disk
                )
            },
            quantization_config=models.TurboQuantization(
                turbo=models.TurboQuantQuantizationConfig(
                    bits=models.TurboQuantBitSize.BITS4,
                    always_ram=True  # Keep quantized vectors in RAM
                )
            )
        )
        print("Update command sent successfully.")
    except Exception as e:
        print(f"Failed to update collection config: {e}")
        return

    print("\n[STEP 2] Monitoring optimization (waiting for status to return to 'green')...")
    start_time = time.time()
    while True:
        info = client.get_collection(collection_name)
        elapsed = time.time() - start_time
        print(f"[{elapsed:.1f}s] Status: {info.status} | Optimizers: {info.optimizer_status} | Points: {info.points_count}")
        if info.status == models.CollectionStatus.GREEN:
            print("\nOptimization complete! Collection status is GREEN.")
            break
        time.sleep(3)

    print("\n[STEP 3] Performing sanity check query...")
    # Query with a dummy vector of 384 dimensions (BAAI/bge-small-en-v1.5 dimensions)
    try:
        dummy_vector = [0.0] * 384
        response = client.query_points(
            collection_name=collection_name,
            query=dummy_vector,
            using="fast-bge-small-en-v1.5",
            limit=2
        )
        results = response.points
        print(f"Sanity check search returned {len(results)} results.")
        for i, r in enumerate(results):
            print(f"  Result {i+1}: ID={r.id}, Score={r.score:.4f}, Payload Keys={list(r.payload.keys()) if r.payload else None}")
        print("\nAll checks PASSED successfully!")
    except Exception as e:
        print(f"Sanity search query failed: {e}")

if __name__ == "__main__":
    main()
