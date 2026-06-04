import { draftMode } from "next/headers";
import { client, previewClient, isSanityConfigured } from "@/lib/sanity/client";
import { homepageQuery } from "@/lib/sanity/queries";
import type { HomepageQueryResult } from "@/types/sanity";
import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { ValueProposition } from "@/components/ValueProposition";
import { FeaturesSection } from "@/components/FeaturesSection";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { FinalCTA } from "@/components/FinalCTA";
import { Footer } from "@/components/Footer";

const defaultData: HomepageQueryResult = {
  homepage: {
    hero: {
      headline: "Work smarter, not harder",
      subheadline:
        "Pulse brings your team's tasks, communication, and goals into one intelligent workspace. Less noise, more flow.",
      ctaText: "Join the Waitlist",
      ctaLink: "/signup",
    },
    valueProposition: {
      title: "Why teams choose Pulse",
      subtitle: "Built for modern teams who value clarity and momentum",
    },
    features: {
      title: "Everything you need",
      subtitle: "A complete toolkit for high-performing teams",
      items: [
        {
          _key: "f1",
          title: "Smart Task Management",
          description:
            "Organize, prioritize, and track tasks with AI-assisted workflows.",
          icon: "layout",
        },
        {
          _key: "f2",
          title: "Unified Communication",
          description:
            "Threads, channels, and direct messages — all contextually linked.",
          icon: "message-circle",
        },
        {
          _key: "f3",
          title: "Goal Tracking",
          description:
            "Set OKRs, track progress, and keep everyone aligned.",
          icon: "target",
        },
      ],
    },
    finalCta: {
      headline: "Ready to transform your workflow?",
      subheadline:
        "Join thousands of teams already using Pulse to work better together.",
      ctaText: "Get Early Access",
      ctaLink: "/signup",
    },
  },
  testimonials: [
    {
      _id: "1",
      name: "Sarah Chen",
      role: "VP of Engineering",
      company: "TechFlow",
      quote:
        "Pulse transformed how our engineering team collaborates. We shipped 40% more features last quarter.",
    },
    {
      _id: "2",
      name: "Marcus Rivera",
      role: "Head of Product",
      company: "ScaleUp",
      quote:
        "The AI insights alone saved us hours of manual reporting.",
    },
    {
      _id: "3",
      name: "Emma Larsson",
      role: "CEO",
      company: "NordTech",
      quote:
        "Finally, a tool that brings everything together without the complexity.",
    },
  ],
  settings: {
    siteName: "Pulse",
    tagline: "The future of team productivity",
  },
};

export default async function HomePage() {
  const { isEnabled: isDraftMode } = await draftMode();
  let data = defaultData;

  if (isSanityConfigured) {
    try {
      // Use preview client in draft mode for live editing, otherwise use published client
      const sanityClient = isDraftMode ? previewClient : client;
      const sanityData = await sanityClient.fetch<HomepageQueryResult>(
        homepageQuery,
        {},
        {
          next: isDraftMode ? { revalidate: 0 } : { revalidate: 60 },
          // Enable stega encoding in draft mode for content links
          ...(isDraftMode && { stega: true }),
        }
      );
      if (sanityData?.homepage) {
        data = {
          homepage: { ...defaultData.homepage, ...sanityData.homepage },
          testimonials:
            sanityData.testimonials?.length > 0
              ? sanityData.testimonials
              : defaultData.testimonials,
          settings: { ...defaultData.settings, ...sanityData.settings },
        };
      }
    } catch (e) {
      console.log("Using default data (Sanity unavailable)");
    }
  }

  // Normalize features data
  const features = Array.isArray(data.homepage.features)
    ? data.homepage.features
    : data.homepage.features?.items || [];

  const featuresTitle = !Array.isArray(data.homepage.features)
    ? data.homepage.features?.title
    : undefined;

  const featuresSubtitle = !Array.isArray(data.homepage.features)
    ? data.homepage.features?.subtitle
    : undefined;

  return (
    <main>
      <Header settings={data.settings} />
      <HeroSection data={data.homepage.hero} />
      <ValueProposition data={data.homepage.valueProposition} />
      <FeaturesSection
        features={features}
        title={featuresTitle}
        subtitle={featuresSubtitle}
      />
      <TestimonialsSection testimonials={data.testimonials} />
      <FinalCTA data={data.homepage.finalCta} />
      <Footer settings={data.settings} />
    </main>
  );
}
