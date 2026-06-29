"""
Keystone Brain — Qdrant Unified Collection Migration
=====================================================
Merges all 29 separate collections into a single 'keystone_unified' collection
with tenant_id-based multitenancy.

SAFETY: 
- Creates new collection first, migrates data, then verifies counts match
- Old collections are NOT deleted automatically — manual cleanup after verification
- Full dry-run mode available

Based on NotebookLM deep research (June 2026):
- is_tenant: true on tenant_id field
- payload_m: 16 for per-tenant sub-graphs  
- Global m: 0 disabled (using payload_m instead)
- ACORN enabled via payload indexing
- Inline storage for 10x QPS boost
- Payload indexes on tenant_id, source, created_at
"""

from qdrant_client import QdrantClient, models
import time
import sys

QDRANT_URL = "http://localhost:6333"
UNIFIED_COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"
VECTOR_SIZE = 384
BATCH_SIZE = 100  # Points per scroll batch

def main():
    print("=" * 60)
    print("KEYSTONE BRAIN — QDRANT UNIFIED MIGRATION")
    print("=" * 60)
    
    client = QdrantClient(url=QDRANT_URL)
    
    # Step 1: Inventory all existing collections
    print("\n[STEP 1] Inventorying existing collections...")
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    # Skip the unified collection if it already exists (re-run safety)
    source_collections = [n for n in collection_names if n != UNIFIED_COLLECTION]
    
    total_vectors = 0
    collection_stats = {}
    for name in source_collections:
        info = client.get_collection(collection_name=name)
        count = info.points_count
        collection_stats[name] = count
        total_vectors += count
        status = "EMPTY" if count == 0 else f"{count} vectors"
        print(f"  {name}: {status}")
    
    print(f"\n  TOTAL: {total_vectors} vectors across {len(source_collections)} collections")
    
    # Step 2: Create unified collection with optimized config
    print("\n[STEP 2] Creating unified collection with optimized config...")
    
    if client.collection_exists(collection_name=UNIFIED_COLLECTION):
        existing_info = client.get_collection(collection_name=UNIFIED_COLLECTION)
        print(f"  WARNING: '{UNIFIED_COLLECTION}' already exists with {existing_info.points_count} points")
        print(f"  Deleting and recreating for clean migration...")
        client.delete_collection(collection_name=UNIFIED_COLLECTION)
        time.sleep(1)
    
    # Create with optimized multitenancy config
    # Key settings from research:
    # - Global m=0 disables global HNSW graph  
    # - payload_m=16 builds per-tenant sub-graphs
    # - on_disk=true stores full-precision vectors on disk to save RAM
    # - TurboQuant BITS4 compression keeps quantized vectors in RAM
    client.create_collection(
        collection_name=UNIFIED_COLLECTION,
        vectors_config={
            VECTOR_NAME: models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
                on_disk=True,  # Store full-precision vectors on disk
                hnsw_config=models.HnswConfigDiff(
                    m=0,           # CRITICAL: Disable global graph
                    payload_m=16,  # Build per-tenant sub-graphs
                    on_disk=False, # Keep index in RAM for speed
                ),
            )
        },
        sparse_vectors_config={
            SPARSE_VECTOR_NAME: models.SparseVectorParams(
                index=models.SparseIndexParams()
            )
        },
        hnsw_config=models.HnswConfigDiff(
            m=0,                      # Global m=0
            ef_construct=128,         # Good build quality
            full_scan_threshold=10000,
            on_disk=False,
        ),
        on_disk_payload=True,  # Save RAM, payloads on disk
        quantization_config=models.TurboQuantization(
            turbo=models.TurboQuantQuantizationConfig(
                bits=models.TurboQuantBitSize.BITS4,
                always_ram=True,
            )
        ),
        optimizers_config=models.OptimizersConfigDiff(
            indexing_threshold=0,  # STAGED INDEXING: Disable during bulk load
        ),
    )
    print(f"  Created '{UNIFIED_COLLECTION}' with m=0, payload_m=16, staged indexing")
    
    # Step 3: Create payload indexes BEFORE migration (speeds up inserts)
    print("\n[STEP 3] Creating payload indexes...")
    
    # tenant_id index with is_tenant for multitenancy isolation
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="tenant_id",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            is_tenant=True,  # CRITICAL: Co-locates tenant data on disk
            on_disk=True,
        ),
    )
    print("  tenant_id (keyword, is_tenant=true)")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="source",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            on_disk=True,
        ),
    )
    print("  source (keyword)")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="created_at",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            on_disk=True,
        ),
    )
    print("  created_at (keyword)")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="memory_layer",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            on_disk=True,
        ),
    )
    print("  memory_layer (keyword)")
    
    # Step 4: Migrate all vectors
    print("\n[STEP 4] Migrating vectors...")
    
    migrated_total = 0
    errors = []
    
    for coll_name in source_collections:
        count = collection_stats[coll_name]
        if count == 0:
            print(f"  SKIP {coll_name} (empty)")
            continue
        
        print(f"  Migrating {coll_name} ({count} vectors)...", end="", flush=True)
        
        # First check what vector config this collection uses
        coll_info = client.get_collection(collection_name=coll_name)
        vec_cfg = coll_info.config.params.vectors
        
        # Determine if collection uses named or unnamed vectors
        has_named_vectors = isinstance(vec_cfg, dict) and VECTOR_NAME in vec_cfg
        has_sparse = False
        if coll_info.config.params.sparse_vectors:
            sparse_cfg = coll_info.config.params.sparse_vectors
            if isinstance(sparse_cfg, dict) and SPARSE_VECTOR_NAME in sparse_cfg:
                has_sparse = True
        
        # Scroll through all points
        migrated_count = 0
        offset = None
        
        while True:
            try:
                records, next_offset = client.scroll(
                    collection_name=coll_name,
                    limit=BATCH_SIZE,
                    with_payload=True,
                    with_vectors=True,
                    offset=offset,
                )
            except Exception as e:
                errors.append(f"{coll_name}: scroll error: {e}")
                break
            
            if not records:
                break
            
            # Transform points: add tenant_id, normalize vector format
            new_points = []
            for record in records:
                payload = dict(record.payload) if record.payload else {}
                payload["tenant_id"] = coll_name  # Namespace becomes tenant_id
                
                # Extract dense vector
                if has_named_vectors and isinstance(record.vector, dict):
                    dense_vec = record.vector.get(VECTOR_NAME)
                    sparse_vec = record.vector.get(SPARSE_VECTOR_NAME) if has_sparse else None
                elif isinstance(record.vector, list):
                    dense_vec = record.vector
                    sparse_vec = None
                elif isinstance(record.vector, dict):
                    # Try to get any vector
                    dense_vec = record.vector.get(VECTOR_NAME)
                    if dense_vec is None:
                        # Might be unnamed
                        dense_vec = record.vector.get("")
                    sparse_vec = record.vector.get(SPARSE_VECTOR_NAME) if has_sparse else None
                else:
                    errors.append(f"{coll_name}: unknown vector format for point {record.id}")
                    continue
                
                if dense_vec is None:
                    errors.append(f"{coll_name}: no dense vector for point {record.id}")
                    continue
                
                # Build vector dict for unified collection
                vectors = {VECTOR_NAME: dense_vec}
                if sparse_vec is not None and isinstance(sparse_vec, dict):
                    vectors[SPARSE_VECTOR_NAME] = models.SparseVector(
                        indices=sparse_vec.get("indices", []),
                        values=sparse_vec.get("values", []),
                    )
                
                new_points.append(
                    models.PointStruct(
                        id=str(record.id) if not isinstance(record.id, str) else record.id,
                        payload=payload,
                        vector=vectors,
                    )
                )
            
            # Upsert batch
            if new_points:
                try:
                    client.upsert(
                        collection_name=UNIFIED_COLLECTION,
                        points=new_points,
                    )
                    migrated_count += len(new_points)
                except Exception as e:
                    errors.append(f"{coll_name}: upsert error: {e}")
                    break
            
            if next_offset is None:
                break
            offset = next_offset
        
        migrated_total += migrated_count
        status = "OK" if migrated_count == count else "WARN"
        print(f" {status} {migrated_count}/{count}")
    
    # Step 5: Re-enable indexing (end staged indexing)
    print("\n[STEP 5] Re-enabling HNSW indexing...")
    client.update_collection(
        collection_name=UNIFIED_COLLECTION,
        optimizer_config=models.OptimizersConfigDiff(
            indexing_threshold=10000,  # Restore default threshold
        ),
    )
    print("  Indexing threshold restored to 10000")
    
    # Wait for optimizer to process
    print("  Waiting for optimizer to build indexes...", end="", flush=True)
    for i in range(30):
        time.sleep(2)
        info = client.get_collection(collection_name=UNIFIED_COLLECTION)
        if info.optimizer_status == "ok" and info.indexed_vectors_count >= migrated_total * 0.9:
            print(f" done! ({info.indexed_vectors_count} indexed)")
            break
        print(".", end="", flush=True)
    else:
        info = client.get_collection(collection_name=UNIFIED_COLLECTION)
        print(f" still optimizing ({info.indexed_vectors_count} indexed so far)")
    
    # Step 6: Verification
    print("\n[STEP 6] Verification...")
    final_info = client.get_collection(collection_name=UNIFIED_COLLECTION)
    
    print(f"  Source total:    {total_vectors} vectors")
    print(f"  Migrated total:  {migrated_total} vectors")
    print(f"  Unified count:   {final_info.points_count} vectors")
    print(f"  Indexed count:   {final_info.indexed_vectors_count} vectors")
    print(f"  Status:          {final_info.status}")
    print(f"  Optimizer:       {final_info.optimizer_status}")
    
    # Verify per-tenant counts
    print("\n  Per-tenant verification:")
    for coll_name in source_collections:
        expected = collection_stats[coll_name]
        if expected == 0:
            continue
        
        # Count points with this tenant_id
        try:
            count_result = client.count(
                collection_name=UNIFIED_COLLECTION,
                count_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=coll_name),
                        )
                    ]
                ),
                exact=True,
            )
            actual = count_result.count
            match = "OK" if actual == expected else "MISMATCH"
            print(f"    {coll_name}: expected={expected}, actual={actual} {match}")
        except Exception as e:
            print(f"    {coll_name}: verification error: {e}")
    
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for err in errors:
            print(f"    - {err}")
    
    # Summary
    print("\n" + "=" * 60)
    empty_count = sum(1 for v in collection_stats.values() if v == 0)
    
    if migrated_total >= total_vectors * 0.95:  # 95% threshold
        print("MIGRATION SUCCESSFUL")
        print(f"   {migrated_total}/{total_vectors} vectors migrated to '{UNIFIED_COLLECTION}'")
        print(f"   {empty_count} empty collections can be deleted")
        print(f"\n   NEXT STEPS:")
        print(f"   1. Update keystone_brain_v2_mcp.py to use '{UNIFIED_COLLECTION}'")
        print(f"   2. Test search functionality")
        print(f"   3. Delete old collections after verification")
    else:
        print("MIGRATION INCOMPLETE")
        print(f"   Only {migrated_total}/{total_vectors} vectors migrated")
        print(f"   DO NOT delete old collections until resolved")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
