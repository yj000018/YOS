---
tool_id: YOT-49
tool_name: "Mermaid Chart"
tool_type: "MCP Connector"
category: "Design / Visual"
status: "Actif — FALLBACK système (diagrammes automatisés)"
ll_ref: "00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://mermaid.js.org/"
auth_credentials: "OAuth MCP"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟡 YOT-49 — Mermaid Chart

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Design / Visual |
| **Statut** | **🟡 FALLBACK système — diagrammes automatisés** |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://mermaid.js.org/ |

## Business Value

Diagrammes techniques pour documentation Y-OS.

## Capabilities

Validation syntaxe, rendu PNG/SVG, gestion projets.

## Dependencies

_N/A_

## Known Limits & Bugs

Aucun bug connu dans Manus sandbox. `manus-render-diagram` fonctionne avec les fichiers `.mmd`.

## Workarounds & Lessons

**Rôle dans le routing diagrammes Y-OS :**
```
PRIMARY:  Excalidraw (YOT-75) — préférence Yannick
FALLBACK: Mermaid (ce tool) — diagrammes automatisés, flowcharts, pipelines
AVOID:    D2 (YOT-74) — bug font rendering dans Manus sandbox
```

Référence LL : `00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml` — LL-2026-08-04-003
