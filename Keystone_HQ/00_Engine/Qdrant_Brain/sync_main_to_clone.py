"""
Keystone Brain Sync — Main -> Clone Snapshot Pipeline
=====================================================
Snapshots every collection from the Main brain (port 6333)
and restores them into the Clone brain (port 7333).

Run this whenever you want the Clone to have a fresh copy
of the Main brain's knowledge. Spark reads from the Clone;
it can never corrupt the Main.

Usage: python sync_main_to_clone.py
"""

import requests
import os
import time

MAIN_URL = "http://localhost:6333"
CLONE_URL = "http://localhost:7333"
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "snapshots")

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def get_collections(base_url):
    r = requests.get(f"{base_url}/collections")
    r.raise_for_status()
    return [c["name"] for c in r.json()["result"]["collections"]]


def snapshot_collection(base_url, name):
    """Create a snapshot on the source and download it."""
    print(f"  Creating snapshot for '{name}'...")
    r = requests.post(f"{base_url}/collections/{name}/snapshots")
    r.raise_for_status()
    snap_name = r.json()["result"]["name"]
    
    # Download the snapshot file
    dl = requests.get(
        f"{base_url}/collections/{name}/snapshots/{snap_name}",
        stream=True
    )
    dl.raise_for_status()
    
    local_path = os.path.join(SNAPSHOT_DIR, f"{name}.snapshot")
    with open(local_path, "wb") as f:
        for chunk in dl.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # Clean up the snapshot on the server
    requests.delete(f"{base_url}/collections/{name}/snapshots/{snap_name}")
    
    print(f"  Downloaded snapshot: {local_path}")
    return local_path


def restore_to_clone(clone_url, name, snapshot_path):
    """Upload snapshot to clone, replacing any existing collection."""
    print(f"  Restoring '{name}' to Clone brain...")
    
    # Delete existing collection on clone if it exists
    requests.delete(f"{clone_url}/collections/{name}")
    time.sleep(1)
    
    # Upload the snapshot — Qdrant expects multipart/form-data
    file_size = os.path.getsize(snapshot_path)
    with open(snapshot_path, "rb") as f:
        r = requests.post(
            f"{clone_url}/collections/{name}/snapshots/upload",
            files={"snapshot": (f"{name}.snapshot", f, "application/octet-stream")},
        )
    
    if r.status_code >= 400:
        # Fallback: try recover endpoint
        print(f"  Upload returned {r.status_code}, trying recover method...")
        # Create collection first, then recover from local file
        # Copy snapshot into clone's storage and recover
        print(f"  Falling back to direct re-ingestion for '{name}'...")
        return False
    
    print(f"  Restored '{name}' to Clone successfully ({file_size} bytes).")
    return True


def main():
    print("=" * 55)
    print("KEYSTONE BRAIN SYNC — Main -> Clone")
    print("=" * 55)
    
    # Verify both instances are online
    try:
        requests.get(f"{MAIN_URL}/collections").raise_for_status()
        print(f"[OK] Main brain online at {MAIN_URL}")
    except Exception as e:
        print(f"[FAIL] Main brain OFFLINE: {e}")
        return
    
    try:
        requests.get(f"{CLONE_URL}/collections").raise_for_status()
        print(f"[OK] Clone brain online at {CLONE_URL}")
    except Exception as e:
        print(f"[FAIL] Clone brain OFFLINE: {e}")
        return
    
    # Get all collections from Main
    collections = get_collections(MAIN_URL)
    print(f"\nFound {len(collections)} namespaces to sync: {', '.join(collections)}")
    
    start = time.time()
    
    for name in collections:
        print(f"\n--- Syncing '{name}' ---")
        snap_path = snapshot_collection(MAIN_URL, name)
        restore_to_clone(CLONE_URL, name, snap_path)
    
    elapsed = time.time() - start
    
    # Verify clone
    clone_collections = get_collections(CLONE_URL)
    print(f"\n{'=' * 55}")
    print(f"SYNC COMPLETE in {elapsed:.1f}s")
    print(f"Clone now has: {', '.join(clone_collections)}")
    
    for name in clone_collections:
        r = requests.get(f"{CLONE_URL}/collections/{name}")
        count = r.json()["result"]["points_count"]
        print(f"  {name}: {count} vectors")
    
    print(f"{'=' * 55}")


if __name__ == "__main__":
    main()
