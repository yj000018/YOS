/**
 * validateParser.mjs — MVP B
 *
 * Node.js test runner for the YMD parser.
 * No Jest. No Vitest. Run with: node test/validateParser.mjs
 *
 * Test cases:
 *   1. MVP A basic 5-type test (regression)
 *   2. MVP B 10-type test (testNoteB.md)
 *   3. Arrow variant: ➡ (no VS) parses as action
 *   4. Warning variant: ⚠ (no VS) parses as risk
 *   5. Free-title decision heading
 *   6. Free-title pattern heading with arrows
 *   7. Heading boundary rule (sub-heading belongs to parent block)
 *   8. Empty note returns zero blocks
 */

import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ─── Inline parser (mirrors src/parser — no TS compilation needed) ──────────

const SEMANTIC_TYPES = {
  "\u{1F4E6}":  { type: "project",      label: "Projects"      },   // 📦
  "\u{1F3D7}\uFE0F": { type: "architecture", label: "Architecture"  }, // 🏗️
  "\u{1F9E9}":  { type: "component",    label: "Components"    },   // 🧩
  "\u2705":     { type: "decision",     label: "Decisions"     },   // ✅
  "\u27A1\uFE0F": { type: "action",     label: "Actions"       },   // ➡️
  "\u26A0\uFE0F": { type: "risk",       label: "Risks"         },   // ⚠️
  "\u2753":     { type: "question",     label: "Questions"     },   // ❓
  "\u{1F4A1}":  { type: "insight",      label: "Insights"      },   // 💡
  "\u{1F9E0}":  { type: "memory",       label: "Memories"      },   // 🧠
  "\u{1F501}":  { type: "pattern",      label: "Patterns"      },   // 🔁
};

const EMOJI_VARIANTS = {
  "\u27A1":      "\u27A1\uFE0F",   // ➡  → ➡️
  "\u26A0":      "\u26A0\uFE0F",   // ⚠  → ⚠️
};

function normalizeEmoji(text) {
  let result = text;
  for (const [bare, canonical] of Object.entries(EMOJI_VARIANTS)) {
    result = result.split(bare).join(canonical);
  }
  return result;
}

function extractSemanticEmoji(headingText) {
  const normalized = normalizeEmoji(headingText);
  for (const emoji of Object.keys(SEMANTIC_TYPES)) {
    if (normalized.startsWith(emoji)) {
      const rest = normalized.slice(emoji.length).trimStart();
      return { emoji, rest };
    }
  }
  return null;
}

const HEADING_RE = /^(#{1,6})\s+(.+)$/;

function parseYmdNote(markdown) {
  if (!markdown || markdown.trim().length === 0) return [];
  const lines = markdown.split("\n");
  const blocks = [];
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
        const contentLines = [];
        let j = i + 1;
        while (j < lines.length) {
          const nextLine = lines[j];
          const nextHeading = nextLine.match(HEADING_RE);
          if (nextHeading && nextHeading[1].length <= level) break;
          contentLines.push(nextLine);
          j++;
        }
        while (contentLines.length > 0 && contentLines[contentLines.length - 1].trim() === "") {
          contentLines.pop();
        }
        const title = rest.length > 0 ? rest : typeDef.label;
        const contentStr = contentLines.join("\n").trim();
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

// ─── extractPreview (mirrors src/parser/ymdParser.ts) ───────────────────────

const PREVIEW_STRIP_RE = /^(?:#{1,6}|[*\->])\s*/;

function extractPreview(content) {
  if (!content || content.trim().length === 0) return undefined;
  const lines = content.split("\n");
  const firstLine = lines.find(l => l.trim().length > 0);
  if (!firstLine) return undefined;
  let stripped = firstLine.trim();
  let prev = "";
  while (stripped !== prev) {
    prev = stripped;
    stripped = stripped.replace(PREVIEW_STRIP_RE, "").trim();
  }
  if (stripped.length === 0) return undefined;
  return stripped.length > 80 ? stripped.slice(0, 80) : stripped;
}

// ─── Test runner ─────────────────────────────────────────────────────────────

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${message}`);
    failed++;
  }
}

function assertEqual(actual, expected, message) {
  if (actual === expected) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.error(`  ❌ FAIL: ${message}`);
    console.error(`     expected: ${JSON.stringify(expected)}`);
    console.error(`     actual:   ${JSON.stringify(actual)}`);
    failed++;
  }
}

function section(name) {
  console.log(`\n── Test ${name} ──────────────────────────────────────`);
}

// ─── Test 1: MVP A basic 5-type regression ───────────────────────────────────

section("1: MVP A basic 5-type regression");
{
  const noteA = readFileSync(join(__dirname, "testNote.md"), "utf8");
  const blocks = parseYmdNote(noteA);
  assertEqual(blocks.length, 5, "5 blocks parsed");
  const types = blocks.map(b => b.type);
  assert(types.includes("decision"),  "has decision");
  assert(types.includes("action"),    "has action");
  assert(types.includes("risk"),      "has risk");
  assert(types.includes("question"),  "has question");
  assert(types.includes("memory"),    "has memory");
  for (const b of blocks) {
    assert(!b.title.startsWith(b.emoji), `title clean for ${b.type}`);
  }
}

// ─── Test 2: MVP B 10-type test ───────────────────────────────────────────────

section("2: MVP B 10-type test (testNoteB.md)");
{
  const noteB = readFileSync(join(__dirname, "testNoteB.md"), "utf8");
  const blocks = parseYmdNote(noteB);

  const expected = {
    project:      1,
    architecture: 1,
    component:    1,
    decision:     2,
    action:       2,
    risk:         2,
    question:     1,
    insight:      1,
    memory:       1,
    pattern:      2,
  };

  const counts = {};
  for (const b of blocks) {
    counts[b.type] = (counts[b.type] || 0) + 1;
  }

  for (const [type, count] of Object.entries(expected)) {
    assertEqual(counts[type] ?? 0, count, `${type} count = ${count}`);
  }
  assertEqual(blocks.length, 14, "total 14 blocks");
}

// ─── Test 3: Arrow variant ➡ (no variation selector) ─────────────────────────

section("3: Arrow variant \u27A1 (no VS) parses as action");
{
  const md = "## \u27A1 Build emoji variant normalization.\n\nThis tests arrow without VS.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks.length, 1, "1 block parsed");
  assertEqual(blocks[0]?.type, "action", "type = action");
  assertEqual(blocks[0]?.title, "Build emoji variant normalization.", "title correct");
}

// ─── Test 4: Warning variant ⚠ (no variation selector) ───────────────────────

section("4: Warning variant \u26A0 (no VS) parses as risk");
{
  const md = "## \u26A0 Risk without variation selector\n\nThis tests warning without VS.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks.length, 1, "1 block parsed");
  assertEqual(blocks[0]?.type, "risk", "type = risk");
  assertEqual(blocks[0]?.title, "Risk without variation selector", "title correct");
}

// ─── Test 5: Free-title decision heading ──────────────────────────────────────

section("5: Free-title decision heading");
{
  const md = "## \u2705 Use current-note parsing only for MVP B\n\nThis keeps the scope small.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks.length, 1, "1 block parsed");
  assertEqual(blocks[0]?.type, "decision", "type = decision");
  assertEqual(blocks[0]?.title, "Use current-note parsing only for MVP B", "free title preserved");
}

// ─── Test 6: Free-title pattern heading with arrows ───────────────────────────

section("6: Free-title pattern heading with arrows");
{
  const md = "## \u{1F501} GPT \u2192 Claude \u2192 Manus\n\nThis validates free-title Pattern headings.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks.length, 1, "1 block parsed");
  assertEqual(blocks[0]?.type, "pattern", "type = pattern");
  assertEqual(blocks[0]?.title, "GPT \u2192 Claude \u2192 Manus", "title with arrows preserved");
}

// ─── Test 7: Heading boundary rule ────────────────────────────────────────────

section("7: Heading boundary rule");
{
  const md = [
    "## \u2705 Decision",
    "",
    "Decision content.",
    "",
    "### Context",
    "",
    "This belongs to the Decision block.",
    "",
    "## \u27A1\uFE0F Action",
    "",
    "Action content.",
  ].join("\n");

  const blocks = parseYmdNote(md);
  assertEqual(blocks.length, 2, "2 blocks");
  assertEqual(blocks[0]?.type, "decision", "first = decision");
  assert(
    blocks[0]?.content.includes("Context"),
    "decision content includes sub-heading '### Context'"
  );
  assert(
    blocks[0]?.content.includes("This belongs to the Decision block."),
    "decision content includes sub-heading body"
  );
  assertEqual(blocks[1]?.type, "action", "second = action");
  assert(
    !blocks[1]?.content.includes("Context"),
    "action content does not include decision sub-heading"
  );
}

// ─── Test 8: Empty note returns zero blocks ───────────────────────────────────

section("8: Empty note returns zero blocks");
{
  assertEqual(parseYmdNote("").length, 0, "empty string \u2192 0 blocks");
  assertEqual(parseYmdNote("   \n\n   ").length, 0, "whitespace-only \u2192 0 blocks");
  assertEqual(parseYmdNote("# Just a title\n\nNo semantic headings.").length, 0, "no semantic headings \u2192 0 blocks");
}

// ─── Test 9: Preview — normal content line ──────────────────────────────────

section("9: Preview — normal content line");
{
  const md = "## \u2705 Decision\n\nUse Obsidian as canonical memory.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks[0]?.preview, "Use Obsidian as canonical memory.", "normal preview extracted");
}

// ─── Test 10: Preview — Markdown-prefixed (quote) ────────────────────────────

section("10: Preview — quote-prefixed line");
{
  const md = "## \u{1F4A1} Insight\n\n> A conversation can become a memory graph.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks[0]?.preview, "A conversation can become a memory graph.", "quote stripped from preview");
}

// ─── Test 11: Preview — bullet-prefixed line ─────────────────────────────────

section("11: Preview — bullet-prefixed line");
{
  const md = "## \u27A1\uFE0F Action\n\n- Build reader polish.";
  const blocks = parseYmdNote(md);
  assertEqual(blocks[0]?.preview, "Build reader polish.", "bullet stripped from preview");
}

// ─── Test 12: Preview — empty content block ──────────────────────────────────

section("12: Preview — empty content block");
{
  const md = "## \u2705 Decision\n";
  const blocks = parseYmdNote(md);
  assertEqual(blocks[0]?.preview, undefined, "empty content → preview undefined");
  assert(true, "no crash on empty content");
}

// ─── Test 13: Preview — long line truncated at 80 chars ──────────────────────

section("13: Preview — long line truncated at 80 chars");
{
  const longLine = "A".repeat(100);
  const md = `## \u2705 Decision\n\n${longLine}`;
  const blocks = parseYmdNote(md);
  assertEqual(blocks[0]?.preview?.length, 80, "preview length = 80");
  assertEqual(blocks[0]?.preview, "A".repeat(80), "preview = first 80 chars");
}

// ─── Test 14: Preview — Markdown link remains raw ────────────────────────────

section("14: Preview — Markdown link remains raw");
{
  const md = "## \u{1F4E6} Project\n\nUse [Obsidian](https://obsidian.md) as the base.";
  const blocks = parseYmdNote(md);
  assertEqual(
    blocks[0]?.preview,
    "Use [Obsidian](https://obsidian.md) as the base.",
    "Markdown link not converted"
  );
}

// ─── Summary ──────────────────────────────────────────────────────────────────

console.log(`\n${"=".repeat(52)}`);
console.log(`Results: ${passed} passed, ${failed} failed`);
if (failed > 0) {
  console.error("SOME TESTS FAILED");
  process.exit(1);
} else {
  console.log("ALL TESTS PASSED \u2705");
}
