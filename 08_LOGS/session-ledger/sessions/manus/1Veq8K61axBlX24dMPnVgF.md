---
session_id: 1Veq8K61axBlX24dMPnVgF
title: "[✓] Taskade MCP Connector — Test Live & Factsheet Y-OS"
date: 2026-06-16 10:49 UTC
url: https://manus.im/app/sessions/1Veq8K61axBlX24dMPnVgF
project_id: none
user_messages: 2
assistant_messages: 5
total_messages: 11
processed: true
---

# [✓] Taskade MCP Connector — Test Live & Factsheet Y-OS

| Field | Value |
|-------|-------|
| **Session ID** | `1Veq8K61axBlX24dMPnVgF` |
| **Date** | 2026-06-16 10:49 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/1Veq8K61axBlX24dMPnVgF](https://manus.im/app/sessions/1Veq8K61axBlX24dMPnVgF) |
| **Messages** | 2 user · 5 assistant · 11 total |

## Initial Prompt

C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l

## First Response

Factsheet Taskade complète, archivée dans Notion et disponible en fichier joint.

**Notion :** [🔌 Taskade MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf8819c8c15d02a2449f722) — placée sous le hub Y-OS Architecture Multi-Agents, au même niveau que la factsheet MailerLite.

---

### Ce que couvre la factsheet

**57 outils** répartis en 4 domaines fonctionnels (Hierarchy, Projects, Tasks, AI Agents), tous testés en live sur ton workspace `ymed`.

**Limites critiques identifiées :**
- Pas de `prompt-an-agent` via MCP — le serveur inbound ne wrape que l'API v1. Pour déclencher un agent programmatiquement, il faut appeler `POST /api/v2/promptAgent` directement.
- MCP complet (outbound) réservé au plan **Business** ($40/mo) minimum.
- Max 5 Personal Access Tokens par compte.

**Interdépendances Y-OS ajoutées :** Notion (archive), Claude/Gemini (priorisation), n8n/Zapier (event-driven), Linear (sync blockers).

**Lessons Learned live (16 juin 2026) :** Connecteu

## Conversation Summary

> **User:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a t...

> **User:** Help me test the Taskade connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** Factsheet Taskade complète, archivée dans Notion et disponible en fichier joint.

**Notion :** [🔌 Taskade MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf8819c8c15d02a2449f722) — placée sous le hub Y-OS Architecture Multi-Agents, au même niveau que la factsheet MailerLite.

---

### Ce que couvre la factsheet

**57 outils** répartis en 4 domaines fonctionnels (Hierarchy, Projects, Tasks, AI Agents), tous testés en live sur ton workspace `ymed`.

**Limites critiques identifiées :**
- Pas de `prompt-an-agent` via MCP — le serveur inbound ne wrape que l'API v1. Pour déclencher un agent programmatiquement, il faut appeler `POST /api/v2/promptAgent` directement.
- MCP complet (outbound) réservé au plan **Business** ($40/mo) minimum.
- Max 5 Personal Access Tokens p...

> **Manus:** Template Y-OS récupéré (MailerLite factsheet). Je recherche maintenant la doc Taskade officielle pour valider les limites API, pricing et contraintes.

## Full Verbatim

<details>
<summary>Expand full conversation (7 messages)</summary>

**[1781616525927] MANUS:** Factsheet Taskade complète, archivée dans Notion et disponible en fichier joint.

**Notion :** [🔌 Taskade MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf8819c8c15d02a2449f722) — placée sous le hub Y-OS Architecture Multi-Agents, au même niveau que la factsheet MailerLite.

---

### Ce que couvre la factsheet

**57 outils** répartis en 4 domaines fonctionnels (Hierarchy, Projects, Tasks, AI Agents), tous testés en live sur ton workspace `ymed`.

**Limites critiques identifiées :**
- Pas de `prompt-an-agent` via MCP — le serveur inbound ne wrape que l'API v1. Pour déclencher un agent programmatiquement, il faut appeler `POST /api/v2/promptAgent` directement.
- MCP complet (outbound) réservé au plan **Business** ($40/mo) minimum.
- Max 5 Personal Access Tokens par compte.

**Interdépendances Y-OS ajoutées :** Notion (archive), Claude/Gemini (priorisation), n8n/Zapier (event-driven), Linear (sync blockers).

**Lessons Learned live (16 juin 2026) :** Connecteu...
**[1781616360887] MANUS:** Template Y-OS récupéré (MailerLite factsheet). Je recherche maintenant la doc Taskade officielle pour valider les limites API, pricing et contraintes.
**[1781616305187] MANUS:** Compris. Je vais d'abord retrouver la structure de factsheet existante dans Notion/mémoire Y-OS, puis aller chercher la doc Taskade en ligne pour valider les limites, et enfin produire la factsheet complète.
**[1781616298611] USER:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l...
**[1781607086079] MANUS:** J'ai testé le connecteur Taskade via MCP et extrait des données réelles de ton espace de travail. 

Voici les points clés :
- **57 outils disponibles** couvrant tout l'écosystème Taskade (Projets, Tâches, Dossiers, Workspaces).
- **Gestion des Agents IA** : Capacité à créer, configurer et alimenter la base de connaissances des agents Taskade.
- **Données live extraites** : J'ai trouvé tes dossiers (`Home`, `Task Flow Manager`), tes projets (`TaskFlow App — Build State`, `Tasks`, `Blockers`), et tes agents (`Deal Finder Agent1`, `Task Coach`). J'ai même extrait le briefing quotidien du 13 Mai généré par ton Task Coach.

Le rapport complet avec les données structurées et les recommandations d'intégration Y-OS est dans le fichier joint.
**[1781606988878] MANUS:** Sur ça. Je lis d'abord le skill tool-router + yos-optimizer, puis j'explore le connecteur Taskade via MCP.
**[1781606982710] USER:** Help me test the Taskade connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>
