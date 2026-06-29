---
id: doc-pwaclonefactory
title: Pwa Clone Factory
type: document
summary: 'PROJECT: Keystone B2B Multi-Tenant Platform'
entities: []
created: '2026-05-23T17:32:44.721032'
updated: '2026-06-14T19:57:36.054106'
---
# Technical [[ARCHITECTURE|Architecture]] Blueprint: PWA & TWA Clone Factory
**PROJECT:** Keystone B2B Multi-Tenant Platform  
**TECHNOLOGY STACK:** Next.js (App Router), Tailwind CSS v4, Serwist, Bubblewrap, Google Play Store TWA  

---

<!-- CONTEXT: Pwa Clone Factory / 1. Multi-Tenant Systems Architecture & Host-Based Routing -->
## 1. Multi-Tenant Systems Architecture & Host-Based Routing

The goal is to serve distinct, customized branding and operational experiences for **Landscaping, Roofing, and Custom Homes** from a single, unified Next.js codebase.

```text
[ Incoming Request ] ──► ( roofing.platform.com )
                             │
                             ▼
                    [ middleware.ts ] ──► Extracts host header
                             │
                             ▼ ( Invisible Internal Rewrite )
                    [ /apps/roofing/page.tsx ]
```

<!-- CONTEXT: Pwa Clone Factory / Host-Based Middleware -->
### Host-Based Middleware
A custom Next.js Middleware layer intercepts all incoming requests before page rendering begins. It extracts the host header, filters out static assets, and performs an invisible rewrite to the dynamic [[Master_Docs/00_DIRECTORY_STRUCTURE|directory structure]].

```typescript
// src/middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  const hostname = request.headers.get("host") || "";

  // Skip static files, API routes, and Next.js internals
  if (
    PUBLIC_FILE.test(url.pathname) ||
    url.pathname.startsWith("/_next") ||
    url.pathname.startsWith("/api") ||
    url.pathname.startsWith("/~offline")
  ) {
    return NextResponse.next();
  }

  const rootDomain = process.env.NEXT_PUBLIC_ROOT_DOMAIN || "platform.com";
  const tenantSlug = hostname.replace(`.${rootDomain}`, "").trim();

  // Route requests directed to the apex domain to the home layout
  if (hostname === rootDomain || tenantSlug === "www") {
    url.pathname = `/home${url.pathname}`;
    return NextResponse.rewrite(url);
  }

  // Rewrite external requests to the dynamic tenant directory
  url.pathname = `/apps/${tenantSlug}${url.pathname}`;
  return NextResponse.rewrite(url);
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

<!-- CONTEXT: Pwa Clone Factory / 2. Dynamic Styling & Theme Injection (Tailwind CSS v4) -->
## 2. Dynamic Styling & Theme Injection (Tailwind CSS v4)

Tailwind CSS v4 introduces a streamlined compiler that deprecates `tailwind.config.js` in favor of standard CSS variables directly within the main CSS entry point.

<!-- CONTEXT: Pwa Clone Factory / Global Stylesheet Mapping (`src/app/globals.css`) -->
### Global Stylesheet Mapping (`src/app/globals.css`)
```css
@import "tailwindcss";

@theme {
  --color-brand-primary: var(--brand-primary);
  --color-brand-secondary: var(--brand-secondary);
  --color-brand-bg: var(--brand-bg);
  --font-brand: var(--brand-font);
  --radius-brand: var(--brand-radius);
}
```

<!-- CONTEXT: Pwa Clone Factory / Brand Default Tokens -->
### Brand Default Tokens

| Token | Landscaping | Roofing | Custom Homes |
| :--- | :--- | :--- | :--- |
| **`--brand-primary`** | `#15803d` (Forest Green) | `#b91c1c` (Safety Red) | `#0f172a` (Slate Black) |
| **`--brand-secondary`** | `#86efac` (Mint) | `#f3f4f6` (Light Gray) | `#b45309` (Amber Gold) |
| **`--brand-bg`** | `#f0fdf4` (Off-white Green) | `#fafafa` (Pure White) | `#f8fafc` (Slate Gray Tint) |
| **`--brand-font`** | `system-ui, sans-serif` | `Roboto, sans-serif` | `Georgia, serif` |
| **`--brand-radius`** | `0.5rem` (Rounded) | `0px` (Sharp/Industrial) | `0.125rem` (Slightly Rounded) |

<!-- CONTEXT: Pwa Clone Factory / Runtime Theme Injector -->
### Runtime Theme Injector
A client-side theme provider dynamically updates root CSS variables at runtime based on the incoming tenant metadata.

```typescript
// src/components/ThemeProvider.tsx
"use client";

import React, { createContext, useEffect } from "react";

interface BrandTheme {
  primary: string;
  secondary: string;
  bg: string;
  font: string;
  radius: string;
}

export const ThemeContext = createContext<{ theme: BrandTheme | null }>({ theme: null });

export function ThemeProvider({ theme, children }: { theme: BrandTheme; children: React.ReactNode }) {
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty("--brand-primary", theme.primary);
    root.style.setProperty("--brand-secondary", theme.secondary);
    root.style.setProperty("--brand-bg", theme.bg);
    root.style.setProperty("--brand-font", theme.font);
    root.style.setProperty("--brand-radius", theme.radius);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme }}>
      <div style={{ fontFamily: "var(--brand-font)", backgroundColor: "var(--brand-bg)" }} className="min-h-screen">
        {children}
      </div>
    </ThemeContext.Provider>
  );
}
```

---

<!-- CONTEXT: Pwa Clone Factory / 3. Dynamic Manifests & Serwist Offline Optimization -->
## 3. Dynamic Manifests & Serwist Offline Optimization

<!-- CONTEXT: Pwa Clone Factory / Dynamic Manifest Route (`src/app/manifest.ts`) -->
### Dynamic Manifest Route (`src/app/manifest.ts`)
```typescript
import { MetadataRoute } from "next";
import { headers } from "next/headers";

export default async function manifest(): Promise<MetadataRoute.Manifest> {
  const headersList = await headers();
  const host = headersList.get("host") || "platform.com";
  const tenant = host.split(".")[0];

  const tenantConfigs: Record<string, { name: string; short: string; color: string }> = {
    landscaping: { name: "GreenScape Operations", short: "GreenScape", color: "#15803d" },
    roofing: { name: "Apex Roofing & Estimation", short: "ApexRoof", color: "#b91c1c" },
    "custom-homes": { name: "Elysian Home Builders", short: "Elysian", color: "#0f172a" },
  };

  const config = tenantConfigs[tenant] || tenantConfigs["landscaping"];

  return {
    name: config.name,
    short_name: config.short,
    description: `Core operational application for ${config.name}`,
    start_url: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: "#ffffff",
    theme_color: config.color,
    icons: [
      { src: `/icons/${tenant}/icon-192.png`, sizes: "192x192", type: "image/png" },
      { src: `/icons/${tenant}/icon-512.png`, sizes: "512x512", type: "image/png" }
    ],
  };
}
```

<!-- CONTEXT: Pwa Clone Factory / Serwist Service Worker Config -->
### Serwist Service Worker Config
Using `Serwist` (the successor to `next-pwa`) to pre-cache offline layouts and enable caching models custom-tailored for field contractors:
*   **App Shell (`Cache-Only`):** Instant, reliable launch screen and offline [[STATE|state]] fallback.
*   **API Queries (`Network-First`):** Tries network for latest work orders, falls back to cache if offline in the field.
*   **Media Library (`Network-Only`):** Completely bypasses local cache to prevent local storage bloat from drone photos/videos.

---

<!-- CONTEXT: Pwa Clone Factory / 4. Bubblewrap TWA Compilation Pipeline -->
## 4. Bubblewrap TWA Compilation Pipeline

A Trusted Web Activity (TWA) wraps the PWA in an Android container. Use Google Chrome Labs' `Bubblewrap` utility:

```bash
# 1. Install CLI
npm install -g @bubblewrap/cli

# 2. Initialize project pointing to your dynamic manifest
bubblewrap init --manifest https://roofing.platform.com/manifest.webmanifest

# 3. Compile project
bubblewrap build

# 4. Sideload for testing
bubblewrap install
```

<!-- CONTEXT: Pwa Clone Factory / Keystore Artifacts Produced: -->
### Keystore Artifacts Produced:
*   `app-release-signed.apk`: Optimized for local side-loading and physical device testing.
*   `app-release-bundle.aab`: Production Android App Bundle required for Google Play uploads.

---

<!-- CONTEXT: Pwa Clone Factory / 5. Digital Asset Links Verification -->
## 5. Digital Asset Links Verification

To remove the URL address bar inside the native Android container, host a verified JSON payload at:

`https://roofing.platform.com/.well-known/assetlinks.json`

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.platform.roofing.twa",
      "sha256_cert_fingerprints": [
        "LOCAL_DEBUG_UPLOAD_SHA256_FINGERPRINT",
        "GOOGLE_PLAY_STORE_PRODUCTION_SIGNING_FINGERPRINT"
      ]
    }
  }
]
```

---

<!-- CONTEXT: Pwa Clone Factory / 6. Google Play Store Submission Strategy -->
## 6. Google Play Store Submission Strategy

To scale this SaaS platform white-label model without triggering Google Play suspensions:

1.  **Avoid spam/repetitive rejections:** Ensure each client app listing has a completely unique title, custom descriptive text, and real screenshots showing their domain-specific UI (not just color swaps on standard mockups).
2.  **Developer Account Model (Decentralized is MANDATORY):**
    *   Do **not** publish all white-label customer apps under a single Centralized developer profile. If one client violates a policy, Google will terminate the entire account, bringing down all your clients' apps.
    *   **Decentralized Account Model:** Strictly mandate that each contractor client sets up their own **Business Developer Account** using their corporate **D-U-N-S number**. 
    *   *The Benefit:* Organization/Business accounts are **fully exempted** from Google Play's 12-tester, 14-day closed testing mandate, letting you publish TWAs to production tracks instantly.


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
