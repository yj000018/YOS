---
tool_id: YOT-75
tool_name: "Excalidraw"
tool_type: "Visual Diagramming / Whiteboard"
category: "Design / Visual"
status: "Préférence Yannick — PRIMARY"
pricing: "Open Source / Freemium (Plus)"
source_type: "Officiel"
source_url: "https://excalidraw.com/"
auth_credentials: "Optionnel (compte pour sync)"
tags: ["diagram", "whiteboard", "visual", "archetype", "excalidraw", "yannick-preference"]
migrated_from_notion: false
migration_date: "2026-08-04"
ll_ref: "00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml"
---

# ⭐ YOT-75 — Excalidraw

| Champ | Valeur |
| :--- | :--- |
| **Type** | Visual Diagramming / Whiteboard |
| **Catégorie** | Design / Visual |
| **Statut** | **⭐ PRÉFÉRENCE YANNICK — outil PRIMARY pour tous les diagrammes** |
| **Pricing** | Open Source (gratuit) / Plus (sync, collaboration) |
| **URL** | https://excalidraw.com |
| **Format fichier** | `.excalidraw` (JSON) |

## Description

Excalidraw est un outil de diagramme visuel à style "hand-drawn". Il est particulièrement adapté aux diagrammes d'architecture, aux cartes de modules, aux archétypes visuels et aux diagrammes Y-OS. Il supporte les icônes, les couleurs, les formes libres et l'édition interactive.

## Pourquoi c'est la préférence Yannick

Yannick travaille avec une approche archétypale : chaque module Y-OS doit avoir un nom, un acronyme, une icône et un code couleur. Excalidraw est le seul outil qui permet de représenter cette dimension visuelle/archétypale de façon naturelle et éditable.

## Règle d'utilisation dans Y-OS

```
DIAGRAM_TOOL_ROUTING:
  PRIMARY:  Excalidraw — diagrammes visuels, cartes de modules Y-OS,
                         archétypes, diagrammes interactifs/éditables
  FALLBACK: Mermaid (.mmd) — diagrammes automatisés, flowcharts,
                              séquences, pipelines CI/CD
  AVOID:    D2 (Manus sandbox — bug font rendering, voir YOT-74)
```

## Intégration Manus

Excalidraw ne dispose pas d'un MCP ou d'une API de génération automatique dans Manus. Les diagrammes sont créés :
1. **Manuellement** par Yannick dans https://excalidraw.com
2. **Via export** : Manus génère le JSON `.excalidraw` que Yannick importe
3. **Futur** : Génération automatique de JSON `.excalidraw` par Manus (à implémenter)

## Référence LL

`00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml` — LL-2026-08-04-003
