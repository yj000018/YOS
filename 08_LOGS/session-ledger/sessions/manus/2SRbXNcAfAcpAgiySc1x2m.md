---
id: "2SRbXNcAfAcpAgiySc1x2m"
title: "[✓] Read AI MCP Connector — Test Live & Factsheet Y-OS"
date: "2026-06-16"
importance: "3"
depth_score: "minor"
projects: ["Y-OS", "MCP Connector"]
tags: ["AI", "Connector", "Factsheet", "Testing", "API Integration", "Documentation"]
summary: ""
executive_summary: "The session involved the creation of a factsheet for a new iOS tool, the 'AI MCP Connector'. The assistant successfully generated and published the factsheet in Notion, addressing the user's detailed requirements regarding capabilities, limitations, access, and business value."
context_and_intent: "The user requested a factsheet for a new iOS tool, the 'AI MCP Connector'. The factsheet needed to detail its capabilities, limitations, lessons learned, access methods (API, entry points), technical possibilities (read, write), business features, and cost (free/paid). The user emphasized that this tool was thoroughly tested and that the factsheet should leverage existing metadata structures rather than reinventing them."
what_was_done: "The assistant created and published the requested factsheet in Notion, specifically under '🔌 Y-OS — Registre Connecteurs Manus'."
outputs_produced: [{"description": "A detailed factsheet for the 'AI MCP Connector' iOS tool, covering capabilities, limitations, lessons learned, access methods, technical possibilities, business features, and cost.", "name": "Factsheet for AI MCP Connector", "type": "Document"}]
key_decisions: []
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": []}
challenges_and_blockers: []
open_questions: []
next_steps: []
url: "https://manus.im/app/task/2SRbXNcAfAcpAgiySc1x2m"
---

# [✓] Read AI MCP Connector — Test Live & Factsheet Y-OS

| Field | Value |
|-------|-------|
| **Session ID** | `2SRbXNcAfAcpAgiySc1x2m` |
| **Date** | 2026-06-16 09:03 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/2SRbXNcAfAcpAgiySc1x2m](https://manus.im/app/sessions/2SRbXNcAfAcpAgiySc1x2m) |
| **Messages** | 2 user · 6 assistant · 12 total |

## Initial Prompt

C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l

## First Response

Factsheet créée et publiée dans Notion sous **🔌 Y-OS — Registre Connecteurs Manus** :
👉 https://app.notion.com/p/38135e218cf881a8a54af354a1ad4008

---

**Résumé exécutif — Read AI MCP**

Read AI est un **notetaker IA** (Zoom, Meet, Teams) qui expose ses données via un serveur MCP remote (OAuth 2.1, beta ouverte). Le connecteur Manus donne accès à **3 outils** :

| Outil | Mode | Ce que ça fait |
|---|---|---|
| `list_meetings` | **Read** | Lister l'historique avec filtres temporels + pagination |
| `get_meeting_by_id` | **Read** | Extraire résumé, chapitres, actions, questions, transcript, métriques, lien MP4 |
| `create_meeting_agent` | **Write** | Envoyer un bot enregistrer une réunion Zoom/Meet/Teams (URL ou ID) |

**Capabilities confirmées (live-testées) :**
- Extraction structurée de `action_items`, `key_questions`, `topics`, `chapter_summaries`
- Métriques analytiques : Read Score, Sentiment, Engagement (scores 0–100)
- Transcript complet avec identification des locuteurs
- Déplo

## Conversation Summary

> **User:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a t...

> **User:** Help me test the Read AI connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** Factsheet créée et publiée dans Notion sous **🔌 Y-OS — Registre Connecteurs Manus** :
👉 https://app.notion.com/p/38135e218cf881a8a54af354a1ad4008

---

**Résumé exécutif — Read AI MCP**

Read AI est un **notetaker IA** (Zoom, Meet, Teams) qui expose ses données via un serveur MCP remote (OAuth 2.1, beta ouverte). Le connecteur Manus donne accès à **3 outils** :

| Outil | Mode | Ce que ça fait |
|---|---|---|
| `list_meetings` | **Read** | Lister l'historique avec filtres temporels + pagination |
| `get_meeting_by_id` | **Read** | Extraire résumé, chapitres, actions, questions, transcript, métriques, lien MP4 |
| `create_meeting_agent` | **Write** | Envoyer un bot enregistrer une réunion Zoom/Meet/Teams (URL ou ID) |

**Capabilities confirmées (live-testées) :**
- Extraction structurée de ...

> **Manus:** Structure existante identifiée — parent: "🔌 Y-OS — Registre Connecteurs Manus". Je vais maintenant chercher la doc officielle Read AI (pricing, API limits, intégrations) avant de rédiger la factsheet.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1781616517500] MANUS:** Factsheet créée et publiée dans Notion sous **🔌 Y-OS — Registre Connecteurs Manus** :
👉 https://app.notion.com/p/38135e218cf881a8a54af354a1ad4008

---

**Résumé exécutif — Read AI MCP**

Read AI est un **notetaker IA** (Zoom, Meet, Teams) qui expose ses données via un serveur MCP remote (OAuth 2.1, beta ouverte). Le connecteur Manus donne accès à **3 outils** :

| Outil | Mode | Ce que ça fait |
|---|---|---|
| `list_meetings` | **Read** | Lister l'historique avec filtres temporels + pagination |
| `get_meeting_by_id` | **Read** | Extraire résumé, chapitres, actions, questions, transcript, métriques, lien MP4 |
| `create_meeting_agent` | **Write** | Envoyer un bot enregistrer une réunion Zoom/Meet/Teams (URL ou ID) |

**Capabilities confirmées (live-testées) :**
- Extraction structurée de `action_items`, `key_questions`, `topics`, `chapter_summaries`
- Métriques analytiques : Read Score, Sentiment, Engagement (scores 0–100)
- Transcript complet avec identification des locuteurs
- Déplo...
**[1781616428387] MANUS:** Structure existante identifiée — parent: "🔌 Y-OS — Registre Connecteurs Manus". Je vais maintenant chercher la doc officielle Read AI (pricing, API limits, intégrations) avant de rédiger la factsheet.
**[1781616370341] MANUS:** Compris. Je cherche d'abord la structure existante des factsheets d'outils dans Notion/Y-OS, puis je vais en ligne valider les capabilities/limites Read AI, et je produis la factsheet complète.
**[1781616363961] USER:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l...
**[1781600701639] MANUS:** J'ai testé le connecteur Read AI. Il expose 3 outils puissants (lister, lire en détail, envoyer un bot). J'ai extrait les données réelles de ta dernière réunion (Onboarding to Read AI). Le brief structuré avec les données live et mes recommandations d'intégration Y-OS est dans le fichier joint. Dis-moi si tu veux explorer un flux spécifique (ex: automatiser l'envoi du bot).
**[1781600653206] MANUS:** 3 outils confirmés. Je fetch maintenant les meetings réels — liste + summaries + action items.
**[1781600627875] MANUS:** Sur ça — je lis le skill yos-optimizer d'abord, puis j'explore le connecteur Read AI via MCP.
**[1781600624890] USER:** Help me test the Read AI connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>