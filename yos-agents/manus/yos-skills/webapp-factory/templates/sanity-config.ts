import { defineConfig } from "sanity";
import { deskTool } from "sanity/desk";
import { visionTool } from "@sanity/vision";
import { schemaTypes } from "./src/lib/sanity/schemas";

const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "placeholder";
const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET || "production";

export default defineConfig({
  name: "PROJECT_NAME",
  title: "PROJECT_TITLE",
  projectId,
  dataset,
  basePath: "/studio",
  plugins: [
    deskTool(),
    visionTool({ defaultApiVersion: "2024-01-01" }),
    // NOTE: presentationTool requiert Sanity v5 — ne pas ajouter avec v3
  ],
  schema: {
    types: schemaTypes,
  },
});
