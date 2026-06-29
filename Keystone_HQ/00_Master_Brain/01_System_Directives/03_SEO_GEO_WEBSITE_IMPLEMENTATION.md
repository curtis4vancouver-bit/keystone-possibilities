# SEO/GEO Website Implementation

**For:** Gemini 3.1 Pro (autonomous execution)  
**Created:** 2026-06-10 by Antigravity  
**Purpose:** Deploy SEO/GEO optimizations to both Keystone websites without breaking them  
**Risk Level:** MEDIUM (modifying live websites)  

---

## ⚠️ Critical Safety Rules

1. **NEVER modify WordPress core files directly** — use the Customizer, theme `functions.php`, or a plugin.
2. **ALWAYS back up before changes** — Export full WordPress site before any modification.
3. **Test schema with Google Rich Results Test BEFORE deploying** — https://search.google.com/test/rich-results
4. **Deploy sameAs and schema via JSON-LD in `<head>`** — NOT inline microdata (easier to maintain/rollback).
5. **If anything looks wrong, STOP and document what happened** — Wayne can fix it when he returns.

---

## Critical Context

### Websites
* **Keystone Possibilities**: `keystonepossibilities.com` (WordPress) — Construction business
* **Keystone Recomposition**: `keystonerecomposition.com` (WordPress) — Health/wellness/music

### Brand Owner
* **Name:** Wayne Stevenson
* **Location:** Sea-to-Sky Corridor (Squamish/Whistler/Pemberton), British Columbia, Canada
* **Email:** curtis4vancouver@gmail.com

### Available Tools
* `chrome-devtools-mcp` — Navigate to websites and inspect them
* `brave-search` — Web search
* `keystone_instant_indexer` — Push URLs to Google Indexing API
* `seo-geo` — Schema templates and audit checklists

---

## Phase 1: Audit Current Website State

### Step 1.1: Crawl Keystone Possibilities website
Navigate to `https://keystonepossibilities.com` and:

1. **Check robots.txt**: Navigate to `https://keystonepossibilities.com/robots.txt`
   * Are AI bots allowed? (GPTBot, PerplexityBot, ClaudeBot, ChatGPT-User, anthropic-ai)
   * Is the sitemap listed?
2. **Check sitemap**: Navigate to `https://keystonepossibilities.com/sitemap.xml`
   * Does it exist? Are all pages included?
3. **Check homepage for schema**: Take a DOM snapshot of the homepage.
   * Is there existing JSON-LD schema? What Organization/LocalBusiness schema exists? Is there sameAs linking?
4. **Check meta tags**: Look for title, description, and og:tags on key pages (Homepage, Services, About, Contact, Blog posts).
5. **Check Core Web Vitals**: Run lighthouse audit via chrome-devtools-mcp:
   ```bash
   lighthouse_audit URL=https://keystonepossibilities.com
   ```

### Step 1.2: Document findings
Create `Master_Docs/SEO_Audit_Results/possibilities_audit_20260610.md` to record all findings (what's good, missing, or broken).

### Step 1.3: Repeat for Keystone Recomposition
Perform the exact same audit process for `https://keystonerecomposition.com`.

---

## Phase 2: Build Schema Markup

### Step 2.1: Create Organization + LocalBusiness schema for Possibilities
```json
{
  "@context": "https://schema.org",
  "@type": ["Organization", "LocalBusiness", "GeneralContractor"],
  "name": "Keystone Possibilities",
  "description": "Custom home construction, renovation, and project management in the Sea-to-Sky Corridor. Serving Squamish, Whistler, and Pemberton, BC.",
  "url": "https://keystonepossibilities.com",
  "logo": "https://keystonepossibilities.com/logo.png",
  "image": "https://keystonepossibilities.com/hero-image.jpg",
  "telephone": "+1-XXX-XXX-XXXX",
  "email": "curtis4vancouver@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Squamish",
    "addressRegion": "BC",
    "addressCountry": "CA"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "49.7016",
    "longitude": "-123.1558"
  },
  "areaServed": [
    {
      "@type": "City",
      "name": "Squamish",
      "sameAs": "https://en.wikipedia.org/wiki/Squamish,_British_Columbia"
    },
    {
      "@type": "City",
      "name": "Whistler",
      "sameAs": "https://en.wikipedia.org/wiki/Whistler,_British_Columbia"
    },
    {
      "@type": "City",
      "name": "Pemberton",
      "sameAs": "https://en.wikipedia.org/wiki/Pemberton,_British_Columbia"
    }
  ],
  "sameAs": [
    "GOOGLE_BUSINESS_PROFILE_URL",
    "LINKEDIN_COMPANY_URL",
    "FACEBOOK_PAGE_URL",
    "YOUTUBE_CHANNEL_URL",
    "INSTAGRAM_URL"
  ],
  "founder": {
    "@type": "Person",
    "name": "Wayne Stevenson"
  },
  "knowsAbout": [
    "Custom Home Construction",
    "Renovation",
    "Project Management",
    "Bill 44 Compliance",
    "BC Building Code",
    "Energy Efficient Building",
    "Sea-to-Sky Corridor Construction"
  ]
}
```
*Note: Fill in the actual phone number, social media URLs, GBP URL, lat/long coordinates, logo, and hero image before deploying.*

### Step 2.2: Create schema for Recomposition
Apply a similar structure using `@type: ["Organization", "MedicalBusiness"]` or another appropriate health/wellness type.

### Step 2.3: Create FAQPage schema for key service pages
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does custom home construction cost in Squamish?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Custom home construction in Squamish typically ranges from $350 to $600+ per square foot in 2026, depending on complexity, materials, and site conditions. According to BC Housing data, the Sea-to-Sky Corridor has seen 15% construction cost increases since 2024."
      }
    }
  ]
}
```

### Step 2.4: Create BreadcrumbList schema
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://keystonepossibilities.com"},
    {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://keystonepossibilities.com/services"},
    {"@type": "ListItem", "position": 3, "name": "Custom Homes", "item": "https://keystonepossibilities.com/services/custom-homes"}
  ]
}
```

---

## Phase 3: Deploy to WordPress

### Method 1: Code Snippet Plugin (SAFEST)
If a code snippets plugin (e.g., WPCode, Code Snippets) is active:
1. Add JSON-LD as a header snippet.
2. Set to load on all pages (Organization) or specific pages (FAQ).
3. Disable instantly if any layout/logical issues occur.

### Method 2: Theme functions.php
```php
function keystone_add_schema_markup() {
    if (is_front_page()) {
        ?>
        <script type="application/ld+json">
        {
            // Insert Organization JSON-LD here
        }
        </script>
        <?php
    }
}
add_action('wp_head', 'keystone_add_schema_markup');
```

### Method 3: Yoast SEO / RankMath
If an SEO plugin is already active, use its built-in custom schema editor instead of modifying files directly.

---

## Phase 4: AI Bot Access

### Step 4.1: Update robots.txt to allow AI bots
Ensure the following rules are active in your `robots.txt`:

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
```

### Step 4.2: Edit robots.txt in WordPress
If physical access is limited, edit the file virtualized via Yoast SEO's Tools, RankMath's file editor, or write directly to a physical `robots.txt` in the root directory.

### Step 4.3: Verify indexability
Submit updated URLs via Google Search Console, Bing Webmaster Tools, or the `keystone_instant_indexer` tool.

---

## Phase 5: Content Optimization for AI Extraction

### Step 5.1: Implement "Answer-First" format on key pages

**Before (Ineffective for LLMs):**
> Welcome to Keystone Possibilities! We are a family-owned construction company that has been serving the community for many years...

**After (Optimized for LLM retrieval):**
> Keystone Possibilities is a custom home construction and renovation company serving Squamish, Whistler, and Pemberton in BC's Sea-to-Sky Corridor. Founded by Wayne Stevenson, we specialize in energy-efficient custom builds, Bill 44 compliance renovations, and full-service project management. Contact us at (XXX) XXX-XXXX for a free consultation.

### Step 5.2: Add statistics and citations
Incorporate authoritative, direct data points to increase AI search engine trust:
* "Over [X] projects completed in the Sea-to-Sky Corridor."
* "Serving homeowners since [Year]."
* Citation of BC Building Code requirements and compliance metrics.

### Step 5.3: Create Q&A content sections
Match direct questions to FAQ schema on your pages:
* "How much does custom building cost in Squamish?"
* "What permits are required for secondary suites under Bill 44 in British Columbia?"

---

## Phase 6: Local Citation Checklist

Ensure Name, Address, and Phone (NAP) are matching exactly across all profiles.

### High Priority
- [ ] Google Business Profile (Verify information details match site schema)
- [ ] Bing Places for Business (Crucial for Microsoft Copilot/ChatGPT web search)
- [ ] Yelp Business listing
- [ ] Better Business Bureau (BBB) listing
- [ ] HomeStars directory listing (Top Canadian contractor directory)

### Medium Priority
- [ ] Houzz (Contractor portfolio)
- [ ] RenoQuotes
- [ ] Yellow Pages Canada
- [ ] Facebook Business Page
- [ ] LinkedIn Company Page

### Low Priority
- [ ] Apple Maps
- [ ] Waze
- [ ] MapQuest
- [ ] Foursquare

Save absolute NAP parameters inside `Master_Docs/NAP_MASTER_REFERENCE.md`.

---

## Phase 7: Wikidata Entity Creation

To build absolute entity clarity for LLM datasets:

1. Search for existing entries: `https://www.wikidata.org/wiki/Special:Search?search=Keystone+Possibilities`
2. Create entry if missing with properties:
   * **Label:** Keystone Possibilities
   * **Description:** Construction company in Squamish, British Columbia, Canada
   * **Instance of (P31):** Q4830453 (construction company) or Q891723 (general contractor)
   * **Country (P17):** Q16 (Canada)
   * **Located in (P131):** Q184694 (Squamish)
   * **Official website (P856):** `https://keystonepossibilities.com`
   * **Founder (P112):** Wayne Stevenson
3. Link the new Wikidata entity URL into your schema `sameAs` array.

---

## Phase 8: Blog-to-Video Traffic Loop

```
YouTube Video → Blog Post (embedded video + transcript + FAQ)
                     ↓
               Google indexes blog post
                     ↓
               AI engines cite blog post in answers
                     ↓
               Traffic flows back to YouTube + website
```

### Post Conversion Template
```markdown
# [Video Title] — [Primary Keyword] in [Location]

[Embed YouTube Video Link]

## Overview
[2-3 sentence summary with answer-first format]

## Key Points
* [Key take-away from video transcript]
* [Key take-away from video transcript]

## Detailed Breakdown
[Detailed explanation of construction methodology, BC building code rules, or project management notes]

## Frequently Asked Questions
[Insert FAQ Q&As that align with schema]

## About the Author
Wayne Stevenson is the founder of Keystone Possibilities, specializing in custom home construction and renovations in BC's Sea-to-Sky Corridor.
```

---

## Phase 9: Verification

1. **Schema validation**: Run live schema assets through:
   * Google Rich Results Test (https://search.google.com/test/rich-results)
   * Schema Markup Validator (https://validator.schema.org/)
2. **AI visibility check**: Check search outputs on ChatGPT, Bing, and Perplexity using targeted queries:
   * "Who is the best contractor in Squamish?"
   * "Custom home builders Squamish BC"
3. **Save proof reports**: Save all diagnostics under `Master_Docs/SEO_Audit_Results/`.

---

## Success Criteria
- [ ] Both websites audited with full reports compiled.
- [ ] Organization + LocalBusiness schema created and validated.
- [ ] FAQPage schema created for service pages.
- [ ] Schema successfully deployed to the homepage of both sites.
- [ ] robots.txt explicitly allows AI search bots.
- [ ] NAP master reference file completed.
- [ ] Wikidata entity linked to schema where applicable.
- [ ] Blog-to-video loop content workflow ready.
- [ ] Both live sites verified functional with no syntax or code errors.