# Architecting High-Speed Local Memory for Autonomous [[AGENTS|Agents]]
## A Hybrid FTS5 and SQLite Vector Search Workflow

### Introduction: The Imperative for Local-First Agentic Memory Architectures
The rapid proliferation of autonomous AI [[AGENTS|agents]] relies on the Observe-Orient-Decide-Act (OODA) loop, which requires instantaneous retrieval of episodic and semantic memories. Cloud-native distributed vector databases (Milvus, Pinecone) introduce network latency overheads that bottleneck this cognitive loop and cost $89-$114 monthly. 

To achieve sub-10ms retrieval speeds, the memory [[ARCHITECTURE|architecture]] must be physically co-located. SQLite provides ACID-compliant durability and file-based portability. Hybrid Search fuses traditional lexical keyword matching (BM25) with high-dimensional semantic vector similarity, creating the most robust retrieval mechanism.

### The Evolution of Local Vector Search
- **sqlite-vss (Legacy):** Exposed Faiss C++ API through SQLite's virtual tables. Suffered from dependency bloat (3-5MB files), RAM memory leaks, and massive write amplification unsuited for OLTP (continuous agent observation appending).
- **sqlite-vec (Modern):** Written in pure C, devoid of Faiss. Operates natively within SQLite B-trees using shadow tables, allowing chunk-by-chunk on-disk reads. Drastically reduces write amplification. Supports 8-bit integer (int8) and binary quantization for extreme speed via brute-force linear scanning.

### The Lexical Engine: FTS5 and Okapi BM25
While vector search finds conceptual similarity, SQLite's built-in FTS5 handles exact keyword retrieval (e.g., API keys, timestamps). 
- **BM25 Algorithm:** Computes relevance via Term Frequency (TF) and Inverse Document Frequency (IDF). 
- **Polarity Quirk:** SQLite's FTS5 multiplies BM25 scores by -1. A score of -15.4 is vastly superior to -2.1.
- **Trigram Tokenization:** Breaks text into 3-character groups for language-agnostic matching and typo resilience.

### Mathematical Synthesis: Reciprocal Rank Fusion (RRF)
Vector engines produce Cosine Distance (0.0 to 2.0, lower is better). Lexical engines produce BM25 scores (negative float, lower is better). These cannot be linearly averaged.
- **RRF Solution:** Evaluates the relative ordinal rank (position) of a document in both lists and merges them mathematically using a smoothing constant (k=60).
- **SQL Execution:** Performing RRF via Python loops introduces micro-latencies. True sub-10ms performance requires pushing RRF deep into the SQLite C engine using Common Table Expressions (CTEs) and a FULL OUTER JOIN.

### Database Internal Tuning (Sub-10ms PRAGMA)
To hit 10ms speeds, SQLite must utilize physical RAM aggressively:
- `PRAGMA journal_mode = WAL;` (Concurrent read/writes)
- `PRAGMA mmap_size = 268435456;` (256MB Memory-Mapped I/O for bus-speed reads)
- `PRAGMA cache_size = -32000;` (32MB PCache1 limit)
- `PRAGMA temp_store = MEMORY;` (RAM-based transient storage for CTE joins)

---

# Advanced Economics of Context Caching
## A Mathematical Deep Dive into Anthropic, Google [[GEMINI|Gemini]], and vLLM

### The Paradigm Shift: Stateful Computation
LLM inference was traditionally stateless, forcing massive redundant compute for [[master|Master]] System Prompts. Prompt caching shifts this to a stateful computation by preserving the KV cache of the attention layers.

### Anthropic [[CLAUDE|Claude]] (Ephemeral Caching)
- Uses `cache_control` blocks with exact prefix matching.
- **TTL:** 5-minutes (ephemeral) or 1-hour extended. Reset upon successful read.
- **Economics:** 
  - Write (5m): 1.25x base rate
  - Write (1h): 2.0x base rate
  - Read: 0.1x base rate (90% discount)
- Minimum token thresholds apply (e.g., 4,096 for Opus/Haiku, 1,024 for Sonnet).

*(Note: Report truncated, but captures core economics of stateful KV caching vs semantic similarity routing).*


---
📁 **See also:** [[Research_Archives/02_MCP_Tools/INDEX|← Directory Index]]
