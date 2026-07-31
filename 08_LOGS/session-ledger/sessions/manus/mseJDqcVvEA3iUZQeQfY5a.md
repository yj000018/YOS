---
id: mseJDqcVvEA3iUZQeQfY5a
title: "[✓] Meta Ads Audit (No Data) + Meta Marketing MCP Factsheet Creation"
date: "2026-06-16"
importance: 3
projects: ["Y-OS", "Meta Marketing MCP"]
tags: ["meta ads", "meta marketing"]
summary: ""
url: "https://manus.im/app/task/mseJDqcVvEA3iUZQeQfY5a"
---

# [✓] Meta Ads Audit (No Data) + Meta Marketing MCP Factsheet Creation

| Field | Value |
|-------|-------|
| **Session ID** | `mseJDqcVvEA3iUZQeQfY5a` |
| **Date** | 2026-06-16 08:44 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/mseJDqcVvEA3iUZQeQfY5a](https://manus.im/app/sessions/mseJDqcVvEA3iUZQeQfY5a) |
| **Messages** | 2 user · 7 assistant · 16 total |

## Initial Prompt

C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l

## First Response

## Factsheet Meta Marketing MCP générée et poussée

J'ai documenté en profondeur le connecteur Meta Marketing. La factsheet a été créée dans ta section **TECH — Technologie & Infra** (au même niveau que les factsheets Apify et MailerLite).

🔗 **Lien direct Notion :** [🔵 Meta Marketing MCP — Factsheet & Capability Assessment](https://app.notion.com/p/38135e218cf88103b70eefe72e1305d3)

### Synthèse Télégraphique des découvertes

1️⃣ **Capacités (Read-Only) :** 9 outils MCP disponibles. Excellent pour l'extraction de data granulaire (campagnes, adsets, insights, ROAS, metrics) et l'audit de performance.
2️⃣ **Limites critiques (Write) :** Le connecteur actuel **ne permet pas d'écrire**. Impossible de créer une campagne, de changer un budget ou de mettre une pub en pause via MCP. Pour ça, il faudra passer par n8n/Make ou l'API REST.
3️⃣ **Filtre "Special Category" :** Les campagnes liées au logement, à l'emploi ou au crédit sont automatiquement bloquées par l'API (elles n'apparaissent même

## Conversation Summary

> **User:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a t...

> **User:** Review my Meta Ads performance for the last 30 days. Identify what's working, what's wasting budget, and give me actionable next steps.

> **Manus:** ## Factsheet Meta Marketing MCP générée et poussée

J'ai documenté en profondeur le connecteur Meta Marketing. La factsheet a été créée dans ta section **TECH — Technologie & Infra** (au même niveau que les factsheets Apify et MailerLite).

🔗 **Lien direct Notion :** [🔵 Meta Marketing MCP — Factsheet & Capability Assessment](https://app.notion.com/p/38135e218cf88103b70eefe72e1305d3)

### Synthèse Télégraphique des découvertes

1️⃣ **Capacités (Read-Only) :** 9 outils MCP disponibles. Excellent pour l'extraction de data granulaire (campagnes, adsets, insights, ROAS, metrics) et l'audit de performance.
2️⃣ **Limites critiques (Write) :** Le connecteur actuel **ne permet pas d'écrire**. Impossible de créer une campagne, de changer un budget ou de mettre une pub en pause via MCP. Pour ça, il f...

> **Manus:** Doc extraite. Je compile maintenant les tests réels + doc officielle pour rédiger la factsheet complète.

## Full Verbatim

<details>
<summary>Expand full conversation (9 messages)</summary>

**[1781616791946] MANUS:** ## Factsheet Meta Marketing MCP générée et poussée

J'ai documenté en profondeur le connecteur Meta Marketing. La factsheet a été créée dans ta section **TECH — Technologie & Infra** (au même niveau que les factsheets Apify et MailerLite).

🔗 **Lien direct Notion :** [🔵 Meta Marketing MCP — Factsheet & Capability Assessment](https://app.notion.com/p/38135e218cf88103b70eefe72e1305d3)

### Synthèse Télégraphique des découvertes

1️⃣ **Capacités (Read-Only) :** 9 outils MCP disponibles. Excellent pour l'extraction de data granulaire (campagnes, adsets, insights, ROAS, metrics) et l'audit de performance.
2️⃣ **Limites critiques (Write) :** Le connecteur actuel **ne permet pas d'écrire**. Impossible de créer une campagne, de changer un budget ou de mettre une pub en pause via MCP. Pour ça, il faudra passer par n8n/Make ou l'API REST.
3️⃣ **Filtre "Special Category" :** Les campagnes liées au logement, à l'emploi ou au crédit sont automatiquement bloquées par l'API (elles n'apparaissent même...
**[1781616589827] MANUS:** Doc extraite. Je compile maintenant les tests réels + doc officielle pour rédiger la factsheet complète.
**[1781616519324] MANUS:** Template récupéré (Apify + MailerLite). Je recherche maintenant la doc officielle Meta Marketing API pour valider les capabilities réelles, les limites et le pricing.
**[1781616453672] MANUS:** Compris. Je cherche d'abord la structure de factsheet existante dans Notion/mémoire yOS, puis je documente le connecteur Meta Marketing en profondeur avec la doc officielle. Je reviens avec la factsheet complète.
**[1781616449231] USER:** C'est donc un nouvel outil disponible pour iOS. Il faut donc une factsheet et d'un outil avec ses capabilités, ses limites, les lessons learned, les éventuels accès, etc. Comme d'habitude, on fait cette factsheet pour cet outil. Là, on l'a vraiment testé avec tous les accès et tous les API, les entry points, etc. D'autres fois, on n'a pas eu le temps de tester et donc c'est ce que ça donne en général d'après la documentation que tu retrouves online. Mais je veux savoir que pour tel outil, on a telle possibilité et que ça offre. On est capable d'écrire, de lire, de faire, les possibilités techniques d'accès à l'outil et les possibilités en termes de capabilities, de features, donc business-wise. Qu'est-ce que ça m'importe d'avoir cette connexion-là ? Et puis, c'est gratuit, payant, etc. Donc, tout ça, on a déjà une description de chaque outil, on a déjà des feuilles qui décrivent chaque outil, on a déjà une structure de métadonnées. Donc, il ne faut pas réinventer, il faut repartir de l...
**[1781599672406] MANUS:** ## Meta Ads — Audit 30 jours : Résultat du diagnostic

### Constat : Aucune donnée de performance disponible

Après interrogation complète des deux comptes connectés via le MCP Meta Marketing, voici ce que j'ai trouvé :

| Compte | ID | Devise | Statut | Dépense totale | Campagnes actives |
|---|---|---|---|---|---|
| 157086230 | `act_157086230` | CHF | ACTIVE | CHF 0.00 | 0 (1 filtrée*) |
| Yannick Jolliet | `act_498904971225575` | EUR | ACTIVE | EUR 0.00 | 0 |

**\*** 1 campagne filtrée automatiquement car classée **Special Category** (logement, emploi, ou services financiers) — politique Meta stricte, non analysable via ce connecteur.

---

### Pourquoi aucune donnée ?

Trois causes possibles, à vérifier dans cet ordre :

**1. Comptes sans activité récente**
`amount_spent: "0.00"` sur les deux comptes — aucune dépense enregistrée. Soit les campagnes sont en pause/archivées, soit le budget est épuisé, soit les comptes ne sont pas les bons.

**2. Compte principal non connecté**
Les co...
**[1781599512290] MANUS:** Skill chargé. Je pull maintenant les données Meta Ads — ad accounts, campagnes, ad sets, et métriques sur 30 jours.
**[1781599493429] MANUS:** Sur ça. Je lis d'abord les skills meta-ads-analyzer et tool-router avant de plonger dans les données.
**[1781599490409] USER:** Review my Meta Ads performance for the last 30 days. Identify what's working, what's wasting budget, and give me actionable next steps.



</details>
