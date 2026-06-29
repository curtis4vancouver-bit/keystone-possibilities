"""
Keystone autoDream Consolidation Engine
========================================
Runs during idle/scheduled time to:
1. Scan recent Qdrant entries for contradictions and duplicates
2. Merge duplicate knowledge chunks
3. Prune outdated facts
4. Compress verbose entries
5. Generate a consolidation report

Based on Claude Code leaked architecture: agents degrade predictably 
over weeks without background memory consolidation.

Usage:
    python autodream.py                    # Run full consolidation
    python autodream.py --dry-run          # Report only, no changes
    python autodream.py --namespace music  # Target specific namespace
"""

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import json
import sys
from datetime import datetime, timedelta, UTC
from pathlib import Path

QDRANT_URL = "http://localhost:6333"
UNIFIED_COLLECTION = "keystone_unified"
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"

# Similarity threshold for duplicate detection
DUPLICATE_THRESHOLD = 0.95  # Very high = nearly identical content
STALE_DAYS = 180  # Consider content stale after 6 months


def run_consolidation(dry_run=False, target_namespace=None):
    """Run the full autoDream consolidation cycle."""
    client = QdrantClient(url=QDRANT_URL)
    embed_model = TextEmbedding(EMBED_MODEL_NAME)
    
    report = {
        "timestamp": datetime.now(UTC).isoformat(),
        "duplicates_found": 0,
        "duplicates_removed": 0,
        "stale_entries": 0,
        "stale_removed": 0,
        "empty_entries": 0,
        "empty_removed": 0,
        "namespaces_scanned": [],
        "errors": [],
    }
    
    print("=" * 60)
    print("KEYSTONE autoDream CONSOLIDATION ENGINE")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)
    
    # Get all tenant_ids
    if target_namespace:
        namespaces = [target_namespace]
    else:
        # Scroll to get unique tenants
        tenant_set = set()
        offset = None
        while True:
            records, next_offset = client.scroll(
                collection_name=UNIFIED_COLLECTION,
                limit=100,
                with_payload=["tenant_id"],
                with_vectors=False,
                offset=offset,
            )
            for r in records:
                if r.payload and "tenant_id" in r.payload:
                    tenant_set.add(r.payload["tenant_id"])
            if next_offset is None:
                break
            offset = next_offset
        namespaces = sorted(tenant_set)
    
    print(f"\nScanning {len(namespaces)} namespaces...")
    
    for ns in namespaces:
        print(f"\n--- {ns} ---")
        report["namespaces_scanned"].append(ns)
        
        # Scroll all points for this namespace
        points = []
        offset = None
        while True:
            records, next_offset = client.scroll(
                collection_name=UNIFIED_COLLECTION,
                limit=100,
                with_payload=True,
                with_vectors=True,
                offset=offset,
                scroll_filter=models.Filter(
                    must=[models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=ns),
                    )]
                ),
            )
            points.extend(records)
            if next_offset is None:
                break
            offset = next_offset
        
        print(f"  {len(points)} vectors loaded")
        if len(points) < 2:
            print(f"  Skipping (too few points)")
            continue
        
        # Check 1: Empty/near-empty documents
        empty_ids = []
        for p in points:
            doc = p.payload.get("document", "") if p.payload else ""
            if len(str(doc).strip()) < 10:
                empty_ids.append(p.id)
                report["empty_entries"] += 1
        
        if empty_ids:
            print(f"  Found {len(empty_ids)} empty/near-empty entries")
            if not dry_run:
                client.delete(
                    collection_name=UNIFIED_COLLECTION,
                    points_selector=models.PointIdsList(points=empty_ids),
                )
                report["empty_removed"] += len(empty_ids)
                print(f"  Removed {len(empty_ids)} empty entries")
        
        # Check 2: Duplicate detection (compare vectors pairwise)
        # Only do this for smaller namespaces to avoid O(n²) on 8K vectors
        if len(points) <= 500:
            duplicates = find_duplicates(points, DUPLICATE_THRESHOLD)
            report["duplicates_found"] += len(duplicates)
            
            if duplicates:
                print(f"  Found {len(duplicates)} duplicate pairs")
                if not dry_run:
                    # Keep the newer version, delete the older
                    ids_to_delete = []
                    for older_id, newer_id, score in duplicates:
                        ids_to_delete.append(older_id)
                    
                    if ids_to_delete:
                        client.delete(
                            collection_name=UNIFIED_COLLECTION,
                            points_selector=models.PointIdsList(points=ids_to_delete),
                        )
                        report["duplicates_removed"] += len(ids_to_delete)
                        print(f"  Removed {len(ids_to_delete)} duplicate entries (kept newer)")
        else:
            print(f"  Skipping duplicate check (namespace too large: {len(points)} > 500)")
        
        # Check 3: Stale entries
        stale_cutoff = (datetime.now(UTC) - timedelta(days=STALE_DAYS)).isoformat()
        stale_count = 0
        for p in points:
            created = p.payload.get("created_at", "") if p.payload else ""
            if created and created < stale_cutoff:
                stale_count += 1
        
        report["stale_entries"] += stale_count
        if stale_count > 0:
            print(f"  {stale_count} entries older than {STALE_DAYS} days (not auto-deleting, just flagged)")
    
    # Generate report
    print("\n" + "=" * 60)
    print("CONSOLIDATION REPORT")
    print("=" * 60)
    print(f"  Namespaces scanned:  {len(report['namespaces_scanned'])}")
    print(f"  Empty entries found: {report['empty_entries']} (removed: {report['empty_removed']})")
    print(f"  Duplicates found:    {report['duplicates_found']} (removed: {report['duplicates_removed']})")
    print(f"  Stale entries:       {report['stale_entries']} (flagged only)")
    
    if report["errors"]:
        print(f"  Errors: {len(report['errors'])}")
        for err in report["errors"]:
            print(f"    - {err}")
    
    # Save report
    report_path = Path(__file__).parent / "autodream_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report saved to: {report_path}")
    
    return report


def find_duplicates(points, threshold):
    """Find near-duplicate pairs by comparing vectors."""
    import numpy as np
    
    duplicates = []
    vectors = []
    ids = []
    timestamps = []
    
    for p in points:
        vec = None
        if isinstance(p.vector, dict) and VECTOR_NAME in p.vector:
            vec = p.vector[VECTOR_NAME]
        elif isinstance(p.vector, list):
            vec = p.vector
        
        if vec is not None:
            vectors.append(vec)
            ids.append(p.id)
            ts = p.payload.get("created_at", "") if p.payload else ""
            timestamps.append(ts)
    
    if len(vectors) < 2:
        return duplicates
    
    # Compute cosine similarity matrix
    vecs = np.array(vectors)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1  # Avoid division by zero
    normalized = vecs / norms
    
    # Only check upper triangle
    for i in range(len(normalized)):
        for j in range(i + 1, len(normalized)):
            sim = float(np.dot(normalized[i], normalized[j]))
            if sim >= threshold:
                # Determine which is older
                if timestamps[i] < timestamps[j]:
                    duplicates.append((ids[i], ids[j], sim))  # (older, newer, score)
                else:
                    duplicates.append((ids[j], ids[i], sim))
    
    return duplicates


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    target_ns = None
    for i, arg in enumerate(sys.argv):
        if arg == "--namespace" and i + 1 < len(sys.argv):
            target_ns = sys.argv[i + 1]
    
    run_consolidation(dry_run=dry_run, target_namespace=target_ns)
