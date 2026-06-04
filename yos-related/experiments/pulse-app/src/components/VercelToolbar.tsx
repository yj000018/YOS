"use client";

import { VercelToolbar } from "@vercel/toolbar/next";

export function VercelToolbarProvider() {
  const shouldInjectToolbar = process.env.NEXT_PUBLIC_VERCEL_ENV !== "production";
  return shouldInjectToolbar ? <VercelToolbar /> : null;
}
