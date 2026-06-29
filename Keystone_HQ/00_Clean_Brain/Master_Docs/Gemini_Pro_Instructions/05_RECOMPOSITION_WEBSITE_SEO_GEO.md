---
id: doc-05recompositionwebsiteseogeo
title: Recomposition Website Seo Geo
type: document
summary: '> For: Gemini 3.1 Pro (autonomous execution)'
entities:
- BPC-157
- Keystone Possibilities
- Keystone Recomposition
- Sea-to-Sky
- Spotify
- Squamish
- Wayne Stevenson
- YouTube
created: '2026-06-10T08:33:08.231863'
updated: '2026-06-14T19:57:36.112663'
---
# INSTRUCTION SET 5: Keystone Recomposition Website SEO/GEO Implementation
> **For:** [[GEMINI|Gemini]] 3.1 Pro (autonomous execution)  
> **Created:** 2026-06-10 by Antigravity  
> **Purpose:** Deploy SEO/GEO optimizations to the Keystone Recomposition website (health/wellness/[[music|music]] brand)  
> **Estimated Time:** 2-3 hours  
> **Risk Level:** MEDIUM — modifying live website + YMYL (Your Money Your Life) health content  
> **Depends on:** Instruction Set 01 (Brain) should be done first. Set 03 is the SEPARATE [[possibilities|Possibilities]] site guide — DO NOT MIX.

---

<!-- CONTEXT: Recomposition Website Seo Geo / ⚠️ CRITICAL SAFETY RULES — HEALTH CONTENT -->
## ⚠️ CRITICAL SAFETY RULES — HEALTH CONTENT

1. **This is a YMYL (Your Money Your Life) site** — Google and AI engines apply EXTRA scrutiny to health content
2. **NEVER make medical claims** — All content must be educational, not prescriptive
3. **ALWAYS include medical disclaimers** — Every page with health content needs one
4. **ALWAYS cite peer-reviewed sources** — PubMed, FDA, Health Canada only
5. **NEVER say "cure", "treat", or "diagnose"** — Use "may support", "research suggests", "consult your healthcare provider"
6. **AI Disclosure is MANDATORY** — YouTube, blog, and social content must disclose AI generation
7. **NEVER modify WordPress core files** — Use Customizer, functions.php, or plugins
8. **ALWAYS back up before changes** — Export full WordPress site first

---

<!-- CONTEXT: Recomposition Website Seo Geo / CRITICAL CONTEXT -->
## CRITICAL CONTEXT

<!-- CONTEXT: Recomposition Website Seo Geo / Website: -->
### Website:
- **Keystone Recomposition**: keystonerecomposition.com (WordPress) — Health/wellness/music brand
- **NOT** keystonepossibilities.com — that's the construction brand (covered in Set 03)

<!-- CONTEXT: Recomposition Website Seo Geo / Brand [[Brand_Constitution/protocol/IDENTITY|Identity]]: -->
### Brand [[Brand_Constitution/protocol/IDENTITY|Identity]]:
- **Tone:** Scientific, trustworthy, empowering, accessible. NOT clinical or cold.
- **Voice:** "We translate cutting-edge science into protocols you can actually follow."
- **Topics:** Peptide science, wellness protocols, biohacking, nootropics, music for wellness
- **Music arm:** AI-generated music (Recomposition Music) — separate content stream

<!-- CONTEXT: Recomposition Website Seo Geo / Brand Owner: -->
### Brand Owner:
- **Name:** Wayne Stevenson
- **Location:** Sea-to-Sky Corridor, BC, Canada
- **Email:** curtis4vancouver@gmail.com
- **YouTube Channels:**
  - OAC (Recomposition main): uses `youtube_token_oac.json`
  - Protocols (health content): uses `youtube_token_protocols.json`
  - **Protocol brand NEVER has its own social tokens** — it always inherits from Recomposition

<!-- CONTEXT: Recomposition Website Seo Geo / Brand Constitution: -->
### Brand Constitution:
- Read `Brand_Constitution/protocol/` for Protocol-specific voice and visual standards
- Read `Brand_Constitution/music/` for Music-specific brand guidelines
- Read `Brand_Constitution/[[Brand_Constitution/BRAND_VOICE|BRAND_VOICE]].md` for overall tone guidelines

<!-- CONTEXT: Recomposition Website Seo Geo / Key Research Files: -->
### Key Research Files:
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_1_AI_Search_Sourcing|3_1_AI_Search_Sourcing]].md` — How AI engines source businesses
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_2_Content_Strategy_AI|3_2_Content_Strategy_AI]].md` — Content strategy for AI
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_4_Schema_Markup_GEO|3_4_Schema_Markup_GEO]].md` — Schema for GEO
- `Research_Archives/12_Branding_Marketing/[[Research_Archives/12_Branding_Marketing/Opus_Level_Copywriting_Framework|Opus_Level_Copywriting_Framework]].md` — Copywriting standards
- All files in `Research_Archives/12_Branding_Marketing/` — Shopify, branding, marketing research

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 1: AUDIT RECOMPOSITION WEBSITE -->
## PHASE 1: AUDIT RECOMPOSITION WEBSITE

<!-- CONTEXT: Recomposition Website Seo Geo / Step 1.1: Crawl the site -->
### Step 1.1: Crawl the site
Using chrome-devtools-mcp, navigate to `https://keystonerecomposition.com` and check:

1. **robots.txt**: `https://keystonerecomposition.com/robots.txt`
   - Are AI bots allowed?
   - Is sitemap listed?

2. **Sitemap**: `https://keystonerecomposition.com/sitemap.xml`
   - Does it exist?
   - Are all pages included?

3. **Homepage DOM snapshot**: 
   - Existing JSON-LD schema?
   - Meta tags (title, description, og:tags)?
   - Medical disclaimers present?

4. **Key pages to audit:**
   - Homepage
   - About/mission page
   - Any protocol/wellness content pages
   - Music section (if separate)
   - Blog posts
   - Contact page

5. **Lighthouse audit:**
   ```
   lighthouse_audit URL=https://keystonerecomposition.com
   ```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 1.2: Document findings -->
### Step 1.2: Document findings
Save to: `Master_Docs/SEO_Audit_Results/recomposition_audit_20260610.md`

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 2: BUILD SCHEMA MARKUP (DIFFERENT FROM POSSIBILITIES) -->
## PHASE 2: BUILD SCHEMA MARKUP (DIFFERENT FROM POSSIBILITIES)

<!-- CONTEXT: Recomposition Website Seo Geo / Step 2.1: Organization schema for Recomposition -->
### Step 2.1: Organization schema for Recomposition
```json
{
  "@context": "https://schema.org",
  "@type": ["Organization", "MedicalBusiness"],
  "name": "Keystone Recomposition",
  "alternateName": "Recomposition",
  "description": "Evidence-based wellness protocols, peptide science education, and music for wellness. Translating cutting-edge research into actionable health optimization strategies.",
  "url": "https://keystonerecomposition.com",
  "logo": "https://keystonerecomposition.com/logo.png",
  "image": "https://keystonerecomposition.com/hero-image.jpg",
  "email": "curtis4vancouver@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Squamish",
    "addressRegion": "BC",
    "addressCountry": "CA"
  },
  "sameAs": [
    "YOUTUBE_OAC_CHANNEL_URL",
    "YOUTUBE_PROTOCOLS_CHANNEL_URL",
    "LINKEDIN_URL",
    "FACEBOOK_PAGE_URL",
    "INSTAGRAM_URL",
    "TIKTOK_URL",
    "SPOTIFY_ARTIST_URL"
  ],
  "founder": {
    "@type": "Person",
    "name": "Wayne Stevenson"
  },
  "knowsAbout": [
    "Peptide Science",
    "Wellness Protocols",
    "Biohacking",
    "Health Optimization",
    "Music Therapy",
    "AI-Generated Music",
    "Nootropics"
  ],
  "medicalSpecialty": "Preventive Medicine",
  "isAcceptingNewPatients": false
}
```

> **IMPORTANT:** Setting `isAcceptingNewPatients: false` signals this is NOT a medical practice — it's educational content. This is a critical distinction for YMYL compliance.

<!-- CONTEXT: Recomposition Website Seo Geo / Step 2.2: WebSite schema with search action -->
### Step 2.2: WebSite schema with search action
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Keystone Recomposition",
  "url": "https://keystonerecomposition.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://keystonerecomposition.com/?s={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 2.3: MedicalWebPage schema for health content pages -->
### Step 2.3: MedicalWebPage schema for health content pages
Every health/protocol page needs this INSTEAD of regular WebPage:
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "BPC-157 Research Summary — What the Science Says",
  "description": "Evidence-based overview of BPC-157 peptide research, including peer-reviewed studies, mechanisms of action, and current regulatory status.",
  "lastReviewed": "2026-06-10",
  "reviewedBy": {
    "@type": "Person",
    "name": "Wayne Stevenson"
  },
  "about": {
    "@type": "Drug",
    "name": "BPC-157",
    "alternateName": "Body Protection Compound-157"
  },
  "audience": {
    "@type": "MedicalAudience",
    "audienceType": "Patient"
  },
  "medicalDisclaimer": "This content is for educational purposes only and is not intended as medical advice. Always consult a qualified healthcare provider before starting any supplement or protocol."
}
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 2.4: FAQPage schema for protocol pages -->
### Step 2.4: FAQPage schema for protocol pages
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is BPC-157 and what does the research say?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "BPC-157 (Body Protection Compound-157) is a synthetic peptide derived from a protein found in human gastric juice. According to peer-reviewed research published in journals including the Journal of Physiology-Paris and Current Pharmaceutical Design, BPC-157 has shown regenerative properties in animal studies. However, large-scale human clinical trials are still lacking. Always consult a healthcare provider before considering any peptide protocol."
      }
    },
    {
      "@type": "Question",
      "name": "Is BPC-157 legal in Canada?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "As of 2026, BPC-157 is not approved by Health Canada or the FDA as a pharmaceutical drug. It is available as a research chemical in some jurisdictions. Regulations vary by province and country. Consult a healthcare professional and verify current regulations before purchasing or using any peptide."
      }
    }
  ]
}
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 2.5: MusicGroup schema for the music arm -->
### Step 2.5: MusicGroup schema for the music arm
```json
{
  "@context": "https://schema.org",
  "@type": "MusicGroup",
  "name": "Keystone Recomposition",
  "description": "AI-generated ambient and wellness music blending technology with mindfulness.",
  "url": "https://keystonerecomposition.com/music",
  "genre": ["Ambient", "Wellness", "Electronic", "Meditation"],
  "sameAs": [
    "SPOTIFY_ARTIST_URL",
    "APPLE_MUSIC_URL",
    "YOUTUBE_MUSIC_URL"
  ],
  "member": {
    "@type": "Person",
    "name": "Wayne Stevenson"
  }
}
```

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 3: MANDATORY MEDICAL DISCLAIMERS -->
## PHASE 3: MANDATORY MEDICAL DISCLAIMERS

<!-- CONTEXT: Recomposition Website Seo Geo / Step 3.1: Site-wide medical disclaimer -->
### Step 3.1: Site-wide medical disclaimer
Deploy a site-wide footer disclaimer on EVERY page:
```html
<div class="medical-disclaimer">
  <p><strong>Medical Disclaimer:</strong> The content on this website is for 
  educational and informational purposes only. It is not intended to be a 
  substitute for professional medical advice, diagnosis, or treatment. Always 
  seek the advice of your physician or other qualified health provider with 
  any questions you may have regarding a medical condition. Never disregard 
  professional medical advice or delay in seeking it because of something 
  you have read on this website.</p>
</div>
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 3.2: Per-page disclaimers for protocol content -->
### Step 3.2: Per-page disclaimers for protocol content
Any page discussing specific compounds (BPC-157, TB-500, Semaglutide, etc.) needs an ADDITIONAL prominent disclaimer at the top:
```html
<div class="protocol-disclaimer" style="background: #fff3cd; border: 1px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 8px;">
  <p>⚠️ <strong>Important:</strong> This article discusses research findings 
  for educational purposes only. The compounds discussed are NOT approved by 
  Health Canada or the FDA for the uses described. This is NOT medical advice. 
  Consult a qualified healthcare professional before starting any protocol. 
  <a href="/medical-disclaimer">Full medical disclaimer</a>.</p>
</div>
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 3.3: Create a dedicated medical disclaimer page -->
### Step 3.3: Create a dedicated medical disclaimer page
Create `/medical-disclaimer` page with full legal language covering:
- Not a medical practice
- Not prescribing or diagnosing
- Educational purposes only
- Individual results may vary
- Consult your healthcare provider
- Not endorsed by Health Canada or FDA
- Research citations are for reference only

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 4: AI BOT ACCESS (SAME PATTERN AS POSSIBILITIES BUT SEPARATE) -->
## PHASE 4: AI BOT ACCESS (SAME PATTERN AS POSSIBILITIES BUT SEPARATE)

<!-- CONTEXT: Recomposition Website Seo Geo / Step 4.1: Update robots.txt -->
### Step 4.1: Update robots.txt
Same AI bot allowances as Possibilities (see Set 03), but for this domain:
```
# AI Search Engine Bots — ALLOW
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://keystonerecomposition.com/sitemap.xml
```

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 5: HEALTH CONTENT OPTIMIZATION FOR AI EXTRACTION -->
## PHASE 5: HEALTH CONTENT OPTIMIZATION FOR AI EXTRACTION

<!-- CONTEXT: Recomposition Website Seo Geo / Step 5.1: Answer-first format (even more critical for health/YMYL) -->
### Step 5.1: Answer-first format (even more critical for health/YMYL)
AI engines are EXTRA cautious with health content. They need crystal-clear, instantly extractable answers.

**BEFORE (bad):**
```
Welcome to our protocol page. We've been researching peptides for years and 
have found some interesting results...
```

**AFTER (good):**
```
BPC-157 is a synthetic peptide derived from human gastric juice that has 
shown regenerative properties in over 50 peer-reviewed animal studies 
(Journal of Physiology-Paris, 2018; Current Pharmaceutical Design, 2021). 
No large-scale human clinical trials have been completed as of 2026. 
This article summarizes the current scientific evidence.
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 5.2: Citation hygiene -->
### Step 5.2: Citation hygiene
Every health claim MUST have a citation:
- **Format:** "[Finding] (Author et al., Journal, Year)"
- **Link:** DOI link or PubMed URL
- **Type:** Prefer RCTs > meta-analyses > observational studies > case reports
- **Recency:** Prefer studies from last 5 years

<!-- CONTEXT: Recomposition Website Seo Geo / Step 5.3: E-E-A-T signals for health content -->
### Step 5.3: E-E-A-T signals for health content
These are CRITICAL for YMYL content:

1. **Author bio** — Wayne's qualifications, certifications, experience
2. **Reviewed by** — If any medical professional reviews content, cite them
3. **Last updated date** — Show when content was last reviewed
4. **Sources section** — Full reference list at bottom of every article
5. **About page** — Detailed founder story with credentials

<!-- CONTEXT: Recomposition Website Seo Geo / Step 5.4: Content structure for AI extraction -->
### Step 5.4: Content structure for AI extraction
```markdown
# [Topic] — What the Research Says [Year]

[1-sentence TL;DR answer]

**Medical Disclaimer:** [Inline disclaimer]

<!-- CONTEXT: Recomposition Website Seo Geo / What is [Topic]? -->
## What is [Topic]?
[Clear definition with citations]

<!-- CONTEXT: Recomposition Website Seo Geo / What Does the Research Say? -->
## What Does the Research Say?
[Peer-reviewed findings with specific citations]

<!-- CONTEXT: Recomposition Website Seo Geo / Current Regulatory Status -->
## Current Regulatory Status
[Health Canada/FDA status — HONEST and current]

<!-- CONTEXT: Recomposition Website Seo Geo / Potential Benefits (According to Research) -->
## Potential Benefits (According to Research)
[Bullet points, each with citation]

<!-- CONTEXT: Recomposition Website Seo Geo / Risks and Side Effects -->
## Risks and Side Effects
[ALWAYS include this section — builds trust with AI engines]

<!-- CONTEXT: Recomposition Website Seo Geo / Bottom Line -->
## Bottom Line
[Summary with "consult your healthcare provider"]

<!-- CONTEXT: Recomposition Website Seo Geo / Sources -->
## Sources
[Full reference list with DOI links]
```

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 6: MUSIC CONTENT OPTIMIZATION -->
## PHASE 6: MUSIC CONTENT OPTIMIZATION

<!-- CONTEXT: Recomposition Website Seo Geo / Step 6.1: Music section schema -->
### Step 6.1: Music section schema
If the site has a dedicated music section, add:
- `MusicGroup` schema (see Phase 2.5)
- `MusicAlbum` and `MusicRecording` schemas for individual releases
- Link to all streaming platforms via `sameAs`

<!-- CONTEXT: Recomposition Website Seo Geo / Step 6.2: AI disclosure for music -->
### Step 6.2: AI disclosure for music
All AI-generated music content should clearly [[STATE|state]]:
```html
<div class="ai-disclosure">
  <p>🎵 This music was created using AI-assisted composition tools. 
  Creative direction, lyrics, and production oversight by Wayne Stevenson.</p>
</div>
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 6.3: Music SEO keywords -->
### Step 6.3: Music SEO keywords
Optimize for:
- "ambient wellness music"
- "meditation music AI"
- "biohacking music playlist"
- "focus music for work"
- "healing frequency music"

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 7: SEPARATE THE BRANDS PROPERLY -->
## PHASE 7: SEPARATE THE BRANDS PROPERLY

<!-- CONTEXT: Recomposition Website Seo Geo / Step 7.1: Cross-linking between sites -->
### Step 7.1: Cross-linking between sites
Both sites should reference each other but be CLEARLY SEPARATE entities:

On keystonerecomposition.com footer:
```html
<p>Keystone Recomposition is part of the Keystone family. 
See also: <a href="https://keystonepossibilities.com" rel="noopener">
Keystone Possibilities</a> — Custom home construction in BC's Sea-to-Sky Corridor.</p>
```

On keystonepossibilities.com footer:
```html
<p>See also: <a href="https://keystonerecomposition.com" rel="noopener">
Keystone Recomposition</a> — Evidence-based wellness protocols and music.</p>
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 7.2: NO brand confusion in schema -->
### Step 7.2: NO brand confusion in schema
- Possibilities schema uses `@type: GeneralContractor`
- Recomposition schema uses `@type: MedicalBusiness`
- They are SEPARATE Organization entities with SEPARATE sameAs arrays
- They share the same founder (Wayne Stevenson) — this is fine

<!-- CONTEXT: Recomposition Website Seo Geo / Step 7.3: Wikidata (if creating) -->
### Step 7.3: Wikidata (if creating)
If a Wikidata entry is created for Recomposition:
- It should be a SEPARATE entity from Keystone Possibilities
- Instance of (P31): Q4830453 (business) — NOT medical practice
- Industry (P452): Q1744607 (wellness industry)
- Do NOT use medical/healthcare classifications unless actually licensed

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 8: LOCAL CITATIONS FOR RECOMPOSITION -->
## PHASE 8: LOCAL CITATIONS FOR RECOMPOSITION

<!-- CONTEXT: Recomposition Website Seo Geo / Step 8.1: Different citation platforms than Possibilities -->
### Step 8.1: Different citation platforms than Possibilities
Recomposition needs presence on DIFFERENT platforms:

**HIGH PRIORITY:**
- [ ] Google Business Profile — as a separate business listing
- [ ] Bing Places — separate listing from Possibilities
- [ ] YouTube channels — already have tokens, ensure branding is consistent
- [ ] Spotify for Artists — claim and optimize artist profile
- [ ] Apple Music for Artists — claim profile

**MEDIUM PRIORITY:**
- [ ] LinkedIn Company Page — separate from Possibilities
- [ ] Facebook Business Page — ensure NAP consistency
- [ ] Instagram Business Profile — bio matches website exactly
- [ ] TikTok Business — health content presence
- [ ] Podcast directories (if launching podcast) — Apple Podcasts, Spotify

**HEALTH-SPECIFIC:**
- [ ] Healthline contributor directory (if applicable)
- [ ] Psychology Today (if applicable)
- [ ] Local wellness directories for BC

<!-- CONTEXT: Recomposition Website Seo Geo / Step 8.2: NAP consistency -->
### Step 8.2: NAP consistency
Create: `Master_Docs/NAP_RECOMPOSITION_REFERENCE.md`
- Name, Address, Phone MUST be consistent
- If using different address than Possibilities, document clearly
- If sharing address, that's fine — Google handles multi-brand locations

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 9: BLOG-TO-VIDEO LOOP (HEALTH VERSION) -->
## PHASE 9: BLOG-TO-VIDEO LOOP (HEALTH VERSION)

<!-- CONTEXT: Recomposition Website Seo Geo / Step 9.1: Template for health video → blog post -->
### Step 9.1: Template for health video → blog post
```markdown
Title: [Protocol/Topic] — What [X] Studies Say [Year]

⚠️ Medical Disclaimer: [inline disclaimer]

[Embed YouTube video from Protocols channel]

<!-- CONTEXT: Recomposition Website Seo Geo / TL;DR -->
## TL;DR
[1-2 sentence summary with key finding + citation]

<!-- CONTEXT: Recomposition Website Seo Geo / What the Research Shows -->
## What the Research Shows
[Expanded from video transcript with additional citations]

<!-- CONTEXT: Recomposition Website Seo Geo / Key Studies Referenced -->
## Key Studies Referenced
[Table of studies: Author, Year, Journal, Finding, Sample Size]

<!-- CONTEXT: Recomposition Website Seo Geo / Frequently Asked Questions -->
## Frequently Asked Questions
[FAQ section with FAQPage schema]

<!-- CONTEXT: Recomposition Website Seo Geo / Important Safety Information -->
## Important Safety Information
[Side effects, contraindications, regulatory status]

<!-- CONTEXT: Recomposition Website Seo Geo / Sources -->
## Sources
[Full reference list with PubMed/DOI links]

<!-- CONTEXT: Recomposition Website Seo Geo / About the Author -->
## About the Author
Wayne Stevenson is the founder of Keystone Recomposition, dedicated to 
translating peer-reviewed research into accessible wellness education. 
This content is for educational purposes only and is not medical advice.
```

<!-- CONTEXT: Recomposition Website Seo Geo / Step 9.2: Music video → blog post template -->
### Step 9.2: Music video → blog post template
```markdown
Title: [Song Title] — Behind the Music | Keystone Recomposition

[Embed YouTube video]

<!-- CONTEXT: Recomposition Website Seo Geo / About This Track -->
## About This Track
[Description of the creative vision, inspiration, genre]

<!-- CONTEXT: Recomposition Website Seo Geo / Production Details -->
## Production Details
- Composed using: [AI tools used]
- Genre: [genre tags]
- Duration: [length]
- Available on: [Spotify, Apple Music, YouTube Music links]

<!-- CONTEXT: Recomposition Website Seo Geo / Listen on Your Preferred Platform -->
## Listen on Your Preferred Platform
[Streaming platform links with icons]
```

---

<!-- CONTEXT: Recomposition Website Seo Geo / PHASE 10: VERIFICATION -->
## PHASE 10: VERIFICATION

<!-- CONTEXT: Recomposition Website Seo Geo / Step 10.1: Schema validation -->
### Step 10.1: Schema validation
Test ALL deployed schemas at:
- https://search.google.com/test/rich-results
- https://validator.schema.org/

<!-- CONTEXT: Recomposition Website Seo Geo / Step 10.2: Medical disclaimer check -->
### Step 10.2: Medical disclaimer check
Verify disclaimer appears on:
- [ ] Site footer (every page)
- [ ] Every protocol/health content page (inline at top)
- [ ] Dedicated /medical-disclaimer page exists

<!-- CONTEXT: Recomposition Website Seo Geo / Step 10.3: AI visibility check -->
### Step 10.3: AI visibility check
- Ask ChatGPT: "What is Keystone Recomposition?"
- Ask Perplexity: "wellness protocols Keystone Recomposition"
- Google: "site:keystonerecomposition.com" (verify indexing)

<!-- CONTEXT: Recomposition Website Seo Geo / Step 10.4: Brand separation check -->
### Step 10.4: Brand separation check
- Verify Possibilities schema does NOT appear on Recomposition site
- Verify Recomposition schema does NOT appear on Possibilities site
- Verify cross-links are present but not confusing

<!-- CONTEXT: Recomposition Website Seo Geo / Step 10.5: Document everything -->
### Step 10.5: Document everything
Save to: `Master_Docs/SEO_Audit_Results/recomposition_audit_20260610.md`

---

<!-- CONTEXT: Recomposition Website Seo Geo / SUCCESS CRITERIA -->
## SUCCESS CRITERIA
- [ ] Recomposition website fully audited with report
- [ ] Organization + MedicalBusiness schema deployed
- [ ] MedicalWebPage schema ready for health content pages
- [ ] MusicGroup schema deployed for music section
- [ ] FAQPage schema for protocol pages
- [ ] Medical disclaimers deployed (site-wide + per-page + dedicated page)
- [ ] AI disclosure for music content
- [ ] robots.txt updated for AI bots
- [ ] NAP reference created (separate from Possibilities)
- [ ] Blog-to-video templates created (health + music)
- [ ] Brand separation verified (NO mixing with Possibilities)
- [ ] All schemas validated
- [ ] NO website breakage


---
📁 **See also:** [[Master_Docs/Gemini_Pro_Instructions/INDEX|← Directory Index]]
