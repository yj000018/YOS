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

# Manus Operating Manual

## 1. Principles
1. **Never delete files** without explicit instruction.
2. **Never modify `.obsidian/`** without backup or Git commit.
3. **Document all structural changes** in [[Manus Change Log]].
4. **Prefer creating notes and dashboards** before touching config files.
5. **Keep Y-WORLD navigable and simple**.
6. **Avoid plugin sprawl**.
7. **Distinguish core, optional, experimental, and deprecated**.
8. **Every automation must have a fallback manual path**.
9. **Every generated structure must be human-readable**.
10. **Obsidian remains portable markdown-first infrastructure**.

## 2. Interaction Protocol
Manus should manage Obsidian using, in this order:
1. Markdown files
2. Templates
3. Dataview-compatible metadata
4. Git commits
5. Advanced URI links
6. Local REST API if enabled
7. Shell Commands only if approved
