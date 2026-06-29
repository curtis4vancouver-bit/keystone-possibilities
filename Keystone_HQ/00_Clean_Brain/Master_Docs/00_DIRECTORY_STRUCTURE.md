---
id: doc-00directorystructure
title: Directory Structure
type: document
summary: '├── .agents/skills/             # Antigravity skill definitions (banner-creator,
  logo-creator, etc.)'
entities: []
created: '2026-06-11T09:45:50.532685'
updated: '2026-06-14T19:57:35.825388'
---
# Directory Structure

```
00_Master_Brain/
├── .agents/skills/             # Antigravity skill definitions (banner-creator, logo-creator, etc.)
├── .learnings/                 # Self-evolution persistent memory
│   ├── correction_journal.json # Error→fix mappings (18 entries, v2.0)
│   ├── refined_prevention_rules.json  # Auto-generated prevention rules (18 rules)
│   ├── working_memory.db       # SQLite ephemeral key-value store
│   ├── corrections/            # Individual correction records
│   ├── dream_logs/             # Dream engine consolidation reports
│   ├── errors/                 # Structured error cards (auto-archived after 30 days)
│   │   └── _archive/           # Archived stale error cards
│   ├── insights/               # Daily digests, morning reports, compacted logs
│   └── mock_tests/             # Mock test result snapshots
├── Agent_Fleet/                # 13 agent directories (inbox, output logs, status)
│   ├── analytics_reporting/
│   ├── chronos_master/
│   ├── executive_assistant/
│   ├── legal_counsel/
│   ├── local_seo/
│   ├── music_brand/
│   ├── possibilities_brand/
│   ├── protocol_brand/
│   ├── recomposition_music/
│   ├── research_scout/
│   ├── site_superintendent/
│   ├── tax_strategist/
│   └── webmaster/
├── Brand_Constitution/         # Brand identity, voice, visuals, evolution log
│   ├── BRAND_VOICE.md
│   ├── BRAND_VISUAL.md
│   ├── CURRENT_DIRECTION.md
│   ├── BRAND_EVOLUTION_LOG.jsonl
│   ├── possibilities/
│   ├── protocol/
│   ├── music/
│   └── shared/
├── Cognitive_Substrates_Console/ # Web-based brain monitoring UI (HTML/JS/CSS)
├── Deep_Research_Results/       # Overnight Chrome research output (markdown)
├── Fleet_Dashboard/             # Fleet status JSON and analytics feed
├── Master_Docs/                 # 60+ strategic documents (numbered 01–27 + named)
├── Qdrant_Brain/                # Local Qdrant vector DB storage
├── Research_Archives/           # Archived research outputs
├── Skill_Vault/                 # Shared skill resources
├── Transcripts/                 # Agent execution logs (auto-compacted weekly)
├── dynamic_skills/              # Hot-deployed Python skills (SEO, tax, diagnostics, etc.)
├── scripts/                     # 14 production scripts (audiobook, video, search, etc.)
├── scratch/                     # Temporary working files
└── deprecated_scripts/          # Retired scripts kept for reference
```


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
