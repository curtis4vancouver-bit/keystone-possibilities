# Amazon KDP E-Book & Paperback Packaging Guide

> **Prepared For:** Wayne Stevenson / Keystone Empire  
> **Topic:** Packaging and Formatting the *Keystone Protocol E-Manual*  
> **Objective:** Distribute the manual globally via Amazon KDP (paperback + Kindle) while bypassing App Store fees by offering direct high-fidelity downloads to PWA members.

---

## 🎯 Section 1: KDP Formatting & Design Specifications

To ensure the book prints perfectly on Amazon and compiles cleanly into Kindle format, the manuscript source document must adhere to strict typography and layout rules.

### 📐 1. Physical Layout Standards (6" x 9" Industry Standard)
For high-end men's health and wellness manuals, the standard industry trim size is **6 in x 9 in (15.24 x 22.86 cm)**.

| Layout Attribute | Specification (No Bleed) | Specification (With Bleed) |
| :--- | :--- | :--- |
| **Trim Size** | 6.00" x 9.00" | 6.125" x 9.25" |
| **Inside Margin (Gutter)** | **0.75 in** (crucial for bound pages) | **0.875 in** |
| **Outside Margin** | **0.50 in** | **0.50 in** |
| **Top & Bottom Margins** | **0.50 in** | **0.50 in** |
| **Font Family** | **Garamond, Georgia, or Minion** | Standard Serif family |
| **Font Size (Body)** | **11 pt or 12 pt** | 1.15 line spacing |

### 🖋️ 2. Formatting Typography Guidelines
*   **The "Journal vs. Blueprint" Phrasing Guardrail:** Under Amazon’s strict health guidelines and YouTube's YMYL compliance, keep terminology academic. Use phrases like *"physiological case study"* or *"cellular health schedule"* instead of *"medical prescription"* or *"dosing schedule"*.
*   **Aesthetics:** Headings should be in sans-serif (e.g., **Inter** or **Outfit**) to match the modern, premium aesthetic of the Keystone brand. Headings should be centered with exact page-break commands pre-set in the compilation pipeline.

---

## 📂 Section 2: PWA Digital Handoff (The Bypass Strategy)

To bypass Apple's and Google's 30% digital store cuts, we will utilize the **WordPress REST API & WooCommerce Handshake**:

```
[Customer buys book on website / PWA Portal]
           │
           ▼
[WooCommerce issues unique single-use token]
           │
           ▼
[Secure Node/Postgres script verifies user session]
           │
           ▼
[Serves highly secure PDF/ePub download from Supabase Storage]
```

1.  **Secure Storage Bucket:** The finalized manual compiles into a secure, access-controlled Supabase Storage Bucket (`/manuals/keystone-protocol-v1.pdf`).
2.  **JWT Verification:** Only users authenticated via our Next.js PWA with an active 'member' role are permitted to request the download endpoint, preventing link sharing.

---

## 🛠️ Section 3: Creating your Local Workspace

We will maintain the master files and compilation scripts inside a local directory:  
`C:\Users\Curtis\Keystone_Downloads\`

### File Structure:
*   `C:\Users\Curtis\Keystone_Downloads\Manuscript_Raw.txt` - Your raw content files.
*   `C:\Users\Curtis\Keystone_Downloads\Templates\` - PDF and Word templates pre-sized to 6" x 9".
*   `C:\Users\Curtis\Keystone_Downloads\Output\` - Final compiled `.epub` and `.pdf` files ready to upload.

---

> **Action Item:** Run the automated script `setup_kdp_workspace.ps1` in your workspace's `scratch/` folder to build this folder structure at `C:\Users\Curtis\Keystone_Downloads` and pull down the basic layout files.