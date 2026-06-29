# TikTok Content Posting API v2 -- Complete Technical Reference

**Research Date:** May 22, 2026
**Domain:** self_correction_tonight
**Problem Context:** Our pipeline got `scope_not_authorized` because the token only had `video.upload` (drafts) not `video.publish` (direct post). This guide documents everything needed to fix this permanently.

---

## 1. Scope Reference: video.upload vs video.publish

This is the root cause of our failure. These two scopes serve fundamentally different purposes:

| Aspect | `video.upload` | `video.publish` |
|---|---|---|
| **Purpose** | Draft / Inbox Mode | Direct Post Mode |
| **What happens** | Uploads media as a DRAFT to user's TikTok inbox. User must manually review and publish inside the TikTok app. | Publishes video DIRECTLY to user's profile programmatically. |
| **Endpoint** | `/v2/post/publish/inbox/video/init/` | `/v2/post/publish/video/init/` |
| **User action required** | YES - user must open TikTok, review, add [[music|music]]/effects, then tap Post | NO - video goes live automatically |
| **Metadata control** | Limited - user sets caption/privacy in-app | Full - you set title, privacy, disable_comment, disable_duet, disable_stitch, video_cover_timestamp_ms |
| **Audit required for public** | No (but drafts are private until user publishes) | YES - unaudited apps are restricted to private/SELF_ONLY visibility |

**Key takeaway:** We had `video.upload` which only creates drafts. We need `video.publish` for our automated pipeline to directly post videos.

---

## 2. How to Request video.publish Scope

### Step-by-Step Process

1. **Log into TikTok Developer Portal:** Go to https://developers.tiktok.com/ and navigate to your app settings.

2. **Add Content Posting API:** In your app's product list, ensure "Content Posting API" is added/enabled.

3. **Enable Scopes:** In the "Scopes" section, explicitly check/request `video.publish`. Also ensure "Direct Post" configuration toggle is enabled.

4. **Update OAuth Flow:** When redirecting users to authorize, include `video.publish` in the scope parameter:
   ```
   https://www.tiktok.com/v2/auth/authorize/?client_key=YOUR_KEY&scope=user.info.basic,video.publish&response_type=code&redirect_uri=YOUR_URI
   ```

5. **Re-authorize Users:** Any existing users must re-authorize the app so their access tokens include the new `video.publish` scope. Old tokens with only `video.upload` will NOT work.

6. **Submit for App Audit:** (See Section 3 below)

### CRITICAL: Token Must Include the Scope

Even after adding the scope in the developer portal, if the user authorized your app BEFORE you added `video.publish`, their token will NOT have it. You must:
- Revoke the old token
- Re-redirect the user through the OAuth flow with `video.publish` in the scope list
- Store the new access_token and refresh_token

---

## 3. App Audit Process and Timeline

### Why Audit Is Required

TikTok requires a formal manual audit for apps using `video.publish` because it allows direct public posting to user accounts. **Without passing audit, ALL posts from your app are forced to `SELF_ONLY` (private) visibility**, regardless of what `privacy_level` you set in the API request.

### What You Need to Submit

1. **Clear description** of how your app uses the Content Posting API
2. **Demo video or screenshots** showing the complete user experience (UX flow)
3. **Valid URLs** for your Privacy Policy and Terms of Service
4. **Test accounts/credentials** for TikTok reviewers to access and test your app
5. **Fully functional integration** -- reviewers must be able to test the features live

### Timeline

- **Estimated review time: 2 to 6 weeks** (manual process, no SLA guaranteed)
- No official fast-track option exists
- Clean, complete submissions on first attempt are the best way to avoid delays
- If rejected, you receive feedback and can resubmit after corrections

### Ongoing Compliance

Even after approval, TikTok may conduct periodic audits. Violations can result in immediate API access revocation.

---

## 4. Complete API Endpoint Reference

Base URL: `https://open.tiktokapis.com`

### 4.1 Query Creator Info (MANDATORY before posting)

```
POST /v2/post/publish/creator_info/query/
Authorization: Bearer {access_token}
Content-Type: application/json; charset=UTF-8
```

**Response includes:**
- `creator_nickname` -- display name
- `privacy_level_options` -- array of allowed privacy settings for this user:
  - `PUBLIC_TO_EVERYONE`
  - `MUTUAL_FOLLOW_FRIENDS`
  - `FOLLOWER_OF_CREATOR`
  - `SELF_ONLY`
- `max_video_post_duration_sec` -- maximum video duration this creator can post
- Interaction settings (comment, duet, stitch availability)

**Rate limit:** 20 requests/minute per user token.

**IMPORTANT:** You MUST call this endpoint before posting and use only the `privacy_level` values it returns. Do not hardcode privacy levels.

### 4.2 Direct Post Video Init

```
POST /v2/post/publish/video/init/
Authorization: Bearer {access_token}
Content-Type: application/json; charset=UTF-8
```

**Scope required:** `video.publish`

**Request body (PULL_FROM_URL method):**

```json
{
  "post_info": {
    "title": "Your video caption here #hashtag",
    "privacy_level": "PUBLIC_TO_EVERYONE",
    "disable_comment": false,
    "disable_duet": false,
    "disable_stitch": false,
    "video_cover_timestamp_ms": 5000
  },
  "source_info": {
    "source": "PULL_FROM_URL",
    "video_url": "https://your-verified-domain.com/path/to/video.mp4"
  }
}
```

**Request body (FILE_UPLOAD method):**

```json
{
  "post_info": {
    "title": "Your video caption here",
    "privacy_level": "SELF_ONLY",
    "disable_comment": false,
    "disable_duet": false,
    "disable_stitch": false,
    "video_cover_timestamp_ms": 1000
  },
  "source_info": {
    "source": "FILE_UPLOAD",
    "video_size": 52428800,
    "chunk_size": 10485760,
    "total_chunk_count": 5
  }
}
```

**Response:**
```json
{
  "data": {
    "publish_id": "v_pub_abc123...",
    "upload_url": "https://open-upload.tiktokapis.com/video/?upload_id=xxx&upload_token=yyy"
  },
  "error": {
    "code": "ok",
    "message": "",
    "log_id": "..."
  }
}
```

### 4.3 Inbox/Draft Video Init (uses video.upload scope)

```
POST /v2/post/publish/inbox/video/init/
```

Same structure but uses `video.upload` scope. Creates a draft, not a direct post.

### 4.4 Status Fetch (Poll for completion)

```
POST /v2/post/publish/status/fetch/
Authorization: Bearer {access_token}
Content-Type: application/json; charset=UTF-8

{
  "publish_id": "v_pub_abc123..."
}
```

**Terminal statuses:**
- `PUBLISH_COMPLETE` -- success, video is live
- `FAILED` -- something went wrong, check error details

**Recommended polling interval:** Every 10-30 seconds until terminal status.

**Alternative:** TikTok provides Content Posting webhooks that notify your endpoint immediately on completion, eliminating the need for polling.

---

## 5. PULL_FROM_URL -- Formats and Host Requirements

### Supported Video Specifications

| Parameter | Requirement |
|---|---|
| **Containers** | MP4 (recommended), WebM, MOV |
| **Codecs** | H.264 (recommended), H.265, VP8, VP9 |
| **Framerate** | 23-60 FPS |
| **Resolution** | Min 360x360, Max 4096x4096, Recommended 1080x1920 (9:16) |
| **Duration** | 3 seconds to 10 minutes (check `max_video_post_duration_sec` from creator_info) |
| **File Size** | Max 4GB (some sources say 1GB -- use creator_info to verify) |
| **Caption Length** | Max 2,200 characters |

### Host/Domain Requirements

There is NO whitelist of specific hosting providers. Instead:

1. **You must own and verify the domain** through "Manage URL properties" in your app settings on the TikTok Developer Portal.
2. Verification can be at domain level (e.g., `static.example.com`) or URL prefix level (e.g., `https://example.com/videos/`).
3. The URL must be **publicly accessible** without authentication.
4. Avoid short-lived pre-signed URLs that may expire before TikTok finishes downloading.
5. Once a domain/prefix is verified, all files under it are eligible.

### Practical Hosting Options

- Your own web server with a verified domain
- Cloud storage (AWS S3, Google Cloud Storage, Azure Blob) with a verified custom domain in front
- Any CDN with a verified domain

---

## 6. video_cover_timestamp_ms Parameter

This parameter selects the video thumbnail (cover image) by specifying a timestamp in milliseconds.

**Key details:**
- Value is in **milliseconds** from the start of the video
- Example: `1000` = thumbnail from 1-second mark
- Example: `5000` = thumbnail from 5-second mark
- **Default:** If omitted or invalid, TikTok uses the FIRST frame of the video
- **For last frame:** Calculate your video duration in ms and use that value (e.g., for a 30-second video: `video_cover_timestamp_ms: 30000`)
- **Limitation:** You can only select a frame FROM the video. You CANNOT upload a separate custom thumbnail image via the API.

### Selecting the Last Frame

```python
# To use the last frame as thumbnail:
# If your video is 30 seconds (30000ms), use:
video_cover_timestamp_ms = 29900  # slightly before end to ensure valid frame

# You can get exact duration using ffprobe:
# ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4
# Returns: 30.033333
# Convert to ms: int(30.033333 * 1000) - 100 = 29933
```

---

## 7. Rate Limits and Constraints

| Limit | Value |
|---|---|
| **Posting requests** | 6 per minute per user access_token |
| **Creator info queries** | 20 per minute per user access_token |
| **Status fetch requests** | ~30 per minute |
| **Daily posting cap** | 15-25 videos per account per 24 hours (varies by tier) |
| **Access token lifetime** | ~24 hours (use refresh_token to renew) |
| **Refresh token lifetime** | 365 days |
| **Upload URL expiry** | 1 hour after issuance |
| **Chunked upload - chunk size** | Min 5MB, Max 64MB per chunk (final chunk up to 128MB) |
| **Chunked upload - max chunks** | 1,000 chunks |
| **Chunked upload - small files** | Files under 5MB: upload as single chunk |

---

## 8. Complete Working Python Code

```python
"""
TikTok Content Posting API v2 -- Direct Post Pipeline
Requires: pip install requests

Scopes needed: user.info.basic, video.publish
"""
import requests
import time
import os
import math

# --- Configuration ---
ACCESS_TOKEN = os.environ.get("TIKTOK_ACCESS_TOKEN", "your_access_token_here")
BASE_URL = "https://open.tiktokapis.com"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json; charset=UTF-8"
}


def query_creator_info():
    """Step 1: Query creator info to get available privacy levels."""
    url = f"{BASE_URL}/v2/post/publish/creator_info/query/"
    response = requests.post(url, headers=HEADERS, json={})
    data = response.json()

    if data.get("error", {}).get("code") != "ok":
        raise Exception(f"Creator info query failed: {data}")

    creator_data = data.get("data", {})
    print(f"Creator: {creator_data.get('creator_nickname', 'Unknown')}")
    print(f"Privacy options: {creator_data.get('privacy_level_options', [])}")
    print(f"Max video duration: {creator_data.get('max_video_post_duration_sec', 'N/A')}s")
    return creator_data


def publish_video_pull_from_url(video_url, title, privacy_level="SELF_ONLY",
                                 cover_timestamp_ms=1000):
    """Step 2a: Direct post using PULL_FROM_URL method."""
    url = f"{BASE_URL}/v2/post/publish/video/init/"

    payload = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_comment": False,
            "disable_duet": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": cover_timestamp_ms
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()

    if data.get("error", {}).get("code") != "ok":
        raise Exception(f"Publish init failed: {data}")

    publish_id = data["data"]["publish_id"]
    print(f"Publish initiated. ID: {publish_id}")
    return publish_id


def publish_video_file_upload(file_path, title, privacy_level="SELF_ONLY",
                               cover_timestamp_ms=1000):
    """Step 2b: Direct post using FILE_UPLOAD (chunked) method."""
    file_size = os.path.getsize(file_path)
    chunk_size = min(max(5 * 1024 * 1024, file_size), 64 * 1024 * 1024)  # 5MB-64MB
    total_chunks = max(1, math.ceil(file_size / chunk_size))

    url = f"{BASE_URL}/v2/post/publish/video/init/"

    payload = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_comment": False,
            "disable_duet": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": cover_timestamp_ms
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    data = response.json()

    if data.get("error", {}).get("code") != "ok":
        raise Exception(f"Upload init failed: {data}")

    publish_id = data["data"]["publish_id"]
    upload_url = data["data"]["upload_url"]
    print(f"Upload initialized. ID: {publish_id}")

    # Upload chunks sequentially
    with open(file_path, "rb") as f:
        for i in range(total_chunks):
            chunk_data = f.read(chunk_size)
            first_byte = i * chunk_size
            last_byte = first_byte + len(chunk_data) - 1

            chunk_headers = {
                "Content-Type": "video/mp4",
                "Content-Length": str(len(chunk_data)),
                "Content-Range": f"bytes {first_byte}-{last_byte}/{file_size}"
            }

            put_response = requests.put(upload_url, headers=chunk_headers, data=chunk_data)
            if put_response.status_code not in (200, 201, 206):
                raise Exception(f"Chunk {i+1}/{total_chunks} upload failed: {put_response.status_code}")
            print(f"  Chunk {i+1}/{total_chunks} uploaded ({len(chunk_data)} bytes)")

    return publish_id


def poll_publish_status(publish_id, max_attempts=30, interval=15):
    """Step 3: Poll until PUBLISH_COMPLETE or FAILED."""
    url = f"{BASE_URL}/v2/post/publish/status/fetch/"

    for attempt in range(max_attempts):
        response = requests.post(url, headers=HEADERS, json={"publish_id": publish_id})
        data = response.json()

        if data.get("error", {}).get("code") != "ok":
            print(f"  Status fetch error: {data}")
            time.sleep(interval)
            continue

        status = data.get("data", {}).get("status", "UNKNOWN")
        print(f"  Attempt {attempt+1}: Status = {status}")

        if status == "PUBLISH_COMPLETE":
            print(f"  Video published! Post ID: {data['data'].get('publicaly_available_post_id', 'N/A')}")
            return data
        elif status == "FAILED":
            fail_reason = data.get("data", {}).get("fail_reason", "Unknown")
            raise Exception(f"Publish failed: {fail_reason}")

        time.sleep(interval)

    raise Exception(f"Publish timed out after {max_attempts * interval} seconds")


# --- Main Pipeline ---
def main():
    # Step 1: Check creator capabilities
    creator = query_creator_info()
    privacy_options = creator.get("privacy_level_options", ["SELF_ONLY"])

    # Choose best available privacy level
    preferred = "PUBLIC_TO_EVERYONE"
    privacy = preferred if preferred in privacy_options else privacy_options[0]
    print(f"Using privacy level: {privacy}")

    # Step 2: Initiate publish (choose one method)
    # Method A: Pull from URL (video must be on your verified domain)
    publish_id = publish_video_pull_from_url(
        video_url="https://your-verified-domain.com/videos/latest.mp4",
        title="Check out our latest project! #construction #keystone",
        privacy_level=privacy,
        cover_timestamp_ms=5000
    )

    # Method B: File upload (uncomment to use instead)
    # publish_id = publish_video_file_upload(
    #     file_path="./video.mp4",
    #     title="Check out our latest project! #construction #keystone",
    #     privacy_level=privacy,
    #     cover_timestamp_ms=5000
    # )

    # Step 3: Poll until complete
    result = poll_publish_status(publish_id)
    print("Pipeline complete!")
    return result


if __name__ == "__main__":
    main()
```

---

## 9. Common Errors and [[Troubleshooting|Troubleshooting]]

| Error Code | HTTP | Cause | Fix |
|---|---|---|---|
| `scope_not_authorized` | 403 | Token lacks `video.publish` scope | Re-authorize user with `video.publish` in scope parameter. Check app has scope enabled in developer portal. |
| `access_token_invalid` | 401 | Token expired or revoked | Refresh using `refresh_token`. If refresh fails, re-authorize. |
| `scope_permission_missed` | 403 | Endpoint requires a scope not in token | Check docs for required scopes, re-authorize with all needed scopes. |
| `invalid_grant` | 400 | Auth code expired, already used, or mismatched redirect_uri | Use a fresh authorization code. Verify redirect_uri matches exactly. |
| `rate_limit_exceeded` | 429 | Too many requests per minute | Implement exponential backoff. Max 6 posts/min per user token. |
| `invalid_params` | 400 | Bad request body or invalid parameter values | Check all fields match API spec. Verify `privacy_level` matches creator_info response. |
| `invalid_file_upload` | 400 | Video doesn't meet specs | Check format (MP4/H.264), resolution (min 360x360), duration (3s-10min), size limits. |
| `url_ownership_unverified` | 403 | PULL_FROM_URL domain not verified | Verify domain in "Manage URL properties" in developer portal. |
| `internal_error` | 5xx | TikTok server issue | Retry after delay. Include `log_id` if contacting support. |
| Posts are private despite setting PUBLIC | N/A | App not audited | Complete app audit process. Unaudited apps are forced to SELF_ONLY. |

### Troubleshooting Checklist

1. **Check token scopes:** Decode or inspect the access_token to verify it includes `video.publish`
2. **Re-authorize if needed:** Users must go through OAuth again after you add new scopes
3. **Call creator_info FIRST:** Always query available privacy levels before posting
4. **Verify domain for PULL_FROM_URL:** Domain must be verified in developer portal
5. **Check file specs:** MP4/H.264, 1080x1920, 23-60fps, 3s-10min, under 4GB
6. **Handle token refresh:** Access tokens expire in ~24 hours; use refresh_token proactively
7. **Log everything:** Always capture the `log_id` from error responses for TikTok support

---

## 10. Immediate Action Items for Our Pipeline

1. **TONIGHT:** Go to https://developers.tiktok.com/, add `video.publish` scope to our app
2. **TONIGHT:** Enable "Direct Post" toggle in app settings
3. **TONIGHT:** Update our OAuth redirect URL to include `scope=user.info.basic,video.publish`
4. **TONIGHT:** Re-authorize our TikTok account to get a new token with `video.publish`
5. **TONIGHT:** Update our code to use `/v2/post/publish/video/init/` (NOT the inbox endpoint)
6. **THIS WEEK:** Verify our hosting domain in "Manage URL properties" for PULL_FROM_URL
7. **THIS WEEK:** Submit app for audit (prepare demo video, privacy policy, ToS)
8. **EXPECT:** 2-6 weeks for audit approval; until then, posts will be private (SELF_ONLY)
9. **INTERIM:** We CAN post with `video.publish` immediately, but visibility is SELF_ONLY until audit passes

---

## Sources Consulted

- TikTok Content Posting API v2 official documentation (developers.tiktok.com)
- TikTok Developer Portal scope management documentation
- TikTok app audit process guidelines
- Multiple developer community posts (Stack Overflow, Medium, Dev.to)
- Third-party API wrapper documentation (Zernio, Ayrshare, PostProxy)
- TikTok error code reference documentation

---

*Generated by Keystone Sovereign overnight research agent, May 22, 2026*


---
📁 **See also:** [[Research_Archives/09_Social_Media/INDEX|← Directory Index]]

**Related:** [[20260522_social_media_automation_tiktok_content_posting_api_v2_direct_publish_flow_complete_g]]
