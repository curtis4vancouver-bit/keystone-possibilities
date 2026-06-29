# INSTRUCTION SET 5: Keystone Recomposition Website SEO/GEO Implementation

> **Brand:** Keystone Recomposition (keystonerecomposition.com - WordPress)
> **Purpose:** Deploy SEO/GEO optimizations, schema markups, and YMYL safety protocols for the health/wellness and music brand.
> **Depends on:** Instruction Set 01 (Brain). Separate from the Possibilities site (Set 03).

---

## ⚠️ CRITICAL SAFETY RULES — HEALTH CONTENT (YMYL)

1. **High Scrutiny:** Google and AI engines apply extra scrutiny to health content.
2. **No Medical Claims:** Content must be strictly educational, not prescriptive.
3. **Medical Disclaimers:** Mandatory on every page carrying health or supplement-related content.
4. **Peer-Reviewed Sourcing:** Cite PubMed, FDA, and Health Canada only.
5. **Forbidden Language:** Do not use "cure", "treat", or "diagnose". Use "may support", "research suggests", "consult your healthcare provider".
6. **AI Disclosure:** Mandatory on all AI-assisted content (blog, video, music).
7. **No Direct Core Edits:** Use WordPress Customizer, child-theme functions.php, or trusted SEO plugins.
8. **Backup Rule:** Always export a full WordPress site backup before making modifications.

---

## BRAND & ASSET CONTEXT

* **Tone:** Scientific, trustworthy, empowering, accessible.
* **Topics:** Peptide science, wellness protocols, biohacking, nootropics, music for wellness.
* **Music Stream:** AI-assisted ambient and wellness music under "Recomposition Music".
* **Founder:** Wayne Stevenson (Squamish / Sea-to-Sky Corridor, BC, Canada).
* **Email:** curtis4vancouver@gmail.com
* **YouTube Integration:** 
  * Main Brand Channel (OAC): uses `youtube_token_oac.json`
  * Protocols Channel: uses `youtube_token_protocols.json` (inherits Recomposition social tokens).

---

## PHASE 1: SITE AUDIT PROCEDURES

Perform a standard crawl of `https://keystonerecomposition.com` to check:
1. **robots.txt**: Verify AI crawler access and correct sitemap declaration.
2. **Sitemap**: Validate XML existence and freshness.
3. **DOM Snapshot**: Scan for correct JSON-LD schema integration, meta title/description tags, and footer disclaimers.
4. **Lighthouse Audit**: Run standard performance, accessibility, and SEO audits.
5. **Reporting**: Document results in `Master_Docs/SEO_Audit_Results/recomposition_audit_20260610.md`.

---

## PHASE 2: SCHEMA MARKUP ARCHITECTURE

### 2.1 Organization & MedicalBusiness Schema (Homepage)
```json
{
  "@context": "https://schema.org",
  "@type": ["Organization", "MedicalBusiness"],
  "name": "Keystone Recomposition",
  "alternateName": "Recomposition",
  "description": "Evidence-based wellness protocols, peptide science education, and music for wellness.",
  "url": "https://keystonerecomposition.com",
  "logo": "https://keystonerecomposition.com/logo.png",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Squamish",
    "addressRegion": "BC",
    "addressCountry": "CA"
  },
  "sameAs": [
    "YOUTUBE_OAC_CHANNEL_URL",
    "YOUTUBE_PROTOCOLS_CHANNEL_URL",
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
    "Music Therapy"
  ],
  "medicalSpecialty": "Preventive Medicine",
  "isAcceptingNewPatients": false
}
```
*Note: Setting `isAcceptingNewPatients` to `false` is critical to clarify that the brand is educational, not a primary care clinic.*

### 2.2 MedicalWebPage Schema (Health & Protocol Articles)
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "BPC-157 Research Summary — What the Science Says",
  "description": "Evidence-based overview of BPC-157 peptide research, mechanisms of action, and regulatory status.",
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

### 2.3 FAQPage Schema Template
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
        "text": "BPC-157 is a synthetic peptide derived from gastric juice. Animal studies suggest regenerative properties, but large-scale human clinical trials are lacking. Consult a healthcare provider before considering peptide protocols."
      }
    }
  ]
}
```

### 2.4 MusicGroup Schema (Recomposition Music Arm)
```json
{
  "@context": "https://schema.org",
  "@type": "MusicGroup",
  "name": "Keystone Recomposition",
  "description": "AI-assisted ambient and wellness music blending technology with mindfulness.",
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

## PHASE 3: MANDATORY MEDICAL DISCLAIMERS

### 3.1 Site-Wide Footer Disclaimer
```html
<div class="medical-disclaimer">
  <p><strong>Medical Disclaimer:</strong> The content on this website is for 
  educational and informational purposes only. It is not intended to be a 
  substitute for professional medical advice, diagnosis, or treatment. Always 
  seek the advice of your physician or other qualified health provider with 
  any questions you may have regarding a medical condition.</p>
</div>
```

### 3.2 Top-of-Page Inline Disclaimer (Compound & Protocol Pages)
```html
<div class="protocol-disclaimer" style="background: #fff3cd; border: 1px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 8px;">
  <p>⚠️ <strong>Important:</strong> This article discusses research findings 
  for educational purposes only. The compounds discussed are NOT approved by 
  Health Canada or the FDA for the uses described. This is NOT medical advice. 
  Consult a qualified healthcare professional before starting any protocol. 
  <a href="/medical-disclaimer">Full medical disclaimer</a>.</p>
</div>
```

---

## PHASE 4: ROBOTS.TXT (AI BOT VISIBILITY)

Deploy this exact layout on `keystonerecomposition.com` to ensure search-engine optimization across AI indexing hubs:
```text
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

## PHASE 5: AI-OPTIMIZED CONTENT STRUCTURING (E-E-A-T)

* **Answer-First Writing:** Begin topics with direct, single-sentence TL;DR definitions containing high-level scientific consensus before elaborating.
* **Strict Citation Standards:** Format claims with inline parenthetical citations: `[Finding] (Author et al., Journal, Year)` with links to DOIs or PubMed URLs.
* **Regulatory Transparency:** Always clearly declare the legal and regulatory standing of compounds (e.g., "not approved by Health Canada or the FDA for personal use").
* **Comprehensive Risk Profile:** Balance benefit points with documented risks, side effects, and regulatory caveats to build ranking authority.

---

## PHASE 6: BRAND CO-EXISTENCE & ISOLATION

Keep Keystone Recomposition and Keystone Possibilities explicitly separated in schemas and data structures to prevent search algorithm confusion.

* **Footer Cross-Linking:**
  * On `keystonerecomposition.com`: 
    `Keystone Recomposition is part of the Keystone family. See also: <a href="https://keystonepossibilities.com">Keystone Possibilities</a> — Custom home construction in BC's Sea-to-Sky Corridor.`
  * On `keystonepossibilities.com`: 
    `See also: <a href="https://keystonerecomposition.com">Keystone Recomposition</a> — Evidence-based wellness protocols and music.`
* **Schema Separation:**
  * Possibilities = `@type: GeneralContractor`
  * Recomposition = `@type: MedicalBusiness` / `MusicGroup`

---

## PHASE 7: BLOG-TO-VIDEO LOOP TEMPLATES

### 7.1 Health & Wellness Protocol Layout
```markdown
# [Topic/Compound] — What the Research Says [Year]

[1-sentence TL;DR answer explaining compound and safety status]

⚠️ **Medical Disclaimer:** [Inline warning with link to dedicated disclaimer page]

[Embed YouTube Video from Protocols Channel]

## What the Research Shows
[Scientific review referencing clinical trials / animal models]

## Key Studies Referenced
| Study / Author | Journal / Year | Key Finding | Sample Type |
| --- | --- | --- | --- |

## Risks, Side Effects, and Safety Profile
[Detail warnings and known issues]

## Sources
* [Full peer-reviewed citations with links]
```

### 7.2 Music Release Layout
```markdown
# [Song Title] — Behind the Music | Keystone Recomposition

[Embed YouTube Release / Spotify Widget]

## About This Track
[Describe creative intention, ambient style, target biohacking/mindfulness applications]

🎵 *AI Disclosure: This music was created using AI-assisted composition tools. Creative direction, engineering, and execution curated by Wayne Stevenson.*