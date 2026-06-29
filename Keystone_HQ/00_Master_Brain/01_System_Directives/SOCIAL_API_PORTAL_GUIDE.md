# Keystone Empire: Social Media API Portal Setup Guide

To automate posting to LinkedIn, Facebook, Instagram, and TikTok, we need client credentials (Client ID / Client Secret / Client Key) from each platform's developer portal. These keys allow our local orchestration scripts to authorize content publishing without paying third-party SaaS fees.

This guide walks you through setting up developer apps on each portal and registering the local callback URI: `http://localhost:8080/callback`.

---

## 1. LinkedIn Developer Portal (Personal & Company Page)

### Steps to get Credentials:
1. Go to the [LinkedIn Developer Portal](https://developer.linkedin.com/).
2. Log in with your LinkedIn account and click **Create App** in the top right.
3. Fill out the application details:
   - **App Name:** `Keystone Content Engine`
   - **LinkedIn Page:** Search and link your Keystone Possibilities company page (you must be an admin of this page to link it).
   - **App Logo:** Upload a high-resolution logo (use the gold/charcoal Keystone asset).
4. Go to the **Auth** tab:
   - Under **Authorized Redirect URLs**, add: `http://localhost:8080/callback`
   - Copy your **Client ID** and **Client Secret**.
5. Go to the **Products** tab and request access to:
   - **Share on LinkedIn** (Provides personal feed publishing via `w_member_social`).
   - **Community Management API** (Provides company page publishing via `w_organization_social`). *Note: Organization access requires a brief approval review.*

---

## 2. Meta Developer Portal (Facebook Pages & Instagram Business)

To post to Instagram, you must have an **Instagram Business Account** connected to a **Facebook Page** under your control.

### Steps to get Credentials:
1. Go to the [Meta Developer Portal](https://developers.facebook.com/).
2. Log in and click **Create App** in the top right.
3. Select **Other** as the app type, then click **Next**.
4. Select **Business** or **Consumer** (select **Business** for full Page/Instagram integrations) and click **Next**.
5. Name your app (e.g., `Keystone Automator`), connect your Business Portfolio (if applicable), and click **Create App**.
6. In the App Dashboard left sidebar, click **Add Product** and select **Facebook Login for Business** (or standard **Facebook Login**).
7. Go to **Settings** under the login product:
   - Set **Valid OAuth Redirect URIs** to: `http://localhost:8080/callback`
   - Set **Login with the JavaScript SDK** to `Yes`.
8. Go to the main **App Settings -> Basic** tab:
   - Copy your **App ID** (Client ID) and **App Secret** (Client Secret).
9. During the OAuth login, you will request the following permissions:
   - `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`

---

## 3. TikTok Developer Portal (YouTube Shorts & TikTok Posting)

### Steps to get Credentials:
1. Go to the [TikTok for Developers Portal](https://developers.tiktok.com/).
2. Log in with your TikTok account.
3. Click **My Apps** in the top navigation, and click **Create App**.
4. Select **Web App** as the platform type.
5. Fill out the app form:
   - **App Name:** `Keystone Syndicator`
   - **Redirect URI:** `http://localhost:8080/callback` *(Ensure you enter this exactly)*
6. Copy your **Client Key** (TikTok's version of Client ID) and **Client Secret**.
7. Go to **Products** (under your app) and toggle on **Content Posting API**.
8. Save and submit your app configuration. TikTok allows immediate testing using your own developer account (Sandbox Mode) before full public review.

---

## 4. Automatic Local Token Generation

Once you have your credentials, run the custom python utility to launch a local server, trigger the web-based login approvals, and fetch your API tokens:

```bash
python social_oauth_manager.py
```

The script will:
1. Spin up a secure, temporary local callback server on port `8080`.
2. Generate the platform-specific authorization request link.
3. Open your default web browser for you to log in and approve permissions.
4. Capture the secure authorization code.
5. Auto-exchange the code for short-lived and long-lived **Access Tokens**.
6. Save the verified credentials locally in a secure file named `social_tokens.json`.