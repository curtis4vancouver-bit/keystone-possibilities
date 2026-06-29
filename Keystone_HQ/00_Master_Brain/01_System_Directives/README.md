# Gemini Pro Instruction Sets — Master Index

**Created:** 2026-06-10 by Antigravity  
**Total Sets:** 5  
**Execution Order:** Run in a single chat in sequence: 01 → 02 → 03 → 05 → 04

---

## 🚀 Bootstrap Prompt

```text
Read Master_Docs/Gemini_Pro_Instructions/README.md to understand the full scope. Then execute EACH instruction set in this exact order, one at a time. Complete each set fully before moving to the next. After finishing each set, write a summary of what you did to .learnings/insights/gemini_pro_execution_log_20260610.md before starting the next one.

Execution Order: Set 01 (Brain) → Set 02 (Skills) → Set 03 (Possibilities Website) → Set 05 (Recomposition Website) → Set 04 (Research Topics)

Brand Isolation Warning: keystonepossibilities.com (Construction) and keystonerecomposition.com (Health/Music) are SEPARATE brands. NEVER cross-contaminate schema or content between them. Keep them completely isolated.
```

---

## 📋 Instruction Sets

### 1. [Brain Optimization & Bootstrap](./01_BRAIN_OPTIMIZATION_AND_BOOTSTRAP.md)
*   **Vector Database Setup:** Optimize Qdrant vector brain using hybrid search, semantic chunking, and temporal metadata.
*   **Data Architecture:** Organize all project assets and data into their designated folders.
*   **Bootstrap Updates:** Update the session bootstrap skill configuration.
*   **Persistent Context:** Create `.agents/rules/` to store always-loaded context rules.
*   *Time Allocation:* 2-3 hours | *Risk Profile:* LOW

### 2. [Skills Implementation & Documentation](./02_SKILLS_IMPLEMENTATION_AND_DOCUMENTATION.md)
*   **Skill Audit:** Audit and update all 29+ core skill files.
*   **New Skills:** Develop 3 new skills: GEO deployment, client acquisition, and self-documentation.
*   **Caching & Registry:** Build a skill registry cache.
*   **Brand Alignment:** Verify brand consistency across all content-producing skills.
*   **Mapping:** Document all integration links and internal connections.
*   *Time Allocation:* 2-3 hours | *Risk Profile:* LOW

### 3. [SEO/GEO — Keystone POSSIBILITIES Website](./03_SEO_GEO_WEBSITE_IMPLEMENTATION.md)
*   **Brand Scope:** Focus exclusively on keystonepossibilities.com (Construction Brand).
*   **Schema Markup:** Implement Organization, LocalBusiness, GeneralContractor, FAQ, and Breadcrumb structured data.
*   **AI Crawler Policy:** Configure `robots.txt` specifically optimized for AI search crawlers.
*   **Local SEO:** Deploy local citation checklists (HomeStars, Houzz, BBB) and create Wikidata entities.
*   **Content Loop:** Set up a blog-to-video traffic loop.
*   *Time Allocation:* 2-3 hours | *Risk Profile:* MEDIUM (live website changes)
*   ⚠️ **DO NOT touch keystonerecomposition.com** during this set.

### 4. [70 New Deep Research Topics](./04_SEVENTY_NEW_RESEARCH_TOPICS.md)
*   **Topic Bank:** 70 categorized research topics spanning target business verticals.
*   **Execution Prompts:** Ready-to-use prompts optimized for Chrome Deep Research.
*   **Data Filing:** Structured filing rules for each target topic.
*   **Prioritization:** Ordered by impact (🔴 HIGH → 🟡 MEDIUM → 🟢 LOW).
*   *Time Allocation:* Overnight batching (max 30 prompts per 5-hour window) | *Risk Profile:* NONE

### 5. [SEO/GEO — Keystone RECOMPOSITION Website](./05_RECOMPOSITION_WEBSITE_SEO_GEO.md)
*   **Brand Scope:** Focus exclusively on keystonerecomposition.com (Health, Wellness, & Music Brand).
*   **Structured Data:** Implement Organization, MedicalBusiness, MedicalWebPage (YMYL compliant), and MusicGroup schemas.
*   **YMYL Compliance:** Mandate medical disclaimers site-wide, on a dedicated disclaimer page, and on individual content posts.
*   **AI Disclosures:** Add clear AI-generation disclosures for music content.
*   **Niche Citations:** Build health-specific citation profiles.
*   *Time Allocation:* 2-3 hours | *Risk Profile:* MEDIUM (live website + YMYL compliance requirements)
*   ⚠️ **DO NOT touch keystonepossibilities.com** during this set.

---

## ⚠️ Core System Constraints

1.  **Workspace Root Path:** `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\`
2.  **Agent Architecture:** Review `AGENTS.md` in the root folder for the complete system topology before executing tasks.
3.  **Preservation Policy:** Do not hard-delete files. Move obsolete items to `deprecated_scripts/` or `_archive/`.
4.  **Audit Trail:** Log all changes to `.learnings/insights/` and ingest them into the vector brain.
5.  **Pre-Deployment Testing:** Validate changes locally before deploying live site updates (Sets 03 & 05).
6.  **API Rate Limits:** Manage Deep Research token usage carefully (strict 30 prompts per 5-hour window).
7.  **Token Routing Rule:** Protocol brand assets must always use Recomposition tokens; never consume Possibilities tokens.
8.  **Complete Brand Isolation:** Never mix schema, metadata, or content between the construction brand (Possibilities) and health/music brand (Recomposition).
9.  **YMYL Requirement:** Medical disclaimers are legally mandatory on all Recomposition health-related pages.