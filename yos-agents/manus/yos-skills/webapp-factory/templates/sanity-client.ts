import { createClient } from "next-sanity";

// IMPORTANT: fallback "placeholder" — jamais "" (crashe createClient au build)
export const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "placeholder";
export const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET || "production";
export const apiVersion = "2024-01-01";

// Guard: ne fetch que si le projectId est réellement configuré
const isSanityConfigured =
  !!process.env.NEXT_PUBLIC_SANITY_PROJECT_ID &&
  process.env.NEXT_PUBLIC_SANITY_PROJECT_ID !== "placeholder";

// Client toujours créé (projectId valide syntaxiquement) pour éviter les erreurs de build
export const client = createClient({
  projectId,
  dataset,
  apiVersion,
  useCdn: true,
  perspective: "published",
});

export const previewClient = createClient({
  projectId,
  dataset,
  apiVersion,
  useCdn: false,
  perspective: "previewDrafts",
  token: process.env.SANITY_API_TOKEN,
});

export function getClient(preview = false) {
  return preview ? previewClient : client;
}

export { isSanityConfigured };
