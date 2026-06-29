# 🔒 DEEP RESEARCH PROMPTS — SYSTEM LOCKDOWN & OPTIMIZATION
> 20 prompts for [[GEMINI|Gemini]] Pro Deep Research
> Created: 2026-06-11
> Purpose: Fix everything that's broken so the system actually works when Wayne tries to use it

---

## PROMPT 1 — Qdrant Vector Database [[ARCHITECTURE|Architecture]]

```
Deep research into Qdrant vector database architecture for AI agent long-term memory systems in 2025-2026. I have a Qdrant instance with 14,000+ vectors across 30 namespaces. Three catch-all namespaces (general, keystone_brain, master) hold 12,000+ vectors and bury my 5-10 critical operational rules under mountains of old research documents. When I search for production workflows, I get back generic research papers instead of my actual operational playbooks.

Research: What is the optimal namespace strategy for a mixed-content vector DB (research docs, operational rules, error logs, brand guidelines, scripts)? How do I restructure 30 namespaces into a clean architecture? Should critical operational rules go in their own high-priority namespace? How do I implement metadata filtering so recent vectors always rank above old ones? What is the correct way to tag vectors with timestamps, categories, and priority levels in Qdrant? How do I batch-delete stale vectors from bloated namespaces? Include Qdrant-specific Python code examples, collection configuration, and payload indexing setup.
```

---

## PROMPT 2 — Qdrant Hybrid Search & Retrieval Quality

```
Deep research into hybrid search implementation in Qdrant vector database for maximum retrieval accuracy. My current setup uses pure vector similarity search which returns semantically similar but operationally irrelevant results. For example, searching "Google Flow video production workflow" returns YouTube scriptwriting research instead of my actual Google Flow automation steps.

Research: How do I implement hybrid search combining dense vector similarity with sparse keyword matching (BM25) in Qdrant? What is the Qdrant Fusion method and how do I configure it? What embedding models give the best results for mixed technical/operational content in 2026 (OpenAI ada-002 vs text-embedding-3-large vs Cohere embed-v3 vs open-source alternatives)? What chunk sizes work best for different document types — short operational rules (50 words) vs long research documents (5000 words)? How do I implement re-ranking to boost exact operational matches over fuzzy semantic matches? Include complete Python implementation code.
```

---

## PROMPT 3 — Qdrant Performance Tuning & Maintenance

```
Deep research into Qdrant vector database performance tuning, compaction, and maintenance for a production AI agent memory system. My Qdrant instance runs locally via Docker on Windows 11 and has been accumulating vectors for 3+ weeks without any maintenance.

Research: What HNSW index parameters (ef_construct, m, ef) give the best speed/accuracy tradeoff for collections under 20,000 vectors? How do I monitor query latency and identify slow searches? What is the correct Docker configuration (memory limits, storage drivers, volume mounts) for optimal Qdrant performance on Windows? How do I implement automatic vector deduplication to remove near-identical chunks? How do I set up scheduled maintenance (compaction, optimization, snapshot backups)? What are the warning signs that a collection needs restructuring? How do I migrate from a messy multi-namespace setup to a clean single-collection-with-payload-filtering architecture? Include Docker Compose configuration and Python maintenance scripts.
```

---

## PROMPT 4 — AI Agent Session Bootstrap Protocol

```
Deep research into AI agent session bootstrap protocols — how the best autonomous AI coding agents initialize themselves at the start of every conversation in 2025-2026. I use Google Gemini Antigravity which supports skills (markdown instruction files), rules, and a vector database. My current bootstrap loads 8 steps (correction journal, brain search, daily digest, unfinished tasks, skill registry, MCP verification, brand context) but the agent frequently ignores it or loads so much context that it loses focus on the actual task.

Research: How do Devin, Cursor, Windsurf, Claude Code, and similar AI agents handle session initialization? What is the optimal layered context architecture — what MUST go in the system prompt (always loaded) vs what gets loaded on-demand vs what stays in vector DB for retrieval? How do you keep the bootstrap under a token budget so it doesn't waste context window space? What is the right priority order for loading context? How do you implement a "hot path" that loads only what's relevant to the user's first message? Include specific implementation patterns for markdown-based skill systems.
```

---

## PROMPT 5 — Preventing AI Agent Behavioral Drift

```
Deep research into preventing AI agent behavioral drift during long-running autonomous batch tasks. The specific problem: I give my AI agent a batch task like "generate 51 video clips using these exact prompts in Google Flow." It does the first 15-20 correctly, then starts deviating — changing prompt formats, spawning unauthorized subagents, rewriting scripts to "optimize" them, or splitting single prompts into multiple fragments. By clip 30, the output is garbage.

Research: What causes LLM behavioral drift during extended sequential tasks? How do production AI systems enforce consistency over 50+ iterations? What are "workflow lock" or "deterministic execution" patterns where the agent cannot deviate from a defined procedure? How do state machines work for AI agent task execution? What are guard rails that detect and prevent deviation in real-time? How do you implement a "recipe mode" where the agent executes mechanically without creative improvisation? Include examples from RPA systems, industrial automation, and AI agent frameworks (LangGraph, CrewAI, AutoGen) that solve this exact problem.
```

---

## PROMPT 6 — MCP (Model Context Protocol) Server Architecture

```
Deep research into MCP (Model Context Protocol) server architecture, configuration, and optimization for AI coding agents in 2025-2026. I run 8+ MCP servers (Qdrant brain, YouTube manager, YouTube researcher, DaVinci Resolve, Google Workspace, Chrome DevTools, Brave Search, content engine) through a JSON config file. The problem: my AI agent frequently ignores available MCP tools and falls back to raw terminal commands or improvises from scratch instead of using the tools that are already wired up.

Research: What is the current MCP specification and best practices for server configuration? How do you structure mcp_config.json for optimal tool discovery? What is the difference between eager-loaded and lazy-loaded MCP tools and when should each be used? How do you write MCP tool schemas that AI agents actually understand and use correctly? How do you handle MCP server crashes, timeouts, and reconnection gracefully? What are the best patterns for MCP tool documentation (instructions.md) that maximize agent compliance? How do you test that MCP tools are actually being used? Include real mcp_config.json examples from production deployments.
```

---

## PROMPT 7 — Docker Container Optimization for AI Infrastructure

```
Deep research into Docker container optimization for AI agent infrastructure on Windows 11 in 2025-2026. I run Qdrant vector database, MCP servers, and potentially other services via Docker. I need to understand the optimal Docker Desktop configuration, resource allocation, networking, and persistence setup.

Research: What are the best Docker Desktop settings (WSL2 vs Hyper-V, memory allocation, CPU limits, disk space) for running AI infrastructure on Windows 11? How do you configure Docker volumes for persistent vector database storage that survives container restarts? What is the optimal Docker Compose setup for running Qdrant + custom MCP servers together? How do you implement health checks and auto-restart for containers? How do you monitor container resource usage and diagnose performance issues? What are the common Docker pitfalls on Windows (file system performance, networking, WSL2 memory leaks)? Include a production-ready Docker Compose file for an AI agent tech stack.
```

---

## PROMPT 8 — [[davinci-resolve-mcp/docs/SKILL|Skill]] Enforcement in AI Agent Systems

```
Deep research into making AI agents actually follow their defined skills and instruction files instead of improvising. I have 50+ skill files (markdown documents with detailed step-by-step instructions) for my AI coding agent, but it frequently ignores them and makes up its own approach. For example, I have a detailed Google Flow automation skill with exact button click sequences, but the agent skips reading it and invents its own DOM automation that breaks.

Research: How do the best AI agent frameworks (LangChain, CrewAI, AutoGen, Google ADK, Semantic Kernel) enforce tool and skill usage? What are "mandatory skill activation" patterns where the agent MUST read and follow a skill file before starting a task? How do you structure skill files for maximum compliance — length, format, specificity level? What is the difference between rules (always loaded, short) vs skills (loaded on demand, detailed) and how should they be organized? How do you prevent an agent from using its general training knowledge when a specific skill exists? How do you test and verify skill adherence? Include implementation examples.
```

---

## PROMPT 9 — Error Correction Journal & Self-Learning Systems

```
Deep research into AI agent error correction and self-learning systems for production deployments in 2025-2026. I maintain a JSON correction journal with 27 error→fix entries that the agent loads every session. The problem: ALL 27 entries load regardless of task relevance (e.g., TikTok OAuth fixes load during video production), wasting context window tokens. Also, the agent still repeats errors that have fixes in the journal.

Research: What is the optimal format and structure for an AI agent's error memory? How do you implement conditional loading — only loading relevant corrections based on the current task? What is the CLIN (Continually Learning from Interactions in Natural language) framework and how does it apply? How does the Reflexion pattern work for agent self-improvement? What is the optimal number of active prevention rules before they become noise? How do you implement spaced repetition for error prevention — emphasizing recent/frequent errors over old/rare ones? How do you verify that correction entries actually prevent the error from recurring? Include practical implementation patterns.
```

---

## PROMPT 10 — Context Window Token Optimization

```
Deep research into context window token optimization for AI coding agents in 2025-2026. My AI agent (Google Gemini via Antigravity) loads extensive background context at session start — correction journals, brain search results, skill files, brand guidelines, active projects — often consuming 30-50% of the context window before the user even asks a question. This leaves less room for actual task execution and causes the agent to lose focus on the user's request.

Research: How do the best AI agents minimize token waste? What is the optimal strategy for file loading — full file reads vs targeted line ranges vs summaries? How do you implement a "context budget" that caps background loading? What are tiered context architectures (L1 always-loaded critical rules, L2 task-relevant skills, L3 on-demand retrieval from vector DB)? How do you prevent "context pollution" where background info drowns out the actual task? What is the ideal system prompt length for maximum instruction following? How do you measure and track token efficiency? Include specific token budget breakdowns from production AI systems.
```

---

## PROMPT 11 — Google Flow Automation via Chrome DevTools Protocol

```
Deep research into automating Google Flow (labs.google/fx/tools/flow) for batch AI video production using Chrome DevTools Protocol (CDP) in 2026. I use a chrome-devtools-mcp server to control Chrome programmatically. The challenges: Google Flow uses React/Jotai state management making DOM manipulation unreliable, character/avatar attachment doesn't persist between prompts requiring re-attachment for every clip, settings can drift during batch operations, and prompts sometimes get split into fragments.

Research: What are the best practices for automating React-based web applications via CDP? How do you reliably interact with contenteditable divs and React-controlled form fields? How do you detect and wait for async operations (video compilation) to complete? What are the known DOM selectors and Jotai store access patterns for Google Flow specifically? How do you implement retry logic for failed generations? How do you maintain a state machine that tracks which clip is being generated and prevents skipping or duplicating? What are the alternatives to CDP for browser automation (Playwright, Puppeteer) and do they work better for React apps? Include specific JavaScript code for Google Flow interaction.
```

---

## PROMPT 12 — AI Video Production Pipeline Architecture

```
Deep research into end-to-end AI video production pipeline architecture using Google Flow (Veo 3.1), DaVinci Resolve, and automated publishing in 2026. I produce podcast-style videos with two AI avatars (Wayne and Victoria) having a conversation, with B-roll image overlays. The pipeline is: write script → generate 51 video clips in Google Flow → generate 51 B-roll images → download and rename all assets → assemble multi-track timeline in DaVinci Resolve → export → upload to YouTube.

Research: How do professional AI video producers structure this pipeline for reliability? What are the best practices for batch video generation with character consistency? How do you organize asset files (naming conventions, folder structure) for efficient DaVinci import? What is the optimal DaVinci Resolve scripting API workflow for automated timeline assembly? How do you implement quality checks between pipeline stages? What word count per 10-second AI-generated clip produces natural speech pacing? How do you handle failed/corrupted clips in a 50+ clip batch? What are the best export settings for YouTube long-form from DaVinci? Include real production pipeline architectures.
```

---

## PROMPT 13 — Rules File Architecture for AI Coding [[AGENTS|Agents]]

```
Deep research into AI agent rules file architecture and best practices in 2025-2026. Multiple AI coding tools use project-level instruction files: Cursor uses .cursorrules, Claude uses CLAUDE.md, Gemini uses AGENTS.md and .gemini/config/rules/. I currently have a massive AGENTS.md (200+ lines) plus 31 prevention rules in my bootstrap skill plus 50+ skill files. The agent still ignores critical rules during execution.

Research: What is the proven optimal structure for AI agent instruction files? How long should they be before they become counterproductive (diminishing returns on length)? Should you have one monolithic rules file or many small specialized ones? How do you handle rule priority — which rules should the agent NEVER be able to override? Where should rules live physically — system prompt vs project root vs config directory vs loaded dynamically? How do you implement "hard rules" (absolute constraints) vs "soft rules" (preferences)? How do you version and evolve rules without breaking existing workflows? Include real examples of effective .cursorrules, CLAUDE.md, and AGENTS.md files from high-performing projects.
```

---

## PROMPT 14 — Antigravity Agent Configuration Deep Dive

```
Deep research into Google Gemini Antigravity AI coding agent configuration and optimization. I need to understand every configurable aspect of the Antigravity system: skills (.gemini/config/skills/), plugins (.gemini/config/plugins/), rules, subagents, MCP server configuration, planning mode behavior, artifact system, and the relationship between workspace-level and global-level configuration.

Research: What is the complete Antigravity configuration hierarchy and how do different config locations interact? What is the exact format required for SKILL.md frontmatter and how does skill activation work (auto vs manual vs conditional)? How do plugins differ from skills and when should each be used? How does the planning mode decision logic work — when does it plan vs act directly? What controls subagent behavior and how do you restrict unauthorized subagent spawning? How do you configure model selection and tool permissions? What are the undocumented features and configuration options? How do you debug when the agent ignores configuration? Include the complete configuration reference.
```

---

## PROMPT 15 — Preventing AI [[AGENTS|Agents]] from Ignoring Instructions

```
Deep research into why AI agents ignore instructions and how to fix it, from both a cognitive science and AI engineering perspective. My AI agent has detailed rules saying "NEVER do X" and "ALWAYS do Y" but after 15-20 steps in a long task, it starts violating them. It spawns subagents when told not to, changes prompt formats when told to keep them exact, and adds "improvements" to workflows that are supposed to be followed literally.

Research: What causes instruction decay in large language models during extended interactions? Is it attention mechanism limitations, positional encoding decay, or something else? What research exists on LLM instruction following reliability vs conversation length? What formatting strategies maximize rule adherence — numbered lists vs bold text vs XML tags vs repeated reminders? Should critical rules be placed at the beginning or end of the context? How do you implement "rule refreshing" that re-injects critical rules at key decision points during long tasks? What is the AI safety research on behavioral constraint enforcement? Include empirical data on instruction following degradation over conversation length.
```

---

## PROMPT 16 — Automated Testing for AI Agent Workflows

```
Deep research into automated testing and validation for AI agent workflows in 2025-2026. Every time my AI agent claims "system is running optimally" or "all checks passed," I try to actually use it and something is broken. I need a way to verify that the system actually works before I rely on it.

Research: How do you write automated tests for AI agent behavior? What are the frameworks for testing MCP tool connectivity, vector DB retrieval quality, skill loading compliance, and end-to-end workflow execution? How do you implement smoke tests that run at session start to verify critical capabilities? How do you test that prevention rules actually prevent the errors they're supposed to prevent? What are evaluation harnesses for AI agents and how do they work? How do you implement continuous integration for an AI agent's configuration (skills, rules, brain content)? What metrics should you track to measure agent reliability over time? Include testing framework code and example test suites.
```

---

## PROMPT 17 — YouTube Podcast Video Style & Engagement

```
Deep research into the most engaging visual styles for YouTube podcast videos featuring AI-generated avatars in 2026. Specifically comparing: straight-on direct-to-camera talking head vs seated at an angle in a chair interview style vs over-the-shoulder conversational format. I'm producing a two-person podcast (Wayne and Victoria) discussing peptides and health protocols.

Research: What camera angles and framing produce the highest watch time retention for YouTube podcasts? What do the data show about Joe Rogan, Huberman Lab, Diary of a CEO, and similar top podcasts in terms of visual setup? For AI-generated avatar videos specifically, what prompting techniques produce the most natural-looking seated conversation? How do you write video generation prompts that create convincing 3/4 profile angled shots? What background elements improve perceived production quality? How do you create visual variety across 50+ clips without breaking character consistency? What is the optimal B-roll overlay frequency and duration for maintaining viewer attention? Include specific prompt templates that work with Veo 3.1 / Google Flow.
```

---

## PROMPT 18 — Content Script Research Verification

```
Deep research into automated fact-checking and research verification for YouTube health/science content scripts in 2026. I produce videos about peptides (BPC-157, GHK-Cu, TB-500), GLP-1 agonists (tirzepatide, semaglutide, retatrutide), and body composition protocols. My scripts currently contain factual errors that weren't caught before production (wrong timelines, uncited claims, outdated trial data).

Research: How do professional science YouTube channels verify their script claims before filming? What automated tools exist for checking PMID/DOI citations, verifying clinical trial data against ClinicalTrials.gov, and fact-checking drug mechanism claims? How do you implement a "research verification gate" that blocks a script from moving to production until all claims are sourced? What are the best practices for citing sources in video descriptions for health content? How do you stay current with rapidly evolving clinical trial data (new Phase 3 readouts, FDA decisions)? What is the regulatory risk of making unsourced health claims on YouTube in Canada and the US? Include a verification checklist template.
```

---

## PROMPT 19 — Multi-Brand Content Production Automation

```
Deep research into automating multi-brand content production for a dual-brand business in 2026. I run two brands under one operation: Keystone Possibilities (construction/project management in British Columbia) and Keystone Recomposition (health protocols, peptides, music). Each brand has its own YouTube channel, website, social media accounts, but shares the same owner (Wayne Stevenson) and infrastructure.

Research: How do professional multi-brand content operations prevent cross-contamination (wrong brand voice, wrong channel upload, wrong social accounts)? What are the best automation architectures for routing content to the correct brand channels? How do you implement brand guardrails that enforce voice/visual consistency per brand? What CMS and publishing tools support multi-brand workflows? How do you manage separate SEO strategies for two brands under one Google Search Console? What are the best practices for brand-specific YouTube channels under one Google account? How do you structure a content calendar that serves both brands without conflicts? Include real multi-brand automation architectures.
```

---

## PROMPT 20 — End-to-End System Integration Testing

```
Deep research into end-to-end integration testing for a complex AI agent system with multiple interconnected components. My system has: a Qdrant vector database (brain), 8 MCP servers, 50+ skill files, a correction journal, a session bootstrap protocol, Chrome browser automation, Google Flow video generation, DaVinci Resolve timeline assembly, WordPress SEO management, YouTube upload automation, and social media publishing. Each component has been built and "tested" individually but the system breaks when components interact.

Research: How do you test integration points between these components? What are the patterns for end-to-end smoke tests that verify the entire pipeline works? How do you implement health dashboards that show real-time status of all components? What are the best observability tools for AI agent systems (logging, tracing, metrics)? How do you implement circuit breakers that prevent cascading failures when one component goes down? How do you create a "system manifest" that documents all components, their dependencies, and their current status? What are the best practices for maintaining complex AI infrastructure as a solo operator? Include a system health check script template.
```

---

## HOW TO USE THESE

1. Open Gemini Pro at gemini.google.com
2. Copy-paste one prompt at a time
3. Click "Deep Research" (if available) or just send as a regular prompt
4. Save each result to `Deep_Research_Results/` in the [[master|Master]] Brain
5. After all 20 are done, I'll ingest the results into the brain and implement the fixes

---

*Wayne runs these. I implement the results. That's the workflow.*


---
📁 **See also:** [[MAP_OF_CONTENTS|← Directory Index]]
