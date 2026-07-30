---
tool_id: YOT-70
tool_name: "Tally"
tool_type: "MCP Connector"
category: "Automation / Workflows"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://tally.so"
auth_credentials: "OAuth MCP"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-70 — Tally

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Automation / Workflows |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://tally.so |

## Business Value

Automatisation complète de la création et gestion de formulaires. Génération dynamique de formulaires d'onboarding, collecte de feedback, sondages. Extraction de charte graphique depuis URL pour alignement de marque.

## Capabilities

25 outils MCP : list_workspaces, list_forms, load_form, save_form, create_new_form, create_blocks, remove_blocks, move_blocks, update_text, configure_blocks, apply_logic, set_column_layout, update_styling, extract_brand, update_custom_css, fetch_submissions, fetch_insights, list_blocks. Système de Ledger (UUIDs). Logique conditionnelle DSL.

## Dependencies

Compte Tally (Free ou Pro). MCP server tally activé. OAuth via navigateur.

## Known Limits & Bugs

load_form obligatoire avant manipulation. CSS custom nécessite Tally Pro. fetch_insights : 401 si pas Pro, enums stricts requis. Auth OAuth bloquante (timeout 230s) — nécessite action manuelle navigateur.

## Workarounds & Lessons

Source: test live 21 Juin 2026. fetch_insights : utiliser period=all et include parmi metrics/visits/submissions/dimensions/drop-off. Auth : prévoir take_over_browser. Ledger : toujours appeler list_blocks avant toute modification structurelle.
