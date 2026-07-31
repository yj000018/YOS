---
id: "fBp5U8X4djsSbCVBP9jHr5"
title: "[✓] Y-OS Proto Tana Import + Architecture ngrok Full-Mac Control Panel"
date: "2026-03-14"
importance: "3"
depth_score: "standard"
projects: ["Y-OS", "Tana Import", "Full-Mac Control Panel"]
tags: ["Y-OS", "Tana"]
summary: ""
executive_summary: "The session provided a direct and comprehensive response to the user's queries about Peekaboo. It confirmed Peekaboo is free and open-source under an MIT license, detailed two installation methods for macOS (Homebrew and npx), outlined required macOS permissions, and listed the tool's core functionalities."
context_and_intent: "The user inquired about the Peekaboo tool, specifically asking if it is free, how to download it, and how to install it using bash commands on a Mac."
what_was_done: "The assistant confirmed Peekaboo's open-source and free status, provided two detailed installation methods for macOS (Homebrew and npx), explained the necessary macOS permissions, and listed the main functionalities of Peekaboo v3 with examples of commands."
outputs_produced: [{"description": "Confirmation that Peekaboo is free, open-source, and licensed under MIT, with details on its active maintenance.", "name": "Peekaboo Cost and License Information", "type": "Information"}, {"description": "Bash command for installing Peekaboo via Homebrew, recommended for CLI.", "name": "Peekaboo Installation Command (Homebrew)", "type": "Code Snippet"}, {"description": "Bash command for installing Peekaboo via npx for the MCP server (Node 22+).", "name": "Peekaboo Installation Command (npx)", "type": "Code Snippet"}, {"description": "Instructions for granting necessary macOS permissions (Screen Recording, Accessibility) after installation.", "name": "macOS Permissions Guide for Peekaboo", "type": "Instructions"}, {"description": "A table listing key Peekaboo v3 commands and their corresponding actions (e.g., image, see, click, type, press).", "name": "Peekaboo v3 Command List", "type": "Table"}]
key_decisions: ["Confirmed Peekaboo is free and open-source under the MIT license.", "Recommended Homebrew for CLI installation of Peekaboo on macOS."]
lessons_learned: {"discoveries": ["Peekaboo is an actively maintained, open-source tool with a MIT license.", "It offers two primary installation methods on macOS: Homebrew for CLI and npx for a MCP server.", "Specific macOS permissions (Screen Recording, Accessibility) are required post-installation for Peekaboo to function."], "failed_or_suboptimal": [], "worked_well": ["The assistant provided clear, direct, and comprehensive answers to all user questions.", "Specific bash commands for installation were provided, along with a recommendation for the preferred method.", "Additional useful context, such as required permissions and a list of functionalities, was included."]}
challenges_and_blockers: []
open_questions: []
next_steps: ["The user can proceed with installing Peekaboo using the provided instructions."]
url: "https://manus.im/app/task/fBp5U8X4djsSbCVBP9jHr5"
---

# [✓] Y-OS Proto Tana Import + Architecture ngrok Full-Mac Control Panel

| Field | Value |
|-------|-------|
| **Session ID** | `fBp5U8X4djsSbCVBP9jHr5` |
| **Date** | 2026-03-14 03:18 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/fBp5U8X4djsSbCVBP9jHr5](https://manus.im/app/sessions/fBp5U8X4djsSbCVBP9jHr5) |
| **Messages** | 12 user · 22 assistant · 63 total |

## Initial Prompt

Ok on garde les 3 comme ça
Peekaboo gratuit? Download? Install en bash?

## First Response

**Peekaboo — réponse directe.**

---

## Gratuit ? Oui. Licence MIT.

Open source, aucun abonnement, aucun coût. 2.8k stars GitHub, maintenu activement (dernier commit : hier).

---

## Installation sur ton Mac — 2 commandes

**Option A — CLI via Homebrew (recommandé)**
```bash
brew install steipete/tap/peekaboo
```

**Option B — MCP server via npx (Node 22+, sans install globale)**
```bash
npx -y @steipete/peekaboo
```

**Permissions macOS requises après install :**
```bash
peekaboo permissions grant
# → macOS demande : Screen Recording + Accessibility
# → tu cliques OK dans les deux popups système
```

---

## Ce que Peekaboo v3 sait faire (liste complète)

| Commande | Action |
|----------|--------|
| `peekaboo image` | Screenshot écran / fenêtre / menu bar |
| `peekaboo see` | Capture + analyse UI → retourne les éléments cliquables |
| `peekaboo click` | Click par label ("bouton Clean"), ID ou coordonnées |
| `peekaboo type` | Tape du texte dans un champ |
| `peekaboo press` | Touc

## Conversation Summary

> **User:** Ok on garde les 3 comme ça
Peekaboo gratuit? Download? Install en bash?

> **User:** Super
Peekabo pourquoi ? Autres alternatives suggérées pas mieux?

> **User:** L'étape suivante, c'est vraiment le contrôle du Mac. Donc, il y a des choses qui peuvent se passer en script, j'imagine, réorganiser mes fichiers et cetera. Tout ça, c'est en back-end script, mais il y a des choses qui se passent en front-end, lancer le scan sur CleanMyMac par exemple. Donc, il faut que j'ai un agent front-end à la Playwright qui puisse cliquer et faire des actions et voir le résultat. Rajoute bien ça à notre module.  Et regarde en même temps s'il existe pas des des solutions SA...

> **Manus:** **Peekaboo — réponse directe.**

---

## Gratuit ? Oui. Licence MIT.

Open source, aucun abonnement, aucun coût. 2.8k stars GitHub, maintenu activement (dernier commit : hier).

---

## Installation sur ton Mac — 2 commandes

**Option A — CLI via Homebrew (recommandé)**
```bash
brew install steipete/tap/peekaboo
```

**Option B — MCP server via npx (Node 22+, sans install globale)**
```bash
npx -y @steipete/peekaboo
```

**Permissions macOS requises après install :**
```bash
peekaboo permissions grant
# → macOS demande : Screen Recording + Accessibility
# → tu cliques OK dans les deux popups système
```

---

## Ce que Peekaboo v3 sait faire (liste complète)

| Commande | Action |
|----------|--------|
| `peekaboo image` | Screenshot écran / fenêtre / menu bar |
| `peekaboo see` | Capture ...

> **Manus:** Vérification de l'installation Peekaboo.

## Full Verbatim

<details>
<summary>Expand full conversation (34 messages)</summary>

**[1773485072167] MANUS:** **Peekaboo — réponse directe.**

---

## Gratuit ? Oui. Licence MIT.

Open source, aucun abonnement, aucun coût. 2.8k stars GitHub, maintenu activement (dernier commit : hier).

---

## Installation sur ton Mac — 2 commandes

**Option A — CLI via Homebrew (recommandé)**
```bash
brew install steipete/tap/peekaboo
```

**Option B — MCP server via npx (Node 22+, sans install globale)**
```bash
npx -y @steipete/peekaboo
```

**Permissions macOS requises après install :**
```bash
peekaboo permissions grant
# → macOS demande : Screen Recording + Accessibility
# → tu cliques OK dans les deux popups système
```

---

## Ce que Peekaboo v3 sait faire (liste complète)

| Commande | Action |
|----------|--------|
| `peekaboo image` | Screenshot écran / fenêtre / menu bar |
| `peekaboo see` | Capture + analyse UI → retourne les éléments cliquables |
| `peekaboo click` | Click par label ("bouton Clean"), ID ou coordonnées |
| `peekaboo type` | Tape du texte dans un champ |
| `peekaboo press` | Touc...
**[1773485036636] MANUS:** Vérification de l'installation Peekaboo.
**[1773485032703] USER:** Ok on garde les 3 comme ça
Peekaboo gratuit? Download? Install en bash?
**[1773484868264] MANUS:** **Comparaison honnête — pourquoi Peekaboo et pas les autres.**

---

## Analyse par critère

| Critère | Peekaboo | macOS-use | UI-TARS | Claude Computer Use | osascript + cliclick |
|---------|----------|-----------|---------|---------------------|----------------------|
| **Intégration Manus** | ✅ MCP natif | ❌ Python local seulement | ❌ app desktop fermée | ⚠️ API Anthropic (pas Manus direct) | ✅ via SSH |
| **Vision écran** | ✅ screenshot + analyse AI | ✅ screenshot | ✅ VLM intégré | ✅ screenshot | ❌ aucune |
| **Actions GUI** | ✅ click, type, scroll | ✅ click, keyboard | ✅ souris + clavier | ✅ souris + clavier | ✅ partiel |
| **Accès distant** | ✅ via tunnel | ❌ local seulement | ❌ local seulement | ✅ mais sandbox Anthropic | ✅ via SSH |
| **Installation** | `brew install` | pip + config Python | app DMG | API key | natif macOS |
| **Maintenance** | ✅ actif (2025-2026) | ⚠️ jeune projet | ✅ ByteDance | ✅ Anthropic | ✅ natif |
| **Coût** | Gratuit | Gratuit | Gratuit | Tokens Anthr...
**[1773484843125] USER:** Super
Peekabo pourquoi ? Autres alternatives suggérées pas mieux?
**[1773484691058] MANUS:** **Carte complète — solutions existantes + recommandation.**

---

## Solutions existantes : contrôle Mac par LLM (vision + action)

| Solution | Type | Vision | Action | Accès distant | Intégration Manus |
|----------|------|--------|--------|---------------|-------------------|
| **Peekaboo** | MCP server macOS | ✅ screenshot + analyse AI | ✅ GUI automation (click, type) | Via tunnel | ✅ MCP natif |
| **macOS-use** | Agent Python (fork browser-use) | ✅ screenshot | ✅ click, keyboard, scroll | Local | ⚠️ via SSH |
| **UI-TARS Desktop** | App desktop (ByteDance) | ✅ VLM natif | ✅ souris + clavier | Local | ⚠️ via SSH |
| **Claude Computer Use** | API Anthropic | ✅ screenshot | ✅ souris + clavier | Via sandbox | ✅ API directe |
| **ScreenAgent** | Research framework | ✅ VLM | ✅ actions | Local | ⚠️ complexe |
| **osascript / cliclick** | CLI macOS natif | ❌ | ✅ actions shell | Via SSH | ✅ SSH direct |

---

## Recommandation architecturale

**Ne pas réinventer la roue. Combiner deux outi...
**[1773484652515] MANUS:** Recherche en cours — solutions existantes pour contrôle Mac par LLM (vision + action).
**[1773484648337] USER:** L'étape suivante, c'est vraiment le contrôle du Mac. Donc, il y a des choses qui peuvent se passer en script, j'imagine, réorganiser mes fichiers et cetera. Tout ça, c'est en back-end script, mais il y a des choses qui se passent en front-end, lancer le scan sur CleanMyMac par exemple. Donc, il faut que j'ai un agent front-end à la Playwright qui puisse cliquer et faire des actions et voir le résultat. Rajoute bien ça à notre module.  Et regarde en même temps s'il existe pas des des solutions SAS ou app déjà prêtes pour ça et qui permettent à des agents LLM comme Manus de contrôler le Mac avec la vision et l'action pour pas réinventer la roue non plus.
**[1773484147925] MANUS:** **Architecture d'abord. Exécution ensuite.**

Laisse-moi modéliser l'équipe Y-OS complète avec les bons rôles avant de coder quoi que ce soit.

---

## Y-OS Agent Team — Structure proposée

```
Manus (Orchestrateur central)
    │
    ├── IT Manager          ← rôle / persona
    │       │
    │       ├── Mac Agent   ← sous-agent technique
    │       ├── iOS Agent   ← sous-agent (limité, via projection)
    │       └── NAS Agent   ← sous-agent (SSH NAS)
    │
    ├── Helpdesk            ← rôle / interface utilisateur
    │       │
    │       └── délègue à IT Manager pour exécution
    │
    ├── Knowledge Manager   ← Tana + Notion
    ├── Project Manager     ← Asana / Linear
    └── ...autres rôles Y-OS
```

---

## Distinction critique : Rôle vs Agent

| Concept | Définition | Exemple |
|---------|------------|---------|
| **Rôle** | Persona avec responsabilités, scope, style de réponse | "IT Manager" — pense en systèmes, parle en KPIs |
| **Agent** | Capacité d'exécution technique sur...
**[1773484120748] USER:** On va aller pour le développement et faire tout. On va bien réfléchir l'architecture. Est-ce que j'ai un agent qui s'appelle Helpdesk qui a un sous-agent de ou iOS Mac agent ? Est-ce que j'ai un  un des rôles dans mon équipe qui est le IT manager et qui contrôle entre autres le Mac via ce sous-agent. Donc en fait, je pourrais avoir IT management, le IT manager qui est le chef de l'équipe avec un Mac agent qui est juste un agent mais pas un agent local.  Il faut bien réfléchir pour que je puisse dire je parle au help desk et fixe ce problème par exemple. Donc il faut bien que les rôles rentrent bien dans mon équipe ou iOS d'agent interopérabilité soit suffisamment générique pour que le help desk puisse aider aussi sur l'iPhone par exemple. S'il a pas accès en en en vision de l'écran sur l'iPhone, on pourrait projeter l'iPhone sur le Mac et comme il aurait accès au Mac, il verrait ce qu'il y a sur l'iPhone et donc pourrait au moins faire des recommandations.
**[1773483987782] MANUS:** **Vision claire. C'est exactement l'architecture Y-OS.**

Laisse-moi la structurer avant d'exécuter.

---

## Ce que tu décris : Y-OS Mac Agent

Un système en 3 couches :

| Couche | Rôle | Technologie |
|--------|------|-------------|
| **Perception** | Manus voit ton écran, lit les métriques système | SSH + screencapture + top/df/ps |
| **Cognition** | Manus comprend, diagnostique, décide | LLM + contexte Y-OS |
| **Action** | Manus exécute sur ton Mac | SSH → shell, AppleScript, osascript |

---

## Ce que ça permet concrètement

**Commandes naturelles → exécution autonome :**

> "Efface les apps non utilisées depuis 1 an qui font +1 Go"
→ Manus : SSH → `system_profiler SPApplicationsDataType` → filtre → `rm -rf` ciblé → rapport

> "Lance CleanMyMac et dis-moi ce qu'il trouve"
→ Manus : SSH → `open -a CleanMyMac` + screencapture → analyse visuelle → résumé

> "Regarde ce qui se passe sur mon écran, c'est bizarre"
→ Manus : SSH → `screencapture -x /tmp/screen.png` → upload → analyse ...
**[1773483966354] USER:** Donc on pourrait développer maintenant un module iOS qui soit  IT manager  et qui et contrôle et accès contrôle donc tous mes devices, disons en particulier le Mac. Et donc je pourrais lui demander de faire n'importe quoi sur mon Mac. Je pourrais lui dire d'effacer les les apps non utilisées depuis une année et qui prennent plus qu'1 Go, à d'aller effacer la poubelle ou de lancer CleanMyMac pour cleaner le Mac et de réorganiser mes fichiers selon ma carte mentale globale, de lancer un  backup de me donner des KPI et de construire un dashboard. Bref, j'ai j'ai une super couche qui me permet d'éviter d'installer  et je peux développer mes propres apps via manus au-dessus de mon de mon système.  pour la gestion, le monitoring, le mind mapping et cetera. Mais donc toute la gestion de mon Mac inclus le débugage pourrait être fait complètement et par manus. Je dirai à manus, regarde ce qui se passe sur mon écran, il y a des choses bizarres et il voit que il y a plus de mémoire, que le disque...
**[1773482869552] MANUS:** Les deux livrables sont prêts.

---

**1. Y-OS Control Panel** — dashboard live, design Terminal Cartographique

- 16 services modélisés (tunnels, APIs, AI, hardware, home, automation)
- Carte SVG des ponts avec lignes animées (flux actif = vert pulsant)
- Filtres par Layer (Y-OS / YOU / MAP) et par Type
- Panneau détail par service (endpoints, connexions entrantes/sortantes, tags)
- Auto-refresh toutes les 30s avec indicateur de latence
- Les services cloud (Manus, Claude, Gemini, Notion, GitHub) sont marqués online — les tunnels et services locaux restent `UNKNOWN` jusqu'à ce que tu colles les URLs ngrok

---

**2. Script ngrok full Mac** — 3 fichiers joints

| Fichier | Usage |
|---------|-------|
| `setup_ngrok_yos.sh` | Installation complète (une seule fois) |
| `yos_tunnels_status.sh` | Vérifier les tunnels actifs à tout moment |
| `README.md` | Instructions complètes |

**Setup en 3 commandes :**
```bash
chmod +x setup_ngrok_yos.sh
bash setup_ngrok_yos.sh
# → entre ton ngrok aut...
**[1773482828243] MANUS:** Dashboard opérationnel. Je finalise le checkpoint et je livre les deux livrables.
**[1773482605361] MANUS:** Design choisi : **Terminal Cartographique** — fond noir, monospace JetBrains Mono + Space Grotesk, grille asymétrique 3 colonnes, lignes SVG animées entre les nœuds actifs. Dense, opérationnel, pas de centrage générique. Je construis maintenant.
**[1773482488709] MANUS:** Lancé. Je travaille sur 1 et 2 en parallèle.
**[1773482484311] USER:** 1-2
Je vais fana token pdt ce temps
**[1773482176651] MANUS:** **Deux sujets distincts. Je les traite séparément.**

---

## 1. ngrok pour Y-OS — accès full Mac

Architecture recommandée :

```
Manus / Y-OS (cloud)
    ↓ HTTPS
ngrok TCP 22  →  SSH Mac  →  tout (fichiers, terminal, apps, Tana local, réseau)
ngrok HTTP 8262  →  Tana Local MCP  →  lecture + écriture workspace
ngrok HTTP 8123  →  Home Assistant  →  domotique
```

**Sécurisation minimale obligatoire :**
- ngrok authtoken (compte ngrok) → URLs stables et authentifiées
- SSH key-only (désactiver password auth)
- ngrok IP restrictions (whitelist IP sandbox Manus si fixe, sinon authtoken suffit)

Je peux te générer le script de setup complet pour ton Mac + la config ngrok permanente (launchd daemon = démarre au boot).

---

## 2. Visualisation des ponts / accès / outils Y-OS

**Le problème que tu décris :**
> "Je dois voir d'un coup d'œil : quels tunnels sont actifs, quelles apps sont connectées, quels agents tournent où, quels outils sont disponibles depuis quel contexte."

C'est un **Y-O...
**[1773482154132] USER:** Super ngrok pour yOS à distribuer 
Pour moi yOS (master version) contrôle le max de chose et fait TOuT pour moi: donc donner accès full

(Mais challenge je dois me souvenir et VISUALISER tous ces ponts accès api tools… carte mentale nécessaire pour moi… Tana? Mindmap? Custom a developper?? 
Vision interrelation et outils actifs ici et là devient critique epigram y retrouver (quelle app de scan pour veneraner un pla 3d navigable pour home automation qui tourne sur HA mais avec tunnel grok pour cela…)
**[1773482019431] MANUS:** **Non. Ngrok seul = tunnel très limité.**

---

## Ce que ngrok fait réellement

Ngrok expose **un port spécifique** sur internet. Si tu exposes `localhost:8262` (Tana Local API), j'accède uniquement à **Tana** — rien d'autre.

Ce n'est pas un accès Mac général. C'est un tuyau vers une seule application.

---

## Ce qu'il faut pour contrôler ton Mac depuis Manus

| Capacité | Outil | Principe |
|----------|-------|----------|
| **Fichiers** (lire, écrire, déplacer) | SSH + ngrok TCP | `ngrok tcp 22` → j'accède via SSH |
| **Terminal / commandes** | SSH | Même chose |
| **Interface graphique** | VNC + tunnel | Plus lourd |
| **Automatisation apps** | Playwright local + tunnel | Pour browser automation |
| **Tana uniquement** | ngrok http 8262 | Minimal, ciblé |

---

## Architecture propre pour Y-OS

Le vrai pattern pour ce que tu veux :

```
Manus (cloud)
    ↓ HTTPS
n8n sur NAS  ←→  Mac local (SSH, Tana, fichiers, Home Assistant...)
    ↓
Services locaux
```

**n8n sur NAS** = gateway...
**[1773482004886] USER:** Ngrok permettra à mais de contrôler mon Mac? Fichiers changer paramètres réparer problème etc
**[1773459084643] MANUS:** **Bonne question d'architecture. Réponse directe.**

---

## Pourquoi Claude Code / Gemini CLI peuvent accéder à localhost:8262

Ces outils tournent **sur ta machine locale** (macOS/Windows), pas dans un sandbox distant. Quand Tana Desktop expose `localhost:8262`, ces CLIs y accèdent directement car ils partagent le même réseau loopback.

Manus tourne dans un **sandbox cloud isolé** — réseau séparé, pas de tunnel vers ton localhost.

---

## Options pour piloter le Local MCP Tana depuis l'extérieur

| Option | Principe | Complexité | Faisable maintenant |
|--------|----------|------------|---------------------|
| **ngrok / Cloudflare Tunnel** | Expose `localhost:8262` sur une URL publique temporaire | Faible | ✅ Tu lances ngrok sur ton Mac, tu me donnes l'URL |
| **n8n local → webhook** | n8n sur ton NAS appelle Tana Local API, Manus appelle n8n | Moyenne | ✅ Si n8n tourne déjà |
| **Fly.io + proxy** | Déploie un proxy sur Fly qui relaie vers ton tunnel | Haute | ⚠️ Overkill |
| **Clau...
**[1773459069169] USER:** Accessible via Claude Code, Gemini CLI, Codex CLI — pas depuis mon sandbox (localhost isolé)

Vers 3 sont pas sandboxes?
Comment en général sorti de sandbox?
Piloter Claude via fly? Ou….?
**[1773458758675] MANUS:** **Problème identifié : token de type "personal", pas "workspace".**

Le token que tu as fourni est un **personal token** (JWT décodé : `"type":"personal"`). L'Input API exige un **workspace token** — différent.

**Comment générer le bon token (30 sec) :**

1. Ouvre **Tana**
2. Coin bas-gauche → **Settings** → **API Tokens**
3. Tu verras une liste de workspaces — sélectionne le tien
4. Clique **Create token** → **Copy**

Le token workspace ressemble à une chaîne courte (pas un JWT long), par exemple : `tana_XXXXXXXXXX`

Colle-le ici et je relance immédiatement.
**[1773458701911] MANUS:** Token reçu. Je lance l'import complet.
**[1773458689792] MANUS:** **Carte complète des APIs Tana — état mars 2026**

| API | Type | Accès | Lecture | Écriture | Condition |
|-----|------|-------|---------|----------|-----------|
| **Input API** | Cloud (REST) | Token API | ❌ | ✅ | Token workspace |
| **Local API / MCP** | Local (localhost:8262) | OAuth | ✅ | ✅ | Desktop app ouvert |

---

**Input API (cloud)**
- POST uniquement, pas de lecture
- Crée nodes, supertags, fields
- Nécessite un token API workspace
- La doc dit explicitement : *"APIs for reading from Tana Graphs are currently not available"*

**Local API / MCP (desktop)**
- Exposé sur `localhost:8262` quand Tana Desktop tourne
- **Lecture complète** : `search_nodes`, `read_node`, `get_children`, `list_tags`, `get_tag_schema`
- **Écriture complète** : `import_tana_paste`, `tag`, `set_field_content`, `create_tag`, `edit_node`...
- Nécessite : Tana Desktop + feature flag "Local API" activé dans Tana Labs
- Accessible via Claude Code, Gemini CLI, Codex CLI — **pas depuis mon sandbox** (localho...
**[1773458664856] MANUS:** Vérification de l'état actuel de l'API Tana — lecture + écriture.
**[1773458662406] USER:** Aussi api lecture?
**[1773458648530] MANUS:** **Situation claire.**

Tana a bien une **Input API** programmatique (POST JSON) — je peux créer tous les nodes, supertags et fields via code.

**Blocage unique : le token API.**

Pour que j'exécute l'import + le post-import complet en autonomie, j'ai besoin de ton **Tana API Token**.

**Comment le récupérer (30 secondes) :**

1. Ouvre Tana
2. Coin bas-gauche → **Settings** → **API Tokens**
3. Sélectionne ton workspace → **Create token**
4. **Copy** → colle-le ici

Une fois le token reçu, j'exécute tout en une passe :
- Création des supertags (`#layer`, `#domain`, `#system`, `#project`, `#task`, `#resource`, `#idea`, `#knowledge`, `#report`)
- Création des fields (`status`, `domain`, `system`, `project`, `resource_type`, `priority`, `purpose`, `role`, `description`, `topic`)
- Import de tous les nodes avec leurs champs et relations
- Page Galaxy Home structurée
**[1773458486183] MANUS:** Je vérifie ce qui est disponible via MCP pour interagir avec Tana.
**[1773458484004] USER:** Importe dans Tana?
 Fait Post-import
**[1773458331519] MANUS:** Fichier prêt.

**Import : Tana → Import → Markdown**

---

**Post-import — 4 étapes**

| # | Action | Détail |
|---|--------|--------|
| 1 | Convertir hashtags → Supertags | `#layer` `#domain` `#system` `#project` `#task` `#resource` `#idea` `#knowledge` `#report` |
| 2 | Convertir champs → Fields Tana | `status::` `domain::` `system::` `project::` `resource_type::` `priority::` |
| 3 | Créer 3 Search Views | `#task status=open` / `#project status=active` / `#resource resource_type=tool` |
| 4 | Page principale "Galaxy Home" | Afficher : Layers · Domains · Systems · Active projects · Open tasks |

---

**Structure importée**

- 3 Layers (Y-OS / YOU / MAP)
- 7 Domains
- 5 Systems
- 4 Projects
- 4 Tasks
- 4 Resources
- 2 Ideas
- 2 Knowledge nodes
- 1 Report template (Weekly Review)

---

**Suites disponibles**

1. Galaxy Map 2D visuelle (layout optimal, rendu réel)
2. Version Tana avancée (40–60 champs intelligents, relations croisées)
3. Connexion Y-OS + agents AI (routing, triggers, au...
**[1773458299342] MANUS:** Lu. Je lis le fichier et je prépare le proto Tana.
**[1773458292368] USER:** Tana proto

Créer pour moi



</details>