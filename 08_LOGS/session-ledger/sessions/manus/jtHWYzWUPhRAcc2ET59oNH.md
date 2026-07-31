---
id: "jtHWYzWUPhRAcc2ET59oNH"
title: "[✓] XR Copilot MVP Development - Full Flutter App Architecture"
date: "2026-03-14"
importance: "3"
depth_score: "substantial"
projects: ["XR Copilot", "Y-OS", "CasaTAO"]
tags: ["XR"]
summary: ""
executive_summary: "The session focused on defining and delivering the MVP for an \"XR Copilot\" Flutter app. The app aims to be a useful daily wearable interface combining AI copilot features and translation, validating the core architecture for future XR applications. The MVP was delivered as a complete Flutter project with no errors and minor warnings."
context_and_intent: "The intent was to build a minimal viable product (MVP) for an Android XR app, specifically an \"XR Copilot\" that serves as a combined Copilot and Translation HUD. This app is designed to provide immediate value and validate the underlying architecture for all subsequent XR applications."
what_was_done: "The session outlined the core features of the XR Copilot MVP: voice input (speech-to-text, AI routing for commands like translation, smart home control, and summarization), AI copilot responses (short, glanceable text in an XR panel), and a continuous translation mode providing subtitles. The first response indicates the complete Flutter project for this MVP was delivered."
outputs_produced: [{"description": "A complete Flutter project for the XR Copilot MVP, delivered with 0 errors and 10 minor warnings, implementing voice input, AI responses, and translation mode.", "name": "XR Copilot MVP", "type": "Flutter Application"}]
key_decisions: []
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": []}
challenges_and_blockers: []
open_questions: []
next_steps: []
url: "https://manus.im/app/task/jtHWYzWUPhRAcc2ET59oNH"
---

# [✓] XR Copilot MVP Development - Full Flutter App Architecture

| Field | Value |
|-------|-------|
| **Session ID** | `jtHWYzWUPhRAcc2ET59oNH` |
| **Date** | 2026-03-14 22:13 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/jtHWYzWUPhRAcc2ET59oNH](https://manus.im/app/sessions/jtHWYzWUPhRAcc2ET59oNH) |
| **Messages** | 9 user · 14 assistant · 41 total |

## Initial Prompt

Below is a concrete MVP plan for the first Android XR app you should build.
Goal: create a useful daily wearable interface that validates the architecture for all the other apps.

The best first app is a combined Copilot + Translation HUD.

This gives immediate value and tests most of the system.

⸻

MVP XR App: “XR Copilot”

Purpose

A minimal XR interface that allows you to:
	•	speak to your AI system
	•	get short responses in the glasses
	•	translate speech
	•	send commands to Home Assistant / Y-OS

This single app validates 90% of the stack.

⸻

Core features

1️⃣ Voice input

User speaks a command.

Example:

“Translate this conversation”
“Turn off CasaTAO lights”
“Summarize this idea”

Pipeline:

voice input
↓
speech-to-text
↓
AI routing


⸻

2️⃣ AI copilot response

Short response displayed in XR panel.

Example UI:

AI Copilot

• Suggestion 1
• Suggestion 2
• Next step

Important:
Responses must be short and glanceable.

⸻

3️⃣ Translation mode

Continuous translation subtitles

## First Response

MVP **XR Copilot** livré. Projet Flutter complet, 0 erreur, 10 warnings mineurs (deprecations non bloquantes).

---

## Ce qui a été généré

**2 302 lignes de Dart** réparties en 15 fichiers :

| Fichier | Rôle |
|---|---|
| `halo_adapter.dart` | Y-OS Halo Adapter — BLE scan/connect, display Lua, audio stream, tap events |
| `voice_module.dart` | STT on-device + Whisper API, intent detection (5 catégories) |
| `copilot_module.dart` | LLM routing OpenAI / Y-OS backend, historique, truncation HUD |
| `translation_module.dart` | Boucle continue STT → GPT-4o-mini → HUD subtitle |
| `ha_module.dart` | HA REST API, entity registry, NLP command parser, scoring |
| `app_controller.dart` | Orchestrateur central, pipeline voix → intent → module → HUD |
| `home_screen.dart` | UI principale : HUD overlay, mode selector, activity log, voice button |
| `settings_screen.dart` | Config API keys (secure storage), HA URL/token |
| `app_theme.dart` | Thème sombre minimaliste, couleurs HUD cyan/vert/ambre

## Conversation Summary

> **User:** Below is a concrete MVP plan for the first Android XR app you should build.
Goal: create a useful daily wearable interface that validates the architecture for all the other apps.

The best first app is a combined Copilot + Translation HUD.

This gives immediate value and tests most of the system.

⸻

MVP XR App: “XR Copilot”

Purpose

A minimal XR interface that allows you to:
	•	speak to your AI system
	•	get short responses in the glasses
	•	translate speech
	•	send commands to Home Assistant ...

> **User:** Je valide auth

> **User:** Utilise browser

> **Manus:** MVP **XR Copilot** livré. Projet Flutter complet, 0 erreur, 10 warnings mineurs (deprecations non bloquantes).

---

## Ce qui a été généré

**2 302 lignes de Dart** réparties en 15 fichiers :

| Fichier | Rôle |
|---|---|
| `halo_adapter.dart` | Y-OS Halo Adapter — BLE scan/connect, display Lua, audio stream, tap events |
| `voice_module.dart` | STT on-device + Whisper API, intent detection (5 catégories) |
| `copilot_module.dart` | LLM routing OpenAI / Y-OS backend, historique, truncation HUD |
| `translation_module.dart` | Boucle continue STT → GPT-4o-mini → HUD subtitle |
| `ha_module.dart` | HA REST API, entity registry, NLP command parser, scoring |
| `app_controller.dart` | Orchestrateur central, pipeline voix → intent → module → HUD |
| `home_screen.dart` | UI principale : HUD over...

> **Manus:** Specs lues. Je planifie et démarre immédiatement.

## Full Verbatim

<details>
<summary>Expand full conversation (23 messages)</summary>

**[1773535362144] MANUS:** MVP **XR Copilot** livré. Projet Flutter complet, 0 erreur, 10 warnings mineurs (deprecations non bloquantes).

---

## Ce qui a été généré

**2 302 lignes de Dart** réparties en 15 fichiers :

| Fichier | Rôle |
|---|---|
| `halo_adapter.dart` | Y-OS Halo Adapter — BLE scan/connect, display Lua, audio stream, tap events |
| `voice_module.dart` | STT on-device + Whisper API, intent detection (5 catégories) |
| `copilot_module.dart` | LLM routing OpenAI / Y-OS backend, historique, truncation HUD |
| `translation_module.dart` | Boucle continue STT → GPT-4o-mini → HUD subtitle |
| `ha_module.dart` | HA REST API, entity registry, NLP command parser, scoring |
| `app_controller.dart` | Orchestrateur central, pipeline voix → intent → module → HUD |
| `home_screen.dart` | UI principale : HUD overlay, mode selector, activity log, voice button |
| `settings_screen.dart` | Config API keys (secure storage), HA URL/token |
| `app_theme.dart` | Thème sombre minimaliste, couleurs HUD cyan/vert/ambre...
**[1773534761781] MANUS:** Specs lues. Je planifie et démarre immédiatement.
**[1773534758343] USER:** Below is a concrete MVP plan for the first Android XR app you should build.
Goal: create a useful daily wearable interface that validates the architecture for all the other apps.

The best first app is a combined Copilot + Translation HUD.

This gives immediate value and tests most of the system.

⸻

MVP XR App: “XR Copilot”

Purpose

A minimal XR interface that allows you to:
	•	speak to your AI system
	•	get short responses in the glasses
	•	translate speech
	•	send commands to Home Assistant / Y-OS

This single app validates 90% of the stack.

⸻

Core features

1️⃣ Voice input

User speaks a command.

Example:

“Translate this conversation”
“Turn off CasaTAO lights”
“Summarize this idea”

Pipeline:

voice input
↓
speech-to-text
↓
AI routing


⸻

2️⃣ AI copilot response

Short response displayed in XR panel.

Example UI:

AI Copilot

• Suggestion 1
• Suggestion 2
• Next step

Important:
Responses must be short and glanceable.

⸻

3️⃣ Translation mode

Continuous translation subtitles...
**[1773534605070] MANUS:** Le browser n'est pas connecté à ton compte ChatGPT — il affiche la page de login anonyme et le redirect vers la conversation partagée ne fonctionne pas sans session active.

**Deux options :**

1. **Prends le contrôle du browser** pour te connecter à ChatGPT, puis je reprendrai la navigation
2. **Colle directement le contenu** de la conversation ici (copier-coller du texte)
**[1773534526889] MANUS:** OK, je reprends la navigation après ton auth.
**[1773534523666] USER:** Je valide auth
**[1773534488635] MANUS:** Je tente d'accéder via le browser avec authentification.
**[1773534485686] USER:** Utilise browser
**[1773534454123] MANUS:** Le lien ChatGPT nécessite une connexion — la conversation partagée n'est pas accessible publiquement sans authentification.

Deux options :

1. **Colle le contenu ici** directement (copier-coller du texte de la conversation)
2. **Résume les specs du MVP** : quelles features, quel flux, quelle stack attendue

Je peux démarrer immédiatement dès que j'ai les specs.
**[1773534399043] MANUS:** Je lis le document de spécifications du MVP avant de planifier.
**[1773534394050] USER:** Génère MVP described here https://chatgpt.com/share/e/69b5fc8f-3204-800c-9771-56d9dd76dbbf
**[1773530557794] MANUS:** **Oui. C'est exactement le modèle.**

---

## Ce que Halo est, architecturalement

Halo n'est pas un téléphone. C'est un **périphérique BLE avec 5 canaux d'I/O** :

| Canal | Direction | Ce que ça permet |
|---|---|---|
| **Microphone** | Input → app | Capture audio, STT, commandes vocales, détection d'ambiance |
| **Capteur optique** | Input → app | Inférence visuelle, détection d'objets, pointage |
| **IMU 6 axes** | Input → app | Orientation tête, gestes, tap, direction du regard |
| **Micro OLED HUD** | Output ← app | Texte, images, icônes, sous-titres, dashboards minimalistes |
| **Haut-parleurs (conduction osseuse)** | Output ← app | Audio, TTS, alertes sonores, réponses vocales |

**N'importe quelle app qui peut parler à un périphérique BLE peut utiliser ces 5 canaux.** Le SDK Flutter (`frame_ble` + `frame_msg`) abstrait la complexité BLE.

---

## Conséquence directe

Tout ce qu'une app iOS/Android peut faire, elle peut maintenant le faire **avec Halo comme interface** :

| Typ...
**[1773530532686] USER:** Donc vraiment capacité de développer tout app iOS ou SaaS qui utilise Halo comme input ou display/audio output? (Asked to Manaus)
**[1773530361133] MANUS:** **Oui. C'est même une meilleure approche que la vision pure.**

---

## Pourquoi le pointage du doigt est supérieur

Le problème de la vision seule : Halo voit "lampe" mais ne sait pas laquelle parmi plusieurs. Le pointage résout exactement ce problème — il fournit un **vecteur directionnel précis** vers la cible.

---

## Comment ça fonctionne techniquement

```
Utilisateur pointe le doigt vers la lampe
  → IMU Halo (gyro + accéléro 6 axes) capture l'orientation de la tête
  → Capteur optique Halo confirme "objet lumineux / lampe" dans l'axe du regard
  → App croise : orientation tête + carte spatiale CasaTAO → entity_id
  → Utilisateur dit "allume toi"
  → Commande HA
```

Le pointage du doigt **aligne naturellement la tête** dans la direction de la cible. L'IMU de Halo capte cet azimut. C'est le signal le plus fiable disponible sans caméra haute résolution.

---

## Ce qu'il faut construire côté app

| Composant | Description | Complexité |
|---|---|---|
| **Carte spatiale CasaTAO**...
**[1773530339699] USER:** Alternative: je pointe du doigt la lampe: aide à reconnaître non?
**[1773530260935] MANUS:** Trois méthodes, par ordre de complexité croissante.

---

## Méthode A — Vocal explicite (le plus simple)

L'utilisateur dit **"allume la lampe du salon"**. Le LLM extrait l'entité nommée et la mappe sur un `entity_id` HA.

Aucune vision requise. Zéro complexité. Limite : l'utilisateur doit nommer.

---

## Méthode B — Zone / Pièce (le plus robuste pour CasaTAO)

L'app sait **dans quelle pièce tu es** (BLE beacons, WiFi RSSI, ou simplement un menu de sélection de pièce dans l'app). "Allume toi" = lampe de la pièce courante.

Pas de vision. Très fiable. C'est ce que font 99% des apps domotiques vocales.

---

## Méthode C — Vision Halo (le plus ambitieux)

C'est la question réelle. Voici comment ça fonctionne concrètement :

```
Capteur optique Halo
  → image basse résolution (le NPU Alif B1 fait l'inférence)
  → modèle de détection d'objets (YOLO nano ou équivalent)
  → détecte : "lampe de table"
  → l'app mappe : "lampe de table" + "pièce courante" → entity_id HA
  → commande HA
```

...
**[1773530239400] USER:** Reconnaissance d elamlampe = fait comment?
**[1773530230201] MANUS:** **Oui. Scénario 100% faisable.** C'est même l'un des cas d'usage les plus propres de l'architecture trois-tiers.

---

## Flux exact du scénario

```
Utilisateur regarde la lampe → dit "allume toi"
        ↓
Halo mic capture l'audio
        ↓ BLE (frame_msg)
App Compagnon iPhone
  → STT : "allume toi"
  → Intent Detection : commande domotique
  → Identification de la cible : lampe (via vision ou contexte)
        ↓ HTTPS / WebSocket
Y-OS Halo Gateway
  → Agent Router → Home Assistant Tool
        ↓ HA REST API / WebSocket
Home Assistant
  → light.turn_on(entity_id: "light.lampe_X")
        ↓ confirmation
App Compagnon
        ↓ BLE
Halo HUD → affiche "✓ Lampe allumée"
```

---

## Points techniques clés

| Point | Réalité |
|---|---|
| **Capture vocale** | Halo mic → BLE → app : confirmé, c'est le flux de base |
| **STT sur téléphone** | Whisper local ou API (OpenAI, Deepgram) : trivial |
| **Intent detection** | LLM léger sur téléphone ou Y-OS : "allume toi" → `light.turn_on` |
| **Id...
**[1773530204566] USER:** Je regarde une lampe et dis “allume toi”, halo peut faire passer l ordre qui peut être analysé sur le tel via une app à designer pour piloter la maison via HA. Scénario ok?
**[1773527290898] MANUS:** Plan d'architecture complet livré. Le document couvre :

1. **Contexte technique Halo** — specs hardware confirmées, modèle de dev hérité de Frame, évolution mars 2026 (IA on-device)
2. **Architecture 3-tiers** — Device (Halo/Lua/ZephyrOS) ↔ Bridge (Flutter Companion App) ↔ Backend (Y-OS)
3. **Composants détaillés** — chaque tier décomposé avec ses responsabilités
4. **2 flux de séquence** — Commande Vocale et Capture Mémoire, avec diagrammes
5. **Y-OS Halo Adapter** — 4 modules SDK (display, audio, input, system) avec primitives documentées
6. **Backlog 10 micro-apps** — priorisées P0/P1/P2, avec les 3 fondatrices identifiées
7. **Contraintes et risques** — SDK pas encore mature, latence BLE, taille affichage, batterie
8. **Plan d'exécution** — 6 phases estimées

4 diagrammes d'architecture inclus (architecture globale, flux commande vocale, flux capture mémoire, adapter layer).
**[1773526975224] MANUS:** Recherche terminée. Architecture conçue. Je génère maintenant les diagrammes d'architecture et les flux.
**[1773526424230] MANUS:** Je lis les fichiers joints pour comprendre la demande.
**[1773526418605] USER:** Can you?



</details>