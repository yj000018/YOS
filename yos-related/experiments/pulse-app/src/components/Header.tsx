import Link from "next/link";
import type { SiteSettingsData } from "@/types/sanity";

interface HeaderProps {
  settings?: SiteSettingsData;
}

export function Header({ settings }: HeaderProps) {
  const siteName = settings?.siteName || "Pulse";
  const navigation = settings?.navigation || [];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-cream-50/80 backdrop-blur-md border-b border-cream-200">
      <nav className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <span className="text-white font-display text-sm font-bold">
              {siteName.charAt(0)}
            </span>
          </div>
          <span className="font-display text-xl font-semibold text-charcoal-800">
            {siteName}
          </span>
        </Link>
        <div className="flex items-center gap-6">
          {navigation.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-charcoal-600 hover:text-charcoal-800 transition-colors hidden md:block"
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/signup"
            className="px-5 py-2 bg-charcoal-800 text-cream-50 rounded-full text-sm font-medium hover:bg-charcoal-700 transition-colors"
          >
            Join Waitlist
          </Link>
        </div>
      </nav>
    </header>
  );
}
