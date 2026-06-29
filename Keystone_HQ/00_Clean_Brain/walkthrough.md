# Walkthrough: Website Upgrades, GBP Optimization & Gmail Triage

This walkthrough summarizes the technical deliverables completed across your website child theme, Google Business Profile, and Gmail inbox organization.

---

## Technical Details

### 1. Person Schema Triangulation (Wayne Stevenson)
Unified Wayne Stevenson's authority between the B2B construction brand (`keystonepossibilities.ca`) and the B2C health/[[music|music]] brand (`keystonerecomposition.com`):
- **Canonical ID:** Unified under `https://www.keystonepossibilities.com/wayne-stevenson/#person`.
- **WorksFor Roles:** Linked to Managing Director ([[possibilities|Possibilities]] Ltd) and Founder/Researcher (Recomposition).
- **sameAs Social Graph:** Triangulated all profile pages (LinkedIn, YouTube, Spotify, Facebook, Instagram, TikTok, MusicBrainz, and Audiomack).

### 2. Organization Schema & GeoCoordinates
- Consolidated duplicate Rank Math publisher/org nodes into a single authoritative entity with `@id: https://keystonepossibilities.ca/#organization`.
- Injected credentials (BC Housing Residential Builder #52603, Registered BC Hydro Civil Contractor).
- Mapped precise `GeoCoordinates` (Latitude `49.7016`, Longitude `-123.1558`) to boost Google Map Pack relevance.

### 3. Google Indexing API Integration
- Stored the GCS service account key in the database options.
- Set up auto-push hooks on post publishing and updates.
- Injected custom OpenSSL assertion signing code directly into the child theme's `functions.php`.

### 4. New BC Hydro Civil Contractor Landing Page
- Created and deployed `bc-hydro-registered-civil-contractor.html` in the websites directory.
- Highlights the September 2024 grid mandate, Wayne's 20+ years of local civil experience, and transparent 10–15% flat-fee structures.
- Appended the new civil utility link to all 6 other landing page footers.

### 5. Google Business Profile Services Audit
- Verified all 21 active service entries across 4 categories ([[general|General]] Contractor, Custom Home Builder, Construction Company, Excavating Contractor) have custom, keyword-rich descriptions (max 300 characters).
- Verified that all irrelevant suggested services (e.g., *furniture assembly, fan repair, TV mounting*) remain unchecked/excluded.

### 6. Gmail Clean-up & Triage (NEW)
To stop you from missing important emails that were being auto-archived:
- **Filter Removal:** Deleted the 14 custom Gmail filters that were automatically labeling and archiving incoming messages (marking them to skip the Inbox). All future emails will now stay in your main Inbox.
- **New Folders (Labels) Created:**
  - `00_Junk_Review` (For promotions, newsletters, and codes to review and delete in bulk).
  - `Bills & Payments` (For utility invoices, transaction statements, and payments).
  - `School & Kids` (For secondary school alerts and kids' activities).
- **Inbox Triage:** Read all active Inbox emails one-by-one and filed them:
  - **Archived to `00_Junk_Review`:** Expired HomeStars login codes, Nextdoor verification emails, expired Apple verification codes, and Mounjaro privacy policy updates.
  - **Categorized to `Bills & Payments` (Kept in Inbox):** Starlink payment failure alert and Sunshine Coast Credit Union transaction denied notification.
  - **Categorized to `02_Keystone_Projects` (Kept in Inbox):** Google Business Profile verification alert, YellowPages listing confirmation, and BC Housing builder licence renewal approval.
  - **Categorized to `School & Kids` (Kept in Inbox):** HSS secondary school announcements.
  - **Categorized to `03_Personal_Kids` (Kept in Inbox):** Google Home member invite and Ana's screenshot attachments.

---

## 7. Chrome Deep Research — System Optimization & Second Brain Ingestion
Conducted intensive multi-tab concurrent Chrome Deep Research runs across the remaining 7 system optimization and automation topics, saving detailed, comprehensive markdown documents directly to your Second Brain under `Research_Archives/`:
- **Prompt 4 (Drive-to-NotebookLM Sync):** Extracted protocol-level API synchronization methods, rclone format coercion (`md` to Google Docs), and Playwright automation architectures. Saved to [[Research_Archives/20260615_SYS_drive_to_notebooklm_sync_automation|20260615_SYS_drive_to_notebooklm_sync_automation]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_drive_to_notebooklm_sync_automation|20260615_SYS_drive_to_notebooklm_sync_automation]].md).
- **Prompt 5 (Local Context Memory & Digests):** Outlined log parsing (JSONL), dynamic token chunking, LLM history compaction, and templates for Obsidian Daily Digests. Saved to [[Research_Archives/20260615_SYS_obsidian_conversation_logs_briefing|20260615_SYS_obsidian_conversation_logs_briefing]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_obsidian_conversation_logs_briefing|20260615_SYS_obsidian_conversation_logs_briefing]].md).
- **Prompt 6 (Local Agentic Frameworks):** Analyzed CrewAI, AutoGen, and LangGraph local setups, custom tool definitions, memory management, and fleet coordination. Saved to [[Research_Archives/20260615_SYS_local_multi_agent_frameworks_integration|20260615_SYS_local_multi_agent_frameworks_integration]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_local_multi_agent_frameworks_integration|20260615_SYS_local_multi_agent_frameworks_integration]].md).
- **Prompt 7 (Google Indexing API Clients):** Mapped out OAuth2 token caching, JSON Web Token (JWT) assertion signing, batch queue management, and rate-limit backoffs. Saved to [[Research_Archives/20260615_SYS_google_indexing_api_integration|20260615_SYS_google_indexing_api_integration]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_google_indexing_api_integration|20260615_SYS_google_indexing_api_integration]].md).
- **Prompt 8 (GSC Video Indexing Schema):** Generated PHP hooks for WordPress child themes to automatically extract iframe sources, pull YouTube/Vimeo metadata, and output valid `VideoObject` JSON-LD schema. Saved to [[Research_Archives/20260615_SYS_wordpress_gsc_video_indexing_schema|20260615_SYS_wordpress_gsc_video_indexing_schema]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_wordpress_gsc_video_indexing_schema|20260615_SYS_wordpress_gsc_video_indexing_schema]].md).
- **Prompt 9 (WordPress Speed Optimization):** Provided clean `functions.php` snippets for asset cache-busting using `filemtime`, HTML minification, transient purging, and bypassing CDN caches for instant raw file delivery. Saved to [[Research_Archives/20260615_SYS_wordpress_speed_optimization_cache_busting|20260615_SYS_wordpress_speed_optimization_cache_busting]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_wordpress_speed_optimization_cache_busting|20260615_SYS_wordpress_speed_optimization_cache_busting]].md).
- **Prompt 10 (Local LLM Gmail Automation):** Detailed IMAP/Gmail API connection flows, message classification using local Ollama/Llama-3 models, and automatic drafting in the Gmail Drafts folder for review. Saved to [[Research_Archives/20260615_SYS_local_llm_gmail_draft_automation|20260615_SYS_local_llm_gmail_draft_automation]].md](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/[[Research_Archives/20260615_SYS_local_llm_gmail_draft_automation|20260615_SYS_local_llm_gmail_draft_automation]].md).

---

## Verification Results

| Verification Check | Status | Method / Result |
|--------------------|--------|-----------------|
| GBP Services Descriptions | ✅ Verified | All active services are fully populated; no descriptions are missing. |
| Gmail Filter Deletion | ✅ Verified | All 14 auto-archiving filters successfully deleted. |
| Label Creation | ✅ Verified | `00_Junk_Review`, `Bills & Payments`, and `School & Kids` labels are active. |
| Inbox Triage | ✅ Verified | Triaged all messages; junk archived, critical items labeled and kept in Inbox. |
| Deep Research Run (Batch 2) | ✅ Verified | Completed and saved Prompts 4, 5, and 6. |
| Deep Research Run (Batch 3) | ✅ Verified | Completed and saved Prompts 7, 8, and 9. |
| Deep Research Run (Batch 4) | ✅ Verified | Completed and saved Prompt 10. |
| Obsidian Vault Ingestion | ✅ Verified | All 10 high-end research logs indexed and stored inside [Research_Archives/](file:///C:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/Research_Archives/). |
| Git remote sync | ✅ Verified | Website adjustments, new landing page, and child theme changes committed and pushed. |
| Music Conductor CLI | ✅ Verified | music_conductor.py script created and copied to workspace. |

### 8. Music & Lyrics Conductor CLI (NEW)
Created and deployed [music_conductor.py](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/06_Music_Recomposition/music_conductor.py):
- **Curation Loop:** Terminal prompt system that scans `Desktop/New Songs/` directories for tracks.
- **Vertex AI Lyric Writer:** Generates desaturated, minimal deep house/organic house lyrics matching Wayne's biohacking (YLM) and civil construction (C) goals. Supports English, Spanish, and Italian.
- **Automation Integration:** Programmatically packages TooLost JSON metadata manifests and Musixmatch lyric sheets, and places files directly into `sounds/`, `ready for toolost/`, and `musicmacth/`.
- **Queue Syncer:** Automatically matches disk filenames to the table in [[06_Music_Recomposition/MUSIC_PRODUCTION_QUEUE|MUSIC_PRODUCTION_QUEUE]].md](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/06_Music_Recomposition/[[06_Music_Recomposition/MUSIC_PRODUCTION_QUEUE|MUSIC_PRODUCTION_QUEUE]].md) and updates titles and statuses.


---
📁 **See also:** [[MAP_OF_CONTENTS|← Directory Index]]
