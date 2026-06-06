/**
 * ymdParser.ts — MVP B
 *
 * Pure parser: takes a Markdown string, returns SemanticBlock[].
 * No side effects. Does not mutate input.
 *
 * MVP B additions over MVP A:
 *   - emoji variant normalization (➡ → ➡️, ⚠ → ⚠️)
 *   - free-title headings (## ✅ Use Obsidian as canonical memory)
 *   - `label` field on SemanticBlock
 *   - heading boundary rule verified (sub-headings belong to parent block)
 */

import { SEMANTIC_TYPES, EMOJI_VARIANTS } from "./semanticTypes";

export interface SemanticBlock {
  type: string;
  emoji: string;
  label: string;    // sidebar group label (e.g. "Decisions")
  title: string;    // item title (emoji stripped)
  content: string;
  lineStart: number;
  lineEnd: number;
}

/** Matches any Markdown heading: captures hashes and the rest of the line. */
const HEADING_RE = /^(#{1,6})\s+(.+)$/;

/**
 * normalizeEmoji
 *
 * Replaces known bare-codepoint emoji variants with their canonical
 * variation-selector form before matching against SEMANTIC_TYPES.
 *
 * Only the leading characters of the heading text need normalization;
 * we scan the full string for safety.
 */
function normalizeEmoji(text: string): string {
  let result = text;
  for (const [bare, canonical] of Object.entries(EMOJI_VARIANTS)) {
    // Replace all occurrences (a heading could theoretically have multiple)
    result = result.split(bare).join(canonical);
  }
  return result;
}

/**
 * extractSemanticEmoji
 *
 * After normalization, check whether the heading text starts with a
 * known semantic emoji. Returns { emoji, rest } or null.
 *
 * `rest` is the title: everything after the emoji, trimmed.
 * If rest is empty (pure type-label heading like "## ✅ Decision"),
 * the caller should fall back to the type label.
 */
function extractSemanticEmoji(
  headingText: string
): { emoji: string; rest: string } | null {
  const normalized = normalizeEmoji(headingText);
  for (const emoji of Object.keys(SEMANTIC_TYPES)) {
    if (normalized.startsWith(emoji)) {
      const rest = normalized.slice(emoji.length).trimStart();
      return { emoji, rest };
    }
  }
  return null;
}

/**
 * parseYmdNote
 *
 * @param markdown - raw Markdown string of the active note
 * @returns SemanticBlock[] in source order
 */
export function parseYmdNote(markdown: string): SemanticBlock[] {
  if (!markdown || markdown.trim().length === 0) return [];

  const lines = markdown.split("\n");
  const blocks: SemanticBlock[] = [];

  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const headingMatch = line.match(HEADING_RE);

    if (headingMatch) {
      const level = headingMatch[1].length;
      const headingText = headingMatch[2].trim();
      const extracted = extractSemanticEmoji(headingText);

      if (extracted) {
        const { emoji, rest } = extracted;
        const typeDef = SEMANTIC_TYPES[emoji];
        const lineStart = i;

        // Collect content lines until next heading of equal or higher level.
        // Sub-headings (lower level = more #) belong to this block.
        const contentLines: string[] = [];
        let j = i + 1;

        while (j < lines.length) {
          const nextLine = lines[j];
          const nextHeading = nextLine.match(HEADING_RE);
          if (nextHeading && nextHeading[1].length <= level) {
            break;
          }
          contentLines.push(nextLine);
          j++;
        }

        // Trim trailing blank lines
        while (
          contentLines.length > 0 &&
          contentLines[contentLines.length - 1].trim() === ""
        ) {
          contentLines.pop();
        }

        // Title: use rest if non-empty (free-title), else fall back to
        // the singular form of the label (e.g. "Decisions" → "Decision").
        // The singular is the label minus trailing 's' — but only for the
        // standard type-label case where rest is exactly the label word.
        // Simpler and more robust: use rest if non-empty, else use typeDef.label.
        const title = rest.length > 0 ? rest : typeDef.label;

        blocks.push({
          type: typeDef.type,
          emoji,
          label: typeDef.label,
          title,
          content: contentLines.join("\n").trim(),
          lineStart,
          lineEnd: j - 1,
        });

        i = j;
        continue;
      }
    }

    i++;
  }

  return blocks;
}
