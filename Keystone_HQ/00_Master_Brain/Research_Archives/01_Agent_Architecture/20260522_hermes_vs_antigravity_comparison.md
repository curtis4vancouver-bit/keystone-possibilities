# Hermes Agent vs Antigravity/Keystone: Comprehensive Feature Comparison

**Research Date:** May 22, 2026
**Researcher:** Keystone Overnight Research Agent
**Domain:** hermes_agent_analysis
**Sources Consulted:** hermes-agent.org, nousresearch.com, github.com/NousResearch/hermes-agent, medium.com, nvidia.com, dev.to, honcho.dev, agentskills.io, gepa-ai/gepa, deepeval.com, dailydoseofds.com, yuv.ai, glukhov.org

---

## Executive Summary

Hermes Agent (by Nous Research) and Google Antigravity (powering our Keystone Sovereign system) represent two fundamentally different philosophies for building autonomous AI [[AGENTS|agents]]. Hermes is an **open-source, self-hosted, model-agnostic agent runtime** designed for persistent self-improvement and multi-platform accessibility. Antigravity is a **Google-native agentic harness** tightly coupled to the Gemini model ecosystem with deep IDE integration and multi-agent orchestration.

Our Keystone system has already built several capabilities that parallel Hermes. However, there are **seven critical gaps** where Hermes offers features we either lack entirely or have only partially implemented.

---

## 1. Detailed Feature-by-Feature Comparison

### 1.1 Memory Architecture

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Session-to-session memory** | 3-layer system: MEMORY.md (curated facts, ~2200 chars), skills dir (procedural), SQLite FTS5 (episodic) | Correction journal + brain vector DB + daily digest. Implemented via `keystone-session-bootstrap` SKILL.md |
| **Frozen snapshot at boot** | MEMORY.md and USER.md auto-injected into system prompt every session | Session bootstrap skill reads correction journal + brain search + daily digest. Similar approach. |
| **Full-text episodic search** | SQLite FTS5 `session_search` tool across all past messages | Brain vector DB via `search_master_brain` MCP tool (450+ chunks). Semantic, not full-text. |
| **User modeling** | Honcho dialectical reasoning -- builds a psychological model of the user over time with dual-peer architecture (User Peer + AI Peer) | **GAP -- We have no user modeling layer.** Wayne's preferences are manually encoded in skills, not learned. |
| **Memory size management** | Hard cap at ~2200 chars forces consolidation and prioritization | No hard cap. Correction journal grows unbounded. No consolidation mechanism. |

**Verdict:** Keystone has a comparable 3-layer approach (correction journal = curated, brain DB = episodic, skills = procedural). However, we lack **Honcho-style user modeling** and **memory consolidation/pruning on the curated layer**.

### 1.2 Self-Learning and Self-Evolution

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Autonomous skill creation** | After 5+ tool-call tasks, auto-extracts successful workflows into SKILL.md files stored in `~/.hermes/skills/` | `self_evolution.py` can deploy dynamic skills, but requires explicit invocation -- not automatic. Skills go to `dynamic_skills/` dir. |
| **GEPA prompt evolution** | Genetic-Pareto Prompt Evolution -- evolutionary algorithm that mutates prompts/skills using LLM reflection, selects via Pareto frontier. 35x more sample-efficient than RL. Runs offline. | **GAP -- No prompt evolution system.** Our prompts/skills are static once written. No automated optimization. |
| **Data flywheel** | Captures execution trajectories as ShareGPT-compatible JSONL. Feeds into Atropos RL framework to fine-tune apprentice models. | **GAP -- No trajectory capture or model fine-tuning pipeline.** |
| **Skill refinement loop** | Skills continue to self-improve through continued use; GEPA re-optimizes periodically | `self_evolution.py` has retry loops and correction recording, but no iterative skill improvement after initial deployment. |
| **Verification gate** | All evolved variants must pass full pytest suite, size constraints, semantic preservation checks | `evaluation_harness.py` + `security_sandbox.py` provide AST validation and fixture tests. **This is comparable.** |

**Verdict:** Our self-evolution engine is solid for error recovery and sandboxed skill deployment. The critical gaps are **GEPA-style prompt optimization** (automating prompt improvements without GPU training) and **autonomous skill creation triggers** (the agent should auto-extract skills without being told to).

### 1.3 Error Recovery and Learning from Mistakes

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Self-correction reflection loop** | Attempts task, validates, feeds error diagnostics back to LLM for retry | `self_evolution.py` has `run_evolution_cycle()` with exponential backoff retry (up to 3 attempts). **Comparable.** |
| **Error fingerprinting** | Not explicitly documented as fingerprinting, but skill updates encode lessons learned | `_compute_error_fingerprint()` using SHA-256 hashing of error type + context + traceback. **We are ahead here.** |
| **Known-fix lookup** | Encoded in evolved skills -- no explicit journal | `_find_known_fix()` searches correction journal for matching fingerprints. **We are ahead here.** |
| **Goal persistence** | `/goal` command runs multi-turn workflows with judge model monitoring | **GAP -- No goal persistence system.** Tasks run within a single session or subagent invocation. |
| **Git-based audit trail** | Skills dir tracked in Git; can diff, revert agent "lessons" | `self_evolution.py` creates Git snapshots and can rollback. **Comparable.** |
| **Verbose debugging** | `/verbose` cycles through output modes | Antigravity provides tool output in context. **Comparable.** |

**Verdict:** Our correction journal with fingerprinting and known-fix lookup is **more structured than Hermes' approach**. However, we lack **goal persistence** -- the ability for a multi-step goal to survive session boundaries.

### 1.4 Multi-Platform Access

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Messaging gateway** | Single daemon serves CLI + Telegram + Discord + Slack + WhatsApp + Signal + Matrix + Email. Per-user session isolation. | **GAP -- Terminal/IDE only.** Antigravity runs in VS Code or CLI. No messaging platform integration. |
| **Always-on availability** | Self-hosted daemon runs 24/7 on VPS/server | Overnight research daemon (`overnight_research_daemon.py`) runs scheduled tasks, but no always-on conversational interface. |
| **Cross-platform continuation** | Start conversation in terminal, continue on phone via Telegram | **GAP -- No cross-device conversation continuity.** |
| **Scheduled delivery** | Cron scheduler pushes reports to messaging platforms | We have `schedule` tool and cron capability, but output stays in Antigravity context -- not pushed to external platforms. |

**Verdict:** This is a **major gap**. Hermes' multi-platform gateway is a killer feature for a business owner like Wayne who needs to interact with his AI from a phone on a job site.

### 1.5 Project Context Injection

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Auto-discovery** | Scans CWD for `.hermes.md` -> `[[AGENTS|AGENTS]].md` -> `CLAUDE.md` -> `.cursorrules` | Antigravity uses GEMINI.md files and skill YAML frontmatter. **Comparable.** |
| **Progressive subdirectory injection** | As agent navigates into subdirs, discovers and injects local [[AGENTS|AGENTS]].md | Antigravity has workspace-scoped context. Skills are loaded progressively (Level 0/1/2 pattern). **Comparable.** |
| **SOUL.md personality** | Separate file defines agent personality/identity globally | Our skills define behavioral rules but no dedicated personality file. **Minor gap.** |

**Verdict:** Roughly equivalent. Both systems support hierarchical project context.

### 1.6 Tooling and Extensibility

| Capability | Hermes Agent | Keystone/Antigravity |
|:---|:---|:---|
| **Built-in tools** | 70+ tools across toolsets (web search, browser automation, vision, image gen, TTS, file ops) | Antigravity provides file I/O, code editing, shell execution, sub-[[AGENTS|agents]], web search, browser (via MCP). We also have 40+ science skills, keystone-brain, postgres, chrome-devtools, brave-search. **Comparable or superior.** |
| **MCP support** | Not native -- Hermes uses its own tool registry | Antigravity has **first-class MCP support** with lazy/eager loading, multiplexer, and schema discovery. **We are ahead.** |
| **Model flexibility** | Model-agnostic: supports OpenAI, Nous Portal, OpenRouter, local models (vLLM/Ollama), credential pooling, auto-fallback | Locked to Gemini ecosystem. **Hermes is ahead on model flexibility.** |
| **Community skill sharing** | agentskills.io open standard, hermeshub, skilldock.io marketplaces | No community marketplace. Skills are local to our config. **GAP.** |

**Verdict:** Our MCP architecture is more extensible than Hermes' tool registry. However, we lack **model fallback/pooling** and **community skill sharing**.

### 1.7 Unique Hermes Features We Lack Entirely

| Feature | Description | Impact |
|:---|:---|:---|
| **GEPA Prompt Evolution** | Evolutionary algorithm that optimizes prompts, tool descriptions, and skills via LLM-driven reflection and Pareto selection. No GPU needed -- runs via API calls. Repository: `NousResearch/hermes-agent-self-evolution` and `gepa-ai/gepa` | HIGH -- Our prompts and skills are static. GEPA could automatically improve our system instructions. |
| **Honcho User Modeling** | Dialectical reasoning that builds a deep psychological model of the user. Tools: `honcho_profile`, `honcho_search`, `honcho_conclude`. Configurable strategy: per-session, per-directory, per-repo, global. | MEDIUM -- Useful for Wayne's workflow personalization but can be partially simulated with our brain DB. |
| **Multi-Platform Gateway** | Single daemon serving CLI + 7 messaging platforms with session isolation, media handling, and platform-specific formatting. | HIGH -- Wayne needs to interact from job sites via phone. This is the #1 missing UX feature. |
| **Data Flywheel / Atropos** | Captures execution trajectories as training data. Atropos RL framework enables fine-tuning of smaller models from the agent's own experience. | LOW (for us) -- We don't train our own models. But trajectory capture for audit/improvement is valuable. |
| **Goal Persistence** | `/goal` command that runs multi-turn autonomous workflows with judge-model monitoring, surviving across turns until objective is met or budget exhausted. | MEDIUM -- Our subagent system handles task delegation but goals don't persist across sessions. |
| **Autonomous Skill Trigger** | After 5+ tool calls on a complex task, automatically extracts and saves a reusable skill without user prompting. | HIGH -- Our `self_evolution.py` creates skills but only when explicitly called. The auto-trigger is the key difference. |

---

## 2. Gap Analysis: Priority Actions

### Priority 1 (HIGH -- Build This Month)

1. **Autonomous Skill Extraction Trigger**
   - Modify the agent loop to detect when a task used 5+ tool calls and completed successfully
   - Auto-generate a SKILL.md capturing the workflow
   - Save to `dynamic_skills/` and sync to multiplexer
   - Implementation: Add a post-task hook in the session bootstrap that counts tool invocations and triggers `workflow-skill-creator` skill automatically

2. **Multi-Platform Gateway (Telegram MVP)**
   - Build a lightweight Telegram bot bridge that connects to Antigravity CLI
   - Use Telegram Bot API + a relay daemon that pipes messages to/from an Antigravity agent process
   - Store session [[STATE|state]] in SQLite for cross-platform continuity
   - Start with text-only, add media handling later

3. **GEPA-Lite Prompt Optimizer**
   - Implement a simplified version of GEPA for our skill files
   - Weekly cron job that: (a) loads recent correction journal entries, (b) identifies skills with high error rates, (c) uses Gemini to propose mutations, (d) evaluates mutations against test fixtures, (e) deploys winners
   - Repository reference: `github.com/gepa-ai/gepa`

### Priority 2 (MEDIUM -- Build Next Month)

4. **Memory Consolidation Engine**
   - Add a hard cap to the correction journal (e.g., keep last 100 entries)
   - Weekly consolidation: compress old entries into summary insights
   - Prune the brain vector DB of outdated/superseded knowledge

5. **Goal Persistence Layer**
   - Create a `goals.json` file that tracks multi-session objectives
   - Session bootstrap reads active goals and attempts to advance them
   - Goals have: objective, success criteria, turn budget, current status, history

6. **User Preference Modeling (Honcho-Lite)**
   - Create a `USER_MODEL.md` that the agent updates based on observed patterns
   - Track: preferred communication style, common requests, project priorities, scheduling patterns
   - Inject into session bootstrap alongside correction journal

### Priority 3 (LOW -- Backlog)

7. **Trajectory Capture for Audit**
   - Log successful multi-step workflows as structured JSONL
   - Use for: debugging, skill extraction training data, performance analytics
   - Store in `.learnings/trajectories/`

---

## 3. What We Already Do Better Than Hermes

Our Keystone system has several advantages that Hermes lacks:

1. **MCP Architecture:** First-class Model Context Protocol support with dynamic multiplexer, lazy/eager tool loading, and multi-server orchestration. Hermes uses a monolithic tool registry.

2. **Structured Error Fingerprinting:** SHA-256 fingerprinting with known-fix lookup in the correction journal is more sophisticated than Hermes' skill-based error encoding.

3. **Vector Brain DB:** Semantic search over 450+ knowledge chunks via `keystone-brain` MCP provides deeper knowledge retrieval than Hermes' FTS5 text search.

4. **Science Skills Ecosystem:** 40+ specialized science skills (AlphaFold, PubChem, gnomAD, etc.) that Hermes has no equivalent for.

5. **Security Sandbox:** AST-level code validation before skill deployment. Hermes has community-contributed hardening patches but no formal AST sandbox.

6. **Deep Research Daemon:** Automated overnight research with web scraping, report generation, and brain ingestion. Hermes has cron scheduling but no dedicated research pipeline.

---

## 4. Recommended Implementation: Autonomous Skill Extraction

Here is a concrete design for the highest-priority gap -- automatic skill extraction:

```python
# auto_skill_extractor.py
# Post-task hook that monitors tool call count and triggers skill creation

import json
import os
from datetime import datetime

SKILL_THRESHOLD = 5  # Minimum tool calls to trigger extraction
DYNAMIC_SKILLS_DIR = "dynamic_skills"

class AutoSkillExtractor:
    def __init__(self):
        self.tool_call_count = 0
        self.tool_call_log = []
        self.task_description = ""

    def record_tool_call(self, tool_name: str, args: dict, result: str):
        self.tool_call_count += 1
        self.tool_call_log.append({
            "tool": tool_name,
            "args_summary": str(args)[:200],
            "result_summary": str(result)[:200],
            "timestamp": datetime.now().isoformat()
        })

    def should_extract_skill(self, task_succeeded: bool) -> bool:
        return (
            task_succeeded
            and self.tool_call_count >= SKILL_THRESHOLD
            and len(set(t["tool"] for t in self.tool_call_log)) >= 2
        )

    def generate_skill_md(self, skill_name: str, description: str) -> str:
        tools_used = list(set(t["tool"] for t in self.tool_call_log))
        steps = "\n".join(
            f"{i+1}. Call `{t['tool']}` with relevant parameters"
            for i, t in enumerate(self.tool_call_log)
        )
        return f"""---
name: {skill_name}
description: "{description}"
auto_generated: true
generated_at: "{datetime.now().isoformat()}"
tool_calls: {self.tool_call_count}
---

# {skill_name}

## Description
{description}

## Tools Required
{chr(10).join(f'- `{t}`' for t in tools_used)}

## Workflow Steps
{steps}

## Notes
This skill was automatically extracted from a successful task execution.
Review and refine before relying on it in production.
"""
```

---

## 5. Recommended Implementation: Telegram Bridge MVP

```python
# telegram_bridge.py (skeleton)
# Minimal Telegram <-> Antigravity relay

import asyncio
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def handle_message(update: Update, context):
    user_msg = update.message.text
    user_id = update.effective_user.id

    # Relay to Antigravity CLI via subprocess
    result = subprocess.run(
        ["gemini", "--prompt", user_msg],
        capture_output=True, text=True, timeout=120
    )

    response = result.stdout.strip() or "Processing error. Check logs."
    await update.message.reply_text(response[:4096])  # Telegram limit

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
```

---

## 6. Key Takeaways

| Area | Status | Action |
|:---|:---|:---|
| Memory & Learning | 80% parity | Add consolidation + user modeling |
| Self-Evolution | 60% parity | Add GEPA-lite + auto skill triggers |
| Error Recovery | 110% (we're ahead) | Maintain current system |
| Multi-Platform Access | 0% parity | Build Telegram gateway ASAP |
| Tooling/MCP | 120% (we're ahead) | Maintain MCP advantage |
| Community/Sharing | 10% parity | Consider agentskills.io compatibility |
| Goal Persistence | 20% parity | Add goals.json layer |

**Bottom line:** Hermes' three killer features we lack are (1) multi-platform messaging gateway, (2) autonomous skill extraction triggers, and (3) GEPA prompt evolution. Everything else we either match or exceed. Closing these three gaps would make our Keystone system definitively superior.


---
📁 **See also:** ← Directory Index

**Related:** [[20260522_gemini_platform_gemini_api_vs_antigravity_vs_chrome_deep_research_comparison]]
