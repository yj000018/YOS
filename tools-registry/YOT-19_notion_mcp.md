---
tool_id: YOT-19
tool_name: "Notion MCP"
tool_type: "MCP Connector"
category: "Memory / Knowledge"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://developers.notion.com/"
auth_credentials: "OAuth MCP"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-19 — Notion MCP

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Memory / Knowledge |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://developers.notion.com/ |

## Business Value

Store principal Y-OS. Toute la mémoire structurée, projets, sessions, fiches outils.

## Capabilities

Créer/modifier pages et databases, recherche, gestion de contenu.

## Dependencies

_N/A_

## Known Limits & Bugs

Pas de tables HTML standard. Syntaxe Notion-flavored Markdown spécifique.

## Workarounds & Lessons

Utiliser notion-create-database avec SQL DDL. Tables: <table header-row> uniquement.
