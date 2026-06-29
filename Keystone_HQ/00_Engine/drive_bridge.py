"""
Keystone Drive Bridge v1.0
Syncs Spark research output from Google Drive to Qdrant Brain.

Watches: G:/My Drive/Keystone_Spark_Bridge/spark_inbox/
Processes: .txt, .md, .json files
Namespace routing: filename prefix determines Qdrant namespace
  - possibilities_*.txt → possibilities
  - protocol_*.txt → protocol
  - webmaster_*.txt → webmaster
  - general_*.txt → general (default)
  - music_*.txt → music

After ingestion, files move to spark_inbox/processed/

Usage:
  python drive_bridge.py              # One-shot: process all pending files
  python drive_bridge.py --watch      # Continuous polling (30s interval)
  python drive_bridge.py --status     # Show inbox status
"""

import os
import sys
import json
import time
import shutil
import uuid
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# ── Configuration ──────────────────────────────────────────────
SPARK_INBOX = Path("G:/My Drive/Keystone_Spark_Bridge/spark_inbox")
PROCESSED_DIR = SPARK_INBOX / "processed"
SUPPORTED_EXTS = {".txt", ".md", ".json"}
POLL_INTERVAL = 30  # seconds

# Namespace routing by filename prefix
NAMESPACE_MAP = {
    "possibilities_": "possibilities",
    "protocol_": "protocol_brand",
    "webmaster_": "webmaster",
    "music_": "music",
    "general_": "general",
    "leads_": "possibilities",
    "seo_": "local_seo",
}
DEFAULT_NAMESPACE = "general"

# Qdrant connection
QDRANT_URL = "http://localhost:6333"
UNIFIED_COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"

# ── Qdrant Ingestion ──────────────────────────────────────────
def ingest_to_qdrant(content: str, source_id: str, namespace: str) -> dict:
    """Ingest content into the Qdrant unified collection under the proper tenant mapping."""
    try:
        from qdrant_client import QdrantClient, models
        from fastembed import TextEmbedding
        
        client = QdrantClient(url=QDRANT_URL)
        embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
        
        # Verify collection exists
        if not client.collection_exists(collection_name=UNIFIED_COLLECTION):
            return {"status": "error", "error": f"Unified collection '{UNIFIED_COLLECTION}' does not exist."}

        # Markdown-aware chunking
        chunks = []
        current_chunk = []
        current_size = 0
        for line in content.split('\n'):
            if line.startswith('#') and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            elif current_size + len(line) > 1500 and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            else:
                current_chunk.append(line)
                current_size += len(line)
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        chunks = [c.strip() for c in chunks if c.strip()]
        if not chunks:
            return {"status": "skipped", "reason": "no valid chunks after filtering"}

        # Generate embeddings
        embeddings = list(embed_model.embed(chunks))
        
        now_iso = datetime.utcnow().isoformat() + "Z"
        points = []
        
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Deterministic UUID: same source_id + chunk_index = same point_id
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{source_id}:{idx}"))
            vec = embedding.tolist()
            
            payload = {
                "tenant_id": namespace,         # Multi-tenancy tenant key
                "source": source_id,            # Attributed source
                "chunk_index": idx,
                "created_at": now_iso,
                "document": chunk,              # Text content field
                "type": "spark_note",
                "filename": f"{source_id}.txt",
                "topic": source_id.replace("spark_", "").replace("_", " ").replace("-", " ")
            }
            
            points.append(
                models.PointStruct(
                    id=point_id,
                    payload=payload,
                    vector={VECTOR_NAME: vec}
                )
            )
            
        client.upsert(collection_name=UNIFIED_COLLECTION, points=points)

        return {"status": "ok", "chunks": len(chunks), "namespace": namespace}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def detect_namespace(filename: str) -> str:
    """Detect Qdrant namespace from filename prefix."""
    lower = filename.lower()
    for prefix, ns in NAMESPACE_MAP.items():
        if lower.startswith(prefix):
            return ns
    return DEFAULT_NAMESPACE


def process_file(filepath: Path) -> dict:
    """Process a single file from the inbox."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            return {"file": filepath.name, "status": "skipped", "reason": "empty"}

        namespace = detect_namespace(filepath.name)
        source_id = f"spark_{filepath.stem}"

        result = ingest_to_qdrant(content, source_id, namespace)

        if result["status"] == "ok":
            # Move to processed
            PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            dest = PROCESSED_DIR / filepath.name
            if dest.exists():
                dest = PROCESSED_DIR / f"{filepath.stem}_{int(time.time())}{filepath.suffix}"
            shutil.move(str(filepath), str(dest))

        return {
            "file": filepath.name,
            "namespace": namespace,
            **result
        }
    except Exception as e:
        return {"file": filepath.name, "status": "error", "error": str(e)}


def get_pending_files() -> list:
    """Get all unprocessed files in the inbox."""
    if not SPARK_INBOX.exists():
        return []
    return [
        f for f in SPARK_INBOX.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
    ]


def process_all() -> list:
    """Process all pending files in the inbox."""
    files = get_pending_files()
    if not files:
        print("No pending files in spark_inbox/")
        return []

    results = []
    for f in files:
        print(f"Processing: {f.name}...")
        result = process_file(f)
        results.append(result)
        if result.get("status") == "ok":
            print(f"  [OK] Ingested {result['chunks']} chunks -> {result['namespace']}")
        else:
            print(f"  [FAIL] {result.get('error', result.get('reason', 'unknown'))}")

    return results


def show_status():
    """Show inbox status."""
    if not SPARK_INBOX.exists():
        print(f"Inbox directory does not exist: {SPARK_INBOX}")
        print("Create it or verify Google Drive sync is running.")
        return

    pending = get_pending_files()
    processed = list((PROCESSED_DIR).glob("*")) if PROCESSED_DIR.exists() else []

    print(f"Spark Drive Bridge Status")
    print(f"{'-' * 40}")
    print(f"Inbox:     {SPARK_INBOX}")
    print(f"Pending:   {len(pending)} files")
    print(f"Processed: {len(processed)} files")

    if pending:
        print(f"\nPending files:")
        for f in pending:
            ns = detect_namespace(f.name)
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB) -> {ns}")


def watch_loop():
    """Continuous polling loop."""
    print(f"Drive Bridge watching: {SPARK_INBOX}")
    print(f"Poll interval: {POLL_INTERVAL}s")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            results = process_all()
            if results:
                ok = sum(1 for r in results if r.get("status") == "ok")
                err = sum(1 for r in results if r.get("status") == "error")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch: {ok} ingested, {err} errors")
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--status" in args:
        show_status()
    elif "--watch" in args:
        watch_loop()
    else:
        results = process_all()
        if results:
            ok = sum(1 for r in results if r.get("status") == "ok")
            err = sum(1 for r in results if r.get("status") == "error")
            print(f"\nDone: {ok} ingested, {err} errors")
