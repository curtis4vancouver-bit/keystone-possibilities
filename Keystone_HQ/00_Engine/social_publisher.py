# Keystone Sovereign - Multi-Platform Social Publisher & Scheduler
# Integrates with LinkedIn, Meta (Facebook & Instagram), and TikTok APIs.
# Enforces strict YMYL compliance checks via sovereign_coordinator.py.
# Manages a 2-week content queue to stage posts and avoid overlaps.

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import argparse
from datetime import datetime, timedelta

# Reconfigure stdout to use UTF-8 to prevent Windows console encoding crashes with emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
TOKENS_FILE = os.path.join(ROOT_DIR, "social_tokens.json")
QUEUE_FILE = os.path.join(ROOT_DIR, "content_queue.json")

# Import the master sovereign coordinator for YMYL scrubbing
sys.path.append(ROOT_DIR)
try:
    from sovereign_coordinator import KeystoneSovereign
    sovereign = KeystoneSovereign()
except ImportError:
    sovereign = None
    print("Warning: sovereign_coordinator.py not imported. YMYL compliance scrubbing will run locally.")

# Import the GCS video hosting bridge for TikTok/Instagram local file uploads
try:
    from video_hosting_bridge import upload_to_gcs
    GCS_BRIDGE_AVAILABLE = True
except ImportError:
    GCS_BRIDGE_AVAILABLE = False

# Channel routing map — which YouTube channel each brand uploads to
# CRITICAL: Must match youtube_mcp.py CHANNEL_TOKEN_MAP
BRAND_CHANNEL_MAP = {
    "possibilities": "possibilities",    # Construction content
    "recomposition": "recomposition",    # Health/wellness content (OAC Brand Account)
    "protocol": "recomposition",         # Protocol content now routes to Recomposition channel!
}

class SocialPublisher:
    def __init__(self):
        self.tokens = self._load_tokens()
        self.queue = self._load_queue()

    def _load_tokens(self) -> dict:
        if os.path.exists(TOKENS_FILE):
            try:
                with open(TOKENS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error reading tokens file: {str(e)}")
        return {}

    def _load_queue(self) -> list:
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_queue(self):
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, indent=4, ensure_ascii=False)

    def _save_tokens(self):
        """Persists the current token state back to social_tokens.json."""
        with open(TOKENS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tokens, f, indent=4, ensure_ascii=False)

    def _auto_refresh_tiktok(self):
        """Automatically refreshes the TikTok access token if expired (24hr lifespan).
        Uses the long-lived refresh_token (~1 year) to obtain a new access_token."""
        tiktok = self.tokens.get("recomposition", {}).get("tiktok", {})
        if not tiktok.get("refresh_token"):
            return  # No refresh token available

        acquired_at = tiktok.get("acquired_at", 0)
        expires_in = tiktok.get("expires_in", 86400)
        age_seconds = time.time() - acquired_at

        # Refresh if token has less than 1 hour of life remaining
        if age_seconds < (expires_in - 3600):
            return  # Token still valid

        print("  TikTok token expired or expiring soon. Auto-refreshing...")
        try:
            url = "https://open.tiktokapis.com/v2/oauth/token/"
            payload = {
                "client_key": tiktok["client_key"],
                "client_secret": tiktok["client_secret"],
                "grant_type": "refresh_token",
                "refresh_token": tiktok["refresh_token"]
            }
            data = urllib.parse.urlencode(payload).encode("utf-8")
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "KeystoneApp/2.0"}
            )
            with urllib.request.urlopen(req) as res:
                resp = json.loads(res.read().decode("utf-8"))

            if "access_token" in resp:
                tiktok["access_token"] = resp["access_token"]
                tiktok["refresh_token"] = resp.get("refresh_token", tiktok["refresh_token"])
                tiktok["expires_in"] = resp.get("expires_in", 86400)
                tiktok["refresh_expires_in"] = resp.get("refresh_expires_in", 31536000)
                tiktok["acquired_at"] = int(time.time())
                self.tokens["recomposition"]["tiktok"] = tiktok
                self._save_tokens()
                print("  TikTok token refreshed successfully.")
            else:
                print(f"  WARNING: TikTok refresh failed: {resp}")
        except Exception as e:
            print(f"  WARNING: TikTok auto-refresh error: {str(e)}")

    def scrub_text(self, text: str) -> str:
        """Enforces YMYL scrubbing on outgoing copy."""
        if sovereign:
            return sovereign.run_ymyl_compliance_check(text)
        
        # Local fallback scrubber
        scrubbed = text
        local_dict = {
            r"\bprotocol\b": "case study",
            r"\bprotocols\b": "case studies",
            r"\bdosing\b": "titration schedule",
            r"\bdoses\b": "titration schedules",
            r"\bstack\b": "combinatorial model"
        }
        import re
        for pattern, replacement in local_dict.items():
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        return scrubbed

    def api_post_json(self, url: str, payload: dict, headers: dict) -> dict:
        """Utility method to make a POST request with JSON payload."""
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={**headers, "Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise Exception(f"HTTP {e.code}: {e.reason} - {err_body}")

    def api_get_json(self, url: str, headers: dict) -> dict:
        """Utility method to make a GET request."""
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise Exception(f"HTTP {e.code}: {e.reason} - {err_body}")

    # ── GCS Auto-Upload Helper ────────────────────────────────────────

    def _ensure_public_url(self, media_path_or_url: str) -> str:
        """If the input is a local file path, uploads it to GCS and returns a public URL.
        If already a URL (http/https), returns as-is."""
        if not media_path_or_url:
            return media_path_or_url

        # Already a URL — pass through
        if media_path_or_url.startswith("http://") or media_path_or_url.startswith("https://"):
            return media_path_or_url

        # It's a local file path — upload to GCS
        if not os.path.exists(media_path_or_url):
            raise FileNotFoundError(f"Local media file not found: {media_path_or_url}")

        if not GCS_BRIDGE_AVAILABLE:
            raise ImportError(
                "video_hosting_bridge.py not available. "
                "Cannot auto-upload local files to GCS for TikTok/Instagram. "
                "Install google-cloud-storage and ensure video_hosting_bridge.py exists."
            )

        print(f"  Auto-uploading local file to GCS: {os.path.basename(media_path_or_url)}")
        public_url = upload_to_gcs(media_path_or_url)
        print(f"  GCS URL ready: {public_url[:80]}...")
        return public_url

    # ── Platform Publishing Implementations ──────────────────────────

    def publish_to_linkedin(self, brand: str, text: str, dry_run: bool = False) -> str:
        """Publishes optimized update to LinkedIn feed using w_member_social scope."""
        # Fallback to recomposition if brand is protocol (shares recomposition LinkedIn)
        auth_brand = "recomposition" if brand == "protocol" and "linkedin" not in self.tokens.get(brand, {}) else brand
        token_info = self.tokens.get(auth_brand, {}).get("linkedin", {})
        access_token = token_info.get("access_token")
        if not access_token:
            return f"Error: No LinkedIn credentials for brand '{brand}'."

        scrubbed_text = self.scrub_text(text)
        
        if dry_run:
            return f"[Dry-Run] LinkedIn Post to brand '{brand}': '{scrubbed_text}'"

        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 1. Fetch member URN via modern OIDC userinfo endpoint
        try:
            user_info = self.api_get_json("https://api.linkedin.com/v2/userinfo", headers)
            sub = user_info.get("sub")
        except Exception:
            # Fallback to legacy /me endpoint
            try:
                me_info = self.api_get_json("https://api.linkedin.com/v2/me", headers)
                sub = me_info.get("id")
            except Exception as e:
                return f"LinkedIn Auth Failure: Could not retrieve user URN profile ({str(e)})."

        if not sub:
            return "LinkedIn Profile URN empty."

        author_urn = f"urn:li:person:{sub}"

        # 2. Construct and publish UGC post
        post_url = "https://api.linkedin.com/v2/posts"
        payload = {
            "author": author_urn,
            "commentary": scrubbed_text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED"
            },
            "lifecycleState": "PUBLISHED"
        }

        try:
            self.api_post_json(post_url, payload, headers)
            return f"Success: Published update to LinkedIn feed for URN {author_urn}."
        except Exception as e:
            return f"LinkedIn Publishing Failed: {str(e)}"

    def publish_to_meta_facebook(self, brand: str, text: str, media_url: str = None, dry_run: bool = False) -> str:
        """Publishes update (text or video) to connected Meta Facebook Page."""
        # Fallback to recomposition if brand is protocol (shares recomposition Meta)
        auth_brand = "recomposition" if brand == "protocol" and "meta" not in self.tokens.get(brand, {}) else brand
        token_info = self.tokens.get(auth_brand, {}).get("meta", {})
        user_access_token = token_info.get("user_access_token")
        
        scrubbed_text = self.scrub_text(text)
        target_page_id = "898671469990393" if brand in ["recomposition", "protocol"] else "166025896601563"

        if dry_run:
            if media_url:
                return f"[Dry-Run] Facebook Video Post to brand '{brand}' (Video: {media_url}): '{scrubbed_text}'"
            return f"[Dry-Run] Facebook Post to brand '{brand}': '{scrubbed_text}'"

        # ── n8n Webhook Router Integration ──
        n8n_webhook_url = "http://localhost:5678/webhook/publish-facebook"
        try:
            n8n_payload = {
                "brand": brand,
                "text": scrubbed_text,
                "media_url": media_url
            }
            n8n_req = urllib.request.Request(
                n8n_webhook_url,
                data=json.dumps(n8n_payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(n8n_req, timeout=5) as n8n_res:
                n8n_resp = json.loads(n8n_res.read().decode("utf-8"))
                return f"Success: Published to Facebook (routed via n8n). Response: {n8n_resp}"
        except Exception as n8n_err:
            print(f"[SocialPublisher] n8n routing unavailable or failed ({n8n_err}). Falling back to standard API...")

        # Check if we should directly trigger fallback
        if not user_access_token or token_info.get("app_id") == "1004714315742024":
            # API is hard-locked, directly trigger browser fallback
            fallback_payload = {
                "text": scrubbed_text,
                "media_path": media_url,
                "brand": brand,
                "platform": "facebook",
                "page_id": target_page_id,
                "business_id": "1512692486433786"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # 1. Retrieve connected Facebook Pages
        headers = {}
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
        pages = []
        try:
            pages_data = self.api_get_json(pages_url, headers)
            pages = pages_data.get("data", [])
        except Exception as e:
            # If the initial call fails due to invalid/suspended tokens, trigger fallback
            fallback_payload = {
                "text": scrubbed_text,
                "media_path": media_url,
                "brand": brand,
                "platform": "facebook",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"API pages retrieval failed: {str(e)}"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # Select target page with strict entity isolation
        selected_page = next((p for p in pages if p["id"] == target_page_id), None)
        if not selected_page:
            # Direct query fallback (vital for business login returning empty me/accounts)
            direct_url = f"https://graph.facebook.com/v20.0/{target_page_id}?fields=name,access_token&access_token={user_access_token}"
            try:
                page_data = self.api_get_json(direct_url, headers)
                if "access_token" in page_data:
                    selected_page = {
                        "id": target_page_id,
                        "name": page_data.get("name", f"Facebook Page {target_page_id}"),
                        "access_token": page_data["access_token"]
                    }
            except Exception:
                pass

        if not selected_page and pages:
            # Fallback by name match
            if brand in ["recomposition", "protocol"]:
                selected_page = next((p for p in pages if "recomposition" in p.get("name", "").lower()), None)
            else:
                selected_page = next((p for p in pages if "possibilities" in p.get("name", "").lower()), None)

        if not selected_page:
            fallback_payload = {
                "text": scrubbed_text,
                "media_path": media_url,
                "brand": brand,
                "platform": "facebook",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"Page ID {target_page_id} not found in accessible pages."
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        page_id = selected_page["id"]
        page_token = selected_page["access_token"]
        page_name = selected_page["name"]

        is_video = False
        if media_url:
            is_video = any(media_url.lower().split('?')[0].endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"])
            # Auto-upload local files to GCS
            try:
                media_url = self._ensure_public_url(media_url)
            except Exception as e:
                return f"Facebook GCS Upload Error: {str(e)}"

        # 2. Publish to page feed / videos
        if media_url and is_video:
            # Upload video
            video_url = f"https://graph.facebook.com/v20.0/{page_id}/videos"
            payload_dict = {
                "description": scrubbed_text,
                "file_url": media_url,
                "access_token": page_token
            }
            data = urllib.parse.urlencode(payload_dict).encode("utf-8")
            req = urllib.request.Request(video_url, data=data, headers={"User-Agent": "KeystoneApp/2.0"})
            try:
                with urllib.request.urlopen(req) as res:
                    result = json.loads(res.read().decode("utf-8"))
                return f"Success: Published video to Facebook Page '{page_name}' (Video ID: {result.get('id')})."
            except Exception as e:
                # Trigger fallback on publishing failure
                fallback_payload = {
                    "text": scrubbed_text,
                    "media_path": media_url,
                    "brand": brand,
                    "platform": "facebook",
                    "page_id": target_page_id,
                    "business_id": "1512692486433786",
                    "reason": f"Video upload failed: {str(e)}"
                }
                return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"
        else:
            # Publish standard text feed post
            feed_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
            payload_dict = {
                "message": scrubbed_text,
                "access_token": page_token
            }
            data = urllib.parse.urlencode(payload_dict).encode("utf-8")
            req = urllib.request.Request(feed_url, data=data, headers={"User-Agent": "KeystoneApp/2.0"})
            try:
                with urllib.request.urlopen(req) as res:
                    result = json.loads(res.read().decode("utf-8"))
                return f"Success: Published update to Facebook Page '{page_name}' (ID: {result.get('id')})."
            except Exception as e:
                # Trigger fallback on publishing failure
                fallback_payload = {
                    "text": scrubbed_text,
                    "media_path": media_url,
                    "brand": brand,
                    "platform": "facebook",
                    "page_id": target_page_id,
                    "business_id": "1512692486433786",
                    "reason": f"Feed post failed: {str(e)}"
                }
                return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

    def publish_to_meta_instagram(self, brand: str, caption: str, image_url: str = None, dry_run: bool = False) -> str:
        """Prepares and posts caption/photo/video to Instagram Business Account."""
        # Fallback to recomposition if brand is protocol (shares recomposition Meta)
        auth_brand = "recomposition" if brand == "protocol" and "meta" not in self.tokens.get(brand, {}) else brand
        token_info = self.tokens.get(auth_brand, {}).get("meta", {})
        user_access_token = token_info.get("user_access_token")
        
        scrubbed_caption = self.scrub_text(caption)
        target_page_id = "898671469990393" if brand in ["recomposition", "protocol"] else "166025896601563"

        if dry_run:
            is_video = any(image_url.lower().split('?')[0].endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"]) if image_url else False
            media_type = "Video (Reels)" if is_video else "Image"
            return f"[Dry-Run] Instagram Post to brand '{brand}' ({media_type}: {image_url}): '{scrubbed_caption}'"

        # Check if we should directly trigger fallback
        if not user_access_token or token_info.get("app_id") == "1004714315742024":
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # 1. Fetch page details to resolve Instagram Business Account ID
        pages = []
        try:
            pages_data = self.api_get_json(f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}", {})
            pages = pages_data.get("data", [])
        except Exception as e:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"API pages retrieval failed: {str(e)}"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # Select target page with strict entity isolation
        selected_page = next((p for p in pages if p["id"] == target_page_id), None)
        if not selected_page:
            # Direct query fallback (vital for business login returning empty me/accounts)
            direct_url = f"https://graph.facebook.com/v20.0/{target_page_id}?fields=name,access_token&access_token={user_access_token}"
            try:
                page_data = self.api_get_json(direct_url, {})
                if "access_token" in page_data:
                    selected_page = {
                        "id": target_page_id,
                        "name": page_data.get("name", f"Facebook Page {target_page_id}"),
                        "access_token": page_data["access_token"]
                    }
            except Exception:
                pass

        if not selected_page and pages:
            # Fallback by name match
            if brand in ["recomposition", "protocol"]:
                selected_page = next((p for p in pages if "recomposition" in p.get("name", "").lower()), None)
            else:
                selected_page = next((p for p in pages if "possibilities" in p.get("name", "").lower()), None)

        if not selected_page:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"Page ID {target_page_id} not found in accessible pages."
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        page_id = selected_page["id"]
        page_token = selected_page["access_token"]

        # 2. Get instagram business account link
        try:
            ig_data = self.api_get_json(f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}", {})
            ig_account = ig_data.get("instagram_business_account", {})
            ig_id = ig_account.get("id")
        except Exception as e:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"Instagram link verification failed: {str(e)}"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        if not ig_id:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": "No linked Instagram Business Account found."
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        if not image_url:
            return f"Instagram Posting Bypass: Instagram requires a public media URL. Staged caption: '{scrubbed_caption}'"

        is_video = any(image_url.lower().split('?')[0].endswith(ext) for ext in [".mp4", ".mov", ".avi", ".mkv", ".webm"])

        # Auto-upload local files to GCS
        try:
            image_url = self._ensure_public_url(image_url)
        except Exception as e:
            return f"Instagram GCS Upload Error: {str(e)}"

        # 3. Create media container
        container_url = f"https://graph.facebook.com/v20.0/{ig_id}/media"
        if is_video:
            container_payload = {
                "media_type": "REELS",
                "video_url": image_url,
                "caption": scrubbed_caption,
                "access_token": page_token
            }
        else:
            container_payload = {
                "image_url": image_url,
                "caption": scrubbed_caption,
                "access_token": page_token
            }
        
        try:
            container_res = self.api_post_json(container_url, container_payload, {})
            creation_id = container_res.get("id")
        except Exception as e:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"Media container creation failed: {str(e)}"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # If video, we must poll until the video is processed
        if is_video:
            print(f"  Instagram Video uploaded (Container: {creation_id}). Waiting for processing...")
            max_attempts = 15
            for attempt in range(max_attempts):
                time.sleep(10)
                try:
                    status_url = f"https://graph.facebook.com/v20.0/{creation_id}?fields=status_code,status&access_token={user_access_token}"
                    status_res = self.api_get_json(status_url, {})
                    status_code = status_res.get("status_code")
                    print(f"    Processing status: {status_code}")
                    if status_code == "FINISHED":
                        break
                    elif status_code == "ERROR":
                        fallback_payload = {
                            "text": scrubbed_caption,
                            "media_path": image_url,
                            "brand": brand,
                            "platform": "instagram",
                            "page_id": target_page_id,
                            "business_id": "1512692486433786",
                            "reason": f"Video processing error: {status_res.get('status')}"
                        }
                        return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"
                except Exception as e:
                    print(f"    Error checking status: {str(e)}")
            else:
                fallback_payload = {
                    "text": scrubbed_caption,
                    "media_path": image_url,
                    "brand": brand,
                    "platform": "instagram",
                    "page_id": target_page_id,
                    "business_id": "1512692486433786",
                    "reason": "Video processing timed out."
                }
                return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

        # 4. Publish media container
        publish_url = f"https://graph.facebook.com/v20.0/{ig_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": page_token
        }

        try:
            publish_res = self.api_post_json(publish_url, publish_payload, {})
            media_label = "Reels Video" if is_video else "Picture"
            return f"Success: Published {media_label} to Instagram Business Feed (Post ID: {publish_res.get('id')})."
        except Exception as e:
            fallback_payload = {
                "text": scrubbed_caption,
                "media_path": image_url,
                "brand": brand,
                "platform": "instagram",
                "page_id": target_page_id,
                "business_id": "1512692486433786",
                "reason": f"Media publish confirmation failed: {str(e)}"
            }
            return f"BROWSER_AUTOMATION_FALLBACK_REQUIRED: {json.dumps(fallback_payload)}"

    def publish_to_tiktok(self, brand: str, title: str, video_url: str = None, dry_run: bool = False, cover_timestamp_ms: int = 1000) -> str:
        """Publishes Short video to TikTok Business Feed using Content Posting API."""
        # Auto-refresh TikTok token if expired (24hr lifespan)
        self._auto_refresh_tiktok()

        # Fallback to recomposition if brand is protocol or possibilities (TikTok is shared under curtis4van)
        auth_brand = brand
        if brand in ["protocol", "possibilities"] and "tiktok" not in self.tokens.get(brand, {}):
            auth_brand = "recomposition"
            
        token_info = self.tokens.get(auth_brand, {}).get("tiktok", {})
        access_token = token_info.get("access_token")
        if not access_token:
            return f"Error: No TikTok credentials for brand '{brand}'."

        scrubbed_title = self.scrub_text(title)

        if not video_url:
            return f"TikTok Posting Bypass: TikTok requires a public MP4 video URL. Staged caption: '{scrubbed_title}'"

        # Auto-upload local files to GCS
        try:
            video_url = self._ensure_public_url(video_url)
        except Exception as e:
            return f"TikTok GCS Upload Error: {str(e)}"

        if dry_run:
            return f"[Dry-Run] TikTok Post to brand '{brand}' (Video: {video_url}): '{scrubbed_title}'"

        # 1. Initialize video upload request (direct fetch method)
        init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "post_info": {
                "title": scrubbed_title,
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "video_cover_timestamp_ms": cover_timestamp_ms
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url
            }
        }

        try:
            res = self.api_post_json(init_url, payload, headers)
            publish_id = res.get("data", {}).get("publish_id")
            return f"Success: Queued TikTok Video upload. TikTok Publish Transaction ID: {publish_id}"
        except Exception as e:
            return f"TikTok Video Initialization Failed: {str(e)}"

    # ── Scheduling & Queue Management (2-Week Batches) ──────────────────

    def enqueue_post(self, brand: str, platforms: list, content: str, title: str = "", media_url: str = "", delay_days: int = 0):
        """Enqueues a post in the local 2-week staging queue."""
        publish_time = datetime.now() + timedelta(days=delay_days)
        
        post_entry = {
            "id": len(self.queue) + 1,
            "brand": brand,
            "platforms": platforms, # List e.g. ["linkedin", "facebook", "instagram", "tiktok"]
            "title": title,
            "content": content,
            "media_url": media_url,
            "scheduled_time": publish_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Queued",
            "published_at": None,
            "logs": []
        }
        
        self.queue.append(post_entry)
        self._save_queue()
        print(f"📥 Enqueued new B2B post {post_entry['id']} for brand '{brand}' on {post_entry['scheduled_time']}.")

    def process_due_posts(self, dry_run: bool = False):
        """Checks the queue and fires all posts whose scheduled time is in the past."""
        now = datetime.now()
        due_posts = []
        
        for post in self.queue:
            if post["status"] == "Queued":
                sched_time = datetime.strptime(post["scheduled_time"], "%Y-%m-%d %H:%M:%S")
                if sched_time <= now:
                    due_posts.append(post)

        if not due_posts:
            print("📅 Staging Queue Check: No scheduled posts are currently due for release.")
            return

        print(f"🚀 Found {len(due_posts)} due posts. Initiating multi-platform distribution...")
        
        for post in due_posts:
            print(f"\n[Processing Post ID {post['id']}] Brand: {post['brand']}")
            post["status"] = "Processing"
            self._save_queue()
            
            success_platforms = []
            
            for platform in post["platforms"]:
                print(f" -> Publishing to {platform.upper()}...")
                log_msg = ""
                
                try:
                    if platform == "linkedin":
                        log_msg = self.publish_to_linkedin(post["brand"], post["content"], dry_run)
                    elif platform == "facebook":
                        log_msg = self.publish_to_meta_facebook(post["brand"], post["content"], post["media_url"], dry_run)
                    elif platform == "instagram":
                        log_msg = self.publish_to_meta_instagram(post["brand"], post["content"], post["media_url"], dry_run)
                    elif platform == "tiktok":
                        log_msg = self.publish_to_tiktok(post["brand"], post["title"] or post["content"][:50], post["media_url"], dry_run)
                    else:
                        log_msg = f"Skipped: Unsupported platform '{platform}'."
                except Exception as ex:
                    log_msg = f"Error: {str(ex)}"
                
                print(f"    Result: {log_msg}")
                post["logs"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "platform": platform,
                    "log": log_msg
                })
                
                if "Success" in log_msg or "[Dry-Run]" in log_msg or "Instagram Posting Bypass" in log_msg or "TikTok Posting Bypass" in log_msg:
                    success_platforms.append(platform)

            # Update final status
            if len(success_platforms) == len(post["platforms"]):
                post["status"] = "Published"
                post["published_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                post["status"] = "Partially Published" if success_platforms else "Failed"
            
            self._save_queue()
            
        print("\nDistribution sprint complete.\n")

    def get_token_status(self) -> dict:
        """Returns status of all social media tokens across all brands."""
        status = {}
        for brand in ["possibilities", "recomposition", "protocol"]:
            brand_status = {}
            for platform in ["linkedin", "meta", "tiktok"]:
                # Check direct credentials first
                token_info = self.tokens.get(brand, {}).get(platform, {})
                is_fallback = False
                fallback_from = ""
                
                # Check for inherited/fallback tokens
                if not (token_info.get("access_token") or token_info.get("user_access_token")):
                    if brand == "protocol" and platform in ["linkedin", "meta", "tiktok"]:
                        token_info = self.tokens.get("recomposition", {}).get(platform, {})
                        is_fallback = True
                        fallback_from = "recomposition"
                    elif brand == "possibilities" and platform == "tiktok":
                        token_info = self.tokens.get("recomposition", {}).get(platform, {})
                        is_fallback = True
                        fallback_from = "recomposition"
                
                if token_info.get("access_token") or token_info.get("user_access_token"):
                    acquired = token_info.get("acquired_at", 0)
                    expires_in = token_info.get("expires_in", 0)
                    age_hours = (time.time() - acquired) / 3600 if acquired else 0
                    expires_hours = (expires_in / 3600) - age_hours if expires_in else 0
                    brand_status[platform] = {
                        "connected": True,
                        "expires_in_hours": round(max(0, expires_hours), 1),
                        "inherited": is_fallback,
                        "shared_from": fallback_from
                    }
                else:
                    brand_status[platform] = {"connected": False, "expires_in_hours": 0, "inherited": False, "shared_from": ""}
            status[brand] = brand_status
        return status

    def print_queue_report(self):
        """Prints a detailed status report of the content schedule."""
        print("\n" + "="*80)
        print("                 KEYSTONE 2-WEEK SOCIAL CONTENT QUEUE")
        print("="*80)
        if not self.queue:
            print("  Staging Queue is currently empty.")
        else:
            for post in self.queue:
                print(f"Post ID {post['id']}: [{post['status']}] Brand: {post['brand'].upper()}")
                print(f"   Platforms: {', '.join(post['platforms']).upper()}")
                print(f"   Schedule:  {post['scheduled_time']}")
                print(f"   Draft:     \"{post['content'][:70]}...\"")
                if post["media_url"]:
                    print(f"   Media:     {post['media_url']}")
                if post["published_at"]:
                    print(f"   Released:  {post['published_at']}")
                if post["logs"]:
                    print("   Logs:")
                    for log in post["logs"]:
                        print(f"     • [{log['platform'].upper()}] {log['log']}")
                print("-"*80)
        print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keystone Social Media Posting & Queue Engine")
    parser.add_argument("--status", action="store_true", help="Print the 2-week content queue status report")
    parser.add_argument("--process", action="store_true", help="Process and distribute all due posts")
    parser.add_argument("--dry-run", action="store_true", help="Perform publishing checks in dry-run simulation mode")
    parser.add_argument("--enqueue", action="store_true", help="Enqueue a new post in the staging area")
    
    # Staging parameters
    parser.add_argument("--brand", type=str, choices=["possibilities", "recomposition", "protocol"], default="possibilities")
    parser.add_argument("--platforms", type=str, default="linkedin,facebook,instagram", help="Comma-separated platforms")
    parser.add_argument("--content", type=str, help="Text caption or post body")
    parser.add_argument("--title", type=str, default="", help="TikTok video title/hook")
    parser.add_argument("--media-url", type=str, default="", help="Public URL for photos/videos")
    parser.add_argument("--delay-days", type=int, default=0, help="Days to delay scheduling from now")

    args = parser.parse_args()
    publisher = SocialPublisher()
    
    if args.status:
        publisher.print_queue_report()
    elif args.process:
        publisher.process_due_posts(args.dry-run if hasattr(args, "dry-run") else args.dry_run)
    elif args.enqueue:
        if not args.content:
            print("Error: Post content required using --content.")
            sys.exit(1)
            
        p_list = [p.strip().lower() for p in args.platforms.split(",")]
        publisher.enqueue_post(
            brand=args.brand,
            platforms=p_list,
            content=args.content,
            title=args.title,
            media_url=args.media_url,
            delay_days=args.delay_days
        )
    else:
        publisher.print_queue_report()
