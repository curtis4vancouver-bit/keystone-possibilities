# 🔧 Keystone System Upgrade Report
## Based on Overnight Research R001–R006 | June 17, 2026

---

## 🔴 HIGH PRIORITY — Upgrade Now

### 1. Skill File Progressive Disclosure (from R004)
**Current State:** Our skills load full SKILL.md content into context on every session.
**Research Says:** Use 3-tier progressive disclosure — Metadata (~100 tokens) → Instructions → Resources. Only load full content when a skill is activated.
**Action:** Refactor our 20+ skill files to separate metadata headers from instruction bodies. Only mount full instructions when the agent matches intent to a skill.

### 2. Correction Journal Schema Upgrade (from R004)
**Current State:** We have a correction journal but it uses freeform text entries.
**Research Says:** Use deterministic schemas: `{ tried, wrong_because, fix, timestamp }`. Agents should auto-load relevant corrections contextually before repeating past mistakes.
**Action:** Standardize `correction_journal.jsonl` entries to the structured schema. Add a pre-task query step that searches the journal for relevant past errors.

### 3. Vector DB Memory Stratification (from R002)
**Current State:** Our keystone-brain vector DB stores everything in one flat namespace.
**Research Says:** Memory must be split into 4 layers: Working (volatile), Episodic (time-decayed), Semantic (permanent facts), Procedural (workflows).
**Action:** Create separate namespaces in keystone-brain for each memory layer. Implement temporal decay on episodic entries.

### 4. Cross-Encoder Reranking (from R002)
**Current State:** We search the brain with basic vector similarity only.
**Research Says:** Vector search alone misses negations, contradictions, and subtle semantic matches. Add a cross-encoder reranking stage between retrieval and prompt injection.
**Action:** Integrate Cohere Rerank or Jina Reranker v2 as a second-pass filter on brain search results before injecting into context.

---

## 🟡 MEDIUM PRIORITY — Plan & Schedule

### 5. MCP Tool Description Separation (from R001)
**Current State:** Our custom MCP servers mix parameter rules into root tool descriptions.
**Research Says:** Root `tool.description` should focus on discovery intent + exclusionary guidance. Parameter constraints belong in `inputSchema.properties.description`.
**Action:** Audit keystone-brain, content-engine, and other custom MCP servers. Move parameter formatting rules to property-level descriptions.

### 6. MCP Error Handling Upgrade (from R001, R006)
**Current State:** Some MCP servers throw raw errors that crash agent reasoning.
**Research Says:** Return structured JSON with `isError: true`, descriptive correction text, and `retry_after` hints. Never expose raw stack traces to the LLM.
**Action:** Wrap all custom MCP tool handlers with structured error responses.

### 7. Deterministic Orchestration (from R003)
**Current State:** Our Chronos master brain uses LLM-driven routing to decide which agent handles a task.
**Research Says:** Dynamic LLM orchestration is deprecated. Use deterministic code paths (Router, Planner-Executor patterns) for predictable execution.
**Action:** Refactor fleet orchestrator to use hardcoded routing rules for known task categories, reserving LLM routing only for truly ambiguous requests.

### 8. Context Isolation Between Agents (from R003)
**Current State:** Agents share a common brain with no isolation during exploration.
**Research Says:** Shared global memory causes "context poisoning" — early errors corrupt downstream agents.
**Action:** Run exploratory tasks in sandboxed contexts. Only merge findings into shared state after task completion and validation.

### 9. Dreaming / Consolidation Pipeline (from R002)
**Current State:** We have a dream_engine.py but it's basic.
**Research Says:** Use Frequency × Recency × Diversity scoring. Memories crossing the threshold graduate from episodic to permanent semantic storage. Apply exponential decay: R(t) = e^(-t/S) with ~30-day half-life.
**Action:** Upgrade dream_engine.py to implement proper scoring and graduated memory promotion.

---

## 🟢 NICE TO HAVE — Future Improvements

### 10. Model Tiering (from R003)
**What:** Route cheap tasks (routing, summarization, log compaction) to fast models (Flash/Haiku), reserve premium models (Opus/Sonnet) for complex code generation only.
**Impact:** Major cost savings on token consumption.

### 11. Narrative Casting for Agent Handoffs (from R003)
**What:** When passing conversation history between agents, translate raw assistant messages into third-person narrative to prevent sub-agents from hallucinating prior actions as their own.
**Impact:** Cleaner agent transitions, fewer hallucinations during handoffs.

### 12. Git-Backed Skill Versioning (from R004)
**What:** Track skill file mutations on separate git branches. Only merge back to main after passing validation benchmarks.
**Impact:** Safe self-evolution without risking behavioral regression.

### 13. MCP Proxy Gateway (from R006)
**What:** Deploy a centralized proxy layer for all MCP traffic with connection pooling, rate limiting, and circuit breakers.
**Impact:** Better fault isolation, prevents cascading MCP failures.

### 14. Long-Running Operation Support (from R006)
**What:** For expensive tasks, use async task IDs with `keepAlive` duration so network drops don't lose completed work.
**Impact:** More resilient overnight research and batch processing.

---

## 📊 Summary Scoreboard

| Area | Current Grade | After Upgrades |
|------|:---:|:---:|
| Skill Files & Progressive Disclosure | C | A |
| Vector Memory Architecture | C+ | A- |
| Correction Journal | B- | A |
| MCP Tool Schemas | B | A |
| MCP Error Handling | C+ | A- |
| Agent Orchestration | B- | A- |
| Context Isolation | C | B+ |
| Dream/Consolidation Engine | D+ | B+ |
| Model Cost Optimization | C | B+ |

---

> **Bottom Line:** The biggest wins come from upgrading the **memory architecture** (stratified layers + temporal decay + reranking) and **skill file progressive disclosure** (saving massive context tokens). These two changes alone would make the entire Keystone system significantly smarter and more efficient per session.
