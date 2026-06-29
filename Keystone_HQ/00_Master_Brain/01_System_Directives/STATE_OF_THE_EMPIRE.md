---
id: doc-stateoftheempire
title: State Of The Empire
type: document
summary: 'LAST SYNCHRONIZED: 2026-06-14T16:47:00Z'
tags:
- davinci
- davinci-resolve
- document
- elevenlabs
- keystone-possibilities
- keystone-recomposition
- okf
- spotify
- youtube
created: '2026-05-23T18:43:31.291546'
updated: '2026-06-14T19:57:36.069223'
entities:
- DaVinci
- DaVinci Resolve
- ElevenLabs
- Keystone Possibilities
- Keystone Recomposition
- Spotify
- YouTube
---
# Sovereign Blackboard: State of the Empire
**LAST SYNCHRONIZED:** 2026-06-14T16:47:00Z  
**STATUS:** Master Ingestion Complete // Phase 1 Locked // System Check Clean  

---

## 1. Brand Identity & Operating Parameters
*   **The Brand:** Keystone Dual-Brand Empire.
    *   *Side A (B2B SaaS):* Keystone Possibilities (Custom dynamic multi-tenant estimation portal for contractors - Landscaping, Roofing, Custom Homes).
    *   *Side B (B2C Media):* Keystone Recomposition (Hormone/metabolic longevity optimization media, synthetic audiobooks, Spotify focus music distribution).
*   **Aesthetics:** High-end, premium dark-mode, minimalist typography (Outfit/Inter/Georgia), organic atmospheric audio, cinematic visual loops.
*   **Compliance:** Strict FDA/DSHEA compliance for supplement promotion. Strict YMYL compliance for YouTube scripts (scrubbing red-flag terms via `sovereign_coordinator.py`).

---

## 2. Active Technical Endpoints
*   **Possibilities Dynamic Portal:** Coded inside `possibilities-portal/`.
    *   *Middleware:* `src/middleware.ts` routes subdomains (`roofing`, `landscaping`) dynamically at the edge.
    *   *Styling:* Tailwind CSS v4 variables mapped directly inside `globals.css` for instant runtime theme rendering.
    *   *Email Delivery:* Serverless Gmail REST API in `src/app/api/contact-api/route.ts` utilizing OAuth2 and raw base64 MIME packets (Method B).
    *   *TWA Compiler:* Headless Bubblewrap project assembly (`twa-manifest.json`) bypassing interactive prompts inside isolated CI/CD runners.
    *   *Dynamic App Links:* Android 15 dynamic relation extensions with query fragments and staging/admin exclusions.
    *   *SaaS Publishing:* Decentralized multi-tenant Fastlane Match and Supply deployment pipelines to prevent Google Play cascading bans.
*   **Audiobook Project Space:** Located in `00_Master_Brain/Audiobook/`.
    *   *Direct Ingestion:* Spotify for Authors (commission-free direct release).
    *   *Wide Aggregator:* Voices by INaudio (Apple Books, Google Play distribution at 80/20 royalty split).
    *   *Mastering Standards:* Audacity ACX Macro (-20dB RMS, -3.5dBFS peak, 80Hz/16kHz roll-offs).
    *   *Dynamic Lexicon:* W3C PLS 1.0 XML Phonetic Lexicons with multilingual `<alias>` bypass checks.
    *   *Timeline Assembly:* ElevenLabs Studio Projects API (`/v1/studio/projects`) with HTML paragraph-level voice mappings.
    *   *E-Commerce:* Shopify $5/mo Starter tier mapped to Linkpop shoppable checkouts with automatic digital download fulfillment.
*   **Visual Assembly Space:** Located in `09_YouTube_Operations/Scripts_Approved/`.
    *   *Temporal Decay Boundary:* Enforced 8-second maximum duration checks to prevent mouth jitter and face warping.
    *   *Compositing Matting:* VP9-with-alpha transparent WebMs over DOM backgrounds, utilizing the two WebM browser playback rules.
    *   *Skill Choreography:* OpenClaw/MediaClaw metadata [[STATE|state]] exchange sheets (`AVATAR-WAYNE.md`, `AVATAR-ANNA.md`).

---

## 3. Active Task Roadmap & Next Steps
- [x] Scaffold Multi-Tenant Next.js Portal and Tailwind v4 themes.
- [x] Set up dynamic subdomains middleware and metadata manifests.
- [x] Stage Audiobook compilation workspace and spelling lexicon (`lexicon.json`).
- [x] Build automated ElevenLabs Audiobook synthesis python scripts (`audiobook_synthesizer.py`).
- [x] Build HeyGen automated video generation scripts with 8-second look-aways (`heygen_video_engine.py`).
- [x] Build B2B cold outreach email campaign engine (`sponsorship_outreach.py`).
- [x] Deploy persistent background Google Spark Antigravity SDK agent (`spark_agent.py`).
- [ ] Execute live ElevenLabs voice synthesis production runs for all chapters.
- [ ] Perform final video compilation assemblies in DaVinci Resolve using the whip-pan transitions.
- [ ] Launch live Shopify $5 Starter plan and register Linkpop shop funnels.
- [ ] Perform weekly compaction checks to keep prompt memory under 135k tokens.

---

## 4. Prompt Engineering & Blackboard Evolution Rules
Adhere to the **Sovereign Blackboard Update Rule** to prevent information decay and memory loss between chat sessions:

### 1. The Dynamic Evolution Directive
Whenever a milestone is achieved, an architectural pivot is made, or a new custom script is written, **immediately modify this document (`STATE_OF_THE_EMPIRE.md`)** to record the change.

### 2. "Google Flow" Prompt Construction Style
When writing prompts for subagents or configuring system instructions, use the **Continuous Semantic Anchoring** structure:
*   **Role Anchor:** Define the agent's exact operational role and context (e.g. `[ROLE: Audiobook Synthesizer Engine]`).
*   **Blackboard Sync:** Instruct the agent to read `STATE_OF_THE_EMPIRE.md` first.
*   **Operational Directives (Markdown Checklist):** Use strict, bulleted instructions.
*   **Output Constraint:** Define exact JSON or structured markdown schemas.
*   **Feedback Hook:** End with instructions on how to write progress back to the Blackboard.

*Example Prompt Style:*
```markdown
[CONTEXT: B2C Media Engine Launch]
1. Read STATE_OF_THE_EMPIRE.md Section 2 to resolve active endpoints.
2. Read AUDIOBOOK_SOP.md Phase 1 to capture ElevenLabs stability configurations (0.60 Stability / 0.15 Style).
3. Execute the Python synthesis script and download WAV chapters to Audiobook/01_Raw_Voice/.
4. Upon successful chapter creation, write the updated milestone into STATE_OF_THE_EMPIRE.md Section 3 and alert the coordinator.
```