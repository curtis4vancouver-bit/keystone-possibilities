---
name: 00_mcp_tool_reference
description: "Master reference for all 6 MCP servers and 42+ tools available to Keystone agents. Every agent MUST read this to understand what tools exist and how to call them."
---

# MCP Tool Reference — [[master|Master]] [[davinci-resolve-mcp/docs/SKILL|Skill]] Document

This is the canonical reference for every MCP tool available in the Keystone [[ARCHITECTURE|architecture]]. All [[AGENTS|agents]] must understand this before executing tasks.

---

## Server 1: keystone-brain (3 tools)
**Purpose:** Vector memory database. The empire's persistent brain across all conversations.

| Tool | What It Does | When To Use |
|------|-------------|-------------|
| `search_master_brain` | Semantic + keyword hybrid search across 4,027 chunks / 159 sources | FIRST thing on every task — check what the brain already knows before doing anything |
| `ingest_to_brain` | Save new knowledge (auto-chunks content > 1000 chars) | After discovering valuable research, making strategic decisions, or completing analysis |
| `list_brain_sources` | Lists all stored sources with chunk counts | Before large ingestions to avoid duplicates |

**How to call:** `call_mcp_tool(ServerName="keystone-brain", ToolName="search_master_brain", Arguments={"query": "your search", "limit": 5})`

**Best Practices:**
- Always search brain BEFORE running brave_web_search
- Use multiple targeted queries, not one vague query
- Use descriptive source names when ingesting: `deep_research/topic_date`, `agent_session/date`, `strategy/plan_name`

---

## Server 2: brave-search (2 tools)
**Purpose:** Live web search for current information, news, competitor intelligence, and documentation.

| Tool | What It Does | When To Use |
|------|-------------|-------------|
| `brave_web_search` | [[general|General]] web search — news, docs, market research (max 20 results) | When brain doesn't have the answer and you need current web data |
| `brave_local_search` | Local business search by geographic area | Competitor intelligence in Sea-to-Sky corridor, finding local contractors/suppliers |

**How to call:** `call_mcp_tool(ServerName="brave-search", ToolName="brave_web_search", Arguments={"query": "your search query"})`

**Best Practices:**
- Always check brain first — then search web
- Break complex research into multiple focused queries
- Ingest valuable web findings into the brain so they're not lost
- For competitors: search by service type + location (e.g., "custom home builder Squamish BC")

---

## Server 3: chrome-devtools-mcp (29 tools)
**Purpose:** Full Chrome browser automation — navigate, click, fill forms, screenshot, audit, and scrape web pages.

### Navigation & Inspection
| Tool | What It Does |
|------|-------------|
| `list_pages` | Find open pages/tabs |
| `select_page` | Switch to a specific tab |
| `new_page` | Open a new browser tab |
| `close_page` | Close a tab (always clean up!) |
| `navigate_page` | Load a URL |
| `take_snapshot` | Get the DOM tree for structure analysis |
| `take_screenshot` | Visual screenshot for QA/verification |
| `wait_for` | Wait for async content to load before interacting |

### Interaction & Automation
| Tool | What It Does |
|------|-------------|
| `click` | Click an element by CSS selector |
| `fill` | Fill a single input field |
| `fill_form` | Fill multiple form fields at once |
| `type_text` | Type character by character (for inputs with event listeners) |
| `press_key` | Simulate keyboard keys (Enter, Tab, Escape) |
| `hover` | Trigger hover states for dropdowns/tooltips |
| `drag` | Drag and drop |
| `upload_file` | Upload files to file inputs |
| `handle_dialog` | Accept/dismiss browser dialogs |

### Auditing & Performance
| Tool | What It Does |
|------|-------------|
| `lighthouse_audit` | Run Lighthouse for performance/SEO/accessibility scores |
| `performance_start_trace` | Start a performance trace |
| `performance_stop_trace` | Stop and save trace |
| `performance_analyze_insight` | Get actionable performance insights |
| `take_memory_snapshot` | Diagnose memory leaks |

### Scripting & Debugging
| Tool | What It Does |
|------|-------------|
| `evaluate_script` | Run arbitrary JavaScript on the page |
| `list_console_messages` | Read console output |
| `get_console_message` | Get a specific console message |
| `list_network_requests` | Inspect API calls and responses |
| `get_network_request` | Get a specific network request details |

### Device Emulation
| Tool | What It Does |
|------|-------------|
| `emulate` | Emulate mobile devices for responsive testing |
| `resize_page` | Set custom viewport dimensions |

**Workflow:** Always: `list_pages` → `select_page` → do work → `close_page`
**Best Practice:** Always `wait_for` after navigation. Use `take_screenshot` liberally to verify visual [[STATE|state]].

---

## Server 4: keystone_multiplexer (5 gateway tools → 12 sub-[[AGENTS|agents]])
**Purpose:** Gateway to 12 specialized backend [[AGENTS|agents]] that handle YouTube, Google Workspace, DaVinci Resolve, [[music|music]] production, and more.

### Gateway Tools
| Tool | What It Does |
|------|-------------|
| `mcp_multiplexer_execute_tool` | Execute a tool on a specific sub-agent |
| `mcp_multiplexer_list_agents` | List all available sub-[[AGENTS|agents]] |
| `mcp_multiplexer_list_all_tools` | List all tools for a specific agent |
| `mcp_multiplexer_refresh_tool_cache` | Refresh after config changes |
| `mcp_multiplexer_reset_all_agents` | Emergency restart all sub-[[AGENTS|agents]] |

**How to call:** `call_mcp_tool(ServerName="keystone_multiplexer", ToolName="mcp_multiplexer_execute_tool", Arguments={"agent": "youtube_manager", "tool": "upload_video", "args": {...}})`

### The 12 Sub-[[AGENTS|Agents]]
| Sub-Agent | Purpose | Key Tools |
|-----------|---------|-----------|
| `search_console` | Google Search Console data | Performance reports, keyword data, indexing status |
| `google_workspace` | Gmail, Drive, Calendar, Docs | Send emails, manage calendar, read/write docs |
| `gemini_web_researcher` | Multi-threaded browser research | Deep research via [[GEMINI|Gemini]] proxy |
| `youtube_manager` | YouTube channel management | Upload videos, update metadata, manage playlists |
| `youtube_researcher` | YouTube analytics & research | Channel stats, video performance, competitor analysis |
| `content_engine` | Content creation pipelines | Script compilation, content queue management |
| `davinci_resolve` | Video editing automation | Timeline assembly, render queue, color grading |
| `music_production` | Music/audio production | DAW commands, stem mixing, album packaging |
| `health` | Health tracking & analysis | Biometric data, protocol tracking |
| `dev` | Development & coding | Code generation, build scripts, testing |
| `research` | General research & synthesis | Deep research, report generation |
| `dynamic_skills` | Runtime [[davinci-resolve-mcp/docs/SKILL|skill]] [[hot|hot]]-loading | Load/execute dynamic Python skills |

**Best Practice:** Always `list_agents` first to confirm an agent is online, then `list_all_tools` to see what it can do before calling `execute_tool`.

---

## Server 5: postgres (1 tool)
**Purpose:** Direct SQL access to the Keystone [[possibilities|Possibilities]] PWA database (construction project tracker).

| Tool | What It Does |
|------|-------------|
| `query` | Execute SQL queries against the PWA PostgreSQL database |

**Known Tables:** `projects`, `tasks`, `users`, `budgets`, `timelines`

**Safety Rules:**
- NEVER DROP tables
- Always SELECT first to understand schema
- Use WHERE clauses on all UPDATEs
- LIMIT exploratory queries
- Use transactions for multi-step operations

**Note:** The Supabase Docker containers have been shut down. This tool connects to the PWA database, NOT the vector brain. The vector brain runs on SQLite-vec locally.

---

## Server 6: sequential-thinking (1 tool)
**Purpose:** Structured multi-step reasoning for complex decisions, architecture planning, and strategic analysis.

| Tool | What It Does |
|------|-------------|
| `sequentialthinking` | Break problems into numbered reasoning steps with branching and revision |

**When to use:**
- ✅ Complex multi-step planning, architecture decisions, strategic analysis, debugging with multiple root causes, weighing tradeoffs
- ❌ Simple lookups, single-step operations, obvious answers

**Power combo:** `search_master_brain` (load context) → `sequentialthinking` (analyze) → `ingest_to_brain` (save decision)

---

## Agent-to-MCP Wiring Guide

| Agent | brain | brave | chrome | multiplexer | postgres | sequential |
|-------|-------|-------|--------|-------------|----------|------------|
| 01 Chronos | ✅ ALL | ✅ ALL | ✅ ALL | ✅ ALL 12 [[AGENTS|agents]] | ✅ | ✅ |
| 02 Possibilities | ✅ search+ingest | ❌ | ❌ | content_engine, youtube_researcher, research | ❌ | ✅ |
| [[dynamic_skills/03_keystone_uploader|03 Keystone Uploader]] | ✅ search | ❌ | ❌ | youtube_manager, google_workspace | ❌ | ❌ |
| 04 Local SEO | ✅ search+ingest | ✅ ALL | ❌ | search_console, google_workspace | ❌ | ✅ |
| [[dynamic_skills/05_youtube_protocol|05 YouTube Protocol]] | ✅ search+ingest | ❌ | ❌ | youtube_researcher, content_engine, research | ❌ | ✅ |
| [[dynamic_skills/06_protocol_uploader|06 Protocol Uploader]] | ✅ search | ❌ | ❌ | youtube_manager, google_workspace | ❌ | ❌ |
| 07 Brand Awareness | ✅ search+ingest | ✅ ALL | ❌ | search_console, research, google_workspace | ❌ | ✅ |
| [[dynamic_skills/08_music_creator|08 Music Creator]] | ✅ search+ingest | ❌ | ❌ | music_production, davinci_resolve, content_engine | ❌ | ✅ |
| [[dynamic_skills/09_music_uploader|09 Music Uploader]] | ✅ search | ❌ | ❌ | youtube_manager, google_workspace | ❌ | ❌ |
| [[dynamic_skills/10_music_awareness|10 Music Awareness]] | ✅ search+ingest | ✅ ALL | ❌ | search_console, research | ❌ | ✅ |
| 11 Website Branding | ✅ search+ingest | ❌ | ✅ lighthouse+screenshot | dev, content_engine, search_console | ❌ | ✅ |
| 12 Legal Counsel | ✅ search+ingest | ✅ ALL | ❌ | research, google_workspace | ❌ | ✅ |
| [[dynamic_skills/13_tax_strategist|13 Tax Strategist]] | ✅ search+ingest | ✅ ALL | ❌ | research, google_workspace | ✅ | ✅ |
| [[dynamic_skills/14_property_scout|14 Property Scout]] | ✅ search+ingest | ✅ ALL | ✅ navigation+screenshot | research, gemini_web_researcher | ❌ | ✅ |
| 15 Site Superintendent | ✅ search+ingest | ❌ | ❌ | dev, research | ❌ | ✅ |


---
📁 **See also:** [[dynamic_skills/INDEX|← Directory Index]]
