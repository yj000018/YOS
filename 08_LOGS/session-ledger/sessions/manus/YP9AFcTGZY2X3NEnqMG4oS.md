---
id: "YP9AFcTGZY2X3NEnqMG4oS"
title: "[✓] Veille MCP Bimensuelle Juin 2026 — Activation Context7, Mem0, Supabase, Perplexity"
date: "2026-06-15"
importance: "3"
depth_score: "minor"
projects: ["Y-OS", "Manus"]
tags: ["MCP", "Veille", "Activation", "Installation", "Connectors", "Custom MCP"]
summary: ""
executive_summary: "The session provided clear instructions on how to install five non-native MCPs (Exa Search, Mesh, OrgX, WhisperGraph, DecisionNode) as Custom MCPs in Manus. The response detailed the installation method, specific commands (npx or Docker), and required API keys or accounts for each."
context_and_intent: "The user wanted to understand how to activate or install specific MCPs: Exa Search, Mesh (Clay), OrgX, WhisperGraph, and DecisionNode, within the Manus platform."
what_was_done: "The assistant clarified that the requested MCPs are not native to Manus and must be installed as Custom MCPs. It then provided a general method for adding Custom MCPs through Manus settings and a detailed table for each MCP, including its type, installation command (npx or Docker), and any necessary API keys or accounts."
outputs_produced: [{"description": "A table detailing the installation method (Custom MCP), specific npx or Docker commands, and required API keys or accounts for Exa Search, Mesh (Clay), OrgX, WhisperGraph, and DecisionNode MCPs.", "name": "Custom MCP Installation Guide", "type": "Instructions/Documentation"}]
key_decisions: []
lessons_learned: {"discoveries": ["Exa Search, Mesh (Clay), OrgX, WhisperGraph, and DecisionNode are not native Manus MCPs.", "Custom MCPs can be installed via 'Manus → Settings → Connectors → + Add → Custom MCP'.", "Specific npx commands and API keys are required for most custom MCP installations, while WhisperGraph MCP is self-hosted via Docker."], "failed_or_suboptimal": [], "worked_well": ["The assistant provided a clear, structured response with a table format, making the installation instructions easy to follow.", "The response directly addressed the user's query by differentiating native vs. custom MCPs and providing detailed steps."]}
challenges_and_blockers: ["The requested MCPs (Exa Search, Mesh, OrgX, WhisperGraph, DecisionNode) are not natively available in Manus and require custom installation."]
open_questions: []
next_steps: ["The user can proceed to install the specified Custom MCPs by following the provided instructions and commands."]
url: "https://manus.im/app/task/YP9AFcTGZY2X3NEnqMG4oS"
---

# [✓] Veille MCP Bimensuelle Juin 2026 — Activation Context7, Mem0, Supabase, Perplexity

| Field | Value |
|-------|-------|
| **Session ID** | `YP9AFcTGZY2X3NEnqMG4oS` |
| **Date** | 2026-06-15 07:04 UTC |
| **Project** | 9GjP3A95mkVdcWbXKJmQQX |
| **URL** | [https://manus.im/app/sessions/YP9AFcTGZY2X3NEnqMG4oS](https://manus.im/app/sessions/YP9AFcTGZY2X3NEnqMG4oS) |
| **Messages** | 9 user · 16 assistant · 40 total |

## Initial Prompt

4 activation ok
comment faire pour Exa Search MCP, Mesh MCP (Clay), OrgX MCP,WhisperGraph MCP, DecisionNode MCP

## First Response

## Exa, Mesh (Clay), OrgX, WhisperGraph, DecisionNode — Mode d'installation

Ces 5 MCP **ne sont pas dans le catalogue natif Manus** (contrairement à Context7, Mem0, Supabase, Perplexity qui y étaient). Il faut les installer comme **Custom MCP**.

---

### Méthode : Custom MCP dans Manus

**Manus → Settings → Connectors → + Add → Custom MCP**

---

| MCP | Type | Commande d'installation | Clé requise |
|---|---|---|---|
| **Exa Search MCP** | Custom MCP (npx) | `npx -y exa-mcp-server` | `EXA_API_KEY` (déjà dans tes secrets) |
| **Mesh MCP (Clay)** | Custom MCP (npx) | `npx -y @clay-labs/mesh-mcp` | Compte Clay + API key |
| **OrgX MCP** | Custom MCP (npx) | `npx -y @orgx/mcp-server` | Compte OrgX (orgx.ai) |
| **WhisperGraph MCP** | Custom MCP (Docker) | Self-hosted — voir ci-dessous | Aucune (self-hosted) |
| **DecisionNode MCP** | Custom MCP (npx) | `npx -y decisionnode-mcp` | Clé Gemini (embeddings) |

---

### Détail par MCP

**1️⃣ Exa Search MCP** ⭐ Priorité haute
- Config JSON Ma

## Conversation Summary

> **User:** 4 activation ok
comment faire pour Exa Search MCP, Mesh MCP (Clay), OrgX MCP,WhisperGraph MCP, DecisionNode MCP

> **User:** Active Context7, Mem0, Supabase et Perplexit

> **User:** Ok

> **Manus:** ## Exa, Mesh (Clay), OrgX, WhisperGraph, DecisionNode — Mode d'installation

Ces 5 MCP **ne sont pas dans le catalogue natif Manus** (contrairement à Context7, Mem0, Supabase, Perplexity qui y étaient). Il faut les installer comme **Custom MCP**.

---

### Méthode : Custom MCP dans Manus

**Manus → Settings → Connectors → + Add → Custom MCP**

---

| MCP | Type | Commande d'installation | Clé requise |
|---|---|---|---|
| **Exa Search MCP** | Custom MCP (npx) | `npx -y exa-mcp-server` | `EXA_API_KEY` (déjà dans tes secrets) |
| **Mesh MCP (Clay)** | Custom MCP (npx) | `npx -y @clay-labs/mesh-mcp` | Compte Clay + API key |
| **OrgX MCP** | Custom MCP (npx) | `npx -y @orgx/mcp-server` | Compte OrgX (orgx.ai) |
| **WhisperGraph MCP** | Custom MCP (Docker) | Self-hosted — voir ci-dessous | Auc...

> **Manus:** Recherche des 5 MCP dans la config Manus...

## Full Verbatim

<details>
<summary>Expand full conversation (25 messages)</summary>

**[1781635951694] MANUS:** ## Exa, Mesh (Clay), OrgX, WhisperGraph, DecisionNode — Mode d'installation

Ces 5 MCP **ne sont pas dans le catalogue natif Manus** (contrairement à Context7, Mem0, Supabase, Perplexity qui y étaient). Il faut les installer comme **Custom MCP**.

---

### Méthode : Custom MCP dans Manus

**Manus → Settings → Connectors → + Add → Custom MCP**

---

| MCP | Type | Commande d'installation | Clé requise |
|---|---|---|---|
| **Exa Search MCP** | Custom MCP (npx) | `npx -y exa-mcp-server` | `EXA_API_KEY` (déjà dans tes secrets) |
| **Mesh MCP (Clay)** | Custom MCP (npx) | `npx -y @clay-labs/mesh-mcp` | Compte Clay + API key |
| **OrgX MCP** | Custom MCP (npx) | `npx -y @orgx/mcp-server` | Compte OrgX (orgx.ai) |
| **WhisperGraph MCP** | Custom MCP (Docker) | Self-hosted — voir ci-dessous | Aucune (self-hosted) |
| **DecisionNode MCP** | Custom MCP (npx) | `npx -y decisionnode-mcp` | Clé Gemini (embeddings) |

---

### Détail par MCP

**1️⃣ Exa Search MCP** ⭐ Priorité haute
- Config JSON Ma...
**[1781635913198] MANUS:** Recherche des 5 MCP dans la config Manus...
**[1781635907137] USER:** 4 activation ok
comment faire pour Exa Search MCP, Mesh MCP (Clay), OrgX MCP,WhisperGraph MCP, DecisionNode MCP
**[1781623689579] MANUS:** La suggestion a encore été refusée automatiquement. Le log indique **"not accepted"** pour les 4 — ce n'est pas un bug de ma part, c'est le système de confirmation Manus qui rejette les activations dans ce contexte.

**Ce que tu dois faire directement dans l'UI Manus :**

1. Ouvre **Manus → Settings → Connectors** (icône engrenage)
2. Recherche et active un par un :
   - `Context7`
   - `mem0`
   - `Supabase`
   - `Perplexity`

Chaque activation peut demander une clé API :
- **Context7** → pas de clé requise (gratuit)
- **mem0** → clé API Mem0 (créer compte sur mem0.ai)
- **Supabase** → `SUPABASE_ACCESS_TOKEN` (déjà dans tes secrets selon le registre)
- **Perplexity** → clé SONAR API (déjà dans tes secrets)

Je ne peux pas contourner la confirmation UI — c'est une protection Manus intentionnelle.
**[1781623658715] MANUS:** Activation des 4 connecteurs en cours...
**[1781623654677] USER:** Active Context7, Mem0, Supabase et Perplexit
**[1781623641570] MANUS:** Noté. Résumé de la session planifiée :

**Accompli ✅**
- Veille MCP 3 couches exécutée (4 sources, ~36k MCP indexés)
- Rapport publié dans Notion TECH : [🔌 RADAR-MCP — Rapport 15 Juin 2026](https://app.notion.com/p/38035e218cf8817ca235cf5e684b94bf)
- 7 MCP pertinents scorés + 3 signaux émergents identifiés

**Pending — action manuelle requise**
Dans ta prochaine session interactive, dis : *"Active Context7, Mem0, Supabase et Perplexity"* → confirmation en 1 clic.
**[1781623632649] USER:** Ok
**[1781617018613] MANUS:** ## Statut MCP — 16 Juin 2026

La config lue ici est la **config de session planifiée** (snapshot isolé), pas la config live de ton compte Manus. C'est pourquoi seul "My Browser" apparaît actif dans ce contexte.

**Statut réel des 4 connecteurs ciblés :**

| Connecteur | Statut config session | Action requise |
|---|---|---|
| **Context7** | `false` (non confirmé) | Activer manuellement |
| **Mem0** | `false` (non confirmé) | Activer manuellement |
| **Supabase** | `false` (non confirmé) | Activer manuellement |
| **Perplexity** | `false` (non confirmé) | Activer manuellement |

**Cause** : `manus-config config save` soumet une *suggestion* — elle requiert ta confirmation dans l'UI Manus. Les sessions planifiées ne peuvent pas auto-confirmer (sécurité by design).

**Action directe** → Dans une session interactive, dis simplement :
> "Active Context7, Mem0, Supabase et Perplexity"

Je soumets, tu confirmes en 1 clic. Ça prend 30 secondes.
**[1781616985737] MANUS:** Vérification statuts MCP en cours...
**[1781616982472] USER:** Vérifie nouveaux status installations MCP
**[1781616967326] USER:** Erudite état nouveau installations
**[1781508708598] MANUS:** Le mécanisme `manus-config config save` soumet les changements pour **confirmation utilisateur** — c'est une contrainte de sécurité Manus, non contournable depuis une session planifiée ou autonome.

**État actuel :**

| Connecteur | Statut | Action requise |
|---|---|---|
| Context7 | Désactivé | Confirmation manuelle |
| Mem0 | Désactivé | Confirmation manuelle |
| Supabase | Désactivé | Confirmation manuelle |
| Perplexity | Désactivé | Confirmation manuelle |

**Pour activer les 4 en une fois :**
→ Va dans **Manus → Settings → Connectors**
→ Recherche et active : `Context7`, `mem0`, `Supabase`, `Perplexity`

Ou dans une session interactive (non planifiée), dis-moi "active Context7, Mem0, Supabase, Perplexity" — je soumets la suggestion et tu confirmes en 1 clic.

Le registre Notion a été mis à jour avec les recommandations. Le rapport RADAR-MCP 15 Juin 2026 est publié sous TECH : https://app.notion.com/p/38035e218cf8817ca235cf5e684b94bf
**[1781508653996] MANUS:** Session planifiée — confirmation manuelle requise pour Supabase + Perplexity. Mise à jour du registre Notion en cours.
**[1781508649400] USER:** [Auto-reply] Please continue the task based on current context, proceed if you are on track. Do not ask the same question repeatedly.
**[1781508649302] MANUS:** Les deux connecteurs ont été soumis pour activation mais la confirmation a été refusée automatiquement (probablement une restriction de la session planifiée).

**Supabase** et **Perplexity** nécessitent une confirmation manuelle de ta part dans l'interface Manus.

Pour les activer :
1️⃣ Va dans **Manus → Settings → Connectors**
2️⃣ Recherche "Supabase" → activer
3️⃣ Recherche "Perplexity" → activer

Note : Supabase nécessitera ton `SUPABASE_ACCESS_TOKEN` (déjà dans les secrets selon le registre). Perplexity nécessitera ta clé SONAR.

Veux-tu que je tente une autre approche, ou tu confirmes manuellement ?
**[1781508609684] MANUS:** Activation Supabase + Perplexity en cours...
**[1781508606102] USER:** Active Supabase et perplexity
**[1781508593241] MANUS:** Activation Mem0 + Context7 en cours — lecture config Manus.
**[1781508588621] USER:** Active mem0 et context7
**[1781507599002] MANUS:** ## RADAR-MCP — Rapport 15 Juin 2026 ✅

Page Notion publiée sous TECH : [🔌 RADAR-MCP — Rapport 15 Juin 2026](https://app.notion.com/p/38035e218cf8817ca235cf5e684b94bf)

---

### Couche 2 — Top 7 Pertinents Y-OS

| Rang | MCP | Agent | Reco |
|---|---|---|---|
| 1 | **Context7** (upstash) | TECH/DEV | ✅ ACTIVER — 57k stars, 6.4k uses, déjà en attente |
| 2 | **Mem0** (mem0ai) | KMM/CORE | ✅ ACTIVER — 58k stars, mémoire cross-session, déjà en attente |
| 3 | **Figma-Context-MCP** | CREA/TECH | ✅ ACTIVER — 15k stars, pont design-to-code, déjà en attente |
| 4 | **Supabase MCP** | TECH/DATA | ✅ ACTIVER — DB relationnelle + Edge Functions, nouveau |
| 5 | **Exa Search MCP** | TECH/KMM | ✅ ACTIVER — 32k uses Smithery, clé déjà dans secrets |
| 6 | **Perplexity MCP** | KMM/TECH | 👁️ SURVEILLER — déjà couvert via SONAR_API_KEY |
| 7 | **Mesh MCP (Clay)** | COMM/CRM | 👁️ SURVEILLER — prospection B2B, partiel avec HubSpot |

---

### Couche 3 — 3 Signaux Émergents

**Signal 1 — OrgX MCP** : OS or...
**[1781507563175] MANUS:** Page Notion créée. Ajout du commentaire avec tag Manus en cours...
**[1781507085800] MANUS:** Mode BALANCED activé. Scraping parallèle des 4 sources MCP en cours...
**[1781507063467] MANUS:** Veille MCP bimensuelle lancée. Lecture du skill yos-optimizer en cours avant exécution.
**[1781507060495] USER:** Effectuer la veille MCP bimensuelle pour Y-OS (agent TECH-ARCHI).

SOURCES :
- mcp.so, smithery.ai, github.com/punkpeye/awesome-mcp-servers, glama.ai/mcp/servers

---

LOGIQUE DE FILTRAGE EN 3 COUCHES :

COUCHE 1 — TRACTION OBJECTIVE (score marché)
Critères indépendants de Y-OS :
- Stars GitHub (volume + croissance 30j)
- Score Smithery / upvotes communauté
- Nouveauté < 3 mois + momentum rapide
- Mentions communauté IA/dev (Reddit, HN, Twitter)
→ Garder les top 20 par score objectif

COUCHE 2 — PERTINENCE Y-OS (focus)
Filtrer les 20 par alignement avec les besoins Y-OS actuels :
- Agents actifs : CORE, KMM, FIN, PROJ, CREA, TECH, COMM
- Stack existant : voir registre Notion ID 31435e21-8cf8-8136-83ba-e720d799b0b6
- Éliminer doublons fonctionnels avec connecteurs déjà actifs
→ Garder les top 5-7 pertinents

COUCHE 3 — OUVERTURE D'HORIZON (signal faible)
Parmi les top 20 de la couche 1, identifier 2-3 MCP qui :
- N'entrent pas dans les catégories Y-OS actuelles
- Mais représentent une n...



</details>