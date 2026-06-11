---
slug: command--yos-launcher
name: "/YOS"
type: command
status: active
visibility: public
registration_stage: registry
version: "1.0.0"
description: "Main Y-OS launcher command. Displays all public and advanced objects from Y-REG and allows navigation and execution."
tags: ["launcher", "command", "yos", "cli"]
git_path: "registry/command--yos-launcher.md"
---

# /YOS — Y-OS Launcher Command

The primary entry point to Y-OS. Queries Supabase (runtime cache) for all visible objects and renders a structured text menu. Falls back to Git/Markdown parsing if Supabase is unavailable.

## Visibility filter
- Default: public objects only
- With --advanced flag: public + advanced objects
- With --all flag: all objects (requires admin)

## Fallback
If Supabase unreachable → parse registry/*.md directly
