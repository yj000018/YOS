# Example Session — Book-Factory

This document demonstrates a complete Y-Menu session using the Book-Factory module.

---

## Step 1 — User opens Y-Menu

**User:** Open Y-Menu

**Y-Menu:**
```
╭──────────────────────────────────────────╮
│                  Y-MENU                  │
│    Cognitive Orchestration Interface     │
╰──────────────────────────────────────────╯

1️⃣ 📚 Book-Factory / Y-Publishing Factory
2️⃣ 🔬 Research Factory
3️⃣ 🧠 Memory Factory
...

Commands: home · back · status · help · diagnose
Reply with a number or describe your goal.
```

---

## Step 2 — User selects Book-Factory

**User:** 1

**Y-Menu:**
```
╭──────────────────────────────────────────╮
│           Y-PUBLISHING FACTORY           │
│    AI-native book production cockpit     │
╰──────────────────────────────────────────╯

Context
• Active module: book-factory
• Active book: Visual Reality
• Status: Manuscript imported · 7 exports pending

Recommended next action ⭐
Build outputs.

1️⃣ 🏗 Build outputs
2️⃣ 🤖 Generate cover design brief 🤖
   ↳ Cover is missing. Required for KDP and IngramSpark uploads.
...
```

---

## Step 3 — User asks "produce Kindle version"

**User:** produce Kindle version

**Y-Menu (Intent Router):**
```
╭────────────────────────────────────────────╮
│           INTENT ROUTER                    │
╰────────────────────────────────────────────╯

Goal detected: "produce kindle version"
Best match: Produce Kindle-ready package
Confidence: 90%

Decision paths:
  1. Book type: visual_essay → Fixed-layout EPUB workflow
  2. Use HTML/CSS/SVG engine → EPUB FXL → Kindle validation
  3. Workflow: book-factory/build-epub-fxl.md
```

---

## Step 4 — Y-Menu infers book type from state

Since `book_type: visual_essay` is in the state, Y-Menu skips the clarification question and directly recommends the fixed-layout EPUB path.

---

## Step 5 — Y-Menu outputs workflow

**Y-Menu (Workflow Composer):**
```
Goal: Produce Kindle-ready package (visual book)
Why: Book type "visual_essay" requires fixed-layout EPUB for Kindle.

⚠️  Missing inputs: cover image

Steps:
  1. Prepare HTML/CSS/SVG page layouts [html-css-svg-fxl-engine]
  2. Generate fixed-layout EPUB [epub-fxl-builder] → epub_fixed_layout
  3. Validate EPUB [epubcheck] → epub_validated
  4. Preview in Kindle Previewer [kindle-previewer]
  5. Generate KDP upload checklist [kdp-checklist] → kdp_package

Expected outputs: epub_fixed_layout, kdp_package
```

---

## Step 6 — User generates Lovable mini-site

**User:** create mini-site for my book

**Y-Menu:**
```
Decision paths:
  1. Use Lovable if: one book · simple landing page · speed matters
  2. Use Astro if: multi-book catalogue · industrial platform · long-term site

Workflow: Generate Lovable mini-site
Steps:
  1. Generate Lovable prompt package → lovable_site_prompt
  2. Generate assets package → lovable_assets
  3. Generate purchase/download section copy → purchase_copy
  4. Generate SEO metadata → seo_metadata
```

---

## Step 7 — Y-Menu suggests distribution package

After the Lovable site is generated, Y-Menu automatically suggests:

```
Recommended next action ⭐
Prepare Amazon KDP package.

1️⃣ 📦 Prepare Amazon KDP package
2️⃣ 📚 Prepare IngramSpark package
3️⃣ 📱 Prepare Draft2Digital package
```
