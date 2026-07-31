---
session_id: baAN1J7u248tAG4G7uzDY5
title: "...mymind.com : API/MCP ?"
date: 2026-07-29 21:38 UTC
url: https://manus.im/app/sessions/baAN1J7u248tAG4G7uzDY5
project_id: deP744efwf6gY4e7rA8M7C
user_messages: 1
assistant_messages: 4
total_messages: 7
processed: true
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
