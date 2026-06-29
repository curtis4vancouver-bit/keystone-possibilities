# Keystone Fleet Architecture — Deployment Summary

**Deployed:** 2026-05-28  
**Last Updated:** 2026-06-14  
**Entities:** DaVinci Resolve, YouTube, Spark Bridge

---

### Agent Fleet (13 Agents)
All agents have dedicated silo folders located at `Agent_Fleet/{agent_name}/` featuring standard tracking schemas:
- `STATE.json` (status, outputs, claimed topics)
- `CAPABILITIES.json` (skills, APIs, strengths)
- `OUTPUT_LOG.jsonl` (production history)
- `INBOX.json` (messages from Master Brain)

**Deployed Agent Fleet:**
* `chronos_master`
* `possibilities_brand`
* `protocol_brand`
* `music_brand`
* `recomposition_music`
* `webmaster`
* `analytics_reporting`
* `legal_counsel`
* `tax_strategist`
* `site_superintendent`
* `research_scout`
* `executive_assistant`
* `local_seo`

---

### Fleet Orchestrator
Use the orchestrator script to manage cross-agent workloads and task assertions:
- **Full System Scan:** `python fleet_orchestrator.py --sweep`
- **Live Dashboard Status:** `python fleet_orchestrator.py --status`
- **Claim Topic/Task:** `python fleet_orchestrator.py --claim TOPIC AGENT`

---

### Brand Constitution Architecture
All assets and tone guidelines are centrally deployed at `/Brand_Constitution/`:
- `BRAND_VOICE.md` (voice/tone parameters across all brands)
- `BRAND_VISUAL.md` (hex codes, asset styling, visual identities)
- `CURRENT_DIRECTION.md` (Strategic direction roadmap)
- `BRAND_EVOLUTION_LOG.jsonl` (Version control timeline)
- **Per-Brand Folders:**
  - `possibilities/IDENTITY.md`
  - `protocol/IDENTITY.md`
  - `music/IDENTITY.md`
- **Shared Directives:** `AVATAR_RULES.md`, `PLATFORM_STANDARDS.md`

---

### Session Bootstrap Integration
Bootstrap execution parameters defined in `keystone_session_bootstrap SKILL.md` (Steps 8-9):
- **Step 8:** Automatically load the Brand Constitution on system boot.
- **Step 9:** Spin up the active agent fleet silo context on boot.
- **Verification:** Always query the overlap registry prior to initiation of new content sprint parameters.
- **Reporting:** Sync state back to the corresponding agent silo upon work completion.

---

### Spark Bridge
Provides synchronization between Google Drive and the local database:
- **Local Path:** `G:/My Drive/Keystone_Spark_Bridge/`
  - `/brain_export/` (System snapshots, current fleet state, and synchronized Brand Constitution)
  - `/spark_inbox/` (Target directory for external research ingestion and integration via Antigravity)
- *Status:* Fully operational.

---

### Caption & Video Production Strategy
- **Omi Warning:** Avoid direct text generation/prompting inside Omi to prevent stylized artifacting.
- **Caption Standards:** Use DaVinci Resolve exclusively for generating high-quality karaoke-style captions.
- **SEO Directive:** Always export and upload clean `.srt` files directly to YouTube to maximize SEO metadata indexing.