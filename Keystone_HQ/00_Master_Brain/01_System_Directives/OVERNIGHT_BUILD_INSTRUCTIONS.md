# Overnight Build: Hermes → Antigravity Brain Transplant

This is the complete build instruction set for the overnight goal session. All code goes into `00_Master_Brain/`.

---

## PHASE 1: SQLite State Store (P0)
Build: `00_Master_Brain/core/state_store.py`

1. Create SQLite database at `00_Master_Brain/memory/state.db`
2. Implement tables: sessions, messages, messages_fts (FTS5)
3. WAL mode for concurrent read/write
4. Session chaining via parent_session_id
5. Write contention handling (15 retries, 20-150ms jitter)
6. Schema versioning with auto-migration
7. Full-text search across all stored messages
8. Self-repair: detect corruption → backup → repair → rebuild FTS
9. WAL checkpoint every 50 writes
10. API functions:
    - `create_session(source, model, system_prompt)` → `session_id`
    - `add_message(session_id, role, content, tool_calls, reasoning)`
    - `search_messages(query, limit)` → list of matches with session context
    - `get_session_chain(session_id)` → full lineage
    - `get_recent_sessions(n)` → last N sessions with summaries
    - `close_session(session_id, end_reason, title)`
    - `repair_database()` → self-healing

---

## PHASE 2: Auto-Skill Generator (P0)
Build: `00_Master_Brain/core/skill_generator.py`  
Build: `00_Master_Brain/agents/skills/self-learning-engine/SKILL.md`

1. Skill format matching Hermes spec (YAML frontmatter + markdown)
2. Validator: name ≤64 chars, description ≤1024, total ≤100K
3. Name regex: `^[a-z0-9][a-z0-9._-]*$`
4. Collision detection across all skill directories
5. Atomic write (temp file + `os.replace`)
6. Auto-detection: "Is this pattern reusable?" heuristic
7. Nudge counter: every N tool calls, consider skill creation
8. Save to: `00_Master_Brain/agents/skills/auto-generated/<name>/SKILL.md`
9. Usage tracking in `.usage.json`:
   - `use_count`, `view_count`, `patch_count`, `last_activity_at`, `state`, `pinned`
10. Curator: archive skills unused for 30+ days (never delete)

---

## PHASE 3: Memory Context Injection (P1)
Build: `00_Master_Brain/core/memory_manager.py`  
Update: session bootstrap skill

1. Pre-turn recall: query state_store + keystone-brain vector DB
2. Inject relevant memories as `<memory-context>` blocks
3. Post-turn sync: save new learnings to state_store (background)
4. Context fencing: prevent injection content from leaking to output
5. Relevance scoring: only inject memories above similarity threshold
6. Recency weighting: recent memories ranked higher
7. Update session_bootstrap skill to use memory_manager on startup

---

## PHASE 4: Conversation Compression (P1)
Build: `00_Master_Brain/core/conversation_compressor.py`

1. **Tier 1 - Tool output pruning (no LLM):**
   - Replace old tool outputs with 1-line summaries
   - Deduplicate identical tool results
   - Truncate large arguments
2. **Tier 2 - Middle window summarization:**
   - Protect first exchange + last 4 turns
   - Summarize middle turns
   - Never split tool-call/response pairs
3. **Tier 3 - Iterative summary updates:**
   - Store `_previous_summary`
   - Build each new summary on top of previous
   - Prefix with `"[CONTEXT COMPACTION — REFERENCE ONLY]"`
4. Anti-thrashing: skip if last 2 compressions saved <10%
5. Image/media stripping from old messages
6. Session splitting: create child session on compression

---

## PHASE 5: Error Classification & Self-Healing (P2)
Build: `00_Master_Brain/core/error_classifier.py`  
Build: `00_Master_Brain/core/self_healer.py`

1. Error taxonomy enum (20+ types)
2. `ClassifiedError` with recovery hints (retryable, should_compress, etc.)
3. Classification pipeline: provider → status → error code → message pattern
4. Recovery actions:
   - `context_overflow` → compress
   - `rate_limit` → jittered backoff
   - `corrupted state` → auto-repair
   - `truncated` → continue prompt
5. Jittered exponential backoff (5s base, 120s cap)
6. Fallback chain support

---

## PHASE 6: Self-Knowledge & Correction (P2)
Build: `00_Master_Brain/core/self_knowledge.py`  
Update: correction_journal system

1. AI self-modeling: track tendencies, patterns, common mistakes
2. Self-correction logging: "I tend to [X], I should [Y]"
3. Self-audit queries: "How do I handle [situation]?"
4. Integrate with `correction_journal.json` (upgrade from flat file to SQLite)
5. Auto-load self-knowledge into system prompt

---

## PHASE 7: Integration & Testing

1. Create unified `brain_init.py` that initializes all components
2. Update `self_evolution.py` to use new state store
3. Update `dream_engine.py` to use conversation compressor
4. Write Antigravity skill: `keystone-self-learning-engine/SKILL.md`
5. Test: create a session, add messages, search, compress, generate skill
6. Test: self-repair on corrupted database
7. Test: memory injection on fresh session
8. Save test results to vault
9. Update `INDEX.md` with new `core/` directory

---

## VERIFICATION CHECKLIST

- [ ] `state.db` created and queryable
- [ ] FTS5 search returns relevant results
- [ ] Session chaining works (parent → child)
- [ ] Auto-skill generator creates valid `SKILL.md` files
- [ ] Skill validator catches malformed files
- [ ] Usage tracking writes to `.usage.json`
- [ ] Memory recall returns relevant context
- [ ] Conversation compression preserves head + tail
- [ ] Iterative summaries build on previous
- [ ] Error classifier categorizes common errors correctly
- [ ] Self-repair recovers from intentional corruption
- [ ] Self-knowledge entries persist across sessions
- [ ] All `core/` modules import cleanly
- [ ] Existing `self_evolution.py` still works
- [ ] `INDEX.md` updated