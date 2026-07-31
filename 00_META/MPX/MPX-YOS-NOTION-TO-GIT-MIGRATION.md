# MPX: YOS-NOTION-TO-GIT-MIGRATION

**Date**: 2026-07-31
**Author**: Manus AI
**Status**: DRAFT
**Prerequisite**: MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR must be completed and merged.

## Objective

Migrate all existing session cards from the legacy Notion database ("Manus Memory — Sessions") into the new canonical Git store (`00_META/SESSIONS/`) using the `yos_memory.LegacyNotionReader` and `yos_memory.SessionStore`.

## Scope

- Read all pages from Notion DB `0720db9b-5e1d-41a2-bd0c-6721fe0dab94`.
- Convert Notion properties into `yos-memory/v1` YAML frontmatter.
- Convert Notion page content (blocks) into standard Markdown.
- Save each session as a `.md` file in `00_META/SESSIONS/YYYY-MM/UID.md`.
- **Do NOT push to Mem0** (to avoid duplicating what was already pushed via the old `mem0-sync` skill).
- **Do NOT delete** the Notion pages (keep them as read-only archive).

## Execution Phases

### Phase 1: Preparation & Dry Run
1. Create a script `scripts/yos-llm-pipeline/migrate_notion_to_git.py`.
2. Initialize `LegacyNotionReader` to fetch all page IDs from the database (handling pagination).
3. Select 5 random pages for a dry run.
4. For each page, extract properties (UID, Title, Date, Themes, etc.) and content.
5. Use `SessionStore` (with Mem0 disabled) to save the Markdown files.
6. **GATE: GO_MIGRATION_DRY_RUN**

### Phase 2: Full Migration
1. Run the script on all remaining pages (~325+ sessions).
2. Handle Notion API rate limits (HTTP 429) with exponential backoff.
3. Save progress in a local state file (`migration_state.json`) to resume if interrupted.
4. **GATE: GO_MIGRATION_FULL**

### Phase 3: Verification & Cleanup
1. Count the number of `.md` files generated in `00_META/SESSIONS/`.
2. Compare the count with the total number of pages in the Notion database.
3. Commit all `.md` files to the YOS Git repository.
4. Push to GitHub.
5. **GATE: GO_MIGRATION_COMPLETE**

## Technical Specifications

### Disable Mem0 Push
The `SessionStore.archive_session()` method accepts a `push_to_mem0` boolean parameter (defaults to True). During this migration, it MUST be explicitly set to `False`.

```python
store.archive_session(
    uid=session_uid,
    title=session_title,
    summary=session_summary,
    metadata=session_metadata,
    full_markdown=markdown_content,
    push_to_mem0=False  # CRITICAL
)
```

### Notion Markdown Conversion
The Notion API returns blocks, not Markdown. Use the `manus-mcp-cli` or a Python library like `notion2md` to convert the page blocks into clean Markdown before saving.

## Expected Output
A fully populated `00_META/SESSIONS/` directory containing hundreds of Markdown files, each with a valid `yos-memory/v1` frontmatter, fully committed to the YOS repository.
