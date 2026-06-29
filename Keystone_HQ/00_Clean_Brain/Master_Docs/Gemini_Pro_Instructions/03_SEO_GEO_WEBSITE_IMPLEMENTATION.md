---
id: doc-03seogeowebsiteimplementation
title: Seo Geo Website Implementation
type: document
summary: '> For: Gemini 3.1 Pro (autonomous execution)'
entities:
- Bill 44
- Keystone Possibilities
- Keystone Recomposition
- Sea-to-Sky
- Squamish
- Wayne Stevenson
- Whistler
- YouTube
created: '2026-06-10T08:24:19.927575'
updated: '2026-06-14T19:57:36.097017'
---
# INSTRUCTION SET 3: SEO/GEO Website Implementation
> **For:** [[GEMINI|Gemini]] 3.1 Pro (autonomous execution)  
> **Created:** 2026-06-10 by Antigravity  
> **Purpose:** Deploy SEO/GEO optimizations to both Keystone websites WITHOUT breaking them  
> **Estimated Time:** 2-3 hours  
> **Risk Level:** MEDIUM — modifying live websites, must be careful  
> **Depends on:** Instruction Set 01 and 02 should be done first

---

<!-- CONTEXT: Seo Geo Website Implementation / ⚠️ CRITICAL SAFETY RULES -->
## ⚠️ CRITICAL SAFETY RULES

1. **NEVER modify WordPress core files directly** — use the Customizer, theme functions.php, or a plugin
2. **ALWAYS back up before changes** — Export full WordPress site before any modification
3. **Test schema with Google Rich Results Test BEFORE deploying** — https://search.google.com/test/rich-results
4. **Deploy sameAs and schema via JSON-LD in `<head>`** — NOT inline microdata (easier to maintain/rollback)
5. **If anything looks wrong, STOP and document what happened** — Wayne can fix it when he returns

---

<!-- CONTEXT: Seo Geo Website Implementation / CRITICAL CONTEXT -->
## CRITICAL CONTEXT

<!-- CONTEXT: Seo Geo Website Implementation / Websites: -->
### Websites:
- **Keystone [[possibilities|Possibilities]]**: keystonepossibilities.com (WordPress) — Construction business
- **Keystone Recomposition**: keystonerecomposition.com (WordPress) — Health/wellness/[[music|music]]

<!-- CONTEXT: Seo Geo Website Implementation / Brand Owner: -->
### Brand Owner:
- **Name:** Wayne Stevenson
- **Location:** Sea-to-Sky Corridor (Squamish/Whistler/Pemberton), British Columbia, Canada
- **Email:** curtis4vancouver@gmail.com

<!-- CONTEXT: Seo Geo Website Implementation / Available Tools: -->
### Available Tools:
- `chrome-devtools-mcp` — Can navigate to websites and inspect them
- `brave-search` — Can search the web
- `keystone_instant_indexer` [[davinci-resolve-mcp/docs/SKILL|skill]] — Can push URLs to Google Indexing API
- `seo-geo` [[davinci-resolve-mcp/docs/SKILL|skill]] — Has schema templates and audit checklists

<!-- CONTEXT: Seo Geo Website Implementation / Key Research Files: -->
### Key Research Files:
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_1_AI_Search_Sourcing|3_1_AI_Search_Sourcing]].md` — How AI engines source local businesses
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_2_Content_Strategy_AI|3_2_Content_Strategy_AI]].md` — Content strategy for AI visibility
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_3_Knowledge_Panel|3_3_Knowledge_Panel]].md` — Knowledge Panel strategy
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/3_4_Schema_Markup_GEO|3_4_Schema_Markup_GEO]].md` — Schema markup for GEO
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/1_2_Schema_Markup|1_2_Schema_Markup]].md` — Technical schema implementation
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/2_1_Google_Business_Profile|2_1_Google_Business_Profile]].md` — GBP optimization
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/2_2_Local_Citation_Building|2_2_Local_Citation_Building]].md` — Citation platforms
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/4_1_Service_Page_Architecture|4_1_Service_Page_Architecture]].md` — Service page structure
- `Research_Archives/08_SEO_Website/[[Research_Archives/08_SEO_Website/10_1_Video_to_Blog_Loop|10_1_Video_to_Blog_Loop]].md` — Blog-to-video traffic loop

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 1: AUDIT CURRENT WEBSITE [[STATE|STATE]] -->
## PHASE 1: AUDIT CURRENT WEBSITE [[STATE|STATE]]

<!-- CONTEXT: Seo Geo Website Implementation / Step 1.1: Crawl Keystone Possibilities website -->
### Step 1.1: Crawl Keystone Possibilities website
Using chrome-devtools-mcp, navigate to `https://keystonepossibilities.com` and:

1. **Check robots.txt**: Navigate to `https://keystonepossibilities.com/robots.txt`
   - Are AI bots allowed? (GPTBot, PerplexityBot, ClaudeBot, ChatGPT-User, anthropic-ai)
   - Is the sitemap listed?

2. **Check sitemap**: Navigate to `https://keystonepossibilities.com/sitemap.xml`
   - Does it exist?
   - Are all pages included?

3. **Check homepage for schema**: Take a DOM snapshot of the homepage
   - Is there existing JSON-LD schema?
   - What Organization/LocalBusiness schema exists?
   - Is there sameAs linking?

4. **Check meta tags**: Look for title, description, og:tags on key pages
   - Homepage
   - Services page
   - About page
   - Contact page
   - Any blog posts

5. **Check Core Web Vitals**: Run lighthouse audit via chrome-devtools-mcp
   ```
   lighthouse_audit URL=https://keystonepossibilities.com
   ```

<!-- CONTEXT: Seo Geo Website Implementation / Step 1.2: Document findings -->
### Step 1.2: Document findings
Create a file: `Master_Docs/SEO_Audit_Results/possibilities_audit_20260610.md`
Record ALL findings — what's good, what's missing, what's broken.

<!-- CONTEXT: Seo Geo Website Implementation / Step 1.3: Repeat for Keystone Recomposition -->
### Step 1.3: Repeat for Keystone Recomposition
Same process for `https://keystonerecomposition.com`

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 2: BUILD SCHEMA MARKUP -->
## PHASE 2: BUILD SCHEMA MARKUP

<!-- CONTEXT: Seo Geo Website Implementation / Step 2.1: Create Organization + LocalBusiness schema for Possibilities -->
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

**IMPORTANT:** Before deploying:
1. Fill in the actual phone number, social media URLs, and GBP URL
2. Find the actual lat/long coordinates for the business address
3. Find the real logo and hero image URLs from the live site
4. Test at https://search.google.com/test/rich-results

<!-- CONTEXT: Seo Geo Website Implementation / Step 2.2: Create schema for Recomposition -->
### Step 2.2: Create schema for Recomposition
Similar structure but with `@type: ["Organization", "MedicalBusiness"]` or appropriate type for health/wellness.

<!-- CONTEXT: Seo Geo Website Implementation / Step 2.3: Create FAQPage schema for key service pages -->
### Step 2.3: Create FAQPage schema for key service pages
For each major service page, create FAQ schema:
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

<!-- CONTEXT: Seo Geo Website Implementation / Step 2.4: Create BreadcrumbList schema -->
### Step 2.4: Create BreadcrumbList schema
For proper page hierarchy navigation:
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

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 3: DEPLOY TO WORDPRESS (CAREFULLY) -->
## PHASE 3: DEPLOY TO WORDPRESS (CAREFULLY)

<!-- CONTEXT: Seo Geo Website Implementation / Method 1: Code Snippet Plugin (SAFEST) -->
### Method 1: Code Snippet Plugin (SAFEST)
If WordPress has a code snippets plugin (WPCode, Code Snippets, or similar):
1. Add JSON-LD as a header snippet
2. Set to load on all pages (Organization) or specific pages (FAQ)
3. This is the SAFEST method — can be disabled instantly

<!-- CONTEXT: Seo Geo Website Implementation / Method 2: Theme Functions.php -->
### Method 2: Theme Functions.php
```php
function keystone_add_schema_markup() {
    // Only add Organization schema to homepage
    if (is_front_page()) {
        ?>
        <script type="application/ld+json">
        {
            // ... Organization schema here
        }
        </script>
        <?php
    }
}
add_action('wp_head', 'keystone_add_schema_markup');
```

<!-- CONTEXT: Seo Geo Website Implementation / Method 3: Yoast SEO / RankMath (if installed) -->
### Method 3: Yoast SEO / RankMath (if installed)
If either SEO plugin is installed, use its built-in schema editor instead of custom code.

<!-- CONTEXT: Seo Geo Website Implementation / ⚠️ BEFORE DEPLOYING: -->
### ⚠️ BEFORE DEPLOYING:
1. Take a full backup of the site
2. Test the JSON-LD at https://search.google.com/test/rich-results using "Code" input
3. Deploy to ONE page first (homepage) and verify
4. Wait 5 minutes, check the site loads correctly
5. Then deploy to remaining pages

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 4: AI BOT ACCESS -->
## PHASE 4: AI BOT ACCESS

<!-- CONTEXT: Seo Geo Website Implementation / Step 4.1: Update robots.txt to allow AI bots -->
### Step 4.1: Update robots.txt to allow AI bots
The following bots should be ALLOWED:
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
```

<!-- CONTEXT: Seo Geo Website Implementation / Step 4.2: Check if robots.txt is editable -->
### Step 4.2: Check if robots.txt is editable
In WordPress, robots.txt is usually virtual (generated by WordPress). To customize:
- Use Yoast SEO's robots.txt editor (if installed)
- Or create a physical `robots.txt` file in the web root
- Or use a robots.txt plugin

<!-- CONTEXT: Seo Geo Website Implementation / Step 4.3: Verify indexability -->
### Step 4.3: Verify indexability
After changes, submit URLs via:
- Google Search Console (manual URL inspection)
- The `keystone_instant_indexer` [[davinci-resolve-mcp/docs/SKILL|skill]] (pushes to Google Indexing API)
- Bing [[webmaster|Webmaster]] Tools (for ChatGPT/Copilot visibility)

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 5: CONTENT OPTIMIZATION FOR AI EXTRACTION -->
## PHASE 5: CONTENT OPTIMIZATION FOR AI EXTRACTION

<!-- CONTEXT: Seo Geo Website Implementation / Step 5.1: Implement "Answer-First" format on key pages -->
### Step 5.1: Implement "Answer-First" format on key pages
AI engines extract the first paragraph of a page. Restructure service pages:

**BEFORE (bad for AI):**
```
Welcome to Keystone Possibilities! We are a family-owned construction 
company that has been serving the community for many years...
```

**AFTER (good for AI):**
```
Keystone Possibilities is a custom home construction and renovation 
company serving Squamish, Whistler, and Pemberton in BC's Sea-to-Sky 
Corridor. Founded by Wayne Stevenson, we specialize in energy-efficient 
custom builds, Bill 44 compliance renovations, and full-service project 
management. Contact us at (XXX) XXX-XXXX for a free consultation.
```

<!-- CONTEXT: Seo Geo Website Implementation / Step 5.2: Add statistics and citations to pages -->
### Step 5.2: Add statistics and citations to pages
Research shows +37% AI visibility with statistics:
- "Over X projects completed in the Sea-to-Sky Corridor"
- "Serving homeowners since [year]"
- "Average build time: X months"
- "XX% client satisfaction rate"
- Reference BC Building Code sections where relevant

<!-- CONTEXT: Seo Geo Website Implementation / Step 5.3: Create Q&A content sections -->
### Step 5.3: Create Q&A content sections
On each service page, add a "Common Questions" section that maps to FAQ schema:
- Use the exact phrasing people would ask an AI
- "How much does X cost in Squamish?"
- "What permits do I need for Y in BC?"
- "How long does Z take?"

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 6: LOCAL CITATION BUILDING CHECKLIST -->
## PHASE 6: LOCAL CITATION BUILDING CHECKLIST

<!-- CONTEXT: Seo Geo Website Implementation / Step 6.1: Create/claim profiles on these platforms -->
### Step 6.1: Create/claim profiles on these platforms
(Don't do this automatically — create a checklist for Wayne to do manually with his login)

**HIGH PRIORITY (ChatGPT/Perplexity use these):**
- [ ] Google Business Profile — verify complete and up-to-date
- [ ] Bing Places for Business — https://www.bingplaces.com/ (CRITICAL for ChatGPT)
- [ ] Yelp Business — claim and optimize
- [ ] Better Business Bureau (BBB) — apply for listing
- [ ] HomeStars — https://www.homestars.com/ (Canada's #1 contractor directory)

**MEDIUM PRIORITY (AI engines cross-reference):**
- [ ] Houzz — https://www.houzz.com/ (contractor portfolios)
- [ ] RenoQuotes — https://www.renoquotes.com/ (Canadian reno leads)
- [ ] Yellow Pages Canada — https://www.yellowpages.ca/
- [ ] Facebook Business Page — ensure NAP matches exactly
- [ ] LinkedIn Company Page — complete with services and location

**LOWER PRIORITY (builds entity consistency):**
- [ ] Apple Maps — submit business listing
- [ ] Waze — add business location
- [ ] MapQuest — claim listing
- [ ] Foursquare — claim listing (feeds other platforms)

<!-- CONTEXT: Seo Geo Website Implementation / Step 6.2: NAP Consistency Check -->
### Step 6.2: NAP Consistency Check
**CRITICAL:** The Name, Address, Phone number MUST be IDENTICAL across ALL platforms.
- Even small differences like "St." vs "Street" confuse AI engines
- Create a [[master|master]] NAP reference and use it EXACTLY everywhere

Save this as: `Master_Docs/NAP_MASTER_REFERENCE.md`

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 7: WIKIDATA ENTITY CREATION -->
## PHASE 7: WIKIDATA ENTITY CREATION

<!-- CONTEXT: Seo Geo Website Implementation / Step 7.1: Check if Keystone Possibilities already has a Wikidata entry -->
### Step 7.1: Check if Keystone Possibilities already has a Wikidata entry
Search: https://www.wikidata.org/wiki/Special:Search?search=Keystone+Possibilities

<!-- CONTEXT: Seo Geo Website Implementation / Step 7.2: If not, create one -->
### Step 7.2: If not, create one
Wikidata is free and open — anyone can create entries. This is MASSIVELY important because:
- ChatGPT cites Wikipedia/Wikidata in 47.9% of top responses
- A Wikidata entry makes you a "verified entity" to all AI engines

**Required properties:**
- Label: "Keystone Possibilities"
- Description: "Construction company in Squamish, British Columbia, Canada"
- Instance of (P31): Q4830453 (construction company) or Q891723 ([[general|general]] contractor)
- Country (P17): Q16 (Canada)
- Located in (P131): Q184694 (Squamish)
- Official website (P856): https://keystonepossibilities.com
- Founder (P112): Wayne Stevenson

<!-- CONTEXT: Seo Geo Website Implementation / Step 7.3: Link Wikidata to sameAs schema -->
### Step 7.3: Link Wikidata to sameAs schema
Once created, add the Wikidata URL to the sameAs array in the Organization schema.

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 8: BLOG-TO-VIDEO TRAFFIC LOOP -->
## PHASE 8: BLOG-TO-VIDEO TRAFFIC LOOP

<!-- CONTEXT: Seo Geo Website Implementation / Step 8.1: Understand the loop -->
### Step 8.1: Understand the loop
```
YouTube Video → Blog Post (embedded video + transcript + FAQ)
                     ↓
               Google indexes blog post
                     ↓
               AI engines cite blog post in answers
                     ↓
               Traffic flows back to YouTube + website
```

<!-- CONTEXT: Seo Geo Website Implementation / Step 8.2: Template for converting videos to blog posts -->
### Step 8.2: Template for converting videos to blog posts
For each YouTube video published, create a corresponding blog post:
```markdown
Title: [Video Title] — [Primary Keyword] in [Location]

[Embed YouTube video]

<!-- CONTEXT: Seo Geo Website Implementation / Overview -->
## Overview
[2-3 sentence summary with answer-first format]

<!-- CONTEXT: Seo Geo Website Implementation / Key Points -->
## Key Points
[Bullet points extracted from video transcript]

<!-- CONTEXT: Seo Geo Website Implementation / Detailed Breakdown -->
## Detailed Breakdown
[Expanded content with statistics, citations, expert quotes]

<!-- CONTEXT: Seo Geo Website Implementation / Frequently Asked Questions -->
## Frequently Asked Questions
[FAQ section matching FAQ schema]

<!-- CONTEXT: Seo Geo Website Implementation / About the Author -->
## About the Author
Wayne Stevenson is the founder of Keystone Possibilities, specializing in 
custom home construction in BC's Sea-to-Sky Corridor. [credentials]
```

<!-- CONTEXT: Seo Geo Website Implementation / Step 8.3: Set up the workflow -->
### Step 8.3: Set up the workflow
Create a new [[davinci-resolve-mcp/docs/SKILL|skill]] or update `10_content_pipeline` to include:
1. After video upload → automatically generate blog post draft
2. Blog post includes embedded video, transcript, and FAQ schema
3. Push to WordPress via REST API (if credentials available)
4. Submit URL to Google Indexing API via `keystone_instant_indexer`

---

<!-- CONTEXT: Seo Geo Website Implementation / PHASE 9: VERIFICATION -->
## PHASE 9: VERIFICATION

<!-- CONTEXT: Seo Geo Website Implementation / Step 9.1: Schema validation -->
### Step 9.1: Schema validation
Test all deployed schemas at:
- https://search.google.com/test/rich-results
- https://validator.schema.org/

<!-- CONTEXT: Seo Geo Website Implementation / Step 9.2: AI visibility check -->
### Step 9.2: AI visibility check
Use brave-search or chrome-devtools to check:
- Ask ChatGPT: "Who is the best contractor in Squamish?"
- Ask Perplexity: "construction companies in Squamish BC"
- Check Google for: "site:keystonepossibilities.com" (verify indexing)

<!-- CONTEXT: Seo Geo Website Implementation / Step 9.3: Document everything -->
### Step 9.3: Document everything
Save all audit results, changes made, and verification results to:
`Master_Docs/SEO_Audit_Results/`

---

<!-- CONTEXT: Seo Geo Website Implementation / SUCCESS CRITERIA -->
## SUCCESS CRITERIA
- [ ] Both websites audited with full reports
- [ ] Organization + LocalBusiness schema created and validated
- [ ] FAQPage schema created for service pages
- [ ] Schema deployed to at least the homepage of both sites
- [ ] robots.txt updated to allow AI bots
- [ ] NAP master reference created
- [ ] Local citation checklist created for Wayne
- [ ] Wikidata entity creation documented (or created)
- [ ] Blog-to-video loop template established
- [ ] All changes verified with schema validators
- [ ] NO website breakage — both sites load correctly


---
📁 **See also:** [[Master_Docs/Gemini_Pro_Instructions/INDEX|← Directory Index]]
