---
id: doc-02skillsimplementationanddocumentation
title: Skills Implementation And Documentation
type: document
summary: '> For: Gemini 3.1 Pro (autonomous execution)'
entities:
- DaVinci
- Keystone Possibilities
- Sea-to-Sky
- YouTube
created: '2026-06-10T08:22:51.124389'
updated: '2026-06-14T19:57:36.091718'
---
# INSTRUCTION SET 2: Skills Implementation & Documentation System
> **For:** [[GEMINI|Gemini]] 3.1 Pro (autonomous execution)  
> **Created:** 2026-06-10 by Antigravity  
> **Purpose:** Update all [[davinci-resolve-mcp/docs/SKILL|skill]] sets, create missing ones, build auto-documentation system  
> **Estimated Time:** 2-3 hours  
> **Risk Level:** LOW — creating/updating text files only
> **Depends on:** Instruction Set 01 (Brain Optimization) should be done first

---

<!-- CONTEXT: Skills Implementation And Documentation / CRITICAL CONTEXT -->
## CRITICAL CONTEXT

Skills live in TWO locations:
1. **Global skills:** `C:\Users\Curtis\.gemini\config\skills\` (loaded for ALL workspaces)
2. **Workspace skills:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.[[AGENTS|agents]]\skills\` (loaded for [[master|Master]] Brain only)

Every [[davinci-resolve-mcp/docs/SKILL|skill]] has a `[[davinci-resolve-mcp/docs/SKILL|SKILL]].md` file with YAML frontmatter:
```yaml
---
name: skill-name
description: One-line description for registry scanning
---
```

The Master Brain coordinates **13 [[AGENTS|agents]]** defined in `[[AGENTS|AGENTS]].md` (see `Agent_Fleet/` directory).

The **Brand Constitution** is at: `Brand_Constitution/`
- `[[Brand_Constitution/BRAND_VOICE|BRAND_VOICE]].md` — Tone and messaging
- `[[Brand_Constitution/BRAND_VISUAL|BRAND_VISUAL]].md` — Visual [[Brand_Constitution/protocol/IDENTITY|identity]]
- `[[Brand_Constitution/CURRENT_DIRECTION|CURRENT_DIRECTION]].md` — Current strategic priorities

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 1: AUDIT ALL EXISTING SKILLS -->
## PHASE 1: AUDIT ALL EXISTING SKILLS

<!-- CONTEXT: Skills Implementation And Documentation / Step 1.1: Inventory global skills -->
### Step 1.1: Inventory global skills
```bash
dir "C:\Users\Curtis\.gemini\config\skills" /b /ad
```

Expected skills (verify each has a [[davinci-resolve-mcp/docs/SKILL|SKILL]].md and it's not empty):
| [[davinci-resolve-mcp/docs/SKILL|Skill]] | Purpose | Needs Update? |
|-------|---------|---------------|
| `00_keystone_foundation` | Universal foundation, loaded every time | CHECK |
| `01_chronos_master_brain` | Master orchestrator | CHECK |
| `02_possibilities_brand` | Construction content pipeline | CHECK |
| `[[dynamic_skills/03_keystone_uploader|03_keystone_uploader]]` | [[possibilities|Possibilities]] YouTube/FB/IG upload | CHECK |
| `04_keystone_local_seo` | Local SEO for Sea-to-Sky | CHECK |
| `05_protocol_script_studio` | Health/wellness content (APOLLO engine) | CHECK |
| `[[dynamic_skills/06_protocol_uploader|06_protocol_uploader]]` | Protocol social media upload | CHECK |
| `07_protocol_brand_awareness` | Protocol PR campaigns | CHECK |
| `08_music_brand` | [[music|Music]] production pipeline | CHECK |
| `09_youtube_operations` | YouTube upload + research unified | CHECK |
| `10_content_pipeline` | End-to-end content orchestrator | CHECK |
| `11_webmaster` | SEO, landing pages, Knowledge Panel | CHECK |
| `12_legal_counsel` | Legal matters | CHECK |
| `[[dynamic_skills/13_tax_strategist|13_tax_strategist]]` | Tax strategies | CHECK |
| `[[dynamic_skills/14_property_scout|14_property_scout]]` | Property/retreat research | CHECK |
| `15_site_superintendent` | Active job site management | CHECK |
| `16_research_scout` | Proactive research agent | CHECK |
| `17_analytics_reporting` | Cross-brand performance reports | CHECK |
| `18_executive_assistant` | Gmail/Docs management | CHECK |
| `keystone-session-bootstrap` | Session initialization | UPDATING in Set 01 |
| `keystone-chrome-research-automation` | Chrome Deep Research | CHECK |
| `keystone-davinci-timeline-assembly` | DaVinci timeline Python scripts | CHECK |
| `keystone-short-production-pipeline` | Script→Flow→DaVinci→Upload | CHECK |
| `keystone-overnight-sweep-monitor` | Overnight research monitor | CHECK |
| `keystone_sovereign_evolution` | DB scrub, cache-bust, watch-page | CHECK |
| `keystone_instant_indexer` | Google Indexing API push | CHECK |
| `google-flow-automation` | Chrome automation for Google Flow | CHECK |
| `upload_quality_gate` | Pre-upload verification | CHECK |
| `research_verification_gate` | Scientific fact-checking | CHECK |

<!-- CONTEXT: Skills Implementation And Documentation / Step 1.2: Inventory workspace skills -->
### Step 1.2: Inventory workspace skills
```bash
dir "c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.agents\skills" /b /ad
```

Expected: `banner-creator`, `domain-hunter`, `logo-creator`, `requesthunt`, `seo-geo`

<!-- CONTEXT: Skills Implementation And Documentation / Step 1.3: For each [[davinci-resolve-mcp/docs/SKILL|skill]], verify: -->
### Step 1.3: For each [[davinci-resolve-mcp/docs/SKILL|skill]], verify:
- [ ] [[davinci-resolve-mcp/docs/SKILL|SKILL]].md exists and is not empty
- [ ] YAML frontmatter has `name` and `description` fields
- [ ] Description is a single, clear sentence (for registry scanning)
- [ ] Content is accurate and up-to-date
- [ ] References to file paths are correct (Windows paths)
- [ ] MCP tool names match actual MCP server tool names

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 2: UPDATE SKILLS THAT NEED FIXING -->
## PHASE 2: UPDATE SKILLS THAT NEED FIXING

<!-- CONTEXT: Skills Implementation And Documentation / 2.1: Update `02_possibilities_brand` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 2.1: Update `02_possibilities_brand` [[davinci-resolve-mcp/docs/SKILL|skill]]
This [[davinci-resolve-mcp/docs/SKILL|skill]] drives the construction content pipeline. Ensure it includes:
- Reference to `keystone-short-production-pipeline` for video workflows
- Reference to `google-flow-automation` for asset generation
- Reference to `seo-geo` [[davinci-resolve-mcp/docs/SKILL|skill]] for blog post optimization
- Updated file paths for Research_Archives organization
- [[Brand_Constitution/BRAND_VOICE|Brand voice]] reference: `Brand_Constitution/possibilities/`

<!-- CONTEXT: Skills Implementation And Documentation / 2.2: Update `11_webmaster` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 2.2: Update `11_webmaster` [[davinci-resolve-mcp/docs/SKILL|skill]]
This [[davinci-resolve-mcp/docs/SKILL|skill]] handles SEO. It needs to be updated with GEO research findings:
- Add the 9 Princeton GEO methods (cite sources +40%, statistics +37%, etc.)
- Add platform-specific strategies (ChatGPT→Bing Places, Perplexity→Reddit, Gemini→GBP)
- Add sameAs schema deployment instructions
- Add Wikidata entity creation workflow
- Add blog-to-video loop implementation
- Reference `Research_Archives/08_SEO_Website/` for detailed research

<!-- CONTEXT: Skills Implementation And Documentation / 2.3: Update `04_keystone_local_seo` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 2.3: Update `04_keystone_local_seo` [[davinci-resolve-mcp/docs/SKILL|skill]]
Add findings from research:
- Local citation platforms to claim: HomeStars, Houzz, BBB, RenoQuotes, Yelp
- Bing Places claiming process
- Review strategy: aim for 4.3+ stars (ChatGPT threshold)
- GBP optimization: categories, 750-char description, service lists, attributes
- Photo authenticity: use real project photos, NOT stock/AI images (Google Vision AI checks)
- Review response strategy: respond to ALL reviews with specific project details

<!-- CONTEXT: Skills Implementation And Documentation / 2.4: Update `05_protocol_script_studio` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 2.4: Update `05_protocol_script_studio` [[davinci-resolve-mcp/docs/SKILL|skill]]
Ensure it includes:
- `research_verification_gate` integration (mandatory for health content)
- Proper medical disclaimer requirements
- PubMed citation workflow
- AI disclosure requirements for YouTube

<!-- CONTEXT: Skills Implementation And Documentation / 2.5: Update `09_youtube_operations` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 2.5: Update `09_youtube_operations` [[davinci-resolve-mcp/docs/SKILL|skill]]
Add findings from research:
- Token-optimized competitor analysis workflow
- Phase 4 algorithmic ranking (consistency, outlier magnitude, niche performance)
- Upload time optimization based on competitor analysis
- YouTube Shorts 2026 best practices

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 3: CREATE NEW SKILLS THAT DON'T EXIST YET -->
## PHASE 3: CREATE NEW SKILLS THAT DON'T EXIST YET

<!-- CONTEXT: Skills Implementation And Documentation / 3.1: Create `keystone-geo-deployment` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 3.1: Create `keystone-geo-deployment` [[davinci-resolve-mcp/docs/SKILL|skill]]
Location: `C:\Users\Curtis\.gemini\config\skills\keystone-geo-deployment\[[davinci-resolve-mcp/docs/SKILL|SKILL]].md`

This [[davinci-resolve-mcp/docs/SKILL|skill]] handles deploying GEO optimizations to LIVE websites:
```yaml
---
name: keystone-geo-deployment
description: Deploy Generative Engine Optimization (GEO) to Keystone websites. Schema markup, sameAs links, FAQ schema, structured data, AI bot access. Use when implementing SEO/GEO changes on live WordPress sites.
---
```

Content should include:
1. Pre-deployment checklist (backup, staging test)
2. sameAs schema template for Keystone Possibilities:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Keystone Possibilities",
  "url": "https://keystonepossibilities.com",
  "sameAs": [
    "https://www.google.com/maps/place/...",
    "https://www.linkedin.com/company/...",
    "https://www.facebook.com/...",
    "https://www.youtube.com/@...",
    "https://www.wikidata.org/wiki/Q..."
  ]
}
```
3. FAQPage schema template
4. robots.txt AI bot whitelist (GPTBot, PerplexityBot, ClaudeBot, ChatGPT-User, anthropic-ai)
5. WordPress deployment method (header injection vs plugin)
6. Verification steps (Google Rich Results Test, Schema Validator)
7. **SAFETY:** Always test on staging first, never push directly to production

<!-- CONTEXT: Skills Implementation And Documentation / 3.2: Create `keystone-client-acquisition` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 3.2: Create `keystone-client-acquisition` [[davinci-resolve-mcp/docs/SKILL|skill]]
Location: `C:\Users\Curtis\.gemini\config\skills\keystone-client-acquisition\[[davinci-resolve-mcp/docs/SKILL|SKILL]].md`

```yaml
---
name: keystone-client-acquisition
description: Automated client acquisition for Keystone Possibilities construction. LinkedIn leads, local citations, PR pitching, competitor intelligence. Use when finding new construction clients in Sea-to-Sky corridor.
---
```

Content should reference:
- `linkedin_leads.py` script
- `competitor_intel.py` script
- Local citation building checklist (HomeStars, Houzz, BBB, RenoQuotes)
- Automated PR pitching workflow (from `Research_Archives/12_Branding_Marketing/`)
- Reddit competitor intelligence (from `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/09_reddit_competitor_intelligence|09_reddit_competitor_intelligence]].md`)

<!-- CONTEXT: Skills Implementation And Documentation / 3.3: Create `keystone-self-documentation` [[davinci-resolve-mcp/docs/SKILL|skill]] -->
### 3.3: Create `keystone-self-documentation` [[davinci-resolve-mcp/docs/SKILL|skill]]
Location: `C:\Users\Curtis\.gemini\config\skills\keystone-self-documentation\[[davinci-resolve-mcp/docs/SKILL|SKILL]].md`

```yaml
---
name: keystone-self-documentation
description: Auto-document new skills, workflows, and learnings into the Master Brain. Use after completing any task to ensure the system remembers what it learned.
---
```

Content:
```markdown
<!-- CONTEXT: Skills Implementation And Documentation / When to Use -->
## When to Use
After ANY task that:
- Teaches a new workflow
- Discovers a new tool or technique
- Fixes a bug or error
- Creates a new process

<!-- CONTEXT: Skills Implementation And Documentation / Documentation Workflow -->
## Documentation Workflow

<!-- CONTEXT: Skills Implementation And Documentation / Step 1: Create Skill File (if new capability) -->
### Step 1: Create Skill File (if new capability)
If the task created a new capability, create a SKILL.md in:
`C:\Users\Curtis\.gemini\config\skills\{skill-name}\SKILL.md`

<!-- CONTEXT: Skills Implementation And Documentation / Step 2: Update Correction Journal (if error was fixed) -->
### Step 2: Update Correction Journal (if error was fixed)
Add entry to `.learnings/correction_journal.json`:
```json
{
    "error": "what went wrong",
    "fix": "what fixed it",
    "prevention": "how to prevent in future",
    "timestamp": "ISO-8601"
}
```

<!-- CONTEXT: Skills Implementation And Documentation / Step 3: Ingest to Brain -->
### Step 3: Ingest to Brain
Use `ingest_to_brain` MCP tool to add the new knowledge to the vector DB:
- namespace: appropriate category (agent_arch, video_prod, seo, etc.)
- Include metadata: created_at, domain, doc_type

<!-- CONTEXT: Skills Implementation And Documentation / Step 4: Update AGENTS.md -->
### Step 4: Update AGENTS.md
If any agent gained new capabilities, update the agent table in:
`c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AGENTS.md`

<!-- CONTEXT: Skills Implementation And Documentation / Step 5: Log the Learning -->
### Step 5: Log the Learning
Create a dated file in `.learnings/insights/` with a summary.
```

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 4: BUILD THE [[davinci-resolve-mcp/docs/SKILL|SKILL]] REGISTRY CACHE -->
## PHASE 4: BUILD THE [[davinci-resolve-mcp/docs/SKILL|SKILL]] REGISTRY CACHE

<!-- CONTEXT: Skills Implementation And Documentation / Step 4.1: Create a compact [[davinci-resolve-mcp/docs/SKILL|skill]] registry -->
### Step 4.1: Create a compact [[davinci-resolve-mcp/docs/SKILL|skill]] registry
This is a lightweight JSON file that the bootstrap can load quickly to know what skills exist:

Location: `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.[[AGENTS|agents]]\skill_registry.json`

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
    // ... one entry per skill
  ]
}
```

<!-- CONTEXT: Skills Implementation And Documentation / Step 4.2: Populate from scanning all [[davinci-resolve-mcp/docs/SKILL|SKILL]].md files -->
### Step 4.2: Populate from scanning all [[davinci-resolve-mcp/docs/SKILL|SKILL]].md files
Scan both [[davinci-resolve-mcp/docs/SKILL|skill]] directories and extract `name` + `description` from YAML frontmatter.

<!-- CONTEXT: Skills Implementation And Documentation / Step 4.3: Ingest the registry into the brain -->
### Step 4.3: Ingest the registry into the brain
So that any agent can query "what skills do I have for X?" and get relevant answers.

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 5: ENSURE BRAND CONSISTENCY -->
## PHASE 5: ENSURE BRAND CONSISTENCY

<!-- CONTEXT: Skills Implementation And Documentation / Step 5.1: Verify Brand Constitution files are populated -->
### Step 5.1: Verify Brand Constitution files are populated
Read each file in `Brand_Constitution/`:
- `[[Brand_Constitution/BRAND_VOICE|BRAND_VOICE]].md` — Should define tone for each brand (Possibilities=professional/authoritative, Protocol=scientific/trustworthy, Music=creative/emotional)
- `[[Brand_Constitution/BRAND_VISUAL|BRAND_VISUAL]].md` — Colors, logos, typography for each brand
- `[[Brand_Constitution/CURRENT_DIRECTION|CURRENT_DIRECTION]].md` — What Wayne is focused on RIGHT NOW

If any file is empty or outdated, populate it from context in `Master_Docs/`.

<!-- CONTEXT: Skills Implementation And Documentation / Step 5.2: Ensure every content-producing [[davinci-resolve-mcp/docs/SKILL|skill]] references the Brand Constitution -->
### Step 5.2: Ensure every content-producing [[davinci-resolve-mcp/docs/SKILL|skill]] references the Brand Constitution
Skills 02, 05, 07, 08, 10, 11 all produce public content. Each should include:
```markdown
<!-- CONTEXT: Skills Implementation And Documentation / Brand Compliance -->
## Brand Compliance
Before publishing ANY content, verify against:
- `Brand_Constitution/BRAND_VOICE.md` for tone
- `Brand_Constitution/BRAND_VISUAL.md` for visual standards
- `Brand_Constitution/CURRENT_DIRECTION.md` for strategic alignment
```

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 6: DOCUMENT CONNECTION LINKS & INTEGRATIONS -->
## PHASE 6: DOCUMENT CONNECTION LINKS & INTEGRATIONS

<!-- CONTEXT: Skills Implementation And Documentation / Step 6.1: Create/update [[Master_Docs/INTEGRATION_MAP|integration map]] -->
### Step 6.1: Create/update [[Master_Docs/INTEGRATION_MAP|integration map]]
Location: `Master_Docs/[[Master_Docs/INTEGRATION_MAP|INTEGRATION_MAP]].md`

```markdown
# Keystone Integration Map

<!-- CONTEXT: Skills Implementation And Documentation / MCP Servers (Active) -->
## MCP Servers (Active)
| Server | Script | Port/Method | Status |
|--------|--------|-------------|--------|
| keystone-brain | Qdrant_Brain/keystone_brain_v2_mcp.py | stdio | ✅ Active |
| youtube-manager | youtube_mcp.py | stdio | ✅ Active |
| youtube-researcher | youtube_researcher_mcp.py | stdio | ✅ Active |
| chrome-devtools-mcp | npx chrome-devtools-mcp | stdio | ✅ Active |
| brave-search | npx @modelcontextprotocol/server-brave-search | stdio | ✅ Active |
| sequential-thinking | npx @modelcontextprotocol/server-sequential-thinking | stdio | ✅ Active |

<!-- CONTEXT: Skills Implementation And Documentation / Docker Services -->
## Docker Services
| Container | Image | Ports | Volume |
|-----------|-------|-------|--------|
| keystone_qdrant_brain | qdrant/qdrant:v1.18.2 | 6333-6334 | Qdrant_Brain/ |
| keystone_qdrant_clone | qdrant/qdrant:v1.18.2 | 7333-7334 | (backup) |

<!-- CONTEXT: Skills Implementation And Documentation / Token Files -->
## Token Files
| Platform | Token File | Brand |
|----------|-----------|-------|
| YouTube Possibilities | youtube_token_possibilities.json | Construction |
| YouTube OAC | youtube_token_oac.json | Recomposition (shared with Protocol) |
| YouTube Protocols | youtube_token_protocols.json | Protocol channel |
| Meta/Social | social_tokens.json | All brands |

<!-- CONTEXT: Skills Implementation And Documentation / Websites -->
## Websites
| Site | Platform | Purpose |
|------|----------|---------|
| keystonepossibilities.com | WordPress | Construction business |
| keystonerecomposition.com | WordPress | Health/wellness/music |

<!-- CONTEXT: Skills Implementation And Documentation / Google Service Account -->
## Google Service Account
| Purpose | Key Location |
|---------|-------------|
| Indexing API | (find in Master_Brain or document location) |
```

---

<!-- CONTEXT: Skills Implementation And Documentation / PHASE 7: VERIFICATION -->
## PHASE 7: VERIFICATION

<!-- CONTEXT: Skills Implementation And Documentation / Step 7.1: Validate every [[davinci-resolve-mcp/docs/SKILL|skill]] loads without errors -->
### Step 7.1: Validate every [[davinci-resolve-mcp/docs/SKILL|skill]] loads without errors
For each [[davinci-resolve-mcp/docs/SKILL|skill]], verify the [[davinci-resolve-mcp/docs/SKILL|SKILL]].md parses correctly:
- Valid YAML frontmatter
- No broken file references
- No references to deleted/moved files

<!-- CONTEXT: Skills Implementation And Documentation / Step 7.2: Test [[davinci-resolve-mcp/docs/SKILL|skill]] registry -->
### Step 7.2: Test [[davinci-resolve-mcp/docs/SKILL|skill]] registry
Query the brain: "what skills do I have for video production?"
Expected: Returns `keystone-short-production-pipeline`, `google-flow-automation`, `keystone-davinci-timeline-assembly`

<!-- CONTEXT: Skills Implementation And Documentation / Step 7.3: Document all changes -->
### Step 7.3: Document all changes
Create a change log entry in `.learnings/insights/` summarizing what was updated.

---

<!-- CONTEXT: Skills Implementation And Documentation / SUCCESS CRITERIA -->
## SUCCESS CRITERIA
- [ ] All 29+ skills verified with valid [[davinci-resolve-mcp/docs/SKILL|SKILL]].md
- [ ] 3 new skills created (geo-deployment, client-acquisition, self-documentation)
- [ ] [[davinci-resolve-mcp/docs/SKILL|Skill]] registry cache created and ingested to brain
- [ ] Brand Constitution verified complete
- [ ] [[Master_Docs/INTEGRATION_MAP|Integration map]] created/updated
- [ ] All content-producing skills reference Brand Constitution
- [ ] Self-documentation workflow established


---
📁 **See also:** [[Master_Docs/Gemini_Pro_Instructions/INDEX|← Directory Index]]
