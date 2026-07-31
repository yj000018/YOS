# memory-manager

**Status:** Migrated to yos_memory (Phase 3)
**Canonical Store:** Git (Markdown + YAML)
**Projection:** Mem0
**Notion:** Deprecated (Reads only)

## Description
Persistent memory system for storing conversations, projects, knowledge, and preferences.

## Usage
When user requests to store information, archive conversations, load project context, search past discussions, create/update projects, or manage memory.

## Scripts
- `scripts/archive_conversation.py` — Wraps `yos_memory.SessionStore` to archive full conversations.
