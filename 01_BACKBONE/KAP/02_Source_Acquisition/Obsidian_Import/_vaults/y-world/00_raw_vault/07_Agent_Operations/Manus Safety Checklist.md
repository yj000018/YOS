---
type: protocol
status: active
domain: Y-OS
project: Y-WORLD
created: 2026-05-28
updated: 2026-05-28
system_layer: system
automation_relevance: high
manus_actionable: true
---

# Manus Safety Checklist

Before performing any action inside Y-WORLD, Manus must verify compliance with this checklist.

- [ ] **C-1**: Am I deleting or overwriting any file? If yes, is there explicit user approval?
- [ ] **C-2**: Am I changing `.obsidian/`? If yes, is there a backup or Git commit?
- [ ] **C-3**: Am I exposing API keys, tokens, or personal secrets in markdown text?
- [ ] **C-4**: Is Git status clean before running this bulk operation?
- [ ] **C-5**: Is there a clear, manual fallback path if this automation fails?
