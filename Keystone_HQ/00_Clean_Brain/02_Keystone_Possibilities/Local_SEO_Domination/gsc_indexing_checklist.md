# GSC Fast-Track Indexing Playbook: 24-Hour Local SEO Domination

This operational checklist outlines the precise technical sequence required to [[wiki/index|index]] and reconcile the three new Suna Spa backyard wellness landing pages and the [[master|Master]] JSON-LD schema within 24 hours of deployment.

---

## Phase 1: Deployment & Structural Validation (Hours 1–2)

- [ ] **Step 1.1: Deploy Static Pages to Live Environment**
  - Push the four HTML files (`whistler_sauna.html`, `west_vancouver_sauna.html`, `north_vancouver_sauna.html`, `squamish_sauna.html`) and the Master Schema (`master_schema.json`) to the live production server (e.g., via the WP Pusher or manual CI/CD pipeline).
  - Verify that the URLs resolve perfectly and return a clean HTTP `200 OK` status with correct MIME types (`text/html` and `application/json`).
  - **Live URL Map:**
    - `https://www.keystonepossibilities.com/whistler-sauna/`
    - `https://www.keystonepossibilities.com/west-vancouver-sauna/`
    - `https://www.keystonepossibilities.com/north-vancouver-sauna/`
    - `https://www.keystonepossibilities.com/squamish-sauna/`
    - `https://www.keystonepossibilities.com/sunshine-coast-sauna/`
    - `https://www.keystonepossibilities.com/wp-content/uploads/seo/master_schema.json`

- [ ] **Step 1.2: Validate H-Tag Layout Hierarchy**
  - Run each URL through a local validator or the Chrome DevTools lighthouse audit.
  - Confirm **H-Tag Integrity** to protect the Knowledge Panel:
    * Exactly ONE `<h1>` per page.
    * No skipped heading levels (e.g., `<h1>` followed immediately by `<h2>` and `<h3>`, never skipping from `<h2>` to `<h4>`).
    * Zero non-semantic elements (like divs or buttons) wrapped in H-tags.

- [ ] **Step 1.3: Verify Integrated JSON-LD Schema Syntactical Accuracy**
  - Copy the embedded JSON-LD scripts from the HTML headers and test them in the [Google Rich Results Test](https://search.google.com/test/rich-results) tool.
  - Ensure zero "Critical Errors" or "Warnings" are flagged.
  - Confirm the local schemas (`LocalBusiness`, `Service`) successfully reference the primary Organization ID (`https://www.keystonepossibilities.com/#organization`) and Wayne Stevenson's Person ID (`https://www.keystonepossibilities.com/wayne-stevenson/#person`) to establish the semantic bridge.

---

## Phase 2: Internal Linking & Crawl Equity Distribution (Hours 2–4)

- [ ] **Step 2.1: Header/Footer Hardlink Integration**
  - Do not orphan the new landing pages. Hardlink all four pages in the global footer of the primary `https://www.keystonepossibilities.com/` domain.
  - Anchor text must be highly localized and entity-focused:
    * `"Custom Alpine Saunas - Whistler"`
    * `"Panoramic Cliffside Saunas - West Vancouver"`
    * `"Root-Sensitive Forest Saunas - North Vancouver"`
    * `"Cantilevered Cliffside Saunas - Squamish"`
  - This guarantees that Googlebot discovers the links immediately during its next sweep of the home page.

- [ ] **Step 2.2: Contextual Link Placement (The B2B Gateway)**
  - Edit the main Project Management / Custom Build pages of the website to insert highly contextual internal anchors linking to the new local wellness targets.
  - Example copy: *"Our extreme-environment construction expertise is deployed in both multi-million dollar developments and bespoke wellness sanctuaries like our [deck-engineered Whistler sauna builds](/whistler-sauna/), [cliffside West Vancouver installations](/west-vancouver-sauna/), and [cantilevered Squamish builds](/squamish-sauna/)."*

---

## Phase 3: Google Search Console (GSC) Execution (Hours 4–8)

- [ ] **Step 3.1: XML Sitemap Injection**
  - Regenerate the website XML sitemap (`sitemap.xml`) to include the four new URLs.
  - Set the `<lastmod>` tag for each page to the current date and time in ISO 8601 format.
  - Set the `<changefreq>` to `weekly` and `<priority>` to `0.80`.
  - Access the **Sitemaps** report in GSC and re-submit the root `sitemap.xml` URL. This triggers an automated crawl scheduler scan.

- [ ] **Step 3.2: URL Inspection & Force-Indexation Queue**
  - Open the **GSC Dashboard** for the verified `keystonepossibilities.com` property.
  - Paste the Whistler sauna page URL into the search bar at the top (URL Inspection tool).
  - Click **Test Live URL** to force Googlebot to render the page in real-time, verifying mobile friendliness and schema detection.
  - Click **Request Indexing**. This places the URL in a priority indexing queue.
  - Repeat this exact process for the West Vancouver, North Vancouver, and Squamish landing pages.

---

## Phase 4: Programmatic API Indexation Bypass (Hours 8–12)

If organic crawl budgets are constrained, use Google's Programmatic Indexing API to trigger indexing within 15–60 minutes.

- [ ] **Step 4.1: Google Cloud Service Account Setup**
  - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
  - Create a new project named `Keystone-Fast-Indexing`.
  - Enable the **Google Indexing API** for the project.
  - Create a Service Account, generate a **JSON Private Key**, and download it locally.
  - Copy the unique email address of the service account (`your-service-account@keystone-fast-indexing.iam.gserviceaccount.com`).

- [ ] **Step 4.2: Link Service Account to Google Search Console**
  - Open GSC, navigate to **Settings > Users and Permissions**.
  - Click **Add User**, paste the Service Account email address, and grant **Owner** permissions (required for indexing API verification).

- [ ] **Step 4.3: Execute Indexing Request Script**
  - Run the following quick Python utility from your workstation. It sends a direct publish request to Google's real-time [[wiki/index|index]].

```python
import json
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# Define scopes and endpoints
SCOPES = ['https://www.googleapis.com/auth/indexing']
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# Path to the downloaded GCP Service Account credentials JSON
credentials_file = "C:/Users/Curtis/.google_workspace_mcp/credentials/indexing_service_account.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, SCOPES)
http = credentials.authorize(httplib2.Http())

urls = [
    "https://www.keystonepossibilities.com/whistler-sauna/",
    "https://www.keystonepossibilities.com/west-vancouver-sauna/",
    "https://www.keystonepossibilities.com/north-vancouver-sauna/",
    "https://www.keystonepossibilities.com/squamish-sauna/",
    "https://www.keystonepossibilities.com/sunshine-coast-sauna/"
]

for url in urls:
    content = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response, content_bytes = http.request(
        ENDPOINT,
        method="POST",
        body=json.dumps(content),
        headers={"Content-Type": "application/json"}
    )
    print(f"URL: {url} -> Response Status: {response.status}")
    print(content_bytes.decode('utf-8'))
```

---

## Phase 5: Monitoring & Verification (Hours 12–24)

- [ ] **Step 5.1: Live Log Inspection**
  - Monitor the web server access logs for user agent `Googlebot`.
  - Look for requests fetching the newly added URLs:
    `"GET /whistler-sauna/ HTTP/1.1" 200 - "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"`
  - Confirm the crawl has successfully parsed the page and returned code `200`.

- [ ] **Step 5.2: Verification via GSC Coverage Report**
  - Within 24 hours, enter the URLs back into the URL Inspection tool.
  - The status should transition from *"URL is not on Google"* to **"URL is on Google"** (indicated by green checkmarks).
  - Verify that the **Enhanced Features / Rich Results** section shows green checkmarks for `LocalBusiness` and `Service` types, proving that the structured data has been successfully parsed and linked to the Enterprise Knowledge Graph.


---
📁 **See also:** [[02_Keystone_Possibilities/Local_SEO_Domination/INDEX|← Directory Index]]
