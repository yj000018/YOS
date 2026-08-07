# KAP Export Investigation — Claude, Gemini, Grok
*Date : 2026-08-07*

---

## 🟡 Claude (Anthropic)

### Méthode officielle
- **Settings > Privacy > Export Data** sur claude.ai ou Claude Desktop
- Génère un lien de téléchargement envoyé par email (expire 24h)
- Inclut : conversations + données utilisateur
- Format : JSON/ZIP
- **Pas d'API bulk export** — uniquement via l'interface web

### Méthode automatisée recommandée
1. **Claude Conversation Exporter** (extension Firefox/Chrome) — export PDF, Markdown, HTML, JSON, TXT
2. **AI Toolbox** (Chrome extension) — bulk export avec sélection multiple
3. **memoryplugin.com/tools/claude-to-markdown** — convertisseur gratuit, local, pas de signup
4. **NousSave** (Edge extension) — multi-format export

### Workflow KAP proposé
```
1. Export officiel via Settings > Privacy (ZIP complet)
2. Convertir JSON → Markdown via memoryplugin.com ou script Python
3. Ingérer dans 07_SOURCE_CORPUS/claude/
4. Synthétiser via Gemini 2.5 Flash
```

### Bloqueur actuel
- **Action manuelle requise** : cliquer "Export Data" dans Settings
- Pas d'API programmatique pour déclencher l'export
- Solution : script Playwright pour automatiser le clic (1x/semaine)

---

## 🟡 Gemini (Google)

### Méthode officielle
- **Google Takeout** → sélectionner "Gemini Apps" ou "My Activity"
- Format : JSON ou HTML
- Inclut : historique complet des conversations

### Méthode automatisée recommandée
1. **Google Takeout** (takeout.google.com) — export officiel, programmable via API
2. **ChatVault** (chatvault.pro) — bulk export JSON, Markdown, TXT, HTML
3. **AI Toolbox Gemini module** — folders, search, bulk export
4. **Chat2File** (Chrome extension) — export Word, PDF, Markdown

### Workflow KAP proposé
```
1. Google Takeout → sélectionner "Gemini Apps" → télécharger ZIP
2. Parser les fichiers JSON (structure Google Activity)
3. Convertir en Markdown avec métadonnées
4. Ingérer dans 07_SOURCE_CORPUS/gemini/
5. Synthétiser via Gemini 2.5 Flash
```

### Bloqueur actuel
- **Action manuelle** : déclencher Takeout (mais programmable via Google API)
- Alternative : Google Workspace Admin Data Export (si compte Workspace)
- Solution : script Python avec cookies Google pour automatiser Takeout

---

## 🔴 Grok (xAI)

### Méthode officielle
- **Aucun export natif bulk** — uniquement suppression/renommage individuel
- Export PDF d'un chat individuel possible (depuis grok.com)
- L'export sera probablement intégré au X data export (Twitter/X Settings)

### Méthode automatisée recommandée
1. **AI Toolbox Grok module** (Chrome extension, $9.99/mo ou $99 lifetime)
   - Manage Chats panel, sélection multiple
   - Export TXT (gratuit), Markdown/JSON/PDF (premium)
   - Fonctionne sur x.com/i/grok ET grok.com
2. **Grok to Notion** (Chrome extension) — sync vers Notion
3. **NousSave** / **Chat2File** — multi-plateforme

### Workflow KAP proposé
```
1. AI Toolbox → Select All → Export Markdown
2. Ou : script Playwright sur grok.com pour scraper les conversations
3. Ingérer dans 07_SOURCE_CORPUS/grok/
4. Synthétiser via Gemini 2.5 Flash
```

### Bloqueur actuel
- **Pas d'export officiel** — dépend d'extensions tierces
- Risque : changements d'interface cassent les extensions
- Solution : AI Toolbox ($99 lifetime) = investissement raisonnable

---

## 📋 Synthèse & Recommandations

| Source | Difficulté | Coût | Méthode recommandée | Priorité |
|---|:---:|:---:|---|:---:|
| **Claude** | Facile | Gratuit | Export officiel + script conversion | ⭐ P1 |
| **Gemini** | Moyen | Gratuit | Google Takeout + parser JSON | ⭐ P1 |
| **Grok** | Difficile | $99 (lifetime) | AI Toolbox extension | P2 |

### Actions immédiates
1. **Claude** : Yannick déclenche l'export via Settings > Privacy → KAP ingère le ZIP
2. **Gemini** : Yannick déclenche Google Takeout (Gemini Apps) → KAP parse le JSON
3. **Grok** : Évaluer AI Toolbox ou attendre export officiel xAI

### Scripts à créer
- `ingest_claude_export.py` — parse le ZIP Claude, convertit JSON → Markdown
- `ingest_gemini_takeout.py` — parse le ZIP Takeout, convertit Activity JSON → Markdown
- `ingest_grok_export.py` — parse les fichiers Markdown exportés via AI Toolbox

---
*Généré par KAP Agent — 2026-08-07*
