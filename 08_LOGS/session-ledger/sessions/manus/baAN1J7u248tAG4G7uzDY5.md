---
id: "baAN1J7u248tAG4G7uzDY5"
title: "...mymind.com : API/MCP ?"
date: "2026-07-29"
importance: "3"
depth_score: "standard"
projects: ["Y-OS"]
tags: ["MyMind", "API", "MCP", "veille technologique", "monitoring", "Raycast", "PyPI", "GitHub", "Python", "CLI", "Raindrop", "schedule"]
summary: "Setup of a weekly tech watch for MyMind API/MCP, confirming an official private API via Raycast and a community PyPI package."
executive_summary: "An AI agent, Y-OS, was configured to monitor MyMind.com's API and MCP weekly. The initial prompt outlined the known state (no official API, fragile community MCP, recent tweet by Tobias van Schneider hinting at new API/MCP). The agent's first run on July 29, 2026, indicated 'Du nouveau' (something new) was found, triggering a structured report."
context_and_intent: "The AI agent Y-OS is tasked with weekly technology watch on the evolution of MyMind.com's API and MCP (MyMind Community Protocol)."
what_was_done: "An AI agent was configured to perform weekly web searches for 'mymind API', 'mymind MCP', 'mymind developer', site:mymind.com, and mentions on X (@mymind @vanschneider). It also checks github.com/iamumeransari/mymind-mcp for updates and mymind.com for /api, /developers, or /mcp pages. The first run was initiated on July 29, 2026."
outputs_produced: [{"description": "A structured report detailing what was found, its impact on Y-OS, and recommended actions, along with an update to the Raindrop vs MyMind comparison.", "name": "Structured Report", "type": "Report"}, {"description": "A brief confirmation stating 'Pas de changement MyMind API/MCP cette semaine' if no new information is found.", "name": "Brief Confirmation", "type": "Status Update"}]
key_decisions: ["Launch the monitoring schedule immediately upon configuration."]
lessons_learned: {"discoveries": ["Tobias van Schneider tweeted on July 23, 2026, about 'the new MCP and API' without published documentation.", "The first run of the monitoring agent successfully identified 'Du nouveau' regarding MyMind API/MCP."], "failed_or_suboptimal": [], "worked_well": ["The AI agent successfully initiated its first scheduled run as per instructions."]}
challenges_and_blockers: ["No official public API for MyMind.com", "Fragile community MCP (github.com/iamumeransari/mymind-mcp) based on reverse-engineering internal endpoints, with low adoption (~10 stars)"]
open_questions: ["What specific 'new' information was discovered in the first run?", "What are the details of the 'new MCP and API' hinted at by Tobias van Schneider?", "What is the impact of the 'new' findings on Y-OS and what are the recommended actions?"]
next_steps: ["Execute the monitoring schedule every Monday at 9h UTC.", "Produce a structured report if new information is found, including impact on Y-OS and recommended actions, plus an update to the Raindrop vs MyMind comparison.", "Provide a brief confirmation if no changes are found."]
url: "https://manus.im/app/task/baAN1J7u248tAG4G7uzDY5"
---

# ...mymind.com : API/MCP ?

| Field | Value |
|-------|-------|
| **Session ID** | `baAN1J7u248tAG4G7uzDY5` |
| **Date** | 2026-07-29 21:38 UTC |
| **Project** | deP744efwf6gY4e7rA8M7C |
| **URL** | [https://manus.im/app/sessions/baAN1J7u248tAG4G7uzDY5](https://manus.im/app/sessions/baAN1J7u248tAG4G7uzDY5) |
| **Messages** | 1 user · 4 assistant · 7 total |

## Initial Prompt

Tu es un agent de veille technologique Y-OS. Ton rôle : surveiller chaque semaine l'évolution de l'API et du MCP de l'application MyMind (mymind.com).
État connu au 28 juillet 2026 :
Pas d'API publique officielle
MCP communautaire fragile (github.com/iamumeransari/mymind-mcp, \~10 étoiles, reverse-engineering d'endpoints internes)
Tobias van Schneider a tweeté le 23 juillet 2026 "the new MCP and API" — annonce sans documentation publiée
Chaque lundi à 9h, exécute :
Recherche web : "mymind API", "mymind MCP", "mymind developer", site:mymind.com, @mymind @vanschneider sur X
Vérifie github.com/iamumeransari/mymind-mcp (nouveaux commits, issues, stars)
Vérifie mymind.com pour toute page /api, /developers, /mcp
Si du nouveau : rapport structuré (quoi, impact Y-OS, action recommandée) + mise à jour de la comparaison Raindrop vs MyMind
Si rien de nouveau : confirmation brève "Pas de changement MyMind API/MCP cette semaine"
Lance maintenant le schedule : manus-config schedule create --title "V

## First Response

# Veille MyMind API/MCP — Run #1 · 29 juillet 2026

## 🔔 Du nouveau — Rapport structuré

### Ce qui a changé (vs état connu au 28 juillet 2026)

**Signal majeur : API officielle privée confirmée**

L'extension Raycast officielle (publiée ~juillet 2026, 1 226 installs) utilise une **"official mymind API"** avec un système de clés API générées depuis la page Extensions de mymind (`access.mymind.com/extension`). Ce n'est pas une API publique documentée, mais c'est une API officielle avec authentification par clé — un cran au-dessus du reverse-engineering pur.

**MCP communautaire : publication PyPI**

Le package `mymind-api` v0.1.0 a été publié sur PyPI le **27 juillet 2026** (hier). Le repo GitHub reste à 10 stars, dernier commit 29 juin 2026. Le package est installable via `pip install mymind-api` et inclut le MCP server, le SDK Python et la CLI.

**Signal @vanschneider / @mymind**

- Tweet @sethsaler du 7 juillet 2026 : le MCP officiel mymind supporte désormais Claude, ChatGPT, **Herme

## Conversation Summary

> **User:** Tu es un agent de veille technologique Y-OS. Ton rôle : surveiller chaque semaine l'évolution de l'API et du MCP de l'application MyMind (mymind.com).
État connu au 28 juillet 2026 :
Pas d'API publique officielle
MCP communautaire fragile (github.com/iamumeransari/mymind-mcp, \~10 étoiles, reverse-engineering d'endpoints internes)
Tobias van Schneider a tweeté le 23 juillet 2026 "the new MCP and API" — annonce sans documentation publiée
Chaque lundi à 9h, exécute :
Recherche web : "mymind API", ...

> **Manus:** # Veille MyMind API/MCP — Run #1 · 29 juillet 2026

## 🔔 Du nouveau — Rapport structuré

### Ce qui a changé (vs état connu au 28 juillet 2026)

**Signal majeur : API officielle privée confirmée**

L'extension Raycast officielle (publiée ~juillet 2026, 1 226 installs) utilise une **"official mymind API"** avec un système de clés API générées depuis la page Extensions de mymind (`access.mymind.com/extension`). Ce n'est pas une API publique documentée, mais c'est une API officielle avec authentification par clé — un cran au-dessus du reverse-engineering pur.

**MCP communautaire : publication PyPI**

Le package `mymind-api` v0.1.0 a été publié sur PyPI le **27 juillet 2026** (hier). Le repo GitHub reste à 10 stars, dernier commit 29 juin 2026. Le package est installable via `pip install mymi...

> **Manus:** Veille terminée — données collectées. Rédaction du playbook + création du schedule.

## Full Verbatim

<details>
<summary>Expand full conversation (5 messages)</summary>

**[1785361324517] MANUS:** # Veille MyMind API/MCP — Run #1 · 29 juillet 2026

## 🔔 Du nouveau — Rapport structuré

### Ce qui a changé (vs état connu au 28 juillet 2026)

**Signal majeur : API officielle privée confirmée**

L'extension Raycast officielle (publiée ~juillet 2026, 1 226 installs) utilise une **"official mymind API"** avec un système de clés API générées depuis la page Extensions de mymind (`access.mymind.com/extension`). Ce n'est pas une API publique documentée, mais c'est une API officielle avec authentification par clé — un cran au-dessus du reverse-engineering pur.

**MCP communautaire : publication PyPI**

Le package `mymind-api` v0.1.0 a été publié sur PyPI le **27 juillet 2026** (hier). Le repo GitHub reste à 10 stars, dernier commit 29 juin 2026. Le package est installable via `pip install mymind-api` et inclut le MCP server, le SDK Python et la CLI.

**Signal @vanschneider / @mymind**

- Tweet @sethsaler du 7 juillet 2026 : le MCP officiel mymind supporte désormais Claude, ChatGPT, **Herme...
**[1785361249265] MANUS:** Veille terminée — données collectées. Rédaction du playbook + création du schedule.
**[1785361107058] MANUS:** Phase 2 — Run immédiat de veille. Lancement des recherches parallèles : web + GitHub + mymind.com.
**[1785361084051] MANUS:** Sur le coup. Je lis d'abord le skill yos-optimizer + manus-config avant d'exécuter.
**[1785361080542] USER:** Tu es un agent de veille technologique Y-OS. Ton rôle : surveiller chaque semaine l'évolution de l'API et du MCP de l'application MyMind (mymind.com).
État connu au 28 juillet 2026 :
Pas d'API publique officielle
MCP communautaire fragile (github.com/iamumeransari/mymind-mcp, \~10 étoiles, reverse-engineering d'endpoints internes)
Tobias van Schneider a tweeté le 23 juillet 2026 "the new MCP and API" — annonce sans documentation publiée
Chaque lundi à 9h, exécute :
Recherche web : "mymind API", "mymind MCP", "mymind developer", site:mymind.com, @mymind @vanschneider sur X
Vérifie github.com/iamumeransari/mymind-mcp (nouveaux commits, issues, stars)
Vérifie mymind.com pour toute page /api, /developers, /mcp
Si du nouveau : rapport structuré (quoi, impact Y-OS, action recommandée) + mise à jour de la comparaison Raindrop vs MyMind
Si rien de nouveau : confirmation brève "Pas de changement MyMind API/MCP cette semaine"
Lance maintenant le schedule : manus-config schedule create --title "V...



</details>