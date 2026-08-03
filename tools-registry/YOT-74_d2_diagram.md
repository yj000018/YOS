---
tool_id: YOT-74
tool_name: "D2 Diagram"
tool_type: "CLI / Diagramming"
category: "Design / Visual"
status: "Bug connu — éviter dans Manus"
pricing: "Open Source"
source_type: "Officiel"
source_url: "https://d2lang.com/"
auth_credentials: "Aucune"
tags: ["diagram", "architecture", "cli", "d2", "bug"]
migrated_from_notion: false
migration_date: "2026-08-04"
ll_ref: "00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml"
---

# 🔴 YOT-74 — D2 Diagram

| Champ | Valeur |
| :--- | :--- |
| **Type** | CLI / Diagramming |
| **Catégorie** | Design / Visual |
| **Statut** | **Bug connu — éviter dans Manus sandbox** |
| **Pricing** | Open Source (gratuit) |
| **CLI** | `/usr/local/bin/d2` v0.7.1 |

## Description

D2 est un langage de diagramme déclaratif (comme Mermaid mais plus puissant). Il supporte des layouts avancés (ELK, DAGRE), des styles riches, des shapes personnalisés et des animations.

## Statut dans Manus Sandbox

**⛔ Bug critique : font rendering cassé**

- `d2 CLI` compile `.d2 → .svg` correctement
- `manus-render-diagram` avec `.d2` échoue (Playwright 1.47.2 introuvable sur CDN)
- `cairosvg` (seul convertisseur SVG→PNG disponible) ne supporte pas les fonts woff2 embarquées par D2
- **Résultat** : shapes rendues, tous les labels texte invisibles (tirets uniquement)

## Règle d'utilisation

```
MANUS SANDBOX: ❌ Ne pas utiliser pour des diagrammes avec labels
FALLBACK: Mermaid (.mmd via manus-render-diagram)
PRÉFÉRENCE YANNICK: Excalidraw (voir YOT-75)
```

## Référence LL

`00_META/LESSONS-LEARNED/2026-08-04_diagram-tools-routing.yaml` — LL-2026-08-04-001 et LL-2026-08-04-002
