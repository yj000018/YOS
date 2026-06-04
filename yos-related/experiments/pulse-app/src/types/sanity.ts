export interface HeroData {
  headline: string;
  subheadline: string;
  ctaText: string;
  ctaLink?: string;
  secondaryCtaText?: string;
  secondaryCtaLink?: string;
}

export interface ValuePropositionItem {
  _key: string;
  icon: string;
  title: string;
  description: string;
}

export interface ValuePropositionData {
  title: string;
  subtitle?: string;
  description?: string;
  items?: ValuePropositionItem[];
}

export interface FeatureData {
  _key?: string;
  title: string;
  description: string;
  icon: string;
}

export interface FeaturesData {
  title: string;
  subtitle?: string;
  items: FeatureData[];
}

export interface FinalCtaData {
  headline?: string;
  title?: string;
  subheadline?: string;
  description?: string;
  ctaText?: string;
  ctaLink?: string;
  buttonText?: string;
}

export interface TestimonialData {
  _id: string;
  name: string;
  role: string;
  company: string;
  quote: string;
  order?: number;
  // Legacy support
  author?: {
    name: string;
    title: string;
    company?: string;
  };
}

export interface NavigationLink {
  label: string;
  href: string;
}

export interface SiteSettingsData {
  siteName?: string;
  tagline?: string;
  title?: string;
  description?: string;
  url?: string;
  primaryColor?: string;
  secondaryColor?: string;
  navigation?: NavigationLink[];
  footer?: {
    copyright: string;
    links: NavigationLink[];
  };
}

export interface HomepageData {
  hero: HeroData;
  valueProposition: ValuePropositionData;
  features: FeaturesData | FeatureData[];
  finalCta: FinalCtaData;
}

export interface SignupPageData {
  headline: string;
  subheadline: string;
  formFields: {
    firstNameLabel: string;
    firstNamePlaceholder: string;
    emailLabel: string;
    emailPlaceholder: string;
    submitText: string;
    submittingText: string;
  };
  successMessage: {
    headline: string;
    body: string;
  };
  socialProof?: string;
}

export interface HomepageQueryResult {
  homepage: HomepageData;
  testimonials: TestimonialData[];
  settings: SiteSettingsData;
}

export interface SignupQueryResult {
  page: SignupPageData;
  settings: SiteSettingsData;
}
