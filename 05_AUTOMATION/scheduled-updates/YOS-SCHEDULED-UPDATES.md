# Y-OS Scheduled Updates — Architecture Canonique
> Last updated: 2026-07-31 | Status: ACTIVE

## Principe

Chaque source de données Y-OS (Manus, Raindrop, ChatGPT, Notion, etc.) dispose d'un **pipeline delta** qui tourne automatiquement sur le Cloud Computer (cron) et maintient le corpus GitHub `yj000018/YOS` à jour sans intervention humaine.

**Architecture universelle :**
```
Source API → delta_<source>.py → fact sheets enrichies (MD + YAML) → GitHub main
                ↑
           state.json (cutoff date par source)
```

---

## Sources actives

### 1. Manus Sessions ✅ ACTIF

| Paramètre | Valeur |
|---|---|
| Script | `/home/ubuntu/yos/ledger/delta_manus.py` |
| Cron | `0 2 * * *` (02:00 UTC chaque nuit) |
| State | `/home/ubuntu/yos/ledger/state.json` → `manus_cutoff` |
| Output | `08_LOGS/session-ledger/sessions/manus/{task_id}.md` |
| API | `GET https://api.manus.im/v2/task.list` + `task.listMessages` |
| Auth | `x-manus-api-key: sk-...` (fichier `/home/ubuntu/yos/ledger/.manus_key`) |
| Enrichissement | Gemini 2.5 Flash → importance, projects, tags, summary |
| Redaction | Secrets auto-redactés avant push GitHub |
| Corpus initial | 564 sessions (2025-06-13 → 2026-07-31) |

**Logique delta :**
1. Lire `state.json` → `manus_cutoff`
2. Appeler `task.list` avec pagination jusqu'à `created_at <= cutoff`
3. Filtrer les subtasks parallèles (patterns : "wide research subtask", "parallel subtask", etc.)
4. Pour chaque nouvelle session : `task.listMessages` → verbatim → Gemini → fact sheet enrichie
5. Push GitHub en 1 commit atomique
6. Mettre à jour `manus_cutoff` → date de la session la plus récente traitée

**Points critiques :**
- Rate limit `429` → backoff 5s × 3 tentatives
- `content` peut être string ou array `[{"type":"text","text":"..."}]`
- Toujours redacter avant push (patterns : `sk-`, `ghp_`, `AIza`, `re_`, `r8_`, `ops_`)

---

### 2. Raindrop Bookmarks 🔲 À IMPLÉMENTER

| Paramètre | Valeur |
|---|---|
| Script | `/home/ubuntu/yos/ledger/delta_raindrop.py` (à créer) |
| Cron | `0 3 * * *` (03:00 UTC chaque nuit) |
| State | `/home/ubuntu/yos/ledger/state.json` → `raindrop_cutoff` |
| Output | `01_SOURCES/raindrop/{bookmark_id}.md` |
| API | `GET https://api.raindrop.io/rest/v1/raindrops/0?sort=-created&perpage=50&page=0` |
| Auth | `Authorization: Bearer <token>` (MCP Raindrop ou 1Password) |
| Enrichissement | Gemini → tags, category, summary |
| Corpus initial | À faire (bulk import first) |

**Logique delta :**
1. Lire `raindrop_cutoff` depuis `state.json`
2. Appeler l'API Raindrop triée par `created DESC`
3. Paginer jusqu'à `created <= cutoff`
4. Pour chaque nouveau bookmark : générer fact sheet MD avec titre, URL, tags, excerpt, summary Gemini
5. Push GitHub + update cutoff

---

### 3. ChatGPT Conversations 🔲 À IMPLÉMENTER

| Paramètre | Valeur |
|---|---|
| Script | `/home/ubuntu/yos/ledger/delta_chatgpt.py` (à créer) |
| Cron | `0 4 * * *` (04:00 UTC chaque nuit) |
| State | `/home/ubuntu/yos/ledger/state.json` → `chatgpt_cutoff` |
| Output | `08_LOGS/session-ledger/sessions/chatgpt/{conv_id}.md` |
| API | `/backend-api/conversations?offset=N&limit=100&order=updated` |
| Auth | Bearer token via cookies Brave (voir pipeline ChatGPT dans AGENTS.md) |
| Prérequis | Brave ouvert sur chatgpt.com + bore tunnel actif |
| Corpus initial | 1000+ conversations (pipeline validé 2026-07-30) |

**⚠️ Contrainte** : nécessite cookies Brave frais → pipeline semi-automatique (refresh cookies via osascript Mac).

---

### 4. Notion Pages 🔲 DÉPRÉCIÉ

> **Notion est mort** (RÈGLE CANON #2). Ne pas implémenter de pipeline delta Notion.
> Migration one-shot déjà faite (401 pages → GitHub, 2026-07-28).

---

### 5. GitHub Activity 🔲 OPTIONNEL

| Paramètre | Valeur |
|---|---|
| Script | `/home/ubuntu/yos/ledger/delta_github.py` (à créer) |
| Cron | `0 5 * * *` |
| API | `GET https://api.github.com/users/yj000018/events` |
| Output | `08_LOGS/github-activity/{date}.md` |

---

## State.json — Format canonique

```json
{
  "manus_cutoff": "2026-07-31T00:00:00Z",
  "raindrop_cutoff": null,
  "chatgpt_cutoff": null,
  "last_run_manus": "2026-07-31T02:00:00Z",
  "last_run_raindrop": null,
  "last_run_chatgpt": null,
  "total_manus": 564,
  "total_raindrop": 0,
  "total_chatgpt": 0
}
```

---

## Crontab actuel (CC)

```bash
# Y-OS Delta Pipelines
0 2 * * * python3 /home/ubuntu/yos/ledger/delta_manus.py >> /home/ubuntu/yos/ledger/logs/delta_manus.log 2>&1
# 0 3 * * * python3 /home/ubuntu/yos/ledger/delta_raindrop.py >> /home/ubuntu/yos/ledger/logs/delta_raindrop.log 2>&1
# 0 4 * * * python3 /home/ubuntu/yos/ledger/delta_chatgpt.py >> /home/ubuntu/yos/ledger/logs/delta_chatgpt.log 2>&1
```

---

## Clés API — Fichiers sur CC

| Source | Fichier | Format |
|---|---|---|
| Manus | `/home/ubuntu/yos/ledger/.manus_key` | `sk-...` |
| Gemini | `/home/ubuntu/yos/ledger/.gemini_key` | `AIza...` |
| GitHub PAT | `/home/ubuntu/yos/ledger/.github_pat` | `ghp_...` |
| Raindrop | `/home/ubuntu/yos/ledger/.raindrop_token` | À créer |

> **Source de vérité** : 1Password MAIN VAULT. Les fichiers `.key` sur CC sont des caches locaux.

---

## Notification Layer 🔲 PARQUÉ

> **Projet parqué** — À activer dans une session dédiée.
>
> Concept : quand un pipeline delta termine, envoyer une notification multi-canal :
> - Email via Resend (`re_...` dans secrets Manus)
> - Telegram bot (déjà en place dans Y-OS)
> - Push notification (ntfy.sh ou Pushover)
> - GitHub Action → webhook → fanout
>
> Architecture cible : fin de script → `notify.py` → fanout (email + Telegram + push).
> Mini-chaînes sans LLM pour les notifications simples.

---

## Logs

| Date | Action |
|---|---|
| 2026-07-31 | Pipeline delta_manus.py créé + cron installé. Corpus initial : 564 sessions. |
| 2026-07-31 | Architecture canonique documentée pour Raindrop, ChatGPT, GitHub. |
