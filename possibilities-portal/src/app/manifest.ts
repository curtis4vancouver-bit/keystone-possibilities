import { MetadataRoute } from "next";
import { headers } from "next/headers";

export default async function manifest(): Promise<MetadataRoute.Manifest> {
  const headersList = await headers();
  const host = headersList.get("host") || "platform.com";
  
  // Extract tenant subdomain
  const tenant = host.split(".")[0];

  const tenantConfigs: Record<string, { name: string; short: string; color: string }> = {
    landscaping: {
      name: "GreenScape Professional Operations",
      short: "GreenScape",
      color: "#15803d",
    },
    roofing: {
      name: "Apex Roofing and Estimation",
      short: "ApexRoof",
      color: "#b91c1c",
    },
    "custom-homes": {
      name: "Elysian Custom Home Builder",
      short: "Elysian",
      color: "#0f172a",
    },
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
      {
        src: `/icons/${tenant}/icon-192.png`,
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: `/icons/${tenant}/icon-512.png`,
        sizes: "512x512",
        type: "image/png",
      },
    ],
  };
}
