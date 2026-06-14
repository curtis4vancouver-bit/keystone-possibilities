import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Keystone Possibilities LTD — Client Portal",
  description: "Licensed residential builder and fiduciary construction project manager serving Squamish, Whistler, West Vancouver, and the Sea-to-Sky corridor. BC Builder License #52603.",
  openGraph: {
    title: "Keystone Possibilities LTD — Client Portal",
    description: "Licensed residential builder and fiduciary construction project manager serving the Sea-to-Sky corridor. BC Builder License #52603.",
    url: "https://keystonepossibilities.ca",
    siteName: "Keystone Possibilities LTD",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Keystone Possibilities LTD — Client Portal",
    description: "Licensed residential builder and fiduciary construction project manager. BC Builder License #52603.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "https://keystonepossibilities.ca/#organization",
        "name": "Keystone Possibilities LTD",
        "url": "https://keystonepossibilities.ca",
        "logo": "https://keystonepossibilities.ca/wp-content/uploads/2023/12/screenshot-2023-12-03-at-2.30.29-pm-1.png",
        "description": "Licensed residential builder and fiduciary construction project manager serving Squamish, Whistler, West Vancouver, and the Sea-to-Sky corridor in British Columbia, Canada. BC Builder License #52603.",
        "founder": {
          "@type": "Person",
          "@id": "https://keystonepossibilities.ca/#person",
          "name": "Wayne Stevenson",
          "jobTitle": "Founder & Certified BC Builder"
        },
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Watts Point Road",
          "addressLocality": "Squamish",
          "addressRegion": "BC",
          "postalCode": "V8B 0B1",
          "addressCountry": "CA"
        },
        "hasCredential": {
          "@type": "EducationalOccupationalCredential",
          "credentialCategory": "Licensed Residential Builder",
          "recognizedBy": {
            "@type": "Organization",
            "name": "BC Housing"
          },
          "identifier": "52603"
        },
        "areaServed": [
          { "@type": "City", "name": "Squamish", "sameAs": "https://en.wikipedia.org/wiki/Squamish,_British_Columbia" },
          { "@type": "City", "name": "Whistler", "sameAs": "https://en.wikipedia.org/wiki/Whistler,_British_Columbia" },
          { "@type": "City", "name": "West Vancouver", "sameAs": "https://en.wikipedia.org/wiki/West_Vancouver" },
          { "@type": "City", "name": "North Vancouver" },
          { "@type": "City", "name": "Sunshine Coast" }
        ],
        "sameAs": [
          "https://www.youtube.com/@KeyStoneRecomposition",
          "https://www.youtube.com/@KeystoneProtocols",
          "https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y",
          "https://keystonerecomposition.com",
          "https://www.facebook.com/profile.php?id=61554185128555",
          "https://www.instagram.com/keystonerecomposition"
        ]
      }
    ]
  };

  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
