---
session_id: e1go2qvypP9x5K8HiGjzXU
title: "[✓] LLM Router Skill v1.1 — OpenRouter + Kimi K2.6 + Provider Pricing Strategy"
date: 2026-06-25 16:56 UTC
url: https://manus.im/app/sessions/e1go2qvypP9x5K8HiGjzXU
project_id: none
user_messages: 2
assistant_messages: 6
total_messages: 15
processed: true
---

# [✓] LLM Router Skill v1.1 — OpenRouter + Kimi K2.6 + Provider Pricing Strategy

| Field | Value |
|-------|-------|
| **Session ID** | `e1go2qvypP9x5K8HiGjzXU` |
| **Date** | 2026-06-25 16:56 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/e1go2qvypP9x5K8HiGjzXU](https://manus.im/app/sessions/e1go2qvypP9x5K8HiGjzXU) |
| **Messages** | 2 user · 6 assistant · 15 total |

## Initial Prompt

Tu me propose. Al instant se remplacer la skil….

## First Response

Exact — quand j'envoie le `SKILL.md` en pièce jointe, le système te propose automatiquement une carte avec **"Add to My Skills"** (= remplace/met à jour le skill existant) ou **"Download"**.

**C'est le bon moment de cliquer "Add to My Skills"** — ça va remplacer le `llm-router` v1.0 par la v1.1 avec OpenRouter + Kimi K2.6 + Provider Pricing Strategy.

Le fichier ci-joint est prêt et validé (`Skill is valid!`).

## Conversation Summary

> **User:** Tu me propose. Al instant se remplacer la skil….

> **User:** Skill exist already I replace it?

> **Manus:** Exact — quand j'envoie le `SKILL.md` en pièce jointe, le système te propose automatiquement une carte avec **"Add to My Skills"** (= remplace/met à jour le skill existant) ou **"Download"**.

**C'est le bon moment de cliquer "Add to My Skills"** — ça va remplacer le `llm-router` v1.0 par la v1.1 avec OpenRouter + Kimi K2.6 + Provider Pricing Strategy.

Le fichier ci-joint est prêt et validé (`Skill is valid!`).

> **Manus:** Je relis le skill-creator pour comprendre le workflow exact de remplacement.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1782413318668] MANUS:** Exact — quand j'envoie le `SKILL.md` en pièce jointe, le système te propose automatiquement une carte avec **"Add to My Skills"** (= remplace/met à jour le skill existant) ou **"Download"**.

**C'est le bon moment de cliquer "Add to My Skills"** — ça va remplacer le `llm-router` v1.0 par la v1.1 avec OpenRouter + Kimi K2.6 + Provider Pricing Strategy.

Le fichier ci-joint est prêt et validé (`Skill is valid!`).
**[1782413306932] MANUS:** Je relis le skill-creator pour comprendre le workflow exact de remplacement.
**[1782413302721] USER:** Tu me propose. Al instant se remplacer la skil….
**[1782413264050] MANUS:** **Non, ne remplace pas le skill — il a été mis à jour en place (v1.0 → v1.1).**

Le skill `llm-router` existant a été modifié directement :

- Frontmatter corrigé (clés invalides supprimées, description enrichie)
- Section `## Provider Pricing Strategy` ajoutée
- `OPENROUTER_API_KEY` ajouté aux dépendances
- Validation : **`Skill is valid!`** ✅

Les nouveaux fichiers (`llm-matrix.yaml`, `openrouter-kimi-k2.py`) sont des **ressources additives** dans le même répertoire — ils n'écrasent rien d'existant.

Rien à remplacer manuellement. Tout est en place.
**[1782413205621] MANUS:** Je vérifie l'état actuel du skill llm-router avant de décider.
**[1782413202066] USER:** Skill exist already I replace it?
**[1782406754064] MANUS:** ## LLM Matrix — Mise à jour complète ✅

Tous les fichiers sont dans `/home/ubuntu/skills/llm-router/`. Validation : **4/4 assertions passées**, zéro clé API exposée.

---

### Changements effectués

| Fichier | Action | Contenu clé |
|---|---|---|
| `SKILL.md` | Mis à jour (v1.0 → v1.1) | Section `## Provider Pricing Strategy` + règle clé + tableau comparatif + note volume + `OPENROUTER_API_KEY` dans les dépendances |
| `llm-matrix.yaml` | **Créé** (nouveau) | 7 providers (anthropic, openai, google, perplexity, xai, **openrouter**, **manus**) + 8 règles de routage + task_routing matrix |
| `openrouter-kimi-k2.py` | **Créé** (nouveau) | Snippet Python complet : `call_kimi_k2()`, fallback Moonshot direct, cost_tags, auth via `OPENROUTER_API_KEY` env var |

---

### Règles de routage actives

| Famille | Provider | Logique |
|---|---|---|
| `kimi`, `llama`, `deepseek`, `qwen` | `openrouter` | Open-weight — concurrence des hébergeurs |
| `gpt`, `claude`, `gemini` | `openai` / `anthropic` /...
**[1782406605107] MANUS:** Je lis le fichier et optimise avant d'exécuter.



</details>
