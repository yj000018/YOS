---
slug: workflow--yreg-sync
name: "Y-REG Sync"
type: workflow
status: active
visibility: advanced
registration_stage: registry
version: "1.0.0"
description: "Parses all Markdown/YAML files in the Y-REG Git repository and upserts them into the Supabase runtime cache. Unidirectional: Git → Supabase only."
tags: ["sync", "parser", "supabase", "git"]
git_path: "registry/workflow--yreg-sync.md"
---

# Y-REG Sync — Git → Supabase Parser

This workflow reads all `.md` files in the `registry/` directory, parses their YAML frontmatter, and upserts the data into the `yreg_objects` table in Supabase.

## Direction
Git (source of truth) → Supabase (runtime cache)
NEVER the reverse.

## Trigger
Manual (MVP) → GitHub Actions (future)
