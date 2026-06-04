import type { Metadata } from "next";
import { DM_Sans, Playfair_Display } from "next/font/google";
import { draftMode } from "next/headers";
import { VisualEditing } from "next-sanity";
import { VercelToolbarProvider } from "@/components/VercelToolbar";
import "./globals.css";

const displayFont = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});

const bodyFont = DM_Sans({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Pulse — Calm Productivity for Creatives",
  description:
    "A refined productivity tool crafted for creative professionals seeking tranquility and efficiency.",
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isEnabled: isDraftMode } = await draftMode();

  return (
    <html lang="en" className={`${displayFont.variable} ${bodyFont.variable}`}>
      <body>
        {children}
        {isDraftMode && <VisualEditing />}
        <VercelToolbarProvider />
      </body>
    </html>
  );
}
