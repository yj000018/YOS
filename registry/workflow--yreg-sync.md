---
id: yos-workflow--yreg-sync
title: workflow--yreg-sync
type: workflow
status: active
date: '2026-06-13'
version: 1.0.0
owner: Manus Y-OS
tags:
- sync
- parser
- supabase
- git
source_branch: y-os-doctrine
canonical: true
---


# Y-REG Sync — Git → Supabase Parser

This workflow reads all `.md` files in the `registry/` directory, parses their YAML frontmatter, and upserts the data into the `yreg_objects` table in Supabase.

## Direction
Git (source of truth) → Supabase (runtime cache)
NEVER the reverse.

## Trigger
Manual (MVP) → GitHub Actions (future)
