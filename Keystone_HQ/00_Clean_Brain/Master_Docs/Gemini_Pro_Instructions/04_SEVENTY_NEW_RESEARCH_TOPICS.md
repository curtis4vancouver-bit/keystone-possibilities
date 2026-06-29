---
id: doc-04seventynewresearchtopics
title: Seventy New Research Topics
type: document
summary: '> For: Gemini 3.1 Pro (autonomous execution via Chrome Deep Research)'
entities:
- BPC-157
- Bill 44
- DaVinci
- DaVinci Resolve
- ElevenLabs
- Keystone Possibilities
- Keystone Recomposition
- Kling
- Runway
- Sea-to-Sky
- Spotify
- Squamish
- Suno
- Udio
- Vancouver
- Whistler
- YouTube
created: '2026-06-10T08:27:22.172207'
updated: '2026-06-14T19:57:36.105349'
---
# INSTRUCTION SET 4: 70 New Deep Research Topics for Tonight
> **For:** [[GEMINI|Gemini]] 3.1 Pro (autonomous execution via Chrome Deep Research)  
> **Created:** 2026-06-10 by Antigravity  
> **Purpose:** Next-level research topics across all Keystone verticals  
> **Method:** Use `keystone-chrome-research-automation` [[davinci-resolve-mcp/docs/SKILL|skill]] or `keystone-overnight-sweep-monitor` [[davinci-resolve-mcp/docs/SKILL|skill]]  
> **Credit Budget:** 30 prompts per 5-hour window (Google Deep Research limits)

---

<!-- CONTEXT: Seventy New Research Topics / HOW TO USE THIS LIST -->
## HOW TO USE THIS LIST

Each topic has:
- **Domain tag** — For filing in the correct Research_Archives subfolder
- **Priority** — 🔴 HIGH (do first), 🟡 MEDIUM, 🟢 LOW
- **Research prompt** — The exact prompt to paste into Google Deep Research

After each research completes:
1. Save the output to `Research_Archives/{domain_folder}/`
2. Use naming format: `20260610_{DOMAIN}_{first_60_chars_of_topic}.md`
3. Ingest into the Qdrant brain using `ingest_to_brain` MCP tool

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 1: ADVANCED AGENT [[ARCHITECTURE|ARCHITECTURE]] (Topics 1-10) -->
## CATEGORY 1: ADVANCED AGENT ARCHITECTURE (Topics 1-10)

<!-- CONTEXT: Seventy New Research Topics / 1. 🔴 [AGENT_ARCH] Context Engram Protocol -->
### 1. 🔴 [AGENT_ARCH] Context Engram Protocol
```
Deep research into "Context Engrams" for AI agent memory management. How do frameworks like Antigravity SDK, LangGraph, and CrewAI implement persistent memory that survives across conversation sessions without context window overflow? Include implementation patterns for mem_save() and mem_search() functions, compression algorithms for long-term storage, and strategies for preventing memory staleness. Focus on 2026 best practices.
```

<!-- CONTEXT: Seventy New Research Topics / 2. 🔴 [AGENT_ARCH] PreToolUse Hook Security Patterns -->
### 2. 🔴 [AGENT_ARCH] PreToolUse Hook Security Patterns
```
Deep research into PreToolUse and PostToolUse lifecycle hooks for AI agents in 2026. How to implement synchronous tool-call interception that blocks dangerous commands, mutates tool arguments for safety (e.g., injecting --dry-run), and logs all tool executions for audit trails. Include implementation specs for Claude Code hooks, Antigravity SDK hooks, and ADK 2.0 hooks. Focus on patterns that prevent prompt injection attacks via tool arguments.
```

<!-- CONTEXT: Seventy New Research Topics / 3. 🟡 [AGENT_ARCH] Circuit Breaker Patterns for Autonomous [[AGENTS|Agents]] -->
### 3. 🟡 [AGENT_ARCH] Circuit Breaker Patterns for Autonomous [[AGENTS|Agents]]
```
Deep research into circuit breaker algorithms for autonomous AI agents. How to detect infinite loops, no-progress states, and repeated error fingerprints in long-running agent tasks. Include the three diagnostic heuristics: No-Progress Trigger, Same-Error Fingerprint (hash-based), and Token Decline Metric. Compare implementations in LangGraph, ADK 2.0, and the-architect system. Include code examples for Python.
```

<!-- CONTEXT: Seventy New Research Topics / 4. 🟡 [AGENT_ARCH] A2A Protocol (Agent-to-Agent) Implementation -->
### 4. 🟡 [AGENT_ARCH] A2A Protocol (Agent-to-Agent) Implementation
```
Deep research into Google's Agent-to-Agent (A2A) protocol released at Cloud Next 2026. How do autonomous agents discover, authenticate with, and delegate tasks to other agents across organizational boundaries? Include the complete handshake protocol, capability advertisement, task delegation patterns, and security isolation between agents. Compare with MCP for tool access vs A2A for agent coordination.
```

<!-- CONTEXT: Seventy New Research Topics / 5. 🟡 [AGENT_ARCH] Dynamic Prompt Injection for Subagent Delegation -->
### 5. 🟡 [AGENT_ARCH] Dynamic Prompt Injection for Subagent Delegation
```
Research the best practices for safely injecting context into subagent prompts in multi-agent systems (2026). How should a master orchestrator pre-load relevant memory, skills, and constraints into a subagent's prompt WITHOUT letting the subagent access the full skill registry or memory store? Include patterns from Antigravity SDK, Google ADK 2.0, and CrewAI. Focus on preventing context window bloat and maintaining security boundaries.
```

<!-- CONTEXT: Seventy New Research Topics / 6. 🟢 [AGENT_ARCH] Evaluation Harness Design for Agent Skills -->
### 6. 🟢 [AGENT_ARCH] Evaluation Harness Design for Agent Skills
```
Deep research into building evaluation harnesses for autonomous AI agent skills. How to design sandboxed test suites that validate agent skills before deployment, including fixture assertions, deterministic output validation, and regression testing for prompt changes. Include patterns for Python subprocess isolation and AST-level code safety scanning.
```

<!-- CONTEXT: Seventy New Research Topics / 7. 🟢 [AGENT_ARCH] Dream Engine and Memory Consolidation -->
### 7. 🟢 [AGENT_ARCH] Dream Engine and Memory Consolidation
```
Research biologically-inspired memory consolidation systems for AI agents. How do "dream engines" use Ebbinghaus forgetting curves to score, consolidate, prune, and promote memories during idle periods? Include implementation specs for nightly consolidation jobs that compress episodic memory into semantic memory, and strategies for detecting memory staleness.
```

<!-- CONTEXT: Seventy New Research Topics / 8. 🟡 [AGENT_ARCH] FastMCP Server Development Guide -->
### 8. 🟡 [AGENT_ARCH] FastMCP Server Development Guide
```
Complete guide to building custom MCP servers using the FastMCP Python framework in 2026. Step-by-step tutorial covering tool definition, Pydantic input/output schemas, state management via SQLite, authentication via environment variables, and deployment. Include examples of wrapping REST APIs and local Python scripts as MCP tools. Focus on Windows compatibility.
```

<!-- CONTEXT: Seventy New Research Topics / 9. 🔴 [AGENT_ARCH] Google Workspace MCP Server Setup on Windows -->
### 9. 🔴 [AGENT_ARCH] Google Workspace MCP Server Setup on Windows
```
Step-by-step guide to installing and configuring the Google Workspace MCP Server (gws CLI) on Windows 11 in 2026. Cover Google Cloud project creation, OAuth credential generation, CLI authentication, and binding to Antigravity/Gemini. Include known Windows-specific issues (gcloud.cmd path resolution failures) and workarounds. Cover Gmail, Drive, Calendar, and Chat MCP tools. Include the complete mcp_config.json entry.
```

<!-- CONTEXT: Seventy New Research Topics / 10. 🔴 [AGENT_ARCH] DaVinci Resolve MCP Server Architecture -->
### 10. 🔴 [AGENT_ARCH] DaVinci Resolve MCP Server Architecture
```
Deep research into building a Model Context Protocol (MCP) server that wraps the DaVinci Resolve Python scripting API. Cover timeline manipulation (add/remove clips, set in/out points), color grading automation (LUT application, color wheels), Fusion node creation (text overlays, lower thirds), render queue management, and project/timeline switching. Include the FastMCP implementation pattern and Pydantic schemas for each tool. Focus on DaVinci Resolve 19+ scripting API.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 2: VIDEO PRODUCTION & AI CONTENT (Topics 11-22) -->
## CATEGORY 2: VIDEO PRODUCTION & AI CONTENT (Topics 11-22)

<!-- CONTEXT: Seventy New Research Topics / 11. 🔴 [VIDEO_PROD] Google Flow Advanced Prompting 2026 -->
### 11. 🔴 [VIDEO_PROD] Google Flow Advanced Prompting 2026
```
Advanced prompt engineering for Google Flow (labs.google/fx/tools/flow) video generation in June 2026. What are the latest model updates, new features, and optimal prompt structures for generating consistent AI avatar characters? Cover aspect ratio control, scene composition, camera angles, lighting, and how to maintain character identity across multiple clips. Include batch processing strategies.
```

<!-- CONTEXT: Seventy New Research Topics / 12. 🟡 [VIDEO_PROD] AI [[music|Music]] Video Production Pipeline -->
### 12. 🟡 [VIDEO_PROD] AI Music Video Production Pipeline
```
Research the complete 2026 pipeline for producing AI-generated music videos. From lyrics → music generation (Suno, Udio) → visual generation (Google Flow, Veo 3.1, Runway Gen-4) → editing (DaVinci Resolve) → publishing. What are the copyright and licensing implications? Include distribution strategies for Spotify, Apple Music, YouTube Music.
```

<!-- CONTEXT: Seventy New Research Topics / 13. 🟡 [VIDEO_PROD] Interview-Format AI Video Production -->
### 13. 🟡 [VIDEO_PROD] Interview-Format AI Video Production
```
Deep research into producing interview-format AI videos where two AI avatars have a natural conversation. How to write scripts with natural pacing (pauses, interruptions, reactions), generate matching lip-sync clips, and assemble multi-angle timelines. Include the specific Google Flow prompt patterns for generating reaction shots and over-the-shoulder angles.
```

<!-- CONTEXT: Seventy New Research Topics / 14. 🟡 [VIDEO_PROD] YouTube Shorts Algorithm 2026 Deep Dive -->
### 14. 🟡 [VIDEO_PROD] YouTube Shorts Algorithm 2026 Deep Dive
```
Deep research into the YouTube Shorts algorithm as of June 2026. What factors determine Shorts visibility: watch time, replay rate, engagement velocity, posting frequency? How does the new Shorts monetization model work? What's the optimal posting schedule, hook structure, and call-to-action placement? Include data from creator case studies showing what's working RIGHT NOW.
```

<!-- CONTEXT: Seventy New Research Topics / 15. 🟡 [VIDEO_PROD] Topaz Video AI Upscaling Integration -->
### 15. 🟡 [VIDEO_PROD] Topaz Video AI Upscaling Integration
```
Research Topaz Video AI upscaling workflow for AI-generated video content in 2026. How to batch-process Google Flow clips through Topaz for resolution enhancement, noise reduction, and frame interpolation. Include CLI/scripting options for automation, optimal settings for 9:16 vertical video, and quality comparison benchmarks.
```

<!-- CONTEXT: Seventy New Research Topics / 16. 🟢 [VIDEO_PROD] AI Thumbnail Generation Best Practices -->
### 16. 🟢 [VIDEO_PROD] AI Thumbnail Generation Best Practices
```
Research AI-generated YouTube thumbnail design in 2026. What visual elements drive highest click-through rates: face close-ups, text overlays, contrast, color psychology? How to use AI image generation (Gemini, DALL-E, Midjourney) to create thumbnails that match the video content. Include A/B testing strategies and CTR benchmarks by niche (construction, health, music).
```

<!-- CONTEXT: Seventy New Research Topics / 17. 🟢 [VIDEO_PROD] Automated Subtitle and Caption Generation -->
### 17. 🟢 [VIDEO_PROD] Automated Subtitle and Caption Generation
```
Research automated subtitle generation for YouTube videos in 2026. Compare Whisper, AssemblyAI, and YouTube's auto-captions for accuracy. How to generate styled SRT/ASS files for DaVinci Resolve import. Include multi-language subtitle generation for reaching non-English audiences in the Sea-to-Sky corridor (Chinese, Tagalog, Hindi).
```

<!-- CONTEXT: Seventy New Research Topics / 18. 🟡 [VIDEO_PROD] Audiobook Production Pipeline -->
### 18. 🟡 [VIDEO_PROD] Audiobook Production Pipeline
```
Complete guide to producing and distributing audiobooks using AI voice synthesis in 2026. Cover text-to-speech engines (ElevenLabs, Google TTS, Amazon Polly), audio post-processing, chapter splitting, metadata standards (ID3 tags, ONIX), and distribution platforms (Audible/ACX, Google Play Books, Spotify Audiobooks, Apple Books). Include Shopify integration for direct sales.
```

<!-- CONTEXT: Seventy New Research Topics / 19. 🟢 [VIDEO_PROD] DaVinci Resolve Fusion Automation -->
### 19. 🟢 [VIDEO_PROD] DaVinci Resolve Fusion Automation
```
Deep research into automating DaVinci Resolve Fusion compositions via the Python scripting API. How to programmatically create text overlays, lower thirds, animated titles, and transition effects. Include templates for branded intro/outro sequences, subscriber count overlays, and call-to-action animations. Focus on Fusion scripting in Resolve 19+.
```

<!-- CONTEXT: Seventy New Research Topics / 20. 🟡 [VIDEO_PROD] Multi-Platform Video Format Optimization -->
### 20. 🟡 [VIDEO_PROD] Multi-Platform Video Format Optimization
```
Research optimal video encoding settings for each platform in 2026: YouTube (Shorts + Long-form), TikTok, Instagram Reels, Facebook Reels, LinkedIn Video. Cover resolution, bitrate, codec (AV1 vs H.265 vs H.264), frame rate, color space, and audio specifications. Include DaVinci Resolve render preset configurations for each platform.
```

<!-- CONTEXT: Seventy New Research Topics / 21. 🟢 [VIDEO_PROD] AI B-Roll Library Management -->
### 21. 🟢 [VIDEO_PROD] AI B-Roll Library Management
```
Research strategies for building and managing a reusable AI-generated B-roll library. How to categorize, tag, and retrieve AI-generated images and video clips for rapid timeline assembly. Include folder structure recommendations, metadata tagging schemas, and search/retrieval methods using vector similarity.
```

<!-- CONTEXT: Seventy New Research Topics / 22. 🔴 [VIDEO_PROD] Veo 3.1 vs Google Flow vs Runway Gen-4 Comparison -->
### 22. 🔴 [VIDEO_PROD] Veo 3.1 vs Google Flow vs Runway Gen-4 Comparison
```
Comprehensive comparison of AI video generation platforms available in June 2026: Google Veo 3.1, Google Flow, Runway Gen-4 Turbo, Pika 2.2, Kling 2.0, and Sora. Compare video quality, consistency, prompt adherence, pricing, API access, and commercial usage rights. Which is best for construction marketing videos? Health content? Music videos? Include pricing per minute of generated video.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 3: SEO, GEO & CLIENT ACQUISITION (Topics 23-37) -->
## CATEGORY 3: SEO, GEO & CLIENT ACQUISITION (Topics 23-37)

<!-- CONTEXT: Seventy New Research Topics / 23. 🔴 [SEO] Wikidata Entity Creation for Local Businesses -->
### 23. 🔴 [SEO] Wikidata Entity Creation for Local Businesses
```
Step-by-step guide to creating a Wikidata entity for a local construction business in 2026. What properties are required (P31 instance of, P17 country, P131 located in, P856 website, P112 founder)? What evidence/sources does Wikidata require to verify a business entity? How does a Wikidata presence feed into ChatGPT, Perplexity, and Google Knowledge Panel recommendations? Include the complete creation workflow.
```

<!-- CONTEXT: Seventy New Research Topics / 24. 🔴 [SEO] Bing Places Optimization for ChatGPT Visibility -->
### 24. 🔴 [SEO] Bing Places Optimization for ChatGPT Visibility
```
Deep research into optimizing a Bing Places for Business listing specifically for ChatGPT visibility in 2026. ChatGPT uses Bing's index as its primary local data source. What fields matter most? How to verify and claim a listing? What's the review threshold for ChatGPT recommendations (4.3+ stars)? Include the complete setup process and optimization checklist.
```

<!-- CONTEXT: Seventy New Research Topics / 25. 🔴 [SEO] Google Knowledge Panel Acquisition Strategy -->
### 25. 🔴 [SEO] Google Knowledge Panel Acquisition Strategy
```
Research how to acquire a Google Knowledge Panel for a local construction business in 2026. What triggers Google to create a Knowledge Panel? How do sameAs schema, Wikidata entities, and consistent NAP data contribute? Include the process for claiming and editing an existing panel, and strategies for building the entity signals that trigger panel creation.
```

<!-- CONTEXT: Seventy New Research Topics / 26. 🟡 [SEO] Reddit Strategy for Perplexity AI Visibility -->
### 26. 🟡 [SEO] Reddit Strategy for Perplexity AI Visibility
```
Deep research into building a Reddit presence specifically for Perplexity AI citation. Perplexity cites Reddit in 46.7% of top responses. What subreddits matter for construction (r/HomeImprovement, r/construction, r/britishcolumbia)? How to build authentic engagement that gets cited by AI without being seen as spam? Include a monthly posting cadence and content strategy.
```

<!-- CONTEXT: Seventy New Research Topics / 27. 🟡 [SEO] WordPress Schema Deployment Without Breaking Sites -->
### 27. 🟡 [SEO] WordPress Schema Deployment Without Breaking Sites
```
Technical guide to deploying JSON-LD structured data on WordPress sites without breaking anything. Compare methods: code snippets plugin (WPCode), theme functions.php injection, Yoast SEO schema editor, RankMath schema blocks. Which is safest for non-developers? How to test before deployment? How to rollback if something breaks? Include WordPress-specific gotchas.
```

<!-- CONTEXT: Seventy New Research Topics / 28. 🟡 [SEO] Automated Blog-to-Video Content Loop -->
### 28. 🟡 [SEO] Automated Blog-to-Video Content Loop
```
Research the technical implementation of an automated blog-to-video traffic loop in 2026. When a YouTube video is published, automatically generate a companion blog post with embedded video, extracted transcript, and FAQ schema. Cover WordPress REST API for automated posting, transcript extraction methods, and SEO optimization of the generated blog post. Include the complete automation pipeline.
```

<!-- CONTEXT: Seventy New Research Topics / 29. 🟡 [SEO] Local Link Building for BC Construction Companies -->
### 29. 🟡 [SEO] Local Link Building for BC Construction Companies
```
Research effective link building strategies for construction companies in British Columbia in 2026. What local organizations, chambers of commerce, industry associations (CHBA, BCCA), and community groups provide high-authority backlinks? How to get featured in local media (Squamish Chief, Pique Newsmagazine)? Include a prioritized list of link targets for the Sea-to-Sky corridor.
```

<!-- CONTEXT: Seventy New Research Topics / 30. 🟡 [SEO] Google AI Mode and AI Overviews Optimization -->
### 30. 🟡 [SEO] Google AI Mode and AI Overviews Optimization
```
Deep research into optimizing for Google AI Mode and AI Overviews in 2026. How does Google's generative search differ from traditional organic? What content structures get cited in AI Overviews? The OtterlyAI study showed 611% increase in citations from schema markup. What specific optimizations work? Include before/after case studies.
```

<!-- CONTEXT: Seventy New Research Topics / 31. 🟢 [SEO] Review Generation Strategy for AI Visibility -->
### 31. 🟢 [SEO] Review Generation Strategy for AI Visibility
```
Research automated review generation and response strategies that boost AI search visibility in 2026. How to systematically collect reviews on Google, Yelp, HomeStars, and BBB. What review content patterns (specific project details, technical terms) are most valuable for AI extraction? How does review response rate affect visibility? Include email templates and timing strategies.
```

<!-- CONTEXT: Seventy New Research Topics / 32. 🟢 [SEO] Competitor SEO Analysis: Top Squamish Contractors -->
### 32. 🟢 [SEO] Competitor SEO Analysis: Top Squamish Contractors
```
Deep competitive analysis of the top 10 contractors in Squamish/Whistler BC for SEO and AI visibility. Who currently appears in ChatGPT, Perplexity, and Gemini responses for "best contractor in Squamish"? What are their schema implementations, review counts, citation profiles, and content strategies? Identify specific gaps Keystone Possibilities can exploit.
```

<!-- CONTEXT: Seventy New Research Topics / 33. 🟡 [SEO] HomeStars and Houzz Optimization for Contractors -->
### 33. 🟡 [SEO] HomeStars and Houzz Optimization for Contractors
```
Complete guide to optimizing HomeStars and Houzz profiles for Canadian construction companies in 2026. What fields drive the most visibility? How does HomeStars' Star Score algorithm work? What portfolio content performs best on Houzz? How do these platforms feed into AI search engines? Include profile optimization checklists for both platforms.
```

<!-- CONTEXT: Seventy New Research Topics / 34. 🟢 [SEO] Service Page Architecture for Construction Websites -->
### 34. 🟢 [SEO] Service Page Architecture for Construction Websites
```
Research optimal service page architecture for construction company websites targeting both traditional SEO and AI search in 2026. How should services be structured (individual pages vs grouped)? What content elements are required (pricing ranges, timelines, process steps, FAQs)? Include wireframe templates and content outlines for: custom homes, renovations, project management, and permits.
```

<!-- CONTEXT: Seventy New Research Topics / 35. 🟡 [SEO] Google Business Profile Advanced Optimization 2026 -->
### 35. 🟡 [SEO] Google Business Profile Advanced Optimization 2026
```
Deep research into advanced Google Business Profile optimization for construction companies in 2026. Beyond basic NAP: how to use categories, attributes, products/services, Q&A, and Google Posts for maximum AI visibility. How does Google Vision AI analyze uploaded photos? What photo types build authenticity vs trigger weak-authenticity signals? Include a weekly GBP management routine.
```

<!-- CONTEXT: Seventy New Research Topics / 36. 🟢 [SEO] AI Content Detection and Disclosure Requirements -->
### 36. 🟢 [SEO] AI Content Detection and Disclosure Requirements
```
Research the current legal and platform requirements for disclosing AI-generated content in 2026. What are YouTube's AI disclosure rules? Google's stance on AI-generated blog posts? How does the EU AI Act affect content marketing? What are the best practices for using AI-generated content without triggering penalties? Include platform-by-platform disclosure requirements.
```

<!-- CONTEXT: Seventy New Research Topics / 37. 🟡 [SEO] Programmatic SEO for Construction Niches -->
### 37. 🟡 [SEO] Programmatic SEO for Construction Niches
```
Research programmatic SEO strategies for construction companies in 2026. How to automatically generate hundreds of location-specific and service-specific landing pages (e.g., "custom home construction in Whistler", "renovation permits in Squamish"). Include template structures, keyword patterns, and WordPress implementation methods that avoid Google's thin content penalties.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 4: BUSINESS DEVELOPMENT & MARKETING (Topics 38-48) -->
## CATEGORY 4: BUSINESS DEVELOPMENT & MARKETING (Topics 38-48)

<!-- CONTEXT: Seventy New Research Topics / 38. 🔴 [BUSINESS] LinkedIn B2B Lead Generation for Construction 2026 -->
### 38. 🔴 [BUSINESS] LinkedIn B2B Lead Generation for Construction 2026
```
Deep research into automated LinkedIn lead generation for a construction/project management company in 2026. Cover Sales Navigator features, connection request automation (without getting banned), content strategies that attract commercial clients, and CRM integration. What LinkedIn content formats drive the most leads for B2B construction services? Include a 30-day LinkedIn playbook.
```

<!-- CONTEXT: Seventy New Research Topics / 39. 🟡 [BUSINESS] Automated PR Pitching for Local Media -->
### 39. 🟡 [BUSINESS] Automated PR Pitching for Local Media
```
Research automated public relations outreach for local businesses in 2026. How to identify relevant journalists and media outlets (Squamish Chief, Pique Newsmagazine, BC Business, Vancouver Sun), craft AI-assisted pitch emails, and manage media relationships at scale. Include email templates, timing strategies, and tools like HARO/Connectively for earning media coverage.
```

<!-- CONTEXT: Seventy New Research Topics / 40. 🟡 [BUSINESS] Low-Cost Meta and YouTube Ads for Local Contractors -->
### 40. 🟡 [BUSINESS] Low-Cost Meta and YouTube Ads for Local Contractors
```
Complete guide to running highly targeted, low-budget ($500-2000/month) advertising campaigns on Meta (Facebook/Instagram) and YouTube for a local construction company in 2026. Cover audience targeting by geography (Sea-to-Sky corridor), interest, and income level. Include ad creative best practices, A/B testing frameworks, and ROI tracking methods.
```

<!-- CONTEXT: Seventy New Research Topics / 41. 🟢 [BUSINESS] Micro-Influencer Marketing for Local Services -->
### 41. 🟢 [BUSINESS] Micro-Influencer Marketing for Local Services
```
Research micro-influencer outreach strategies for local service businesses in 2026. How to identify and partner with local BC influencers (1K-50K followers) for construction/home improvement content. What compensation models work? How to measure ROI? Include platforms for finding local influencers and outreach templates.
```

<!-- CONTEXT: Seventy New Research Topics / 42. 🟡 [BUSINESS] Email Marketing Automation for Contractors -->
### 42. 🟡 [BUSINESS] Email Marketing Automation for Contractors
```
Research email marketing automation for construction companies in 2026. How to build a subscriber list, segment by interest (custom homes, renovations, commercial), create automated drip sequences, and track conversions. Compare platforms: Mailchimp, ConvertKit, ActiveCampaign, Brevo. Include email templates for different stages of the sales funnel.
```

<!-- CONTEXT: Seventy New Research Topics / 43. 🟢 [BUSINESS] Referral Program Design for Home Builders -->
### 43. 🟢 [BUSINESS] Referral Program Design for Home Builders
```
Research referral program strategies for residential construction companies. How to incentivize past clients to refer new business. What reward structures work best (cash, discounts, gifts)? How to automate referral tracking and reward fulfillment? Include legal considerations for BC real estate referral laws.
```

<!-- CONTEXT: Seventy New Research Topics / 44. 🟡 [BUSINESS] Shopify Store for Construction Consultation Services -->
### 44. 🟡 [BUSINESS] Shopify Store for Construction Consultation Services
```
Research setting up a Shopify store for selling construction consultation services, project management templates, and digital products (e.g., permit checklists, renovation guides). Cover payment processing, booking integration, and SEO for service-based Shopify stores. Include pricing strategy research for professional services.
```

<!-- CONTEXT: Seventy New Research Topics / 45. 🟢 [BUSINESS] Google Local Service Ads for Contractors -->
### 45. 🟢 [BUSINESS] Google Local Service Ads for Contractors
```
Research Google Local Service Ads (LSAs) for construction companies in British Columbia in 2026. How do LSAs differ from regular Google Ads? What's the cost per lead? How does the Google Guaranteed badge affect trust? Include setup requirements, budget recommendations, and performance benchmarks for the construction category.
```

<!-- CONTEXT: Seventy New Research Topics / 46. 🟡 [BUSINESS] Commercial Construction Client Acquisition -->
### 46. 🟡 [BUSINESS] Commercial Construction Client Acquisition
```
Deep research into acquiring commercial construction clients (strata, commercial buildings, institutional) in the Sea-to-Sky corridor. What procurement processes do commercial clients use? Where do they search for contractors? What qualifications and certifications are required? Include strategies for winning RFPs and building relationships with property managers.
```

<!-- CONTEXT: Seventy New Research Topics / 47. 🟢 [BUSINESS] Construction Industry Awards and Certifications BC -->
### 47. 🟢 [BUSINESS] Construction Industry Awards and Certifications BC
```
Research construction industry awards, certifications, and recognitions available in British Columbia. What organizations offer awards (CHBA, UDI, VRCA, GVHBA)? How do awards affect AI search visibility (Perplexity weights "Industry Awards" heavily)? Include application processes, timelines, and portfolio requirements for major awards.
```

<!-- CONTEXT: Seventy New Research Topics / 48. 🟢 [BUSINESS] Bill 44 Content Marketing Strategy -->
### 48. 🟢 [BUSINESS] Bill 44 Content Marketing Strategy
```
Deep research into creating content marketing around BC's Bill 44 (housing legislation). What are homeowners searching for regarding Bill 44 compliance? What renovation requirements does it create? How can a construction company position itself as the expert authority on Bill 44 compliance in the Sea-to-Sky corridor? Include keyword research and content calendar.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 5: HEALTH/WELLNESS CONTENT (Topics 49-55) -->
## CATEGORY 5: HEALTH/WELLNESS CONTENT (Topics 49-55)

<!-- CONTEXT: Seventy New Research Topics / 49. 🟡 [HEALTH] Peptide Science Content Compliance 2026 -->
### 49. 🟡 [HEALTH] Peptide Science Content Compliance 2026
```
Deep research into creating legally compliant educational content about peptides and wellness protocols in 2026. What are the FDA, Health Canada, and FTC regulations for discussing peptides (BPC-157, TB-500, Semaglutide) in online content? What disclaimers are required? How to cite peer-reviewed sources properly? Include a compliance checklist for YouTube and blog content.
```

<!-- CONTEXT: Seventy New Research Topics / 50. 🟡 [HEALTH] Health Content SEO for AI Citation -->
### 50. 🟡 [HEALTH] Health Content SEO for AI Citation
```
Research optimizing health and wellness content specifically for AI search engine citation in 2026. How do ChatGPT, Perplexity, and Gemini handle YMYL (Your Money Your Life) health queries differently? What E-E-A-T signals are mandatory for health content? How to structure articles so AI engines cite them without risk of liability? Include comparison of what gets cited vs what gets flagged.
```

<!-- CONTEXT: Seventy New Research Topics / 51. 🟢 [HEALTH] Wellness Retreat Marketing and Lead Generation -->
### 51. 🟢 [HEALTH] Wellness Retreat Marketing and Lead Generation
```
Research digital marketing strategies for promoting wellness retreats in British Columbia in 2026. Cover booking platform selection, social media marketing for wellness tourism, SEO for retreat-related keywords, and influencer partnerships. Include pricing strategy research for premium wellness experiences in the Sea-to-Sky corridor.
```

<!-- CONTEXT: Seventy New Research Topics / 52. 🟢 [HEALTH] PubMed Citation Workflow for Content Creators -->
### 52. 🟢 [HEALTH] PubMed Citation Workflow for Content Creators
```
Step-by-step guide for content creators to find, verify, and properly cite PubMed research in health content. How to search PubMed effectively, evaluate study quality (RCT vs observational), check retraction status, and format citations for YouTube descriptions and blog posts. Include the PubMed API for automated citation lookup.
```

<!-- CONTEXT: Seventy New Research Topics / 53. 🟢 [HEALTH] Podcast Production Pipeline for Wellness Content -->
### 53. 🟢 [HEALTH] Podcast Production Pipeline for Wellness Content
```
Research starting a health/wellness podcast in 2026 as part of the Recomposition brand. Cover recording equipment, hosting platforms (Spotify for Podcasters, Apple Podcasts, RSS.com), episode structure, guest booking automation, and cross-promotion with YouTube content. Include strategies for podcast SEO and AI discoverability.
```

<!-- CONTEXT: Seventy New Research Topics / 54. 🟡 [HEALTH] Medical Disclaimer and AI Disclosure Standards -->
### 54. 🟡 [HEALTH] Medical Disclaimer and AI Disclosure Standards
```
Deep research into the legal requirements for medical disclaimers and AI content disclosure on health YouTube channels and websites in 2026. What specific disclaimer language is required by US/Canadian regulations? Where must disclaimers appear (video, description, website)? How do YouTube's AI disclosure policies interact with health content rules?
```

<!-- CONTEXT: Seventy New Research Topics / 55. 🟢 [HEALTH] Supplement and Nootropic Content Strategy -->
### 55. 🟢 [HEALTH] Supplement and Nootropic Content Strategy
```
Research content marketing strategy for educational supplement and nootropic content in 2026. What topics drive the most search volume and lowest competition? How to position content as educational rather than promotional to avoid FTC/Health Canada issues? Include keyword research for popular supplements and a 3-month content calendar.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 6: MUSIC BRAND (Topics 56-60) -->
## CATEGORY 6: MUSIC BRAND (Topics 56-60)

<!-- CONTEXT: Seventy New Research Topics / 56. 🟡 [MUSIC] AI Music Distribution Strategy 2026 -->
### 56. 🟡 [MUSIC] AI Music Distribution Strategy 2026
```
Complete guide to distributing AI-generated music across all platforms in 2026. Cover DistroKid, TuneCore, CD Baby policies on AI music. How to properly credit AI-generated compositions. Spotify's AI content policies. Apple Music requirements. ISRC code generation. MusicBrainz cataloging. Include a step-by-step distribution checklist.
```

<!-- CONTEXT: Seventy New Research Topics / 57. 🟢 [MUSIC] Spotify Algorithm and Playlist Placement -->
### 57. 🟢 [MUSIC] Spotify Algorithm and Playlist Placement
```
Deep research into the Spotify algorithm for independent artists in 2026. How to get placed on algorithmic playlists (Discover Weekly, Release Radar). What metrics matter most (save rate, completion rate, skip rate)? How to build a listener base from zero. Include strategies for Spotify for Artists optimization and playlist pitching.
```

<!-- CONTEXT: Seventy New Research Topics / 58. 🟢 [MUSIC] AI Music Video Visual Style Guide -->
### 58. 🟢 [MUSIC] AI Music Video Visual Style Guide
```
Research establishing a consistent visual identity for AI-generated music videos. How to maintain a signature aesthetic across multiple video productions using Google Flow, Veo, and other AI tools. Cover color grading presets, recurring visual motifs, character design consistency, and branded elements. Include a visual style guide template.
```

<!-- CONTEXT: Seventy New Research Topics / 59. 🟢 [MUSIC] Sync Licensing for AI-Generated Music -->
### 59. 🟢 [MUSIC] Sync Licensing for AI-Generated Music
```
Research sync licensing opportunities for AI-generated music in 2026. Can AI music be placed in TV shows, commercials, podcasts, and video games? What platforms facilitate sync deals (Musicbed, Artlist, Epidemic Sound)? What are the legal ownership implications? Include revenue expectations and submission requirements.
```

<!-- CONTEXT: Seventy New Research Topics / 60. 🟢 [MUSIC] Recomposition Brand [[Brand_Constitution/protocol/IDENTITY|Identity]] and Audience Building -->
### 60. 🟢 [MUSIC] Recomposition Brand [[Brand_Constitution/protocol/IDENTITY|Identity]] and Audience Building
```
Research brand identity development for a music project called "Keystone Recomposition" that blends AI-generated music with wellness and mindfulness themes. How to build an authentic audience for a brand at the intersection of technology and wellness. Include social media strategy, content pillars, and community building tactics.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 7: TAX, LEGAL & CORPORATE (Topics 61-65) -->
## CATEGORY 7: TAX, LEGAL & CORPORATE (Topics 61-65)

<!-- CONTEXT: Seventy New Research Topics / 61. 🟡 [TAX_LEGAL] Canadian Small Business Tax Optimization 2026 -->
### 61. 🟡 [TAX_LEGAL] Canadian Small Business Tax Optimization 2026
```
Deep research into tax optimization strategies for Canadian small businesses in 2026, specifically for a construction company and media company operating in BC. Cover incorporation benefits, SR&ED tax credits for AI development, home office deductions, vehicle expenses, and income splitting strategies. Include CRA audit triggers to avoid.
```

<!-- CONTEXT: Seventy New Research Topics / 62. 🟡 [TAX_LEGAL] AI Business Expenses Tax Deductions Canada -->
### 62. 🟡 [TAX_LEGAL] AI Business Expenses Tax Deductions Canada
```
Research what AI tool subscriptions, API costs, and software development expenses are tax-deductible for Canadian businesses in 2026. Cover Google AI Ultra ($100/mo), cloud computing costs, MCP server hosting, AI-generated content production tools. How to categorize these expenses for CRA compliance. Include relevant CRA tax codes.
```

<!-- CONTEXT: Seventy New Research Topics / 63. 🟢 [TAX_LEGAL] Construction Contractor Insurance Requirements BC -->
### 63. 🟢 [TAX_LEGAL] Construction Contractor Insurance Requirements BC
```
Research mandatory and recommended insurance coverage for construction contractors in British Columbia in 2026. Cover WorkSafeBC requirements, general liability, professional liability (E&O), builder's risk, and umbrella policies. What coverage levels are required for different project types? Include cost estimates for the Sea-to-Sky corridor.
```

<!-- CONTEXT: Seventy New Research Topics / 64. 🟢 [TAX_LEGAL] AI Content Liability and Copyright Canada -->
### 64. 🟢 [TAX_LEGAL] AI Content Liability and Copyright Canada
```
Deep research into the legal liability and copyright status of AI-generated content in Canada in 2026. Who owns AI-generated video, music, and text? What are the implications for publishing AI content commercially? How does Canadian copyright law (which requires a human author) affect AI content ownership? Include risk mitigation strategies.
```

<!-- CONTEXT: Seventy New Research Topics / 65. 🟢 [TAX_LEGAL] BC Construction Permit and Licensing Requirements -->
### 65. 🟢 [TAX_LEGAL] BC Construction Permit and Licensing Requirements
```
Comprehensive research into construction licensing, bonding, and permit requirements in British Columbia in 2026. What licenses does a general contractor need? How does the BC Housing registration work? What are the requirements for working in different Sea-to-Sky municipalities (Squamish, Whistler, SLRD)? Include a compliance checklist.
```

---

<!-- CONTEXT: Seventy New Research Topics / CATEGORY 8: INFRASTRUCTURE & AUTOMATION (Topics 66-70) -->
## CATEGORY 8: INFRASTRUCTURE & AUTOMATION (Topics 66-70)

<!-- CONTEXT: Seventy New Research Topics / 66. 🔴 [INFRA] Qdrant v1.18 Advanced Features and Hybrid Search -->
### 66. 🔴 [INFRA] Qdrant v1.18 Advanced Features and Hybrid Search
```
Deep research into Qdrant vector database version 1.18 features for AI agent memory. Cover hybrid search implementation (dense + sparse vectors), filterable HNSW architecture, binary quantization for memory efficiency, payload indexing strategies, and temporal filtering. Include Python code examples using qdrant-client v1.18.0 for all features. Focus on single-node deployment with Docker.
```

<!-- CONTEXT: Seventy New Research Topics / 67. 🔴 [INFRA] BGE-M3 Embedding Model Deployment Guide -->
### 67. 🔴 [INFRA] BGE-M3 Embedding Model Deployment Guide
```
Complete deployment guide for the BGE-M3 (BAAI General Embedding) model for local AI agent memory. Cover installation, configuration, and optimization for CPU-only execution on Windows. How to generate dense, sparse, and multi-vectors in a single forward pass. Include Python code for integration with Qdrant hybrid search. Compare performance vs sentence-transformers and OpenAI embeddings.
```

<!-- CONTEXT: Seventy New Research Topics / 68. 🟡 [INFRA] Docker Compose for AI Agent Infrastructure -->
### 68. 🟡 [INFRA] Docker Compose for AI Agent Infrastructure
```
Research building a Docker Compose configuration for an AI agent's local infrastructure stack. Cover Qdrant vector database, custom MCP servers, background daemons (overnight research, dream engine), and health monitoring. Include volume persistence, resource limits, health checks, and automatic restart policies. Focus on Windows Docker Desktop deployment.
```

<!-- CONTEXT: Seventy New Research Topics / 69. 🟡 [INFRA] WordPress REST API Automation for Content Publishing -->
### 69. 🟡 [INFRA] WordPress REST API Automation for Content Publishing
```
Deep research into automating WordPress content publishing via the REST API in 2026. How to programmatically create blog posts with featured images, categories, tags, and custom fields. Cover authentication methods (application passwords, JWT), media upload, and scheduled publishing. Include Python code examples and error handling for a construction company blog.
```

<!-- CONTEXT: Seventy New Research Topics / 70. 🟡 [INFRA] Overnight Research Automation Improvements -->
### 70. 🟡 [INFRA] Overnight Research Automation Improvements
```
Research improvements to autonomous overnight Chrome Deep Research automation in 2026. How to manage Google's credit limits (30 prompts/5hr window), implement smart queuing with priority ordering, handle stale tab detection, and generate morning reports. Include credit timing algorithms, error recovery patterns, and state persistence strategies. Compare with alternative research automation methods.
```

---

<!-- CONTEXT: Seventy New Research Topics / FILING REFERENCE -->
## FILING REFERENCE

When saving research results, use these folder mappings:

| Domain Tag | Research_Archives Subfolder |
|-----------|---------------------------|
| AGENT_ARCH | 01_Agent_Architecture |
| MCP_TOOLS | 02_MCP_Tools |
| VIDEO_PROD | 05_Video_Production |
| SEO | 08_SEO_Website |
| SOCIAL | 09_Social_Media |
| TAX_LEGAL | 10_Tax_Legal_Corporate |
| BUSINESS | 12_Branding_Marketing |
| HEALTH | 15_Content_Pipeline or create new 18_Health_Content |
| MUSIC | Create new 19_Music_Production |
| INFRA | 07_Coding_Optimization or create new 20_Infrastructure |


---
📁 **See also:** [[Master_Docs/Gemini_Pro_Instructions/INDEX|← Directory Index]]
