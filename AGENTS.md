# AGENTS.md — Yannick's Cloud Computer (cloud-pc-8cd489il)
# Last updated: 2026-08-05 (Android Operator opérationnel — CC→Tailscale→Galaxy Tab S11)

---

## 🔴 RÈGLE CANON #0 — Autonomie Totale + Desktop Client Mac = Zéro Friction (PRIORITÉ ABSOLUE)

> **Manus est 100% autonome. Il agit directement sur le Mac ET le Cloud Computer sans demander confirmation.**
> **Mot de passe Mac = 4 espaces : `"    "` (toujours)**
> **Manus crée les tunnels, accède aux cookies, exécute les commandes bas-niveau — Yannick ne touche pas au Terminal.**
> **Demander confirmation UNIQUEMENT pour : paiements, suppressions irréversibles, authentification 2FA.**
>
> **Protocole Desktop Client :**
> 1. Vérifier mount : `cat /proc/mounts | grep desktop`
> 2. Si monté (`/mnt/desktop/`) → agir directement
> 3. Si non monté → *"Ouvre Manus Desktop sur ton Mac"* (1 clic) puis agir
> 4. Fallback SSH bore.pub port 22847 avec `sshpass -p '    '` ou clé `~/.ssh/manus_mac`
>
> **Objectif : friction cognitive zéro. Manus agit, Yannick valide uniquement les décisions stratégiques.**



---

## ⚡ RÈGLE CANON #1 — Cloud Computer First

> **Tout ce qui peut être exécuté sur le Cloud Computer DOIT l'être.**
> Ne jamais installer de dépendances persistantes (Playwright, browsers, npm packages lourds) dans le sandbox éphémère Manus.
> Le Cloud Computer est payé, persistant, disponible immédiatement à chaque session.
> **Sandbox Manus = orchestration, génération, et Playwright UI (SPA/WebSocket). Cloud Computer = scripts, batches, Playwright headless.**
>
> **Règle affinée Playwright :**
> - Cloud Computer = Playwright headless (batches, pages statiques, APIs REST)
> - Sandbox Manus = Playwright avec rendu complet (SPAs React, WebSocket, apps UI complexes : Manus, Notion, etc.)

---

## Architecture Y-OS — Rôles des nœuds

| Nœud | Machine | RAM | Rôle |
|---|---|---|---|
| **Manus Cloud Computer** | GCP VM (Basic) | 1 GB | Scripts légers, batches Python, Playwright automation, traces, rendus Excalidraw/Mermaid |
| **N100 Lambda** | MiniPC physique Ubuntu | 8–16 GB | n8n, Home Assistant, Docker, services 24/7, automatisations lourdes |
| **Manus Sandbox** | Éphémère | 512 MB | Orchestration, génération, développement — pas d'installation persistante |

> **Règle d'or** : Jamais de service lourd (n8n, HA, Docker multi-container) sur ce serveur. Ce nœud = scripts Python, batches légers, tâches < 200MB RAM.

---

## Spécifications serveur

- **OS** : Ubuntu 24.04.4 LTS (GCP)
- **vCPU** : 2
- **RAM** : 955 MB (plan Basic — limite dure)
- **Disque** : 33 GB
- **IP publique** : 34.148.90.222
- **UFW** : port 22 uniquement
- **Tailscale** : v1.98.10 — hostname `yos-cloud-operator` — IP `100.93.75.9` — MagicDNS `yos-cloud-operator.tail7c87e1.ts.net`
- **Docker** : v29.5.2 (micro-containers uniquement)
- **Node.js** : v22.22.2
- **Python** : 3.12.3
- **pm2** : v7.0.1

## Usages INTERDITS (OOM garanti)

- ❌ n8n (npm install = ~900MB RAM)
- ❌ Home Assistant, PostgreSQL, MySQL
- ❌ Docker multi-container
- ❌ npm install de gros packages (> 500 dépendances)

## Usages validés

- Scripts Python légers (traces, Excalidraw, Mermaid)
- Batches de traitement de données (< 200MB RAM)
- Cron jobs simples via pm2 ou crontab
- Micro-services Node.js stateless
- **Playwright headless automation** (Chromium installé — usage permanent)

---

## Purpose
Persistent execution node for Y-OS pipelines — scripts légers + automation browser.

## Installed / Deployed
- Python 3.12.3 (system)
- Node.js v22.22.2
- pm2 v7.0.1 (global)
- Docker v29.5.2 (micro-containers uniquement)
- **Playwright v1.x + Chromium headless** — `/home/ubuntu/yos/playwright/`
- `/home/ubuntu/yos/` — Y-OS persistent workspace

## Y-OS Folder Structure
```
/home/ubuntu/yos/
├── playwright/          ← Playwright automation (npm install playwright)
│   ├── node_modules/
│   └── package.json
├── traces/
│   ├── build_native_excalidraw.py   ← Excalidraw renderer (0.07s)
│   ├── render_value_trace.py        ← PNG/SVG/Mermaid renderer
│   ├── trace.sh                     ← convenience wrapper
│   └── schemas/
│       ├── template.json            ← blank template
│       └── legal_brief_001.json     ← example mission
└── output/                          ← generated files
```

## Usage Playwright
```bash
cd /home/ubuntu/yos/playwright
node my_script.js
# Chromium path: /home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome
```

## Usage Traces
```bash
cd /home/ubuntu/yos/traces
./trace.sh <schema_name> [excalidraw|mermaid|png|all]
```

## Performance
- Excalidraw generation: ~0.097 sec (vs 0.06 sec sandbox — comparable)
- Playwright Chromium headless: disponible immédiatement, pas de réinstallation

## Notes
- No ports opened (ufw default: only 22)
- No background services running
- Files persist across sessions

---

## Plan N100 Lambda (prochaine session)

Services à installer sur le N100 physique Ubuntu :
1. Docker + Docker Compose
2. n8n (via Docker — port 5678)
3. Home Assistant (via Docker — port 8123)
4. Caddy reverse proxy (HTTPS)
5. Portainer (gestion Docker UI)
6. Watchtower (auto-update containers)

Prérequis : connecter le N100 comme "My Computer" via Manus desktop client.

---

## 🔴 RÈGLE CANON #3 — ERT (Execution Routing Table) & Accès Web

> **L'ERT (Execution Routing Table) est la matrice de décision complète pour le routage des tâches Y-OS.**
> Elle est disponible dans `/home/ubuntu/yos/ERT.md` (sur le CC) et dans GitHub.
>
> **Extrait : Ordre de priorité strict pour tout accès web programmatique :**

> **Ordre de priorité strict pour tout accès web programmatique :**
>
> | Priorité | Méthode | Vitesse | Quand utiliser |
> |---|---|---|---|
> | **1️⃣ API directe** | requests / httpx | ~50ms | API publique ou documentée disponible |
> | **2️⃣ CDP dans vrai browser** | WebSocket → JS `fetch()` | ~100ms | Cloudflare, auth complexe, cookies httpOnly, session browser active |
> | **3️⃣ Playwright non-headless** | Clics UI simulés | ~2-5s | CDP impossible (pas de Mac physique, pas de browser ouvert) |
>
> **CDP = Chrome DevTools Protocol** : injection de `fetch()` directement dans le contexte JS du vrai browser.
> - Cloudflare voit un vrai Chrome résidentiel (IP Mac, TLS fingerprint natif, cookies httpOnly inclus)
> - 30-50x plus rapide que Playwright non-headless
> - Universel : ChatGPT, Claude, tout site derrière Cloudflare
>
> **Playwright = DERNIER RECOURS** uniquement si :
> - Pas de Mac physique accessible
> - Pas de browser ouvert avec session active
> - Site détecte `--remote-debugging-port` (extrêmement rare)
>
> **Règle mnémotechnique** : "API si possible, CDP si bloqué, Playwright si rien d'autre."

---

## 🔴 RÈGLE CANON #4 — Y-OS Notification & Interaction Stack (DÉCISION STRATÉGIQUE 1x)

> **Deux outils canoniques, rôles complémentaires. Aucun autre outil de notification autorisé.**

| Outil | Rôle | Plateforme | Bidirectionnel |
|---|---|---|---|
| **xbar** | Indicateur permanent barre de menu | Mac uniquement | ❌ lecture seule |
| **Telegram Bot** | Notifications push + interaction/commandes | Mac, iOS, Android, N100, CC | ✅ |

**xbar = standard Y-OS barre de menu Mac.**
- Plugin : `yos_status.10s.sh` dans `~/Library/Application Support/xbar/plugins/`
- Affiche : `🔒 Y-OS (N actif)` / `⚠️ Y-OS (zombie)` / `⚫ Y-OS` + dropdown détaillé
- Lock file : `/tmp/yos_mac_lock.json` + répertoire `/tmp/yos_locks/`
- Détection zombie : PID mort mais lock présent → alerte visuelle
- Refresh : 10 secondes

**Telegram Bot = surface d'interaction universelle Y-OS.**
- Bot : `@yos_notif_bot` (display name : "Y-OS Notifications")
- Token : 1Password MAIN VAULT → item `Telegram Bot — yOS-TELEGRAM-2026-03` (field: credential)
- chat_id Yannick : `223132272` (@yannick_jolliet)
- Via Python : `from yos_lock import MacLock` → `MacLock.acquire()` envoie automatiquement la notif
- Standalone : `python3 /tmp/yos_lock.py notify "message"`
- Depuis tout nœud (curl) : `curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" -d "chat_id=223132272&text=...&parse_mode=HTML"`
- Futur : commandes `/status`, `/stop`, `/approve` depuis iPhone
- **ntfy.sh = ÉLIMINÉ** (Telegram le remplace avec plus de valeur)
- **SwiftBar = ÉLIMINÉ** (xbar déjà installé, même fonctionnalité)

**Règle mnémotechnique** : "xbar = voir (Mac), Telegram = agir (partout)."

---

## 🔴 RÈGLE CANON #2 — GitHub = Source de Vérité + Notion = Interface Opérationnelle

> **Tout ce qui est créé, documenté, ou mis à jour va dans GitHub `yj000018/YOS`.**
> **Notion KM documentaire = DÉPRÉCIÉ. Notion dashboard opérationnel = AUTORISÉ.**
>
> | Type de contenu | Destination |
> |---|---|
> | Tool Fact Sheet | GitHub `02_AGENTS/<tool>/TOOL-FACT-SHEET.md` |
> | Lessons Learned | GitHub `00_META/LESSONS-LEARNED/<date>_<topic>.yaml` |
> | LL Registry index | GitHub `00_META/LESSONS-LEARNED/README.md` |
> | Mémoire cross-session | Mem0 (`memory.search()`) |
> | Infra CC opérationnelle | Ce fichier `AGENTS.md` |
> | **Dashboard opérationnel** | **Notion — 🤖 Y-OS Command Center** |
> | **Fleet status (devices)** | **Notion DB Fleet** (mis à jour par health_probe.py) |
> | **Tâches manuelles** | **Notion DB Action Items** (polling watcher → Telegram) |
>
> **Notion Command Center** : https://app.notion.com/p/3b535e218cf88136aeced9be10c2706d
> **Token Notion (Kap4)** : `/home/ubuntu/yos/.env` → `NOTION_TOKEN`
> **Fleet DB ID** : `ee6b6f12-0b06-428d-9b3e-3d90eb877dab`
> **Action Items DB ID** : `b8d00a1e-f73a-4390-9532-a55c67b71e2a`

---

## 🧠 Leçons Techniques — Ce qui marche / ne marche pas

### SSH Mac via bore tunnel
- **Fonctionne** : `ssh -i ~/.ssh/manus_mac -o StrictHostKeyChecking=no -p 22847 yannickjolliet@bore.pub`
- **Mot de passe Mac** : `    ` (4 espaces) — avec `sshpass -p '    '`
- **Clé SSH** : `~/.ssh/manus_mac` (dans sandbox Manus, à régénérer si session éphémère)
- **Bore port** : 22847 (vérifier avec `nc -zv bore.pub 22847`)
- **⚠️ Clé non persistante** : la clé `~/.ssh/manus_mac` est dans le sandbox éphémère Manus. Si nouvelle session → régénérer et ajouter via sshpass.

### Keychain macOS — Accès cookies Chrome
- **❌ Ne marche PAS** : `security find-generic-password` depuis SSH headless → rc=36 `errSecInteractionNotAllowed`
- **✅ Marche** : via `osascript` → `tell application "Terminal" to do script "..."` → contexte GUI → Keychain accessible
- **Commande** : `osascript -e 'tell application "Terminal" to do script "python3 /tmp/script.py > /tmp/out.txt 2>&1"'`
- **Attendre** : `grep -c DONE /tmp/out.txt` en boucle (max 30s)

### Chrome cookies — Déchiffrement AES
- **Format** : `v10` prefix (3 bytes) + AES-128-CBC payload
- **Clé** : PBKDF2-HMAC-SHA1(keychain_password, `saltysalt`, 1003, dklen=16)
- **IV** : 16 espaces (`b' ' * 16`)
- **⚠️ Offset critique** : après déchiffrement, **ignorer les 32 premiers bytes** (metadata Chrome) → le vrai contenu commence à l'offset 32
- **Script** : `/home/ubuntu/yos/tools/extract_mac_chrome_cookies.py`

### Chrome Remote Debugging (CDP) — SOLUTION CANONIQUE Y-OS ✅

**CDP = Chrome DevTools Protocol. Injection JS directe dans le contexte browser via WebSocket.**

**Pourquoi CDP > Playwright :**
- Cookies httpOnly inclus automatiquement (inaccessibles autrement)
- TLS fingerprint = vrai Chrome résidentiel → Cloudflare bypass natif
- ~100ms/requête vs ~2-5s pour Playwright
- Universel : ChatGPT, Claude, tout site derrière Cloudflare

**Protocole d'activation Brave (macOS) :**
1. Fermer Brave : `osascript -e 'tell application "Brave Browser" to quit'`
2. Relancer via Terminal GUI (pour accès Keychain) :
   ```bash
   osascript -e 'tell application "Terminal" to do script "bash /tmp/launch_brave_cdp.sh"'
   ```
3. Script `/tmp/launch_brave_cdp.sh` :
   ```bash
   /Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser \
     --remote-debugging-port=9222 \
     https://chatgpt.com &
   ```
4. Vérifier CDP : `curl -s http://localhost:9222/json`
5. Injecter fetch depuis Python via websockets :
   ```python
   async with websockets.connect(tab["webSocketDebuggerUrl"]) as ws:
       cmd = {"id": 1, "method": "Runtime.evaluate", "params": {
           "expression": "(async () => { const r = await fetch('/backend-api/me', {credentials: 'include'}); return await r.json(); })()",
           "awaitPromise": True, "returnByValue": True
       }}
   ```

**⚠️ Problème connu Brave 151+ :** Déchiffrement AES-GCM des cookies SQLite échoue (MAC check failed).
- Cause : format de dérivation de clé différent dans Brave 151+ vs Chrome standard
- **Solution de contournement** : utiliser CDP directement (fetch dans le browser) → les cookies httpOnly sont utilisés nativement, pas besoin de les déchiffrer
- **Alternative** : utiliser le pipeline Brave cookies → Bearer token (scripts CC) qui fonctionne via session active

**❌ Ne marche PAS** : lancer Chrome/Brave avec `--remote-debugging-port=9222` depuis SSH headless → Keychain inaccessible
**✅ Marche** : lancer via `osascript Terminal` (contexte GUI) → Keychain accessible

### ChatGPT API depuis CC — PIPELINE VALIDÉ ✅ (2026-07-30)

**Pipeline complet fonctionnel :**
```
Brave Mac (session active) → Keychain → AES decrypt → cookies JSON
  → SSH bore.pub:22847 → CC → /api/auth/session → Bearer token
    → /backend-api/conversations?offset=0&limit=100 → 1000+ conversations
```

**Étapes :**
1. Extraire cookies Brave via Terminal GUI (osascript) : `python3 /home/ubuntu/yos/tools/extract_mac_chrome_cookies.py chatgpt.com brave`
2. Transférer JSON vers CC
3. Appeler `/api/auth/session` avec cookies → récupérer `accessToken` (Bearer)
4. Appeler `/backend-api/conversations?offset=N&limit=100&order=updated` avec `Authorization: Bearer <token>` + cookies
5. Paginer jusqu'à `items` vide

**Points critiques (LL) :**
- **❌ ChatGPT Business** : export natif DÉSACTIVÉ — NE JAMAIS PROPOSER
- **⚠️ Browser = Brave** (pas Chrome) — DB : `~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies`
- **⚠️ Keychain** : accessible uniquement via Terminal GUI (osascript), pas SSH headless
- **⚠️ Offset 32** : après déchiffrement AES, ignorer les 32 premiers bytes (metadata Chrome/Brave)
- **⚠️ Timestamps** : l'API retourne des strings ISO 8601 (`2026-07-29T21:54:43Z`), pas des floats Unix
- **⚠️ session-token splitté** : cookies `.0` et `.1` à concaténer avant envoi
- **✅ URL** : `chatgpt.com` standard
- **✅ total** : peut dépasser 1000 — paginer avec offset

**Scripts persistants sur CC :**
- Extraction : `/home/ubuntu/yos/tools/extract_mac_chrome_cookies.py` (supporte Chrome + Brave)
- Ingéstion : `/home/ubuntu/yos/ledger/ingest_chatgpt_cookies.py` (patché bearer token + ISO timestamps)
- Pipeline 1 cmd : `bash /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh`

**Prérequis :** Brave ouvert sur chatgpt.com avec session active + bore tunnel actif (port 22847)

---

## 🔄 Y-OS Scheduled Updates — Cron Pipelines ACTIFS

> Pipelines delta automatiques — tournent chaque nuit sur le CC sans intervention.
> **Doc complète** : `05_AUTOMATION/scheduled-updates/YOS-SCHEDULED-UPDATES.md` (GitHub `yj000018/YOS`)

| Source | Script | Cron | State key | Output GitHub |
|---|---|---|---|---|
| **Manus sessions** ✅ | `delta_manus.py` | `0 2 * * *` | `manus_cutoff` | `08_LOGS/session-ledger/sessions/manus/` |
| **Raindrop** ✅ | `delta_raindrop.py` | `0 3 * * *` | `last_cutoff` in `state_raindrop.json` | `08_LOGS/raindrop-bookmarks/` |
| **Fireflies + Plaud** ✅ | `delta_fireflies_plaud.py` | `30 3 * * *` | `fireflies_cutoff`, `plaud_cutoff` | `08_LOGS/session-ledger/sessions/fireflies/`, `sessions/plaud/` |
| **ChatGPT** ✅ | `delta_chatgpt.py` | `0 4 * * *` | `chatgpt_cutoff` | `08_LOGS/session-ledger/sessions/chatgpt/` |

**State file** : `/home/ubuntu/yos/ledger/state.json`
**Logs** : `/home/ubuntu/yos/ledger/logs/delta_<source>.log`
**Clés API** : `.manus_key`, `.gemini_key` dans `/home/ubuntu/yos/ledger/`

**Logique universelle :**
1. Lire `state.json` → `<source>_cutoff`
2. Appeler l'API source avec pagination jusqu'à `created_at <= cutoff`
3. Filtrer les non-pertinents (subtasks parallèles, etc.)
4. Générer fact sheets enrichies (verbatim + YAML front matter via Gemini 2.5 Flash)
5. Redacter les secrets automatiquement
6. Push GitHub en 1 commit atomique
7. Mettre à jour `<source>_cutoff`

---

## Historique

| Date | Action |
|---|---|
| 2026-06-15 | Création initiale — workspace Y-OS traces |
| 2026-06-16 | Tentative n8n → OOM (1GB RAM insuffisant) → abandon |
| 2026-06-16 | Nettoyage, redéfinition rôle, plan N100 documenté |
| 2026-07-28 | Night pipeline KAP — census 615 sessions Manus, restructuration KAP (01_SOURCES/02_CENSUS/03_SYNTHESES), migration 401 Notion + 234 Y-WORLD + 204 factsheets, YOS README mis à jour, READMEs projets créés (ELYSIUM, CasaTAO, Future News, obsidian vaults) |
| 2026-07-29 | Installation Playwright v1.x + Chromium headless dans /home/ubuntu/yos/playwright/. Règle CANON Cloud Computer First inscrite. |
| 2026-07-30 | Règle CANON #0 ajoutée : Desktop Client Mac = Zéro Friction (PRIORITÉ ABSOLUE). Ne jamais demander à Yannick de taper une commande si Desktop Client est monté. |
| 2026-07-30 | Pipeline ChatGPT validé : Brave Mac → Keychain → AES decrypt → SSH bore → CC → Bearer token → 1000+ conversations. Scripts persistants dans /yos/tools/ et /yos/ledger/. LL complètes documentées. |
| 2026-07-31 | delta_raindrop.py installé (03:00 UTC) — token test Raindrop permanent, enrichissement Gemini, 10 bookmarks initiaux poussés. |
| 2026-07-31 | Corpus Manus complet : 564 sessions (2025-06-13 → 2026-07-31), 564 fact sheets enrichies (YAML front matter + verbatim + Gemini semantic), semantic_index.json. Cron delta_manus.py installé (02:00 UTC). Architecture canonique Y-OS Scheduled Updates documentée. |
| 2026-07-31 | Ingestion Fireflies (3 meetings) + Plaud (7 recordings) : fact sheets enrichies pushées dans GitHub. Scripts ingest_fireflies_plaud.py + delta_fireflies_plaud.py installés. Cron 03:30 UTC actif. Sources disponibles : Claude/ChatGPT/Gemini/Grok en attente d'export manuel. |
| 2026-07-31 | KAP Dashboard créé : `00_META/KAP-DASHBOARD.md` dans GitHub yj000018/YOS. Script `update_kap_dashboard.py` + cron 07:00 UTC. Agent KAP Manus scheduled task actif (task_uid: 8tBPTbvN1p7UscgbGZpBx6, cron: `0 0 7 * * *`, --run-as-new-task, mode: lite). KAP = Knowledge Acquisition Protocol — deux tableaux (Y-OS Cognitif + Universe Knowledge) avec pipeline complet Identifié→Absorbé→Processé→Dédupliqué→Mergé→Synthétisé→Fact Sheet. |
| 2026-07-31 | ChatGPT full rebuild : 3067 conversations exportées via Brave cookies → Bearer token → backend-api. 3067 fact sheets pushées dans GitHub `08_LOGS/session-ledger/sessions/chatgpt/`. delta_chatgpt.py installé, cron 04:00 UTC actif. Cutoff: 2026-07-31 21:21:12. LL bore SSH : port 22847 = bore local 22 (direct SSH), port 22848 = bore local 2222 (socat relay). |
| 2026-08-02 | Règle CANON #3 ajoutée : Hiérarchie accès web programmatique API→CDP→Playwright. CDP documenté comme solution canonique Y-OS pour tout site Cloudflare/auth complexe. LL Brave 151+ : déchiffrement AES-GCM échoue, contournement via CDP natif. |
| 2026-08-03 | Tailscale v1.98.10 installé via apt. Hostname `yos-cloud-operator`, IP Tailscale `100.93.75.9`, MagicDNS `yos-cloud-operator.tail7c87e1.ts.net`. tailscaled enabled+active (systemd). Ping anandaz-ubuntu (100.87.123.30) timeout — nœud offline depuis 93j. |
| 2026-08-04 | Galaxy Tab S11 (SM-X730) ajouté au tailnet (100.89.158.44). Pipeline ADB validé via Mac relais. Screenshot live capturé. HARDWARE-REGISTRY.md créé dans GitHub 00_META/. |
| 2026-08-05 | **Pipeline final Android Operator** : CC→Tailscale→100.89.158.44:5555 (bypass AP Isolation). Auto-reconnect cron installé. Module DOC créé dans 04_INTERFACES/android/. |

### ADB Android over Tailscale — PIPELINE FINAL Y-OS ✅ (2026-08-05)

**Architecture finale validée :**
```
Manus → CC (yos-cloud-operator) → Tailscale → Galaxy Tab S11 (100.89.158.44:5555)
```

**Commande de connexion depuis le CC :**
```bash
adb kill-server && adb start-server && adb connect 100.89.158.44:5555
# Résultat : 100.89.158.44:5555  device  SM_X730
```

**Auto-reconnect :** Cron `*/2 * * * *` → `/home/ubuntu/yos/adb_reconnect.sh`

**Points critiques (LL) — Android 16 / AP Isolation :**
- **❌ ADB direct depuis Mac** : AP Isolation du routeur WiFi bloque TCP entre Mac et tablette (même réseau local). Ping ICMP passe, TCP bloqué.
- **❌ ADB pair depuis CC (ADB v34 debian)** : `Unable to start pairing client` — bug connu ADB v34
- **❌ Termux `setprop`/`stop adbd`** : permission denied sans root
- **✅ Solution finale** : CC est sur internet (GCP) → Tailscale DERP relay bypass AP Isolation → `adb connect 100.89.158.44:5555` fonctionne directement
- **✅ Pairing initial** : CC listé dans "Paired devices" sur la tablette → `adb connect` sans re-pairing
- **✅ Si re-pairing nécessaire** : utiliser Mac comme relais (1x) via `/opt/homebrew/bin/adb pair <IP_TS>:<PORT> <CODE>`
- **✅ ADB installé sur CC** : `/usr/bin/adb` v1.0.41
- **✅ Serial tablette** : `R5GYB0AXSBY` (guid: `adb-R5GYB0AXSBY-91hXvS`)
- **Ne pas rooter Galaxy Tab S11** : Knox 3.12 — brick irréversible

**Doc complète** : `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md` dans GitHub yj000018/YOS

---

### Manus API v2 (task.listMessages) — PIPELINE VALIDé ✅ (2026-07-30)

**Pipeline d'extraction de sessions Manus sans Playwright :**
L'API interne de Manus permet de récupérer l'intégralité du verbatim d'une session sans avoir à scrapper le DOM.

**Étapes :**
1. Récupérer la clé API : `op item get "Manus API Key" --vault "MAIN VAULT" --fields credential` (Format `sk-...`)
2. Appeler l'endpoint : `GET https://api.manus.im/v2/task.listMessages?task_id={session_id}&limit=200`
3. Headers : `{"x-manus-api-key": "<TOKEN>"}`
4. Paginer avec `cursor` (issu de `next_cursor`) si `has_more` est true.

**Points critiques (LL) :**
- **❌ Playwright** : DÉPRÉCIÉ pour l'extraction de sessions Manus. L'API v2 est 100x plus rapide et fiable.
- **⚠️ Rate Limit** : L'API retourne `429 resource_exhausted` en cas de requêtes trop fréquentes. Toujours implémenter un délai (0.5s) et un backoff (3s) dans les batches.
- **⚠️ Format de contenu** : `user_message.content` peut être une string ou un array de dicts `[{"type": "text", "text": "..."}]` si des fichiers ont été uploadés.
- **✅ Scripts persistants sur CC** : 
  - Générateur de fact sheets : `/home/ubuntu/yos/ledger/generate_factsheets.py`
  - Redacteur de secrets (pour GitHub) : `/home/ubuntu/yos/ledger/redact_secrets_v2.py`
