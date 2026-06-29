# THE KEYSTONE AUTONOMOUS ENTERPRISE: MASTER ROADMAP
> Last updated: 2026-06-10 | Audit sweep by Chronos Master Brain

This roadmap outlines the complete architecture required to transition Keystone from a human-operated entity to a fully automated, multi-silo AI enterprise.

## 1. Core Infrastructure & File Management
- [x] **The "Brain" (Vector Memory):** Qdrant vector DB operational — 28 namespaces, ~14K+ vectors, hybrid search (BGE-small + Splade). Docker containers running (6333-6334 primary, 7333-7334 backup). *Self-Healing Note: Supabase/PostgreSQL was replaced with Qdrant to improve speed and vector operations.*
- [x] **Enterprise File Management System:** Master Brain directory structure established. Agent Fleet (13 agents), Brand Constitution, Research Archives, and Skill Vault all organized.
- [ ] **Windows OS Hardening:** `windows_concurrency_tune.ps1` script. *(NOT STARTED — requires manual admin execution)*

## 2. Custom Agentic Tools (MCP Integrations)
- [x] **DaVinci Resolve Assembly MCP:** `davinci-resolve-mcp` installed with 328 granular tools (timeline, media_pool, project, gallery, graph). Wired in `mcp_config.json`.
- [x] **Google Workspace MCP:** `google-workspace-mcp` (v2.3.6) wired in `mcp_config.json`. Covers Gmail, Docs, Drive, Calendar, Sheets, Slides, Forms. *(NEEDS: OAuth completion by running `npx google-workspace-mcp accounts add keystone`)*
- [x] **Content Engine MCP:** `content_engine_mcp.py` (8 tools) wired in `mcp_config.json` — managing empire status, SEO keyword audits, cross-linking, and content calendars.
- [x] **Google Deep Research:** `overnight_research_daemon.py` with credit management (30 prompts/5hr window) and sweep/chrome-research automation skills. *(Self-Healing Note: Replaced gemini_web_researcher.py for better rate-limit handling)*
- [x] **YouTube MCPs:** `youtube-manager` + `youtube-researcher` wired with 3-channel token routing (possibilities, protocols, recomposition/oac).
- [x] **Keystone Brain MCP:** `keystone_brain_v2_mcp.py` with search, list, ingest, list_sources, and delete_namespace tools.
- [x] **Google Flow Automation:** `google-flow-automation` skill with full UI architecture, snapshot strategy, and Veo 3.1 parameters.
- [x] **Spark Drive Bridge:** `drive_bridge.py` syncs Spark output from Google Drive → Qdrant brain with namespace routing.
- [ ] **Suno AI Music MCP:** Build custom API integrations to generate and download Deep House tracks programmatically. *(NOT STARTED)*
- [ ] **TooLost Distribution MCP:** Automate the packaging and distribution of the Keystone Recomposition discography to Spotify/Apple Music. *(NOT STARTED)*

## 3. The Autonomous Social & Ad Machine
- [x] **Social Media Multi-Poster:** `social_publisher.py` + `social_oauth_manager.py` built for multi-platform publishing. Protocol brand routing through Recomposition tokens is set up.
- [ ] **Free Classifieds Automation:** Craigslist and Facebook Marketplace Playwright scripts with ghost-cursor technology. *(NOT STARTED)*
- [/] **PM Advertising & Local SEO:** `04_keystone_local_seo` skill built. GMB optimization and citation building for Sea-to-Sky corridor. *(PARTIAL — skill exists, automation loop inactive)*

## 4. Multi-Silo YouTube Management
- [x] **Keystone Possibilities (Construction):** YouTube upload automation via `youtube-manager` MCP. Script packages operational via Google Flow automation.
- [x] **Keystone Protocols (Health):** Upload, Flow prompts, and DaVinci assembly skills fully in place.
- [/] **Keystone Recomposition (Music):** Upload automation completed. Music production pipeline (`08_music_brand` skill) operational. Visualizer generation and playlist management still partial. *(PARTIAL)*

## 5. Self-Evolution & Memory
- [x] **Self-Evolution Engine:** `self_evolution.py` operational with circuit breaker, error recording, correction journal, and daily health scoring.
- [x] **Dream Engine:** `dream_engine.py` manages Ebbinghaus memory consolidation, scoring, and pruning.
- [x] **Security Sandbox:** `security_sandbox.py` enforces AST-level code validation and dangerous import blocking.
- [x] **Session Bootstrap:** `keystone-session-bootstrap` skill automatically loads the correction journal, prevention rules, active projects, and production skills on every new session init.
- [x] **Prompt Refiner:** `prompt_refiner.py` automatically generates prevention rules directly from the correction journal.