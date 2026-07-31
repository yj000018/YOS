---
id: "3LlE0NGSBHd76UQVWYKMss"
title: "How to Test and Use the Mobbin Connector Features"
date: "2026-07-22"
importance: "3"
depth_score: "standard"
projects: ["Y-OS", "Mobbin Connector"]
tags: ["mobbin", "connector", "testing", "ui/ux", "api_integration", "subscription_required"]
summary: "Tested Mobbin connector features, identified API tools, and found a paid Mobbin account is required for full data."
executive_summary: "The session focused on testing the Mobbin connector. The assistant explored its capabilities, identified available tools, and attempted live data queries. However, a critical blocker was discovered: full functionality, specifically image retrieval, requires a paid Mobbin Pro account. The assistant provided a capabilities brief, listed the tools, and offered recommendations, prompting the user for next steps regarding account access or alternative UI/UX exploration."
context_and_intent: "The user wanted to test the Mobbin connector, see its features in action by fetching data, and receive a brief overview of its capabilities."
what_was_done: "The assistant explored the Mobbin MCP connector, listed its available tools, analyzed their capabilities, and attempted to perform live queries. It identified that a paid Mobbin Pro account is required for full functionality, specifically for image retrieval, which blocked the demonstration of data fetching."
outputs_produced: [{"description": "A comprehensive overview of the Mobbin connector's functionalities.", "name": "Brief complet des capacités", "type": "document"}, {"description": "A list of the specific tools available through the Mobbin connector.", "name": "Liste des outils (search_screens, search_flows, search_sections)", "type": "list"}, {"description": "Suggestions for how to proceed given the identified blocker.", "name": "Recommandations", "type": "document"}]
key_decisions: ["The assistant identified that a paid Mobbin Pro account is necessary for the connector to fully function and retrieve data."]
lessons_learned: {"discoveries": ["The Mobbin connector offers tools such as 'search_screens', 'search_flows', and 'search_sections'.", "Full data retrieval, particularly images, from the Mobbin connector is contingent on having a paid Mobbin Pro subscription."], "failed_or_suboptimal": ["The assistant was unable to demonstrate data fetching (e.g., images) due to the lack of a connected paid Mobbin account."], "worked_well": ["The assistant successfully explored the connector's capabilities and identified its available tools.", "The assistant provided a clear explanation of the blocker and proposed next steps."]}
challenges_and_blockers: ["Access to the Mobbin Connector Platform (MCP) requires a paid Mobbin Pro account (minimum $10/month).", "The inability to access a paid Mobbin account blocked the retrieval of images during live queries."]
open_questions: ["Does the user have a paid Mobbin account to connect?", "Does the user want to explore another approach for UI/UX analysis?"]
next_steps: ["The user needs to confirm if they have a paid Mobbin account to connect.", "The user needs to decide if they wish to explore an alternative approach for UI/UX analysis if a paid Mobbin account is not available."]
url: "https://manus.im/app/task/3LlE0NGSBHd76UQVWYKMss"
---

# How to Test and Use the Mobbin Connector Features

| Field | Value |
|-------|-------|
| **Session ID** | `3LlE0NGSBHd76UQVWYKMss` |
| **Date** | 2026-07-22 22:25 UTC |
| **Project** | imd9BRqHPV68nZkKkiUtWT |
| **URL** | [https://manus.im/app/sessions/3LlE0NGSBHd76UQVWYKMss](https://manus.im/app/sessions/3LlE0NGSBHd76UQVWYKMss) |
| **Messages** | 1 user · 3 assistant · 6 total |

## Initial Prompt

Help me test the Mobbin connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

## First Response

J'ai terminé l'exploration du connecteur Mobbin MCP.

J'ai listé les outils, analysé leurs capacités et lancé des requêtes live. Les tests révèlent que l'accès MCP nécessite un compte Mobbin payant (plan Pro à 10$/mois minimum), ce qui a bloqué la récupération des images lors de mes requêtes.

Tu trouveras le brief complet des capacités, la liste des outils (`search_screens`, `search_flows`, `search_sections`) et mes recommandations dans le document ci-joint. Dis-moi si tu as un compte payant à connecter ou si tu souhaites explorer une autre approche pour l'UI/UX.

## Conversation Summary

> **User:** Help me test the Mobbin connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** J'ai terminé l'exploration du connecteur Mobbin MCP.

J'ai listé les outils, analysé leurs capacités et lancé des requêtes live. Les tests révèlent que l'accès MCP nécessite un compte Mobbin payant (plan Pro à 10$/mois minimum), ce qui a bloqué la récupération des images lors de mes requêtes.

Tu trouveras le brief complet des capacités, la liste des outils (`search_screens`, `search_flows`, `search_sections`) et mes recommandations dans le document ci-joint. Dis-moi si tu as un compte payant à connecter ou si tu souhaites explorer une autre approche pour l'UI/UX.

> **Manus:** 3 outils identifiés : `search_screens`, `search_flows`, `search_sections`. Je lance maintenant 3 requêtes live — une par outil — pour te montrer des données réelles.

## Full Verbatim

<details>
<summary>Expand full conversation (4 messages)</summary>

**[1784759317210] MANUS:** J'ai terminé l'exploration du connecteur Mobbin MCP.

J'ai listé les outils, analysé leurs capacités et lancé des requêtes live. Les tests révèlent que l'accès MCP nécessite un compte Mobbin payant (plan Pro à 10$/mois minimum), ce qui a bloqué la récupération des images lors de mes requêtes.

Tu trouveras le brief complet des capacités, la liste des outils (`search_screens`, `search_flows`, `search_sections`) et mes recommandations dans le document ci-joint. Dis-moi si tu as un compte payant à connecter ou si tu souhaites explorer une autre approche pour l'UI/UX.
**[1784759201825] MANUS:** 3 outils identifiés : `search_screens`, `search_flows`, `search_sections`. Je lance maintenant 3 requêtes live — une par outil — pour te montrer des données réelles.
**[1784759158871] MANUS:** Sur it — je vais explorer le connecteur Mobbin, lister ses outils, tester ses capacités et te montrer des données réelles. Let me dive in.
**[1784759154664] USER:** Help me test the Mobbin connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>