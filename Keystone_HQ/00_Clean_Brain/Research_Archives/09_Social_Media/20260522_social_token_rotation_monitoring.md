# Automated Social Media Token Rotation and Expiry Monitoring

## Multi-Brand [[ARCHITECTURE|Architecture]] Technical Guide

**Research Date:** May 22, 2026
**Domain:** Self-Correction / Infrastructure Hardening
**Trigger:** TikTok token expired (24h lifespan) causing publish failure; Meta token approaching 60-day limit without monitoring.

---

## 1. Platform Token Lifecycle Reference

Understanding each platform's token lifespan is the foundation of any rotation strategy.

| Platform | Access Token TTL | Refresh Token TTL | Refresh Mechanism |
|----------|-----------------|-------------------|-------------------|
| **TikTok** | 24 hours | 365 days | POST to `/v2/oauth/token/` with `grant_type=refresh_token` |
| **Meta (Facebook/Instagram)** | ~60 days (long-lived) | N/A (exchange-based) | GET `fb_exchange_token` endpoint |
| **Meta System User** | Non-expiring | N/A | Generated in Business Manager; can be rotated manually |
| **LinkedIn** | 60 days | 1 year (fixed, does NOT reset) | POST to `/oauth/v2/accessToken` with `grant_type=refresh_token` |
| **TikTok Research API** | 2 hours | 365 days | Same refresh endpoint, more frequent rotation needed |

**Critical insight:** LinkedIn's refresh token has a FIXED 1-year lifespan that does NOT reset on use. After 1 year, full re-authorization is required regardless of refresh activity.

---

## 2. Token Refresh Implementations (Python)

### 2.1 TikTok Token Refresh

TikTok's 24-hour access token is the most aggressive expiry we manage. This MUST be automated.

```python
import requests
import time
import json
from datetime import datetime, timezone

def refresh_tiktok_token(client_key: str, client_secret: str, refresh_token: str) -> dict:
    """
    Refresh TikTok access token. Must run at least every 20 hours
    to maintain a safety buffer before the 24h expiry.
    """
    url = "https://open.tiktokapis.com/v2/oauth/token/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }

    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        result = {
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),  # May rotate!
            "expires_at": datetime.now(timezone.utc).timestamp() + token_data.get("expires_in", 86400),
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
            "platform": "tiktok"
        }
        return result
    else:
        raise Exception(f"TikTok refresh failed: {response.status_code} - {response.text}")
```

**IMPORTANT:** TikTok may return a NEW refresh token alongside the new access token. Always store both -- the old refresh token may be invalidated.

### 2.2 Meta (Facebook/Instagram) Token Refresh

Meta uses a token exchange model rather than a traditional refresh token flow:

```python
def refresh_meta_token(app_id: str, app_secret: str, current_token: str,
                       api_version: str = "v21.0") -> dict:
    """
    Exchange a valid long-lived token for a fresh 60-day token.
    MUST be called BEFORE the current token expires.
    Cannot refresh an already-expired token.
    """
    url = f"https://graph.facebook.com/{api_version}/oauth/access_token"

    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": current_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "access_token": data["access_token"],
            "expires_at": datetime.now(timezone.utc).timestamp() + data.get("expires_in", 5184000),
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
            "platform": "meta"
        }
    else:
        raise Exception(f"Meta refresh failed: {response.status_code} - {response.text}")
```

**Meta System User tokens** (generated in Business Manager) are effectively non-expiring but can be invalidated if permissions change. For server-to-server automation, prefer System User tokens over Page tokens when possible.

### 2.3 LinkedIn Token Refresh

```python
def refresh_linkedin_token(client_id: str, client_secret: str,
                           refresh_token: str) -> dict:
    """
    Refresh LinkedIn access token. Access tokens last 60 days,
    refresh tokens last 1 year (FIXED - does not reset on use).
    """
    url = "https://www.linkedin.com/oauth/v2/accessToken"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),  # New refresh token
            "expires_at": datetime.now(timezone.utc).timestamp() + data.get("expires_in", 5184000),
            "refreshed_at": datetime.now(timezone.utc).isoformat(),
            "platform": "linkedin"
        }
    else:
        raise Exception(f"LinkedIn refresh failed: {response.status_code} - {response.text}")
```

---

## 3. Token Storage Architecture

### 3.1 Database Schema

```sql
CREATE TABLE social_tokens (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,           -- 'keystone_sovereign' or 'wayne_stevenson'
    platform VARCHAR(30) NOT NULL,         -- 'tiktok', 'meta', 'linkedin'
    account_identifier VARCHAR(255),       -- platform-specific account/page ID
    access_token_encrypted BYTEA NOT NULL, -- Fernet-encrypted token
    refresh_token_encrypted BYTEA,         -- Fernet-encrypted refresh token (if applicable)
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    refresh_token_expires_at TIMESTAMP WITH TIME ZONE,
    last_refreshed_at TIMESTAMP WITH TIME ZONE,
    last_health_check_at TIMESTAMP WITH TIME ZONE,
    health_status VARCHAR(20) DEFAULT 'unknown',  -- 'healthy', 'expiring_soon', 'expired', 'revoked'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(brand, platform, account_identifier)
);

CREATE INDEX idx_tokens_expiry ON social_tokens(expires_at);
CREATE INDEX idx_tokens_brand ON social_tokens(brand);
```

### 3.2 Encryption at Rest with Fernet

```python
from cryptography.fernet import Fernet
import os

class TokenVault:
    """
    Encrypts/decrypts tokens at rest using Fernet symmetric encryption.
    Encryption key MUST be stored in an environment variable, never in code.
    """

    def __init__(self):
        key = os.environ.get("TOKEN_ENCRYPTION_KEY")
        if not key:
            raise ValueError("TOKEN_ENCRYPTION_KEY environment variable not set")
        self.cipher = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> bytes:
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        return self.cipher.decrypt(ciphertext).decode()

    @staticmethod
    def generate_key() -> str:
        """Run once to generate a new encryption key."""
        return Fernet.generate_key().decode()
```

Generate a key once with `TokenVault.generate_key()` and store it in your `.env` or system environment. Add `TOKEN_ENCRYPTION_KEY` to `.gitignore` and never commit it.

---

## 4. Multi-Brand Token Isolation

For Keystone's dual-brand architecture (Keystone Sovereign + Wayne Stevenson):

### 4.1 Isolation Principles

1. **Separate OAuth apps per brand** -- Each brand should have its own registered OAuth application on each social platform. This prevents cross-brand credential leakage.
2. **Brand-scoped database queries** -- Every token query MUST include a `WHERE brand = ?` filter. Use Row-Level Security (RLS) in PostgreSQL for defense-in-depth.
3. **Separate encryption keys per brand** (ideal) -- Use `TOKEN_ENCRYPTION_KEY_KEYSTONE` and `TOKEN_ENCRYPTION_KEY_WAYNE` for maximum isolation.
4. **Namespace environment variables** -- e.g., `KEYSTONE_TIKTOK_CLIENT_KEY`, `WAYNE_TIKTOK_CLIENT_KEY`.

### 4.2 Brand-Aware Token Manager

```python
class BrandTokenManager:
    """Manages tokens with brand isolation."""

    BRANDS = ["keystone_sovereign", "wayne_stevenson"]
    PLATFORMS = ["tiktok", "meta", "linkedin"]

    def __init__(self, db_connection, vault: TokenVault):
        self.db = db_connection
        self.vault = vault

    def get_token(self, brand: str, platform: str) -> str:
        """Retrieve and decrypt the current access token for a brand+platform."""
        if brand not in self.BRANDS:
            raise ValueError(f"Unknown brand: {brand}")

        row = self.db.execute(
            "SELECT access_token_encrypted FROM social_tokens "
            "WHERE brand = %s AND platform = %s",
            (brand, platform)
        ).fetchone()

        if not row:
            raise ValueError(f"No token found for {brand}/{platform}")

        return self.vault.decrypt(row[0])

    def update_token(self, brand: str, platform: str, token_data: dict):
        """Store refreshed token data with encryption."""
        self.db.execute(
            """UPDATE social_tokens
               SET access_token_encrypted = %s,
                   refresh_token_encrypted = %s,
                   expires_at = to_timestamp(%s),
                   last_refreshed_at = NOW(),
                   health_status = 'healthy',
                   updated_at = NOW()
               WHERE brand = %s AND platform = %s""",
            (
                self.vault.encrypt(token_data["access_token"]),
                self.vault.encrypt(token_data.get("refresh_token", "")),
                token_data["expires_at"],
                brand,
                platform
            )
        )
        self.db.commit()
```

---

## 5. Token Monitoring Daemon

### 5.1 Daily Expiry Audit with APScheduler

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timezone, timedelta
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("token_monitor")

# Alert thresholds per platform (in hours)
ALERT_THRESHOLDS = {
    "tiktok": 4,       # Alert 4 hours before 24h expiry
    "meta": 168,        # Alert 7 days before 60-day expiry
    "linkedin": 168,    # Alert 7 days before 60-day expiry
}

# Proactive refresh thresholds (in hours)
REFRESH_THRESHOLDS = {
    "tiktok": 6,        # Refresh 6 hours before 24h expiry
    "meta": 336,        # Refresh 14 days before 60-day expiry
    "linkedin": 336,    # Refresh 14 days before 60-day expiry
}

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")


def send_alert(message: str, severity: str = "warning"):
    """Send alert to Slack and log it."""
    logger.warning(f"ALERT [{severity}]: {message}")

    if SLACK_WEBHOOK_URL:
        prefix = "[WARNING]" if severity == "warning" else "[CRITICAL]"
        payload = {"text": f"{prefix} *Token Monitor:* {message}"}
        try:
            requests.post(
                SLACK_WEBHOOK_URL,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")


def audit_all_tokens(db_connection):
    """
    Daily audit: Check all tokens for upcoming expiry.
    Categorizes each token as healthy, expiring_soon, or expired.
    """
    now = datetime.now(timezone.utc)
    rows = db_connection.execute(
        "SELECT brand, platform, expires_at, refresh_token_expires_at "
        "FROM social_tokens ORDER BY expires_at ASC"
    ).fetchall()

    report_lines = [f"=== Token Audit Report - {now.isoformat()} ==="]

    for row in rows:
        brand, platform, expires_at, refresh_expires_at = row
        hours_remaining = (expires_at - now).total_seconds() / 3600
        threshold = ALERT_THRESHOLDS.get(platform, 24)

        if hours_remaining <= 0:
            status = "EXPIRED"
            send_alert(
                f"{brand}/{platform} token has EXPIRED! "
                f"Manual re-auth required.",
                severity="critical"
            )
        elif hours_remaining <= threshold:
            status = "EXPIRING_SOON"
            send_alert(
                f"{brand}/{platform} token expires in "
                f"{hours_remaining:.1f} hours. Auto-refresh should handle this.",
                severity="warning"
            )
        else:
            status = "HEALTHY"

        report_lines.append(
            f"  [{status}] {brand}/{platform}: "
            f"{hours_remaining:.1f}h remaining"
        )

        # Also check refresh token expiry (especially LinkedIn's 1-year limit)
        if refresh_expires_at:
            refresh_hours = (refresh_expires_at - now).total_seconds() / 3600
            if refresh_hours <= 720:  # 30 days warning for refresh tokens
                send_alert(
                    f"{brand}/{platform} REFRESH token expires in "
                    f"{refresh_hours / 24:.0f} days. "
                    f"Full re-authorization will be needed!",
                    severity="critical"
                )

        # Update health status in DB
        db_connection.execute(
            "UPDATE social_tokens SET health_status = %s, "
            "last_health_check_at = NOW() "
            "WHERE brand = %s AND platform = %s",
            (status.lower(), brand, platform)
        )

    db_connection.commit()
    report = "\n".join(report_lines)
    logger.info(report)
    return report


def auto_refresh_expiring_tokens(db_connection, vault: TokenVault):
    """
    Proactive refresh: Automatically refresh tokens nearing expiry.
    Runs more frequently than the audit (e.g., every 2 hours).
    """
    now = datetime.now(timezone.utc)
    rows = db_connection.execute(
        "SELECT brand, platform, expires_at, refresh_token_encrypted "
        "FROM social_tokens "
        "WHERE health_status != 'revoked'"
    ).fetchall()

    for row in rows:
        brand, platform, expires_at, refresh_enc = row
        hours_remaining = (expires_at - now).total_seconds() / 3600
        threshold = REFRESH_THRESHOLDS.get(platform, 24)

        if hours_remaining <= threshold and refresh_enc:
            refresh_token = vault.decrypt(refresh_enc)
            try:
                # Dispatch to platform-specific refresh function
                if platform == "tiktok":
                    new_data = refresh_tiktok_token(
                        os.environ[f"{brand.upper()}_TIKTOK_CLIENT_KEY"],
                        os.environ[f"{brand.upper()}_TIKTOK_CLIENT_SECRET"],
                        refresh_token
                    )
                elif platform == "meta":
                    current_token = vault.decrypt(
                        db_connection.execute(
                            "SELECT access_token_encrypted FROM social_tokens "
                            "WHERE brand = %s AND platform = %s",
                            (brand, platform)
                        ).fetchone()[0]
                    )
                    new_data = refresh_meta_token(
                        os.environ[f"{brand.upper()}_META_APP_ID"],
                        os.environ[f"{brand.upper()}_META_APP_SECRET"],
                        current_token
                    )
                elif platform == "linkedin":
                    new_data = refresh_linkedin_token(
                        os.environ[f"{brand.upper()}_LINKEDIN_CLIENT_ID"],
                        os.environ[f"{brand.upper()}_LINKEDIN_CLIENT_SECRET"],
                        refresh_token
                    )
                else:
                    continue

                # Store refreshed tokens
                manager = BrandTokenManager(db_connection, vault)
                manager.update_token(brand, platform, new_data)
                logger.info(f"Auto-refreshed {brand}/{platform} token")

            except Exception as e:
                send_alert(
                    f"Auto-refresh FAILED for {brand}/{platform}: {str(e)}",
                    severity="critical"
                )
```

### 5.2 Scheduler Initialization

```python
def start_token_monitor():
    """Initialize and start the token monitoring scheduler."""

    jobstores = {
        "default": SQLAlchemyJobStore(url="sqlite:///token_jobs.sqlite")
    }

    scheduler = BackgroundScheduler(jobstores=jobstores)

    # Every 2 hours: proactive token refresh for TikTok (24h lifespan)
    scheduler.add_job(
        auto_refresh_expiring_tokens,
        "interval",
        hours=2,
        id="token_refresh",
        replace_existing=True,
        args=[db_connection, vault]
    )

    # Daily at 6 AM UTC: full audit with Slack report
    scheduler.add_job(
        audit_all_tokens,
        "cron",
        hour=6,
        minute=0,
        id="daily_audit",
        replace_existing=True,
        args=[db_connection]
    )

    scheduler.start()
    logger.info("Token monitor started.")
    return scheduler
```

---

## 6. Pre-Publish Token Health Check

This is the pattern that would have prevented tonight's TikTok failure. Before any publish operation, validate the token:

```python
from datetime import datetime, timezone

class PrePublishGuard:
    """
    Gate that validates token health BEFORE attempting any social media publish.
    Integrates into the publishing pipeline as middleware.
    """

    # Minimum remaining time (in seconds) to consider a token safe for publishing
    MIN_BUFFER_SECONDS = {
        "tiktok": 300,      # 5 minutes
        "meta": 3600,       # 1 hour
        "linkedin": 3600,   # 1 hour
    }

    def __init__(self, token_manager: BrandTokenManager, vault: TokenVault):
        self.manager = token_manager
        self.vault = vault

    def check_and_refresh(self, brand: str, platform: str) -> str:
        """
        Returns a valid access token, refreshing if necessary.
        Raises RuntimeError if token cannot be refreshed.
        """
        row = self.manager.db.execute(
            "SELECT access_token_encrypted, refresh_token_encrypted, expires_at "
            "FROM social_tokens WHERE brand = %s AND platform = %s",
            (brand, platform)
        ).fetchone()

        if not row:
            raise RuntimeError(f"No token configured for {brand}/{platform}")

        access_enc, refresh_enc, expires_at = row
        now = datetime.now(timezone.utc)
        remaining = (expires_at - now).total_seconds()
        buffer = self.MIN_BUFFER_SECONDS.get(platform, 600)

        if remaining > buffer:
            # Token is healthy -- return it
            return self.vault.decrypt(access_enc)

        # Token is expiring soon -- attempt refresh
        logger.info(f"Pre-publish refresh for {brand}/{platform} "
                     f"({remaining:.0f}s remaining)")
        try:
            # Trigger platform-specific refresh (uses functions from Section 2)
            refresh_token = self.vault.decrypt(refresh_enc) if refresh_enc else None

            if platform == "tiktok" and refresh_token:
                new_data = refresh_tiktok_token(
                    os.environ[f"{brand.upper()}_TIKTOK_CLIENT_KEY"],
                    os.environ[f"{brand.upper()}_TIKTOK_CLIENT_SECRET"],
                    refresh_token
                )
            elif platform == "meta":
                current_token = self.vault.decrypt(access_enc)
                new_data = refresh_meta_token(
                    os.environ[f"{brand.upper()}_META_APP_ID"],
                    os.environ[f"{brand.upper()}_META_APP_SECRET"],
                    current_token
                )
            elif platform == "linkedin" and refresh_token:
                new_data = refresh_linkedin_token(
                    os.environ[f"{brand.upper()}_LINKEDIN_CLIENT_ID"],
                    os.environ[f"{brand.upper()}_LINKEDIN_CLIENT_SECRET"],
                    refresh_token
                )
            else:
                raise RuntimeError(f"Cannot refresh {platform} -- no refresh token")

            self.manager.update_token(brand, platform, new_data)
            return new_data["access_token"]

        except Exception as e:
            send_alert(
                f"PRE-PUBLISH REFRESH FAILED for {brand}/{platform}: {e}",
                severity="critical"
            )
            raise RuntimeError(
                f"Token for {brand}/{platform} is expired and cannot be refreshed. "
                f"Manual re-authorization required."
            )


# Usage in the publishing pipeline:
def publish_to_social(brand: str, platform: str, content: dict):
    guard = PrePublishGuard(token_manager, vault)
    try:
        token = guard.check_and_refresh(brand, platform)
        # Now use `token` for the actual API call
        # ... platform-specific publish logic ...
    except RuntimeError as e:
        # Save content as draft, alert team
        save_as_draft(brand, platform, content)
        send_alert(str(e), severity="critical")
```

---

## 7. Graceful Re-Authentication When Refresh Tokens Expire

When a refresh token itself expires (LinkedIn after 1 year, TikTok after 365 days), or when a user revokes access, the system must handle this gracefully:

### 7.1 Detection

The API will return an `invalid_grant` error. Your code must catch this specifically:

```python
def handle_refresh_failure(brand: str, platform: str, error_response: dict):
    """
    Called when a refresh attempt returns invalid_grant.
    This means the refresh token is expired or revoked.
    """
    error_code = error_response.get("error", "")

    if error_code in ("invalid_grant", "expired_token", "revoked"):
        # 1. Mark token as revoked in DB
        db.execute(
            "UPDATE social_tokens SET health_status = 'revoked', "
            "updated_at = NOW() WHERE brand = %s AND platform = %s",
            (brand, platform)
        )
        db.commit()

        # 2. Send critical alert with re-auth instructions
        reauth_url = generate_oauth_url(brand, platform)
        send_alert(
            f"REFRESH TOKEN EXPIRED for {brand}/{platform}. "
            f"Manual re-authorization required. "
            f"Re-auth URL: {reauth_url}",
            severity="critical"
        )

        # 3. Log for audit trail
        logger.critical(
            f"Refresh token expired: {brand}/{platform}. "
            f"All scheduled publishes for this account are PAUSED."
        )
```

### 7.2 Re-Auth URL Generator

```python
OAUTH_URLS = {
    "tiktok": (
        "https://www.tiktok.com/v2/auth/authorize/"
        "?client_key={client_key}"
        "&scope=user.info.basic,video.publish"
        "&response_type=code"
        "&redirect_uri={redirect_uri}"
        "&state={state}"
    ),
    "meta": (
        "https://www.facebook.com/v21.0/dialog/oauth"
        "?client_id={app_id}"
        "&redirect_uri={redirect_uri}"
        "&scope=pages_manage_posts,pages_read_engagement"
        "&state={state}"
    ),
    "linkedin": (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        "&client_id={client_id}"
        "&redirect_uri={redirect_uri}"
        "&scope=w_member_social"
        "&state={state}"
    ),
}

def generate_oauth_url(brand: str, platform: str) -> str:
    import secrets
    state = secrets.token_urlsafe(32)
    template = OAUTH_URLS.get(platform, "")
    # Fill in brand-specific credentials from env vars
    # ... (customize per brand)
    return template
```

---

## 8. Recommended Refresh Schedule

Based on each platform's token lifespans, here is the optimal cron schedule:

```
# Token Refresh Schedule (crontab format)
# ========================================

# TikTok: Every 18 hours (24h token, 6h buffer)
0 */18 * * *  python3 /app/refresh_tokens.py --platform tiktok

# Meta: Weekly (60-day token, refresh at day 46)
0 6 * * 1     python3 /app/refresh_tokens.py --platform meta

# LinkedIn: Weekly (60-day token, refresh at day 46)
0 6 * * 3     python3 /app/refresh_tokens.py --platform linkedin

# Daily Audit (all platforms, with Slack report)
0 9 * * *     python3 /app/audit_tokens.py --all --report

# Pre-dawn health check (catch overnight failures before business hours)
30 5 * * *    python3 /app/audit_tokens.py --all --alert-only
```

For Windows (Task Scheduler), the TikTok refresh should run as a persistent service using APScheduler rather than relying on Task Scheduler's interval limits.

---

## 9. Environment Variable Template

```bash
# === Token Encryption ===
TOKEN_ENCRYPTION_KEY=your-fernet-key-here

# === Keystone Sovereign Brand ===
KEYSTONE_SOVEREIGN_TIKTOK_CLIENT_KEY=ks_tiktok_key
KEYSTONE_SOVEREIGN_TIKTOK_CLIENT_SECRET=ks_tiktok_secret
KEYSTONE_SOVEREIGN_META_APP_ID=ks_meta_app_id
KEYSTONE_SOVEREIGN_META_APP_SECRET=ks_meta_app_secret
KEYSTONE_SOVEREIGN_LINKEDIN_CLIENT_ID=ks_linkedin_id
KEYSTONE_SOVEREIGN_LINKEDIN_CLIENT_SECRET=ks_linkedin_secret

# === Wayne Stevenson Brand ===
WAYNE_STEVENSON_TIKTOK_CLIENT_KEY=ws_tiktok_key
WAYNE_STEVENSON_TIKTOK_CLIENT_SECRET=ws_tiktok_secret
WAYNE_STEVENSON_META_APP_ID=ws_meta_app_id
WAYNE_STEVENSON_META_APP_SECRET=ws_meta_app_secret
WAYNE_STEVENSON_LINKEDIN_CLIENT_ID=ws_linkedin_id
WAYNE_STEVENSON_LINKEDIN_CLIENT_SECRET=ws_linkedin_secret

# === Alerting ===
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# === Database ===
TOKEN_DB_URL=postgresql://user:pass@localhost:5432/keystone_tokens
```

---

## 10. Implementation Checklist

### Immediate (Tonight's Fix)
- [ ] Implement TikTok refresh function and test manually
- [ ] Store current tokens in encrypted database
- [ ] Set up APScheduler with 18-hour TikTok refresh cycle
- [ ] Add pre-publish guard to publishing pipeline

### This Week
- [ ] Implement Meta token refresh with 46-day proactive window
- [ ] Implement LinkedIn token refresh
- [ ] Set up Slack alerting webhook
- [ ] Deploy daily audit cron job
- [ ] Add refresh token expiry monitoring (LinkedIn 1-year cliff)

### This Month
- [ ] Migrate token storage to PostgreSQL with RLS
- [ ] Implement per-brand encryption key isolation
- [ ] Build re-auth URL generator and notification flow
- [ ] Add draft-saving for failed publishes
- [ ] Create admin dashboard for token health visibility
- [ ] Document OAuth app credentials for each brand/platform

---

## Sources Consulted

- TikTok Developer Documentation -- Token management and refresh endpoints
- Meta Graph API Documentation -- Long-lived token exchange, System User tokens
- LinkedIn OAuth 2.0 Documentation -- Refresh token lifecycle (1-year fixed)
- OAuth 2.0 RFC 6749 -- Standard refresh token flow
- APScheduler Documentation -- BackgroundScheduler and persistent job stores
- Cryptography (Python) -- Fernet symmetric encryption
- OWASP Token Security Guidelines -- Storage and rotation best practices
- Various Stack Overflow threads and developer blog posts on social media token management (2024-2025)


---
📁 **See also:** [[Research_Archives/09_Social_Media/INDEX|← Directory Index]]

**Related:** [[20260522_social_media_automation_multi-brand_social_media_token_management_and_automatic_refr]] · [[20260522_security_hardening_api_key_and_oauth_token_rotation_and_secure_storage]]
