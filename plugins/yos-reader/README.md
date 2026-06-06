# Y-OS Reader — YMD Reader MVP

**Version:** 0.1.0  
**Status:** MVP A — functional  
**Scope:** Strictly governed by [MVP A Scope Override v0.1]

---

## What this plugin does

Y-OS Reader parses the **active Markdown note** in Obsidian, detects **YMD semantic headings** (headings prefixed with a known emoji), extracts their content blocks, groups them by semantic type, and displays them in a **right-sidebar panel**.

Clicking any item in the sidebar scrolls the editor to the corresponding heading.

The sidebar updates automatically when:
- you switch to a different note
- you open a file
- you edit the current file

---

## What it does NOT do

This MVP **does not**:

- index the vault
- parse frontmatter or HTML comments
- generate block IDs, tags, or metadata
- modify the note in any way
- integrate with Dataview, Excalidraw, or any other plugin
- perform AI extraction
- create tasks, relations, or context packs

Those features belong to future MVP versions (B, C, D, E).

---

## Supported semantic types

| Emoji | Type | Sidebar label |
|-------|------|---------------|
| ✅ | decision | Decisions |
| ➡️ | action | Actions |
| ⚠️ | risk | Risks |
| ❓ | question | Questions |
| 🧠 | memory | Memories |

---

## How to install manually in Obsidian

### Prerequisites

- Obsidian 1.0.0 or later
- Node.js 18+ (for building from source)

### Build from source

```bash
git clone https://github.com/yannick-jolliet/yos-reader.git
cd yos-reader
npm install
npm run build
```

This produces `main.js` in the project root.

### Install in Obsidian

1. Open your vault folder in Finder / Explorer.
2. Navigate to `.obsidian/plugins/`.
3. Create a folder named `yos-reader`.
4. Copy these three files into `.obsidian/plugins/yos-reader/`:
   - `main.js`
   - `manifest.json`
   - (optional) `styles.css` if present
5. In Obsidian: **Settings → Community plugins → Installed plugins** → enable **Y-OS Reader**.
6. Click the **layers** icon in the left ribbon, or run **Open Y-OS Reader** from the command palette.

---

## How to test with test/testNote.md

1. Copy `test/testNote.md` into your Obsidian vault.
2. Open the file in Obsidian.
3. Open the Y-OS Reader panel (ribbon icon or command palette).

**Expected result:**

```
Decisions:  1  →  "Decision"
Actions:    1  →  "Action"
Risks:      1  →  "Risk"
Questions:  1  →  "Question"
Memories:   1  →  "Memory"
```

4. Click any item — the editor should scroll to the corresponding heading.
5. Switch to another note — the sidebar should update immediately (no stale data).

### Offline parser validation (no Obsidian required)

```bash
node test/validateParser.mjs
```

All three acceptance criteria (AC-1, AC-2, AC-6) are verified by this script.

---

## Known limitations

| # | Limitation | Impact |
|---|-----------|--------|
| L1 | Navigation uses `editor.setCursor` + `scrollIntoView`. In Reading View (non-editable), click navigation has no effect. | Low — switch to Editing View. |
| L2 | Live-preview / Source mode only. Reading View does not expose an editor object. | Low |
| L3 | Multi-codepoint emoji (e.g. ➡️ = U+27A1 + U+FE0F) are matched by exact string prefix. If a note uses the base codepoint only (U+27A1 without variation selector), it will not match. | Very low in practice. |
| L4 | No persistence — the sidebar re-parses on every refresh. For very large notes (>10,000 lines) there may be a brief repaint delay. | Negligible for typical notes. |
| L5 | Content preview is limited to the first non-empty line, truncated at 60 characters. | Cosmetic only. |

---

## How to extend semantic types

Open `src/parser/semanticTypes.ts` and add one entry to `SEMANTIC_TYPES`:

```typescript
"🔥": { type: "highlight", label: "Highlights" },
```

**No other file needs to change.** The parser reads the map at runtime; the sidebar reads the same map for group ordering. The new type will appear in the sidebar automatically.

---

## Future roadmap

| MVP | Feature |
|-----|---------|
| B | Additional semantic types, multi-panel layout |
| C | Excalidraw generation from semantic blocks |
| D | Startupizer — session bootstrap from Memory blocks |
| E | Action Layer — task creation and agent routing |

---

## License

MIT
