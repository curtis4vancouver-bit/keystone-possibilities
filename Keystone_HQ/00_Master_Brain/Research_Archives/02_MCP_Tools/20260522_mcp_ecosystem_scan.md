# MCP Ecosystem Scan - May 2026

**Research Date:** May 22, 2026  
**Domain:** mcp_ecosystem  
**Researcher:** Keystone Sovereign Overnight Research Agent  

---

## 1. MCP Server Directories and Marketplaces

There is no single official "app store" for MCP servers. Discovery is distributed across several platforms:

| Platform | URL | Description |
|----------|-----|-------------|
| **Glama.ai** | glama.ai | Comprehensive MCP server metadata and integrations |
| **MCPMarket.com** | mcpmarket.com | Community-curated marketplace, thousands of servers |
| **Smithery** | smithery.ai | Major index with ranking by activity and reliability |
| **PulseMCP** | pulsemcp.com | Server index with ranking and stats |
| **mcpservers.org** | mcpservers.org | Searchable directory with categories |
| **mcp.so** | mcp.so | Discovery hub for MCP tools |
| **Awesome-MCP-Servers** | github.com/punkpeye/awesome-mcp-servers | Community-maintained GitHub list, primary starting point |
| **Official MCP Registry** | modelcontextprotocol.io | Technical REST API for programmatic discovery |

**Enterprise Solutions:** JFrog offers an AI Catalog that acts as a supply chain firewall, managing internal private servers with RBAC and verification.

---

## 2. Top 20 Most Popular/Useful MCP Servers (May 2026)

The ecosystem has over **14,000 servers** available. Here are the most essential:

### Tier 1 - Must-Have (Highest Adoption)

| # | Server | Package/Source | What It Does |
|---|--------|---------------|--------------|
| 1 | **Context7** | npm | Fetches up-to-date, version-specific library docs; prevents LLM hallucinations |
| 2 | **GitHub MCP** | npm: `@modelcontextprotocol/server-github` | Manage repos, PRs, issues, trigger Actions workflows |
| 3 | **Playwright MCP** | npm: `@anthropic/mcp-playwright` | Browser automation - navigate, click, fill forms, extract data |
| 4 | **Filesystem MCP** | npm: `@modelcontextprotocol/server-filesystem` | Secure local file reading, writing, directory management |
| 5 | **Brave Search MCP** | npm: `@anthropic/mcp-brave-search` | Real-time web search capabilities for [[AGENTS|agents]] |
| 6 | **PostgreSQL/Supabase** | npm/pip | Database schema inspection, SQL queries, RLS support |

### Tier 2 - High Value

| # | Server | What It Does |
|---|--------|--------------|
| 7 | **Notion MCP** | Read/write Notion pages and databases |
| 8 | **Slack MCP** | Search channels, send messages, team collaboration |
| 9 | **Docker MCP** | Container lifecycle management, build/tag/push images |
| 10 | **MongoDB MCP** | Natural language queries for MongoDB collections |
| 11 | **Google Workspace MCP** | Gmail, Calendar, Drive, Docs, Sheets in one package |
| 12 | **Firecrawl / Jina Reader** | Convert URLs to clean LLM-friendly markdown |
| 13 | **Tavily MCP** | Alternative web search with structured results |

### Tier 3 - Specialized

| # | Server | What It Does |
|---|--------|--------------|
| 14 | **Grafana/Prometheus** | Query metrics, dashboards, system health monitoring |
| 15 | **PagerDuty MCP** | AI triage alerts, manage on-call schedules |
| 16 | **Zapier MCP** | Connect to Zapier's 7000+ app integrations |
| 17 | **DaVinci Resolve MCP** | Video editing automation via Python Scripting API |
| 18 | **YouTube Uploader MCP** | Upload, schedule, manage video metadata |
| 19 | **Ayrshare Social MCP** | Multi-platform social media posting (13+ platforms) |
| 20 | **Azure MCP** | Integration with 40+ Azure services |

---

## 3. Social Media Automation MCP Servers

### Comprehensive Multi-Platform Solutions

**Ayrshare MCP Server**
- Supports 13+ platforms: TikTok, Instagram, Facebook, LinkedIn, X/Twitter, YouTube
- Features: scheduling, AI-powered content generation, analytics
- Best for: multi-platform content management

**Outstand MCP Server** (outstand.so)
- 25+ tools across 10 platforms including Facebook, Instagram, TikTok, X, LinkedIn
- Features: cross-platform posting, on-demand analytics, media management

**PostProxy MCP** (postproxy.dev)
- Social media scheduling and management
- OAuth-based authentication

### Ad-Focused Solutions

**Pipeboard MCP** (pipeboard.co)
- Meta Ads (Facebook/Instagram), TikTok Ads, Google Ads
- AI-powered campaign analysis, bid optimization, spend management

### Key Social Media Capabilities via MCP
- Content creation (captions, hashtags, brand voice)
- Automated scheduling across multiple platforms
- Analytics and engagement tracking
- Community engagement management (draft/post replies)

---

## 4. File Management, Database, Email, and Calendar MCP Servers

### File Management
- **Filesystem MCP** (Official): Secure scoped file access (read/write/directory)
- **Google Drive MCP**: Cloud file management via Google Workspace

### Database
- **PostgreSQL MCP**: Full SQL query support, schema inspection
- **Supabase MCP**: PostgreSQL with Row Level Security
- **MongoDB MCP**: Natural language queries, schema operations
- **Vectara MCP**: Semantic search and RAG workflows

### Email
- **Google Workspace MCP**: Gmail reading, searching (advanced queries), drafting, replying, archiving, attachments
- **Outlook MCP**: Windows-based local calendar management, expanding to full 365 coverage
- Setup requires: Google Cloud project, OAuth 2.0 credentials, API enablement

### Calendar
- **Google Calendar MCP**: List calendars, retrieve events, check availability, create/update events, manage attendees
- **Outlook Calendar MCP**: View and manage local Outlook calendar
- Workflow chaining: "Schedule a meeting, create a shared Google Doc, and send a confirmation email"

---

## 5. Video Editing / DaVinci Resolve MCP Servers

Three notable implementations exist:

### davinci-resolve-mcp (samuelgursky)
- GitHub: github.com/samuelgursky/davinci-resolve-mcp
- Full API coverage with guarded workflow helpers
- Local control panel included
- Most widely cited implementation

### apvlv/davinci-resolve-mcp
- Focus on project, timeline, and Fusion operations
- Robust implementation

### LobeHub/ResolveMCP
- Extensive tool definitions for Resolve 20
- Specific support for color grading, rendering, and Fusion

### Capabilities
- Project and Timeline management (create, load, save, switch)
- Media Pool operations (import, organize bins)
- Color grading, Fusion node chains
- Page navigation (Edit, Color, Fusion, Deliver)
- Render/export triggering
- Custom Python/Lua script execution

### Requirements
- DaVinci Resolve Studio (scripting API required)
- Preferences > General > External scripting using > Local
- Python installed on system
- Resolve must be running on same machine as MCP server

---

## 6. Antigravity Community Skills and Plugins

### Discovery Methods
There is no centralized "app store" for Antigravity skills. The ecosystem relies on:

- **Community GitHub Repos**: Search for "antigravity skills" or "gemini cli extensions"
  - Example: `rmyndharis/antigravity-skills` (hundreds of specialized skills)
- **CLI Installation**: `gemini skills install <github-url>` or `gemini extensions install <github-url>`
- **Built-in Plugins**: Browse via Customizations page in Antigravity UI

### Skill Structure
```
skill_folder/
  SKILL.md          # Main instruction file (YAML frontmatter + markdown)
  scripts/          # Helper scripts
  examples/         # Reference implementations
  resources/        # Templates, assets
  references/       # Additional documentation
```

### Scope Levels
- **Workspace**: `<workspace-root>/.agent/skills/` or `.[[AGENTS|agents]]/plugins/`
- **Global**: `~/.gemini/antigravity/skills/` or `~/.gemini/config/plugins/`

### Documentation
- Official: antigravity.google
- Commands: `/skills list` or `gemini skills list` to see active skills

---

## 7. Building Custom MCP Servers with FastMCP (Python)

### Installation
```bash
uv pip install fastmcp
# or
pip install fastmcp
```

### Minimal Server Example
```python
from fastmcp import FastMCP

mcp = FastMCP("My Construction MCP Server")

@mcp.tool()
def calculate_material_cost(material: str, quantity: float, unit_price: float) -> float:
    """Calculate total cost for construction materials."""
    return quantity * unit_price

@mcp.resource("project://{project_id}")
def get_project_info(project_id: str) -> str:
    """Get project details by ID."""
    return f"Project {project_id} details here"

if __name__ == "__main__":
    mcp.run()
```

### Running and Testing
```bash
# Run the server
fastmcp run server.py

# Test with MCP Inspector (web UI)
fastmcp dev server.py
```

### Key Features (FastMCP 3.0+, 2026)
- Decorator-based API (`@mcp.tool()`, `@mcp.resource()`)
- Automatic Pydantic schema generation and input validation
- Transport flexibility: `stdio` (local) and `HTTP` (remote)
- Convert FastAPI apps to MCP: `from_fastapi()`
- Component versioning
- Granular authorization
- OpenTelemetry instrumentation for production monitoring

### Official Python SDK
- Package: `mcp` on PyPI
- Latest Version: 1.27.1 (May 8, 2026)
- Supports: stdio, SSE, Streamable HTTP transports
- Documentation: gofastmcp.com

---

## 8. MCP Protocol Version Updates and New Capabilities (2026)

The protocol is now governed by the **Linux Foundation's Agentic AI Foundation (AAIF)** since late 2025. Rather than monolithic version numbers, improvements come via **Spec Enhancement Proposals (SEPs)**.

### 2026 Roadmap Priorities

| Capability | Description |
|-----------|-------------|
| **Stateless Streamable HTTP** | Operates behind load balancers without sticky sessions; enables horizontal scaling |
| **Scalable Session Handling** | Create, resume, migrate sessions transparently during server restarts |
| **MCP Server Cards** | `.well-known` URLs for structured server metadata; enables registry discovery without live connections |
| **Asynchronous Tasks** | Long-running operations where [[AGENTS|agents]] launch work and retrieve results later |
| **Agent-to-Agent Communication** | Multi-agent patterns with "skills" as multi-tool workflow abstractions |
| **Elicitation** | Servers can pause execution to request additional user input via the client |

### Current Specification
- Significant milestone: Version 2025-11-25
- Protocol version negotiated during handshake via `MCP-Protocol-Version` header
- Backward compatible by design

---

## 9. Security Considerations for MCP Servers

The **NSA has issued guidance** on MCP security risks. Key concerns as of 2026:

### Critical Risks
1. **Prompt Injection / Tool Abuse**: Malicious inputs manipulate [[AGENTS|agents]] into unintended tool calls
2. **Confused Deputy Vulnerabilities**: Servers execute with broad service privileges instead of user-specific permissions
3. **Supply Chain Attacks**: Typosquatting, dependency confusion in community-built servers (similar to malicious npm/PyPI packages)
4. **Credential Sprawl**: API keys exposed via environment variables, logs, or unshielded local caches
5. **Missing Auth/AuthZ**: Many servers lack authentication or granular RBAC
6. **Lateral Movement**: Compromised server provides path to deeper internal systems

### Best Practices (Zero Trust Approach)
- **Authentication**: OAuth 2.1 with PKCE for remote servers; verify caller identity on every request
- **Least Privilege**: Workflow-scoped permissions; avoid broad static service identities
- **Sandboxing**: Run servers in containers/chroot jails; limit filesystem access
- **Human-in-the-Loop**: Require explicit user approval for destructive operations (write_file, execute_command)
- **Transport Security**: TLS 1.2+ for remote connections; mTLS for inter-server communication
- **Audit Trails**: Centralized logging for all MCP interactions
- **Gateway Pattern**: Route MCP traffic through a dedicated gateway for policy enforcement

---

## 10. MCP Servers for Construction Business and YouTube Operations

### Construction-Specific Opportunities

**BIM Validation MCP**
- AI can connect to BIM data to scan for clashes or invalid elements
- Autodesk is building public MCP servers for Construction Cloud

**Document and Spec Review**
- [[AGENTS|Agents]] can parse hundreds of pages of project specifications and drawings
- Extract actionable information in minutes instead of hours

**Unified Data Access**
- Connect Procore, Autodesk Construction Cloud, and local files into shared AI context

**Custom Construction MCP Ideas (Build with FastMCP)**
- Material cost calculators
- Project timeline trackers
- Safety checklist automation
- RFI tracking and status updates
- Subcontractor bid comparison tools

### YouTube Operations

**YouTube Uploader MCP** (youtube-uploader-mcp)
- OAuth2 authentication (secure, no secrets shared with LLMs)
- AI-generated titles, descriptions, tags before upload
- Scheduling and bulk upload support
- Multi-channel management
- **Important**: YouTube Data API v3 has a default quota of 10,000 units/day

**YouTube Transcript MCP**
- Extract video transcripts for content repurposing
- Read-only access for analytics

**Integration via Zapier MCP**
- Pre-built YouTube actions: "Upload Video", "Add to Playlist"
- Connect to 7000+ other apps for workflow automation

### Recommended Automation Stack for Keystone
1. **Ayrshare MCP** - Multi-platform social posting (TikTok, Instagram, YouTube, Facebook)
2. **YouTube Uploader MCP** - Direct video upload and scheduling
3. **Google Workspace MCP** - Email, Calendar, Drive for business operations
4. **DaVinci Resolve MCP** - AI-assisted video editing
5. **Custom FastMCP Server** - Construction-specific tools (estimates, project tracking)

---

## Installation Priority Matrix

| Priority | MCP Server | Install Method | Immediate Value |
|----------|-----------|---------------|-----------------|
| **P0** | Google Workspace MCP | npm/pip + OAuth setup | Email, calendar, document automation |
| **P0** | Ayrshare Social MCP | npm + API key | Multi-platform social media posting |
| **P1** | YouTube Uploader MCP | pip + Google Cloud OAuth | Video upload and scheduling |
| **P1** | DaVinci Resolve MCP | pip + Resolve Studio | AI-assisted video editing |
| **P2** | Playwright MCP | npm | Browser automation for research |
| **P2** | Context7 | npm | Accurate developer documentation |
| **P3** | Custom FastMCP Server | pip install fastmcp | Construction business tools |

---

## Sources Consulted
- modelcontextprotocol.io (Official MCP documentation)
- github.com/punkpeye/awesome-mcp-servers
- mcpservers.org
- glama.ai
- mcp.so
- PyPI (mcp package v1.27.1)
- npm registry (MCP server packages)
- gofastmcp.com (FastMCP documentation)
- NSA MCP security guidance (nsa.gov)
- Ayrshare, Outstand, Pipeboard documentation
- github.com/samuelgursky/davinci-resolve-mcp
- antigravity.google (Antigravity platform docs)
- Various Medium, dev.to, and community articles

---

*Report generated by Keystone Sovereign Research Agent, May 22, 2026*


---
📁 **See also:** ← Directory Index
