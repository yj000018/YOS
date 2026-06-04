---
type: world-node
status: active
domain: Y-WORLD
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Manus Operations

This document defines how Manus, the autonomous cognitive agent, operates within the Y-WORLD Obsidian vault.

## 1. Interaction Interface
Manus interacts with the vault primarily using:
1. **Markdown Files**: Reading, writing, and editing files directly.
2. **YAML Frontmatter**: Reading and updating metadata for queryability.
3. **Advanced URIs / Local REST API**: Automating tasks programmatically.
4. **Git Version Control**: Committing changes and maintaining vault integrity.

## 2. Command Protocol
Manus scans the `07_Agent_Operations/Manus Task Queue.md` for active instructions and posts status updates in the `07_Agent_Operations/Manus Change Log.md`.

## 3. Operational Guardrails
* **No Blind Rewrites**: When editing files, use precise edits or append logs. Avoid rewriting massive documents unless requested.
* **Metadata Hygiene**: Always preserve the existing YAML frontmatter when updating a note.
* **Strict Pathing**: Always use absolute paths within the vault (e.g., `01_Cockpit/HOME.md`) to avoid broken links.
