---
type: registry
status: active
domain: Y-OS
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Workflow Registry

This registry tracks active automation workflows running across Y-WORLD.

| ID | Name | Trigger | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| WF-001 | Notion Sync | Cron (Hourly) | Sync Notion projects with Obsidian | `PLANNED` |
| WF-002 | Git Auto-Backup | Cron (60m) | Auto-commit and push to GitHub | `PLANNED` |
| WF-003 | Inbox Sorting | Event (New File) | Sort `10_Inbox/` using LLM classifier | `PLANNED` |
