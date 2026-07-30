---
tool_id: YOT-66
tool_name: "1Password Y-OS"
tool_type: "CLI Tool"
category: "Security / Auth"
status: "Production"
pricing: "Payant"
source_type: "Officiel"
source_url: "https://developer.1password.com/docs/cli/"
auth_credentials: "1Password Item"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-66 — 1Password Y-OS

| Champ | Valeur |
| :--- | :--- |
| **Type** | CLI Tool |
| **Catégorie** | Security / Auth |
| **Statut** | Production |
| **Pricing** | Payant |
| **Source** | Officiel |
| **Auth** | 1Password Item |
| **URL** | https://developer.1password.com/docs/cli/ |

## Business Value

Vault centralisé pour tous les secrets Y-OS. Source of truth credentials.

## Capabilities

Lecture/écriture secrets, items, vaults via CLI op.

## Dependencies

op CLI, OP_SERVICE_ACCOUNT_TOKEN env var

## Known Limits & Bugs

Service account limité aux vaults autorisés.

## Workarounds & Lessons

Utiliser OP_SERVICE_ACCOUNT_TOKEN. Jamais copy-paste manuel de secrets.
