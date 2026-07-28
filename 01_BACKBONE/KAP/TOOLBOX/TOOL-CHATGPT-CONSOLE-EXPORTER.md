# TOOL — ChatGPT Console Exporter

**Status:** ✅ Validé en production (2026-07-28)
**Catégorie:** Data Acquisition / Export
**Coût:** 0 — gratuit, aucune dépendance externe
**Compatibilité:** ChatGPT Personal, Plus, **Business, Team, Enterprise** (fonctionne même quand l'export natif OpenAI est bloqué)

---

## Pourquoi c'est précieux

L'export natif OpenAI (`Settings → Data Controls → Export`) est **désactivé sur les comptes Business/Team**. Ce script contourne cette limitation en s'exécutant directement dans le contexte de la page web — il a accès au token de session et à l'API backend ChatGPT sans restriction.

---

## Utilisation (3 étapes)

### Étape 1 — Récupérer le script JS
Ouvrir dans le navigateur :
```
https://gist.github.com/ocombe/1d7604bd29a91ceb716304ef8b5aa4b5/raw/export-chatgpt-console.js
```
→ Cmd+A → Cmd+C (tout sélectionner et copier)

### Étape 2 — Exécuter dans la console Chrome
1. Aller sur **chat.openai.com** (connecté)
2. Ouvrir la console : **Cmd+Option+J** (Mac) ou **F12 → Console**
3. Coller le script (Cmd+V) → Entrée
4. Un overlay de progression apparaît automatiquement

### Étape 3 — Récupérer le ZIP
- Le ZIP se télécharge automatiquement sur le bureau
- Contient : `json/` + `markdown/` + `html/` + `files/` (images, attachments)

---

## Output structure

```
chatgpt-export/
  json/           ← Raw JSON par conversation (machine-readable)
  markdown/       ← MD par conversation (human-readable, liens vers fichiers)
  html/           ← Viewer HTML avec sidebar navigation
  files/          ← Images DALL-E, uploads, code interpreter outputs
    <conv_name>/
      image.png
      document.pdf
```

---

## Caractéristiques techniques

| Propriété | Valeur |
|---|---|
| **Source** | GitHub Gist — ocombe |
| **URL** | https://gist.github.com/ocombe/1d7604bd29a91ceb716304ef8b5aa4b5 |
| **Méthode** | Browser console injection (same-origin) |
| **Token** | Auto-détecté via `/api/auth/session` |
| **Pagination** | 100 conversations par page, toutes récupérées |
| **Rate limiting** | 500ms entre les appels (respectueux) |
| **Formats** | JSON + Markdown + HTML + fichiers attachés |
| **Dépendances** | Aucune — standard browser APIs uniquement |
| **Privacy** | 100% local — rien ne passe par un serveur externe |

---

## Intégration KAP

Après export :
1. Envoyer le ZIP à Manus
2. Manus dézippe → indexe → génère factsheets Python pur (0 token LLM)
3. Push dans `KAP/01_SOURCES/chatgpt/`
4. Mise à jour `SOURCE-MATRIX.md`

---

## Notes

- **Ne pas coller la commande `curl -sL https://...`** dans la console Chrome — c'est du bash, pas du JS. Ouvrir l'URL dans le navigateur d'abord, copier le contenu JS, puis coller dans la console.
- Le script gère automatiquement la pagination (toutes les conversations, pas de limite)
- Les conversations ChatGPT Projects sont incluses
- Fonctionne aussi sur Edge, Brave, et autres navigateurs Chromium

---

*Formalisé dans YOS Toolbox — 2026-07-28*
