---
id: "nc3htbfJQUCBdJy4xoJXit"
title: "[✓] Manus Share Link Extractor — Cross-Session Context Injection Fix"
date: "2026-05-07"
importance: "3"
depth_score: "substantial"
projects: ["Y-OS"]
tags: ["manus-extract", "scripting", "tooling", "context injection", "cross-session", "clipboard", "fix"]
summary: ""
executive_summary: "A Python script named `manus-extract` was successfully developed, tested, and deployed to extract context from Manus share links. This script provides flexible output options, including standard output, file saving, a compact format for token efficiency, and direct clipboard integration, addressing the user's need for optional context injection into other LLMs."
context_and_intent: "The user required an optional mechanism, potentially involving the clipboard, to extract context from Manus share links for injection into other large language models (LLMs), aiming to streamline their cross-LLM workflow."
what_was_done: "A Python script, `manus_share_extract.py`, was created and installed at `/home/ubuntu/tools/`. This script takes a Manus share link as input and extracts relevant conversational context. It was tested on a real link and confirmed to be operational, extracting approximately 1100 tokens. The script supports outputting the extracted content to standard output, saving it to a file, generating a compact version for token efficiency, and copying it directly to the clipboard (if `xclip` is available). It was also clarified that while user messages, Manus responses, and phase summaries are extracted, shell/terminal outputs are masked."
outputs_produced: [{"description": "A Python script designed to parse Manus share links and extract conversational context, including user messages, assistant responses, and phase summaries, with various output options.", "name": "manus_share_extract.py", "type": "Python Script"}]
key_decisions: ["Developed a dedicated Python script (`manus_share_extract.py`) to handle Manus share link extraction.", "Implemented multiple output modes for the script: standard output, file saving, compact format, and clipboard integration (if `xclip` is available).", "Explicitly documented the known limitations regarding what content can and cannot be extracted from Manus sessions."]
lessons_learned: {"discoveries": ["The script successfully extracts approximately 1100 tokens from a real Manus share link.", "The script effectively extracts user messages, Manus assistant responses, and phase summaries."], "failed_or_suboptimal": ["The inability to extract shell/terminal outputs from Manus sessions is a limitation that could impact the completeness of extracted context in some scenarios."], "worked_well": ["The developed script is operational and was successfully tested on a real Manus share link.", "The script provides versatile usage options, catering to different user preferences for output (stdout, file, compact, clipboard).", "The compact format option is effective for reducing token count when pasting into other LLMs."]}
challenges_and_blockers: ["Shell/terminal outputs are masked and cannot be extracted by the script, which is a known and non-circumventable limitation."]
open_questions: []
next_steps: ["The user can now integrate the `manus_share_extract.py` script into their workflow to facilitate context injection into other LLMs.", "Monitor user feedback for potential enhancements or additional features related to context extraction."]
url: "https://manus.im/app/task/nc3htbfJQUCBdJy4xoJXit"
---

# [✓] Manus Share Link Extractor — Cross-Session Context Injection Fix

| Field | Value |
|-------|-------|
| **Session ID** | `nc3htbfJQUCBdJy4xoJXit` |
| **Date** | 2026-05-07 00:30 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/nc3htbfJQUCBdJy4xoJXit](https://manus.im/app/sessions/nc3htbfJQUCBdJy4xoJXit) |
| **Messages** | 4 user · 6 assistant · 20 total |

## Initial Prompt

Oui, injection optionnelle(dS clipboard--° parfois je pate dans autre llm

## First Response

## ✅ `manus-extract` — Script opérationnel

**Testé sur ton lien réel.** Fonctionne. ~1100 tokens extraits.

---

### 📦 Script installé

`/home/ubuntu/tools/manus_share_extract.py`

---

### 🔧 Usage

```bash
# Affichage stdout (pour coller dans Manus)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX

# Sauvegarde fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --out context.md

# Format compact (moins de tokens — pour Claude/GPT/Gemini)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compact

# Clipboard (si xclip dispo — sinon affiche stdout)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --clipboard

# Combiné : compact + fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compact --out ctx.md
```

---

### ⚠️ Limites connues (non contournables)

| Ce qui est extrait | Ce qui est masqué |
|---|---|
| ✅ Messages user + Manus | ❌ Outputs shell/terminal |
| ✅ Résumés de phases 

## Conversation Summary

> **User:** Oui, injection optionnelle(dS clipboard--° parfois je pate dans autre llm

> **User:** A ca https://manus.im/share/nc3htbfJQUCBdJy4xoJXit

> **User:** Partager un lien de session Manus a manus (cross seSsion ref

> **Manus:** ## ✅ `manus-extract` — Script opérationnel

**Testé sur ton lien réel.** Fonctionne. ~1100 tokens extraits.

---

### 📦 Script installé

`/home/ubuntu/tools/manus_share_extract.py`

---

### 🔧 Usage

```bash
# Affichage stdout (pour coller dans Manus)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX

# Sauvegarde fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --out context.md

# Format compact (moins de tokens — pour Claude/GPT/Gemini)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compact

# Clipboard (si xclip dispo — sinon affiche stdout)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --clipboard

# Combiné : compact + fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compa...

> **Manus:** Construction du script — extraction Firecrawl + copie clipboard + injection contexte.

## Full Verbatim

<details>
<summary>Expand full conversation (10 messages)</summary>

**[1778115110417] MANUS:** ## ✅ `manus-extract` — Script opérationnel

**Testé sur ton lien réel.** Fonctionne. ~1100 tokens extraits.

---

### 📦 Script installé

`/home/ubuntu/tools/manus_share_extract.py`

---

### 🔧 Usage

```bash
# Affichage stdout (pour coller dans Manus)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX

# Sauvegarde fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --out context.md

# Format compact (moins de tokens — pour Claude/GPT/Gemini)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compact

# Clipboard (si xclip dispo — sinon affiche stdout)
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --clipboard

# Combiné : compact + fichier
python3 ~/tools/manus_share_extract.py https://manus.im/share/XXXX --compact --out ctx.md
```

---

### ⚠️ Limites connues (non contournables)

| Ce qui est extrait | Ce qui est masqué |
|---|---|
| ✅ Messages user + Manus | ❌ Outputs shell/terminal |
| ✅ Résumés de phases ...
**[1778114928175] MANUS:** Construction du script — extraction Firecrawl + copie clipboard + injection contexte.
**[1778114925118] USER:** Oui, injection optionnelle(dS clipboard--° parfois je pate dans autre llm
**[1778114801240] MANUS:** ## 🔍 Diagnostic — Cross-session reference via `manus.im/share/`

### Cause racine identifiée

La page `manus.im/share/...` est une **SPA React (Next.js)** qui charge le contenu **dynamiquement via JS côté client**. Quand Manus (ou n'importe quel bot/crawler) tente de la lire :

- Le HTML brut retourné = **squelette vide** (pas de contenu de session)
- L'API directe `/api/share/...` retourne **503**
- Firecrawl (avec JS rendering) récupère le contenu **mais** rencontre un `statusCode: 500` côté Manus + cette ligne critique :

> `"Connector output is hidden in shared sessions for privacy reasons"`

**→ Manus masque délibérément les outputs des outils dans les sessions partagées.** C'est une restriction de sécurité/privacy côté plateforme, pas un bug réseau.

---

### Ce que Firecrawl peut lire (workaround ✅)

Firecrawl avec `waitFor: 3000` arrive à extraire **le texte des messages** (user + Manus) mais **pas les outputs des outils** (shell, browser, etc.).

---

### Workarounds — 3 optio...
**[1778114625720] MANUS:** Je teste l'accès à ce lien maintenant.
**[1778114622731] USER:** A ca https://manus.im/share/nc3htbfJQUCBdJy4xoJXit
**[1778113845223] MANUS:** OK, cross-session reference via lien Manus.

Symptôme exact quand Manus essaie de lire le lien ?

① Erreur 403/401 (accès refusé)
② Page vide / contenu non chargé
③ Manus ignore le lien / ne le traite pas
④ Autre — décris

Et le lien ressemble à quoi ? `app.manus.im/share/...` ou autre format ?
**[1778113839942] USER:** Partager un lien de session Manus a manus (cross seSsion ref
**[1778113819006] MANUS:** Clarification rapide :

Quand tu dis "partager une session Manus avec Manus" — tu veux dire quoi exactement ?

**① Copier/exporter le contenu d'une session Manus** (historique, messages) pour l'injecter dans une nouvelle session ?

**② Partager un lien de session Manus** avec quelqu'un d'autre (ou une autre instance) qui ne peut pas le lire ?

**③ Autre chose** — ex. charger le contexte d'une session précédente dans la session courante ?

Et "qui n'arrive jamais à lire" → c'est quoi le symptôme exact ? Lien inaccessible ? Contenu vide ? Erreur ?
**[1778113810549] USER:** Souvnt Veux partager une session manus avec manus: qui n'arrive jmais a lire... Fix



</details>