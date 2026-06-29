---
id: doc-gcp10kcreditsredemptionguide
title: Gcp 10K Credits Redemption Guide
type: document
summary: '> Prepared For: Wayne Stevenson / Keystone Empire'
tags:
- document
- okf
- wayne-stevenson
created: '2026-05-20T18:45:56.259643'
updated: '2026-06-14T19:57:36.004611'
entities:
- Wayne Stevenson
---

# 💎 Google Cloud $10,000 Model Garden Credits Redemption Guide

> [!IMPORTANT]
> **Prepared For:** Wayne Stevenson / Keystone Empire  
> **Credit Category:** Google for Startups (GFS) Cloud Program — Scale/Scale AI Tier Partner Credits  
> **Application:** Offsets API and hosting costs for third-party partner models (Anthropic Claude, Mistral AI, Llama, AI21) running directly inside **Vertex AI Model Garden**.

---

## 🎯 Section 1: How the $10,000 Credits Work

At Google I/O 2026, Google announced deep partnerships with premium model providers. To accelerate developer scaling, the **Google for Startups Cloud Program** allocates a specialized **$10,000 credit code** (valid for 12 months) for Scale-tier portfolios. 

*   **Standard GCP Credits vs. Model Garden Credits:** Standard credits offset general VM compute (like Cloud Run or Compute Engine). Model Garden partner credits are specifically applied to the **Vertex AI model registry** to cover endpoints of non-Google foundation models.
*   **Automatic Drawdown:** Once activated on your primary billing account, any API calls made to Model Garden partner models will deduct directly from this $10,000 balance, resulting in a **$0.00 net monthly out-of-pocket invoice** for our advanced LLM pipelines.

---

## 🛠️ Section 2: Step-by-Step Redemption Procedure

Follow these steps to claim and apply your $10,000 promotional balance:

### Step 1: Open the Google for Startups Portal
1. Navigate to the [Google for Startups Cloud Program Console](https://cloud.google.com/startup).
2. Click **Sign In** in the top-right corner and use your primary enterprise Google account associated with the Keystone brand.
3. In the navigation sidebar, select **"Benefits & Rewards"**.

### Step 2: Retrieve your GFS Promo Key
1. Locate the active offer panel titled **"Vertex AI Model Garden Partner Model Credits ($10,000)"**.
2. Click **"Generate Promo Key"** or **"Copy Key"**. This is a 24-character alphanumeric string (e.g., `GFS-SCALE-MODEL-GARDEN-XXXX`).

### Step 3: Redeem in the Google Cloud Billing Console
1. Open the [Google Cloud Console Billing Dashboard](https://console.cloud.google.com/billing).
2. Ensure your active billing account (e.g., **"Keystone Empire Billing"**) is selected from the dropdown at the top.
3. In the left navigation pane, select **"Credits"** (located under the Billing section).
4. Scroll to the bottom or locate the **"Promotional Codes"** tab.
5. Click the **"Redeem Promotion Code"** button.
6. Paste your copied 24-character key into the input field and click **"Apply"**.
7. **Verification:** You will instantly see a success dialog: *"Promotion Applied: $10,000 Vertex AI Model Garden Partner Credits active."*

---

## 🚨 Section 3: Setting Up Safeguards (Budgets & Alerts)

To ensure we never exceed your credit allotment and to keep your card completely safe, we must set up a strict budget alarm.

### 1. Create a Budget Alarm
1. In the left navigation of the Billing console, click on **"Budgets & alerts"**.
2. Click **"Create Budget"** at the top.
3. **Name:** `Keystone Model Garden Credit Safeguard`
4. **Time range:** Monthly.
5. **Projects & Services:** Select **Vertex AI** and **Cloud Run** (uncheck other services to keep this specific).
6. **Amount Type:** Specified Amount.
7. **Target Amount:** Enter **`$500.00`** (representing 5% of your total credit buffer).

### 2. Configure Action Thresholds
Set the budget triggers to alert you immediately via email:
*   **Trigger 1 (50%):** Alert when spending reaches **$250** (emails Wayne and the Dev Agent).
*   **Trigger 2 (90%):** Alert when spending reaches **$450**.
*   **Trigger 3 (100%):** Alert when spending reaches **$500**.

> [!TIP]
> **Action Item:** Once redemption is complete, run the local diagnostic check on `content_engine_mcp.py` to confirm that the Vertex AI API connection is successfully hitting your active billing account.

---
📁 **See also:** ← Directory Index