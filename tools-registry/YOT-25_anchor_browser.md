---
tool_id: YOT-25
tool_name: "Anchor Browser"
tool_type: "REST API"
category: "Web Scraping / Automation"
status: "Production"
pricing: "Payant"
source_type: "Officiel"
source_url: "https://docs.anchorbrowser.io/"
auth_credentials: "API Key Env Var"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-25 — Anchor Browser

| Champ | Valeur |
| :--- | :--- |
| **Type** | REST API |
| **Catégorie** | Web Scraping / Automation |
| **Statut** | Production |
| **Pricing** | Payant |
| **Source** | Officiel |
| **Auth** | API Key Env Var |
| **URL** | https://docs.anchorbrowser.io/ |

## Business Value

Sessions browser cloud anti-bot pour scraping de sites protégés.

## Capabilities

Sessions browser managées, anti-bot, fetch de pages protégées.

## Dependencies

ANCHOR_API_KEY env var

## Known Limits & Bugs

Coûteux. Toujours inclure proxy + extra_stealth dans config session.

## Workarounds & Lessons

Config obligatoire: {browser:{extra_stealth:{active:true}}, session:{proxy:{active:true}}}
