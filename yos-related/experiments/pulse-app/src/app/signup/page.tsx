import { client, isSanityConfigured } from "@/lib/sanity/client";
import { signupPageQuery } from "@/lib/sanity/queries";
import type { SignupQueryResult } from "@/types/sanity";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { WaitlistForm } from "@/components/WaitlistForm";
import type { Metadata } from "next";

const defaultData: SignupQueryResult = {
  page: {
    headline: "Get early access to Pulse",
    subheadline:
      "Be among the first to experience the future of team productivity. We'll notify you as soon as we launch.",
    formFields: {
      firstNameLabel: "First Name",
      firstNamePlaceholder: "Enter your first name",
      emailLabel: "Email",
      emailPlaceholder: "you@company.com",
      submitText: "Join the Waitlist",
      submittingText: "Joining...",
    },
    successMessage: {
      headline: "You're on the list!",
      body: "Thanks for joining the Pulse waitlist. We'll be in touch soon with updates and early access details.",
    },
    socialProof: "Join 2,400+ professionals already on the waitlist",
  },
  settings: {
    siteName: "Pulse",
    tagline: "The future of team productivity",
  },
};

export const metadata: Metadata = {
  title: "Join the Waitlist — Pulse",
  description: "Sign up for early access to Pulse.",
};

export default async function SignupPage() {
  let data = defaultData;

  if (isSanityConfigured && client) {
    try {
      const sanityData = await client.fetch<SignupQueryResult>(
        signupPageQuery,
        {},
        { next: { revalidate: 60 } }
      );
      if (sanityData?.page) {
        data = {
          page: { ...defaultData.page, ...sanityData.page },
          settings: { ...defaultData.settings, ...sanityData.settings },
        };
      }
    } catch {
      console.log("Using default signup data");
    }
  }

  return (
    <main>
      <Header settings={data.settings} />
      <section className="min-h-[85vh] flex items-center justify-center pt-16">
        <div className="max-w-lg mx-auto px-6 py-16 w-full">
          <div className="text-center mb-10">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent/10 text-accent text-sm font-medium mb-6">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              Early Access
            </div>
            <h1 className="text-3xl md:text-4xl font-display font-bold text-charcoal-900 mb-4">
              {data.page.headline}
            </h1>
            <p className="text-charcoal-700/60 leading-relaxed">
              {data.page.subheadline}
            </p>
          </div>

          <WaitlistForm
            formFields={data.page.formFields}
            successMessage={data.page.successMessage}
          />

          {data.page.socialProof && (
            <p className="text-center text-charcoal-700/40 text-sm mt-8">
              {data.page.socialProof}
            </p>
          )}
        </div>
      </section>
      <Footer settings={data.settings} />
    </main>
  );
}
