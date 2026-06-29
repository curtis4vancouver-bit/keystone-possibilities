# AGENTS.md — Keystone Sovereign Agent Fleet Architecture
> Last updated: 2026-06-04 by Chronos Master Brain cleanup sweep

## Overview

The Keystone Master Brain is an autonomous AI orchestration system managing **Wayne Stevenson's dual-brand empire**: Keystone Possibilities (construction/PM) and Keystone Recomposition (health protocols, music, wellness). It coordinates 13+ specialized agents, self-healing loops via self-evolution, overnight research automation, and multi-platform content publishing.

See also: State of the Empire · [[DIRECTIVES|Directives]] · Active [[STATE|State]] · Integration Map

**Workspace Root:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\`

---

## Agent Fleet (13 Agents)

All agents live in `Agent_Fleet/` with individual directories containing `INBOX.json`, `OUTPUT_LOG.jsonl`, and status files.

| # | Agent | Brand | Skill File | Purpose |
|---|-------|-------|------------|---------|
| 1 | chronos_master | All | `01_chronos_master_brain` | Top-level orchestrator. Loops through all agents, checks status, triggers self-healing, coordinates the empire. |
| 2 | possibilities_brand | Possibilities | `02_possibilities_brand` | Full-cycle content: PM/Bill 44 research, scripts, Google Flow prompts, B-roll, DaVinci timelines, blog posts, uploads. |
| 3 | local_seo | Possibilities | `04_keystone_local_seo` | Local SEO domination for Sea-to-Sky corridor. GMB optimization, citation building, ranking strategies. |
| 4 | protocol_brand | Protocol | `05_protocol_script_studio` | APOLLO engine. Full-cycle Protocol/Recomposition content: peptide science, serialized scripts, timelines, publishing. |
| 5 | music_brand | Music | `08_music_brand` | Full-cycle Recomposition music production, Google Flow avatar generation, lyrics, MusicBrainz cataloging, multi-platform publishing. |
| 6 | recomposition_music | Music | `08_music_brand` | Companion agent for music distribution and Spotify/streaming optimization. |
| 7 | webmaster | All | `11_webmaster` | SEO domination, landing pages, Google Console fixes, Knowledge Panel management, blog-to-video traffic loops, cross-brand backlinking. |
| 8 | legal_counsel | All | `12_legal_counsel` | Legal matters, compliance, contract review, dispute resolution. |
| 9 | tax_strategist | All | `13_tax_strategist` | Tax strategies, deductions, financial structuring for both brands. |
| 10 | site_superintendent | Possibilities | `15_site_superintendent` | Active job site management. Blueprints, STEP code requirements, construction compliance. |
| 11 | research_scout | All | `16_research_scout` | Proactive self-learning. Autonomously discovers opportunities, identifies threats, curates recommendations. |
| 12 | analytics_reporting | All | `17_analytics_reporting` | Unified performance analytics: YouTube, Spotify, Search Console, social data. Weekly cross-brand reports. |
| 13 | executive_assistant | All | `18_executive_assistant` | Wayne's personal EA. Gmail management, email sorting, reply drafting, Google Docs organization. |

---

## Self-Evolution Cycle & Core Infrastructure

- **For Self-Evolution Engine, Correction Journals, & Daily Digests:** Read Infrastructure & Evolution
- **For the Background Loops & Upgrade Roadmap:** Read [Loops & Daemons Reference](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Master_Docs/35_BACKGROUND_LOOPS_AND_DAEMONS.md)
- **For the full System Directory Structure:** Read Directory Structure
- **For Active Projects:** Read Active Projects
- **For the Sovereign Memory Architecture:** Read Memory Architecture
- **For Wayne's Personal Health & Weight Logs:** Read Wayne's Personal Stats

---

## Account Structure

> **CRITICAL:** ALL social media accounts are under `curtis4vancouver@gmail.com`. Protocol brand NEVER has its own tokens — it always inherits from Recomposition.

| Platform | Possibilities | Recomposition/Protocol |
|----------|--------------|----------------------|
| YouTube | `youtube_token_possibilities.json` | `youtube_token_oac.json` (shared) |
| YouTube (Protocols) | — | `youtube_token_protocols.json` |
| Meta/Facebook | `social_tokens.json` | `social_tokens.json` (same token) |
| TikTok | — | `social_tokens.json` |

See: Social Media Infrastructure Master

---

## Operational Commands

```bash
# Health check
python self_evolution.py --health

# Weekly compaction (prune old logs, free context)
python self_evolution.py --compact

# Dream cycle (overnight memory consolidation)
python dream_engine.py --dream

# Research daemon status
python overnight_research_daemon.py --status

# Fleet status
cat Fleet_Dashboard/fleet_status.json
```

**Related Scripts:** self_evolution · dream_engine · overnight_research_daemon · keystone_os_daemon · nightly_orchestrator · fleet_orchestrator · sovereign_coordinator · brand_guardian · working_memory · hybrid_retrieval

---

*This document is auto-maintained by the Chronos Master Brain self-evolution system.*


---
📁 **See also:** [[MAP_OF_CONTENTS|← Directory Index]]
