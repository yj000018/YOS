---
id: "dVwmwB1SE8zNjYicu2oNje"
title: "[✓] Karpathy's AutoResearch ML Agent Experiment - Status Review and Community Findings"
date: "2026-03-11"
importance: "3"
depth_score: "substantial"
projects: ["Y-OS"]
tags: ["ML Agent", "AutoResearch", "Karpathy", "LLM"]
summary: ""
executive_summary: "Karpathy's `autoresearch` is an autonomous ML research agent, launched March 7, 2026, that uses a single GPU to iteratively modify LLM training code, train for 5 minutes, and keep improvements based on `val_bpb`. Over two days and approximately 700 experiments, it achieved a -11% gain in `val_bpb` and reduced \"Time to GPT-2\" from 2.02h to 1.80h, with the approach confirmed to transfer to larger models."
context_and_intent: "The session aimed to review the status of Karpathy's AutoResearch ML Agent experiment, gather community findings, and identify any \"gray discoveries\" or progress made with this approach."
what_was_done: "An AI agent was configured to receive a real LLM training setup (`train.py`), which included a GPT model and an optimizer (Muon/AdamW). The agent's process involved modifying the code, training the model for 5 minutes, measuring the `val_bpb`, and retaining the changes if an improvement was observed, then repeating this cycle. The human's role was limited to programming the `program.md`, which served as the \"research policy\" guiding the agent's actions."
outputs_produced: [{"description": "An autonomous ML research loop on a single GPU, published March 7, 2026, with 630 lines of code and an MIT License.", "name": "karpathy/autoresearch project", "type": "Project/Codebase"}, {"description": "Approximately 700 experiments were conducted autonomously by the agent over two days.", "name": "Autonomous Experiments Conducted", "type": "Metric/Activity"}, {"description": "Around 20 improvements were identified and retained by the agent's iterative process.", "name": "Improvements Kept", "type": "Metric/Result"}, {"description": "Achieved a -11% gain in validation bits per byte (val_bpb).", "name": "val_bpb Gain", "type": "Metric/Result"}, {"description": "Reduced the time required to reach GPT-2 performance from 2.02 hours to 1.80 hours.", "name": "\"Time to GPT-2\" Reduction", "type": "Metric/Result"}, {"description": "The autonomous research approach was confirmed to transfer successfully to larger models.", "name": "Transferability to Larger Models", "type": "Finding/Confirmation"}]
key_decisions: []
lessons_learned: {"discoveries": ["The agent successfully identified approximately 20 improvements out of ~700 experiments.", "A -11% gain in validation bits per byte (val_bpb) was achieved.", "\"Time to GPT-2\" was reduced from 2.02 hours to 1.80 hours.", "The autonomous research approach was confirmed to transfer successfully to larger models."], "failed_or_suboptimal": [], "worked_well": ["The autonomous ML research loop effectively found performance improvements in LLM training.", "The single-GPU setup allowed for rapid iteration and experimentation (5-minute training cycles).", "The human-defined `program.md` policy proved effective in guiding the agent's research."]}
challenges_and_blockers: []
open_questions: []
next_steps: []
url: "https://manus.im/app/task/dVwmwB1SE8zNjYicu2oNje"
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