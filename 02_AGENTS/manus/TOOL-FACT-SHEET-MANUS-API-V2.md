# TOOL FACT SHEET — Manus API v2
**Version**: 1.0 | **Date**: 2026-07-31 | **Status**: VALIDATED ✅

---

## 1. IDENTITÉ

| Champ | Valeur |
|---|---|
| Nom | Manus API v2 |
| Base URL | `https://api.manus.im/v2` |
| Auth | Header `x-manus-api-key: {KEY}` |
| Clé | 1Password MAIN VAULT → "MANUS API KEY" (item: `d6e3ql7p3ydacesxxj7ym7kelq`) |
| Clé prefix | `sk-Lwjt1ISkT1C73fY9EuIk42wa0JKbrySv` |
| Scope | Lecture des sessions Manus (task list + messages) |

---

## 2. ENDPOINTS VALIDÉS

### 2.1 Lister toutes les sessions

```
GET https://api.manus.im/v2/task.list
Headers: x-manus-api-key: {KEY}
Params:
  - limit: int (max ~100 par page)
  - cursor: string (pagination, depuis le champ "next_cursor" de la réponse)
```

**Réponse** :
```json
{
  "data": [
    {
      "id": "fxLA8xhwk4tHTwqM...",
      "title": "Titre de la session",
      "created_at": "2026-07-29T00:48:16.454Z",
      "updated_at": "2026-07-29T01:23:45.000Z",
      "status": "completed"
    }
  ],
  "next_cursor": "abc123...",
  "has_more": true
}
```

**Notes** :
- Total réel : **2521 tasks** (dont 1957 subtasks parallèles "Wide Research Subtask")
- Sessions nommées réelles : **564** (filtrer les titres != "Wide Research Subtask")
- Pagination obligatoire pour récupérer tout le corpus

### 2.2 Récupérer le verbatim d'une session

```
GET https://api.manus.im/v2/task.listMessages
Headers: x-manus-api-key: {KEY}
Params:
  - task_id: string (ID de la session)
  - limit: int (max 200 par page)
  - cursor: string (pagination)
```

**Réponse** :
```json
{
  "data": [
    {
      "id": "msg_xxx",
      "role": "user" | "assistant",
      "content": "texte du message",
      "created_at": "2026-07-29T00:48:16.454Z"
    }
  ],
  "next_cursor": "...",
  "has_more": false
}
```

---

## 3. SCRIPT DE RÉFÉRENCE — Récupération complète

```python
import json, time, urllib.request

MANUS_API_KEY = "sk-Lwjt1ISkT1C73fY9EuIk42wa0JKbrySv"  # Depuis 1Password

def manus_get(endpoint, params):
    """Call Manus API v2."""
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"https://api.manus.im/v2/{endpoint}?{qs}"
    req = urllib.request.Request(url, headers={"x-manus-api-key": MANUS_API_KEY})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

# Lister toutes les sessions (pagination complète)
def list_all_sessions():
    sessions = []
    cursor = None
    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor
        data = manus_get("task.list", params)
        sessions.extend(data["data"])
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
        time.sleep(0.2)
    return sessions

# Récupérer le verbatim d'une session
def get_session_messages(task_id):
    messages = []
    cursor = None
    while True:
        params = {"task_id": task_id, "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = manus_get("task.listMessages", params)
        messages.extend(data["data"])
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
        time.sleep(0.1)
    return messages
```

---

## 4. CORPUS MANUS (état au 2026-07-31)

| Métrique | Valeur |
|---|---|
| Total API tasks | 2 521 |
| Subtasks parallèles (exclus) | 1 957 |
| **Sessions nommées réelles** | **564** |
| Date la plus ancienne | 2025-06-13 |
| Date la plus récente | 2026-07-31 |
| Fact sheets GitHub | `yj000018/YOS` → `08_LOGS/session-ledger/sessions/manus/` |
| Ledger JSON (CC) | `/home/ubuntu/yos/ledger/master_ledger_manus.json` |
| API full list (CC) | `/home/ubuntu/yos/ledger/api_task_list_full.json` |
| Index sémantique (CC) | `/home/ubuntu/yos/ledger/semantic/semantic_index.json` |

---

## 5. RÈGLES D'UTILISATION

- **Ne jamais utiliser Playwright** pour accéder aux sessions Manus — l'API v2 est 100x plus rapide
- **Rate limiting** : attendre 0.2s entre les appels task.list, 0.1s entre les task.listMessages
- **Filtrage subtasks** : exclure les sessions dont le titre contient "Wide Research Subtask" ou "Parallel"
- **Clé API** : récupérer depuis 1Password MAIN VAULT, ne jamais hardcoder
- **Secrets dans les fact sheets** : toujours redacter avant push GitHub (script: `redact_secrets_v2.py`)

---

## 6. LOCALISATION DES RESSOURCES

| Ressource | Chemin |
|---|---|
| Script de génération fact sheets | CC: `/home/ubuntu/yos/ledger/generate_factsheets.py` |
| Script de retry | CC: `/home/ubuntu/yos/ledger/retry_errors.py` |
| Script extraction sémantique | CC: `/home/ubuntu/yos/ledger/semantic_extraction_gemini.py` |
| Script push Mem0 | Sandbox: `/home/ubuntu/push_mem0_sessions.py` |
| Script redaction secrets | CC: `/home/ubuntu/yos/ledger/redact_secrets_v2.py` |
| Rapport Fusion ChatGPT | GitHub: `08_LOGS/FUSION-COORDINATION-REPORT-2026-07-30.md` |

---

## 7. HISTORIQUE

| Date | Action |
|---|---|
| 2026-07-30 | Déblocage API v2 (clé 1Password MAIN VAULT) |
| 2026-07-30 | Génération 538 fact sheets + push GitHub PR #19 |
| 2026-07-31 | Découverte 26 sessions manquantes → corpus 564 |
| 2026-07-31 | PR #20 mergée — 564 fact sheets dans main |
| 2026-07-31 | Batch sémantique Gemini 2.5 Flash lancé (CC) |
| 2026-07-31 | Push Mem0 lancé (538 sessions) |
