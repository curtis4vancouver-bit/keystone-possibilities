import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure trailing slashes for consistent URL structure
  trailingSlash: false,

  // Security and SEO headers
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Robots-Tag",
            value: "index, follow",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
        ],
      },
      // Allow AI crawlers explicitly
      {
        source: "/project-management/(.*)",
        headers: [
          {
            key: "X-Robots-Tag",
            value: "index, follow, max-snippet:-1, max-image-preview:large",
          },
        ],
      },
    ];
  },

  // Redirect .com to .ca for any stale links
  async redirects() {
    return [
      {
        source: "/squamish_custom_homes",
        destination: "/project-management/squamish_custom_homes.html",
        permanent: true,
      },
      {
        source: "/whistler_custom_homes",
        destination: "/project-management/whistler_custom_homes.html",
        permanent: true,
      },
      {
        source: "/west_vancouver_custom_homes",
        destination: "/project-management/west_vancouver_custom_homes.html",
        permanent: true,
      },
      {
        source: "/north_vancouver_custom_homes",
        destination: "/project-management/north_vancouver_custom_homes.html",
        permanent: true,
      },
      {
        source: "/sunshine_coast_custom_homes",
        destination: "/project-management/sunshine_coast_custom_homes.html",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
