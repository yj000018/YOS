# Build Premium Print PDF with Typst

## Context
This workflow generates a high-quality, print-ready PDF using Typst.
Typst is preferred over Pandoc for print because it offers superior typographic control and layout capabilities.

## Prerequisites
- `manuscript.md` (cleaned and validated)
- `template.typ` (Typst template for the book design)
- `typst` CLI installed

## Steps

1. **Verify Typst Installation**
   Run `typst --version`. If not installed, prompt user to install via `cargo install typst-cli` or download binary.

2. **Prepare Build Directory**
   Create a clean build directory for the PDF generation.

3. **Compile Typst Document**
   Run: `typst compile template.typ output/print_edition.pdf`

4. **Validate PDF Specs**
   Check that the generated PDF meets print requirements (e.g., correct trim size, embedded fonts).

5. **Generate Digital Version (Optional)**
   Run a second compile with a screen-optimised profile if a digital PDF is also requested.

## Expected Outputs
- `print_edition.pdf`
- `digital_edition.pdf` (optional)

## Next Actions
- Build EPUB reflowable
- Prepare KDP package
- Upload to distribution platforms
