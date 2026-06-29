---
id: doc-sparkantigravitysync
title: Spark Antigravity Sync
type: document
summary: '> Last updated: 2026-06-08 | Status: ACTIVE'
entities:
- Keystone Possibilities
- Sea-to-Sky
- Squamish
- Wayne Stevenson
- Whistler
created: '2026-06-07T18:04:19.470444'
updated: '2026-06-14T19:57:36.061273'
---
# Antigravity ↔ Spark Integration Guide
> Last updated: 2026-06-08 | Status: ACTIVE

<!-- CONTEXT: Spark Antigravity Sync / Overview -->
## Overview

**Antigravity** = The architect. Plans, codes, manages brain, orchestrates.
**Spark** = The 24/7 executor. Sends emails, searches the web, monitors leads, creates Google Docs/Sheets.

Both share:
- **Google Drive** (Docs, Sheets, Gmail) — Spark reads/writes natively
- **Qdrant Brain** (keystone-brain MCP) — Antigravity reads/writes, Spark's findings get ingested here

---

<!-- CONTEXT: Spark Antigravity Sync / How to Submit Tasks to Spark -->
## How to Submit Tasks to Spark

**URL:** `https://gemini.google.com/spark`
**Account:** `curtis4vancouver@gmail.com`
**Access Method:** `chrome-devtools-mcp` (browser automation)

<!-- CONTEXT: Spark Antigravity Sync / Step-by-Step: -->
### Step-by-Step:
1. Navigate: `navigate_page` → `https://gemini.google.com/spark`
2. Wait for load (2s)
3. Focus editor: `document.querySelector('.ql-editor').focus()`
4. **CRITICAL:** Use `type_text` tool (NOT programmatic JS insertion)
   - Programmatic text via Quill API does NOT activate the Send button
   - Real keyboard simulation via `type_text` is the only method that works
5. Click Send: `document.querySelector('[aria-label="Send message"]').click()`
6. Spark creates a named task and begins working autonomously

---

<!-- CONTEXT: Spark Antigravity Sync / CRITICAL: File Format Rule -->
## CRITICAL: File Format Rule

> **ALL Spark research output must be saved as plain .txt files.**
> Do NOT create Google Docs (.gdoc), Sheets, or any Google Workspace format.
> The `drive_bridge.py` ingestion system can ONLY read `.txt`, `.md`, and `.json` files.
> Google Docs shortcut files are invisible to the pipeline.

---

<!-- CONTEXT: Spark Antigravity Sync / Active Schedules (5 Total — as of 2026-06-08) -->
## Active Schedules (5 Total — as of 2026-06-08)

| # | Schedule | Time | Purpose | Brain Sync |
|---|----------|------|---------|------------|
| 1 | **Track Google Nest cameras and appliance deals** | Daily 9:00 AM | Nest 2K cameras (2-pack, 40-50% off), washing machine, fridge, stove (40-60% off) | No |
| 2 | **Nightly brain research and sync** | Daily 1:00 AM | Dual-brand research (construction + wellness) → .txt to spark_inbox/ | ✅ Yes |
| 3 | **SEO, GEO and AI self-improvement intel** | Daily 10:00 PM | SEO/GEO strategy, competitor intel, Antigravity/MCP/Qdrant updates → .txt to spark_inbox/ | ✅ Yes |
| 4 | **Email intelligence and reply monitoring** | Daily 10:00 PM | Email digest, reply detection, draft replies → .txt to spark_inbox/ | ✅ Yes |
| 5 | **Sea-to-Sky property scout and PM client prospecting** | Daily 8:00 AM | New luxury properties, high-end realtors, investors, permit activity → draft outreach emails | ✅ Yes |

<!-- CONTEXT: Spark Antigravity Sync / File Naming Convention for Brain Sync -->
### File Naming Convention for Brain Sync
All files saved to `G:/My Drive/Keystone_Spark_Bridge/spark_inbox/` must use namespace prefixes:
- `possibilities_` → construction, PM, civil work
- `protocol_` → wellness, peptides, longevity
- `webmaster_` → SEO, GEO, competitors
- `general_` → industry news, emails, AI updates

---

<!-- CONTEXT: Spark Antigravity Sync / Spark Capabilities -->
## Spark Capabilities

| Capability | How It Works |
|-----------|-------------|
| **Web Search** | Google Search + Computer (remote browser) |
| **Gmail** | Read inbox, draft/send emails with confirmation |
| **Contacts** | Lookup recipient emails from Google Contacts |
| **Google Docs** | Creates research reports automatically |
| **Google Sheets** | Creates tracking spreadsheets (e.g., Lead Tracker) |
| **24/7 Tasks** | Background monitoring tasks that run continuously |
| **Contact Research** | Finds real email addresses from websites, Realtor.ca, company pages |

---

<!-- CONTEXT: Spark Antigravity Sync / Professional Email Signature (for all outreach) -->
## Professional Email Signature (for all outreach)

All client-facing emails drafted by Spark must include:

```
Wayne Stevenson
Keystone Possibilities — Construction Consulting & Project Management
consult@keystonepossibilities.com
keystonepossibilities.com

[Logo: https://www.keystonepossibilities.com/wp-content/uploads/logo.png]
```

---

<!-- CONTEXT: Spark Antigravity Sync / Brain Sync Protocol -->
## Brain Sync Protocol

<!-- CONTEXT: Spark Antigravity Sync / Qdrant Namespaces: -->
### Qdrant Namespaces:
| Namespace | Contents |
|-----------|----------|
| `possibilities_leads` | PM client leads, outreach records, competitor analysis |
| `operational_playbooks` | How-to guides, tool workflows, Spark playbook |
| `general` | [[general|General]] knowledge, corrections, learnings |

<!-- CONTEXT: Spark Antigravity Sync / Anti-Overlap Rules: -->
### Anti-Overlap Rules:
1. **Before ANY outreach** → Search `possibilities_leads` for existing contacts
2. **Before creating Spark tasks** → Check active tasks in sidebar
3. **All sent emails recorded** with: recipient, email, date, subject, property, status
4. **Follow-up window:** 7-10 business days
5. **NEVER re-contact** leads with "Awaiting response" status

---

<!-- CONTEXT: Spark Antigravity Sync / Confirmed Contacts (DO NOT RE-CONTACT) -->
## Confirmed Contacts (DO NOT RE-CONTACT)

| Recipient | Email | Property | Sent |
|-----------|-------|----------|------|
| James L. Wang (RE/MAX) | James.Wang@remax.net | Lions Bay lots | 2026-06-07 |
| Dave Burch (Whistler RE) | daveb@wrec.com | Whistler lot | 2026-06-07 |
| Matt Lees (Engel & Völkers) | matt.lees@engelvoelkers.com | Squamish dev | 2026-06-07 |
| Danielle Menzel (Whistler RE) | danielle@wrec.com | Pemberton SSMUH | 2026-06-07 |
| Adera Development | info@adera.com | Britannia Beach | 2026-06-07 |
| Melissa Pace (DVP owner) | mpace@bcchamber.org | Whistler Drifter Way | 2026-06-07 |

---

<!-- CONTEXT: Spark Antigravity Sync / Deleted Projects (NO LONGER ACTIVE) -->
## Deleted Projects (NO LONGER ACTIVE)

- ~~Glenwood~~
- ~~770 SW Merian~~

These are closed projects. Do not reference them in any outreach, tasks, or schedules.

---

<!-- CONTEXT: Spark Antigravity Sync / Future Spark Task Ideas -->
## Future Spark Task Ideas

- Automated follow-up emails (10 days after no response)
- Content research for video scripts
- [[music|Music]] distribution stat tracking
- Social media engagement monitoring
- Weekly new permit/listing sweeps


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
