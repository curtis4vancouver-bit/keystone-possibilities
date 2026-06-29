#!/usr/bin/env python3
"""
Step 2: Wipe corrupted keystone_unified and recreate with clean schema.
Exact same schema as migrate_to_unified.py — m=0, payload_m=16, ACORN multitenancy.
"""

import sys
import time
from qdrant_client import QdrantClient, models

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

QDRANT_URL = "http://localhost:6333"
UNIFIED_COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"
VECTOR_SIZE = 384


def main():
    print("=" * 60)
    print("STEP 2: WIPE & RECREATE KEYSTONE_UNIFIED")
    print("=" * 60)
    
    client = QdrantClient(url=QDRANT_URL)
    
    # Verify current state
    info = client.get_collection(collection_name=UNIFIED_COLLECTION)
    print(f"\n  Current state: {info.points_count} points, status={info.status}")
    
    # Delete
    print(f"\n  Deleting '{UNIFIED_COLLECTION}'...")
    client.delete_collection(collection_name=UNIFIED_COLLECTION)
    time.sleep(2)
    print(f"  Deleted.")
    
    # Recreate with optimized multitenancy config
    print(f"\n  Recreating '{UNIFIED_COLLECTION}' with clean schema...")
    client.create_collection(
        collection_name=UNIFIED_COLLECTION,
        vectors_config={
            VECTOR_NAME: models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
                on_disk=False,
                hnsw_config=models.HnswConfigDiff(
                    m=0,           # Disable global graph
                    payload_m=16,  # Per-tenant sub-graphs
                    on_disk=False,
                ),
            )
        },
        sparse_vectors_config={
            SPARSE_VECTOR_NAME: models.SparseVectorParams(
                index=models.SparseIndexParams()
            )
        },
        hnsw_config=models.HnswConfigDiff(
            m=0,
            ef_construct=128,
            full_scan_threshold=10000,
            on_disk=False,
        ),
        on_disk_payload=True,
        optimizers_config=models.OptimizersConfigDiff(
            indexing_threshold=0,  # Disable indexing during bulk load
        ),
    )
    print(f"  Created with m=0, payload_m=16, staged indexing.")
    
    # Create payload indexes
    print(f"\n  Creating payload indexes...")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="tenant_id",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            is_tenant=True,
            on_disk=True,
        ),
    )
    print(f"    tenant_id (keyword, is_tenant=true)")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="source",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            on_disk=True,
        ),
    )
    print(f"    source (keyword)")
    
    client.create_payload_index(
        collection_name=UNIFIED_COLLECTION,
        field_name="created_at",
        field_schema=models.KeywordIndexParams(
            type=models.KeywordIndexType.KEYWORD,
            on_disk=True,
        ),
    )
    print(f"    created_at (keyword)")
    
    # Verify
    info = client.get_collection(collection_name=UNIFIED_COLLECTION)
    print(f"\n  Verified: {info.points_count} points, status={info.status}")
    
    print(f"\n{'=' * 60}")
    print(f"STEP 2 COMPLETE — Clean empty collection ready for ingestion")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
