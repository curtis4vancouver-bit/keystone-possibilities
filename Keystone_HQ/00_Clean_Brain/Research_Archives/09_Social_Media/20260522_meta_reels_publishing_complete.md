# Meta Reels Publishing API - Complete Technical Guide

**Research Date:** May 22, 2026
**Domain:** self_correction_tonight
**Sources:** Meta Graph API documentation, developer forums, StackOverflow, Postman collections, multiple third-party API guides
**Graph API Version:** v25.0 (current as of May 2026; adjust to latest)

---

## Table of Contents

1. [Overview & Architecture](#overview)
2. [Prerequisites & Permissions](#prerequisites)
3. [Token Management: Getting Page Token & IG Business Account ID](#token-management)
4. [Instagram Reels Publishing Flow](#instagram-reels)
5. [Facebook Page Reels Publishing Flow](#facebook-reels)
6. [Cover Image / Thumbnail Control](#cover-thumbnail)
7. [Video Format Requirements](#video-format)
8. [Rate Limits & Quotas](#rate-limits)
9. [Complete Python Implementation](#python-code)
10. [Troubleshooting & Common Errors](#troubleshooting)

---

## 1. Overview & [[ARCHITECTURE|Architecture]] <a name="overview"></a>

Meta provides **two completely separate APIs** for publishing Reels:

| Platform | Endpoint Pattern | Flow Type |
|----------|-----------------|-----------|
| **Instagram** | `/{ig-user-id}/media` + `/{ig-user-id}/media_publish` | Container-based (create, poll, publish) |
| **Facebook Pages** | `/{page-id}/video_reels` | Resumable upload (start, upload, finish) |

Both require the video to be hosted at a **publicly accessible URL** (e.g., catbox.moe, S3, CDN). Meta's servers will cURL/fetch the video from that URL during processing.

**Critical difference:** Instagram uses a container model where you create a media container, wait for processing, then publish. Facebook uses a resumable upload model with explicit start/upload/finish phases.

---

## 2. Prerequisites & Permissions <a name="prerequisites"></a>

### Account Requirements

- **Instagram:** Must be an **Instagram Business account** (NOT Creator, NOT Personal) linked to a Facebook Page
- **Facebook:** Must be a **Facebook Page** (not a personal profile)
- **Meta App:** Must be created at developers.facebook.com with App Review completed for required permissions

### Required Permission Scopes (Updated January 2025)

**IMPORTANT:** The old scopes (`instagram_basic`, `instagram_content_publish`) were **deprecated on January 27, 2025**. Use the new scopes:

| Scope | Purpose | Platform |
|-------|---------|----------|
| `instagram_business_basic` | Access IG account info (replaces `instagram_basic`) | Instagram |
| `instagram_business_content_publish` | Publish content to IG (replaces `instagram_content_publish`) | Instagram |
| `pages_show_list` | List Pages the user manages | Both |
| `pages_read_engagement` | Read Page engagement data | Both |
| `pages_manage_posts` | Create/publish posts on Pages | Facebook |
| `business_management` | Access business-level data | Token discovery |

### App Review

Each permission requires a separate submission through Meta's App Review process, including a screencast demonstrating the complete user flow. Development mode allows testing with app admins/testers only.

---

## 3. Token Management <a name="token-management"></a>

### Step 1: Get a Long-Lived User Token

Exchange a short-lived token for a long-lived one (60 days):

```
GET https://graph.facebook.com/v25.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={app-id}
  &client_secret={app-secret}
  &fb_exchange_token={short-lived-user-token}
```

### Step 2: Get Page Access Token & Instagram Business Account ID

```
GET https://graph.facebook.com/v25.0/me/accounts
  ?fields=name,id,access_token,instagram_business_account
  &access_token={user-access-token}
```

**Response:**
```json
{
  "data": [
    {
      "name": "My Business Page",
      "id": "123456789",
      "access_token": "EAAG...page_token...",
      "instagram_business_account": {
        "id": "17841400000000000"
      }
    }
  ]
}
```

- `id` = **Page ID** (used for Facebook Reels)
- `access_token` = **Page Access Token** (use this for all API calls)
- `instagram_business_account.id` = **IG User ID** (used for Instagram Reels)

**Note:** Page tokens derived from long-lived user tokens are themselves long-lived and do not expire.

---

## 4. Instagram Reels Publishing Flow <a name="instagram-reels"></a>

Instagram uses a **three-step container model**:

### Step 1: Create Media Container

```
POST https://graph.facebook.com/v25.0/{ig-user-id}/media
```

**Parameters:**

| Parameter | Required | Value |
|-----------|----------|-------|
| `media_type` | Yes | `REELS` |
| `video_url` | Yes | Public URL of video file |
| `caption` | No | Text caption (supports hashtags, mentions) |
| `share_to_feed` | No | `true` to show on profile grid (default: `true`) |
| `thumb_offset` | No | Milliseconds from video start for cover frame (default: 0) |
| `cover_url` | No | Public URL of custom cover image (JPEG, max 8MB) |
| `location_id` | No | Facebook Location Page ID |
| `collaborators` | No | Array of IG user IDs |
| `access_token` | Yes | Page access token |

**Response:**
```json
{
  "id": "90010778325754"
}
```

### Step 2: Poll Container Status

```
GET https://graph.facebook.com/v25.0/{container-id}
  ?fields=status_code
  &access_token={access-token}
```

Poll every 5 seconds until `status_code` returns `FINISHED`. Possible values:
- `IN_PROGRESS` - Still processing
- `FINISHED` - Ready to publish
- `ERROR` - Processing failed (check `status` field for details)

### Step 3: Publish

```
POST https://graph.facebook.com/v25.0/{ig-user-id}/media_publish
```

**Parameters:**
- `creation_id`: The container ID from Step 1
- `access_token`: Page access token

**Response:**
```json
{
  "id": "90010778325755"
}
```

This `id` is the final published media ID.

---

## 5. Facebook Page Reels Publishing Flow <a name="facebook-reels"></a>

Facebook uses a **three-step resumable upload model**:

### Step 1: Initialize Upload Session

```
POST https://graph.facebook.com/v25.0/{page-id}/video_reels
```

**Parameters:**
- `upload_phase`: `start`
- `access_token`: Page access token

**Response:**
```json
{
  "video_id": "1234567890",
  "upload_url": "https://rupload.facebook.com/video-upload/v25.0/1234567890"
}
```

### Step 2: Upload Video

**Option A: Upload from public URL (our use case with catbox.moe)**

```
POST https://rupload.facebook.com/video-upload/v25.0/{video-id}
```

**Headers:**
- `Authorization`: `OAuth {page-access-token}`
- `file_url`: `https://files.catbox.moe/abc123.mp4`

**Option B: Upload binary data (local file)**

```
POST {upload_url}
```

**Headers:**
- `Authorization`: `OAuth {page-access-token}`
- `file_offset`: `0`
- `file_size`: `{file-size-in-bytes}`

**Body:** Raw binary video data

### Step 3: Publish (Finish)

```
POST https://graph.facebook.com/v25.0/{page-id}/video_reels
```

**Parameters:**

| Parameter | Required | Value |
|-----------|----------|-------|
| `upload_phase` | Yes | `finish` |
| `video_id` | Yes | Video ID from Step 1 |
| `video_state` | Yes | `PUBLISHED` (or `DRAFT`, `SCHEDULED`) |
| `description` | No | Caption text |
| `title` | No | Video title |
| `access_token` | Yes | Page access token |

**IMPORTANT:** Use `graph.facebook.com` for start/finish phases, but `rupload.facebook.com` for the actual upload.

---

## 6. Cover Image / Thumbnail Control <a name="cover-thumbnail"></a>

### Instagram Reels - Full Support

Instagram provides two parameters during container creation (Step 1):

#### `thumb_offset` (Frame Selection)
- **Type:** Integer (milliseconds from video start)
- **Default:** 0 (first frame)
- **Example:** For a 30-second video, to use a frame from the last 2 seconds: `thumb_offset=28000` (28 seconds = 28000ms)
- **Calculation for "last 2 seconds":** `thumb_offset = (video_duration_seconds - 2) * 1000`

#### `cover_url` (Custom Image)
- **Type:** String (public URL to JPEG image)
- **Format:** JPEG only
- **Max size:** 8 MB
- **Color space:** sRGB
- **Recommended aspect ratio:** 9:16 (Meta will center-crop other ratios)
- **IMPORTANT:** If BOTH `cover_url` AND `thumb_offset` are provided, `cover_url` takes precedence and `thumb_offset` is IGNORED

#### Choosing the Right Approach for Our Use Case

Since we want the cover from the **last 2 seconds** of the video:

**Option 1 - Use `thumb_offset` (simpler, recommended):**
```python
# If video is 30 seconds long:
thumb_offset = (30 - 2) * 1000  # = 28000 milliseconds
```

**Option 2 - Use `cover_url` (if you need a specific processed image):**
Extract a frame using ffmpeg, upload to a public URL, then pass that URL as `cover_url`.

### Facebook Reels - Limited Support

Facebook's `video_reels` endpoint does **NOT** reliably support `thumb_offset` or `cover_url` parameters during the finish phase. Options:

1. **Post-publish thumbnail:** After publishing, set a custom thumbnail via:
   ```
   POST https://graph.facebook.com/v25.0/{video-id}/thumbnails
   ```
   With `source` (image file) and `is_preferred=true`

2. **Encode the desired frame** into the video file's metadata before upload

3. **Accept platform-generated thumbnail** - Facebook will auto-select a frame

---

## 7. Video Format Requirements <a name="video-format"></a>

### Instagram Reels Specifications

| Property | Requirement |
|----------|-------------|
| **Format** | MP4 (preferred) or MOV |
| **Video Codec** | H.264 |
| **Audio Codec** | AAC |
| **Resolution** | 1080 x 1920 pixels (1080p vertical) |
| **Aspect Ratio** | 9:16 (vertical) |
| **Frame Rate** | 30 FPS standard; 60 FPS supported |
| **Max File Size** | 4 GB (API), 1 GB practical recommendation |
| **Duration** | 3 seconds to 15 minutes (uploaded files) |
| **Bitrate** | 3,500 kbps or higher recommended |

### Facebook Reels Specifications

| Property | Requirement |
|----------|-------------|
| **Format** | MP4 |
| **Aspect Ratio** | 9:16 (vertical) |
| **Duration** | 3 to 90 seconds (for Reels tab eligibility) |
| **Resolution** | 1080 x 1920 recommended |
| **Codec** | H.264 |

### Cover Image Specifications (Instagram)

| Property | Requirement |
|----------|-------------|
| **Format** | JPEG |
| **Max Size** | 8 MB |
| **Aspect Ratio** | 9:16 recommended |
| **Color Space** | sRGB |

---

## 8. Rate Limits & Quotas <a name="rate-limits"></a>

| Platform | Limit | Window | Notes |
|----------|-------|--------|-------|
| **Instagram** | 50 API-published posts | Rolling 24 hours | Check via `/{ig-user-id}/content_publishing_limit` |
| **Facebook Pages** | 25 posts per Page | Rolling 24 hours | [[general|General]] page posting limit |
| **Facebook Reels** | ~30 Reels | Rolling 24 hours | Specific to video_reels endpoint |
| **General API** | Varies by app tier | Per-app basis | HTTP 429 on throttle |

### Checking Instagram Publishing Quota

```
GET https://graph.facebook.com/v25.0/{ig-user-id}/content_publishing_limit
  ?fields=quota_usage,config
  &access_token={access-token}
```

Returns `quota_total` and current usage count.

### Error Handling

When rate-limited, the API returns HTTP 429 with error code `4` or `32`. Implement exponential backoff:
- Wait 60 seconds after first 429
- Double wait time on subsequent 429s
- Max wait: 15 minutes

---

## 9. Complete Python Implementation <a name="python-code"></a>

```python
"""
Meta Reels Publisher - Publish Reels to both Instagram and Facebook Pages
Requires: pip install requests
"""
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_VERSION = "v25.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


class MetaReelsPublisher:
    """Publish Reels to Instagram Business accounts and Facebook Pages."""

    def __init__(self, page_access_token: str):
        self.token = page_access_token
        self.page_id = None
        self.ig_user_id = None
        self._discover_accounts()

    def _discover_accounts(self):
        """Get Page ID and Instagram Business Account ID from the token."""
        url = f"{BASE_URL}/me"
        params = {
            "fields": "id,name,instagram_business_account",
            "access_token": self.token
        }
        resp = requests.get(url, params=params).json()
        self.page_id = resp.get("id")
        ig_account = resp.get("instagram_business_account", {})
        self.ig_user_id = ig_account.get("id")
        logger.info(
            "Discovered Page ID: %s, IG User ID: %s",
            self.page_id, self.ig_user_id
        )

    # ------------------------------------------------------------------ #
    #  INSTAGRAM REELS
    # ------------------------------------------------------------------ #

    def publish_instagram_reel(
        self,
        video_url: str,
        caption: str = "",
        thumb_offset_ms: int = None,
        cover_url: str = None,
        share_to_feed: bool = True,
        max_poll_seconds: int = 300,
    ) -> dict:
        """
        Publish a Reel to Instagram.

        Args:
            video_url: Public URL of the video file.
            caption: Caption text.
            thumb_offset_ms: Milliseconds from video start for cover frame.
            cover_url: Public URL of custom cover image (JPEG, max 8MB).
                       If provided, thumb_offset_ms is IGNORED by the API.
            share_to_feed: Whether to show on profile grid.
            max_poll_seconds: Max time to wait for processing.

        Returns:
            dict with 'container_id' and 'media_id'.
        """
        if not self.ig_user_id:
            raise ValueError("No Instagram Business Account linked to this Page.")

        # Step 1: Create container
        container_params = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": str(share_to_feed).lower(),
            "access_token": self.token,
        }

        if cover_url:
            container_params["cover_url"] = cover_url
        elif thumb_offset_ms is not None:
            container_params["thumb_offset"] = str(thumb_offset_ms)

        url = f"{BASE_URL}/{self.ig_user_id}/media"
        resp = requests.post(url, data=container_params)
        resp.raise_for_status()
        container_id = resp.json()["id"]
        logger.info("IG container created: %s", container_id)

        # Step 2: Poll until FINISHED
        status = self._poll_ig_container(container_id, max_poll_seconds)
        if status != "FINISHED":
            raise RuntimeError(f"Container processing failed with status: {status}")

        # Step 3: Publish
        publish_url = f"{BASE_URL}/{self.ig_user_id}/media_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": self.token,
        }
        resp = requests.post(publish_url, data=publish_params)
        resp.raise_for_status()
        media_id = resp.json()["id"]
        logger.info("IG Reel published! Media ID: %s", media_id)

        return {"container_id": container_id, "media_id": media_id}

    def _poll_ig_container(self, container_id: str, max_seconds: int) -> str:
        """Poll container status until FINISHED or timeout."""
        url = f"{BASE_URL}/{container_id}"
        params = {
            "fields": "status_code",
            "access_token": self.token,
        }
        elapsed = 0
        interval = 5
        while elapsed < max_seconds:
            resp = requests.get(url, params=params).json()
            status = resp.get("status_code", "UNKNOWN")
            logger.info("IG container status: %s (elapsed: %ds)", status, elapsed)
            if status == "FINISHED":
                return status
            if status == "ERROR":
                logger.error("Container error details: %s", resp)
                return status
            time.sleep(interval)
            elapsed += interval
        raise TimeoutError(
            f"Container {container_id} did not finish within {max_seconds}s"
        )

    # ------------------------------------------------------------------ #
    #  FACEBOOK PAGE REELS
    # ------------------------------------------------------------------ #

    def publish_facebook_reel(
        self,
        video_url: str,
        description: str = "",
        title: str = "",
    ) -> dict:
        """
        Publish a Reel to a Facebook Page using the resumable upload flow.

        Args:
            video_url: Public URL of the video file (e.g., catbox.moe link).
            description: Caption/description for the Reel.
            title: Optional title.

        Returns:
            dict with 'video_id'.
        """
        if not self.page_id:
            raise ValueError("Page ID not found.")

        reels_url = f"{BASE_URL}/{self.page_id}/video_reels"

        # Step 1: Start upload session
        start_params = {
            "upload_phase": "start",
            "access_token": self.token,
        }
        resp = requests.post(reels_url, data=start_params)
        resp.raise_for_status()
        data = resp.json()
        video_id = data["video_id"]
        upload_url = data["upload_url"]
        logger.info("FB upload session started. Video ID: %s", video_id)

        # Step 2: Upload video from public URL
        upload_headers = {
            "Authorization": f"OAuth {self.token}",
            "file_url": video_url,
        }
        resp = requests.post(upload_url, headers=upload_headers)
        resp.raise_for_status()
        logger.info("FB video uploaded from URL: %s", video_url)

        # Step 3: Finish and publish
        finish_params = {
            "upload_phase": "finish",
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "access_token": self.token,
        }
        if description:
            finish_params["description"] = description
        if title:
            finish_params["title"] = title

        resp = requests.post(reels_url, data=finish_params)
        resp.raise_for_status()
        result = resp.json()
        logger.info("FB Reel published! Response: %s", result)

        return {"video_id": video_id, "publish_response": result}

    # ------------------------------------------------------------------ #
    #  CONVENIENCE: Publish to Both Platforms
    # ------------------------------------------------------------------ #

    def publish_to_both(
        self,
        video_url: str,
        caption: str = "",
        thumb_offset_ms: int = None,
        cover_url: str = None,
    ) -> dict:
        """Publish the same Reel to both Instagram and Facebook."""
        results = {}

        # Instagram
        if self.ig_user_id:
            try:
                results["instagram"] = self.publish_instagram_reel(
                    video_url=video_url,
                    caption=caption,
                    thumb_offset_ms=thumb_offset_ms,
                    cover_url=cover_url,
                )
            except Exception as e:
                logger.error("Instagram publish failed: %s", e)
                results["instagram"] = {"error": str(e)}

        # Facebook
        if self.page_id:
            try:
                results["facebook"] = self.publish_facebook_reel(
                    video_url=video_url,
                    description=caption,
                )
            except Exception as e:
                logger.error("Facebook publish failed: %s", e)
                results["facebook"] = {"error": str(e)}

        return results


# ====================================================================== #
#  USAGE EXAMPLE
# ====================================================================== #

if __name__ == "__main__":
    # Your Page Access Token (long-lived, with required permissions)
    PAGE_TOKEN = "EAAG..."

    # Public video URL (e.g., catbox.moe)
    VIDEO_URL = "https://files.catbox.moe/xxxxxx.mp4"

    # Caption
    CAPTION = "Check out this project update! #construction #keystone"

    # For a 30-second video, set cover to frame at 28 seconds (last 2s)
    VIDEO_DURATION_SECONDS = 30
    THUMB_OFFSET = (VIDEO_DURATION_SECONDS - 2) * 1000  # 28000 ms

    publisher = MetaReelsPublisher(PAGE_TOKEN)

    # Publish to both platforms
    results = publisher.publish_to_both(
        video_url=VIDEO_URL,
        caption=CAPTION,
        thumb_offset_ms=THUMB_OFFSET,
    )

    print("Results:", results)
```

---

## 10. [[Troubleshooting|Troubleshooting]] & Common Errors <a name="troubleshooting"></a>

### Error: "The video file you selected is in a format that we don't support"
- Ensure H.264 codec in MP4 container
- Ensure AAC audio codec
- Re-encode with ffmpeg: `ffmpeg -i input.mp4 -c:v libx264 -c:a aac -ar 44100 -b:a 128k -pix_fmt yuv420p output.mp4`

### Error: "Media posted before container is ready"
- You must poll `status_code` until `FINISHED` before calling `media_publish`
- Increase poll interval if network is slow

### Error: "Invalid OAuth access token"
- Token may have expired. Exchange for a long-lived token
- Page tokens from long-lived user tokens do not expire
- Verify token at `https://graph.facebook.com/debug_token?input_token=TOKEN&access_token=TOKEN`

### Error: "The url is not properly formatted / Could not download the file"
- The video URL MUST be publicly accessible (no auth required)
- catbox.moe links are public by default -- ensure the link works in an incognito browser
- Some CDNs require specific headers; Meta's fetcher uses a standard HTTP GET

### Error: "Application does not have permission"
- Verify all required scopes are approved via App Review
- In development mode, only app admins/testers can use the API
- Use the new `instagram_business_content_publish` scope (not the deprecated `instagram_content_publish`)

### Error: `media_product_type` returns `VIDEO` instead of `REELS`
- This is normal behavior. Even content published with `media_type=REELS` may show as `VIDEO` when queried
- Use the `media_product_type` field (returns `REELS`) rather than `media_type` to distinguish

### Catbox.moe Specific Notes
- catbox.moe files are publicly accessible at `https://files.catbox.moe/{filename}`
- Files do not require authentication to download
- Ensure the file extension is `.mp4` for best compatibility
- catbox.moe files expire after a period of inactivity; for production use, consider S3 or similar persistent hosting

---

## Quick Reference: API Endpoints Summary

```
# Instagram Reels
POST  graph.facebook.com/v25.0/{ig-user-id}/media           # Create container
GET   graph.facebook.com/v25.0/{container-id}?fields=status_code  # Poll status
POST  graph.facebook.com/v25.0/{ig-user-id}/media_publish    # Publish

# Facebook Page Reels
POST  graph.facebook.com/v25.0/{page-id}/video_reels         # Start session
POST  rupload.facebook.com/video-upload/v25.0/{video-id}     # Upload file
POST  graph.facebook.com/v25.0/{page-id}/video_reels         # Finish & publish

# Token Discovery
GET   graph.facebook.com/v25.0/me/accounts?fields=name,id,access_token,instagram_business_account

# Rate Limit Check
GET   graph.facebook.com/v25.0/{ig-user-id}/content_publishing_limit?fields=quota_usage,config
```

---

## Key Takeaways for Our Implementation

1. **thumb_offset** is the simplest way to set cover from last 2 seconds: calculate `(duration_seconds - 2) * 1000` and pass as milliseconds
2. **cover_url** overrides thumb_offset if both are provided -- use one or the other
3. **Instagram and Facebook use completely different APIs** -- you need separate publish logic for each
4. **Facebook Reels do NOT support thumb_offset** -- for FB, use the `/{video-id}/thumbnails` endpoint post-publish or accept the auto-generated thumbnail
5. **Use the new permission scopes** (`instagram_business_content_publish`) -- the old ones are deprecated
6. **Poll before publishing** on Instagram -- attempting to publish before FINISHED status will fail
7. **catbox.moe URLs work** as public video URLs since they require no authentication


---
📁 **See also:** [[Research_Archives/09_Social_Media/INDEX|← Directory Index]]

**Related:** [[20260522_social_media_automation_facebook_reels_publishing_via_graph_api_video_upload_from_ur]] · [[20260522_social_media_automation_instagram_reels_programmatic_publishing_with_custom_cover_fr]]
