---
id: doc-02skillsimplementationanddocumentation
title: Skills Implementation And Documentation
type: document
summary: 'For: Gemini 3.1 Pro (autonomous execution)'
tags:
- davinci
- document
- keystone-possibilities
- okf
- sea-to-sky
- youtube
created: '2026-06-10T08:22:51.124389'
updated: '2026-06-14T19:57:36.091718'
entities:
- DaVinci
- Keystone Possibilities
- Sea-to-Sky
- YouTube
---

# INSTRUCTION SET 2: Skills Implementation & Documentation System

**Purpose:** Update all skill sets, create missing ones, and build the auto-documentation system.  
**Dependencies:** Instruction Set 01 (Brain Optimization) must be completed first.

---

## CRITICAL CONTEXT

Skills reside in two distinct locations:
1. **Global skills:** `C:\Users\Curtis\.gemini\config\skills\` (loaded for all workspaces)
2. **Workspace skills:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skills\` (loaded for Master Brain only)

Each skill must contain a `SKILL.md` file with the following YAML frontmatter:
```yaml
---
name: skill-name
description: One-line description for registry scanning
---
```

* **Master Brain Coordination:** Manages 13 agents defined in `AGENTS.md` (under the `Agent_Fleet/` directory).
* **Brand Constitution Location:** `Brand_Constitution/`
  * `BRAND_VOICE.md` — Tone and messaging
  * `BRAND_VISUAL.md` — Visual identity
  * `CURRENT_DIRECTION.md` — Strategic priorities

---

## PHASE 1: AUDIT ALL EXISTING SKILLS

### Step 1.1: Global Skills Inventory
Verify the existence and content of the following global skill directories:

| Skill | Purpose |
|---|---|
| `00_keystone_foundation` | Universal foundation, loaded every time |
| `01_chronos_master_brain` | Master orchestrator |
| `02_possibilities_brand` | Construction content pipeline |
| `03_keystone_uploader` | Possibilities YouTube/FB/IG upload |
| `04_keystone_local_seo` | Local SEO for Sea-to-Sky |
| `05_protocol_script_studio` | Health/wellness content (APOLLO engine) |
| `06_protocol_uploader` | Protocol social media upload |
| `07_protocol_brand_awareness` | Protocol PR campaigns |
| `08_music_brand` | Music production pipeline |
| `09_youtube_operations` | YouTube upload + research unified |
| `10_content_pipeline` | End-to-end content orchestrator |
| `11_webmaster` | SEO, landing pages, Knowledge Panel |
| `12_legal_counsel` | Legal matters |
| `13_tax_strategist` | Tax strategies |
| `14_property_scout` | Property/retreat research |
| `15_site_superintendent` | Active job site management |
| `16_research_scout` | Proactive research agent |
| `17_analytics_reporting` | Cross-brand performance reports |
| `18_executive_assistant` | Gmail/Docs management |
| `keystone-session-bootstrap` | Session initialization |
| `keystone-chrome-research-automation` | Chrome Deep Research |
| `keystone-davinci-timeline-assembly` | DaVinci timeline Python scripts |
| `keystone-short-production-pipeline` | Script→Flow→DaVinci→Upload |
| `keystone-overnight-sweep-monitor` | Overnight research monitor |
| `keystone_sovereign_evolution` | DB scrub, cache-bust, watch-page |
| `keystone_instant_indexer` | Google Indexing API push |
| `google-flow-automation` | Chrome automation for Google Flow |
| `upload_quality_gate` | Pre-upload verification |
| `research_verification_gate` | Scientific fact-checking |

### Step 1.2: Workspace Skills Inventory
Verify the existence of workspace skills in:
`c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skills\`

Expected skills:
* `banner-creator`
* `domain-hunter`
* `logo-creator`
* `requesthunt`
* `seo-geo`

### Step 1.3: Quality Verification Checklist
For every skill, ensure:
- [ ] `SKILL.md` exists and is populated.
- [ ] YAML frontmatter contains valid `name` and `description` fields.
- [ ] Description is a single, clear sentence optimized for registry scanning.
- [ ] File paths use correct Windows syntax.
- [ ] MCP tool references match actual registered MCP server tools.

---

## PHASE 2: UPDATE TARGETED SKILLS

### 2.1: `02_possibilities_brand` Update
Integrate the construction pipeline with the following capabilities:
* Reference `keystone-short-production-pipeline` for automated video generation.
* Reference `google-flow-automation` for automated asset generation.
* Reference `seo-geo` for localized blog optimization.
* Update local file paths to align with the revised `Research_Archives` organizational structure.
* Enforce brand voice protocols defined in `Brand_Constitution/possibilities/`.

### 2.2: `11_webmaster` Update (Generative Engine Optimization)
Incorporate key Princeton GEO research findings:
* **Optimization Drivers:** Implement specific citation formatting (cites sources: +40% visibility improvement, inclusion of statistics: +37% improvement).
* **Platform Mapping:** Direct ChatGPT searches to Bing Places, Perplexity queries to Reddit content syndication, and Gemini requests to Google Business Profile (GBP).
* **sameAs Schema:** Standardize deployment of authoritative identifier mapping.
* **Knowledge Graphs:** Establish a process for creating Wikidata entities.
* **Content Loops:** Implement the blog-to-video loop workflow.
* **Reference Directory:** Direct queries to `Research_Archives/08_SEO_Website/`.

### 2.3: `04_keystone_local_seo` Update
* **Citation Pipeline:** Target directory management on HomeStars, Houzz, BBB, RenoQuotes, and Yelp.
* **Bing Places:** Systematize the ownership verification process.
* **Review Targets:** Maintain Google and directory review ratings above the 4.3-star threshold to satisfy conversational AI filtering.
* **GBP Checklist:** Optimize for primary/secondary categories, a highly semantic 750-character description, detailed services, and core attributes.
* **Asset Authenticity:** Use verified, original project photos. Avoid stock or AI-generated imagery to bypass Google Vision AI quality penalties.
* **Review Interaction:** Respond to all customer feedback with contextual, geo-targeted, and project-specific keywords.

### 2.4: `05_protocol_script_studio` Update
* Ensure strict integration with the `research_verification_gate` for health and scientific content.
* Mandate structured medical disclaimers on all outputs.
* Standardize the PubMed indexing and citation workflow.
* Enforce clear AI-disclosure guidelines to comply with YouTube distribution terms.

### 2.5: `09_youtube_operations` Update
* **Competitor Intelligence:** Apply token-optimized formatting for high-speed analysis of competitor channels.
* **Algorithmic Triggers:** Monitor consistency metrics, outlier view magnitudes, and niche-specific performance curves.
* **Timing:** Program script updates based on dynamic competitor upload windows.
* **Shorts Optimization:** Embed current algorithmic best practices for YouTube Shorts (first-frame loops, retention editing).

---

## PHASE 3: CREATE NEW SKILLS

### 3.1: Create `keystone-geo-deployment`
**Location:** `C:\Users\Curtis\.gemini\config\skills\keystone-geo-deployment\SKILL.md`

```yaml
---
name: keystone-geo-deployment
description: Deploy Generative Engine Optimization (GEO) to Keystone websites. Schema markup, sameAs links, FAQ schema, structured data, AI bot access. Use when implementing SEO/GEO changes on live WordPress sites.
---
```

#### Code & Strategic Implementations

##### 1. pre-deployment Checklist
- [ ] Back up the remote database and application state.
- [ ] Verify execution behavior on staging environment.
- [ ] Validate JSON-LD script execution blocks.

##### 2. sameAs Organization Schema Template
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Keystone Possibilities",
  "url": "https://keystonepossibilities.com",
  "logo": "https://keystonepossibilities.com/logo.png",
  "sameAs": [
    "https://www.google.com/maps/place/Keystone+Possibilities",
    "https://www.linkedin.com/company/keystone-possibilities",
    "https://www.facebook.com/keystonepossibilities",
    "https://www.youtube.com/@keystonepossibilities",
    "https://www.wikidata.org/wiki/Q12345678"
  ]
}
```

##### 3. FAQPage Schema Template
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What construction services do you offer in the Sea-to-Sky corridor?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Keystone Possibilities offers custom home building, architectural renovations, and project management services throughout Squamish, Whistler, and Pemberton."
    }
  }]
}
```

##### 4. Robots.txt Whitelist for AI Crawlers
```text
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: anthropic-ai
Allow: /
```

##### 5. WordPress Deployment Procedure
* Inject structured JSON-LD payloads via the theme's header injection utility or a dedicated schema injection plugin. Avoid direct modifications to core files.

##### 6. Verification
* Test active pages using the Google Rich Results Test suite and Schema.org Validator.

---

### 3.2: Create `keystone-client-acquisition`
**Location:** `C:\Users\Curtis\.gemini\config\skills\keystone-client-acquisition\SKILL.md`

```yaml
---
name: keystone-client-acquisition
description: Automated client acquisition for Keystone Possibilities construction. LinkedIn leads, local citations, PR pitching, competitor intelligence. Use when finding new construction clients in Sea-to-Sky corridor.
---
```

#### Core Processes & Integrations
* **Lead Generation:** Use `linkedin_leads.py` to target local property developers and residential clients.
* **Competitor Intelligence:** Run `competitor_intel.py` to identify pipeline opportunities and track active building permits.
* **Citations:** Implement standard profile optimization on HomeStars, Houzz, and BBB.
* **PR Outreach:** Automate standard PR pitching cycles targeting regional design and architecture publications.
* **Reddit Intelligence:** Scan regional subreddits (`r/squamish`, `r/whistler`) for direct service requests and contractor reviews.

---

### 3.3: Create `keystone-self-documentation`
**Location:** `C:\Users\Curtis\.gemini\config\skills\keystone-self-documentation\SKILL.md`

```yaml
---
name: keystone-self-documentation
description: Auto-document new skills, workflows, and learnings into the Master Brain. Use after completing any task to ensure the system remembers what it learned.
---
```

#### When to Use
Execute this workflow immediately following any task that:
* Establishes a new operational process.
* Fixes a critical execution bug or logic failure.
* Creates new assets, scripts, or schemas.

#### Documentation Workflow

##### Step 1: Create Skill File (For New Capabilities)
If the task created a new system capability, compile a `SKILL.md` under:  
`C:\Users\Curtis\.gemini\config\skills\{skill-name}\SKILL.md`

##### Step 2: Append to the Correction Journal
Add any debugged system errors to `.learnings/correction_journal.json`:
```json
{
  "error": "Detailed description of structural or execution error.",
  "fix": "Resolution step applied to repair the logic.",
  "prevention": "Rule to enforce programmatically to avoid regression.",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```

##### Step 3: Vector Ingestion
Use the `ingest_to_brain` MCP tool to save new knowledge blocks:
* **namespace:** Choose the correct operational namespace (e.g., `agent_arch`, `video_prod`, `seo`).
* **metadata:** Set `created_at`, `domain`, and `doc_type`.

##### Step 4: System Integration updates
Update the agent capabilities directory in:  
`c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AGENTS.md`

##### Step 5: Insights Logging
Save a dated summary report inside `.learnings/insights/`.

---

## PHASE 4: BUILD THE SKILL REGISTRY CACHE

### Step 4.1: Construct the Registry File
Create a lightweight JSON cache file for the bootstrap process.

**Location:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skill_registry.json`

```json
{
  "version": "2026-06-10",
  "skills": [
    {
      "name": "keystone-session-bootstrap",
      "location": "global",
      "description": "Auto-loads on every session. Restores context from correction journal, brain, and daily digest.",
      "auto_load": true
    },
    {
      "name": "00_keystone_foundation",
      "location": "global",
      "description": "Universal foundation — brand identity, MCP tools, workspace paths, operating rules.",
      "auto_load": true
    },
    {
      "name": "keystone-geo-deployment",
      "location": "global",
      "description": "Deploy Generative Engine Optimization (GEO) to Keystone websites. Schema markup, sameAs links, FAQ schema, structured data, AI bot access.",
      "auto_load": false
    }
  ]
}
```

### Step 4.2: Registry Compilation Strategy
Programmatically parse all directory paths in global and local skill storage locations, extract the frontmatter fields, and rebuild the `skill_registry.json` file.

### Step 4.3: Ingestion to Vector Store
Ingest the updated `skill_registry.json` payload directly into the active Qdrant vector memory.

---

## PHASE 5: BRAND CONSISTENCY AND RULES

### Step 5.1: Validate Core Assets
Ensure the following reference materials are fully written out and accurate:
* `Brand_Constitution/BRAND_VOICE.md` — Tone profiles:
  * *Keystone Possibilities:* Professional, authoritative, detail-oriented.
  * *Protocol:* Scientific, objective, high trust.
  * *Music:* Creative, visceral, expressive.
* `Brand_Constitution/BRAND_VISUAL.md` — Typography, palette values, rendering styles.
* `Brand_Constitution/CURRENT_DIRECTION.md` — Master schedule and focus targets.

### Step 5.2: Content Generation Brand Safety Gate
All content-producing skills (including `02`, `05`, `07`, `08`, `10`, `11`) must enforce the following validation before generating final outputs:

```markdown
## Brand Compliance Gate
Ensure all content outputs strictly conform to:
- `Brand_Constitution/BRAND_VOICE.md` (Verbal and stylistic constraints)
- `Brand_Constitution/BRAND_VISUAL.md` (Media and asset guidelines)
- `Brand_Constitution/CURRENT_DIRECTION.md` (Contextual strategic priorities)
```

---

## PHASE 6: SYSTEM INTEGRATION MAP

**Location:** `Master_Docs/INTEGRATION_MAP.md`

### MCP Servers
| Server | Execution Path / Command | Protocol | Status |
|---|---|---|---|
| `keystone-brain` | `Qdrant_Brain/keystone_brain_v2_mcp.py` | stdio | Active |
| `youtube-manager` | `youtube_mcp.py` | stdio | Active |
| `youtube-researcher` | `youtube_researcher_mcp.py` | stdio | Active |
| `chrome-devtools-mcp` | `npx chrome-devtools-mcp` | stdio | Active |
| `brave-search` | `npx @modelcontextprotocol/server-brave-search` | stdio | Active |
| `sequential-thinking` | `npx @modelcontextprotocol/server-sequential-thinking` | stdio | Active |

### Docker Infrastructure
| Container Name | Base Image | Public Port | Map Volume / Config |
|---|---|---|---|
| `keystone_qdrant_brain` | `qdrant/qdrant:v1.18.2` | 6333-6334 | `Qdrant_Brain/` (Active Memory) |
| `keystone_qdrant_clone` | `qdrant/qdrant:v1.18.2` | 7333-7334 | Redundant Target (Hot Standby) |

### API & Token Storage
| Channel Name | Auth File Path | Associated Brand Identity |
|---|---|---|
| YouTube Possibilities | `youtube_token_possibilities.json` | Construction / Contracting |
| YouTube OAC | `youtube_token_oac.json` | Recomposition / Audio Portfolio |
| YouTube Protocols | `youtube_token_protocols.json` | Protocol / Longevity Brand |
| Meta API Service | `social_tokens.json` | Universal Channels |

### Host Web Services
| URL | Site Engine | Target Purpose |
|---|---|---|
| `keystonepossibilities.com` | WordPress | Main Business Presence |
| `keystonerecomposition.com` | WordPress | Audio, Health, and Research Portal |

---

## PHASE 7: SYSTEM VERIFICATION

* **Skill Validation:** Parse each updated or created `SKILL.md` file using an automated script to ensure it has valid YAML headers and active local paths.
* **Registry Retrieval Testing:** Query the vector index for a skill category (e.g., "video production pipelines"). Verify that relevant skills are surfaced accurately based on their registry profiles.
* **Logging Changes:** Create a change entry file inside `.learnings/insights/` summarizing the newly deployed skills, schemas, and configurations.

---

## SUCCESS CRITERIA
- [ ] All 29+ active skills have verified, complete `SKILL.md` files.
- [ ] 3 new functional skills created: `keystone-geo-deployment`, `keystone-client-acquisition`, and `keystone-self-documentation`.
- [ ] `skill_registry.json` is compiled and successfully ingested into vector memory.
- [ ] `Brand_Constitution` baseline files are complete.
- [ ] `INTEGRATION_MAP.md` is updated with correct paths, ports, and configuration states.
- [ ] All content workflows run verification checks against the target brand profile.
- [ ] Self-documentation workflow is integrated into the system exit routines.