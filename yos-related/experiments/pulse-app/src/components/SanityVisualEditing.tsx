"use client";

import { VisualEditing } from "next-sanity";
import { useEffect, useState } from "react";

export function SanityVisualEditingProvider() {
  const [isDraftMode, setIsDraftMode] = useState(false);

  useEffect(() => {
    // Check if draft mode is enabled via cookie
    setIsDraftMode(document.cookie.includes("__prerender_bypass"));
  }, []);

  if (!isDraftMode) return null;

  return <VisualEditing />;
}
