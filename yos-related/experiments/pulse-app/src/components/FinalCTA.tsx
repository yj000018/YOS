import Link from "next/link";
import type { FinalCtaData } from "@/types/sanity";

interface FinalCTAProps {
  data: FinalCtaData;
}

export function FinalCTA({ data }: FinalCTAProps) {
  const headline = data.headline || data.title || "Ready to transform your workflow?";
  const subtext = data.subheadline || data.description || "";
  const buttonText = data.ctaText || data.buttonText || "Get Early Access";
  const buttonLink = data.ctaLink || "/signup";

  return (
    <section className="py-24 md:py-32">
      <div className="max-w-6xl mx-auto px-6">
        <div className="relative overflow-hidden rounded-3xl bg-charcoal-800 p-12 md:p-20 text-center">
          <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full bg-accent/10 blur-3xl" />
          <div className="absolute bottom-0 right-1/4 w-64 h-64 rounded-full bg-accent/5 blur-2xl" />

          <div className="relative">
            <h2 className="text-3xl md:text-5xl font-display font-bold text-cream-50 mb-6 text-balance">
              {headline}
            </h2>
            {subtext && (
              <p className="text-cream-200/70 text-lg max-w-xl mx-auto mb-10 leading-relaxed">
                {subtext}
              </p>
            )}
            <Link
              href={buttonLink}
              className="inline-flex items-center gap-2 px-8 py-4 bg-cream-50 text-charcoal-800 rounded-full text-base font-medium hover:bg-cream-100 transition-all hover:shadow-lg hover:-translate-y-0.5"
            >
              {buttonText}
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
        </div>
      </div>
    </section>
  );
}
