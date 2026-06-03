# Build Reflowable EPUB with Pandoc

## Context
This workflow generates a standard reflowable EPUB using Pandoc. Best for text-only books.

## Prerequisites
- `manuscript.md` (cleaned)
- `metadata.yaml`
- `pandoc` CLI installed

## Steps

1. **Verify Pandoc**: `pandoc --version`
2. **Run Pandoc**: `pandoc manuscript.md -o output/book.epub --metadata-file=metadata.yaml`
3. **Validate EPUB**: `epubcheck output/book.epub`
4. **Fix validation errors** if any.

## Expected Outputs
- `book.epub`

## Next Actions
- Prepare KDP package
- Prepare Draft2Digital package
