---
id: "PIrfBF2GHJOdeSxsEnmlXu"
title: "[✓] Fritz!Box + Deco XE75 Mesh + Sonos — Architecture & Reset Setup"
date: "2026-05-18"
importance: "3"
depth_score: "substantial"
projects: []
tags: ["Fritz!Box", "Deco XE75", "Sonos", "Network Architecture", "WiFi Mesh", "Home Network", "Setup", "Troubleshooting"]
summary: "Configuration et architecture réseau optimale pour Fritz!Box, Deco XE75 Mesh et Sonos, incluant reset et meilleures pratiques."
executive_summary: "The session provides an optimal network architecture and setup guide for integrating a Fritz!Box router with a Deco XE75 Mesh system, specifically addressing compatibility with Sonos. The core solution involves configuring the Deco units in Access Point mode and disabling the Fritz!Box's Wi-Fi to prevent Double NAT, which is crucial for Sonos stability."
context_and_intent: "The user has a Fritz!Box (a recent model, possibly Wi-Fi 6 capable) and a Deco XE75 mesh system. The intent is to set up an optimal network architecture for these devices, specifically considering compatibility with Sonos, and potentially leveraging Wi-Fi 6 capabilities."
what_was_done: "The assistant provided an optimal network architecture, a key concept explaining the rationale behind avoiding Double NAT, a step-by-step reset procedure for the Deco XE75 units, and a specific rule for Sonos integration within this powerful mesh network."
outputs_produced: [{"description": "Detailed steps and rationale for configuring Fritz!Box, Deco XE75, and Sonos for optimal network performance and stability.", "name": "Optimal Architecture and Setup Procedure", "type": "Architectural guidance and setup instructions"}]
key_decisions: ["Configure Deco XE75 in \"Access Point\" mode.", "Disable Wi-Fi on the Fritz!Box.", "Do not connect any Sonos speaker via Ethernet with the powerful XE75 Mesh network."]
lessons_learned: {"discoveries": ["Double NAT is a critical issue for Sonos stability.", "A powerful Mesh network like the Deco XE75 negates the need to connect Sonos speakers via Ethernet."], "failed_or_suboptimal": ["Running both the Fritz!Box and Deco in router mode (leading to Double NAT).", "Connecting Sonos speakers via Ethernet when a strong mesh network is already in place.", "Pressing the Deco reset button for too long (e.g., 10 seconds)."], "worked_well": ["Using the Fritz!Box as the primary router and the Deco XE75 as dedicated Access Points.", "Resetting Deco units by pressing the button for 1-2 seconds."]}
challenges_and_blockers: ["Double NAT (two routers conflicting) which is detrimental to Sonos stability."]
open_questions: []
next_steps: ["Disable Wi-Fi on the Fritz!Box.", "Reset Deco XE75 units following the provided procedure (press reset button 1-2 seconds).", "Configure Deco XE75 in \"Access Point\" mode.", "Ensure no Sonos speakers are connected via Ethernet."]
url: "https://manus.im/app/task/PIrfBF2GHJOdeSxsEnmlXu"
---

# [✓] Fritz!Box + Deco XE75 Mesh + Sonos — Architecture & Reset Setup

| Field | Value |
|-------|-------|
| **Session ID** | `PIrfBF2GHJOdeSxsEnmlXu` |
| **Date** | 2026-05-18 10:34 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/PIrfBF2GHJOdeSxsEnmlXu](https://manus.im/app/sessions/PIrfBF2GHJOdeSxsEnmlXu) |
| **Messages** | 3 user · 4 assistant · 13 total |

## Initial Prompt

Alors, trois décors. Sauf erreur, c'est un, euh... C'est une des dernières frites box. Euh, il y a le wifi- Je pensais que tu l'aidais sur Wi-Fi 6. C'est pour ça que j'ai changé de papier, que... Pour aller avec les décos qui doivent être des 75. Euh...

## First Response

Voici l'architecture optimale et la procédure exacte, structurées pour ton matériel.

### 💡 Le concept clé (Architecture)
Ta Fritz!Box est un excellent routeur. Les Deco XE75 sont d'excellents points d'accès WiFi Mesh. 
👉 **La règle d'or :** Il faut désactiver le WiFi de la Fritz!Box, et configurer les Deco en mode **"Point d'accès" (Access Point)**. Cela évite le "Double NAT" (deux routeurs qui se marchent dessus), ce qui est mortel pour la stabilité de Sonos.

### 🔄 Le Reset des Deco XE75
1. Appareil allumé, trouve le bouton Reset en dessous.
2. Appuie avec un trombone **1 à 2 secondes** (pas plus, pas 10 secondes). La LED devient jaune.
3. Attends 2 minutes jusqu'à ce que ça clignote en bleu.

### 🎵 La règle pour Sonos
Avec un réseau Mesh puissant comme le XE75, **ne branche aucune enceinte Sonos en Ethernet**. Laisse-les toutes en WiFi sur le réseau des Deco. Désactive le "Fast Roaming" dans l'app Deco, car les Sonos détestent ça.

👉 **Le protocole complet étape par étape est dans 

## Conversation Summary

> **User:** Alors, trois décors. Sauf erreur, c'est un, euh... C'est une des dernières frites box. Euh, il y a le wifi- Je pensais que tu l'aidais sur Wi-Fi 6. C'est pour ça que j'ai changé de papier, que... Pour aller avec les décos qui doivent être des 75. Euh...

> **User:** continue

> **User:** YOu are an IT expert helping me with my wifi/network

 have to configure  DECO mesh to extend, think best is Fritz as router (NO WIFI as not mesh?? or better use fritz ifi 6 + extnad with deco?... need o add sonos on top, so mesh must work well 
)but 1rst need to reset them : cant manage

> **Manus:** Voici l'architecture optimale et la procédure exacte, structurées pour ton matériel.

### 💡 Le concept clé (Architecture)
Ta Fritz!Box est un excellent routeur. Les Deco XE75 sont d'excellents points d'accès WiFi Mesh. 
👉 **La règle d'or :** Il faut désactiver le WiFi de la Fritz!Box, et configurer les Deco en mode **"Point d'accès" (Access Point)**. Cela évite le "Double NAT" (deux routeurs qui se marchent dessus), ce qui est mortel pour la stabilité de Sonos.

### 🔄 Le Reset des Deco XE75
1. Appareil allumé, trouve le bouton Reset en dessous.
2. Appuie avec un trombone **1 à 2 secondes** (pas plus, pas 10 secondes). La LED devient jaune.
3. Attends 2 minutes jusqu'à ce que ça clignote en bleu.

### 🎵 La règle pour Sonos
Avec un réseau Mesh puissant comme le XE75, **ne branche aucune ence...

> **Manus:** OK, je synthétise ce que j'ai compris + je complète avec les best practices. On va tout couvrir.

## Full Verbatim

<details>
<summary>Expand full conversation (7 messages)</summary>

**[1779117217766] MANUS:** Voici l'architecture optimale et la procédure exacte, structurées pour ton matériel.

### 💡 Le concept clé (Architecture)
Ta Fritz!Box est un excellent routeur. Les Deco XE75 sont d'excellents points d'accès WiFi Mesh. 
👉 **La règle d'or :** Il faut désactiver le WiFi de la Fritz!Box, et configurer les Deco en mode **"Point d'accès" (Access Point)**. Cela évite le "Double NAT" (deux routeurs qui se marchent dessus), ce qui est mortel pour la stabilité de Sonos.

### 🔄 Le Reset des Deco XE75
1. Appareil allumé, trouve le bouton Reset en dessous.
2. Appuie avec un trombone **1 à 2 secondes** (pas plus, pas 10 secondes). La LED devient jaune.
3. Attends 2 minutes jusqu'à ce que ça clignote en bleu.

### 🎵 La règle pour Sonos
Avec un réseau Mesh puissant comme le XE75, **ne branche aucune enceinte Sonos en Ethernet**. Laisse-les toutes en WiFi sur le réseau des Deco. Désactive le "Fast Roaming" dans l'app Deco, car les Sonos détestent ça.

👉 **Le protocole complet étape par étape est dans ...
**[1779117162114] MANUS:** OK, je synthétise ce que j'ai compris + je complète avec les best practices. On va tout couvrir.
**[1779117158758] USER:** Alors, trois décors. Sauf erreur, c'est un, euh... C'est une des dernières frites box. Euh, il y a le wifi- Je pensais que tu l'aidais sur Wi-Fi 6. C'est pour ça que j'ai changé de papier, que... Pour aller avec les décos qui doivent être des 75. Euh...
**[1779100554125] MANUS:** Tu veux que je continue sans les infos ? Je peux te donner :

**Option A** — Procédure reset générique Deco (couvre 90% des modèles) + archi recommandée Fritz+Deco+Sonos en mode "best practice"

**Option B** — Attendre tes réponses pour une config 100% précise

👉 Dis-moi A ou B — ou donne-moi les infos modèles directement.
**[1779100547939] USER:** continue
**[1779100487697] MANUS:** Contexte capté. Avant de te donner l'archi optimale + procédure reset, j'ai besoin de 3 précisions :

**① Quel modèle exact de DECO ?**
(ex: Deco M5, Deco XE75, Deco BE85…) — ça change la procédure reset et les capacités mesh

**② Quel modèle exact de Fritz !Box ?**
(ex: Fritz!Box 7590, 7690, 6591…) — pour savoir si tu as le Fritz!Repeater ou juste la box

**③ Combien de Deco units tu as, et quel est ton setup actuel ?**
(ex: 3 Deco en place, Fritz comme modem/routeur en entrée, FAI = fibre/ADSL/câble ?)

Avec ça je te donne : reset procédure + archi recommandée Fritz+Deco+Sonos en un bloc.
**[1779100479236] USER:** YOu are an IT expert helping me with my wifi/network

 have to configure  DECO mesh to extend, think best is Fritz as router (NO WIFI as not mesh?? or better use fritz ifi 6 + extnad with deco?... need o add sonos on top, so mesh must work well 
)but 1rst need to reset them : cant manage



</details>