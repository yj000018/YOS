---
id: "5zjZ9CnID1iDdJKFpZjYDi"
title: "[✓] Shopify MCP Connector — Live Test & Factsheet Production"
date: "2026-06-16"
importance: "3"
depth_score: "substantial"
projects: ["Y-OS"]
tags: ["Shopify", "Connector", "Factsheet", "API", "GraphQL", "Integration", "E-commerce"]
summary: ""
executive_summary: "The session successfully produced a comprehensive factsheet for the new Shopify MCP Connector, based on thorough live testing of its APIs and entry points, and subsequently pushed it to the Notion Connectors Registry."
context_and_intent: "The user requested a detailed factsheet for a new iOS tool, the Shopify MCP Connector. The factsheet needed to cover its capabilities, limitations, lessons learned, access points (APIs, entry points), technical functionalities (read/write), business features, and cost. A key requirement was that this factsheet be based on actual live testing, unlike previous instances where documentation was used. The output should leverage existing metadata structures."
what_was_done: "A factsheet for the Shopify MCP Connector was created and subsequently pushed to the Notion Connectors Registry."
outputs_produced: [{"description": "Factsheet detailing the capabilities, limits, lessons learned, access points, technical functionalities, and business features of the Shopify MCP Connector, based on live testing.", "name": "Shopify MCP Connector Factsheet", "type": "Factsheet"}]
key_decisions: []
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": []}
challenges_and_blockers: []
open_questions: []
next_steps: []
url: "https://manus.im/app/task/5zjZ9CnID1iDdJKFpZjYDi"
---

# [✓] Shopify MCP Connector — Live Test & Factsheet Production

| Field | Value |
|-------|-------|
| **Session ID** | `5zjZ9CnID1iDdJKFpZjYDi` |
| **Date** | 2026-06-16 11:08 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/5zjZ9CnID1iDdJKFpZjYDi](https://manus.im/app/sessions/5zjZ9CnID1iDdJKFpZjYDi) |
| **Messages** | 2 user · 6 assistant · 12 total |

## Initial Prompt

C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l

## First Response

Factsheet créée et poussée dans le Registre Connecteurs Notion :
**[🛒 Shopify MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf881e590b3d4232b0738d1)**

---

**Synthèse rapide :** Le connecteur Shopify MCP donne à Y-OS un contrôle programmatique complet sur une boutique Shopify via l'Admin API GraphQL. Il expose **22 outils natifs** couvrant produits, variantes, réductions, inventaire et commandes, plus un fallback GraphQL brut pour tout le reste.

| Dimension | Résumé |
|---|---|
| **Accès** | Lecture + Écriture + Suppression (CRUD complet sur produits, discounts, inventaire) |
| **Testé live** | ✅ Oui — boutique `Winnie-forever` (CHF, plan trial) |
| **Limites clés** | Commandes limitées au canal "Manus" · Produit DRAFT non publiable sans `publish_channels:[]` · Valeurs % en float (0.1, pas 10) · Scopes GraphQL manquants sur `locations` |
| **Rate limits** | Leaky bucket — 1000 pts/s (plan standard) · Max 1000 pts/requête unique |
| **Pricing** | Inclus d

## Conversation Summary

> **User:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a t...

> **User:** Help me test the Shopify connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** Factsheet créée et poussée dans le Registre Connecteurs Notion :
**[🛒 Shopify MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf881e590b3d4232b0738d1)**

---

**Synthèse rapide :** Le connecteur Shopify MCP donne à Y-OS un contrôle programmatique complet sur une boutique Shopify via l'Admin API GraphQL. Il expose **22 outils natifs** couvrant produits, variantes, réductions, inventaire et commandes, plus un fallback GraphQL brut pour tout le reste.

| Dimension | Résumé |
|---|---|
| **Accès** | Lecture + Écriture + Suppression (CRUD complet sur produits, discounts, inventaire) |
| **Testé live** | ✅ Oui — boutique `Winnie-forever` (CHF, plan trial) |
| **Limites clés** | Commandes limitées au canal "Manus" · Produit DRAFT non publiable sans `publish_channels:[]...

> **Manus:** Compris. Je cherche d'abord la structure existante des factsheets d'outils dans Notion/mémoire, puis je complète avec la doc Shopify en ligne et les tests live qu'on vient de faire.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1781616472899] MANUS:** Factsheet créée et poussée dans le Registre Connecteurs Notion :
**[🛒 Shopify MCP Connector — Factsheet & Capabilities](https://app.notion.com/p/38135e218cf881e590b3d4232b0738d1)**

---

**Synthèse rapide :** Le connecteur Shopify MCP donne à Y-OS un contrôle programmatique complet sur une boutique Shopify via l'Admin API GraphQL. Il expose **22 outils natifs** couvrant produits, variantes, réductions, inventaire et commandes, plus un fallback GraphQL brut pour tout le reste.

| Dimension | Résumé |
|---|---|
| **Accès** | Lecture + Écriture + Suppression (CRUD complet sur produits, discounts, inventaire) |
| **Testé live** | ✅ Oui — boutique `Winnie-forever` (CHF, plan trial) |
| **Limites clés** | Commandes limitées au canal "Manus" · Produit DRAFT non publiable sans `publish_channels:[]` · Valeurs % en float (0.1, pas 10) · Scopes GraphQL manquants sur `locations` |
| **Rate limits** | Leaky bucket — 1000 pts/s (plan standard) · Max 1000 pts/requête unique |
| **Pricing** | Inclus d...
**[1781616272585] MANUS:** Compris. Je cherche d'abord la structure existante des factsheets d'outils dans Notion/mémoire, puis je complète avec la doc Shopify en ligne et les tests live qu'on vient de faire.
**[1781616266747] USER:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l...
**[1781608206337] MANUS:** Voici le brief complet sur les capacités du connecteur Shopify MCP, basé sur des tests live sur ta boutique (Winnie-forever).

J'ai testé la lecture GraphQL (infos boutique, collections), la création/mise à jour de produits, et la création de codes promo (%). Le connecteur est robuste, expose 22 outils natifs, et supporte le GraphQL brut en fallback.

Le rapport détaillé est en pièce jointe. 🚀
**[1781608107139] MANUS:** 22 outils détectés. Fetching produits, commandes, inventaire et discounts en parallèle...
**[1781608100581] MANUS:** Mode **BALANCED** — tâche < 20 crédits estimés. Exploration du connecteur Shopify en cours...
**[1781608085227] MANUS:** Sur ça. Je lis d'abord le skill yos-optimizer + tool-router, puis j'explore le connecteur Shopify en live.
**[1781608080047] USER:** Help me test the Shopify connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>