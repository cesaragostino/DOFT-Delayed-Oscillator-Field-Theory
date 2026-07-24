import type { Metadata } from "next";
import { absoluteAssetUrl } from "@/lib/site";
import "./globals.css";

const configuredSiteUrl = process.env.NEXT_PUBLIC_SITE_URL;

export const metadata: Metadata = {
  metadataBase: configuredSiteUrl ? new URL(configuredSiteUrl) : undefined,
  title: "DOFT — Delayed Oscillator Field Theory",
  description:
    "An open research program studying how delay, memory, and phase relations can produce persistent structure in deterministic oscillator networks.",
  keywords: [
    "delayed oscillators",
    "dynamical systems",
    "memory",
    "phase locking",
    "emergence",
    "DOFT",
  ],
  openGraph: {
    title: "DOFT — Delayed Oscillator Field Theory",
    description:
      "Structure, memory, and causal dynamics in deterministic oscillator networks.",
    type: "website",
    images: [
      {
        url: absoluteAssetUrl("/doft-social-card.jpg"),
        width: 1200,
        height: 630,
        alt: "DOFT editorial cover with delayed oscillator traces",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "DOFT — Delayed Oscillator Field Theory",
    description:
      "Structure, memory, and causal dynamics in deterministic oscillator networks.",
    images: [absoluteAssetUrl("/doft-social-card.jpg")],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
