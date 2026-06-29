---
id: doc-fleetdeploymentsummary
title: Fleet Deployment Summary
type: document
summary: 'All agents have silo folders at AgentFleet/{agentname}/ with:'
entities:
- DaVinci
- DaVinci Resolve
- YouTube
created: '2026-05-28T22:40:01.343882'
updated: '2026-06-14T19:57:36.002343'
---
# Keystone Fleet [[ARCHITECTURE|Architecture]] � Deployment Summary
<!-- CONTEXT: Fleet Deployment Summary / Deployed: 2026-05-28 -->
## Deployed: 2026-05-28

<!-- CONTEXT: Fleet Deployment Summary / Agent Fleet (13 [[AGENTS|Agents]]) -->
### Agent Fleet (13 [[AGENTS|Agents]])
All [[AGENTS|agents]] have silo folders at Agent_Fleet/{agent_name}/ with:
- [[STATE|STATE]].json (status, outputs, claimed topics)
- CAPABILITIES.json (skills, APIs, strengths)
- OUTPUT_LOG.jsonl (production history)
- INBOX.json (messages from [[master|Master]] Brain)

[[AGENTS|Agents]]: chronos_master, possibilities_brand, [[protocol_brand|protocol_brand]], music_brand, recomposition_music, [[webmaster|webmaster]], analytics_reporting, legal_counsel, tax_strategist, site_superintendent, research_scout, executive_assistant, [[local_seo|local_seo]]

<!-- CONTEXT: Fleet Deployment Summary / Fleet Orchestrator -->
### Fleet Orchestrator
Run: python fleet_orchestrator.py --sweep (full scan)
Run: python fleet_orchestrator.py --status (dashboard)
Run: python fleet_orchestrator.py --claim TOPIC AGENT (claim topic)

<!-- CONTEXT: Fleet Deployment Summary / Brand Constitution -->
### Brand Constitution
Location: Brand_Constitution/
- [[Brand_Constitution/BRAND_VOICE|BRAND_VOICE]].md (voice/tone rules for all brands)
- [[Brand_Constitution/BRAND_VISUAL|BRAND_VISUAL]].md (visual [[Brand_Constitution/protocol/IDENTITY|identity]], hex colors, thumbnail rules)
- [[Brand_Constitution/CURRENT_DIRECTION|CURRENT_DIRECTION]].md (May 2026 strategic direction)
- BRAND_EVOLUTION_LOG.jsonl (timestamped change log)
- Per-brand: [[possibilities|possibilities]]/[[Brand_Constitution/protocol/IDENTITY|IDENTITY]].md, protocol/[[Brand_Constitution/protocol/IDENTITY|IDENTITY]].md, [[music|music]]/[[Brand_Constitution/protocol/IDENTITY|IDENTITY]].md
- Shared: [[Brand_Constitution/shared/AVATAR_RULES|AVATAR_RULES]].md, [[Brand_Constitution/shared/PLATFORM_STANDARDS|PLATFORM_STANDARDS]].md

<!-- CONTEXT: Fleet Deployment Summary / Session Bootstrap Updated -->
### Session Bootstrap Updated
Steps 8-9 added to keystone_session_bootstrap [[davinci-resolve-mcp/docs/SKILL|SKILL]].md:
- Step 8: Load Brand Constitution on boot
- Step 9: Load agent fleet silo on boot
- Check overlap registry before content work
- Update silo after completing work

<!-- CONTEXT: Fleet Deployment Summary / Spark Bridge -->
### Spark Bridge
Google Drive: G:/My Drive/Keystone_Spark_Bridge/
- brain_export/ (brain snapshots, fleet status, brand constitution synced)
- spark_inbox/ (Spark writes research here, Antigravity ingests to brain)
Already operational with 7 documents processed.

<!-- CONTEXT: Fleet Deployment Summary / Caption Strategy -->
### Caption Strategy
- Never prompt text into Omi (looks cartoonish)
- Use DaVinci Resolve for karaoke-style captions
- Always upload SRT file to YouTube for SEO


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
