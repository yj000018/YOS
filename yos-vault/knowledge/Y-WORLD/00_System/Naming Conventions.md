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

# Naming Conventions

Consistent naming conventions ensure that notes are easy to find, links are predictable, and automation scripts can parse the vault reliably.

## 1. Folder Structure
* System, Cockpit, Maps, Dashboards, and Registries use two-digit prefixes: `00_System/`, `01_Cockpit/`, `02_Maps/`, `03_Dashboards/`.
* Primary domains use two-digit prefixes starting from 20: `20_Life/`, `30_Knowledge/`, `50_Projects/`.
* Specialized sub-domains use sub-numbers: `70_CasaTAO/`, `71_ARC_Anandaz/`.

## 2. Note Names
* **Dashboards**: Must end with `Dashboard` (e.g., `03_Dashboards/Life Dashboard.md`).
* **Maps**: Must end with `MAP` in uppercase (e.g., `02_Maps/Y-OS MAP.md`).
* **Templates**: Must start with `Template -` (e.g., `04_Templates/Template - K-Card.md`).
* **K-Cards**: Use clean, concise, noun-based titles (e.g., `40_K-Cards/Cognitive OS.md`).
* **Projects**: Use kebab-case or Title Case (e.g., `50_Projects/Y-WORLD-Vault.md`).
* **Logs**: Must end with `Log` (e.g., `50_Projects/Y-WORLD Log.md`).
