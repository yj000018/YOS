---
tool_id: YOT-32
tool_name: "Slack"
tool_type: "MCP Connector"
category: "Project Management"
status: "A tester"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://api.slack.com/"
auth_credentials: "OAuth MCP"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# ⚪ YOT-32 — Slack

| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Project Management |
| **Statut** | A tester |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://api.slack.com/ |

## Business Value

Communication équipe Y-OS. Notifications, alertes, coordination.

## Capabilities

Messages, canaux, recherche, notifications.

## Dependencies

_N/A_

## Known Limits & Bugs

[Live test 2026-06-18] FAIL — OAuth expired. Requires Delete + Re-add in Manus Apps.

## Workarounds & Lessons

Toujours passer channel_types: public_channel,private_channel dans search.
