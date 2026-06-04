import { groq } from "next-sanity";

export const homepageQuery = groq`{
  "homepage": *[_type == "homepage"][0]{
    hero,
    valueProposition,
    features,
    finalCta
  },
  "testimonials": *[_type == "testimonial"] | order(order asc) [0...6]{
    _id,
    name,
    role,
    company,
    quote,
    order
  },
  "settings": *[_type == "siteSettings"][0]{
    siteName,
    tagline,
    primaryColor,
    secondaryColor,
    navigation,
    footer
  }
}`;

export const signupPageQuery = groq`{
  "page": *[_type == "signupPage"][0]{
    headline,
    subheadline,
    formFields,
    successMessage,
    socialProof
  },
  "settings": *[_type == "siteSettings"][0]{
    siteName,
    tagline
  }
}`;

export const siteSettingsQuery = groq`*[_type == "siteSettings"][0]{
  siteName,
  tagline,
  primaryColor,
  secondaryColor,
  navigation,
  footer
}`;
