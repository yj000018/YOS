# session-synthesis

**Status:** Migrated to yos_memory (Phase 3)
**Canonical Store:** Git (Markdown + YAML)
**Projection:** Mem0
**Notion:** Deprecated (Reads only)

## Description
Generate a structured session card (fiche synthèse) for a single Manus session and archive it to Y-OS Memory (Git + Mem0).

## Usage
When the user asks to synthesize, archive, or summarize a specific session, or at the end of a session to capture its essence.

## Scripts
- `scripts/archive_to_notion.py` — Wraps `yos_memory.SessionStore` to archive cards. (Name kept for compatibility).
- `scripts/collect_session.py` — Collects session verbatim. Requires `MANUS_JWT_TOKEN` env var.
