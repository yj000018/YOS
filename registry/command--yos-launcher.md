---
id: yos-command--yos-launcher
title: command--yos-launcher
type: command
status: active
date: '2026-06-13'
version: 1.0.0
owner: Manus Y-OS
tags:
- launcher
- command
- yos
- cli
source_branch: y-os-doctrine
canonical: true
---


# /YOS — Y-OS Launcher Command

The primary entry point to Y-OS. Queries Supabase (runtime cache) for all visible objects and renders a structured text menu. Falls back to Git/Markdown parsing if Supabase is unavailable.

## Visibility filter
- Default: public objects only
- With --advanced flag: public + advanced objects
- With --all flag: all objects (requires admin)

## Fallback
If Supabase unreachable → parse registry/*.md directly
