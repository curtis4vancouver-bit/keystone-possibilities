---
id: doc-05pwacommandcenter
title: Pwa Command Center
type: document
summary: The Complete Software Requirements Document
entities:
- GCS
- Squamish
created: '2026-05-02T09:11:51.259014'
updated: '2026-06-14T19:57:35.842012'
---
# KEYSTONE PWA COMMAND CENTER: SYSTEM [[ARCHITECTURE|ARCHITECTURE]]
**The Complete Software Requirements Document**

---

<!-- CONTEXT: Pwa Command Center / 1. CURRENT DEPLOYMENT [[STATE|STATE]] -->
## 1. CURRENT DEPLOYMENT [[STATE|STATE]]

- **Frontend:** Next.js deployed on Vercel.
- **Backend:** Supabase (PostgreSQL Database, Authentication, Edge Functions, Storage).
- **CI/CD:** GitHub + Vercel auto-deploy on merge to main.
- **Repository:** curtis4vancouver-bit/construction-website
- **Critical [[STATE|State]] Check:** The `on_auth_user_created` trigger has been fixed. New users are automatically inserted into the `profiles` table upon signup with the default role of 'trades'.

---

<!-- CONTEXT: Pwa Command Center / 2. ROLE-BASED ACCESS CONTROL (RBAC) -->
## 2. ROLE-BASED ACCESS CONTROL (RBAC)

- **Admin/PM (Wayne):** Full read/write access. Can create projects, assign trades, approve milestones, and upload [[master|master]] blueprints.
- **Trades:** Read access to assigned projects. Can check off milestones, upload photos of completed work, and view relevant site documents.

---

<!-- CONTEXT: Pwa Command Center / 3. TRADE SEQUENCING & CHECKLIST SYSTEM -->
## 3. TRADE SEQUENCING & CHECKLIST SYSTEM

The core feature of the PWA is the automated milestone and trade sequencing system.

- **Sequential Logic:** Trades cannot mark their phase as complete until the prerequisite trade is finished (e.g., Drywall cannot start until Framing and Electrical Rough-in are checked off).
- **Notification Engine:** When a trade checks off a milestone, the system automatically alerts the PM and the next trade in the sequence that the site is ready.

---

<!-- CONTEXT: Pwa Command Center / 4. MASTER TRADE LIST & PHASING -->
## 4. MASTER TRADE LIST & PHASING

| Phase | Trades |
|---|---|
| Phase 1: Pre-Construction & Engineering | GC, Architect, Engineer, Surveyor |
| Phase 2: Site Prep & Foundation | Excavation, Formwork, Concrete, Drainage |
| Phase 3: Framing & Exterior Envelope | Framing, Roofing, Siding, Windows |
| Phase 4: Rough-Ins (MEP) | Plumbing, Electrical, HVAC |
| Phase 5: Insulation & Boarding | Insulation, Drywall |
| Phase 6: Interior Finishes | Cabinetry, Tile, Flooring, Paint |
| Phase 7: Fixtures & Final | Plumbing Fixtures, Electrical Fixtures, Appliances |
| Phase 8: Exterior Final & Handover | Landscaping, Fencing, Cleaning |

---

<!-- CONTEXT: Pwa Command Center / 5. SaaS MULTI-TENANT ARCHITECTURE (Future) -->
## 5. SaaS MULTI-TENANT ARCHITECTURE (Future)

<!-- CONTEXT: Pwa Command Center / Super Admin Tier (SaaS Ownership) -->
### Super Admin Tier (SaaS Ownership)
- Ultimate God-Mode. Can see all Tenants (Renting GCs).
- Features: Tenant Management, Global Platform Metrics, Billing Management (Stripe API placeholder).

<!-- CONTEXT: Pwa Command Center / GC Command Center (Tenant Level) -->
### GC Command Center (Tenant Level)
- Restricted ONLY to this specific GC's company and their respective projects via Tenant_ID.
- Features: Advanced Analytics Dashboard (Budget Variance, Timeline Variance, $/sq ft, Change Order Tracker, Trade Reliability Score), Interactive Master Timeline (FullCalendar.io).

<!-- CONTEXT: Pwa Command Center / Trade Portals (Individual Contractor Tier) -->
### Trade Portals (Individual Contractor Tier)
- Secure, siloed login. Strict RBAC.
- Features: Contract & Permits, Compliance & Formal Reports Upload, Weekly Verification Module (Timestamp/Geotag overlays), Financial Ledger.

---

<!-- CONTEXT: Pwa Command Center / 6. [[GEMINI|GEMINI]] AI AUTOMATION INTEGRATION (Future "Smart" Layer) -->
## 6. GEMINI AI AUTOMATION INTEGRATION (Future "Smart" Layer)

- **API Connection:** Google Gemini API (Multimodal).
- **Invoice Processing:** Extracts Vendor, Amount, Date.
- **Delivery Verification:** Cross-references tickets against Material Take-Offs.
- **Automated Data Entry:** Categorizes uploads via GPS, EXIF data, and visual context.

---

<!-- CONTEXT: Pwa Command Center / 7. CRITICAL SYSTEM REQUIREMENTS -->
## 7. CRITICAL SYSTEM REQUIREMENTS

- **Offline Mode / Service Workers:** Local caching. If offline, the app stores payloads and pushes the REST API POST request automatically upon reconnection.
- **Notification Engine:** Web push notifications or SendGrid alerts.
- **Security & Authorization:** Strict REST API endpoints authenticated via JWT and validated against Tenant_ID and User_Role.

---

<!-- CONTEXT: Pwa Command Center / 8. NEXT DEVELOPMENT STEPS -->
## 8. NEXT DEVELOPMENT STEPS

1. **Magic Link Authentication:** Finalize passwordless login for older trades who struggle with remembering passwords.
2. **Document Storage Bucket:** Hook up the Supabase Storage bucket so PMs can upload PDFs of building plans directly to the specific project dashboard.
3. **LinkedIn Lead Funnel:** Drive traffic from the optimized LinkedIn profile (highlighting St. Andrews and Ballantree residences) directly to a landing page that captures PM leads and funnels them into the PWA.
4. **The "Vault Key" (Future):** PMs issued a single-use, project-specific alphanumeric ID Code (e.g., `SQUAMISH-77A`). They enter this code on the PWA to access their dashboard. Only Admin can reset/deactivate.


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]

**Related:** [[OTS_Command_Center_Deep_Research]]
