# Error-Driven Learning Loops and Correction Journal Best Practices

**Research Date:** May 22, 2026
**Domain:** Self-Learning Patterns for AI [[AGENTS|Agents]]
**Researcher:** Keystone Overnight Research Agent
**Sources:** 11+ web searches across industry publications, engineering blogs, and academic references

---

## 1. Introduction: Why Error-Driven Learning Matters

Production AI [[AGENTS|agents]] fail constantly. The 2025 industry consensus is clear: failures are rarely model hallucinations -- they are **architectural and engineering failures** (infinite loops, poor memory management, lack of observability). The most successful agent systems do not aim for perfection; they aim for **resilience** -- the ability to detect, diagnose, and correct errors autonomously while remembering what went wrong so it never happens again.

This report synthesizes best practices for building error-driven learning loops into AI agent architectures, with a focus on correction journals, error fingerprinting, known-fix lookup, memory consolidation, and session bootstrap patterns.

---

## 2. Core [[ARCHITECTURE|Architecture]]: The Self-Corrective Loop

### 2.1 The Actor-Critic (Reflexion) Pattern

The most widely adopted pattern decouples execution from evaluation:

1. **Actor** agent attempts a task
2. **Evaluator** agent inspects the output against defined success criteria
3. On failure, the agent generates a **verbal self-reflection** (a diagnostic summary like "I forgot to handle empty arrays")
4. The agent retries the task, conditioned on the previous error and its reflection

This "verbal reinforcement" approach -- pioneered by the Reflexion framework -- lets [[AGENTS|agents]] learn from mistakes within a single session by accumulating textual reflections in a sliding memory buffer. Google DeepMind's SCoRe (Self-Correction via Reinforcement Learning) extends this further by training models to self-correct through self-generated data.

### 2.2 The Detect-Diagnose-Correct Triad

Modern "AgentDebug" philosophy structures error handling as three phases:

| Phase | Action | Implementation |
|:------|:-------|:---------------|
| **Detect** | Continuously monitor system health and output quality | Schema validation, confidence scoring, output assertions |
| **Diagnose** | Identify root cause, not just symptom | Causal reasoning, step-by-step trace visualization |
| **Correct** | Apply fix autonomously or escalate when confidence is low | Retry with modified parameters, human-in-the-loop for high-risk |

### 2.3 Budget Tripwires

To prevent runaway correction loops, implement **step-limited retry logic** with cost budgets. If an agent has attempted 3 corrections without success, it should escalate rather than spiral into infinite retry loops.

---

## 3. Correction Journal Design

### 3.1 What to Store

A correction journal is a structured, persistent memory component that records past failures and their resolutions. Each entry should capture:

```
## Entry Schema
- timestamp: ISO-8601 date of occurrence
- error_hash: SHA-256 fingerprint (see Section 4)
- trigger_context: What conditions caused the issue
- error_message: The raw error text or description
- action_attempted: What the agent tried to do
- reason_for_failure: Root cause analysis (why it failed)
- fix_applied: The correct approach or workaround
- category: (encoding | path | api | logic | config | dependency)
- confidence: (high | medium | low)
- occurrences: Count of times this error has been seen
```

### 3.2 What NOT to Store

- Raw, verbose tool outputs (summarize them instead)
- Minor conversational asides that do not influence behavior
- Redundant entries (deduplicate with fingerprinting)
- Intermediate reasoning scratchpads (ephemeral by nature)

### 3.3 How to Query

Use a **hybrid retrieval** approach combining:

1. **Deterministic lookup** by error hash (exact match for known errors)
2. **Semantic search** via vector embeddings (fuzzy match for similar-but-not-identical errors)
3. **Category filtering** to narrow results by error domain

This two-tier approach ensures that known errors are resolved instantly while novel-but-similar errors can still benefit from related past fixes.

---

## 4. Error Fingerprinting with SHA-256

### 4.1 The Fingerprinting Process

Error fingerprinting adapts techniques from production error trackers like Sentry:

1. **Normalize** the error by stripping volatile data (timestamps, memory addresses, line numbers, process IDs, file hashes)
2. **Extract** the stable signal (exception type, function names, error message pattern, file paths)
3. **Hash** the normalized string with SHA-256 to produce a deterministic fingerprint

```python
import hashlib
import re

def fingerprint_error(error_type: str, error_message: str, context: str = "") -> str:
    """Generate a SHA-256 fingerprint for deduplication."""
    # Step 1: Normalize - strip volatile data
    normalized = error_message.lower().strip()
    # Remove line numbers, timestamps, hex addresses
    normalized = re.sub(r'line \d+', 'line N', normalized)
    normalized = re.sub(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', 'TIMESTAMP', normalized)
    normalized = re.sub(r'0x[0-9a-fA-F]+', '0xADDR', normalized)
    # Remove file-specific hashes or build IDs
    normalized = re.sub(r'[a-f0-9]{32,}', 'HASH', normalized)

    # Step 2: Compose the fingerprint source
    source = f"{error_type}::{normalized}::{context}"

    # Step 3: Hash with SHA-256
    return hashlib.sha256(source.encode('utf-8')).hexdigest()[:16]
```

### 4.2 Avoiding Pitfalls

| Risk | Description | Mitigation |
|:-----|:------------|:-----------|
| **Over-grouping** | Stripping too much context merges distinct bugs | Keep error_type and context in fingerprint source |
| **Under-grouping** | Keeping too much detail creates separate entries for the same root cause | Normalize line numbers, paths, and timestamps |
| **Collision** | Two different errors produce the same hash (extremely rare with SHA-256) | Store normalized source text alongside hash; verify on lookup |

### 4.3 Deduplication Workflow

```
1. New error occurs
2. Normalize error text
3. Compute SHA-256 fingerprint (truncated to 16 hex chars)
4. Lookup fingerprint in journal
   - IF FOUND: increment occurrences, update timestamp, skip duplicate entry
   - IF NOT FOUND: create new journal entry with full context
```

---

## 5. Known-Fix Lookup Tables

### 5.1 Design Pattern

A known-fix lookup table maps error fingerprints to proven solutions:

```json
{
  "a3f8b2c1d4e5f6a7": {
    "error_type": "UnicodeEncodeError",
    "pattern": "codec can't encode character",
    "fix": "Replace emoji/special chars before writing. Use encoding='utf-8' with errors='replace'.",
    "confidence": "high",
    "times_applied": 12
  },
  "b7c9d0e1f2a3b4c5": {
    "error_type": "FileNotFoundError",
    "pattern": "path contains spaces or special characters",
    "fix": "Wrap path in quotes. Use pathlib.Path() instead of string concatenation.",
    "confidence": "high",
    "times_applied": 8
  }
}
```

### 5.2 Retrieval-Augmented Correction (RAC)

The full RAC workflow for matching new errors to previous solutions:

1. **Error occurs** -- capture error type, message, and stack trace
2. **Compute fingerprint** -- normalize and hash the error
3. **Exact match lookup** -- check fingerprint against known-fix table
4. **Semantic fallback** -- if no exact match, embed the error context and query a vector database for semantically similar past failures
5. **Inject into context** -- present the retrieved fix(es) to the agent as "lessons learned" in its prompt
6. **Apply and verify** -- agent applies the suggested fix and runs verification
7. **Update table** -- if a new fix is discovered, add it to the lookup table

### 5.3 Promotion and Demotion

- **Promote** a fix entry when it is applied successfully (increase confidence, increment times_applied)
- **Demote** a fix entry when it fails to resolve the issue (decrease confidence, flag for review)
- **Archive** entries with consistently low confidence after human review

---

## 6. Memory Consolidation: Keeping Journals Lean

### 6.1 The Size Problem

Unbounded correction journals lead to "context bloat" where retrieval quality degrades. For systems with hard character limits (like the Hermes MEMORY.md 2200-char cap), aggressive consolidation is mandatory.

### 6.2 Consolidation Strategies

**Tiered Retention Model:**

| Tier | Content | Retention Policy |
|:-----|:--------|:-----------------|
| **Active** | Errors seen in last 7 days | Keep full detail |
| **Consolidated** | Errors older than 7 days but still relevant | Compress to one-line summaries |
| **Archived** | Errors resolved and not recurring | Move to separate archive file, remove from active journal |
| **Deleted** | Superseded entries, duplicates, obsolete fixes | Purge entirely |

**Rolling Summary Approach:**
- Every N sessions (or when journal exceeds size threshold), trigger a consolidation pass
- Use the LLM to summarize groups of related entries into dense, actionable rules
- Replace 10 verbose entries with 1 consolidated rule

Example consolidation:

```
BEFORE (10 entries about encoding errors):
  - Entry 1: UnicodeEncodeError when writing to file...
  - Entry 2: CP1252 codec error on emoji character...
  - ...

AFTER (1 consolidated rule):
  RULE: Never use emoji or special Unicode in file writes on Windows.
  Always specify encoding='utf-8' with errors='replace'. Strip non-ASCII
  from print() statements. [Seen 10 times, last: 2026-05-20]
```

### 6.3 Smart Summarization for Hard Caps (2200 chars)

When working within strict character limits like MEMORY.md:

1. **Prioritize by impact** -- keep entries that have been triggered most frequently
2. **Use imperative format** -- "ALWAYS do X" and "NEVER do Y" instead of narrative explanations
3. **Category headers** -- group entries under 3-4 category headers for scanability
4. **Drop examples** -- keep the rule, drop the illustrative code unless absolutely critical
5. **Count entries** -- aim for 15-20 entries maximum at ~100-120 chars each
6. **Version suffix** -- append a timestamp so you know when the journal was last consolidated

Example MEMORY.md structure (under 2200 chars):

```markdown
# Correction Journal (v2026-05-22)

## Encoding
- NEVER use emoji in file content or print() -- CP1252 crashes on Windows
- ALWAYS use encoding='utf-8' with errors='replace' for file writes
- Strip non-ASCII before writing to any log or output file

## Paths
- ALWAYS use raw strings or pathlib for Windows paths with spaces
- NEVER hardcode drive letters -- use relative paths from project root

## API/Tools
- Brain MCP ingest: content param is required, not optional
- Chrome MCP: always check page load before taking screenshot
- Vector search returns max 10 results -- paginate if needed

## Logic
- Check array length before indexing -- empty arrays crash silently
- Validate JSON structure before parsing -- malformed JSON kills the session
- Always confirm file exists before read operations

## Session
- Load correction journal FIRST in every bootstrap sequence
- Query brain for recent daily digest at session start
- Never assume previous session context is available

[Last consolidated: 2026-05-22 | 14 entries | 1847 chars]
```

---

## 7. Surfacing Past Corrections in New Sessions

### 7.1 Push vs. Pull Strategies

| Strategy | How it Works | Pros | Cons |
|:---------|:-------------|:-----|:-----|
| **Push (Prewarm)** | Inject top corrections into system prompt at session start | Guaranteed visibility; zero-latency | Consumes prompt tokens; may include irrelevant entries |
| **Pull (On-Demand)** | Agent queries correction database when an error occurs | Token-efficient; always relevant | Requires the agent to "know" to search; adds latency |
| **Hybrid** | Push top-5 critical rules; pull the rest on-demand | Best of both worlds | More complex implementation |

### 7.2 Relevance Scoring

When deciding which corrections to surface, score by:

- **Recency** -- errors from the last 7 days are weighted higher
- **Frequency** -- errors seen 5+ times are always included
- **Severity** -- errors that crashed sessions are always included
- **Relevance** -- if the current task involves file I/O, surface encoding corrections

---

## 8. Session Bootstrap Pattern

### 8.1 The Bootstrap Sequence

A robust session bootstrap follows this order:

```
1. LOAD identity and system instructions
2. READ correction journal (MEMORY.md or equivalent)
3. QUERY brain/vector DB for recent daily digest
4. QUERY brain for project-specific context relevant to current task
5. CHECK for any pending tasks or unfinished work from previous sessions
6. VERIFY tool availability (MCP connections, file system access)
7. BEGIN task execution with full context loaded
```

### 8.2 Implementation: Session Bootstrap [[davinci-resolve-mcp/docs/SKILL|Skill]]

```python
def bootstrap_session(config):
    """Initialize agent session with persistent context."""
    context = {}

    # Step 1: Load correction journal
    journal_path = config['correction_journal_path']
    if os.path.exists(journal_path):
        with open(journal_path, 'r', encoding='utf-8') as f:
            context['corrections'] = f.read()

    # Step 2: Query vector DB for recent learnings
    recent_learnings = vector_db.search(
        query="recent corrections and learnings",
        filter={"date": {"$gte": "2026-05-15"}},
        top_k=5
    )
    context['recent_learnings'] = recent_learnings

    # Step 3: Load daily digest
    digest_path = config['daily_digest_path']
    if os.path.exists(digest_path):
        with open(digest_path, 'r', encoding='utf-8') as f:
            context['daily_digest'] = f.read()

    # Step 4: Check for pending tasks
    pending = task_db.query(status='in_progress')
    context['pending_tasks'] = pending

    return context
```

### 8.3 Cold Start vs. Warm Start

- **Cold start** -- first session ever; no journal exists. Agent creates initial journal structure and begins learning from scratch.
- **Warm start** -- journal and brain DB populated from previous sessions. Agent loads context and immediately benefits from accumulated knowledge.
- **[[hot|Hot]] restart** -- agent crashed mid-session. Load journal PLUS session-specific [[STATE|state]] from the last checkpoint to resume exactly where it left off.

---

## 9. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Alternative |
|:-------------|:-------------|:-------------------|
| **Store everything** | Context bloat degrades retrieval quality | Selective storage with consolidation passes |
| **LLM-as-memory** | Relying solely on context window is unreliable | External persistent storage (files, vector DB) |
| **Silent failures** | Unlogged errors lead to invisible quality degradation | Explicit output validation and structured error capture |
| **God Agent** | Single monolithic agent suffers from context degradation | Decompose into specialized sub-[[AGENTS|agents]] |
| **Naive truncation** | Cutting oldest messages loses critical early context | Middle truncation: keep start + end, compress middle |
| **No verification** | Applying fixes without testing leads to false confidence | Always run a verification step after applying a fix |

---

## 10. Implementation Checklist

- [ ] Design correction journal schema with required fields (hash, context, fix, category)
- [ ] Implement SHA-256 error fingerprinting with proper normalization
- [ ] Build known-fix lookup table with promotion/demotion logic
- [ ] Set up hybrid retrieval (exact hash match + semantic vector search)
- [ ] Create consolidation script that runs every N sessions or at size threshold
- [ ] Implement session bootstrap sequence (load journal, query brain, check pending)
- [ ] Configure budget tripwires to prevent infinite correction loops
- [ ] Add output validation gates before returning results
- [ ] Set up MEMORY.md with 2200-char hard cap and smart summarization
- [ ] Establish rolling archive for historical entries that exceed active journal limits

---

## 11. Key Takeaways

1. **Errors are data, not failures.** Every error is an opportunity to strengthen the system's knowledge base.
2. **Fingerprint and deduplicate.** SHA-256 hashing of normalized error text prevents journal bloat from repeated errors.
3. **Push critical corrections at startup.** The session bootstrap should inject top corrections before the agent begins work.
4. **Consolidate aggressively.** Replace verbose entries with dense, imperative rules to stay within character limits.
5. **Verify every fix.** Never trust a correction without running a verification step.
6. **Hybrid retrieval wins.** Combine exact hash lookup for known errors with semantic search for novel-but-similar issues.
7. **Budget your retries.** Step-limited correction loops with escalation prevent runaway costs.

---

## Sources Consulted

- Sentry Documentation: Error fingerprinting and grouping algorithms (sentry.io, sentry.dev)
- Reflexion Framework: Self-reflection and verbal reinforcement for LLM [[AGENTS|agents]] (medium.com)
- Google DeepMind SCoRe: Self-Correction via Reinforcement Learning (youtube.com)
- Letta (MemGPT): Memory blocks and tiered retention architecture (letta.com)
- Anthropic: Structured note-taking and persistent memory (anthropic.com)
- Augment Code: Context correction and failure documentation patterns (augmentcode.com)
- Google ADK Blog: Agent memory bank and journaling patterns (googleblog.com)
- Arize AI: Context pruning and middle truncation strategies (arize.com)
- MindStudio: Learning store and persistent error databases (mindstudio.ai)
- Composio: Event-driven agent architectures (composio.dev)
- Multiple engineering blogs: Context engineering and MEMORY.md management (dev.to, medium.com, agentailor.com)


---
📁 **See also:** [[Research_Archives/01_Agent_Architecture/INDEX|← Directory Index]]
