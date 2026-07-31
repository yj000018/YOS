---
id: nuRRRbRPj57FPEXv8Xns82
title: "[✓] Integration of Lemlist via MCP for personalized outreach campaigns"
date: "2026-02-27"
importance: 3
projects: ["Y-OS"]
tags: ["Lemlist", "MCP", "Integration", "Outreach", "Marketing"]
summary: "Recherche et confirmation d'un MCP officiel Lemlist pour une intégration fluide dans l'écosystème Y-OS pour les campagnes d'outreach personnalisées."
url: "https://manus.im/app/task/nuRRRbRPj57FPEXv8Xns82"
---

# [✓] Integration of Lemlist via MCP for personalized outreach campaigns

| Field | Value |
|-------|-------|
| **Session ID** | `nuRRRbRPj57FPEXv8Xns82` |
| **Date** | 2026-02-27 09:37 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/nuRRRbRPj57FPEXv8Xns82](https://manus.im/app/sessions/nuRRRbRPj57FPEXv8Xns82) |
| **Messages** | 3 user · 4 assistant · 15 total |

## Initial Prompt

Donc idéal serait de créer un MCP ou utiliser un MCP pour accéder à la liste, ça va donner plus de souplesse. C'est le cas pour tous les outils alors. Faut que j'ai des MCP pour tout, faut que j'ai des outils vraiment comme natif. Utiliser les API uniquement pour des call spécifiques de gros volume ou des choses comme ça comme tu m'expliquais.  Si c'est le cas, trouve un MCP pour le liste. Est-ce qu'il existe déjà ? Est-ce qu'il est officiel ? Est-ce qu'on le trouve sur GitHub ou sur n'importe quel repo ou sur Hugging Face ? Trouve la bonne approche.

## First Response

## MCP Lemlist — Cartographie complète

### Verdict immédiat

**Il existe un MCP Lemlist officiel**, publié par Lemlist eux-mêmes. C'est la voie à prendre.

---

### 1. Le MCP officiel Lemlist

| Attribut | Valeur |
|---|---|
| **Source** | Lemlist (équipe officielle) |
| **Endpoint** | `https://app.lemlist.com/mcp` |
| **Protocole** | JSON-RPC over HTTP (MCP standard) |
| **Auth** | OAuth (recommandé) ou API Key (`X-API-Key` header) |
| **Doc officielle** | [help.lemlist.com — Set up MCP](http://help.lemlist.com/en/articles/13728466-set-up-the-lemlist-mcp-server-in-your-llm-client-oauth-or-api-key) |
| **Mise à jour** | Février 2026 (il y a ~2 semaines) |
| **Statut** | Stable, production-ready |

C'est un **MCP remote hébergé** — pas besoin de cloner un repo ou de faire tourner un serveur local. L'endpoint est directement accessible.

---

### 2. Alternatives communautaires identifiées

| Source | Type | Outils | Statut |
|---|---|---|---|
| **Composio** | MCP remote (via leur platef

## Conversation Summary

> **User:** Donc idéal serait de créer un MCP ou utiliser un MCP pour accéder à la liste, ça va donner plus de souplesse. C'est le cas pour tous les outils alors. Faut que j'ai des MCP pour tout, faut que j'ai des outils vraiment comme natif. Utiliser les API uniquement pour des call spécifiques de gros volume ou des choses comme ça comme tu m'expliquais.  Si c'est le cas, trouve un MCP pour le liste. Est-ce qu'il existe déjà ? Est-ce qu'il est officiel ? Est-ce qu'on le trouve sur GitHub ou sur n'importe q...

> **User:** A c
Mais explique diff avantage de a ou de c
Recherche r outreach oui

> **User:** Comment ajouter https://www.lemlist.com/?utm_campaign=02e49082a901&utm_medium=referral&utm_source=partner&pscd=get.lemlist.com&ps_partner_key=MDJlNDkwODJhOTAx&ps_xid=1JJpJg9Ln0g6gx&gsxid=1JJpJg9Ln0g6gx&gspk=MDJlNDkwODJhOTAx&gad_source=1&gad_campaignid=23562277439&gbraid=0AAAABC3_ZE90GBNOY7xZ96bGNBpNHzYv0&gclid=CjwKCAiAnoXNBhAZEiwAnItcGxNvwUo6RvTwM2gg4Cat82NDFcH9KNFDxhNYlOrLVXF-Xj8xp9L1ixoCh-oQAvD_BwE
A yOS poi campagne massive de recherche de contact et email mkt (faible volume mais haute person...

> **Manus:** ## MCP Lemlist — Cartographie complète

### Verdict immédiat

**Il existe un MCP Lemlist officiel**, publié par Lemlist eux-mêmes. C'est la voie à prendre.

---

### 1. Le MCP officiel Lemlist

| Attribut | Valeur |
|---|---|
| **Source** | Lemlist (équipe officielle) |
| **Endpoint** | `https://app.lemlist.com/mcp` |
| **Protocole** | JSON-RPC over HTTP (MCP standard) |
| **Auth** | OAuth (recommandé) ou API Key (`X-API-Key` header) |
| **Doc officielle** | [help.lemlist.com — Set up MCP](http://help.lemlist.com/en/articles/13728466-set-up-the-lemlist-mcp-server-in-your-llm-client-oauth-or-api-key) |
| **Mise à jour** | Février 2026 (il y a ~2 semaines) |
| **Statut** | Stable, production-ready |

C'est un **MCP remote hébergé** — pas besoin de cloner un repo ou de faire tourner un serveu...

> **Manus:** Recherche en cours — MCP Lemlist existant, officiel ou communautaire.

## Full Verbatim

<details>
<summary>Expand full conversation (7 messages)</summary>

**[1772186114449] MANUS:** ## MCP Lemlist — Cartographie complète

### Verdict immédiat

**Il existe un MCP Lemlist officiel**, publié par Lemlist eux-mêmes. C'est la voie à prendre.

---

### 1. Le MCP officiel Lemlist

| Attribut | Valeur |
|---|---|
| **Source** | Lemlist (équipe officielle) |
| **Endpoint** | `https://app.lemlist.com/mcp` |
| **Protocole** | JSON-RPC over HTTP (MCP standard) |
| **Auth** | OAuth (recommandé) ou API Key (`X-API-Key` header) |
| **Doc officielle** | [help.lemlist.com — Set up MCP](http://help.lemlist.com/en/articles/13728466-set-up-the-lemlist-mcp-server-in-your-llm-client-oauth-or-api-key) |
| **Mise à jour** | Février 2026 (il y a ~2 semaines) |
| **Statut** | Stable, production-ready |

C'est un **MCP remote hébergé** — pas besoin de cloner un repo ou de faire tourner un serveur local. L'endpoint est directement accessible.

---

### 2. Alternatives communautaires identifiées

| Source | Type | Outils | Statut |
|---|---|---|---|
| **Composio** | MCP remote (via leur platef...
**[1772185710501] MANUS:** Recherche en cours — MCP Lemlist existant, officiel ou communautaire.
**[1772185708263] USER:** Donc idéal serait de créer un MCP ou utiliser un MCP pour accéder à la liste, ça va donner plus de souplesse. C'est le cas pour tous les outils alors. Faut que j'ai des MCP pour tout, faut que j'ai des outils vraiment comme natif. Utiliser les API uniquement pour des call spécifiques de gros volume ou des choses comme ça comme tu m'expliquais.  Si c'est le cas, trouve un MCP pour le liste. Est-ce qu'il existe déjà ? Est-ce qu'il est officiel ? Est-ce qu'on le trouve sur GitHub ou sur n'importe quel repo ou sur Hugging Face ? Trouve la bonne approche.
**[1772185167325] MANUS:** ## API Lemlist vs MCP Custom — Comparatif architectural

| Dimension | A — API directe | C — MCP Custom |
|---|---|---|
| **Intégration yOS** | Manus appelle Lemlist via HTTP | Lemlist devient un outil natif dans yOS, comme Notion |
| **Friction** | Moyenne — code Python/requests à chaque usage | Zéro — `manus-mcp-cli tool call lemlist_create_campaign` |
| **Composabilité** | Limitée — couplage fort avec le script | Haute — combinable avec n8n, Notion, Slack, etc. |
| **Maintenabilité** | Fragile si l'API change | Encapsulé dans le MCP, un seul point de mise à jour |
| **Temps de setup** | 1h | 4-8h (build + test + deploy) |
| **Puissance long terme** | Faible | Haute — c'est une pièce de l'OS |
| **Cas d'usage idéal** | Test rapide, usage ponctuel | Usage récurrent, intégré dans des workflows yOS |

---

## Recommandation architecturale

**Phase 1 → A** (maintenant) : connecter l'API Lemlist directement depuis Manus pour valider le flux complet :
- Recherche de contact (Apollo / Hunte...
**[1772185149161] USER:** A c
Mais explique diff avantage de a ou de c
Recherche r outreach oui
**[1772185080442] MANUS:** Compris. Avant de structurer l'intégration, je dois clarifier deux points :

**1. Niveau d'intégration souhaité pour Lemlist dans yOS**

- A) Connexion simple via API Lemlist (lecture/écriture de campagnes depuis Manus)
- B) Intégration dans un flux n8n (Manus → n8n → Lemlist)
- C) Intégration MCP custom (Lemlist comme outil natif dans yOS, comme Notion/Slack)
- D) Les trois, en couches

**2. Scope de la campagne "agents de changement"**

Tu mentionnes Elon Musk comme exemple — c'est un cas extrême de personnalisation (contact quasi-inaccessible). Je veux m'assurer de comprendre la logique :

- S'agit-il de construire un système de **recherche + qualification + outreach** pour des profils à fort impact (fondateurs, décideurs, activistes, chercheurs) ?
- Ou d'un cas d'usage plus ciblé : un secteur, un type de problème planétaire, une liste de cibles déjà partiellement définie ?

Dis-moi le périmètre réel et je structure l'architecture complète.
**[1772185070419] USER:** Comment ajouter https://www.lemlist.com/?utm_campaign=02e49082a901&utm_medium=referral&utm_source=partner&pscd=get.lemlist.com&ps_partner_key=MDJlNDkwODJhOTAx&ps_xid=1JJpJg9Ln0g6gx&gsxid=1JJpJg9Ln0g6gx&gspk=MDJlNDkwODJhOTAx&gad_source=1&gad_campaignid=23562277439&gbraid=0AAAABC3_ZE90GBNOY7xZ96bGNBpNHzYv0&gclid=CjwKCAiAnoXNBhAZEiwAnItcGxNvwUo6RvTwM2gg4Cat82NDFcH9KNFDxhNYlOrLVXF-Xj8xp9L1ixoCh-oQAvD_BwE
A yOS poi campagne massive de recherche de contact et email mkt (faible volume mais haute personnalisation: trouver les agents d échange en t pour problème planétaires par ex, contact ELIN musk avec email personalise etc



</details>
