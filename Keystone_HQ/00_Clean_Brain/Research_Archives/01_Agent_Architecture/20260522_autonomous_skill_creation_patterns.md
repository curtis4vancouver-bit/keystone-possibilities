# Autonomous [[davinci-resolve-mcp/docs/SKILL|Skill]] Creation Patterns for AI [[AGENTS|Agents]]

**Research Date:** May 22, 2026
**Domain:** Self-Learning Patterns
**Author:** Keystone Overnight Research Agent

---

## Executive Summary

Autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] creation is the process by which AI [[AGENTS|agents]] transform successful task executions into reusable, portable procedural knowledge -- without human intervention. This report synthesizes research across open standards (agentskills.io), production frameworks (Hermes, Voyager, BabyAGI, Memento-Skills), and engineering best practices for [[davinci-resolve-mcp/docs/SKILL|skill]] extraction, validation, versioning, and deduplication. The key finding is that mature autonomous [[AGENTS|agents]] treat skills as first-class software artifacts: versioned, tested, deduplicated, and stored in searchable libraries for compositional reuse.

---

## 1. The [[davinci-resolve-mcp/docs/SKILL|SKILL]].md Format and agentskills.io Standard

The `[[davinci-resolve-mcp/docs/SKILL|SKILL]].md` format, published at **agentskills.io**, is the emerging open standard for portable agent skills. Originally introduced by Anthropic in late 2025 and released as an open standard on December 18, 2025, it works across [[CLAUDE|Claude]] Code, OpenAI Codex, Cursor, GitHub Copilot, and [[GEMINI|Gemini]] CLI.

### Anatomy of a [[davinci-resolve-mcp/docs/SKILL|Skill]] Directory

```text
skill-name/
  SKILL.md          # Required: YAML metadata + markdown instructions
  scripts/          # Optional: Executable code (Python, Bash, etc.)
  references/       # Optional: Documentation, API schemas
  assets/           # Optional: Templates, images, config files
```

### [[davinci-resolve-mcp/docs/SKILL|SKILL]].md File Structure

```yaml
---
name: code-reviewer
description: >-
  Review code for quality, security, and best practices.
  Use when user submits code for review.
metadata:
  author: your-name
  version: "1.0"
---

# Code Review Skill

When reviewing code, follow these guidelines:
1. Check for security vulnerabilities (e.g., OWASP Top 10).
2. Verify error handling completeness.
3. Suggest improvements based on project-specific style guides.
```

### Progressive Disclosure (Three-Stage Loading)

This is the critical performance optimization that makes large [[davinci-resolve-mcp/docs/SKILL|skill]] libraries practical:

| Stage | What Loads | When |
|:------|:-----------|:-----|
| **Discovery** | Only `name` and `description` from YAML frontmatter | At agent startup |
| **Activation** | Full `[[davinci-resolve-mcp/docs/SKILL|SKILL]].md` markdown body | When user request matches [[davinci-resolve-mcp/docs/SKILL|skill]] description |
| **Execution** | Scripts, references, assets | Only if instructions require them |

This means an agent can have hundreds of installed skills without context window bloat. Only the ~100 tokens of name+description are loaded initially per [[davinci-resolve-mcp/docs/SKILL|skill]].

### Key Design Constraints

- `name`: kebab-case, 1-64 characters
- `description`: 1-1024 characters -- this is the trigger mechanism; [[AGENTS|agents]] match user intent against it
- Skills are trigger-based: no explicit invocation required if the description is well-written
- Security concern: skills with executable scripts represent a supply chain risk; treat installation like adding npm dependencies

---

## 2. How Hermes Creates Skills Autonomously

The Hermes agent (Nous Research) implements a **closed learning loop** for autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] extraction:

### The Execute-Evaluate-Extract-Refine-Retrieve Loop

1. **Execute**: Agent completes a complex task (typically 5+ tool calls)
2. **Evaluate**: Internal evaluation analyzes the sequence of steps, tool calls, and reasoning that led to success
3. **Extract**: Agent autonomously writes a [[davinci-resolve-mcp/docs/SKILL|SKILL]].md document capturing the procedure, pitfalls, and verification steps
4. **Store**: Skills saved to `~/.hermes/skills/` directory
5. **Retrieve**: On future similar tasks, the agent retrieves and loads the relevant [[davinci-resolve-mcp/docs/SKILL|skill]] document
6. **Refine**: During subsequent uses, if a more efficient approach is discovered, the agent updates the existing [[davinci-resolve-mcp/docs/SKILL|skill]]

### Key Implementation Details

- **Performance gain**: [[davinci-resolve-mcp/docs/SKILL|Skill]] reuse reportedly yields ~40% faster task completion vs. fresh reasoning
- **Skills vs. Tools**: Skills are instructional playbooks (markdown); Tools are deterministic Python functions. Both are first-class but serve different purposes
- **Active nudging**: The agent is programmed to periodically self-prompt: "Should I save this as a [[davinci-resolve-mcp/docs/SKILL|skill]]?" when it detects a recurring, automatable pattern
- **Compatibility**: Hermes skills follow the agentskills.io standard, making them portable

### Alongside [[davinci-resolve-mcp/docs/SKILL|Skill]] Memory

Hermes maintains three forms of persistent memory:
- `MEMORY.md`: [[general|General]] knowledge and learnings
- `USER.md`: User preferences and environment quirks
- `~/.hermes/skills/`: Procedural knowledge (the [[davinci-resolve-mcp/docs/SKILL|skill]] library)

---

## 3. The Antigravity Workflow-[[davinci-resolve-mcp/docs/SKILL|Skill]]-Creator Plugin

The `workflow-[[davinci-resolve-mcp/docs/SKILL|skill]]-creator` plugin (installed locally in the Keystone system) provides a structured, human-in-the-loop approach to [[davinci-resolve-mcp/docs/SKILL|skill]] distillation. Unlike fully autonomous extraction, it operates in **four phases**:

### Phase 1: Brainstorming (Mandatory)

An iterative conversation across 5 rounds:
- **Round 1**: Understand the workflow (inputs, outputs, frequency)
- **Round 2**: Flexibility and error handling per step
- **Round 3**: Dependencies -- cross-reference existing installed skills to avoid reimplementation
- **Round 4**: Scope, shape, and whether code is needed (CLI pattern vs. instruction-only)
- **Round 5**: Optional test case for validation

### Phase 2: Design Document

Produces an implementation plan covering name, [[Master_Docs/00_DIRECTORY_STRUCTURE|directory structure]], referenced skills, new scripts, rate limiting, and error handling. Requires explicit user approval.

### Phase 3: Implementation

Key rules enforced:
- **Reuse existing skills** rather than reimplementing
- **Rate limiting** is mandatory for any new API interactions (default: 1 req/sec if undocumented)
- **CLI script pattern** is the default when code is needed (argparse with subcommands)
- **File output** is mandatory -- stdout for status messages only
- Uses `uv run`, never raw `python`

### Phase 4: Validation

Manual testing by invoking the agent with natural language that should trigger the new [[davinci-resolve-mcp/docs/SKILL|skill]], plus running any sample query/answer pairs from brainstorming.

### Architectural Insight

The workflow-[[davinci-resolve-mcp/docs/SKILL|skill]]-creator represents a semi-autonomous pattern: the agent does the heavy lifting of distillation, but human judgment gates the process at Phase 1 (brainstorming) and Phase 2 (design approval). For fully autonomous systems, these gates would need to be replaced by self-evaluation heuristics.

---

## 4. Tool Call Counting Heuristics for Triggering [[davinci-resolve-mcp/docs/SKILL|Skill]] Extraction

When should an agent auto-extract a [[davinci-resolve-mcp/docs/SKILL|skill]]? The research reveals several practical heuristics:

### Primary Trigger: Tool Call Count Threshold

The most common heuristic is a **minimum tool call threshold**:
- **5+ tool calls** in a single task execution is the typical trigger (used by Hermes)
- Below this threshold, the task is likely too simple to warrant [[davinci-resolve-mcp/docs/SKILL|skill]] creation
- The threshold should be tunable per domain

### Secondary Triggers

| Signal | Threshold | Action |
|:-------|:----------|:-------|
| Tool call count | >= 5 calls | Flag for extraction |
| Task recurrence | Same pattern seen 2+ times | Promote to [[davinci-resolve-mcp/docs/SKILL|skill]] |
| Backtracking detected | > 0 retries | Include failure-recovery in [[davinci-resolve-mcp/docs/SKILL|skill]] |
| Execution time | > 60 seconds | Candidate for optimization via [[davinci-resolve-mcp/docs/SKILL|skill]] |
| Confidence score | >= 0.5 relevance to existing skills | Load existing [[davinci-resolve-mcp/docs/SKILL|skill]] instead |

### Anti-Patterns to Avoid

- **Do NOT extract skills from failed tasks** -- only successful completions should become skills
- **Do NOT extract trivially simple tasks** (< 3 tool calls, single-step reasoning)
- **Do NOT extract one-off tasks** that will never recur (e.g., "fix this specific bug")
- **Watch for context saturation**: the soft limit is ~20 active tools/skills per agent; beyond this, decision-making degrades

### Relevance Threshold (tau)

Research from arxiv papers describes a calibrated relevance threshold: only patterns exceeding threshold tau are promoted to skills. This ensures extracted skills represent genuinely reusable patterns rather than project-specific implementations. Quality filters include:
- Successful resolution (no errors)
- Passing tests
- Absence of backtracking or redundant exploration

---

## 5. Validating Auto-Generated Skills Before Deployment

### The Layered Validation Approach

| Layer | What to Test | Method |
|:------|:-------------|:-------|
| **Component-Level** | Individual [[davinci-resolve-mcp/docs/SKILL|skill]] steps in isolation | Unit tests, mocked API calls |
| **End-to-End** | Full workflow in synthetic environment | Integration test with sample data |
| **Silent Trial** | Propose actions without executing | Shadow mode comparison to human decisions |
| **Adversarial** | Edge cases, malformed inputs, prompt injection | Red team testing |
| **Production Monitoring** | Drift, failure rates, latency | Continuous observability |

### Essential Validation Dimensions

1. **Task Success**: Does the [[davinci-resolve-mcp/docs/SKILL|skill]] resolve the intent within defined constraints (time, tool calls)?
2. **Tool Usage**: Correct tools selected? Schema validations in place?
3. **Safety/Policy**: Avoids prohibited outputs, handles PII, respects boundaries?
4. **Reasoning Quality**: Traceable logic? No infinite loops or unnecessary thrashing?
5. **Error Handling**: Graceful recovery from API timeouts, ambiguous inputs, corrupted data?

### LLM-as-Judge Pattern

Use a stronger, separate LLM to grade the auto-generated [[davinci-resolve-mcp/docs/SKILL|skill]]'s outputs and reasoning against a rubric. This enables scalable assessment of qualitative goals like completeness, correctness, and style compliance. This is particularly useful when the [[davinci-resolve-mcp/docs/SKILL|skill]] was created autonomously without human brainstorming.

### Kill-Switch Controls

During staged rollouts, ensure clear rollback paths. If a new [[davinci-resolve-mcp/docs/SKILL|skill]]'s performance degrades or it exhibits unpredictable behavior in canary mode, the system must be able to instantly revert to the previous version or disable the [[davinci-resolve-mcp/docs/SKILL|skill]] entirely.

---

## 6. [[davinci-resolve-mcp/docs/SKILL|Skill]] Versioning and Deduplication Strategies

### Versioning Best Practices

- **Treat skills as code**: Store in version control (Git). Each [[davinci-resolve-mcp/docs/SKILL|skill]] is a versioned directory
- **Semantic versioning**: Use `v1.2.0` format. [[AGENTS|Agents]] can pin to specific versions for stability
- **Version the entire stack**: Not just the prompt -- version the model checkpoint, tool definitions, and environmental context together
- **Deployment patterns**: Blue/green deployments for safe swaps; canary rollouts for gradual migration

### Deduplication via Embedding Similarity

The recommended production workflow for deduplication:

1. **Standardize**: Ensure each [[davinci-resolve-mcp/docs/SKILL|skill]] has uniform `name`, `description`, `tool_bindings`, `permissions` fields
2. **Embed**: Use sentence-transformers (e.g., `all-MiniLM-L6-v2`) to convert [[davinci-resolve-mcp/docs/SKILL|skill]] descriptions to dense vectors
3. **Normalize**: Always normalize vectors so dot product equals cosine similarity
4. **Block**: Use FAISS/Pinecone/Milvus for KNN candidate retrieval (reduces O(n^2) to manageable set)
5. **Threshold**: Apply calibrated cosine similarity threshold

| Threshold Range | Use Case |
|:----------------|:---------|
| 0.90-0.95 | Conservative -- only near-identical skills merged |
| 0.70-0.85 | Group conceptually similar skills (higher false positive risk) |
| 0.60-0.70 | Discovery/organization only -- do not auto-merge |

6. **LLM Validation**: Never auto-merge based on cosine similarity alone. Pass candidate pairs to an LLM for semantic comparison as a final sanity check

### Hierarchical [[davinci-resolve-mcp/docs/SKILL|Skill]] Organization

Group skills into high-level categories (e.g., "Data Analysis", "API Integration", "File Processing"). The agent first selects the category, then the specific [[davinci-resolve-mcp/docs/SKILL|skill]]. This reduces the decision space and prevents the "decision-making fog" that occurs with too many flat, overlapping skills.

---

## 7. Real-World Examples of Autonomous [[davinci-resolve-mcp/docs/SKILL|Skill]] Creation

### Voyager (Minecraft Agent)

The seminal example of autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] creation. Voyager uses GPT-4 to autonomously:
- **Generate** JavaScript programs (using the Mineflayer API) to achieve goals
- **Verify** via self-critique: environment feedback + execution errors + self-verification
- **Store** successful programs in a vector database, indexed by docstrings
- **Retrieve** relevant skills via embedding similarity when facing new tasks
- **Compose** complex behaviors from simpler stored skills

Key insight: Skills stored as executable code (not weight updates) can transfer to entirely new environments.

### BabyAGI

Explores self-building agent [[ARCHITECTURE|architecture]]:
- Breaks objectives into sub-tasks via task decomposition loops
- Newer versions (BabyAGI 2o) dynamically generate and register Python functions as reusable tools
- Stores learnings in persistent memory (learnings.md or vector DB) to avoid repeating mistakes

### Memento-Skills Framework

Implements the **Read-Execute-Reflect-Write** loop:
- **Read**: Retrieve relevant skills from external library
- **Execute**: Run [[davinci-resolve-mcp/docs/SKILL|skill]] in sandbox
- **Reflect**: Analyze failures, attribute to specific weak skills
- **Write**: Optimize, rewrite, or create new skills

Key advantage: Deployment-time learning without model retraining. The external [[davinci-resolve-mcp/docs/SKILL|skill]] bank evolves while the base model remains stable.

### Hermes (Production Agent)

As detailed in Section 2, implements the most complete production-ready autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] extraction with progressive disclosure, compatibility with agentskills.io, and active nudging for [[davinci-resolve-mcp/docs/SKILL|skill]] creation opportunities.

---

## 8. Implementation Recommendations for Keystone

Based on this research, here are actionable recommendations for the Keystone system:

### Immediate Actions

1. **Implement tool call counting**: Add a counter to agent sessions. When a successful task exceeds 5 tool calls, flag it for potential [[davinci-resolve-mcp/docs/SKILL|skill]] extraction
2. **Add a post-task reflection prompt**: After complex tasks, append: "This task involved N tool calls. Should I extract this as a reusable [[davinci-resolve-mcp/docs/SKILL|skill]]?"
3. **Use the existing workflow-[[davinci-resolve-mcp/docs/SKILL|skill]]-creator** for human-guided extraction; build autonomous extraction as a layer on top

### Medium-Term Architecture

4. **Build a [[davinci-resolve-mcp/docs/SKILL|skill]] deduplication pipeline**: Embed all existing [[davinci-resolve-mcp/docs/SKILL|skill]] descriptions, compute pairwise similarity, flag duplicates above 0.90 cosine threshold for review
5. **Implement semantic [[davinci-resolve-mcp/docs/SKILL|skill]] routing**: When a task arrives, embed the task description and retrieve top-k matching skills by cosine similarity before beginning execution
6. **Version skills in Git**: Each [[davinci-resolve-mcp/docs/SKILL|skill]] directory gets its own version in the YAML frontmatter; track changes via the brain vector DB

### Long-Term Vision

7. **Self-improving [[davinci-resolve-mcp/docs/SKILL|skill]] loop**: Implement the full Execute-Evaluate-Extract-Refine-Retrieve cycle
8. **[[davinci-resolve-mcp/docs/SKILL|Skill]] quality scoring**: Track [[davinci-resolve-mcp/docs/SKILL|skill]] usage frequency, success rate, and average time savings to rank and prune the [[davinci-resolve-mcp/docs/SKILL|skill]] library
9. **Cross-agent [[davinci-resolve-mcp/docs/SKILL|skill]] sharing**: Use the agentskills.io standard to share skills between Keystone sub-[[AGENTS|agents]]

---

## Sources Consulted

- agentskills.io -- Open standard specification for portable agent skills
- Anthropic documentation -- [[davinci-resolve-mcp/docs/SKILL|SKILL]].md format and Claude Code integration
- Hermes / Nous Research -- Autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] extraction workflow documentation
- Voyager (NVIDIA / MineDojo) -- Autonomous [[davinci-resolve-mcp/docs/SKILL|skill]] library creation in Minecraft
- BabyAGI (Yohei Nakajima) -- Self-building agent architecture
- Memento-Skills framework -- External procedural memory for LLM [[AGENTS|agents]]
- VentureBeat, Machine Learning Mastery, Medium -- Industry analysis and best practices
- arxiv.org -- Academic papers on [[davinci-resolve-mcp/docs/SKILL|skill]] extraction thresholds and relevance scoring
- Local Antigravity workflow-[[davinci-resolve-mcp/docs/SKILL|skill]]-creator plugin -- [[davinci-resolve-mcp/docs/SKILL|SKILL]].md at C:\Users\Curtis\.gemini\config\plugins\science\skills\workflow_skill_creator\[[davinci-resolve-mcp/docs/SKILL|SKILL]].md

---

*Report generated by Keystone Overnight Research Agent, May 22, 2026*


---
📁 **See also:** [[Research_Archives/01_Agent_Architecture/INDEX|← Directory Index]]

**Related:** [[20260521_hermes_agent_analysis_hermes_autonomous_skill_creation_and_tool_discovery_patterns]] · [[20260610_AGENT_ARCH_circuit_breaker_patterns_for_autonomous_agents__deep_researc]] · [[20260613_AGENT_ARCH_self-healing_error_recovery_patterns_for_autonomous_ai_agent]]
