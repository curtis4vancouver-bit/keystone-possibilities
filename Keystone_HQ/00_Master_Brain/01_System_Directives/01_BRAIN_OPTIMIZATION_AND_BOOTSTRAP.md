# Brain Optimization And Bootstrap

- **ID:** doc-01brainoptimizationandbootstrap
- **Type:** Document
- **Summary:** Optimization, bootstrap, and data organization instructions for Gemini 3.1 Pro (autonomous execution).
- **Tags:** bill-44, davinci, davinci-resolve, document, gemini-spark, keystone-possibilities, keystone-recomposition, okf, sea-to-sky, squamish, step-code, wayne-stevenson, youtube
- **Created:** 2026-06-10T08:21:21.710746
- **Updated:** 2026-06-14T19:57:36.085754
- **Entities:** Bill 44, DaVinci, DaVinci Resolve, Gemini Spark, Keystone Possibilities, Keystone Recomposition, Sea-to-Sky, Squamish, Step Code, Wayne Stevenson, YouTube

---

## Critical Context

### Environment Paths
- **Master Brain Directory:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\`
- **Qdrant Vector Database:** Running in Docker on ports `6333/6334` (container name: `keystone_qdrant_brain`).
- **MCP Server Path:** `C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Qdrant_Brain\keystone_brain_v2_mcp.py`

### Key System Issues Addressed
1. **Dumb search:** Limited to dense vector similarity without exact keyword matching.
2. **Bad chunking:** Document fragmentation at arbitrary fixed sizes.
3. **No time awareness:** Inability to differentiate new information from old.

---

## Phase 1: Brain State Audit

### Step 1.1: Verify Qdrant Service
```bash
docker ps | findstr qdrant
# If container is not running:
docker start keystone_qdrant_brain
```

### Step 1.2: Inspect Active Collections
```python
from qdrant_client import QdrantClient
client = QdrantClient(host="localhost", port=6333)
collections = client.get_collections()
for c in collections.collections:
    info = client.get_collection(c.name)
    print(f"Collection: {c.name}")
    print(f"  Vectors: {info.points_count}")
    print(f"  Dimensions: {info.config.params.vectors}")
    print(f"  ---")
```

### Step 1.3: Audit MCP Server Capabilities
Inspect `keystone_brain_v2_mcp.py` to identify:
- Embedded model dimensions and specifications.
- Implemented chunking and search methodologies (dense-only vs. hybrid).
- Metadata structure attached to indexed vectors.

### Step 1.4: Execute Semantic Baseline Searches
Utilize `search_master_brain` to test responsiveness and relevancy on the following targets:
- "Keystone Possibilities construction"
- "SEO optimization"
- "DaVinci Resolve timeline"
- "video production pipeline"

---

## Phase 2: Hybrid Search Implementation

### Architectural Strategy
Pure dense vector search fails to identify exact match terms such as "Bill 44", "STEP code 9.36.5.3", or specific version identifiers. Transitioning to a hybrid search setup combines dense semantic search with BM25 keyword matching via Reciprocal Rank Fusion (RRF).

### Recommended Embedding Models
- **BGE-M3:** Native dense, sparse, and multi-vector generation in one pass. (Highly Recommended)
- **Gemini Embedding 2 (gemini-embedding-001):** High-performing commercial option supporting Matryoshka truncation.
- **Nomic Embed Text V2:** Extended 8192-token context length.

### Step 2.1: Collection Configuration with Dense and Sparse Fields
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(host="localhost", port=6333)

# Establish hybrid collection
client.create_collection(
    collection_name="keystone_brain_v3",
    vectors_config={
        "dense": models.VectorParams(
            size=768,  # Match BGE-M3 or selected model dimension
            distance=models.Distance.COSINE
        )
    },
    sparse_vectors_config={
        "sparse": models.SparseVectorParams()
    }
)
```

### Step 2.2: Execute Hybrid Vector Search with Reciprocal Rank Fusion
```python
results = client.query_points(
    collection_name="keystone_brain_v3",
    prefetch=[
        models.Prefetch(
            query=dense_embedding,
            using="dense",
            limit=20
        ),
        models.Prefetch(
            query=sparse_embedding,  # Generated via sparse/lexical encoder
            using="sparse",
            limit=20
        )
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    limit=10
)
```

### Step 2.3: Ingestion Payload Specification
All payload items must attach temporal and domain-specific metadata:
```python
payload = {
    "content": chunk_text,
    "source_file": file_path,
    "namespace": namespace,
    "created_at": datetime.utcnow().isoformat() + "Z",
    "domain": "construction|media|health|agent_arch|seo|...",
    "doc_type": "research|skill|correction|insight|script|...",
}
```

### Step 2.4: Temporal Filtering Setup
```python
from datetime import datetime, timedelta

time_boundary = datetime.utcnow() - timedelta(days=30)

search_filter = models.Filter(
    should=[
        models.FieldCondition(
            key="created_at",
            range=models.Range(gte=time_boundary.isoformat() + "Z")
        )
    ]
)
```

---

## Phase 3: Semantic Chunking Engine

Fixed-size token chunking fragments structural logic. Implementing semantic boundary analysis ensures cohesive thematic blocks.

### Step 3.1: Adaptive Semantic Segmenter
```python
import numpy as np
from sentence_transformers import SentenceTransformer

def semantic_chunk(text: str, model, threshold: float = 0.3, max_chunk_size: int = 1500):
    """Splits text at natural semantic boundaries based on adjacent sentence similarity."""
    sentences = [s.strip() for s in text.split('. ') if s.strip()]
    if len(sentences) <= 1:
        return [text]
    
    embeddings = model.encode(sentences)
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        # Calculate cosine similarity
        sim = np.dot(embeddings[i-1], embeddings[i]) / (
            np.linalg.norm(embeddings[i-1]) * np.linalg.norm(embeddings[i])
        )
        
        current_text = '. '.join(current_chunk)
        if sim < threshold or len(current_text) > max_chunk_size:
            chunks.append(current_text + '.')
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
            
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    return chunks
```

### Step 3.2: Structure-Aware Markdown Parser
```python
def markdown_aware_chunk(text: str, max_size: int = 1500):
    """Splits markdown elements using headers as native partition boundaries."""
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in text.split('\n'):
        if line.startswith('#') and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = len(line)
        elif current_size + len(line) > max_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = len(line)
        else:
            current_chunk.append(line)
            current_size += len(line)
            
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks
```

### Step 3.3: Back Up and Re-Ingest Repositories
Prior to executing re-ingestion, generate a cold backup snapshot of the system state:
```python
client.create_snapshot(collection_name="keystone_brain")
```

Target ingestion directories:
- `Research_Archives/`
- `Master_Docs/`
- `Brand_Constitution/`
- `.learnings/correction_journal.json`
- Available `SKILL.md` skill files.

---

## Phase 4: File System Normalization

### Step 4.1: Target Research Archives Structure
Verify and maintain the structural integrity of `Research_Archives/`:
```
Research_Archives/
├── 01_Agent_Architecture/     # ADK, bootstrap, self-evolution logs
├── 02_MCP_Tools/              # MCP protocols and tool research
├── 03_YouTube_Scripts/        # Script formatting rules and writing engines
├── 04_YT_Analytics/           # YouTube algorithm tracking and analytical data
├── 05_Video_Production/       # Production specifications, DaVinci settings
├── 07_Coding_Optimization/    # Logic patterns, execution optimization
├── 08_SEO_Website/            # Local SEO, schema parameters, GEO strategy
├── 09_Social_Media/           # API tracking, distribution policies
├── 10_Tax_Legal_Corporate/    # Administrative, compliance, and legal structures
├── 11_Security/               # Code isolation guidelines and sandboxing
├── 12_Branding_Marketing/     # Brand strategy, layout standards
├── 13_Chrome_Automation/      # DevTools, headless automation scripts
├── 14_Gemini_Platform/        # Spark system, SDK updates, system APIs
├── 15_Content_Pipeline/       # Cross-platform publishing logic
├── 16_Wellness_Retreat/       # Scouting and wellness space planning
└── 17_BC_Construction/        # BC Building Code, Step Code compliance data
```

### Step 4.2: Duplicate Mitigation Rules
- Resolve the overlap between `Master_Docs/Research_Archives/` and the root `Research_Archives/` directory. Consolidate all historical assets under root `Research_Archives/`.
- Clean up obsolete `local_vector_db/` components in favor of the active `Qdrant_Brain/` structure.
- Maintain `Content_Production/` solely as an active work-in-progress script bin.

### Step 4.3: Brand Constitution Core
Verify files inside `Brand_Constitution/`:
- `BRAND_VOICE.md` — Linguistic properties, personality constraints.
- `BRAND_VISUAL.md` — Typography, palette logic, asset mappings.
- `CURRENT_DIRECTION.md` — Immediate targets, current strategic vector.
- `BRAND_EVOLUTION_LOG.jsonl` — Machine-parsable changelog of brand adaptations.
- Sub-brands: `/possibilities` (construction), `/protocol` (health/wellness), `/music` (creative assets).

### Step 4.4: Self-Evolution Logs
Ensure the presence of structural self-healing metadata under `.learnings/`:
- `correction_journal.json` (Minimum 18 operational adjustments tracking failures to fixes).
- `refined_prevention_rules.json` (Structured JSON rules ingested during agent setup).
- `working_memory.db` (Operational SQLite file).

---

## Phase 5: Systematic Bootstrap Configuration

**Bootstrap Skill Location:** `C:\Users\Curtis\.gemini\config\skills\keystone-session-bootstrap\SKILL.md`

### Bootstrap Protocol (8 Phases)

```markdown
### Phase 1: Cold Start Context Verification
- Determine the workspace configuration and analyze the active conversation environment.
- Detect whether this session is an incremental task resumption or a fresh start.

### Phase 2: Structural Memory Extraction
- Read `.learnings/correction_journal.json`.
- Select the 5 most recent corrective updates.
- Load constraints directly into working memory to prevent repeated logic failures.

### Phase 3: Domain Vector Queries
- Execute `search_master_brain` using terms relevant to the current objective.
- Pull the top 5 highly relevant content blocks from the vector store.

### Phase 4: Task Recovery and Backlog Sweep
- Check workspace files for open task manifests (`task.md`).
- Scan `Agent_Fleet/*/INBOX.json` to process pending inter-agent requests.
- Provide a concise status report of active/incomplete projects.

### Phase 5: System Skill Registry Verification
- Scan system tools at `C:\Users\Curtis\.gemini\config\skills\` and `00_Master_Brain\.agents\skills\`.
- Cache an index of available capabilities.

### Phase 6: MCP Server Verification
- Ping `keystone-brain` and `youtube-manager` MCP interfaces to verify connections.

### Phase 7: Brand Strategy Update
- Pull the current tactical objectives from `Brand_Constitution/CURRENT_DIRECTION.md`.

### Phase 8: Context Handshake
- Provide the user with a concise summary of current system state, pending operations, and a prompt for immediate task execution.
```

---

## Phase 6: Core Configuration Directory (`.agents/rules/`)

These highly-compressed configurations are loaded continuously to maintain operational alignment while preserving context tokens.

### Location
`00_Master_Brain\.agents\rules\`

### `workspace.md`
```markdown
# Keystone Workspace
- Root: c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\
- Brand: Keystone Possibilities (construction) + Keystone Recomposition (health/music)
- Owner: Wayne Stevenson
- Location: Sea-to-Sky Corridor, BC, Canada
- Contact: curtis4vancouver@gmail.com
```

### `mcp_tools.md`
```markdown
# Available MCP Tools
- keystone-brain: search_master_brain, list_brain_namespaces, ingest_to_brain, list_brain_sources
- youtube-manager: upload_video, update_video_metadata, set_video_privacy, get_channel_info, list_channel_videos, bulk_update_descriptions
- youtube-researcher: get_video_metadata, get_video_transcript
- chrome-devtools-mcp: navigate_page, take_snapshot, click, fill, evaluate_script
- brave-search: brave_web_search, brave_local_search
- sequential-thinking: sequentialthinking
```

### `token_routing.md`
```markdown
# YouTube Token Routing Rules
- Possibilities: youtube_token_possibilities.json
- Recomposition: youtube_token_oac.json
- Protocols: youtube_token_protocols.json
- Protocol Brand: Inherits credentials from Recomposition (OAC) - never assign independent credentials.
```

---

## Phase 7: Verification Suite

### Hybrid Search Test Cases
Verify accuracy and score calculations for these specific queries:
1. **"Bill 44 building code requirements"** -> Must resolve exact structural regulatory text.
2. **"how to write a YouTube short script"** -> Must return script templates.
3. **"DaVinci Resolve timeline assembly Python"** -> Must map to API execution patterns.
4. **"BGE-M3 embedding model"** -> Must retrieve configuration specifications.
5. **"Squamish construction contractor SEO"** -> Must output targeted regional marketing and local search guidelines.

### Success Metrics Checklist
- [ ] Qdrant is executing hybrid vector and lexical (dense + sparse) queries.
- [ ] Entire 185-file research repository has been re-indexed using structural semantic parsing.
- [ ] Correct temporal fields (`created_at`) are appended to all point payloads.
- [ ] Duplicate target directories have been consolidated.
- [ ] Bootstrap sequences execute through all 8 phases.
- [ ] `.agents/rules/` static configurations load and parse correctly.