#!/usr/bin/env python3
"""
Post-rebuild verification: check collection health, namespace counts,
scroll integrity (the thing that was broken before), and search accuracy.
Also re-enables HNSW indexing after bulk load.
"""

import sys
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"

def main():
    client = QdrantClient(url="http://localhost:6333")
    
    print("=" * 60)
    print("POST-REBUILD VERIFICATION")
    print("=" * 60)
    
    # 1. Collection info
    info = client.get_collection(collection_name=COLLECTION)
    print(f"\n[1] Collection Info")
    print(f"    Points: {info.points_count}")
    print(f"    Status: {info.status}")
    print(f"    Segments: {info.segments_count}")
    print(f"    Indexed vectors: {info.indexed_vectors_count}")
    
    # 2. Namespace breakdown
    namespaces = ["possibilities", "music", "protocol_brand", "content_pipeline", "general", "local_seo", "webmaster"]
    print(f"\n[2] Namespace Breakdown")
    total = 0
    for ns in namespaces:
        try:
            res = client.count(
                collection_name=COLLECTION,
                count_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns)
                        )
                    ]
                )
            )
            print(f"    {ns}: {res.count} vectors")
            total += res.count
        except Exception as e:
            print(f"    {ns}: ERROR - {e}")
    print(f"    TOTAL: {total}")
    
    # 3. Scroll test on EVERY namespace (this is what was broken before)
    print(f"\n[3] Scroll Integrity Test (was broken before rebuild)")
    all_pass = True
    for ns in namespaces:
        try:
            res, next_offset = client.scroll(
                collection_name=COLLECTION,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns)
                        )
                    ]
                ),
                limit=50,
                with_payload=True,
                with_vectors=False
            )
            print(f"    {ns}: PASS (scrolled {len(res)} points)")
        except Exception as e:
            print(f"    {ns}: FAIL ({e})")
            all_pass = False
    
    if all_pass:
        print(f"    === ALL NAMESPACES SCROLL CLEANLY ===")
    else:
        print(f"    === SOME NAMESPACES STILL FAILING ===")
    
    # 4. Search test
    print(f"\n[4] Search Accuracy Test")
    embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    
    test_queries = [
        ("Bill 44 ADU construction permits", "possibilities"),
        ("GHK-Cu peptide protocol dosing", "protocol_brand"),
        ("YouTube thumbnail optimization", "content_pipeline"),
        ("Google Flow avatar character", "general"),
    ]
    
    for query, expected_ns in test_queries:
        query_vec = list(embed_model.embed([query]))[0].tolist()
        results = client.query_points(
            collection_name=COLLECTION,
            query=query_vec,
            using=VECTOR_NAME,
            limit=1,
            with_payload=True,
        )
        if results.points:
            p = results.points[0]
            score = p.score
            source = p.payload.get("source", "?")[:60]
            ns = p.payload.get("tenant_id", "?")
            print(f"    Query: '{query[:40]}...'")
            print(f"      Top result: score={score:.3f} ns={ns} src={source}")
        else:
            print(f"    Query: '{query[:40]}...' -> NO RESULTS")
    
    # 5. Re-enable HNSW indexing (was disabled for bulk load)
    print(f"\n[5] Re-enabling HNSW Indexing")
    client.update_collection(
        collection_name=COLLECTION,
        optimizer_config=models.OptimizersConfigDiff(
            indexing_threshold=10000,  # Default threshold
        ),
    )
    
    # Check indexed count after a moment
    import time
    time.sleep(2)
    info2 = client.get_collection(collection_name=COLLECTION)
    print(f"    Indexed vectors: {info2.indexed_vectors_count} / {info2.points_count}")
    print(f"    Optimizer status: {info2.optimizer_status}")
    
    # 6. Check recovered files exist
    from pathlib import Path
    recovered_dir = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\Recovered_From_Qdrant")
    recovered_files = list(recovered_dir.glob("*.md"))
    print(f"\n[6] Recovered Sources")
    print(f"    Files in Recovered_From_Qdrant/: {len(recovered_files)}")
    
    print(f"\n{'=' * 60}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
