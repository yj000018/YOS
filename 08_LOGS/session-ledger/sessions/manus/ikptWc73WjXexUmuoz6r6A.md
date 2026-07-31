---
id: "ikptWc73WjXexUmuoz6r6A"
title: "[✓] Test & Factsheet du connecteur Mem MCP pour Y-OS"
date: "2026-06-16"
importance: "3"
depth_score: "substantial"
projects: ["Y-OS"]
tags: ["Mem MCP", "connector", "factsheet", "testing", "API integration"]
summary: ""
executive_summary: "A factsheet for Mem MCP was created and pushed to Notion."
context_and_intent: "The primary goal was to create a comprehensive factsheet for a new iOS tool, Mem MCP. This factsheet needed to detail its capabilities, limitations, lessons learned, access methods, technical possibilities (read, write, API entry points), business features, and cost (free/paid). The user emphasized that the tool was thoroughly tested with all available APIs and entry points, distinguishing this analysis from those based solely on documentation."
what_was_done: "A factsheet for Mem MCP was created and pushed to Notion."
outputs_produced: [{"description": "A comprehensive document detailing the capabilities, limits, lessons learned, access, technical possibilities, business features, and cost of the Mem MCP iOS tool.", "name": "Factsheet for Mem MCP", "type": "Document"}]
key_decisions: []
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": []}
challenges_and_blockers: []
open_questions: []
next_steps: []
url: "https://manus.im/app/task/ikptWc73WjXexUmuoz6r6A"
---

# [✓] Test & Factsheet du connecteur Mem MCP pour Y-OS

| Field | Value |
|-------|-------|
| **Session ID** | `ikptWc73WjXexUmuoz6r6A` |
| **Date** | 2026-06-16 09:18 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/ikptWc73WjXexUmuoz6r6A](https://manus.im/app/sessions/ikptWc73WjXexUmuoz6r6A) |
| **Messages** | 2 user · 6 assistant · 12 total |

## Initial Prompt

C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l

## First Response

Factsheet créée et poussée dans Notion. Voici le résumé exécutif :

---

## 🧠 Mem MCP — Factsheet Y-OS (Synthèse)

**Mem est un PKM (Personal Knowledge Manager) avec un MCP natif donnant accès complet à tes notes, collections, pièces jointes et enregistrements audio.**

### Ce qu'on peut faire via MCP (22 outils)

| Domaine | Capacités | Accès |
|---|---|---|
| **Notes** | Créer, lire, lister, chercher, mettre à jour, supprimer (soft), restaurer, backdater | Read + Write |
| **Collections** | Créer, lire, lister, chercher, renommer, supprimer, gérer les membres | Read + Write |
| **Recherche sémantique** | `search_notes`, `find_related_notes` (embedding temps réel) | Read |
| **Pièces jointes** | Lire PDF/images/emails/calendrier, QA ciblée sur un fichier, URL signée | **Read only** |
| **Audio** | Récupérer transcription + métadonnées d'un enregistrement | **Read only** |

### Ce qu'on NE peut PAS faire via MCP

- Uploader ou créer des pièces jointes
- Gérer les permissions / partage


## Conversation Summary

> **User:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a t...

> **User:** Help me test the Mem connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** Factsheet créée et poussée dans Notion. Voici le résumé exécutif :

---

## 🧠 Mem MCP — Factsheet Y-OS (Synthèse)

**Mem est un PKM (Personal Knowledge Manager) avec un MCP natif donnant accès complet à tes notes, collections, pièces jointes et enregistrements audio.**

### Ce qu'on peut faire via MCP (22 outils)

| Domaine | Capacités | Accès |
|---|---|---|
| **Notes** | Créer, lire, lister, chercher, mettre à jour, supprimer (soft), restaurer, backdater | Read + Write |
| **Collections** | Créer, lire, lister, chercher, renommer, supprimer, gérer les membres | Read + Write |
| **Recherche sémantique** | `search_notes`, `find_related_notes` (embedding temps réel) | Read |
| **Pièces jointes** | Lire PDF/images/emails/calendrier, QA ciblée sur un fichier, URL signée | **Read only** |
| **...

> **Manus:** Structure MailerLite récupérée — c'est le template de référence. Je consulte maintenant la doc officielle Mem en ligne.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1781616609137] MANUS:** Factsheet créée et poussée dans Notion. Voici le résumé exécutif :

---

## 🧠 Mem MCP — Factsheet Y-OS (Synthèse)

**Mem est un PKM (Personal Knowledge Manager) avec un MCP natif donnant accès complet à tes notes, collections, pièces jointes et enregistrements audio.**

### Ce qu'on peut faire via MCP (22 outils)

| Domaine | Capacités | Accès |
|---|---|---|
| **Notes** | Créer, lire, lister, chercher, mettre à jour, supprimer (soft), restaurer, backdater | Read + Write |
| **Collections** | Créer, lire, lister, chercher, renommer, supprimer, gérer les membres | Read + Write |
| **Recherche sémantique** | `search_notes`, `find_related_notes` (embedding temps réel) | Read |
| **Pièces jointes** | Lire PDF/images/emails/calendrier, QA ciblée sur un fichier, URL signée | **Read only** |
| **Audio** | Récupérer transcription + métadonnées d'un enregistrement | **Read only** |

### Ce qu'on NE peut PAS faire via MCP

- Uploader ou créer des pièces jointes
- Gérer les permissions / partage
...
**[1781616405349] MANUS:** Structure MailerLite récupérée — c'est le template de référence. Je consulte maintenant la doc officielle Mem en ligne.
**[1781616347604] MANUS:** Je cherche d'abord la structure existante des factsheets Y-OS dans Notion/mémoire, puis je consulte la doc Mem en ligne avant de rédiger.
**[1781616342723] USER:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l...
**[1781601692462] MANUS:** Test du connecteur Mem MCP terminé. Les 22 outils fonctionnent parfaitement (CRUD complet validé).

Le rapport détaillé avec les données réelles de ton espace (collections, notes) est en pièce jointe. Mem est un excellent candidat pour la couche Knowledge de Y-OS.
**[1781601566974] MANUS:** 22 outils détectés. Je lance les opérations live : list_notes, list_collections, search, create, update.
**[1781601534491] MANUS:** Sur ça. Je lis le skill yos-optimizer d'abord, puis j'explore le connecteur Mem MCP.
**[1781601530721] USER:** Help me test the Mem connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>