"""
Keystone Drive Bridge — Google Drive ↔ Clone Brain Sync
========================================================
Watches a local Google Drive folder for new .md and .json files
that Spark deposits. Ingests them into the Clone brain (port 7333)
ONLY — never touches the Main brain.

Also exports a brain_snapshot.json summary FROM the Clone brain
INTO the Drive folder so Spark can read current knowledge.

Setup:
  1. Install Google Drive for Desktop (stream or mirror mode)
  2. Create folder: G:/My Drive/Keystone_Spark_Bridge/
     (or wherever your Drive mounts — update DRIVE_BRIDGE_DIR below)
  3. Two subfolders:
     - spark_inbox/    ← Spark writes research here
     - brain_export/   ← This script writes brain summaries here

Usage: python drive_bridge.py           (one-time sync)
       python drive_bridge.py --watch   (continuous watcher)
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from qdrant_client import QdrantClient

# ============================================
# CONFIGURATION
# ============================================
DRIVE_BRIDGE_DIR = r"G:\My Drive\Keystone_Spark_Bridge"
# Fallback paths if Drive is mounted differently:
ALT_PATHS = [
    os.path.join(os.path.expanduser("~"), "Keystone_Spark_Bridge"),
    os.path.join(os.path.expanduser("~"), "Google Drive", "My Drive", "Keystone_Spark_Bridge"),
]

INBOX_DIR = None
EXPORT_DIR = None
PROCESSED_LOG = os.path.join(os.path.dirname(__file__), "drive_processed.json")

CLONE_URL = "http://localhost:7333"

# ============================================
# FIND DRIVE FOLDER
# ============================================
def find_drive_folder():
    global DRIVE_BRIDGE_DIR, INBOX_DIR, EXPORT_DIR
    
    candidates = [DRIVE_BRIDGE_DIR] + ALT_PATHS
    for path in candidates:
        if os.path.exists(os.path.dirname(path)):
            DRIVE_BRIDGE_DIR = path
            break
    
    INBOX_DIR = os.path.join(DRIVE_BRIDGE_DIR, "spark_inbox")
    EXPORT_DIR = os.path.join(DRIVE_BRIDGE_DIR, "brain_export")
    
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    print(f"Drive bridge directory: {DRIVE_BRIDGE_DIR}")
    print(f"  Inbox (Spark writes here):  {INBOX_DIR}")
    print(f"  Export (brain summaries):    {EXPORT_DIR}")


# ============================================
# TRACK PROCESSED FILES
# ============================================
def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG, "r") as f:
            return json.load(f)
    return {}


def save_processed(processed):
    with open(PROCESSED_LOG, "w") as f:
        json.dump(processed, f, indent=2)


def file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ============================================
# INGEST INTO CLONE BRAIN
# ============================================
def ingest_to_clone(filepath, client):
    """Read a file from the Drive inbox and ingest into Clone brain."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  [FAIL] Could not read {filepath}: {e}")
        return False
    
    if len(content.strip()) < 10:
        print(f"  ⊘ Skipping {os.path.basename(filepath)} (too short)")
        return False
    
    # Determine namespace from filename prefix
    # Convention: spark writes files like "protocol_research_bpc157.md"
    basename = os.path.basename(filepath).lower()
    namespace = "spark_inbox"  # default quarantine namespace
    
    for prefix in ["protocol", "possibilities", "music", "legal", "webmaster", "tax"]:
        if basename.startswith(prefix):
            namespace = f"spark_{prefix}"
            break
    
    # Chunk the content
    chunks = []
    chunk_size = 1000
    overlap = 200
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunks.append(content[start:end])
        start += chunk_size - overlap
    
    # Create collection if needed
    if not client.collection_exists(collection_name=namespace):
        client.create_collection(
            collection_name=namespace,
            vectors_config=client.get_fastembed_vector_params()
        )
    
    # Ingest
    metadata = [{"source": os.path.basename(filepath), "ingested_at": datetime.now().isoformat()} for _ in chunks]
    client.add(
        collection_name=namespace,
        documents=chunks,
        metadata=metadata
    )
    
    print(f"  [OK] Ingested {os.path.basename(filepath)} -> Clone '{namespace}' ({len(chunks)} chunks)")
    return True


# ============================================
# EXPORT BRAIN SUMMARY TO DRIVE
# ============================================
def export_brain_summary(client):
    """Write a summary of what's in the Clone brain so Spark can read it."""
    try:
        collections = client.get_collections()
        summary = {
            "exported_at": datetime.now().isoformat(),
            "brain": "Clone (DMZ Quarantine)",
            "namespaces": {}
        }
        
        for col in collections.collections:
            info = client.get_collection(col.name)
            summary["namespaces"][col.name] = {
                "vectors": info.points_count,
                "status": info.status.value if hasattr(info.status, 'value') else str(info.status)
            }
        
        export_path = os.path.join(EXPORT_DIR, "brain_snapshot.json")
        with open(export_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"  [OK] Brain snapshot exported to {export_path}")
    except Exception as e:
        print(f"  [FAIL] Export failed: {e}")


# ============================================
# MAIN SYNC LOOP
# ============================================
def sync_once(client):
    """Process all new files in the inbox."""
    processed = load_processed()
    new_files = 0
    
    if not os.path.exists(INBOX_DIR):
        print("  No inbox directory found.")
        return
    
    for fname in os.listdir(INBOX_DIR):
        if not (fname.endswith(".md") or fname.endswith(".json") or fname.endswith(".txt")):
            continue
        
        fpath = os.path.join(INBOX_DIR, fname)
        fhash = file_hash(fpath)
        
        if fname in processed and processed[fname] == fhash:
            continue  # Already processed, unchanged
        
        print(f"\n  New file detected: {fname}")
        if ingest_to_clone(fpath, client):
            processed[fname] = fhash
            new_files += 1
    
    save_processed(processed)
    
    if new_files > 0:
        print(f"\n  Ingested {new_files} new file(s) into Clone brain.")
        export_brain_summary(client)
    else:
        print("  No new files to process.")


def main():
    find_drive_folder()
    
    print("\nConnecting to Clone brain (port 7333)...")
    try:
        client = QdrantClient(url=CLONE_URL)
        client.set_model("BAAI/bge-small-en-v1.5")
        print("[OK] Clone brain connected.\n")
    except Exception as e:
        print(f"[FAIL] Clone brain OFFLINE: {e}")
        print("  Make sure the Clone Docker container is running.")
        return
    
    watch_mode = "--watch" in sys.argv
    
    if watch_mode:
        print("=" * 55)
        print("DRIVE BRIDGE — Continuous Watch Mode")
        print("Checking every 30 seconds for new Spark deposits...")
        print("Press Ctrl+C to stop.")
        print("=" * 55)
        
        while True:
            try:
                sync_once(client)
                time.sleep(30)
            except KeyboardInterrupt:
                print("\nWatcher stopped.")
                break
    else:
        print("=" * 55)
        print("DRIVE BRIDGE — One-Time Sync")
        print("=" * 55)
        sync_once(client)
        export_brain_summary(client)
        print("\nDone.")


if __name__ == "__main__":
    main()
