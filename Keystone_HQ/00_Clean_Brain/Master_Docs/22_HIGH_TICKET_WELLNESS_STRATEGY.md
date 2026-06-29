---
id: doc-22highticketwellnessstrategy
title: High Ticket Wellness Strategy
type: document
summary: This master document details the technical and operational blueprint for
  the Sea-to-Sky Alpine Wellness Niche Integration, blending active B2B Proj...
entities:
- Sea-to-Sky
- Squamish
- Vancouver
- Whistler
created: '2026-05-24T16:15:51.672948'
updated: '2026-06-14T19:57:35.941453'
---
# High-Ticket Direct-to-Consumer Curated Hybrid E-Commerce & Autonomous SDR Blueprint

This [[master|master]] document details the technical and operational blueprint for the **Sea-to-Sky Alpine Wellness Niche Integration**, blending active B2B Project Management/Construction services with passive, high-ticket Direct-to-Consumer (DTC) hardware affiliate pipelines.

---

<!-- CONTEXT: High Ticket Wellness Strategy / 1. The High-Ticket Curated Hybrid Model -->
## 1. The High-Ticket Curated Hybrid Model

Traditional low-ticket dropshipping and low-margin affiliate loops fail on premium wellness hardware (saunas, cold plunges, connected smart scales). This blueprint overcomes these failures by positioning the digital portal as an **authorized regional showroom and local concierge**, routing fulfillment directly to DTC manufacturing partners while collecting premium commissions.

<!-- CONTEXT: High Ticket Wellness Strategy / A. Core Transactional Matrix -->
### A. Core Transactional Matrix

| Product Category | Representative Brand | AOV (USD/CAD) | Net Commission | Cookie Window | Net Payout / Unit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Commercial Plunge Tub** | Bluecube Malibu | $15,999.00 USD | Flat Fee Structure | Lifetime | **$1,000.00 USD** |
| **All-in-One Home Plunge** | Plunge All-In Gen 2 | $5,500.00 USD | 10.00% Cash Payout | 90 Days | **$550.00 USD** |
| **Luxury Infrared Sauna** | Sunlighten mPulse | $8,500.00 USD | 6.00% (Awin: 63394) | 30 Days | **$510.00 USD** |
| **Connected Biomarker Scale** | Withings Body Scan | $399.00 USD | 10.00% (CJ: 4996850) | 30 Days | **$39.90 USD** |
| **Custom Local Cedars** | Secret Sauna Company | $29,000.00 CAD | 5.00% lead referral fee | Direct | **$1,450.00 CAD** |

---

<!-- CONTEXT: High Ticket Wellness Strategy / 2. Zero-Inventory Localized Fulfillment Map -->
## 2. Zero-Inventory Localized Fulfillment Map

By partnering with local site-prep contractors and physical showrooms, the portal turns online dropshipping friction into a seamless high-end local installation package.

<!-- CONTEXT: High Ticket Wellness Strategy / A. Regional Showroom Partners -->
### A. Regional Showroom Partners
* **Poolside Spa Sales & Service**: Showrooms in Squamish (#316-1201 Commercial Way) and Whistler (#1-1209 Alpha Lake Road). Local distributor of plug-and-play year-round Kodiak Plunges ($7,995 CAD) with integrated Financeit programs. Serves as our warranty and chemical-balancing concierge.

<!-- CONTEXT: High Ticket Wellness Strategy / B. Regional Site Preparation & Construction Partners -->
### B. Regional Site Preparation & Construction Partners
* **Martin Landscapes (Squamish)**: Led by Colin. Specializes in custom stone paver pads, sloped garden grading, retaining walls, and timber decking for Nootka and other prefab saunas.
* **SOLscapes (Squamish & Whistler)**: Focuses on low-impact, ecologically sustainable landscape prep using quiet electric commercial gear.
* **Pika Landscapes (Whistler)**: High-end carpentry and sloped grading for elite chalets.
* **The Great Canadian Landscaping Company (Squamish)**: Over 23 years of North Shore decking, timber framing, and outdoor lighting experience.

---

<!-- CONTEXT: High Ticket Wellness Strategy / 3. Front-End Redirect Engineering (Shopify OS 2.0) -->
## 3. Front-End Redirect Engineering (Shopify OS 2.0)

For high-ticket products requiring external manufacturer checkout, we programmatically strip the standard Shopify cart forms and inject an outbound redirect button tied to the product's metafield (`product.metafields.custom.affiliate_url`).

<!-- CONTEXT: High Ticket Wellness Strategy / Custom Override: `snippets/buy-buttons.liquid` -->
### Custom Override: `snippets/buy-buttons.liquid`

```liquid
{% if product.metafields.custom.affiliate_url != blank %}
  <div class="product-form__buttons custom-redirect-wrapper">
    <a
      href="{{ product.metafields.custom.affiliate_url }}"
      target="_blank"
      rel="noopener nofollow"
      class="product-form__submit button button--full-width button--primary outbound-redirect-btn"
      id="OutboundRedirect-{{ product.id }}"
      data-affiliate-target="{{ product.metafields.custom.affiliate_url | escape }}"
      data-product-title="{{ product.title | escape }}"
      data-product-id="{{ product.id }}"
    >
      <span>Secure Purchase via Certified Partner</span>
    </a>
  </div>

  {% style %}
    .custom-redirect-wrapper { margin: 1.5rem 0; width: 100%; }
    .outbound-redirect-btn {
      display: inline-flex !important; align-items: center; justify-content: center;
      text-decoration: none; box-sizing: border-box; background-color: #080808 !important;
      color: #ffffff !important; border: 1px solid rgba(196, 162, 101, 0.35) !important;
      font-family: 'Outfit', sans-serif; text-transform: uppercase; letter-spacing: 0.18em;
      transition: all 0.4s ease;
    }
    .outbound-redirect-btn:hover {
      background-color: #111111 !important; border-color: rgba(196, 162, 101, 0.85) !important;
      color: #c4a265 !important; box-shadow: 0 0 15px rgba(196, 162, 101, 0.15);
    }
    .product-form__quantity, .shopify-payment-button, .product-form__input--quantity {
      display: none !important;
    }
  {% endstyle %}
{% endif %}
```

---

<!-- CONTEXT: High Ticket Wellness Strategy / 4. Attribution & Web Pixel Sandbox Defenses -->
## 4. Attribution & Web Pixel Sandbox Defenses

Shopify’s secure Web Pixel sandbox isolates script environments and breaks traditional Google Tag Manager DOM click triggers. To bypass this, we run a hybrid routing setup:

```
+-------------------------------------------------------------+
|                      STOREFRONT DOM                         |
|   (GTM Web Container loaded directly via theme.liquid)       |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     GOOGLE TAG MANAGER                      |
|                                                             |
|   1. Auto-Event Variable (Is Outbound = True)               |
|   2. Element Attribute (data-affiliate-target)              |
|   3. Outbound Link Click Trigger (2000ms delay)             |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     GOOGLE ANALYTICS 4                      |
|            (Logs 'affiliate_click' Event)                   |
+-------------------------------------------------------------+
```

<!-- CONTEXT: High Ticket Wellness Strategy / Key GTM Triggers & Wait Delays: -->
### Key GTM Triggers & Wait Delays:
* **Trigger Type**: Click - Just Links
* **Wait for Tags**: Enabled with a **2000ms maximum delay** (giving pixel scripts enough time to fire conversions before the page redirects the user away).
* **Firing Conditions**: `aev - Is Outbound equals true` AND `Click Classes contains outbound-redirect-btn`.

---

<!-- CONTEXT: High Ticket Wellness Strategy / 5. Structured SEO Schema for High-Ticket Visibility -->
## 5. Structured SEO Schema for High-Ticket Visibility

We Consolidation of JSON-LD schemas into a single, comprehensive metadata block to maximize organic click-through rates (CTR) on Google.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://keystonepossibilities.ca/#local-wellness-directory",
      "name": "Sea-to-Sky Alpine Wellness Directory",
      "priceRange": "$$$$",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "316-1201 Commercial Way",
        "addressLocality": "Squamish",
        "addressRegion": "BC",
        "postalCode": "V8B 0G1",
        "addressCountry": "CA"
      },
      "areaServed": [
        {"@type": "AdministrativeArea", "name": "Squamish"},
        {"@type": "AdministrativeArea", "name": "Whistler"},
        {"@type": "AdministrativeArea", "name": "West Vancouver"}
      ]
    }
  ]
}
```

---

<!-- CONTEXT: High Ticket Wellness Strategy / 6. Programmatic SDR Lead-Gen Agent (Google Antigravity SDK) -->
## 6. Programmatic SDR Lead-Gen Agent (Google Antigravity SDK)

To continuously parse the Sea-to-Sky corridor for [[hot|hot]] B2B short-term rental (STR) leads, run financial ROI models, and draft custom proposals, we deploy a secured autonomous agent via the `google-antigravity` framework.

The script initializes a secure execution harness with:
1. **Least-Privilege Containment**: Restricting file writes to a local secure workspace.
2. **Interactive Deciders**: Querying the user for approval via terminal loops before initiating any shell redirects or sending actual outreach emails.
3. **GraphRAG Memory**: Connecting directly to `sqlite-graphrag` to prevent memory drift over long research horizons.

*The fully functioning python SDR lead agent template is permanently stored at `scratch/autonomous_lead_agent.py`.*


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
