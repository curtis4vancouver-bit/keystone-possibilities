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

  // Extract root domain
  const rootDomain = process.env.NEXT_PUBLIC_ROOT_DOMAIN || "localhost:3000";
  const tenantSlug = hostname.replace(`.${rootDomain}`, "").trim();

  // Route apex domain requests to the home directory
  if (hostname === rootDomain || tenantSlug === "www" || tenantSlug === hostname) {
    url.pathname = `/home${url.pathname}`;
    return NextResponse.rewrite(url);
  }

  // Route subdomain requests dynamically to the apps/tenant folder
  url.pathname = `/apps/${tenantSlug}${url.pathname}`;
  return NextResponse.rewrite(url);
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
