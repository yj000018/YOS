---
tool_id: YOT-04
tool_name: "OpenAI GPT-5"
tool_type: "REST API"
category: "LLM / AI"
status: "Production"
pricing: "Pay-as-you-go"
source_type: "Officiel"
source_url: "https://platform.openai.com/docs/"
auth_credentials: "API Key Env Var"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-04 — OpenAI GPT-5

| Champ | Valeur |
| :--- | :--- |
| **Type** | REST API |
| **Catégorie** | LLM / AI |
| **Statut** | Production |
| **Pricing** | Pay-as-you-go |
| **Source** | Officiel |
| **Auth** | API Key Env Var |
| **URL** | https://platform.openai.com/docs/ |

## Business Value

LLM multimodal de référence pour vision, code, et raisonnement complexe.

## Capabilities

Texte, code, images (vision), structured output, function calling, streaming.

## Dependencies

OPENAI_API_KEY, OPENAI_API_BASE env vars

## Known Limits & Bugs

Coûteux sur gros volumes. Pas de mémoire native cross-session.

## Workarounds & Lessons

Utiliser via OPENAI_API_KEY env var. Préférer pour tâches vision.
