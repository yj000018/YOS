---
tool_id: YOT-05
tool_name: "Anthropic Claude"
tool_type: "REST API"
category: "LLM / AI"
status: "Production"
pricing: "Pay-as-you-go"
source_type: "Officiel"
source_url: "https://docs.anthropic.com/"
auth_credentials: "API Key Env Var"
tags: []
migrated_from_notion: true
migration_date: "2026-07-30"
---

# 🟢 YOT-05 — Anthropic Claude

| Champ | Valeur |
| :--- | :--- |
| **Type** | REST API |
| **Catégorie** | LLM / AI |
| **Statut** | Production |
| **Pricing** | Pay-as-you-go |
| **Source** | Officiel |
| **Auth** | API Key Env Var |
| **URL** | https://docs.anthropic.com/ |

## Business Value

LLM défaut Y-OS pour texte long, raisonnement, code et tâches structurées.

## Capabilities

Génération de texte, conversation multi-tours, Tool Calling (JSON structuré), streaming SSE, System Prompt / Persona, Vision (images base64/URL). Modèle actif : claude-opus-4-5-20251101 (SDK v0.109.2, test live 2026-06-18).

## Dependencies

ANTHROPIC_API_KEY env var

## Known Limits & Bugs

Pas de génération images native (FLUX/Replicate). Pas TTS/audio (ElevenLabs). claude-3-5-sonnet et claude-3-haiku retournent 404 sur clé Y-OS. claude-3-opus-20240229 deprecated EOL jan 2026. temperature ignoré silencieusement sur modèles récents.

## Workarounds & Lessons

Modèle actif Y-OS : claude-opus-4-5-20251101. tool_choice forcer type:tool+name pour extraction JSON garantie. stop_reason:max_tokens -> augmenter max_tokens. Source: test live 2026-06-18.
