---
name: self-learning-engine
description: "Handles persistent memory, dynamic [[.agents/skills/seo-geo/SKILL|skill]] validation, conversation compaction, and self-healing error recovery."
version: 1.0.0
author: Keystone Sovereign Agent Fleet
license: MIT
platforms: [windows, macos, linux]
metadata:
  keystone:
    tags: [memory, self-healing, db, compaction]
---

# Self-Learning Engine [[.agents/skills/seo-geo/SKILL|Skill]]

## Overview
The `self-learning-engine` is the cognitive core of the Keystone Sovereign Agent Fleet. It introduces persistent message logging via SQLite WAL, three-tier context compaction to defeat context window overflow, hybrid semantic recall, and runtime self-healing recovery loops.

## Core Components

### 1. SQLite State Store (`core/state_store.py`)
- Persistent SQLite database at `00_Master_Brain/memory/state.db`.
- Implements concurrent WAL (Write-Ahead Logging) write safety with thread locks and random retries.
- Utilizes SQLite FTS5 for instant full-text search across all historical message text.

### 2. Auto-[[.agents/skills/seo-geo/SKILL|Skill]] Generator (`core/skill_generator.py`)
- Programmatically validates and compiles new agent skills.
- Implements strict validation constraints (YAML frontmatter, name length ≤64, description ≤1024, size ≤100KB).
- Employs atomic temp-write-and-replace routines.
- Curates stale skills (unused >30 days) to prevent context bloat.

### 3. Memory Context Injection (`core/memory_manager.py`)
- Performs pre-turn hybrid queries across Qdrant vector spaces and SQLite FTS indexes.
- Computes relevance and recency decay weighting.
- Injects authoritative context inside fenced `<memory-context>` XML blocks.
- Spawns post-turn message logging in background threads to avoid API call latency.

### 4. Conversation Compressor (`core/conversation_compressor.py`)
- Monitored character-count compaction:
  - **Tier 1**: Strips verbose tool stdout, listing results, and media blocks into one-line metadata summaries.
  - **Tier 2**: Summarizes middle-turn exchanges via Gemini API while protecting system instructions and active conversation tails (last 4 turns).
  - **Tier 3**: Iteratively builds summaries on top of previous compactions to prevent hallucination.
- Employs anti-thrashing rules (skips compression if <10% token space is saved twice consecutively).

### 5. Error Classification & Self-Healer (`core/error_classifier.py` & `core/self_healer.py`)
- Matches runtime failures against a 20+ item taxonomy (auth, billing, rate limits, corrupt databases).
- Automatically triggers self-repair routines:
  - **Context Overflow**: Auto-triggers conversation compressor.
  - **DB Corruption**: Drops FTS indexes, vacuums, and rebuilds.
  - **Rate Limits / Busy DB**: Runs jittered exponential backoffs (base 5s, cap 120s).
### 6. Self-Verification Loop (`core/self_verifier.py`)
- After each major tool call or agent action, run a verification check:
  - **Output Validation**: Did the tool return expected data? (non-empty, correct format)
  - **State Consistency**: Does the current state match what we planned?
  - **Strategy Adjustment**: If verification fails, adjust strategy before retrying
- Implements a 3-attempt circuit breaker per action before escalating to Chronos
- Logs all verification results to `memory/verification_log.jsonl`

## Verification Checklist
- [x] State database file `memory/state.db` initialized and queryable.
- [x] FTS5 search index responds to matching queries.
- [x] Compacted messages marked as active while older turns soft-deleted.
- [x] Stale skills curating correctly in dry runs.
- [x] Self-verification logs active at `memory/verification_log.jsonl`.

