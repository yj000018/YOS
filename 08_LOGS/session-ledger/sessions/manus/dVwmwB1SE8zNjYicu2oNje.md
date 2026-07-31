---
session_id: dVwmwB1SE8zNjYicu2oNje
title: "[✓] Karpathy's AutoResearch ML Agent Experiment - Status Review and Community Findings"
date: 2026-03-11 05:40 UTC
url: https://manus.im/app/sessions/dVwmwB1SE8zNjYicu2oNje
project_id: none
user_messages: 1
assistant_messages: 2
total_messages: 7
processed: true
---

# [✓] Karpathy's AutoResearch ML Agent Experiment - Status Review and Community Findings

| Field | Value |
|-------|-------|
| **Session ID** | `dVwmwB1SE8zNjYicu2oNje` |
| **Date** | 2026-03-11 05:40 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/dVwmwB1SE8zNjYicu2oNje](https://manus.im/app/sessions/dVwmwB1SE8zNjYicu2oNje) |
| **Messages** | 1 user · 2 assistant · 7 total |

## Initial Prompt

https://youtu.be/tUkD0oj92Qg?is=_5D_wmApepEQwcq3

Status about this experiment?
Search also from community 
Some gray discoveries and progresses made with this approach?

## First Response

## autoresearch — Karpathy, Mars 2026

**Sujet identifié :** `karpathy/autoresearch` — boucle de recherche ML autonome sur single-GPU, publiée le 7 mars 2026. 630 lignes. MIT License. 23.7k stars en 4 jours.

---

### Principe

Un agent AI reçoit un setup d'entraînement LLM réel (`train.py` = modèle GPT + optimizer Muon/AdamW). Il modifie le code, entraîne 5 minutes, mesure `val_bpb`, garde si ça améliore, recommence. L'humain programme uniquement `program.md` — la "politique de recherche". L'agent exécute.

---

### Résultats officiels (Karpathy, H100, 2 jours)

| Métrique | Résultat |
|---|---|
| Expériences autonomes | ~700 |
| Améliorations conservées | ~20 |
| Gain val_bpb | -11% |
| "Time to GPT-2" | 2.02h → 1.80h |
| Transfert vers modèle plus grand | ✅ Confirmé |

---

### Ce que l'agent a réellement trouvé (session report auto-posté par l'agent, Discussion #32)

**Top découvertes :**
- **Réduire le batch size** (524K → 262K) = gain le plus important. Plus de steps > plus de pa

## Conversation Summary

> **User:** https://youtu.be/tUkD0oj92Qg?is=_5D_wmApepEQwcq3

Status about this experiment?
Search also from community 
Some gray discoveries and progresses made with this approach?

> **Manus:** ## autoresearch — Karpathy, Mars 2026

**Sujet identifié :** `karpathy/autoresearch` — boucle de recherche ML autonome sur single-GPU, publiée le 7 mars 2026. 630 lignes. MIT License. 23.7k stars en 4 jours.

---

### Principe

Un agent AI reçoit un setup d'entraînement LLM réel (`train.py` = modèle GPT + optimizer Muon/AdamW). Il modifie le code, entraîne 5 minutes, mesure `val_bpb`, garde si ça améliore, recommence. L'humain programme uniquement `program.md` — la "politique de recherche". L'agent exécute.

---

### Résultats officiels (Karpathy, H100, 2 jours)

| Métrique | Résultat |
|---|---|
| Expériences autonomes | ~700 |
| Améliorations conservées | ~20 |
| Gain val_bpb | -11% |
| "Time to GPT-2" | 2.02h → 1.80h |
| Transfert vers modèle plus grand | ✅ Confirmé |

---

### Ce que l...

> **Manus:** Analysing the video and searching the latest developments on this experiment. Je reviens avec un état des lieux complet.

## Full Verbatim

<details>
<summary>Expand full conversation (3 messages)</summary>

**[1773208002454] MANUS:** ## autoresearch — Karpathy, Mars 2026

**Sujet identifié :** `karpathy/autoresearch` — boucle de recherche ML autonome sur single-GPU, publiée le 7 mars 2026. 630 lignes. MIT License. 23.7k stars en 4 jours.

---

### Principe

Un agent AI reçoit un setup d'entraînement LLM réel (`train.py` = modèle GPT + optimizer Muon/AdamW). Il modifie le code, entraîne 5 minutes, mesure `val_bpb`, garde si ça améliore, recommence. L'humain programme uniquement `program.md` — la "politique de recherche". L'agent exécute.

---

### Résultats officiels (Karpathy, H100, 2 jours)

| Métrique | Résultat |
|---|---|
| Expériences autonomes | ~700 |
| Améliorations conservées | ~20 |
| Gain val_bpb | -11% |
| "Time to GPT-2" | 2.02h → 1.80h |
| Transfert vers modèle plus grand | ✅ Confirmé |

---

### Ce que l'agent a réellement trouvé (session report auto-posté par l'agent, Discussion #32)

**Top découvertes :**
- **Réduire le batch size** (524K → 262K) = gain le plus important. Plus de steps > plus de pa...
**[1773207626178] MANUS:** Analysing the video and searching the latest developments on this experiment. Je reviens avec un état des lieux complet.
**[1773207621493] USER:** https://youtu.be/tUkD0oj92Qg?is=_5D_wmApepEQwcq3

Status about this experiment?
Search also from community 
Some gray discoveries and progresses made with this approach?



</details>
