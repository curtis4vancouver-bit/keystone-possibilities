# Antigravity ↔ Spark Integration Guide
> Last updated: 2026-06-08 | Status: ACTIVE

## Overview

- **Antigravity** = The architect. Plans, codes, manages brain, orchestrates.
- **Spark** = The 24/7 executor. Sends emails, searches the web, monitors leads, creates Google Docs/Sheets.

### Shared Ecosystem:
- **Google Drive** (Docs, Sheets, Gmail) — Spark reads/writes natively
- **Qdrant Brain** (keystone-brain MCP) — Antigravity reads/writes, Spark's findings get ingested here

---

## How to Submit Tasks to Spark

*   **URL:** `https://gemini.google.com/spark`
*   **Account:** `curtis4vancouver@gmail.com`
*   **Access Method:** `chrome-devtools-mcp` (browser automation)

### Execution Steps:
1. Navigate: `navigate_page` → `https://gemini.google.com/spark`
2. Wait for load (2s)
3. Focus editor: `document.querySelector('.ql-editor').focus()`
4. **CRITICAL SELF-HEALING NOTE:** Use `type_text` tool (NOT programmatic JS insertion). Programmatic text via Quill API does NOT activate the Send button. Real keyboard simulation via `type_text` is the only method that works.
5. Click Send: `document.querySelector('[aria-label="Send message"]').click()`
6. Spark creates a named task and begins working autonomously.

---

## CRITICAL: File Format Rule

> **ALL Spark research output must be saved as plain .txt files.**
> Do NOT create Google Docs (.gdoc), Sheets, or any Google Workspace format for direct pipeline ingestion.
> The `drive_bridge.py` ingestion system can ONLY read `.txt`, `.md`, and `.json` files. Google Docs shortcut files are invisible to the pipeline.

---

## Active Schedules (5 Total — as of 2026-06-08)

| # | Schedule | Time | Purpose | Brain Sync |
|---|----------|------|---------|------------|
| 1 | **Track Google Nest cameras and appliance deals** | Daily 9:00 AM | Nest 2K cameras (2-pack, 40-50% off), washing machine, fridge, stove (40-60% off) | No |
| 2 | **Nightly brain research and sync** | Daily 1:00 AM | Dual-brand research (construction + wellness) → .txt to spark_inbox/ | ✅ Yes |
| 3 | **SEO, GEO and AI self-improvement intel** | Daily 10:00 PM | SEO/GEO strategy, competitor intel, Antigravity/MCP/Qdrant updates → .txt to spark_inbox/ | ✅ Yes |
| 4 | **Email intelligence and reply monitoring** | Daily 10:00 PM | Email digest, reply detection, draft replies → .txt to spark_inbox/ | ✅ Yes |
| 5 | **Sea-to-Sky property scout and PM client prospecting** | Daily 8:00 AM | New luxury properties, high-end realtors, investors, permit activity → draft outreach emails | ✅ Yes |

### File Naming Convention for Brain Sync
All files saved to `G:/My Drive/Keystone_Spark_Bridge/spark_inbox/` must use namespace prefixes:
- `possibilities_` → construction, PM, civil work
- `protocol_` → wellness, peptides, longevity
- `webmaster_` → SEO, GEO, competitors
- `general_` → industry news, emails, AI updates

---

## Spark Capabilities

- **Web Search**: Google Search + Computer (remote browser)
- **Gmail**: Read inbox, draft/send emails with confirmation
- **Contacts**: Lookup recipient emails from Google Contacts
- **Google Docs**: Creates research reports automatically
- **Google Sheets**: Creates tracking spreadsheets (e.g., Lead Tracker)
- **24/7 Tasks**: Background monitoring tasks that run continuously
- **Contact Research**: Finds real email addresses from websites, Realtor.ca, company pages

---

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

## Brain Sync Protocol

### Qdrant Namespaces:
- `possibilities_leads` — PM client leads, outreach records, competitor analysis
- `operational_playbooks` — How-to guides, tool workflows, Spark playbook
- `general` — General knowledge, corrections, learnings

### Anti-Overlap Rules:
1. **Before ANY outreach** → Search `possibilities_leads` for existing contacts.
2. **Before creating Spark tasks** → Check active tasks in sidebar.
3. **Record all sent emails** with: recipient, email, date, subject, property, status.
4. **Follow-up window:** 7-10 business days.
5. **NEVER re-contact** leads with "Awaiting response" status.

---

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

## Closed Projects (Inactive - DO NOT Reference)
- ~~Glenwood~~
- ~~770 SW Merian~~

---

## Future Spark Task Ideas
- Automated follow-up emails (10 days after no response)
- Content research for video scripts
- Music distribution stat tracking
- Social media engagement monitoring
- Weekly new permit/listing sweeps