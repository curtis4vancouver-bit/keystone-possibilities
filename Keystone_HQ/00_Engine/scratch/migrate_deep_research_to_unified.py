"""
Migrates all 2,885 deep research vectors from keystone_brain → keystone_unified.
Maps old namespace values to proper tenant_id values used in keystone_unified.
"""
import sys
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import uuid
import datetime

# Namespace → tenant_id mapping
NAMESPACE_TO_TENANT = {
    "webmaster": "webmaster",
    "music": "music",
    "content_pipeline": "content_pipeline",
    "local_seo": "local_seo",
    "protocol_brand": "protocol_brand",
    # Fallback for anything else
}

EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"

def main():
    client = QdrantClient(url="http://localhost:6333")
    embedder = TextEmbedding(model_name=EMBED_MODEL_NAME)
    
    # 1. Read all points from keystone_brain
    print("Reading all points from keystone_brain...")
    all_points = []
    offset = None
    while True:
        result = client.scroll(
            collection_name="keystone_brain",
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False  # We'll re-embed with the correct named vector
        )
        pts, offset = result
        all_points.extend(pts)
        if offset is None:
            break
    
    print(f"Total points to migrate: {len(all_points)}")
    
    # 2. Extract documents and prepare for re-embedding
    documents = []
    payloads = []
    
    for pt in all_points:
        meta = pt.payload
        doc_text = meta.get("document", "")
        if not doc_text:
            continue
            
        old_ns = meta.get("namespace", "webmaster")
        tenant_id = NAMESPACE_TO_TENANT.get(old_ns, "webmaster")
        
        new_payload = {
            "tenant_id": tenant_id,
            "source": meta.get("source", "deep_research/unknown"),
            "filename": meta.get("filename", "unknown"),
            "chunk_index": meta.get("chunk_index", 0),
            "created_at": meta.get("created_at", datetime.datetime.now().isoformat()),
            "document": doc_text,
            "migration_source": "keystone_brain_deep_research"
        }
        
        documents.append(doc_text)
        payloads.append(new_payload)
    
    print(f"Prepared {len(documents)} documents for migration")
    
    # 3. Embed in batches of 100
    BATCH_SIZE = 100
    total_upserted = 0
    
    for batch_start in range(0, len(documents), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(documents))
        batch_docs = documents[batch_start:batch_end]
        batch_payloads = payloads[batch_start:batch_end]
        
        # Generate embeddings
        embeddings = list(embedder.embed(batch_docs))
        
        # Build points
        points = []
        for i, (emb, payload) in enumerate(zip(embeddings, batch_payloads)):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                payload=payload,
                vector={VECTOR_NAME: emb.tolist()}
            )
            points.append(point)
        
        # Upsert to keystone_unified
        client.upsert(
            collection_name="keystone_unified",
            points=points
        )
        
        total_upserted += len(points)
        print(f"  Upserted batch {batch_start//BATCH_SIZE + 1}: {total_upserted}/{len(documents)} points")
    
    print(f"\n✅ Migration complete! {total_upserted} vectors moved to keystone_unified")
    
    # 4. Verify
    unified_info = client.get_collection("keystone_unified")
    print(f"keystone_unified now has {unified_info.points_count} total vectors")
    
    # 5. Delete old collection
    print("\nDeleting old keystone_brain collection...")
    client.delete_collection("keystone_brain")
    print("✅ keystone_brain deleted. All data now lives in keystone_unified.")

if __name__ == "__main__":
    main()
