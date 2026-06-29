# GCP API Security, Multi-Account Isolation, and Automated Billing Disconnects

This document details the operational strategy to secure Gemini Developer API credentials, analyze Google AI Studio’s rate-limit mathematics, configure anti-fraud isolation profiles, and deploy serverless programmatic billing controls to prevent unexpected cloud development overruns.

---

## 1. The Default API Key Vulnerability

A major security gap exists in default Google Cloud Platform (GCP) configurations:
* **The Vulnerability**: Legacy GCP API keys (prefixed with `AIza`) originally created for public-facing maps or basic analytics inherit access to the **Generative Language API** (Gemini) as soon as it is enabled in the project. Scraper bots regularly sweep public repositories for these unrestricted keys, exploiting them to run massive LLM queries and racking up five-figure API bills.
* **The June 19, 2026 Mandate**: Google blocks unrestricted keys from accessing Gemini. Developers must explicitly restrict every active API key exclusively to the *Generative Language API* or migrate to *Vertex AI* (which utilizes short-lived service account OAuth2 tokens instead of static keys).

---

## 2. AI Studio Free Tier Quota Limits & Token Bucket Math

Google AI Studio manages free tier requests using a **Token Bucket algorithm** rather than static time-window resets, meaning replenishment occurs continuously:

$$T_{\text{available}} = \min\left(T_{\text{max}}, T_{\text{current}} + \Delta t \times r\right)$$

Where $T_{\text{max}}$ is the burst capacity, and $r$ is the token replenishment rate per second.

### Core Developer Rate Limits (GA 2026 Baseline):
* **Gemini 2.0 Flash**: 15 RPM (Requests Per Minute) | 1,000,000 TPM | 1,500 RPD (Requests Per Day) | Paid tier input: $0.075/1M.
* **Gemini 2.5 Flash**: 10 RPM | 250,000 TPM | 1,500 RPD | Paid tier input: $0.30/1M.
* **Gemini 2.5 Pro**: 5 RPM | 150,000 TPM | 50 RPD | Paid tier input: $1.25/1M.

---

## 3. Anti-Fraud Mechanics & Multi-Account Isolation Realism

Google Cloud deploys a machine-learning-driven anti-abuse pipeline to block developers from farming free trials:

1. **Digital Fingerprinting**: Google checks WebGL/Canvas graphics rendering signatures and audio stacks (Web Audio API outputs). This fingerprint remains identical even if you clear cookies or use private browsing.
2. **Network Routing**: Evaluates BGP routing, DNS setups, and local latency. Commercial VPNs or datacenter proxy IPs are instantly flagged.
3. **Payment Profile Hashing**: Credit cards linked to a free trial undergo tokenization checks. Reusing the same credit card, cardholder name, or bank account across multiple Google accounts triggers an **"Identity Association Cascading Ban"** which suspends all connected billing projects immediately.
4. **Phone Carrier Lock**: Throttles SMS verification using carrier-level database lookups (restricting numbers to major Mobile Network Operators like AT&T/Rogers while blocking virtual SIMs or VoIP numbers).

---

## 4. Programmatic Hard & Soft Cost Controls

Because default GCP budget alerts are purely informational (sending emails but letting resources continue to run), developers must implement automated controls to prevent surprise charges:

### A. Programmatic Hard Cap (Billing Decoupling)
When a project crosses a strict budget limit (e.g., $10/month), a Google Pub/Sub alert fires, triggering a serverless Python Cloud Function. This function updates the project’s linked billing account to an empty string (`""`), breaking the billing association:

```
+--------------------------------------------------------------+
| 1. GCP BUDGET MONITOR                                        |
|    Crosses threshold (e.g., $10 USD) and publishes alert      |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| 2. PUB/SUB TOPIC EVENT                                       |
|    Securely routes event payload containing cost metrics     |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
| 3. CLOUD RUN FUNCTION (Python Decoupler)                     |
|    Calls Billing Client and sets Billing Account to ""        |
+--------------------------------------------------------------+
```

*The complete python billing disconnector is permanently stored at `scratch/gcp_billing_decouple.py`.*

### B. Programmatic Soft Cap (Quota Overrides)
To prevent the destructive shutdowns of a hard cap (which kills virtual machines and can corrupt active databases), developers apply regional **Consumer Quota Overrides** via Terraform. This throttles incoming APIs and returns standard `429 Resource Exhausted` errors once a cost threshold is met, leaving storage and logging safe:

```hcl
# File: scratch/gcp_soft_cap.tf
resource "google_service_usage_consumer_quota_override" "bigquery_daily_cap" {
  project        = var.project_id
  service        = "bigquery.googleapis.com"
  metric         = "bigquery.googleapis.com/quota/query/usage"
  limit          = "/d/project"
  override_value = "104857600" # Restricts query usage to 100 TB daily (~$500 cap)
  force          = true
}
```

*The complete Terraform soft-cap override blueprint is permanently stored at `scratch/gcp_soft_cap.tf`.*