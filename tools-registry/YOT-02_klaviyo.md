---
tool_id: YOT-02
tool_name: "Klaviyo"
tool_type: "MCP Connector"
category: "Email Marketing"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://developers.klaviyo.com/en/docs/welcome"
auth_credentials: "OAuth MCP"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-02 — Klaviyo

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Email Marketing |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://developers.klaviyo.com/en/docs/welcome |

## Business Value

Automatiser campagnes email/SMS, segmentation avancée, analytics de délivrabilité pour Y-OS outbound.

## Capabilities

39 outils MCP: profils, listes, segments, campagnes, métriques, templates, flows, catalogues.

## Dependencies

Clé API privée (Full Access) dans Klaviyo Settings.

## Known Limits & Bugs

create_list absent du MCP. assign-template absent API REST. Envoi bloqué si profil sans consentement SUBSCRIBED.

## Workarounds & Lessons

create_list via REST POST /lists. Template via HTML embarqué dans message. Forcer consentement via profile-subscription-bulk-create-jobs.
