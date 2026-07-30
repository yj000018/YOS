---
tool_id: YOT-06
tool_name: "Google Gemini"
tool_type: "REST API"
category: "LLM / AI"
status: "Production"
pricing: "Pay-as-you-go"
source_type: "Officiel"
source_url: "https://ai.google.dev/gemini-api/docs"
auth_credentials: "API Key Env Var"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-06 — Google Gemini

| Champ | Valeur |
| :--- | :--- |
| **Type** | REST API |
| **Catégorie** | LLM / AI |
| **Statut** | Production |
| **Pricing** | Pay-as-you-go |
| **Source** | Officiel |
| **Auth** | API Key Env Var |
| **URL** | https://ai.google.dev/gemini-api/docs |

## Business Value

LLM optimal pour documents longs (1M tokens context) et tâches multimodales.

## Capabilities

Texte, code, images, vidéo, audio, long context, structured output.

## Dependencies

GEMINI_API_KEY env var

## Known Limits & Bugs

Moins précis que Claude sur raisonnement complexe.

## Workarounds & Lessons

Préférer gemini-2.5-flash pour long docs.
