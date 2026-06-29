"""
Backfill SPLADE sparse vectors for all existing points in keystone_unified.
Reads each point's document text, generates sparse embeddings, and upserts.
Uses batched processing for efficiency.
"""
import time
from qdrant_client import QdrantClient, models
from fastembed import SparseTextEmbedding

COLLECTION = "keystone_unified"
SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"
BATCH_SIZE = 100

print("Connecting to Qdrant...")
client = QdrantClient(url="http://localhost:6333")

print(f"Loading SPLADE model: {SPARSE_MODEL}")
sparse_embed = SparseTextEmbedding(SPARSE_MODEL)

# Get total count
info = client.get_collection(COLLECTION)
total = info.points_count
print(f"Total points to process: {total}")

processed = 0
failed = 0
already_has = 0
offset = None
t0 = time.time()

while True:
    # Scroll through all points
    points, next_offset = client.scroll(
        collection_name=COLLECTION,
        limit=BATCH_SIZE,
        offset=offset,
        with_payload=True,
        with_vectors=False,  # Don't need to read existing vectors
    )
    
    if not points:
        break
    
    # Collect texts for batch embedding
    texts = []
    point_ids = []
    for p in points:
        doc_text = p.payload.get('document', p.payload.get('text', ''))
        if not doc_text or len(str(doc_text).strip()) < 10:
            failed += 1
            continue
        texts.append(str(doc_text))
        point_ids.append(p.id)
    
    if texts:
        # Generate sparse embeddings in batch
        sparse_vecs = list(sparse_embed.embed(texts))
        
        # Build upsert points with just the sparse vector
        update_points = []
        for pid, svec in zip(point_ids, sparse_vecs):
            update_points.append(
                models.PointVectors(
                    id=pid,
                    vector={
                        SPARSE_VECTOR_NAME: models.SparseVector(
                            indices=svec.indices.tolist(),
                            values=svec.values.tolist(),
                        )
                    }
                )
            )
        
        # Update vectors without touching payload or dense vectors
        client.update_vectors(
            collection_name=COLLECTION,
            points=update_points,
        )
        processed += len(update_points)
    
    elapsed = time.time() - t0
    rate = processed / elapsed if elapsed > 0 else 0
    print(f"  Processed: {processed}/{total} ({processed*100//total}%) | "
          f"Rate: {rate:.0f} pts/sec | Failed: {failed} | "
          f"Elapsed: {elapsed:.0f}s")
    
    if next_offset is None:
        break
    offset = next_offset

elapsed = time.time() - t0
print(f"\nDone! Processed {processed} points in {elapsed:.1f}s")
print(f"Failed/skipped: {failed}")

# Verify
pts = client.scroll(collection_name=COLLECTION, limit=3, with_vectors=True)[0]
for p in pts:
    vec = p.vector or {}
    print(f"  Point {p.id}: sparse={'fast-sparse-splade_pp_en_v1' in vec}")
