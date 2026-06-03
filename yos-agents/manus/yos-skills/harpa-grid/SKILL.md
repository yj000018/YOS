---
name: harpa-grid
description: Automate web browsers, scrape pages, search the web, and run AI prompts on live websites via HARPA AI Grid REST API
user-invocable: true
homepage: https://harpa.ai/grid/web-automation
metadata:
  emoji: 🌐
  requires:
    anyBins: [curl, wget]
    env: [HARPA_API_KEY]
  primaryEnv: HARPA_API_KEY
  skillKey: harpa-grid
---

# HARPA Grid — Browser Automation API

HARPA Grid lets you orchestrate real web browsers remotely. You can scrape pages, search the web, run built-in or custom AI commands, and send AI prompts with full page context — all through a single REST endpoint.

## Prerequisites

- HARPA AI Chrome Extension installed and running (at least one active Node)
- `HARPA_API_KEY` set in environment (configured dans yOS)

API Reference: https://harpa.ai/grid/grid-rest-api-reference

---

## Endpoint

```
POST https://api.harpa.ai/api/v1/grid
Authorization: Bearer $HARPA_API_KEY
Content-Type: application/json
```

---

## Usage via Script Python

Toujours utiliser le script Python `/home/ubuntu/skills/harpa-grid/harpa.py` pour appeler l'API.

```bash
python3 /home/ubuntu/skills/harpa-grid/harpa.py scrape --url "https://example.com"
python3 /home/ubuntu/skills/harpa-grid/harpa.py search --query "browser automation 2026"
python3 /home/ubuntu/skills/harpa-grid/harpa.py prompt --url "https://example.com" --prompt "Résume cette page : {{page}}"
python3 /home/ubuntu/skills/harpa-grid/harpa.py command --url "https://example.com" --name "Extract data" --inputs "List all headings"
```

---

## Actions

### 1. `scrape` — Extraire le contenu d'une page

Full page (markdown) :
```json
{
  "action": "scrape",
  "url": "https://example.com",
  "timeout": 15000
}
```

Ciblé (sélecteurs CSS) :
```json
{
  "action": "scrape",
  "url": "https://example.com/products",
  "grab": [
    {"selector": ".product-title", "selectorType": "css", "at": "all", "take": "innerText", "label": "titles"},
    {"selector": ".product-price", "selectorType": "css", "at": "all", "take": "innerText", "label": "prices"}
  ],
  "timeout": 15000
}
```

**Champs `grab` :**

| Champ | Requis | Valeurs |
|---|---|---|
| `selector` | oui | CSS, XPath, ou texte |
| `selectorType` | non | `auto`, `css`, `xpath`, `text` |
| `at` | non | `all`, `first`, `last`, ou un index |
| `take` | non | `innerText`, `innerHTML`, `href`, `value`, `attributes`, `[attrName]` |
| `label` | non | Nom du champ dans le résultat JSON |

---

### 2. `serp` — Recherche web

```json
{
  "action": "serp",
  "query": "browser automation 2026",
  "timeout": 15000
}
```

---

### 3. `command` — Commande HARPA prédéfinie

```json
{
  "action": "command",
  "url": "https://example.com/article",
  "name": "Extract data",
  "inputs": "List all headings with their word counts",
  "connection": "HARPA AI",
  "resultParam": "message",
  "timeout": 30000
}
```

- `name` : nom de la commande HARPA (ex: "Summary", "Extract data")
- `connection` : modèle LLM (`"HARPA AI"`, `"gpt-4o"`, `"claude-3.5-sonnet"`)

---

### 4. `prompt` — Prompt IA sur le contenu de la page

```json
{
  "action": "prompt",
  "url": "https://example.com",
  "prompt": "Analyse cette page et extrait toutes les informations de contact. Page: {{page}}",
  "connection": "CHAT AUTO",
  "timeout": 30000
}
```

- `{{page}}` : injecte le contenu complet de la page dans le prompt
- `connection` : modèle LLM à utiliser

---

## Paramètres communs

| Paramètre | Requis | Description |
|---|---|---|
| `action` | oui | `scrape`, `serp`, `command`, `prompt` |
| `url` | non | URL cible (ignoré par `serp`) |
| `node` | non | ID du node (`"r2d2"`), multiple (`"r2d2 c3po"`), N premiers (`"5"`), tous (`"*"`) |
| `timeout` | non | Délai max en ms (max 300000 = 5 min) |
| `resultsWebhook` | non | URL pour recevoir les résultats en async |
| `connection` | non | Modèle LLM pour `command`/`prompt` |

---

## Ciblage de Nodes

- Omettre `node` → utilise le node par défaut
- `"node": "mynode"` → node spécifique par ID
- `"node": "node1 node2"` → plusieurs nodes
- `"node": "3"` → 3 premiers nodes disponibles
- `"node": "*"` → broadcast à tous les nodes

---

## Résultats asynchrones (Webhook)

```json
{
  "action": "scrape",
  "url": "https://example.com",
  "resultsWebhook": "https://your-server.com/webhook",
  "timeout": 15000
}
```

---

## Tips yOS

- **Pages derrière login** : HARPA tourne dans un vrai browser avec les cookies de l'utilisateur → fonctionne sur les pages authentifiées.
- **Extraction structurée** : utiliser `grab` avec plusieurs sélecteurs pour extraire des données JSON en une seule requête.
- **Commandes longues** : augmenter `timeout` (max 300000ms) ou utiliser `resultsWebhook`.
- **`{{page}}`** dans les prompts injecte le contenu complet de la page — toujours l'utiliser pour donner du contexte au LLM.

---

## Positionnement dans yOS

| Outil | Rôle | Force |
|---|---|---|
| Playwright | Automation browser headless | Clics, formulaires, navigation, screenshots |
| Firecrawl | Scraping web à grande échelle | Crawl multi-pages, markdown bulk |
| **HARPA** | **Browser réel + IA contextualisée** | **Prompt LLM sur page ouverte, commandes AI** |

**Règle de routage :**
- Cliquer / remplir → Playwright
- Crawler 50+ pages → Firecrawl
- Comprendre / extraire avec intelligence → HARPA
