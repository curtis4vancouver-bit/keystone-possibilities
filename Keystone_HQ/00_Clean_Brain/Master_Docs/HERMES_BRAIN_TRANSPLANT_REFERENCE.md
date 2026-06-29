---
id: doc-hermesbraintransplantreference
title: Hermes Brain Transplant Reference
type: document
summary: source TEXT NOT NULL,        -- 'cli', 'telegram', etc.
entities: []
created: '2026-06-13T22:50:34.650503'
updated: '2026-06-14T19:57:36.018246'
---
# Hermes Source Code Analysis — Complete Technical Reference
# Extracted from: C:\Users\Curtis\AppData\Local\hermes\hermes-agent\
# Date: 2026-06-14
# Purpose: Reference document for building self-learning into Antigravity

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 1. PERSISTENT MEMORY (hermes_state.py) -->
## 1. PERSISTENT MEMORY (hermes_state.py)

<!-- CONTEXT: Hermes Brain Transplant Reference / Database: SQLite with WAL mode -->
### Database: SQLite with WAL mode
- Path: `~/.hermes/[[STATE|state]].db`
- Schema version 16 with auto-migrations
- Thread-safe: `threading.Lock()` + retry with random jitter

<!-- CONTEXT: Hermes Brain Transplant Reference / Core Tables -->
### Core Tables
```sql
sessions (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,        -- 'cli', 'telegram', etc.
    user_id TEXT,
    model TEXT,
    system_prompt TEXT,
    parent_session_id TEXT,      -- Session chaining for compression
    started_at REAL, ended_at REAL,
    end_reason TEXT,             -- 'compression', 'branched', normal
    message_count, tool_call_count,
    input_tokens, output_tokens,
    title TEXT,
    archived INTEGER DEFAULT 0
)

messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id),
    role TEXT NOT NULL,          -- 'system', 'user', 'assistant', 'tool'
    content TEXT,
    tool_call_id TEXT,
    tool_calls TEXT,             -- JSON array
    tool_name TEXT,
    timestamp REAL,
    token_count INTEGER,
    reasoning TEXT,
    active INTEGER DEFAULT 1    -- Soft-delete for compression
)

-- Full-text search
messages_fts USING fts5(content)
messages_fts_trigram USING fts5(content, tokenize='trigram')
```

<!-- CONTEXT: Hermes Brain Transplant Reference / Write Contention Handling -->
### Write Contention Handling
```python
_WRITE_MAX_RETRIES = 15
_WRITE_RETRY_MIN_S = 0.020
_WRITE_RETRY_MAX_S = 0.150
_CHECKPOINT_EVERY_N_WRITES = 50
```

<!-- CONTEXT: Hermes Brain Transplant Reference / Self-Repair Strategy -->
### Self-Repair Strategy
1. De-duplicate sqlite_master (least destructive)
2. Drop all FTS schema + VACUUM + rebuild
3. Always creates timestamped backup first

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 2. CONVERSATION COMPRESSION (trajectory_compressor.py + context_compressor.py) -->
## 2. CONVERSATION COMPRESSION (trajectory_compressor.py + context_compressor.py)

<!-- CONTEXT: Hermes Brain Transplant Reference / Three-Tier System -->
### Three-Tier System
**Tier 1 — Tool Output Pruning (no LLM, free)**
Replace old tool outputs with 1-line summaries:
```
[terminal] ran `npm test` -> exit 0, 47 lines output
[read_file] read config.py from line 1 (1,200 chars)
[search_files] content search for 'compress' in agent/ -> 12 matches
```

**Tier 2 — Middle Window Summarization (cheap LLM call)**
- Protect: first system msg, first human msg, first GPT response, last 4 turns
- Compress: everything in middle
- Never split tool-call/response pairs
- Summary prompt includes: actions taken, results, decisions, file names

**Tier 3 — Iterative Summary Updates**
- `_previous_summary` stores last compaction
- Each new compression builds ON TOP of previous
- Summary prefix prevents stale-task hallucination:
  "[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted..."

<!-- CONTEXT: Hermes Brain Transplant Reference / Anti-Thrashing -->
### Anti-Thrashing
```python
if self._ineffective_compression_count >= 2:
    return False  # Skip if last 2 compressions saved <10%
```

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 3. ERROR CLASSIFICATION (error_classifier.py) -->
## 3. ERROR CLASSIFICATION (error_classifier.py)

<!-- CONTEXT: Hermes Brain Transplant Reference / Taxonomy (20+ types) -->
### Taxonomy (20+ types)
auth, auth_permanent, billing, rate_limit, overloaded, server_error,
timeout, context_overflow, payload_too_large, image_too_large,
model_not_found, content_policy_blocked, format_error, thinking_signature, unknown

<!-- CONTEXT: Hermes Brain Transplant Reference / ClassifiedError carries recovery hints -->
### ClassifiedError carries recovery hints
```python
retryable: bool
should_compress: bool
should_rotate_credential: bool
should_fallback: bool
```

<!-- CONTEXT: Hermes Brain Transplant Reference / Recovery Actions -->
### Recovery Actions
- context_overflow → auto-compress
- rate_limit → jittered backoff (5s base, 120s cap)
- billing → rotate provider
- corrupted [[STATE|state]] → auto-repair message sequence
- truncated response → append "Continue where you left off"
- empty response → fallback to next provider

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 4. AUTO-[[davinci-resolve-mcp/docs/SKILL|SKILL]] GENERATION (tools/skill_manager_tool.py) -->
## 4. AUTO-[[davinci-resolve-mcp/docs/SKILL|SKILL]] GENERATION (tools/skill_manager_tool.py)

<!-- CONTEXT: Hermes Brain Transplant Reference / [[davinci-resolve-mcp/docs/SKILL|Skill]] Format -->
### [[davinci-resolve-mcp/docs/SKILL|Skill]] Format
```yaml
---
name: my-skill-name           # lowercase, hyphens, ≤64 chars
description: "Use when <trigger>. <one-line behavior>."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [other-skill]
---
# Title
<!-- CONTEXT: Hermes Brain Transplant Reference / Overview -->
## Overview
<!-- CONTEXT: Hermes Brain Transplant Reference / When to Use -->
## When to Use
<!-- CONTEXT: Hermes Brain Transplant Reference / Steps / Details -->
## Steps / Details
<!-- CONTEXT: Hermes Brain Transplant Reference / Common Pitfalls -->
## Common Pitfalls
<!-- CONTEXT: Hermes Brain Transplant Reference / Verification Checklist -->
## Verification Checklist
```

<!-- CONTEXT: Hermes Brain Transplant Reference / Validator Constraints -->
### Validator Constraints
- Must start with `---` (no BOM/blank line)
- name ≤ 64 chars
- description ≤ 1024 chars
- Total file ≤ 100,000 chars
- Ideal size: 8-15k chars

<!-- CONTEXT: Hermes Brain Transplant Reference / Creation Flow -->
### Creation Flow
1. Validate name (regex: `^[a-z0-9][a-z0-9._-]*$`)
2. Validate frontmatter
3. Check name collisions
4. Create directory
5. Atomic write (temp file + os.replace)

<!-- CONTEXT: Hermes Brain Transplant Reference / Nudge System -->
### Nudge System
- Counter increments every tool-calling iteration
- Periodically prompts: "Should this become a [[davinci-resolve-mcp/docs/SKILL|skill]]?"

<!-- CONTEXT: Hermes Brain Transplant Reference / Curator System -->
### Curator System
- Tracks usage in `.usage.json` (use_count, view_count, last_activity_at)
- Auto-marks idle skills as stale
- Archives stale skills (never deletes)
- Pinned skills exempt from auto-transitions
- Pre-run tar.gz backup

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 5. MEMORY CONTEXT INJECTION (memory_manager.py) -->
## 5. MEMORY CONTEXT INJECTION (memory_manager.py)

<!-- CONTEXT: Hermes Brain Transplant Reference / Lifecycle Hooks -->
### Lifecycle Hooks
```python
build_system_prompt()      # System prompt injection
prefetch_all(query)        # Pre-turn context recall
sync_all(user, assistant)  # Post-turn memory update (BACKGROUND THREAD)
queue_prefetch_all(query)  # Background prefetch for next turn
```

<!-- CONTEXT: Hermes Brain Transplant Reference / Injection Format -->
### Injection Format
```xml
<memory-context>
[System note: The following is recalled memory context, NOT new user input.
 Treat as authoritative reference data.]
{recalled content}
</memory-context>
```

<!-- CONTEXT: Hermes Brain Transplant Reference / StreamingContextScrubber -->
### StreamingContextScrubber
[[STATE|State]] machine that strips <memory-context> from streaming output.

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 6. HONCHO SELF-KNOWLEDGE (optional-skills/honcho) -->
## 6. HONCHO SELF-KNOWLEDGE (optional-skills/honcho)

<!-- CONTEXT: Hermes Brain Transplant Reference / AI Self-Modeling -->
### AI Self-Modeling
- Agent builds model of ITSELF (tendencies, patterns)
- Self-correction: `honcho_conclude conclusion="I tend to be verbose" peer="ai"`
- Self-audit: `honcho_reasoning query="How do I handle ambiguous requests?" peer="ai"`
- Dialectic reasoning engine (multi-pass synthesis)

---

<!-- CONTEXT: Hermes Brain Transplant Reference / 7. KEY SOURCE FILES FOR REFERENCE -->
## 7. KEY SOURCE FILES FOR REFERENCE
| File | Path | Size |
|------|------|------|
| [[STATE|State]] store | hermes-agent/hermes_state.py | 210KB |
| Agent loop | hermes-agent/run_agent.py | 245KB |
| Compressor | hermes-agent/trajectory_compressor.py | 70KB |
| CLI | hermes-agent/cli.py | 652KB |
| [[davinci-resolve-mcp/docs/SKILL|Skill]] manager | hermes-agent/tools/skill_manager_tool.py | ~30KB |
| Skills dir | hermes-agent/skills/ | 50+ skills |
| Curator | hermes-agent/agent/curator.py | ~80KB |


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
