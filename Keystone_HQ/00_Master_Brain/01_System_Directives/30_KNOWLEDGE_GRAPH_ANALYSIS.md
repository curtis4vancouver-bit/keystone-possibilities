---
id: doc-30-knowledge-graph-analysis
title: 'Keystone Sovereign: Knowledge Graph & Link Analysis Report'
type: Analysis Report
summary: Vault knowledge graph health analysis, topic clusters, hub identification, and sparse area detection using the Graphthulhu MCP.
tags:
- Analysis Report
- graphthulhu
- obsidian
- okf
- second-brain
created: '2026-06-21T17:26:00'
updated: '2026-06-21T17:26:00'
---

# Keystone Sovereign: Knowledge Graph & Link Analysis Report

> [!IMPORTANT]
> **Owner:** Wayne Stevenson / Keystone Empire  
> **Date:** June 21, 2026  
> **Status:** Approved (OKF v0.1 Compliant)  
> **Context:** Vault structural audit mapping note connectivity, semantic clusters, and sparse gaps using the Graphthulhu Go-compiled server (v0.5.0) backend.

---

## 📊 Knowledge Graph Health Overview

Using the `health` check tool, we verified the configuration and status of the local Obsidian Brain connection:

| Metric | Value | Details / Status |
|--------|-------|------------------|
| **Backend Type** | `obsidian` | Running native vault parsing |
| **Server Status** | `ok` | Stable, connected, and active |
| **Indexed Pages** | 648 | Total markdown nodes cataloged |
| **Read-Only Mode** | `False` | Ready for write operations and links backfill |
| **Version** | `0.5.0` | Latest Go-compiled binary |

---

## 🔍 Topic Clusters & Hubs Analysis

Running the `topic_clusters` algorithm identified **28 distinct connected components** (clusters) inside the vault. The largest clusters and their central hubs (most connected pages) are detailed below:

### 1. Cluster 0 (Primary Core)
*   **Size:** 468 pages (representing ~72% of the vault)
*   **Central Hub:** `Master_Docs/_INDEX.md`
*   **Focus:** Core operational files, fleet directories, standard operating procedures, tax and legal files, and primary content production guides.

### 2. Cluster 1 (Video Production)
*   **Size:** 42 pages
*   **Central Hub:** `Research_Archives/05_Video_Production/_INDEX.md`
*   **Focus:** DaVinci Resolve scripting, ElevenLabs voice blueprints, character consistency guides, and Google Flow prompting.

### 3. Cluster 14 (DaVinci MCP Kernel Docs)
*   **Size:** 22 pages
*   **Central Hub:** `davinci-resolve-mcp/docs/_INDEX.md`
*   **Focus:** Developer manuals, timelines, rendering, color grading, and Fairlight kernel documentation for the DaVinci Resolve MCP.

### 4. Cluster 10 (YouTube Scripting)
*   **Size:** 16 pages
*   **Central Hub:** `Research_Archives/03_YouTube_Scripts/_INDEX.md`
*   **Focus:** Audience retention research, thumbnail psychology, ElevenLabs scripts, and script writing best practices.

### 5. Cluster 11 (Tax & Corporate Law)
*   **Size:** 10 pages
*   **Central Hub:** `Research_Archives/10_Tax_Legal_Corporate/_INDEX.md`
*   **Focus:** CRA CERB dividends, BC dividend/salary tax models, worksafebc obligations, and corporate asset shielding.

### 6. Cluster 16 (Creative Media Automation Pipelines)
*   **Size:** 9 pages
*   **Central Hub:** `Research_Archives/15_Content_Pipeline/_INDEX.md`
*   **Focus:** Omi voice archiving companions, Playwright marketplace scrapers, and yt-dlp integrations.

### 7. Cluster 6 (Agent Fleet Skills)
*   **Size:** 9 pages
*   **Central Hub:** `dynamic_skills/_INDEX.md`
*   **Focus:** Master tool reference files, Suno music creator skills, webmaster SEO directives, and property scout tools.

### 8. Cluster 5 (RAG & Code Optimization)
*   **Size:** 7 pages
*   **Central Hub:** `Research_Archives/07_Coding_Optimization/_INDEX.md`
*   **Focus:** Qdrant HNSW parameters, pgvector optimization, embedding chunk comparisons, and concurrency.

---

## 🕳️ Sparse Area & Knowledge Gaps

Running the `knowledge_gaps` traversal tool (with stray numeric block-refs excluded) returned the following metrics:

*   **Orphan Pages:** `0` (Every note has at least one inbound or outbound link, validating that `orphan_linker.py` has run successfully).
*   **Dead-End Pages:** `0` (Every note containing links links to a page that exists or is valid).
*   **Weakly Linked Nodes (Degree <= 2):** 20 pages. These represent edge nodes in the vault that could benefit from closer cross-linking:
    1.  `Research_Archives/04_YT_Analytics/20260610_YT_ANALYTICS_research_youtube_niche_gap_analysis_techniques._how_do_you_f` (Degree 1)
    2.  `Research_Archives/17_BC_Construction/BC_Building_Code_Memory_Integration` (Degree 2)
    3.  `Research_Archives/08_SEO_Website/20260612_wordpress_management_mcps` (Degree 2)
    4.  `Research_Archives/08_SEO_Website/4_1_Service_Page_Architecture` (Degree 2)
    5.  `Research_Archives/20260610_AGENT_ARCH_pretooluse_hook_security_patterns__deep_research_into_pretoo` (Degree 2)
    6.  `Research_Archives/02_MCP_Tools/20260612_newest_mcps_mar_jun` (Degree 2)
    7.  `Research_Archives/01_Agent_Architecture/20260522_antigravity_skills_discovery_antigravity_subagent_orchestration_patterns_for_parallel_aut` (Degree 2)
    8.  `Research_Archives/01_Agent_Architecture/20260522_antigravity_skills_directory` (Degree 2)
    9.  `Research_Archives/01_Agent_Architecture/20260609_AGENT_ARCH_how_to_build_an_ai_agent_'bootstrap_protocol'_that_runs_auto` (Degree 2)
    10. `Research_Archives/07_Coding_Optimization/Windows_11_High_Concurrency_Optimization` (Degree 2)
    11. `Research_Archives/13_Chrome_Automation/20260522_chrome_devtools_advanced` (Degree 2)
    12. `dynamic_skills/05_youtube_protocol` (Degree 2)
    13. `Content_Production/SCRIPT_001_CLEAN_READ` (Degree 2)
    14. `davinci-resolve-mcp/examples/README` (Degree 2)
    15. `Brand_Constitution/possibilities/IDENTITY` (Degree 2)
    16. `Research_Archives/04_YT_Analytics/20260610_YT_ANALYTICS_research_how_to_use_the_youtube_data_api_v3_for_competitive_` (Degree 2)
    17. `Research_Archives/DeepDive_19_1781284937444` (Degree 2)
    18. `Research_Archives/01_Agent_Architecture/OTS_Command_Center_Deep_Research` (Degree 2)
    19. `Master_Docs/Wayne_Stevenson_Resume` (Degree 2)
    20. `Research_Archives/DeepDive_33_1781284960663` (Degree 2)

---
📁 **See also:** [[INDEX|← Directory Index]] · [[29_OKF_AND_SYSTEM_UPGRADE_MASTER_PLAN|← Master Upgrade Plan]]