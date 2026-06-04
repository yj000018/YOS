import Link from "next/link";
import type { HeroData } from "@/types/sanity";

interface HeroSectionProps {
  data: HeroData;
}

export function HeroSection({ data }: HeroSectionProps) {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center pt-16">
      {/* Subtle gradient background */}
      <div className="absolute inset-0 bg-gradient-to-b from-cream-50 via-cream-100 to-cream-50" />
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-accent/5 blur-3xl" />

      <div className="relative max-w-4xl mx-auto px-6 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent/10 text-accent text-sm font-medium mb-8">
          <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
          Now in early access
        </div>

        <h1 className="text-5xl md:text-7xl font-display font-bold text-charcoal-900 leading-tight mb-6 text-balance">
          {data.headline}
        </h1>

        <p className="text-lg md:text-xl text-charcoal-700/70 max-w-2xl mx-auto mb-10 leading-relaxed">
          {data.subheadline}
        </p>

        <Link
          href="/signup"
          className="inline-flex items-center gap-2 px-8 py-4 bg-charcoal-800 text-cream-50 rounded-full text-base font-medium hover:bg-charcoal-700 transition-all hover:shadow-lg hover:shadow-charcoal-800/20 hover:-translate-y-0.5"
        >
          {data.ctaText}
          <svg
            className="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17 8l4 4m0 0l-4 4m4-4H3"
            />
          </svg>
        </Link>
      </div>
    </section>
  );
}
