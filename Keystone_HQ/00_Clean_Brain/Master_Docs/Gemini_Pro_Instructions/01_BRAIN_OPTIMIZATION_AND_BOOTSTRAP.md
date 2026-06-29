---
id: doc-01brainoptimizationandbootstrap
title: Brain Optimization And Bootstrap
type: document
summary: '> For: Gemini 3.1 Pro (autonomous execution)'
entities:
- Bill 44
- DaVinci
- DaVinci Resolve
- Gemini Spark
- Keystone Possibilities
- Keystone Recomposition
- Sea-to-Sky
- Squamish
- Step Code
- Wayne Stevenson
- YouTube
created: '2026-06-10T08:21:21.710746'
updated: '2026-06-14T19:57:36.085754'
---
# INSTRUCTION SET 1: Brain Optimization, Bootstrap & Data Organization
> **For:** [[GEMINI|Gemini]] 3.1 Pro (autonomous execution)  
> **Created:** 2026-06-10 by Antigravity  
> **Purpose:** Fix the Vector Brain, organize all data, implement proper bootstrap, ensure every new chat starts smart  
> **Estimated Time:** 2-3 hours  
> **Risk Level:** LOW — no destructive operations, all changes are additive

---

<!-- CONTEXT: Brain Optimization And Bootstrap / CRITICAL CONTEXT — READ FIRST -->
## CRITICAL CONTEXT — READ FIRST

You are working inside the **Keystone Sovereign [[master|Master]] Brain** at:
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\
```

The system has a **Qdrant vector database** running in Docker on ports 6333/6334 (container name: `keystone_qdrant_brain`).

The MCP server for the brain is at:
```
C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Qdrant_Brain\keystone_brain_v2_mcp.py
```

The brain has 3 critical problems you need to fix:
1. **Dumb search** — only does dense vector similarity, no keyword matching
2. **Bad chunking** — documents get split at arbitrary fixed sizes
3. **No time awareness** — can't differentiate new vs old information

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 1: AUDIT THE CURRENT BRAIN [[STATE|STATE]] -->
## PHASE 1: AUDIT THE CURRENT BRAIN [[STATE|STATE]]

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 1.1: Verify Qdrant is running -->
### Step 1.1: Verify Qdrant is running
```bash
docker ps | findstr qdrant
```
Expected: `keystone_qdrant_brain` container running on ports 6333-6334.

If not running:
```bash
docker start keystone_qdrant_brain
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 1.2: Check current collections -->
### Step 1.2: Check current collections
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

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 1.3: Read the current MCP server code -->
### Step 1.3: Read the current MCP server code
```
C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Qdrant_Brain\keystone_brain_v2_mcp.py
```
Understand:
- What embedding model is being used
- What chunking method is being used
- What search method is being used (dense only? hybrid?)
- What metadata is stored per vector

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 1.4: Check what's in the brain -->
### Step 1.4: Check what's in the brain
Use the `keystone-brain` MCP tool `search_master_brain` to run test queries:
- "Keystone [[possibilities|Possibilities]] construction"
- "SEO optimization"
- "DaVinci Resolve timeline"
- "video production pipeline"

Note the quality of results. Are they relevant? Are old results mixed with new?

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 2: IMPLEMENT HYBRID SEARCH -->
## PHASE 2: IMPLEMENT HYBRID SEARCH

<!-- CONTEXT: Brain Optimization And Bootstrap / Why this matters: -->
### Why this matters:
Dense vector search finds "conceptually similar" content but fails on exact terms like "Bill 44", "STEP code 9.36.5.3", or "BGE-M3". Hybrid search combines dense vectors with BM25 keyword matching for both semantic AND exact-match retrieval.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 2.1: Evaluate current embedding model -->
### Step 2.1: Evaluate current embedding model
Check what model the MCP server uses. The research recommends:
- **BGE-M3** (BAAI [[general|General]] Embedding) — BEST for hybrid search because it natively generates dense + sparse + multi-vectors in one pass
- **Gemini Embedding 2** (gemini-embedding-001) — Best commercial option, supports Matryoshka truncation
- **Nomic Embed Text V2** — 8192-token context, good for long documents

If the current model is `sentence-transformers/all-MiniLM-L6-v2` or similar lightweight model, it should be upgraded to BGE-M3 for hybrid search support.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 2.2: Update the brain MCP server to support hybrid search -->
### Step 2.2: Update the brain MCP server to support hybrid search
The MCP server needs to:
1. Create collections with BOTH dense and sparse vector fields
2. At ingestion time, generate both dense embeddings AND sparse BM25 vectors
3. At search time, run hybrid search combining both scores

**Qdrant hybrid search pattern:**
```python
from qdrant_client import QdrantClient, models

# When creating collection, define both vector types
client.create_collection(
    collection_name="keystone_brain_v3",
    vectors_config={
        "dense": models.VectorParams(
            size=768,  # BGE-M3 dimension
            distance=models.Distance.COSINE
        )
    },
    sparse_vectors_config={
        "sparse": models.SparseVectorParams()
    }
)

# When searching, use both
results = client.query_points(
    collection_name="keystone_brain_v3",
    prefetch=[
        models.Prefetch(
            query=dense_embedding,
            using="dense",
            limit=20
        ),
        models.Prefetch(
            query=sparse_embedding,
            using="sparse",
            limit=20
        )
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),  # Reciprocal Rank Fusion
    limit=10
)
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 2.3: Add temporal metadata to all vectors -->
### Step 2.3: Add temporal metadata to all vectors
Every vector ingested must include:
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

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 2.4: Add recency filtering to search -->
### Step 2.4: Add recency filtering to search
When searching, apply temporal filtering:
```python
from datetime import datetime, timedelta

# Default: prioritize last 30 days, but include older with decay
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

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 3: IMPLEMENT SEMANTIC CHUNKING -->
## PHASE 3: IMPLEMENT SEMANTIC CHUNKING

<!-- CONTEXT: Brain Optimization And Bootstrap / Why this matters: -->
### Why this matters:
Fixed-size chunking (e.g., 512 tokens) cuts documents in the middle of sentences, tables, and code blocks. Semantic chunking detects natural topic boundaries.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 3.1: Implement semantic chunking in the ingestion pipeline -->
### Step 3.1: Implement semantic chunking in the ingestion pipeline
```python
import numpy as np
from sentence_transformers import SentenceTransformer

def semantic_chunk(text: str, model, threshold: float = 0.3, max_chunk_size: int = 1500):
    """
    Split text at natural semantic boundaries instead of fixed sizes.
    """
    # Split into sentences
    sentences = [s.strip() for s in text.split('. ') if s.strip()]
    if len(sentences) <= 1:
        return [text]
    
    # Embed each sentence
    embeddings = model.encode(sentences)
    
    # Calculate cosine similarity between adjacent sentences
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        # Cosine similarity between adjacent sentences
        sim = np.dot(embeddings[i-1], embeddings[i]) / (
            np.linalg.norm(embeddings[i-1]) * np.linalg.norm(embeddings[i])
        )
        
        # If similarity drops below threshold, start new chunk
        current_text = '. '.join(current_chunk)
        if sim < threshold or len(current_text) > max_chunk_size:
            chunks.append(current_text + '.')
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 3.2: For markdown documents, use structure-aware chunking -->
### Step 3.2: For markdown documents, use structure-aware chunking
```python
def markdown_aware_chunk(text: str, max_size: int = 1500):
    """
    Respect markdown headers as natural chunk boundaries.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in text.split('\n'):
        # Headers create natural boundaries
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

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 3.3: Re-ingest all existing research -->
### Step 3.3: Re-ingest all existing research
After implementing the new chunking, re-ingest all documents from:
- `Research_Archives/` (185 files across 16 folders)
- `Master_Docs/` (60+ strategic documents)
- `Brand_Constitution/` (brand [[Brand_Constitution/protocol/IDENTITY|identity]] files)
- `.learnings/correction_journal.json` (error→fix mappings)
- All [[davinci-resolve-mcp/docs/SKILL|skill]] [[davinci-resolve-mcp/docs/SKILL|SKILL]].md files (so the brain knows what skills exist)

**IMPORTANT:** Before re-ingesting, back up the current collection:
```python
# Create a snapshot before making changes
client.create_snapshot(collection_name="keystone_brain")
```

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 4: ORGANIZE DATA INTO PROPER FOLDERS -->
## PHASE 4: ORGANIZE DATA INTO PROPER FOLDERS

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 4.1: Verify Research Archives structure -->
### Step 4.1: Verify Research Archives structure
The following folder structure should exist under `Research_Archives/`:
```
01_Agent_Architecture/     — ADK, Antigravity SDK, bootstrap, self-evolution
02_MCP_Tools/              — MCP server research and integrations
03_YouTube_Scripts/        — Script templates and writing guides
04_YT_Analytics/           — YouTube algorithm and analytics research
05_Video_Production/       — Google Flow, DaVinci, video editing
07_Coding_Optimization/    — Code patterns, performance, debugging
08_SEO_Website/            — SEO, GEO, schema, local search
09_Social_Media/           — Multi-platform publishing, tokens, APIs
10_Tax_Legal_Corporate/    — Tax strategy, legal compliance
11_Security/               — Security sandbox, data protection
12_Branding_Marketing/     — Brand strategy, copywriting, ads
13_Chrome_Automation/      — Chrome DevTools, web scraping
14_Gemini_Platform/        — Gemini Spark, ADK, API updates
15_Content_Pipeline/       — End-to-end production workflows
16_Wellness_Retreat/       — Property scouting, retreat planning
17_BC_Construction/        — BC Building Code, STEP code, regulations
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 4.2: Check for misplaced files -->
### Step 4.2: Check for misplaced files
Scan `Master_Docs/Research_Archives/` — this is a DUPLICATE location. Files here should be moved to the proper `Research_Archives/` subfolder.

```bash
# Check for duplicate research archives
dir "Master_Docs\Research_Archives" /b
```

If files exist there, move them to the correct subfolder under `Research_Archives/`.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 4.3: Clean up confusing duplicate folders -->
### Step 4.3: Clean up confusing duplicate folders
Check for and resolve:
- `Master_Docs/Research_Archives/` vs `Research_Archives/` — consolidate into `Research_Archives/`
- `local_vector_db/` vs `Qdrant_Brain/` — `Qdrant_Brain/` is the active one, `local_vector_db/` has only an empty vault
- `deprecated_scripts/` — leave as-is, these are archived intentionally
- `Content_Production/` — should contain production scripts (moved here during cleanup)

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 4.4: Verify Brand Constitution is complete -->
### Step 4.4: Verify Brand Constitution is complete
```
Brand_Constitution/
├── BRAND_VOICE.md           — Tone, personality, messaging guidelines
├── BRAND_VISUAL.md          — Colors, logos, typography standards
├── CURRENT_DIRECTION.md     — Current strategic direction
├── BRAND_EVOLUTION_LOG.jsonl — Change history
├── possibilities/           — Construction brand specifics
├── protocol/                — Health/wellness brand specifics
├── music/                   — Music brand specifics
└── shared/                  — Cross-brand assets
```

Read each file. If any are empty or stubs, populate them from existing Master_Docs content.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 4.5: Verify self-evolution files -->
### Step 4.5: Verify self-evolution files
```
.learnings/
├── correction_journal.json        — Should have 18+ entries
├── refined_prevention_rules.json  — Should have 18+ rules
├── working_memory.db              — SQLite, should exist
├── corrections/                   — Individual correction records
├── dream_logs/                    — Consolidation reports
├── errors/                        — Recent error cards
│   └── _archive/                  — Archived old errors
└── insights/                      — Daily digests, morning reports
```

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 5: UPDATE THE BOOTSTRAP [[davinci-resolve-mcp/docs/SKILL|SKILL]] -->
## PHASE 5: UPDATE THE BOOTSTRAP [[davinci-resolve-mcp/docs/SKILL|SKILL]]

<!-- CONTEXT: Brain Optimization And Bootstrap / Current bootstrap [[davinci-resolve-mcp/docs/SKILL|skill]] location: -->
### Current bootstrap [[davinci-resolve-mcp/docs/SKILL|skill]] location:
```
C:\Users\Curtis\.gemini\config\skills\keystone-session-bootstrap\SKILL.md
```

<!-- CONTEXT: Brain Optimization And Bootstrap / What the bootstrap currently does: -->
### What the bootstrap currently does:
- ✅ Loads correction journal
- ✅ Queries brain vector DB
- ✅ Reads daily digest

<!-- CONTEXT: Brain Optimization And Bootstrap / What needs to be ADDED: -->
### What needs to be ADDED:
1. **Unfinished task detection** — Check for any `task.md` files in active conversations
2. **Agent inbox check** — Scan `Agent_Fleet/*/INBOX.json` for pending items
3. **[[davinci-resolve-mcp/docs/SKILL|Skill]] registry loading** — Load a compact [[wiki/index|index]] of all available skills
4. **Circuit breaker check** — Look for repeated errors in recent logs
5. **File tree indexing** — Build a lazy-loadable [[wiki/index|index]] of the workspace

<!-- CONTEXT: Brain Optimization And Bootstrap / Updated bootstrap sequence: -->
### Updated bootstrap sequence:
```markdown
<!-- CONTEXT: Brain Optimization And Bootstrap / Bootstrap Protocol (8 Phases) -->
## Bootstrap Protocol (8 Phases)

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 1: Cold Start -->
### Phase 1: Cold Start
- Identify current workspace and conversation context
- Determine if resuming a task or starting fresh

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 2: Load Correction Journal -->
### Phase 2: Load Correction Journal
- Read `.learnings/correction_journal.json`
- Extract the 5 most recent corrections
- Inject as "MISTAKES TO AVOID" into working context

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 3: Query Brain for Context -->
### Phase 3: Query Brain for Context
- Use `search_master_brain` MCP tool
- Query with current task description
- Retrieve top 5 most relevant knowledge chunks

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 4: Check Unfinished Tasks -->
### Phase 4: Check Unfinished Tasks
- Scan for any `task.md` in recent conversation artifacts
- Check `Agent_Fleet/*/INBOX.json` for pending agent tasks
- Report any unfinished work to user

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 5: Load Skill Registry -->
### Phase 5: Load Skill Registry
- Read compact skill summaries (name + 1-line description)
- Skills are in: C:\Users\Curtis\.gemini\config\skills\
- Also check: 00_Master_Brain\.agents\skills\

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 6: Verify MCP Connections -->
### Phase 6: Verify MCP Connections
- Confirm keystone-brain MCP is responding
- Confirm youtube-manager MCP is responding
- Report any connection failures

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 7: Load Brand Context -->
### Phase 7: Load Brand Context
- Read Brand_Constitution/CURRENT_DIRECTION.md
- Understand current strategic priorities

<!-- CONTEXT: Brain Optimization And Bootstrap / Phase 8: Begin Work -->
### Phase 8: Begin Work
- Present available capabilities to user
- Ask what they need help with
```

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 6: CREATE THE `.[[AGENTS|agents]]/rules/` DIRECTORY -->
## PHASE 6: CREATE THE `.[[AGENTS|agents]]/rules/` DIRECTORY

This directory contains files that are ALWAYS loaded into context, every single chat. Keep them extremely compact to save tokens.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 6.1: Create the rules directory -->
### Step 6.1: Create the rules directory
```
00_Master_Brain\.agents\rules\
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 6.2: Create `workspace.md` -->
### Step 6.2: Create `workspace.md`
```markdown
# Keystone Workspace
- Root: c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\
- Brand: Keystone Possibilities (construction) + Keystone Recomposition (health/music)
- Owner: Wayne Stevenson
- Location: Sea-to-Sky Corridor, BC, Canada
- Email: curtis4vancouver@gmail.com
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 6.3: Create `mcp_tools.md` -->
### Step 6.3: Create `mcp_tools.md`
```markdown
# Available MCP Tools
- keystone-brain: search_master_brain, list_brain_namespaces, ingest_to_brain, list_brain_sources
- youtube-manager: upload_video, update_video_metadata, set_video_privacy, get_channel_info, list_channel_videos, bulk_update_descriptions
- youtube-researcher: get_video_metadata, get_video_transcript
- chrome-devtools-mcp: navigate_page, take_snapshot, click, fill, evaluate_script, etc.
- brave-search: brave_web_search, brave_local_search
- sequential-thinking: sequentialthinking
```

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 6.4: Create `token_routing.md` -->
### Step 6.4: Create `token_routing.md`
```markdown
# YouTube Token Routing (CRITICAL)
- Possibilities channel: youtube_token_possibilities.json
- Recomposition/OAC channel: youtube_token_oac.json (Protocol brand uses this)
- Protocols channel: youtube_token_protocols.json
- Protocol brand NEVER has its own tokens — always inherits from Recomposition
```

---

<!-- CONTEXT: Brain Optimization And Bootstrap / PHASE 7: VERIFICATION -->
## PHASE 7: VERIFICATION

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 7.1: Test hybrid search -->
### Step 7.1: Test hybrid search
Run 5 test queries comparing old vs new search quality:
1. "Bill 44 building code requirements" (should find exact regulatory text)
2. "how to write a YouTube short script" (should find script templates)
3. "DaVinci Resolve timeline assembly Python" (should find API docs)
4. "BGE-M3 embedding model" (should find vector DB research)
5. "Squamish construction contractor SEO" (should find local SEO research)

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 7.2: Test bootstrap -->
### Step 7.2: Test bootstrap
Start a new test session and verify all 8 phases execute properly.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 7.3: Document changes -->
### Step 7.3: Document changes
Update `[[AGENTS|AGENTS]].md` in the Master_Brain root with any architectural changes made.

<!-- CONTEXT: Brain Optimization And Bootstrap / Step 7.4: Record learnings -->
### Step 7.4: Record learnings
Add any issues encountered to `.learnings/correction_journal.json` using the format:
```json
{
    "error": "description of what went wrong",
    "fix": "what fixed it",
    "prevention": "how to prevent it in the future",
    "timestamp": "2026-06-10T..."
}
```

---

<!-- CONTEXT: Brain Optimization And Bootstrap / SUCCESS CRITERIA -->
## SUCCESS CRITERIA
- [ ] Qdrant brain supports hybrid search (dense + sparse)
- [ ] All 185 research files re-ingested with semantic chunking
- [ ] Temporal metadata on every vector
- [ ] No duplicate/confusing folder structures
- [ ] Bootstrap [[davinci-resolve-mcp/docs/SKILL|skill]] updated with 8 phases
- [ ] `.[[AGENTS|agents]]/rules/` directory created with compact context files
- [ ] 5 test queries return relevant, high-quality results
- [ ] All changes documented


---
📁 **See also:** [[Master_Docs/Gemini_Pro_Instructions/INDEX|← Directory Index]]
