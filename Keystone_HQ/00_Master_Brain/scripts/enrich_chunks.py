"""
Contextual Chunk Enrichment — Metadata Approach
================================================
Prepends source context to each chunk's text BEFORE re-embedding.
This makes embeddings "contextually aware" without LLM calls.

Strategy:
- Read each point's payload (source, tenant_id, document text)
- Build a context prefix from metadata
- Re-embed the ENRICHED text (dense + sparse) 
- Update vectors only (payload stays clean for display)

Example:
  Original: "it mandated at least two egress stairs for buildings over 3 storeys"
  Enriched: "[Keystone Possibilities | BC Building Code | 4_2_Blog_Content_Strategy.md] 
             it mandated at least two egress stairs for buildings over 3 storeys"
  
  Now the embedding captures BOTH the content AND the context.
"""
import time
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding, SparseTextEmbedding

COLLECTION = "keystone_unified"
DENSE_MODEL = "BAAI/bge-small-en-v1.5"
DENSE_VECTOR_NAME = "fast-bge-small-en-v1.5"
SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"
BATCH_SIZE = 50  # Smaller batches since we're doing both embeddings

# Namespace to human-readable brand names
BRAND_NAMES = {
    "possibilities": "Keystone Possibilities | Construction & PM",
    "protocol_brand": "Keystone Recomposition | Health Protocols",
    "music": "Keystone Recomposition | Music Production",
    "content_pipeline": "Keystone | Content Pipeline & Video Production",
    "master": "Keystone | System Infrastructure & Agent Architecture",
    "general": "Keystone | General Knowledge",
    "webmaster": "Keystone | Website & SEO",
    "local_seo": "Keystone | Local SEO & Google Business",
}

def build_context_prefix(source: str, namespace: str) -> str:
    """Build a rich context prefix from metadata."""
    brand = BRAND_NAMES.get(namespace, f"Keystone | {namespace}")
    
    # Clean up source name for readability
    clean_source = source.replace('.md', '').replace('_', ' ')
    # Remove date prefixes like "20260612_"
    if len(clean_source) > 9 and clean_source[:8].isdigit():
        clean_source = clean_source[9:]
    
    return f"[{brand} | Source: {clean_source}]"


print("Loading models...")
t0 = time.time()
dense_embed = TextEmbedding(DENSE_MODEL)
sparse_embed = SparseTextEmbedding(SPARSE_MODEL)
client = QdrantClient(url="http://localhost:6333")
print(f"Models loaded in {time.time()-t0:.1f}s")

info = client.get_collection(COLLECTION)
total = info.points_count
print(f"Total points to process: {total}")

processed = 0
failed = 0
offset = None
t0 = time.time()

while True:
    points, next_offset = client.scroll(
        collection_name=COLLECTION,
        limit=BATCH_SIZE,
        offset=offset,
        with_payload=True,
        with_vectors=False,
    )
    
    if not points:
        break
    
    # Build enriched texts for batch embedding
    enriched_texts = []
    point_ids = []
    for p in points:
        doc_text = p.payload.get('document', p.payload.get('text', ''))
        source = p.payload.get('source', 'unknown')
        namespace = p.payload.get('tenant_id', 'general')
        
        if not doc_text or len(str(doc_text).strip()) < 10:
            failed += 1
            continue
        
        # Build contextually-enriched text for embedding
        prefix = build_context_prefix(source, namespace)
        enriched = f"{prefix} {doc_text}"
        
        enriched_texts.append(enriched)
        point_ids.append(p.id)
    
    if enriched_texts:
        # Generate BOTH dense and sparse embeddings from enriched text
        dense_vecs = list(dense_embed.embed(enriched_texts))
        sparse_vecs = list(sparse_embed.embed(enriched_texts))
        
        # Build update points
        update_points = []
        for pid, dvec, svec in zip(point_ids, dense_vecs, sparse_vecs):
            update_points.append(
                models.PointVectors(
                    id=pid,
                    vector={
                        DENSE_VECTOR_NAME: dvec.tolist(),
                        SPARSE_VECTOR_NAME: models.SparseVector(
                            indices=svec.indices.tolist(),
                            values=svec.values.tolist(),
                        ),
                    }
                )
            )
        
        # Update vectors without touching payload
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
print(f"\nDone! Enriched {processed} points in {elapsed:.1f}s")
print(f"Failed/skipped: {failed}")
print(f"Rate: {processed/elapsed:.1f} pts/sec")
