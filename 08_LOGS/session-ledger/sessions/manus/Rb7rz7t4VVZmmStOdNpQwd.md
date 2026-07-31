---
id: "Rb7rz7t4VVZmmStOdNpQwd"
title: "Testing and Using Wireflow Connector Features"
date: "2026-07-22"
importance: "2"
depth_score: "standard"
projects: ["Y-OS"]
tags: ["wireflow", "connector", "testing", "workflow_automation", "AI_models", "tool_integration"]
summary: "Testing and exploring the Wireflow connector's features within Manus, including workflow execution and AI model access."
executive_summary: "The user inquired about the capabilities of the Wireflow connector. The assistant provided a comprehensive overview, detailing functionalities such as exploring the catalogue, executing workflows, and checking account balance. It also noted the user's current credit balance and the absence of personal workflows, offering guidance on how to proceed."
context_and_intent: "The user wanted to understand the functionalities and potential uses of the Wireflow connector."
what_was_done: "The assistant compiled and presented a detailed brief on the Wireflow connector's capabilities, including live account data (credit balance). It outlined three main functionalities: exploring the Wireflow catalogue (templates, models, prices), executing personal workflows, and tracking the user's account. The assistant also identified that the user currently has no personal workflows and advised on the best way to proceed."
outputs_produced: [{"description": "A summary of what the Wireflow connector can do, including exploring the catalogue, executing workflows, and tracking account balance, along with the user's current credit balance.", "name": "Brief on Wireflow connector capabilities and live account data", "type": "text summary"}, {"description": "A comprehensive report containing information about available models, their costs in credits, and a list of tools, provided as an attached file.", "name": "Detailed report on Wireflow models, costs, and tools", "type": "file"}]
key_decisions: []
lessons_learned: {"discoveries": ["The user's Wireflow account currently has 110 credits.", "The user's Wireflow account currently has no personal workflows."], "failed_or_suboptimal": [], "worked_well": ["The assistant successfully provided a clear and concise overview of the connector's capabilities.", "The assistant integrated live account data (credit balance) into the response.", "The assistant provided actionable advice for the next steps."]}
challenges_and_blockers: ["The user currently has no personal workflows created on their Wireflow account, preventing immediate execution of custom workflows."]
open_questions: ["Do you want to explore a template in particular?", "Have you created a workflow that you want to test?"]
next_steps: ["User to create a workflow on the Wireflow web interface.", "User to ask Manus to execute a created workflow with specific instructions.", "User to potentially explore a specific template or test a created workflow."]
url: "https://manus.im/app/task/Rb7rz7t4VVZmmStOdNpQwd"
---

# Testing and Using Wireflow Connector Features

| Field | Value |
|-------|-------|
| **Session ID** | `Rb7rz7t4VVZmmStOdNpQwd` |
| **Date** | 2026-07-22 22:34 UTC |
| **Project** | imd9BRqHPV68nZkKkiUtWT |
| **URL** | [https://manus.im/app/sessions/Rb7rz7t4VVZmmStOdNpQwd](https://manus.im/app/sessions/Rb7rz7t4VVZmmStOdNpQwd) |
| **Messages** | 2 user · 5 assistant · 11 total |

## Initial Prompt

quEpeux faire avec ce connecteur

## First Response

J'ai compilé le brief complet sur les capacités du connecteur Wireflow et les données live de ton compte.

**En résumé, avec ce connecteur tu peux :**
1. **Explorer le catalogue Wireflow** : Lister les templates, les modèles (Flux, Kling, Sora, ElevenLabs) et voir leurs prix en crédits.
2. **Exécuter tes workflows** : Lancer un de tes workflows persos depuis Manus (`run_workflow`), lui passer des prompts, et récupérer le média généré (image, vidéo, audio).
3. **Suivre ton compte** : Vérifier ton solde de crédits (actuellement 110 crédits).

Pour le moment, tu n'as pas de workflows personnels créés sur ton compte. Le mieux pour l'utiliser est de créer un workflow sur l'interface web de Wireflow, puis de me demander de l'exécuter avec tes instructions.

Le rapport détaillé avec les modèles, les coûts et la liste des outils est dans le fichier joint. Dis-moi si tu veux explorer un template en particulier ou si tu as créé un workflow que tu veux tester !

## Conversation Summary

> **User:** quEpeux faire avec ce connecteur

> **User:** Help me test the Wireflow connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** J'ai compilé le brief complet sur les capacités du connecteur Wireflow et les données live de ton compte.

**En résumé, avec ce connecteur tu peux :**
1. **Explorer le catalogue Wireflow** : Lister les templates, les modèles (Flux, Kling, Sora, ElevenLabs) et voir leurs prix en crédits.
2. **Exécuter tes workflows** : Lancer un de tes workflows persos depuis Manus (`run_workflow`), lui passer des prompts, et récupérer le média généré (image, vidéo, audio).
3. **Suivre ton compte** : Vérifier ton solde de crédits (actuellement 110 crédits).

Pour le moment, tu n'as pas de workflows personnels créés sur ton compte. Le mieux pour l'utiliser est de créer un workflow sur l'interface web de Wireflow, puis de me demander de l'exécuter avec tes instructions.

Le rapport détaillé avec les modèles, ...

> **Manus:** Je compile le brief complet depuis toutes les données collectées.

## Full Verbatim

<details>
<summary>Expand full conversation (7 messages)</summary>

**[1784759829542] MANUS:** J'ai compilé le brief complet sur les capacités du connecteur Wireflow et les données live de ton compte.

**En résumé, avec ce connecteur tu peux :**
1. **Explorer le catalogue Wireflow** : Lister les templates, les modèles (Flux, Kling, Sora, ElevenLabs) et voir leurs prix en crédits.
2. **Exécuter tes workflows** : Lancer un de tes workflows persos depuis Manus (`run_workflow`), lui passer des prompts, et récupérer le média généré (image, vidéo, audio).
3. **Suivre ton compte** : Vérifier ton solde de crédits (actuellement 110 crédits).

Pour le moment, tu n'as pas de workflows personnels créés sur ton compte. Le mieux pour l'utiliser est de créer un workflow sur l'interface web de Wireflow, puis de me demander de l'exécuter avec tes instructions.

Le rapport détaillé avec les modèles, les coûts et la liste des outils est dans le fichier joint. Dis-moi si tu veux explorer un template en particulier ou si tu as créé un workflow que tu veux tester !
**[1784759801895] MANUS:** Je compile le brief complet depuis toutes les données collectées.
**[1784759798949] USER:** quEpeux faire avec ce connecteur
**[1784759764246] MANUS:** Le template "Scene Description to Video" consomme ~590 crédits (Seedance 2.0 video model) — soit plus que ton solde actuel (110 crédits). Je ne peux pas le lancer sans risquer un échec.

Options :
1️⃣ **Skip le run** — je livre le brief complet basé sur les données déjà collectées (whoami, templates, models, workflow detail). Aucun crédit consommé.
2️⃣ **Tester un workflow image-only** — si tu crées un workflow perso image-only sur wireflow.ai (coût ~10-25 crédits), je peux le lancer via MCP.
3️⃣ **Top up crédits** sur wireflow.ai, puis je relance sur un template vidéo complet.

⭐ Recommandation : option 1 — les données collectées sont déjà suffisantes pour un brief complet et démonstratif.
**[1784759752470] MANUS:** Compte connecté : **Yannick Jolliet** (free plan, 110 crédits). Aucun workflow personnel existant. Je vais maintenant tester `run_workflow` sur le template "Scene Description to Video" — c'est le plus léger (image → video). Je vérifie d'abord le coût estimé avant de lancer.
**[1784759664734] MANUS:** Sur ça. Je lis le skill wireflow, liste les outils disponibles, et je teste le connecteur en live.
**[1784759660514] USER:** Help me test the Wireflow connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>