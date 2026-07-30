---
tool_id: YOT-17
tool_name: "Mem0"
tool_type: "REST API"
category: "Memory / Knowledge"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://docs.mem0.ai/"
auth_credentials: "API Key Env Var"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-17 — Mem0

| Champ | Valeur |
| :--- | :--- |
| **Type** | REST API |
| **Catégorie** | Memory / Knowledge |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | API Key Env Var |
| **URL** | https://docs.mem0.ai/ |

## Business Value

Mémoire cross-session pour Y-OS. Permet à Manus de se souvenir entre sessions.

## Capabilities

Stockage/récupération de mémoires, recherche sémantique, tags.

## Dependencies

MEM0_API_KEY env var

## Known Limits & Bugs

Pas de structure hiérarchique. Recherche sémantique parfois imprécise.

## Workarounds & Lessons

Utiliser MEM0_API_KEY. Toujours tagger les mémoires (user_id + metadata).
