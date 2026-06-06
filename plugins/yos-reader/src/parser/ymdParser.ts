/**
 * ymdParser.ts — MVP C
 *
 * Pure parser: takes a Markdown string, returns SemanticBlock[].
 * No side effects. Does not mutate input.
 *
 * MVP C additions over MVP B:
 *   - `preview?` field on SemanticBlock
 *   - extractPreview(): first non-empty line, strip leading Markdown markers,
 *     truncate at 80 chars, no Markdown rendering, no link conversion
 */

import { SEMANTIC_TYPES, EMOJI_VARIANTS } from "./semanticTypes";

export interface SemanticBlock {
  type: string;
  emoji: string;
  label: string;    // sidebar group label (e.g. "Decisions")
  title: string;    // item title (emoji stripped)
  content: string;
  preview?: string; // MVP C: first content line, stripped + truncated
  lineStart: number;
  lineEnd: number;
}

/** Matches any Markdown heading: captures hashes and the rest of the line. */
const HEADING_RE = /^(#{1,6})\s+(.+)$/;

/**
 * PREVIEW_STRIP_RE
 *
 * Strips only these leading Markdown markers (one or more, with trailing space):
 *   ##  *  -  >
 *
 * Applied iteratively until no more leading markers remain.
 * Does not strip inline Markdown, links, or any other syntax.
 */
const PREVIEW_STRIP_RE = /^(?:#{1,6}|[*\->])\s*/;

/**
 * extractPreview
 *
 * Rules (per MVP C Scope Override):
 *   1. Find first non-empty content line
 *   2. Strip only leading ## * - > markers (iteratively)
 *   3. Trim whitespace
 *   4. Truncate at 80 characters
 *   5. If no content, return undefined
 *   6. Do not convert Markdown links
 *   7. Do not render Markdown
 *   8. Do not mutate input
 */
export function extractPreview(content: string): string | undefined {
  if (!content || content.trim().length === 0) return undefined;

  const lines = content.split("\n");
  const firstLine = lines.find((l) => l.trim().length > 0);
  if (!firstLine) return undefined;

  // Strip leading Markdown markers iteratively
  let stripped = firstLine.trim();
  let prev = "";
  while (stripped !== prev) {
    prev = stripped;
    stripped = stripped.replace(PREVIEW_STRIP_RE, "").trim();
  }

  if (stripped.length === 0) return undefined;

  // Truncate at 80 characters
  return stripped.length > 80 ? stripped.slice(0, 80) : stripped;
}

/**
 * normalizeEmoji
 *
 * Replaces known bare-codepoint emoji variants with their canonical form.
 */
function normalizeEmoji(text: string): string {
  let result = text;
  for (const [bare, canonical] of Object.entries(EMOJI_VARIANTS)) {
    result = result.split(bare).join(canonical);
  }
  return result;
}

/**
 * extractSemanticEmoji
 *
 * After normalization, check whether the heading text starts with a
 * known semantic emoji. Returns { emoji, rest } or null.
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

        const contentStr = contentLines.join("\n").trim();
        const title = rest.length > 0 ? rest : typeDef.label;

        blocks.push({
          type: typeDef.type,
          emoji,
          label: typeDef.label,
          title,
          content: contentStr,
          preview: extractPreview(contentStr),
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
