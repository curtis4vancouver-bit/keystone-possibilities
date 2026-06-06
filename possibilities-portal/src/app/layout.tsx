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
  title: "Keystone Possibilities LTD",
  description: "High-End Residential Project Management in West Vancouver and the Sea-to-Sky corridor.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "name": "Keystone Possibilities LTD",
    "alternateName": "Keystone Recomposition",
    "url": "https://keystonepossibilities.ca",
    "logo": "https://keystonepossibilities.ca/assets/charcoal-gold-logo.png",
    "image": "https://keystonepossibilities.ca/assets/squamish-luxury-build.jpg",
    "founder": {
      "@type": "Person",
      "name": "Wayne Curtis Stevenson",
      "birthDate": "1983-03-26",
      "jobTitle": "General Contractor & Site Superintendent"
    },
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Squamish",
      "addressRegion": "BC",
      "addressCountry": "CA"
    },
    "hasCredential": {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "Licensed Residential Builder",
      "issuingAuthority": "BC Housing",
      "credentialNumber": "52603"
    },
    "sameAs": [
      "https://www.youtube.com/channel/UCMn1f9DTF_iybKmv5WlTm9Q",
      "https://open.spotify.com/artist/KeystoneRecomposition",
      "https://keystonerecomposition.com"
    ],
    "knowsAbout": [
      "Residential Project Management",
      "Biophilic Design",
      "Subterranean Luxury Construction",
      "Metabolic Recomposition"
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
