# Incremental Ingestion Without Wiping Existing Knowledge

> **Domain:** Vector Brain Optimization
> **Research Date:** May 22, 2026
> **Purpose:** Technical guide for building an incremental ingestion pipeline that updates changed content, inserts new content, and preserves existing knowledge -- without ever wiping the vector database.

---

## 1. The Problem Statement

Most naive RAG ingestion pipelines follow a destructive pattern: drop all vectors, re-embed everything, re-insert. This approach has three critical flaws:

1. **Wasted compute** -- re-embedding unchanged documents burns API credits and time.
2. **Downtime window** -- during rebuild, the vector store is either empty or inconsistent.
3. **Lost metadata** -- any manually curated tags, corrections, or cross-references are destroyed.

The solution is **incremental ingestion**: a pipeline that detects what changed, processes only the delta, and leaves untouched content alone.

---

## 2. Upsert Patterns for Vector Databases

The **upsert** operation (update-or-insert) is the foundational primitive for incremental ingestion. When you upsert a vector:

- **If the ID exists:** The database overwrites the existing embedding and metadata.
- **If the ID does not exist:** The database inserts a new record.

### Key Implementation Rules

1. **Use deterministic IDs** -- never auto-generate UUIDs. Derive the chunk ID from `{source_id}_{chunk_position}` or `{source_id}_{content_hash}`.
2. **Batch upserts** -- most vector databases (Pinecone, Milvus, Qdrant) perform far better with batched operations (100-1000 vectors per call) than individual inserts.
3. **Avoid check-then-insert** -- upsert eliminates race conditions and reduces round-trips.

```python
# Deterministic ID generation pattern
import hashlib

def generate_chunk_id(source_path: str, chunk_index: int) -> str:
    """Position-based deterministic ID."""
    return f"{source_path}::chunk_{chunk_index:04d}"

def generate_content_id(source_path: str, chunk_text: str) -> str:
    """Content-hash-based deterministic ID."""
    content_hash = hashlib.sha256(chunk_text.encode()).hexdigest()[:12]
    return f"{source_path}::{content_hash}"
```

### Tradeoff: Position-Based vs Hash-Based IDs

| Strategy | Pros | Cons |
|----------|------|------|
| Position-based (`doc::chunk_003`) | Predictable, easy to enumerate and delete | Shifts when chunks are added/removed |
| Content-hash (`doc::a3f2b1c8`) | Stable across re-chunking if content unchanged | Cannot predict/enumerate IDs for deletion |
| Hybrid (`doc::section_name::hash`) | Combines structure stability with content awareness | More complex to implement |

---

## 3. Content Deduplication During Ingestion

A two-tier deduplication strategy prevents redundant embeddings:

### Tier 1: Hash-Based Deduplication (Pre-Embedding)

Before sending text to the embedding model, compute a content hash:

```python
import hashlib

class DeduplicationFilter:
    def __init__(self):
        self.seen_hashes = set()

    def is_duplicate(self, text: str) -> bool:
        # Normalize: strip whitespace, lowercase
        normalized = " ".join(text.lower().split())
        content_hash = hashlib.sha256(normalized.encode()).hexdigest()
        if content_hash in self.seen_hashes:
            return True
        self.seen_hashes.add(content_hash)
        return False
```

This catches exact duplicates and saves embedding API costs.

### Tier 2: Semantic Deduplication (Post-Embedding)

For near-duplicates (paraphrased content), use cosine similarity on embeddings:

- **Threshold:** Vectors with cosine similarity > 0.95 are likely semantic duplicates.
- **Tools:** SemHash library, NVIDIA NeMo Curator, or MinHash LSH for large-scale dedup.
- **Schedule:** Run periodically as a batch cleanup job rather than inline.

---

## 4. Detecting Changed vs Unchanged Files

The core of incremental ingestion is a **change detection layer** that classifies each source file:

### The Diff Workflow

```
SCAN sources --> COMPARE against record manager --> CLASSIFY
  |                                                    |
  v                                                    v
[file_a.md: hash=abc123]                        NEW --> chunk, embed, insert
[file_b.md: hash=def456]                        CHANGED --> delete old chunks, re-insert
[file_c.md: hash=ghi789]                        UNCHANGED --> skip
[file_d.md: missing from source]                DELETED --> remove from vector DB
```

### Implementation: Record Manager Table

```sql
CREATE TABLE IF NOT EXISTS ingestion_records (
    source_id     TEXT PRIMARY KEY,   -- file path or document URI
    content_hash  TEXT NOT NULL,       -- SHA-256 of file content
    chunk_count   INTEGER NOT NULL,    -- how many chunks were generated
    ingested_at   TEXT NOT NULL,       -- ISO timestamp
    embedding_model TEXT NOT NULL      -- model used (for drift detection)
);
```

On each ingestion run:

1. Compute `SHA-256(file_content)` for every source file.
2. Compare against `ingestion_records.content_hash`.
3. If hash differs or record missing: process and update the record.
4. If hash matches: skip entirely.
5. If record exists but file is gone: delete associated chunks and record.

---

## 5. Chunking Stability

Small edits should not cause all chunks to regenerate. The key strategies:

### Structure-Aware Chunking

Split on logical boundaries (headings, paragraphs, blank lines) rather than fixed character counts. When you edit paragraph 3, only that chunk changes -- sections 1, 2, 4, 5 remain identical.

```python
# Structure-aware splitting example
def split_by_headings(text: str) -> list[str]:
    """Split markdown by headings -- edits to one section leave others stable."""
    import re
    sections = re.split(r'\n(?=#{1,3}\s)', text)
    return [s.strip() for s in sections if s.strip()]
```

### Content-Defined Chunking (CDC)

Borrowed from backup systems (restic, Borg), CDC uses a rolling hash (Rabin fingerprint or Gear hash) to define chunk boundaries based on content patterns rather than fixed offsets. Benefits:

- **Insertion resilience:** Adding text in one section does not shift boundaries in other sections.
- **Only modified chunks change:** Unchanged regions produce identical chunks across versions.
- **Deterministic:** Same input always produces same chunks.

### Practical Recommendation

For most RAG systems, **heading-based splitting + overlap** provides the best stability/simplicity tradeoff. Reserve CDC for systems with very frequent, fine-grained edits.

---

## 6. Source Tracking Metadata

Every chunk stored in the vector database should carry rich metadata for lifecycle management:

```python
metadata = {
    "source_id": "docs/api-reference.md",      # unique source identifier
    "source_hash": "a3f2b1c8d4e5...",           # content hash at ingestion time
    "chunk_index": 3,                            # position within document
    "chunk_count": 12,                           # total chunks from this source
    "ingested_at": "2026-05-22T06:00:00Z",      # when this was ingested
    "embedding_model": "text-embedding-3-small", # model version
    "section_title": "Authentication",           # structural context
    "char_start": 1450,                          # character offset in source
    "char_end": 2100,
}
```

This enables:

- **Selective deletion:** `DELETE FROM vectors WHERE source_id = 'docs/api-reference.md'`
- **Model migration:** Re-embed only chunks from an older embedding model.
- **Audit trail:** Know exactly when and how each chunk entered the system.
- **Filtered search:** Restrict queries to specific sources or sections.

---

## 7. sqlite-vec Specific Operations

For systems using `sqlite-vec` (the SQLite vector extension), here are the critical patterns:

### Insert and Delete (No Native Upsert on vec0)

The `vec0` virtual table supports standard SQL `INSERT`, `UPDATE`, and `DELETE`, but the `ON CONFLICT` (UPSERT) clause may not work reliably. Use the **delete-then-insert** pattern:

```sql
-- Wrap in a transaction for atomicity
BEGIN TRANSACTION;

-- Remove old vector if it exists
DELETE FROM brain_vectors WHERE id = ?;

-- Insert updated vector
INSERT INTO brain_vectors (id, embedding, source_id, content)
VALUES (?, ?, ?, ?);

COMMIT;
```

### Storage and Compaction

- **DELETE behavior:** Deleting from `vec0` sets a validity bit but may not immediately reclaim storage. The database file can grow monotonically.
- **Reclaim space:** Run `VACUUM;` periodically to rebuild the database and reclaim freed pages.
- **Auto-vacuum:** Set `PRAGMA auto_vacuum = FULL;` before creating the database for automatic space reclamation (but note: this can cause fragmentation).
- **Shadow tables:** `vec0` stores data in shadow tables (e.g., `brain_vectors_vector_chunks00`). Ensure DELETE operations properly clean these.

### Best Practice: Companion Metadata Table

Since `vec0` is limited in metadata storage, maintain a companion table:

```sql
CREATE TABLE IF NOT EXISTS chunk_metadata (
    chunk_id       TEXT PRIMARY KEY,
    source_id      TEXT NOT NULL,
    content_hash   TEXT NOT NULL,
    chunk_index    INTEGER NOT NULL,
    content_text   TEXT NOT NULL,
    ingested_at    TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES ingestion_records(source_id)
);

CREATE INDEX idx_chunk_source ON chunk_metadata(source_id);
```

---

## 8. Versioned Knowledge Bases

For systems that need history (e.g., tracking how documentation evolved):

### Strategy 1: Version Metadata (Lightweight)

Add a `version` field to each chunk. On update, insert new version and mark old as inactive:

```sql
-- Mark old version as inactive
UPDATE chunk_metadata SET is_active = 0 WHERE source_id = ? AND is_active = 1;

-- Insert new version
INSERT INTO chunk_metadata (chunk_id, source_id, version, is_active, ...)
VALUES (?, ?, ?, 1, ...);
```

At query time, filter: `WHERE is_active = 1`.

### Strategy 2: Time-Based Partitioning

Create separate vector indices per time window (daily/weekly). Old partitions become read-only archives. This simplifies garbage collection: just drop the old partition.

### Strategy 3: Snapshot + Delta

Keep a full snapshot of the vector DB periodically. Between snapshots, only store deltas (new/changed chunks). This enables point-in-time recovery.

---

## 9. Garbage Collection for Stale Chunks

When source files are deleted or significantly changed, orphan chunks remain in the vector store. Garbage collection strategies:

### Approach 1: Source-Based Sweep

```python
def garbage_collect(db, current_source_ids: set):
    """Remove chunks whose source no longer exists."""
    stored_sources = db.execute(
        "SELECT DISTINCT source_id FROM chunk_metadata"
    ).fetchall()
    for (source_id,) in stored_sources:
        if source_id not in current_source_ids:
            # Source was deleted -- remove all its chunks
            chunk_ids = db.execute(
                "SELECT chunk_id FROM chunk_metadata WHERE source_id = ?",
                (source_id,)
            ).fetchall()
            for (chunk_id,) in chunk_ids:
                db.execute("DELETE FROM brain_vectors WHERE id = ?", (chunk_id,))
            db.execute("DELETE FROM chunk_metadata WHERE source_id = ?", (source_id,))
    db.execute("VACUUM")
```

### Approach 2: Timestamp-Based Expiry

Mark all chunks with an `ingested_at` timestamp. After each full ingestion run, delete chunks that were not refreshed (their timestamp is older than the run timestamp).

### Approach 3: Reference Counting

Track how many active references point to each chunk. When the count drops to zero, the chunk is eligible for collection.

---

## 10. Batch vs Streaming Ingestion

| Dimension | Batch | Streaming |
|-----------|-------|-----------|
| **Freshness** | Minutes to hours | Milliseconds to seconds |
| **Complexity** | Low -- simple scripts | High -- requires Kafka/CDC infrastructure |
| **Cost** | Lower -- off-peak processing | Higher -- always-on infrastructure |
| **Best for** | Document repos, nightly syncs | Real-time data, live dashboards |
| **Error handling** | Retry entire batch | Complex backpressure management |

### Recommendation for Keystone Brain

Use **batch ingestion** with incremental change detection. The document corpus changes infrequently enough that a "scan-diff-update" pattern run on-demand or nightly is optimal. Reserve streaming for future real-time data sources (e.g., live project feeds).

---

## 11. Framework Approaches: LlamaIndex and LangChain

### LlamaIndex IngestionPipeline

LlamaIndex provides built-in incremental ingestion via `DocstoreStrategy`:

```python
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.core.storage.docstore import SimpleDocumentStore

pipeline = IngestionPipeline(
    transformations=[splitter, embed_model],
    docstore=SimpleDocumentStore(),
    docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,
)

# First run: processes everything
nodes = pipeline.run(documents=docs)

# Second run: only processes new/changed docs
nodes = pipeline.run(documents=updated_docs)
```

**Key strategies:**
- `UPSERTS` -- Update changed, add new, keep old.
- `DUPLICATES_ONLY` -- Skip exact duplicates.
- `UPSERTS_AND_DELETE` -- Full sync: update, add, AND remove docs no longer in input.

### LangChain Indexing API

LangChain uses a **Record Manager** to track document [[STATE|state]]:

```python
from langchain.indexes import SQLRecordManager, index

record_manager = SQLRecordManager(
    namespace="keystone_brain",
    db_url="sqlite:///record_manager.db",
)
record_manager.create_schema()

# Incremental mode: updates changed, skips unchanged
result = index(
    docs_source=documents,
    record_manager=record_manager,
    vector_store=vectorstore,
    cleanup="incremental",  # or "full" for complete sync
)
print(result)
# {'num_added': 5, 'num_updated': 2, 'num_skipped': 43, 'num_deleted': 1}
```

**Cleanup modes:**
- `"incremental"` -- Deletes outdated versions as new ones are indexed.
- `"full"` -- Removes anything not in the current batch (full sync).
- `None` -- Only adds, never deletes.

---

## 12. Recommended Architecture for Keystone Brain

Based on all research, here is the recommended incremental ingestion architecture:

```
                    [Source Files]
                         |
                    [1. SCAN & HASH]
                         |
              +----------+----------+
              |          |          |
           [NEW]    [CHANGED]  [DELETED]
              |          |          |
        [2. CHUNK]  [3. DELETE   [5. DELETE
              |      OLD CHUNKS]  CHUNKS +
        [3. EMBED]       |        RECORD]
              |     [4. RE-CHUNK
        [4. UPSERT  + RE-EMBED
         + RECORD]  + UPSERT
              |      + RECORD]
              |          |
              +----+-----+
                   |
           [6. VACUUM if needed]
                   |
           [VECTOR DB READY]
```

### Implementation Checklist

1. **Record Manager table** in SQLite to track source_id, content_hash, chunk_count.
2. **Deterministic chunk IDs** using `{source_path}::chunk_{index}`.
3. **Structure-aware splitting** on headings/paragraphs for stability.
4. **Hash-based dedup filter** before embedding to save API costs.
5. **Delete-then-insert pattern** for sqlite-vec upserts (wrapped in transactions).
6. **Rich metadata** on every chunk (source_id, ingested_at, model version).
7. **Garbage collection sweep** to remove chunks from deleted sources.
8. **Periodic VACUUM** to reclaim storage after deletions.

---

## Sources Consulted

- Pinecone documentation on upsert operations
- Milvus documentation on update/delete behavior
- LlamaIndex IngestionPipeline and DocstoreStrategy docs
- LangChain Indexing API and Record Manager docs
- sqlite-vec GitHub repository and documentation (alexgarcia.xyz)
- SQLite VACUUM and auto_vacuum documentation (sqlite.org)
- Research papers on Content-Defined Chunking and Rabin fingerprinting
- SemHash library for semantic deduplication
- NVIDIA NeMo Curator documentation
- Streamkap, Confluent, and Unstructured.io on streaming vs batch ingestion
- Various community discussions on Reddit and Stack Overflow


---
📁 **See also:** ← Directory Index
