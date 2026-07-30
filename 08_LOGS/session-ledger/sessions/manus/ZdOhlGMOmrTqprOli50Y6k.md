---
session_id: ZdOhlGMOmrTqprOli50Y6k
title: "[✓] Install fast-navigation v2.0 skill and enforce via yos-optimizer"
date: 2026-05-31 08:04 UTC
url: https://manus.im/app/sessions/ZdOhlGMOmrTqprOli50Y6k
project_id: none
user_messages: 3
assistant_messages: 5
total_messages: 14
processed: true
---

# [✓] Install fast-navigation v2.0 skill and enforce via yos-optimizer

| Field | Value |
|-------|-------|
| **Session ID** | `ZdOhlGMOmrTqprOli50Y6k` |
| **Date** | 2026-05-31 08:04 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/ZdOhlGMOmrTqprOli50Y6k](https://manus.im/app/sessions/ZdOhlGMOmrTqprOli50Y6k) |
| **Messages** | 3 user · 5 assistant · 14 total |

## Initial Prompt

O

## First Response

Fait. `yos-optimizer` mis à jour avec deux ajouts :

1. **Section dédiée "Règle web — fast-navigation FIRST"** — workflow obligatoire en 4 étapes avant tout appel browser
2. **O-Rules enrichies** — `fast_nav.py` remplace `webpage_extract` comme outil par défaut pour web scraping et multi-URL (tous modes)

Désormais, à chaque prompt web, yos-optimizer (lu systématiquement) forcera le passage par `fast_nav.py` avant d'autoriser le browser.

## Conversation Summary

> **User:** O

> **User:** Est utilisé systématiquement??

> **User:** add this skill:

> **Manus:** Fait. `yos-optimizer` mis à jour avec deux ajouts :

1. **Section dédiée "Règle web — fast-navigation FIRST"** — workflow obligatoire en 4 étapes avant tout appel browser
2. **O-Rules enrichies** — `fast_nav.py` remplace `webpage_extract` comme outil par défaut pour web scraping et multi-URL (tous modes)

Désormais, à chaque prompt web, yos-optimizer (lu systématiquement) forcera le passage par `fast_nav.py` avant d'autoriser le browser.

> **Manus:** Lu. Je lis yos-optimizer et j'ajoute la règle fast-navigation.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1780270942539] MANUS:** Fait. `yos-optimizer` mis à jour avec deux ajouts :

1. **Section dédiée "Règle web — fast-navigation FIRST"** — workflow obligatoire en 4 étapes avant tout appel browser
2. **O-Rules enrichies** — `fast_nav.py` remplace `webpage_extract` comme outil par défaut pour web scraping et multi-URL (tous modes)

Désormais, à chaque prompt web, yos-optimizer (lu systématiquement) forcera le passage par `fast_nav.py` avant d'autoriser le browser.
**[1780270924122] MANUS:** Lu. Je lis yos-optimizer et j'ajoute la règle fast-navigation.
**[1780270920069] USER:** O
**[1780270879078] MANUS:** **Non, pas systématiquement — voici la réalité :**

Le skill est **disponible** dans la liste des skills actifs, mais il ne s'active que si :

1. **Le trigger de description match** — Manus lit la description du skill et décide si elle est pertinente pour la tâche en cours
2. **Manus choisit de le lire** — c'est un choix contextuel, pas une règle forcée

**Ce qui se passe concrètement :**
- Pour une tâche web/extraction → le skill sera proposé dans les "related skills" → Manus le lit → applique les règles
- Pour une tâche sans rapport (code, image, etc.) → ignoré

**Pour le rendre systématique :**
Deux options :

1️⃣ **Instruction dans le profil utilisateur** — ajouter dans tes custom instructions : `"ALWAYS use fast-navigation skill for any web task"` → force le trigger

2️⃣ **Intégrer dans yos-optimizer** — le skill yos-optimizer (lu à chaque prompt) peut inclure une règle : `"Pour toute tâche web → lire fast-navigation avant d'utiliser le browser"`

**Recommandation ⭐ :** Option 2 —...
**[1780270868336] USER:** Est utilisé systématiquement??
**[1780214758487] MANUS:** Skill **fast-navigation v2.0** créé, testé, validé ✅

**Structure :**
```
/home/ubuntu/skills/fast-navigation/
├── SKILL.md          ← trigger + doc complète
└── scripts/
    └── fast_nav.py   ← toolkit opérationnel
```

**Tests passés :** `auto` (JSON), `fetch` (HTML), `status` (multi-URL async), `decide`, `cache_clear`

**Stack installée :** `httpx[http2]` + `selectolax` + `orjson` (auto-install au premier run si absent)

Clique "Add to My Skills" sur la carte ci-dessous pour l'activer.
**[1780214652576] MANUS:** Lu. Je lis le contenu et le skill-creator avant d'intégrer.
**[1780214648013] USER:** add this skill:



</details>
