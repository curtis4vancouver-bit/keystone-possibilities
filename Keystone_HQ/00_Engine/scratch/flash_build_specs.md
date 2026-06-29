# Flash 3.5 Build Specs — 5 MCP Servers & Antigravity Skills

> **Created**: 2026-05-22  
> **Author**: Antigravity Architect Agent  
> **Purpose**: Copy-paste-ready specifications for building 5 new components  
> **Workspace Root**: `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain`

---

## Table of Contents

1. [Brave Research Validator (Antigravity Skill)](#1-brave-research-validator)
2. [Brain Health Audit (Antigravity Skill)](#2-brain-health-audit)
3. [Social Analytics MCP Server](#3-social-analytics-mcp-server)
4. [Shopify Manager MCP Server](#4-shopify-manager-mcp-server)
5. [Google Analytics 4 MCP Server](#5-google-analytics-4-mcp-server)
6. [MCP Multiplexer Registration (agents.json)](#6-mcp-multiplexer-registration)
7. [Testing Commands Summary](#7-testing-commands-summary)

---

## Global Conventions

### File Encoding
All Python files must use UTF-8. Do NOT add `sys.stdout = io.TextIOWrapper(...)` overrides — this causes Python 3.14 closed-file errors.

### FastMCP Server Boilerplate
Every MCP server MUST follow this exact pattern (taken from the working `youtube_mcp.py` and `content_engine_mcp.py`):

```python
import os
import sys
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server Name Here")

# ... tool definitions ...

if __name__ == "__main__":
    mcp.run()
```

### Antigravity Skill YAML Frontmatter
Every skill MUST start with this exact format:
```yaml
---
name: skill-name-kebab-case
description: "Single-line description in quotes. This appears in the skill list."
---
```

### MCP Multiplexer [[AGENTS|agents]].json Format
Every new agent entry follows this structure:
```json
"agent_name": {
    "command": "python",
    "args": ["../relative/path/to/server.py"],
    "enabled": true
}
```
Relative paths are from `MCP_Multiplexer/` directory.

### Existing Token Files (DO NOT RECREATE)
| File | Location | Contents |
|------|----------|----------|
| `youtube_token.json` | `{WORKSPACE_ROOT}/youtube_token.json` | Google OAuth2 token with `youtube.upload` and `youtube` scopes, client_id `911189793704-...`, client_secret `GOCSPX-...` |
| `youtube_token_oac.json` | `{WORKSPACE_ROOT}/youtube_token_oac.json` | OAC brand account token, same client_id/secret |
| `social_tokens.json` | `{WORKSPACE_ROOT}/social_tokens.json` | LinkedIn ([[possibilities|Possibilities]]), Meta/Facebook (Possibilities), TikTok (Recomposition) |

### Existing MCP Tool Schemas (Available at Runtime)

**keystone-brain MCP** (lazy-loaded, call via `call_mcp_tool`):
- `search_master_brain(query: string, limit?: number)` — Searches Supabase vector DB
- `list_brain_sources()` — Lists all unique document sources with chunk counts
- `ingest_to_brain(content: string, source: string)` — Saves knowledge to vector DB

**brave-search MCP** (lazy-loaded, call via `call_mcp_tool`):
- `brave_web_search(query: string, count?: number, offset?: number)` — Web search, max 20 results

---

## 1. Brave Research Validator

### File Location
```
C:\Users\Curtis\.gemini\config\skills\keystone_brave_validator\SKILL.md
```

### Purpose
After every Deep Research report is ingested into the brain, automatically extract 3–5 key factual claims from the report, run Brave searches on each claim, compare results, and flag any discrepancies. Appends a validation summary to the bottom of the report file.

### Directory to Create
```
C:\Users\Curtis\.gemini\config\skills\keystone_brave_validator\
└── SKILL.md
```

### Complete SKILL.md Content

```markdown
---
name: keystone-brave-research-validator
description: "After every Deep Research report is ingested, extract 3-5 key factual claims, run Brave searches on each, compare results, and flag discrepancies. Appends validation summary to the report."
---

# Brave Research Validator

This skill validates Deep Research reports by cross-referencing factual claims against live Brave Search results. Run this AFTER every Chrome Deep Research cycle or manual report ingestion.

## When to Activate

- After any file is saved to `Research_Archives/`
- After `ingest_to_brain` is called with a research report
- When the user says "validate research" or "fact-check the latest report"
- Automatically at the end of every Chrome Deep Research cycle (see `keystone-chrome-research-automation` skill)

## Validation Protocol

### Step 1: Identify the Latest Report

Read the `Research_Archives/` directory to find the most recently modified `.md` file:

```
Research Archives Location:
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\
```

Sort files by modification date (newest first). The target file is the most recent `.md` file.

If the user specifies a particular report, use that file instead.

### Step 2: Extract Key Claims

Read the full report content and identify 3–5 **verifiable factual claims**. Prioritize these categories (in order):

1. **API endpoints or URLs** — e.g., "The TikTok Business API endpoint is `https://business-api.tiktok.com/open_api/v1.3/`"
2. **Version numbers** — e.g., "GA4 Data API is currently at v1beta"
3. **Pricing information** — e.g., "Shopify Basic plan costs $39/month"
4. **Feature availability** — e.g., "YouTube Analytics API supports real-time reporting"
5. **Statistical claims** — e.g., "Deep house music category has grown 40% YoY"

For each claim, create a structured object:
```json
{
    "claim_id": 1,
    "claim_text": "The exact claim from the report",
    "category": "api_endpoint|version|pricing|feature|statistic",
    "search_query": "optimized Brave search query to verify this claim",
    "source_line": "approximate line or section reference in the report"
}
```

### Step 3: Run Brave Searches

For EACH extracted claim, call the Brave Search MCP tool:

```
Tool: brave_web_search (MCP server: brave-search)
Arguments:
  query: string — The search query derived from the claim (max 400 chars, 50 words)
  count: number — 5 (we only need top 5 results for validation)
```

Example calls:
```
# Claim: "Shopify Admin API uses version 2024-01"
brave_web_search(query="Shopify Admin API latest version 2026", count=5)

# Claim: "YouTube Analytics API requires oauth2 scope youtube.readonly"
brave_web_search(query="YouTube Analytics API required OAuth scopes", count=5)

# Claim: "TikTok Business API rate limit is 600 requests per minute"
brave_web_search(query="TikTok Business API rate limit requests per minute", count=5)
```

### Step 4: Compare and Classify

For each claim, compare the Brave results against the report's assertion:

| Status | Criteria |
|--------|----------|
| `[VERIFIED]` | At least 2 Brave results confirm the claim |
| `[UNVERIFIED]` | No Brave results confirm OR results contradict the claim |
| `[OUTDATED]` | Brave results show newer information than what the report states |
| `[INCONCLUSIVE]` | Brave results are ambiguous or unrelated |

### Step 5: Write Validation Summary

Append the following block to the **bottom** of the original report file:

```markdown

---

## 🔍 Brave Validation Summary

**Validated**: {TIMESTAMP}
**Report**: {FILENAME}
**Claims Checked**: {N}

| # | Claim | Status | Brave Evidence |
|---|-------|--------|----------------|
| 1 | {claim_text} | [VERIFIED] | {brief evidence from Brave} |
| 2 | {claim_text} | [UNVERIFIED] | {what Brave found instead} |
| 3 | {claim_text} | [VERIFIED] | {brief evidence from Brave} |
| 4 | {claim_text} | [OUTDATED] | {Brave shows version X, report says Y} |

**Overall Confidence**: {VERIFIED_COUNT}/{TOTAL_COUNT} claims verified ({percentage}%)

### Flagged Issues
- ⚠️ Claim 2: Report states "{claim}", but Brave results indicate "{correction}". Manual review recommended.
- ⚠️ Claim 4: Version number may be outdated. Current version per Brave: {current_version}.
```

### Step 6: Log to Brain (Optional)

If any claims are `[UNVERIFIED]` or `[OUTDATED]`, ingest a correction note into the brain:

```
Tool: ingest_to_brain (MCP server: keystone-brain)
Arguments:
  content: "CORRECTION: Report '{filename}' contained unverified claim: {claim}. Brave search on {date} found: {correction}."
  source: "brave_validation/{filename_without_extension}"
```

## Error Handling

- If `Research_Archives/` is empty, report: "No reports found in Research_Archives/. Nothing to validate."
- If Brave search fails (rate limit, network error), mark the claim as `[SEARCH_FAILED]` and note the error.
- If a report has no verifiable factual claims (e.g., it's purely strategic/opinion), report: "No verifiable factual claims found. Validation skipped."
- Never modify the report content above the validation summary section. Only append.

## Example Full Run

1. Agent finds latest file: `Research_Archives/20260522_shopify_audiobook_marketing_shopify_seo_and_high-intent_organic_traffic_acquisition_stra.md`
2. Extracts 4 claims:
   - "Shopify Plus costs $2,000/month minimum" → `brave_web_search("Shopify Plus pricing 2026", count=5)`
   - "Google Shopping integration requires Merchant Center" → `brave_web_search("Shopify Google Shopping Merchant Center requirement", count=5)`
   - "Shopify SEO supports canonical URLs natively" → `brave_web_search("Shopify canonical URL SEO native support", count=5)`
   - "Shopify conversion rate average is 1.4%" → `brave_web_search("Shopify average conversion rate 2026", count=5)`
3. Compares results, writes summary
4. Appends validation block to the report file
```

---

## 2. Brain Health Audit

### File Location
```
C:\Users\Curtis\.gemini\config\skills\keystone_brain_health_audit\SKILL.md
```

### Purpose
Run comprehensive health checks on the [[master|Master]] Brain vector database (Supabase). Count chunks, flag broken sources, detect duplicates, test semantic search quality, and generate a scored health report.

### Directory to Create
```
C:\Users\Curtis\.gemini\config\skills\keystone_brain_health_audit\
└── SKILL.md
```

### Complete SKILL.md Content

```markdown
---
name: keystone-brain-health-audit
description: "Run health checks on the Master Brain vector database. Counts chunks, flags broken sources, detects duplicates, tests semantic queries, generates a health score (0-100), and saves report to .learnings/insights/."
---

# Brain Health Audit

This skill performs a comprehensive health assessment of the Keystone Master Brain vector database. Run it periodically (daily or weekly) to ensure the brain is in good shape.

## When to Activate

- When the user asks "how's the brain?" or "brain health check"
- At the start of the daily digest generation (part of self-evolution pipeline)
- After any bulk ingestion session
- When semantic search returns poor results

## Audit Protocol

### Step 1: Get Source Inventory

Call the `list_brain_sources` tool to get all sources and their chunk counts:

```
Tool: list_brain_sources (MCP server: keystone-brain)
Arguments: {} (no arguments required)
```

The response returns a JSON array like:
```json
[
    {"source": "deep_research/competitor_analysis_2026", "chunk_count": 12},
    {"source": "agent_session/2026-05-21", "chunk_count": 5},
    ...
]
```

Parse this response and compute:
- `total_sources`: Count of unique sources
- `total_chunks`: Sum of all chunk_count values
- `avg_chunks_per_source`: total_chunks / total_sources

### Step 2: Flag Broken Sources

Iterate through all sources. Flag any source where `chunk_count < 3` as potentially broken:

```json
{
    "broken_sources": [
        {"source": "some_source_name", "chunk_count": 1, "reason": "Only 1 chunk — may be a failed or truncated ingestion"}
    ]
}
```

A healthy source should have at least 3 chunks (one ingestion of ~1000+ chars produces multiple chunks). Sources with 1-2 chunks may indicate:
- Truncated ingestion
- Very short content that may not be useful
- Failed mid-ingestion

### Step 3: Detect Duplicate Source Names

Look for source names that are suspiciously similar:
- Exact duplicates (should not happen, but check)
- Near-duplicates: sources that differ only by a trailing number, date, or minor variation

Example detection logic:
```
"deep_research/shopify_seo" and "deep_research/shopify_seo_2" → Flag as potential duplicate
"agent_session/2026-05-21" and "agent_session/2026-05-21_v2" → Flag as potential duplicate
```

Build a list:
```json
{
    "potential_duplicates": [
        {"sources": ["source_a", "source_b"], "similarity": "high"}
    ]
}
```

### Step 4: Run Test Semantic Queries

Execute 5 predetermined test queries to verify the brain returns relevant results:

```
Tool: search_master_brain (MCP server: keystone-brain)
Arguments:
  query: string — the test query
  limit: 3
```

**Test queries** (these cover the major knowledge domains):

| # | Query | Expected Domain | Pass Criteria |
|---|-------|-----------------|---------------|
| 1 | `"Keystone Possibilities luxury construction Vancouver"` | Brand/construction | At least 1 result mentions construction, building, or Vancouver |
| 2 | `"GLP-1 peptide protocol BPC-157"` | Health/protocols | At least 1 result mentions peptides, GLP-1, or health |
| 3 | `"YouTube channel optimization SEO tags"` | YouTube/content | At least 1 result mentions YouTube, SEO, or content |
| 4 | `"self evolution error correction journal"` | System/architecture | At least 1 result mentions self-evolution, errors, or corrections |
| 5 | `"Shopify audiobook digital products"` | Business/commerce | At least 1 result mentions Shopify, audiobook, or products |

For each query, evaluate:
- **PASS**: At least 1 of 3 results is relevant to the expected domain
- **FAIL**: No results returned, or all results are irrelevant
- **DEGRADED**: Results returned but relevance is weak (tangentially related)

### Step 5: Calculate Health Score

Compute a score from 0–100 using this formula:

```
Base Score: 100

Deductions:
- Each broken source (< 3 chunks): -3 points
- Each duplicate source pair: -5 points
- Each FAILED test query: -10 points
- Each DEGRADED test query: -5 points
- If total_chunks < 100: -10 points (brain is too small)
- If total_chunks > 10000: -5 points (brain may need pruning)
- If avg_chunks_per_source < 3: -5 points (sources too shallow)
- If avg_chunks_per_source > 50: -5 points (sources too granular)

Minimum score: 0
Maximum score: 100
```

### Step 6: Generate Health Report

Save the report as JSON to:
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\insights\brain_health_report.json
```

Report schema:
```json
{
    "timestamp": "2026-05-22T08:47:00-07:00",
    "health_score": 85,
    "grade": "B+",
    "summary": {
        "total_sources": 110,
        "total_chunks": 450,
        "avg_chunks_per_source": 4.1
    },
    "broken_sources": [
        {"source": "name", "chunk_count": 1, "reason": "description"}
    ],
    "potential_duplicates": [
        {"sources": ["a", "b"], "similarity": "high"}
    ],
    "semantic_test_results": [
        {
            "query": "...",
            "expected_domain": "...",
            "status": "PASS|FAIL|DEGRADED",
            "top_result_source": "...",
            "top_result_preview": "first 100 chars..."
        }
    ],
    "recommendations": [
        "Re-ingest broken source 'xyz' — only has 1 chunk",
        "Consider merging duplicate sources 'a' and 'b'",
        "Test query 3 failed — YouTube content may not be ingested yet"
    ]
}
```

### Grade Scale
| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent — brain is healthy and comprehensive |
| 80-89 | B | Good — minor issues to address |
| 70-79 | C | Fair — some sources broken or search quality degraded |
| 60-69 | D | Poor — significant issues, immediate attention needed |
| 0-59 | F | Critical — brain may be corrupted or severely incomplete |

### Step 7: Output Summary

After saving the report, output a human-readable summary:

```
🧠 Brain Health Audit Complete
━━━━━━━━━━━━━━━━━━━━━━━━━
Health Score: 85/100 (B+)
Total Sources: 110 | Total Chunks: 450
Avg Chunks/Source: 4.1

⚠️ Issues Found:
  - 3 broken sources (< 3 chunks)
  - 1 potential duplicate pair
  - 1 semantic test degraded

📋 Report saved to: .learnings/insights/brain_health_report.json
```

## Error Handling

- If `list_brain_sources` fails or returns empty, set health_score to 0 with grade "F" and recommendation "Brain may be offline or empty."
- If `search_master_brain` times out on a query, mark that test as `FAIL` and note the error.
- If the `.learnings/insights/` directory doesn't exist, create it.
- Always overwrite the previous `brain_health_report.json` (it's a snapshot, not a log).
```

---

## 3. Social Analytics MCP Server

### File Location
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\social_analytics_mcp.py
```

### Purpose
Unified analytics dashboard pulling from YouTube Analytics API, Meta Graph API page insights, and TikTok Business API. Provides per-platform and cross-platform metrics.

### Dependencies to Install
```bash
pip install mcp google-auth google-auth-oauthlib google-api-python-client requests
```

### Token File Locations (Already Exist)
| Token | Path | Structure |
|-------|------|-----------|
| YouTube | `youtube_token.json` | `{"token": "...", "refresh_token": "...", "token_uri": "...", "client_id": "911189793704-...", "client_secret": "GOCSPX-...", "scopes": ["...youtube..."]}` |
| YouTube OAC | `youtube_token_oac.json` | Same structure as above, for brand account |
| Meta/Facebook | `social_tokens.json` → `possibilities.meta` | `{"app_id": "1495585472113538", "app_secret": "e5a3e39595196161314b30a5e4e45ff6", "user_access_token": "EAA..."}` |
| TikTok | `social_tokens.json` → `recomposition.tiktok` | `{"client_key": "sbawve91fhxu7wf6sw", "client_secret": "X6pdMZRF4ICEuKY6IxH15DHdS5cZOixB", "access_token": "act.OvX...", "refresh_token": "rft.1UR..."}` |

### Complete File Content

```python
"""
Keystone Social Analytics MCP v1.0
Unified analytics dashboard: YouTube Analytics API, Meta Graph API, TikTok Business API.
Pulls metrics across all Keystone brands from a single interface.
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

mcp = FastMCP("Social Analytics")

# ── Token Loading ─────────────────────────────────────────────────

SOCIAL_TOKENS_PATH = os.path.join(SCRIPT_DIR, "social_tokens.json")
YT_TOKEN_PATH = os.path.join(SCRIPT_DIR, "youtube_token.json")
YT_OAC_TOKEN_PATH = os.path.join(SCRIPT_DIR, "youtube_token_oac.json")

CHANNELS = {
    "possibilities": {"id": "UCu8gdU_R8XE2RvcttGa3drg", "token": "primary"},
    "protocols":     {"id": "UCxURlqMNhAtxUTpdXmlOYaw", "token": "primary"},
    "oac":           {"id": "UCMn1f9DTF_iybKmv5WlTm9Q", "token": "oac"},
}


def _load_social_tokens():
    """Load social_tokens.json and return parsed dict."""
    if not os.path.exists(SOCIAL_TOKENS_PATH):
        return {}
    with open(SOCIAL_TOKENS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_yt_analytics(channel_key: str):
    """Build a YouTube Analytics API client for the given channel."""
    ch = CHANNELS.get(channel_key)
    if not ch:
        return None, f"Unknown channel: {channel_key}"
    token_path = YT_OAC_TOKEN_PATH if ch["token"] == "oac" else YT_TOKEN_PATH
    if not os.path.exists(token_path):
        return None, f"Token file not found: {token_path}"
    creds = Credentials.from_authorized_user_file(token_path)
    # YouTube Analytics API requires the youtubeAnalytics.readonly scope.
    # If not present, we'll attempt anyway — the token may have been issued with it.
    service = build("youtubeAnalytics", "v2", credentials=creds)
    return service, None


# ── Tool 1: YouTube Analytics ─────────────────────────────────────

@mcp.tool()
def get_youtube_analytics(channel: str, metric: str = "views", start_date: str = None, end_date: str = None) -> str:
    """
    Fetches YouTube Analytics data for a Keystone channel.

    Args:
        channel: 'possibilities', 'protocols', or 'oac'
        metric: Comma-separated metrics. Options: views, estimatedMinutesWatched,
                averageViewDuration, likes, dislikes, comments, shares,
                subscribersGained, subscribersLost, annotationClickThroughRate.
                Default: 'views'
        start_date: Start date in YYYY-MM-DD format. Default: 30 days ago.
        end_date: End date in YYYY-MM-DD format. Default: today.

    Returns:
        JSON string with analytics data including column headers and rows.

    API Reference: https://developers.google.com/youtube/analytics/reference/reports/query
    """
    try:
        service, error = _get_yt_analytics(channel)
        if error:
            return json.dumps({"error": error})

        ch = CHANNELS[channel]
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        response = service.reports().query(
            ids=f"channel=={ch['id']}",
            startDate=start_date,
            endDate=end_date,
            metrics=metric,
            dimensions="day",
            sort="day"
        ).execute()

        return json.dumps({
            "channel": channel,
            "channel_id": ch["id"],
            "metric": metric,
            "start_date": start_date,
            "end_date": end_date,
            "column_headers": [h["name"] for h in response.get("columnHeaders", [])],
            "rows": response.get("rows", []),
            "total_rows": len(response.get("rows", []))
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "hint": "Ensure youtube_token.json has youtubeAnalytics.readonly scope. Re-run OAuth with added scope if needed."})


# ── Tool 2: Meta/Facebook Insights ────────────────────────────────

@mcp.tool()
def get_meta_insights(brand: str = "possibilities", metric: str = "page_impressions", period: str = "day") -> str:
    """
    Fetches Meta (Facebook/Instagram) Page Insights for a Keystone brand.

    Args:
        brand: 'possibilities' (only brand with Meta tokens currently).
        metric: Comma-separated metrics. Options: page_impressions, page_engaged_users,
                page_post_engagements, page_fan_adds, page_views_total,
                page_video_views, page_fans. Default: 'page_impressions'
        period: 'day', 'week', 'days_28', or 'lifetime'. Default: 'day'

    Returns:
        JSON string with insights data.

    API Reference: https://developers.facebook.com/docs/graph-api/reference/page/insights/
    """
    try:
        tokens = _load_social_tokens()
        meta_config = tokens.get(brand, {}).get("meta")
        if not meta_config:
            return json.dumps({"error": f"No Meta tokens found for brand '{brand}'. Check social_tokens.json."})

        access_token = meta_config["user_access_token"]

        # Step 1: Get the Page ID (user's managed pages)
        pages_url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={access_token}"
        pages_resp = requests.get(pages_url, timeout=15)
        pages_data = pages_resp.json()

        if "error" in pages_data:
            return json.dumps({"error": f"Graph API error: {pages_data['error'].get('message', 'Unknown')}"})

        if not pages_data.get("data"):
            return json.dumps({"error": "No pages found. User may need to grant page permissions."})

        # Use first page (or iterate if multiple)
        page = pages_data["data"][0]
        page_id = page["id"]
        page_token = page["access_token"]
        page_name = page.get("name", "Unknown")

        # Step 2: Fetch insights
        metrics_list = metric.replace(" ", "")
        insights_url = (
            f"https://graph.facebook.com/v21.0/{page_id}/insights"
            f"?metric={metrics_list}&period={period}&access_token={page_token}"
        )
        insights_resp = requests.get(insights_url, timeout=15)
        insights_data = insights_resp.json()

        if "error" in insights_data:
            return json.dumps({"error": f"Insights API error: {insights_data['error'].get('message', 'Unknown')}"})

        results = []
        for item in insights_data.get("data", []):
            results.append({
                "name": item.get("name"),
                "period": item.get("period"),
                "title": item.get("title"),
                "description": item.get("description"),
                "values": item.get("values", [])[-7:]  # Last 7 data points
            })

        return json.dumps({
            "brand": brand,
            "page_name": page_name,
            "page_id": page_id,
            "metrics": results
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 3: TikTok Analytics ─────────────────────────────────────

@mcp.tool()
def get_tiktok_analytics(metric: str = "video_views", days: int = 7) -> str:
    """
    Fetches TikTok Business Account analytics for Keystone Recomposition.

    Args:
        metric: Metric to fetch. Options: video_views, likes, comments, shares,
                profile_views, followers_count. Default: 'video_views'
        days: Number of past days to query (1-365). Default: 7.

    Returns:
        JSON string with TikTok analytics data.

    API Reference: https://business-api.tiktok.com/portal/docs?id=1738864915188737
    Note: TikTok Business API requires approved app. Uses Content Posting API tokens.
    """
    try:
        tokens = _load_social_tokens()
        tiktok_config = tokens.get("recomposition", {}).get("tiktok")
        if not tiktok_config:
            return json.dumps({"error": "No TikTok tokens found in social_tokens.json under recomposition.tiktok"})

        access_token = tiktok_config["access_token"]
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # TikTok Business API — Creator Insights endpoint
        # Note: This requires the user.insights scope. If using Content Posting API
        # tokens only, this may need upgrading. The endpoint attempts the call and
        # returns a clear error if scopes are insufficient.
        url = "https://business-api.tiktok.com/open_api/v1.3/business/get/"
        headers = {
            "Access-Token": access_token,
            "Content-Type": "application/json"
        }
        params = {
            "business_id": tiktok_config.get("business_id", ""),
            "fields": json.dumps([metric]),
            "start_date": start_date,
            "end_date": end_date
        }

        resp = requests.get(url, headers=headers, params=params, timeout=15)
        data = resp.json()

        if data.get("code") != 0:
            # Fallback: try the creator stats endpoint
            creator_url = "https://open.tiktokapis.com/v2/research/user/info/"
            creator_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            creator_resp = requests.post(creator_url, headers=creator_headers, json={}, timeout=15)
            creator_data = creator_resp.json()

            return json.dumps({
                "metric": metric,
                "days": days,
                "start_date": start_date,
                "end_date": end_date,
                "note": "TikTok Business API returned non-zero code. Attempted fallback.",
                "primary_response": data,
                "fallback_response": creator_data,
                "hint": "TikTok analytics may require Business Center access or upgraded app permissions. "
                        "Check: https://business-api.tiktok.com/portal/docs?id=1738864915188737"
            }, indent=2, ensure_ascii=False)

        return json.dumps({
            "metric": metric,
            "days": days,
            "start_date": start_date,
            "end_date": end_date,
            "data": data.get("data", {})
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 4: Cross-Platform Summary ───────────────────────────────

@mcp.tool()
def get_cross_platform_summary(brand: str = "all", days: int = 30) -> str:
    """
    Aggregates analytics from YouTube, Meta, and TikTok into a unified summary.

    Args:
        brand: 'possibilities', 'protocols', 'oac', or 'all'. Default: 'all'.
        days: Number of past days to aggregate. Default: 30.

    Returns:
        JSON string with per-platform metrics and combined totals.
    """
    try:
        summary = {
            "period_days": days,
            "brand_filter": brand,
            "timestamp": datetime.now().isoformat(),
            "platforms": {},
            "combined": {}
        }
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        total_views = 0
        total_engagement = 0

        # YouTube — pull for relevant channels
        channels_to_query = list(CHANNELS.keys()) if brand == "all" else [brand] if brand in CHANNELS else []
        yt_total_views = 0
        yt_total_watch = 0

        for ch_key in channels_to_query:
            try:
                service, error = _get_yt_analytics(ch_key)
                if error:
                    summary["platforms"][f"youtube_{ch_key}"] = {"error": error}
                    continue
                ch = CHANNELS[ch_key]
                response = service.reports().query(
                    ids=f"channel=={ch['id']}",
                    startDate=start_date,
                    endDate=end_date,
                    metrics="views,estimatedMinutesWatched,likes,subscribersGained"
                ).execute()
                rows = response.get("rows", [])
                if rows:
                    row = rows[0]  # Aggregated single row when no dimensions
                    views = row[0] if len(row) > 0 else 0
                    watch_mins = row[1] if len(row) > 1 else 0
                    likes = row[2] if len(row) > 2 else 0
                    subs = row[3] if len(row) > 3 else 0
                    yt_total_views += views
                    yt_total_watch += watch_mins
                    total_views += views
                    total_engagement += likes
                    summary["platforms"][f"youtube_{ch_key}"] = {
                        "views": views,
                        "watch_minutes": watch_mins,
                        "likes": likes,
                        "subscribers_gained": subs
                    }
            except Exception as e:
                summary["platforms"][f"youtube_{ch_key}"] = {"error": str(e)}

        # Meta — only available for Possibilities
        if brand in ("all", "possibilities"):
            try:
                tokens = _load_social_tokens()
                meta_config = tokens.get("possibilities", {}).get("meta")
                if meta_config:
                    access_token = meta_config["user_access_token"]
                    pages_resp = requests.get(
                        f"https://graph.facebook.com/v21.0/me/accounts?access_token={access_token}",
                        timeout=15
                    )
                    pages = pages_resp.json().get("data", [])
                    if pages:
                        page = pages[0]
                        insights_resp = requests.get(
                            f"https://graph.facebook.com/v21.0/{page['id']}/insights"
                            f"?metric=page_impressions,page_post_engagements"
                            f"&period=days_28&access_token={page['access_token']}",
                            timeout=15
                        )
                        insights = insights_resp.json()
                        meta_data = {}
                        for item in insights.get("data", []):
                            values = item.get("values", [])
                            if values:
                                meta_data[item["name"]] = values[-1].get("value", 0)
                        impressions = meta_data.get("page_impressions", 0)
                        engagements = meta_data.get("page_post_engagements", 0)
                        total_views += impressions
                        total_engagement += engagements
                        summary["platforms"]["meta_possibilities"] = {
                            "impressions": impressions,
                            "engagements": engagements,
                            "period": "days_28"
                        }
            except Exception as e:
                summary["platforms"]["meta_possibilities"] = {"error": str(e)}

        # TikTok — only available for Recomposition (OAC)
        if brand in ("all", "oac"):
            try:
                tokens = _load_social_tokens()
                tiktok_config = tokens.get("recomposition", {}).get("tiktok")
                if tiktok_config:
                    summary["platforms"]["tiktok_recomposition"] = {
                        "note": "TikTok analytics requires Business API access. Call get_tiktok_analytics() for details.",
                        "token_status": "present" if tiktok_config.get("access_token") else "missing"
                    }
            except Exception as e:
                summary["platforms"]["tiktok_recomposition"] = {"error": str(e)}

        summary["combined"] = {
            "total_views_impressions": total_views,
            "total_engagements": total_engagement,
            "youtube_total_views": yt_total_views,
            "youtube_total_watch_minutes": yt_total_watch,
            "platforms_reporting": len([p for p in summary["platforms"].values() if "error" not in p])
        }

        return json.dumps(summary, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()
```

### Tool Schemas Summary

| Tool | Parameters | Types | Required |
|------|-----------|-------|----------|
| `get_youtube_analytics` | `channel`, `metric`, `start_date`, `end_date` | `str`, `str`, `str`, `str` | `channel` |
| `get_meta_insights` | `brand`, `metric`, `period` | `str`, `str`, `str` | none (all default) |
| `get_tiktok_analytics` | `metric`, `days` | `str`, `int` | none (all default) |
| `get_cross_platform_summary` | `brand`, `days` | `str`, `int` | none (all default) |

### API References
- **YouTube Analytics API v2**: https://developers.google.com/youtube/analytics/reference/reports/query
- **Meta Graph API Page Insights**: https://developers.facebook.com/docs/graph-api/reference/page/insights/
- **TikTok Business API**: https://business-api.tiktok.com/portal/docs?id=1738864915188737

### OAuth Scope Requirements
- YouTube: Needs `https://www.googleapis.com/auth/yt-analytics.readonly` added to existing scopes
- Meta: Uses existing `user_access_token` from `social_tokens.json` (already has `pages_read_engagement`)
- TikTok: Uses existing `access_token` from `social_tokens.json` (may need `user.insights` scope)

### Error Handling Pattern
Every tool wraps its logic in `try/except` and returns `{"error": "message"}` JSON on failure. Specific hints are included for common auth issues (missing scopes, expired tokens).

---

## 4. Shopify Manager MCP Server

### File Location
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\shopify_mcp.py
```

### Purpose
Manage Shopify store for audiobook/digital products via Shopify Admin REST API. List products, get orders, view analytics, update products, and create discount codes.

### Dependencies to Install
```bash
pip install mcp requests
```

### Environment Variables Needed
```
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxx
```

### Config File to Create
Also create a placeholder config at:
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\shopify_config.json
```

```json
{
    "store_url": "YOUR_STORE.myshopify.com",
    "access_token": "shpat_PLACEHOLDER_REPLACE_WITH_REAL_TOKEN",
    "api_version": "2025-01",
    "notes": "Get access token from Shopify Admin > Settings > Apps > Develop apps > Create app > Configure Admin API scopes > Install app. Required scopes: read_products, write_products, read_orders, read_analytics, write_discounts, read_discounts."
}
```

### Complete File Content

```python
"""
Keystone Shopify Manager MCP v1.0
Manage audiobook/digital product store via Shopify Admin REST API.
Products, orders, analytics, discounts.
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Shopify Manager")

# ── Configuration ─────────────────────────────────────────────────

CONFIG_PATH = os.path.join(SCRIPT_DIR, "shopify_config.json")


def _load_config():
    """Load Shopify config from file or environment variables."""
    config = {}
    # Try config file first
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    # Environment variables override file config
    store_url = os.environ.get("SHOPIFY_STORE_URL", config.get("store_url", ""))
    access_token = os.environ.get("SHOPIFY_ACCESS_TOKEN", config.get("access_token", ""))
    api_version = config.get("api_version", "2025-01")
    return store_url, access_token, api_version


def _shopify_request(method, endpoint, data=None, params=None):
    """Make an authenticated request to the Shopify Admin API."""
    store_url, access_token, api_version = _load_config()
    if not store_url or not access_token or "PLACEHOLDER" in access_token:
        return {"error": "Shopify not configured. Set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN env vars, or update shopify_config.json."}

    url = f"https://{store_url}/admin/api/{api_version}/{endpoint}"
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=15)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=data, timeout=15)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}

        if resp.status_code == 401:
            return {"error": "Shopify authentication failed. Check access token."}
        if resp.status_code == 404:
            return {"error": f"Endpoint not found: {endpoint}. Check API version and resource."}
        if resp.status_code >= 400:
            return {"error": f"Shopify API error {resp.status_code}: {resp.text[:500]}"}

        return resp.json()
    except requests.exceptions.Timeout:
        return {"error": "Shopify API request timed out."}
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to {store_url}. Check store URL."}
    except Exception as e:
        return {"error": str(e)}


# ── Tool 1: List Products ────────────────────────────────────────

@mcp.tool()
def list_products() -> str:
    """
    Lists all products in the Shopify store with prices, inventory, and status.

    Returns:
        JSON string with product list including id, title, product_type, status,
        variants (with prices and inventory), and tags.

    API Reference: https://shopify.dev/docs/api/admin-rest/2025-01/resources/product
    """
    try:
        result = _shopify_request("GET", "products.json", params={"limit": 250})
        if "error" in result:
            return json.dumps(result)

        products = []
        for p in result.get("products", []):
            variants = []
            for v in p.get("variants", []):
                variants.append({
                    "variant_id": v["id"],
                    "title": v.get("title", "Default"),
                    "price": v.get("price", "0.00"),
                    "compare_at_price": v.get("compare_at_price"),
                    "inventory_quantity": v.get("inventory_quantity", 0),
                    "sku": v.get("sku", ""),
                    "requires_shipping": v.get("requires_shipping", False)
                })
            products.append({
                "product_id": p["id"],
                "title": p["title"],
                "product_type": p.get("product_type", ""),
                "status": p.get("status", "unknown"),
                "tags": p.get("tags", ""),
                "created_at": p.get("created_at", "")[:10],
                "updated_at": p.get("updated_at", "")[:10],
                "variants": variants,
                "images_count": len(p.get("images", []))
            })

        return json.dumps({
            "total_products": len(products),
            "products": products
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 2: Get Orders ──────────────────────────────────────────

@mcp.tool()
def get_orders(status: str = "any", days: int = 30) -> str:
    """
    Fetches recent orders from the Shopify store.

    Args:
        status: Order status filter. Options: 'open', 'closed', 'cancelled', 'any'.
                Default: 'any'
        days: Number of past days to query. Default: 30.

    Returns:
        JSON string with order list including id, order_number, total_price,
        financial_status, fulfillment_status, customer info, and line items.

    API Reference: https://shopify.dev/docs/api/admin-rest/2025-01/resources/order
    """
    try:
        created_at_min = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00-07:00")
        params = {
            "status": status,
            "created_at_min": created_at_min,
            "limit": 250,
            "order": "created_at DESC"
        }
        result = _shopify_request("GET", "orders.json", params=params)
        if "error" in result:
            return json.dumps(result)

        orders = []
        total_revenue = 0.0
        for o in result.get("orders", []):
            line_items = []
            for li in o.get("line_items", []):
                line_items.append({
                    "title": li.get("title", ""),
                    "quantity": li.get("quantity", 0),
                    "price": li.get("price", "0.00")
                })
            order_total = float(o.get("total_price", "0.00"))
            total_revenue += order_total
            orders.append({
                "order_id": o["id"],
                "order_number": o.get("order_number"),
                "created_at": o.get("created_at", "")[:10],
                "total_price": o.get("total_price", "0.00"),
                "currency": o.get("currency", "CAD"),
                "financial_status": o.get("financial_status", "unknown"),
                "fulfillment_status": o.get("fulfillment_status", "unfulfilled"),
                "customer_name": f"{o.get('customer', {}).get('first_name', '')} {o.get('customer', {}).get('last_name', '')}".strip() or "Guest",
                "customer_email": o.get("customer", {}).get("email", ""),
                "line_items": line_items
            })

        return json.dumps({
            "status_filter": status,
            "days": days,
            "total_orders": len(orders),
            "total_revenue": f"{total_revenue:.2f}",
            "orders": orders
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 3: Get Analytics ───────────────────────────────────────

@mcp.tool()
def get_analytics(days: int = 30) -> str:
    """
    Calculates sales analytics: total revenue, order count, average order value,
    and estimated conversion rate from the Shopify store.

    Args:
        days: Number of past days to analyze. Default: 30.

    Returns:
        JSON string with revenue, order count, average order value, top products
        by revenue, and daily revenue breakdown.

    Note: Shopify Admin REST API does not have a dedicated analytics endpoint.
    This tool computes analytics from order data.
    """
    try:
        created_at_min = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00-07:00")
        params = {
            "status": "any",
            "created_at_min": created_at_min,
            "limit": 250,
            "order": "created_at ASC"
        }
        result = _shopify_request("GET", "orders.json", params=params)
        if "error" in result:
            return json.dumps(result)

        orders = result.get("orders", [])
        total_revenue = 0.0
        product_revenue = {}
        daily_revenue = {}
        paid_orders = 0

        for o in orders:
            total_price = float(o.get("total_price", "0.00"))
            order_date = o.get("created_at", "")[:10]
            financial = o.get("financial_status", "")

            if financial in ("paid", "partially_refunded"):
                total_revenue += total_price
                paid_orders += 1
                daily_revenue[order_date] = daily_revenue.get(order_date, 0) + total_price

                for li in o.get("line_items", []):
                    title = li.get("title", "Unknown")
                    rev = float(li.get("price", "0")) * li.get("quantity", 1)
                    product_revenue[title] = product_revenue.get(title, 0) + rev

        top_products = sorted(product_revenue.items(), key=lambda x: -x[1])[:10]
        avg_order = total_revenue / max(paid_orders, 1)

        return json.dumps({
            "days": days,
            "total_revenue": f"{total_revenue:.2f}",
            "total_orders": len(orders),
            "paid_orders": paid_orders,
            "cancelled_orders": len([o for o in orders if o.get("cancelled_at")]),
            "average_order_value": f"{avg_order:.2f}",
            "top_products_by_revenue": [{"title": t, "revenue": f"{r:.2f}"} for t, r in top_products],
            "daily_revenue": {k: f"{v:.2f}" for k, v in sorted(daily_revenue.items())},
            "currency": "CAD"
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 4: Update Product ──────────────────────────────────────

@mcp.tool()
def update_product(product_id: int, title: str = None, description: str = None, price: str = None) -> str:
    """
    Updates an existing product's metadata in the Shopify store.

    Args:
        product_id: The Shopify product ID (numeric). Get from list_products().
        title: New product title. Optional — only updates if provided.
        description: New product description (HTML allowed). Optional.
        price: New price for the first variant (e.g., "29.99"). Optional.

    Returns:
        JSON string confirming the update with the updated product data.

    API Reference: https://shopify.dev/docs/api/admin-rest/2025-01/resources/product#put-products-product-id
    """
    try:
        product_data = {}
        if title:
            product_data["title"] = title
        if description:
            product_data["body_html"] = description

        if not product_data and not price:
            return json.dumps({"error": "No fields to update. Provide at least one of: title, description, price."})

        # Update product metadata
        if product_data:
            product_data["id"] = product_id
            result = _shopify_request("PUT", f"products/{product_id}.json", data={"product": product_data})
            if "error" in result:
                return json.dumps(result)

        # Update price on first variant
        if price:
            # First, get the product to find variant ID
            prod_result = _shopify_request("GET", f"products/{product_id}.json")
            if "error" in prod_result:
                return json.dumps(prod_result)
            variants = prod_result.get("product", {}).get("variants", [])
            if variants:
                variant_id = variants[0]["id"]
                variant_result = _shopify_request(
                    "PUT",
                    f"variants/{variant_id}.json",
                    data={"variant": {"id": variant_id, "price": price}}
                )
                if "error" in variant_result:
                    return json.dumps(variant_result)

        return json.dumps({
            "success": True,
            "product_id": product_id,
            "updated_fields": {
                "title": title,
                "description": "updated" if description else None,
                "price": price
            }
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 5: Create Discount ─────────────────────────────────────

@mcp.tool()
def create_discount(code: str, percentage: int, expiry_days: int = 30) -> str:
    """
    Creates a percentage-based discount code in the Shopify store.

    Args:
        code: The discount code string (e.g., "LAUNCH20", "WELCOME10").
        percentage: Discount percentage (1-100). e.g., 20 for 20% off.
        expiry_days: Number of days until the code expires. Default: 30.

    Returns:
        JSON string confirming discount creation with the code and details.

    API Reference: https://shopify.dev/docs/api/admin-rest/2025-01/resources/price-rule
    """
    try:
        if not code or not code.strip():
            return json.dumps({"error": "Discount code cannot be empty."})
        if percentage < 1 or percentage > 100:
            return json.dumps({"error": f"Percentage must be 1-100, got {percentage}."})

        starts_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-07:00")
        ends_at = (datetime.now() + timedelta(days=expiry_days)).strftime("%Y-%m-%dT23:59:59-07:00")

        # Step 1: Create Price Rule
        price_rule_data = {
            "price_rule": {
                "title": code.upper(),
                "target_type": "line_item",
                "target_selection": "all",
                "allocation_method": "across",
                "value_type": "percentage",
                "value": f"-{percentage}.0",
                "customer_selection": "all",
                "starts_at": starts_at,
                "ends_at": ends_at,
                "usage_limit": None,
                "once_per_customer": True
            }
        }
        pr_result = _shopify_request("POST", "price_rules.json", data=price_rule_data)
        if "error" in pr_result:
            return json.dumps(pr_result)

        price_rule_id = pr_result.get("price_rule", {}).get("id")
        if not price_rule_id:
            return json.dumps({"error": "Failed to create price rule", "response": pr_result})

        # Step 2: Create Discount Code linked to Price Rule
        discount_data = {
            "discount_code": {
                "code": code.upper()
            }
        }
        dc_result = _shopify_request("POST", f"price_rules/{price_rule_id}/discount_codes.json", data=discount_data)
        if "error" in dc_result:
            return json.dumps(dc_result)

        return json.dumps({
            "success": True,
            "discount_code": code.upper(),
            "percentage_off": percentage,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "expiry_days": expiry_days,
            "once_per_customer": True,
            "price_rule_id": price_rule_id,
            "discount_code_id": dc_result.get("discount_code", {}).get("id")
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()
```

### Tool Schemas Summary

| Tool | Parameters | Types | Required |
|------|-----------|-------|----------|
| `list_products` | *(none)* | — | — |
| `get_orders` | `status`, `days` | `str`, `int` | none |
| `get_analytics` | `days` | `int` | none |
| `update_product` | `product_id`, `title`, `description`, `price` | `int`, `str`, `str`, `str` | `product_id` |
| `create_discount` | `code`, `percentage`, `expiry_days` | `str`, `int`, `int` | `code`, `percentage` |

### API Reference
- **Shopify Admin REST API**: https://shopify.dev/docs/api/admin-rest/2025-01
- **Products**: https://shopify.dev/docs/api/admin-rest/2025-01/resources/product
- **Orders**: https://shopify.dev/docs/api/admin-rest/2025-01/resources/order
- **Price Rules**: https://shopify.dev/docs/api/admin-rest/2025-01/resources/price-rule
- **Discount Codes**: https://shopify.dev/docs/api/admin-rest/2025-01/resources/discount-code

### Required Shopify Scopes
When creating the Shopify custom app:
- `read_products`, `write_products`
- `read_orders`
- `read_discounts`, `write_discounts`
- `read_analytics` (if available)

---

## 5. Google Analytics 4 MCP Server

### File Location
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\ga4_mcp.py
```

### Purpose
Query Google Analytics 4 properties for website traffic data: page views, traffic sources, top pages, and conversion funnels. Reuses existing Google OAuth credentials from `youtube_token.json` with an additional scope.

### Dependencies to Install
```bash
pip install mcp google-analytics-data google-auth google-auth-oauthlib
```

### OAuth Scope Addition Required
The existing `youtube_token.json` has scopes:
```
["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
```

You'll need to add:
```
"https://www.googleapis.com/auth/analytics.readonly"
```

**To add the scope without breaking existing tokens**, create a helper script `ga4_oauth.py` that re-runs OAuth with the combined scope list. See the complete file content below — it includes the OAuth helper inline as comments.

### Config File to Create
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\ga4_config.json
```

```json
{
    "property_id": "REPLACE_WITH_GA4_PROPERTY_ID",
    "notes": "Find your GA4 property ID in Google Analytics > Admin > Property Settings. It's a numeric ID like 123456789. The token file must include analytics.readonly scope."
}
```

### Complete File Content

```python
"""
Keystone Google Analytics 4 MCP v1.0
Query GA4 for website traffic data: page views, traffic sources, top pages, conversion funnels.
Uses Google Analytics Data API (v1beta).
"""
import os
import sys
import json
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Google Analytics 4")

# ── Configuration ─────────────────────────────────────────────────

GA4_CONFIG_PATH = os.path.join(SCRIPT_DIR, "ga4_config.json")
YT_TOKEN_PATH = os.path.join(SCRIPT_DIR, "youtube_token.json")


def _load_ga4_config():
    """Load GA4 property ID from config file."""
    if os.path.exists(GA4_CONFIG_PATH):
        with open(GA4_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _get_ga4_client():
    """Build a GA4 BetaAnalyticsDataClient using existing YouTube OAuth credentials.

    The youtube_token.json must include the analytics.readonly scope.
    If it doesn't, you'll need to re-run OAuth with the added scope:

    1. Open a Python shell in this directory.
    2. Run:
        from google_auth_oauthlib.flow import InstalledAppFlow
        SCOPES = [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/yt-analytics.readonly",
            "https://www.googleapis.com/auth/analytics.readonly"
        ]
        flow = InstalledAppFlow.from_client_config(
            {"installed": {
                "client_id": "911189793704-0dhnkc0g3f7tlq197ujal3o1ie0e2nk8.apps.googleusercontent.com",
                "client_secret": "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",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }},
            SCOPES
        )
        creds = flow.run_local_server(port=0)
        import json
        with open("youtube_token.json", "w") as f:
            f.write(creds.to_json())
    3. This replaces youtube_token.json with a new token that has all 4 scopes.
    """
    try:
        from google.oauth2.credentials import Credentials
        from google.analytics.data_v1beta import BetaAnalyticsDataClient

        if not os.path.exists(YT_TOKEN_PATH):
            return None, "youtube_token.json not found. Run OAuth first."

        creds = Credentials.from_authorized_user_file(YT_TOKEN_PATH)
        client = BetaAnalyticsDataClient(credentials=creds)
        return client, None
    except ImportError:
        return None, "google-analytics-data package not installed. Run: pip install google-analytics-data"
    except Exception as e:
        return None, str(e)


def _get_property_id(property_id: str = None):
    """Resolve GA4 property ID from argument or config."""
    if property_id:
        return property_id
    config = _load_ga4_config()
    pid = config.get("property_id", "")
    if not pid or "REPLACE" in pid:
        return None
    return pid


# ── Tool 1: Get Page Views ──────────────────────────────────────

@mcp.tool()
def get_page_views(property_id: str = None, start_date: str = None, end_date: str = None) -> str:
    """
    Fetches daily page view counts from GA4.

    Args:
        property_id: GA4 property ID (numeric string). If omitted, reads from ga4_config.json.
        start_date: Start date in YYYY-MM-DD format. Default: 30 days ago.
        end_date: End date in YYYY-MM-DD format. Default: today.

    Returns:
        JSON with daily page view counts, total, and average.

    API Reference: https://developers.google.com/analytics/devguides/reporting/data/v1
    """
    try:
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric, Dimension
        )

        client, error = _get_ga4_client()
        if error:
            return json.dumps({"error": error})

        pid = _get_property_id(property_id)
        if not pid:
            return json.dumps({"error": "No GA4 property ID. Set in ga4_config.json or pass property_id parameter."})

        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{pid}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[Metric(name="screenPageViews"), Metric(name="sessions"), Metric(name="activeUsers")],
            dimensions=[Dimension(name="date")],
            order_bys=[{"dimension": {"dimension_name": "date"}}]
        )
        response = client.run_report(request)

        rows = []
        total_views = 0
        total_sessions = 0
        total_users = 0
        for row in response.rows:
            date = row.dimension_values[0].value
            views = int(row.metric_values[0].value)
            sessions = int(row.metric_values[1].value)
            users = int(row.metric_values[2].value)
            total_views += views
            total_sessions += sessions
            total_users += users
            rows.append({
                "date": f"{date[:4]}-{date[4:6]}-{date[6:]}",
                "page_views": views,
                "sessions": sessions,
                "active_users": users
            })

        num_days = max(len(rows), 1)
        return json.dumps({
            "property_id": pid,
            "start_date": start_date,
            "end_date": end_date,
            "total_page_views": total_views,
            "total_sessions": total_sessions,
            "total_active_users": total_users,
            "avg_daily_views": round(total_views / num_days),
            "daily_data": rows
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e), "hint": "Ensure youtube_token.json has analytics.readonly scope."})


# ── Tool 2: Get Traffic Sources ──────────────────────────────────

@mcp.tool()
def get_traffic_sources(property_id: str = None, days: int = 30) -> str:
    """
    Fetches traffic source breakdown from GA4 (organic, direct, referral, social, etc.).

    Args:
        property_id: GA4 property ID. If omitted, reads from ga4_config.json.
        days: Number of past days to analyze. Default: 30.

    Returns:
        JSON with traffic sources ranked by session count.
    """
    try:
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric, Dimension, OrderBy
        )

        client, error = _get_ga4_client()
        if error:
            return json.dumps({"error": error})

        pid = _get_property_id(property_id)
        if not pid:
            return json.dumps({"error": "No GA4 property ID configured."})

        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{pid}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
                Metric(name="engagedSessions"),
                Metric(name="bounceRate")
            ],
            dimensions=[
                Dimension(name="sessionDefaultChannelGroup"),
                Dimension(name="sessionSource")
            ],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=50
        )
        response = client.run_report(request)

        sources = []
        total_sessions = 0
        for row in response.rows:
            channel = row.dimension_values[0].value
            source = row.dimension_values[1].value
            sessions = int(row.metric_values[0].value)
            users = int(row.metric_values[1].value)
            engaged = int(row.metric_values[2].value)
            bounce = float(row.metric_values[3].value)
            total_sessions += sessions
            sources.append({
                "channel_group": channel,
                "source": source,
                "sessions": sessions,
                "active_users": users,
                "engaged_sessions": engaged,
                "bounce_rate": f"{bounce:.1%}"
            })

        # Add percentage
        for s in sources:
            s["share"] = f"{s['sessions'] / max(total_sessions, 1):.1%}"

        return json.dumps({
            "property_id": pid,
            "days": days,
            "total_sessions": total_sessions,
            "sources": sources
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 3: Get Top Pages ───────────────────────────────────────

@mcp.tool()
def get_top_pages(property_id: str = None, days: int = 30, limit: int = 20) -> str:
    """
    Fetches the top pages by page views from GA4.

    Args:
        property_id: GA4 property ID. If omitted, reads from ga4_config.json.
        days: Number of past days to analyze. Default: 30.
        limit: Maximum number of pages to return. Default: 20.

    Returns:
        JSON with top pages ranked by views, including avg engagement time.
    """
    try:
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric, Dimension, OrderBy
        )

        client, error = _get_ga4_client()
        if error:
            return json.dumps({"error": error})

        pid = _get_property_id(property_id)
        if not pid:
            return json.dumps({"error": "No GA4 property ID configured."})

        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{pid}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate")
            ],
            dimensions=[
                Dimension(name="pagePath"),
                Dimension(name="pageTitle")
            ],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
            limit=limit
        )
        response = client.run_report(request)

        pages = []
        for row in response.rows:
            path = row.dimension_values[0].value
            title = row.dimension_values[1].value
            views = int(row.metric_values[0].value)
            users = int(row.metric_values[1].value)
            avg_duration = float(row.metric_values[2].value)
            bounce = float(row.metric_values[3].value)
            pages.append({
                "path": path,
                "title": title[:60],
                "page_views": views,
                "active_users": users,
                "avg_session_duration_sec": round(avg_duration, 1),
                "bounce_rate": f"{bounce:.1%}"
            })

        return json.dumps({
            "property_id": pid,
            "days": days,
            "total_pages": len(pages),
            "pages": pages
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool 4: Get Conversion Funnel ────────────────────────────────

@mcp.tool()
def get_conversion_funnel(property_id: str = None, days: int = 30) -> str:
    """
    Analyzes the conversion funnel: sessions → engaged sessions → conversions.
    Also shows event counts for key conversion events.

    Args:
        property_id: GA4 property ID. If omitted, reads from ga4_config.json.
        days: Number of past days to analyze. Default: 30.

    Returns:
        JSON with funnel metrics and top events.
    """
    try:
        from google.analytics.data_v1beta.types import (
            RunReportRequest, DateRange, Metric, Dimension, OrderBy
        )

        client, error = _get_ga4_client()
        if error:
            return json.dumps({"error": error})

        pid = _get_property_id(property_id)
        if not pid:
            return json.dumps({"error": "No GA4 property ID configured."})

        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")

        # Funnel overview (aggregate metrics)
        overview_request = RunReportRequest(
            property=f"properties/{pid}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="sessions"),
                Metric(name="engagedSessions"),
                Metric(name="activeUsers"),
                Metric(name="newUsers"),
                Metric(name="conversions"),
                Metric(name="engagementRate"),
                Metric(name="averageSessionDuration")
            ]
        )
        overview_response = client.run_report(overview_request)

        overview = {}
        if overview_response.rows:
            row = overview_response.rows[0]
            overview = {
                "sessions": int(row.metric_values[0].value),
                "engaged_sessions": int(row.metric_values[1].value),
                "active_users": int(row.metric_values[2].value),
                "new_users": int(row.metric_values[3].value),
                "conversions": int(row.metric_values[4].value),
                "engagement_rate": f"{float(row.metric_values[5].value):.1%}",
                "avg_session_duration_sec": round(float(row.metric_values[6].value), 1)
            }
            sessions = overview["sessions"]
            engaged = overview["engaged_sessions"]
            conversions = overview["conversions"]
            overview["funnel"] = {
                "sessions_to_engaged": f"{engaged / max(sessions, 1):.1%}",
                "engaged_to_conversion": f"{conversions / max(engaged, 1):.1%}",
                "overall_conversion_rate": f"{conversions / max(sessions, 1):.1%}"
            }

        # Top events
        events_request = RunReportRequest(
            property=f"properties/{pid}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[Metric(name="eventCount"), Metric(name="totalUsers")],
            dimensions=[Dimension(name="eventName")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="eventCount"), desc=True)],
            limit=15
        )
        events_response = client.run_report(events_request)

        events = []
        for row in events_response.rows:
            events.append({
                "event_name": row.dimension_values[0].value,
                "event_count": int(row.metric_values[0].value),
                "unique_users": int(row.metric_values[1].value)
            })

        return json.dumps({
            "property_id": pid,
            "days": days,
            "overview": overview,
            "top_events": events
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()
```

### Tool Schemas Summary

| Tool | Parameters | Types | Required |
|------|-----------|-------|----------|
| `get_page_views` | `property_id`, `start_date`, `end_date` | `str`, `str`, `str` | none |
| `get_traffic_sources` | `property_id`, `days` | `str`, `int` | none |
| `get_top_pages` | `property_id`, `days`, `limit` | `str`, `int`, `int` | none |
| `get_conversion_funnel` | `property_id`, `days` | `str`, `int` | none |

### API Reference
- **GA4 Data API v1beta**: https://developers.google.com/analytics/devguides/reporting/data/v1
- **RunReport**: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
- **Dimensions & Metrics Explorer**: https://ga-dev-tools.google/ga4/dimensions-metrics-explorer/

### Key GA4 Metrics Available
| Metric | API Name | Description |
|--------|----------|-------------|
| Page Views | `screenPageViews` | Total page/screen views |
| Sessions | `sessions` | Total sessions |
| Active Users | `activeUsers` | Users who had an engaged session |
| Bounce Rate | `bounceRate` | % of sessions that were not engaged |
| Conversions | `conversions` | Total conversion events |
| Engagement Rate | `engagementRate` | % of sessions that were engaged |
| Avg Duration | `averageSessionDuration` | Average time in seconds |

---

## 6. MCP Multiplexer Registration

### Updated agents.json

Add these 3 entries to:
```
c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\MCP_Multiplexer\agents.json
```

Append after the existing `"dynamic_skills"` entry (before the closing `}`):

```json
  "social_analytics": {
    "command": "python",
    "args": ["../social_analytics_mcp.py"],
    "enabled": true
  },
  "shopify": {
    "command": "python",
    "args": ["../shopify_mcp.py"],
    "enabled": true
  },
  "ga4": {
    "command": "python",
    "args": ["../ga4_mcp.py"],
    "enabled": true
  }
```

### After Adding Entries — Refresh the Cache

The multiplexer needs to rebuild its tool cache after adding new agents:

```bash
# From the MCP_Multiplexer directory
cd "c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\MCP_Multiplexer"

# Refresh the tool cache (this calls mcp_multiplexer_refresh_tool_cache)
# Or simply restart the multiplexer — it auto-discovers on boot
```

From Antigravity, call:
```
call_mcp_tool(
    ServerName="keystone_multiplexer",
    ToolName="mcp_multiplexer_refresh_tool_cache",
    Arguments={}
)
```

### Updated Orchestration Skill Reference

After building, update `C:\Users\Curtis\.gemini\config\skills\keystone_architect_orchestration\SKILL.md` to add:

```markdown
13. `social_analytics`: YouTube Analytics, Meta Insights, TikTok Business API.
14. `shopify`: Shopify store management — products, orders, discounts.
15. `ga4`: Google Analytics 4 — page views, traffic sources, conversions.
```

---

## 7. Testing Commands Summary

### Test Each MCP Server Individually

```powershell
# Test Social Analytics MCP
cd "c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
python -c "from social_analytics_mcp import mcp; print('Social Analytics MCP loaded OK, tools:', [t.name for t in mcp._tools.values()])"

# Test Shopify MCP
python -c "from shopify_mcp import mcp; print('Shopify MCP loaded OK, tools:', [t.name for t in mcp._tools.values()])"

# Test GA4 MCP
python -c "from ga4_mcp import mcp; print('GA4 MCP loaded OK, tools:', [t.name for t in mcp._tools.values()])"
```

### Test via Multiplexer (After Registration)

From Antigravity, use `mcp_multiplexer_execute_tool`:

```javascript
// Test social analytics
mcp_multiplexer_execute_tool({
    agentName: "social_analytics",
    toolName: "get_cross_platform_summary",
    arguments: { brand: "all", days: 7 }
})

// Test Shopify
mcp_multiplexer_execute_tool({
    agentName: "shopify",
    toolName: "list_products",
    arguments: {}
})

// Test GA4
mcp_multiplexer_execute_tool({
    agentName: "ga4",
    toolName: "get_page_views",
    arguments: { days: 7 }
})
```

### Test Skills (From Antigravity)

**Brave Validator**: Navigate to `Research_Archives/`, pick the latest `.md` file, and say:
> "Validate the latest research report using the Brave validator skill"

**Brain Health Audit**: Simply say:
> "Run a brain health audit"

The agent should read the skill, execute the 7-step protocol, and output a scored report.

### Verify Skill Files Exist

```powershell
# Check skill directories exist
Test-Path "C:\Users\Curtis\.gemini\config\skills\keystone_brave_validator\SKILL.md"
Test-Path "C:\Users\Curtis\.gemini\config\skills\keystone_brain_health_audit\SKILL.md"

# Verify YAML frontmatter
Get-Content "C:\Users\Curtis\.gemini\config\skills\keystone_brave_validator\SKILL.md" -Head 4
Get-Content "C:\Users\Curtis\.gemini\config\skills\keystone_brain_health_audit\SKILL.md" -Head 4
```

### Dependency Check

```powershell
# Verify all Python packages are installed
python -c "import mcp; print('mcp OK')"
python -c "from google.oauth2.credentials import Credentials; print('google-auth OK')"
python -c "from googleapiclient.discovery import build; print('google-api-python-client OK')"
python -c "import requests; print('requests OK')"
python -c "from google.analytics.data_v1beta import BetaAnalyticsDataClient; print('google-analytics-data OK')"
```

If any fail, install:
```powershell
pip install mcp google-auth google-auth-oauthlib google-api-python-client requests google-analytics-data
```

---

## Build Checklist

| # | Item | File | Status |
|---|------|------|--------|
| 1 | Brave Research Validator Skill | `C:\Users\Curtis\.gemini\config\skills\keystone_brave_validator\SKILL.md` | ⬜ |
| 2 | Brain Health Audit Skill | `C:\Users\Curtis\.gemini\config\skills\keystone_brain_health_audit\SKILL.md` | ⬜ |
| 3 | Social Analytics MCP Server | `{WORKSPACE}/social_analytics_mcp.py` | ⬜ |
| 4 | Shopify Manager MCP Server | `{WORKSPACE}/shopify_mcp.py` | ⬜ |
| 4a | Shopify Config Placeholder | `{WORKSPACE}/shopify_config.json` | ⬜ |
| 5 | GA4 MCP Server | `{WORKSPACE}/ga4_mcp.py` | ⬜ |
| 5a | GA4 Config Placeholder | `{WORKSPACE}/ga4_config.json` | ⬜ |
| 6 | Update agents.json | `{WORKSPACE}/MCP_Multiplexer/agents.json` | ⬜ |
| 7 | Refresh Multiplexer Cache | `mcp_multiplexer_refresh_tool_cache` | ⬜ |
| 8 | Install Dependencies | `pip install ...` | ⬜ |
| 9 | Test All Servers Load | `python -c "from X import mcp"` | ⬜ |
| 10 | Test Via Multiplexer | `mcp_multiplexer_execute_tool` | ⬜ |
| 11 | Update Orchestration Skill | Add agents 13-15 | ⬜ |

`{WORKSPACE}` = `c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain`
