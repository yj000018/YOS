import Link from "next/link";
import type { SiteSettingsData } from "@/types/sanity";

interface FooterProps {
  settings?: SiteSettingsData;
}

export function Footer({ settings }: FooterProps) {
  const siteName = settings?.siteName || "Pulse";
  const footerData = settings?.footer;

  return (
    <footer className="py-12 border-t border-cream-200">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-accent flex items-center justify-center">
              <span className="text-white font-display text-xs font-bold">
                {siteName.charAt(0)}
              </span>
            </div>
            <span className="font-display text-sm font-semibold text-charcoal-800">
              {siteName}
            </span>
          </div>
          {footerData?.links && (
            <div className="flex items-center gap-4">
              {footerData.links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-sm text-charcoal-700/50 hover:text-charcoal-700 transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          )}
          <p className="text-charcoal-700/50 text-sm">
            &copy; {footerData?.copyright || `${new Date().getFullYear()} ${siteName}. All rights reserved.`}
          </p>
        </div>
      </div>
    </footer>
  );
}
