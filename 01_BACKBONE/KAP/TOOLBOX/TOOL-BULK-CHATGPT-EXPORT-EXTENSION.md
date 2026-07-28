# TOOL — Bulk ChatGPT Export (Extension Chrome)

**Status:** ✅ Acheté et validé (2026-07-28)
**Catégorie:** Data Acquisition / Export
**Coût:** Payant (achat unique) — licence Yannick
**Compatibilité:** ChatGPT Personal, Plus, **Business, Team, Enterprise**

---

## Pourquoi c'est précieux

Conçu spécifiquement pour les comptes **Teams et Business** où l'export natif OpenAI est désactivé. Gère les historiques massifs (1000+ conversations), supporte les **ChatGPT Projects**, et exporte le format JSONL complet avec toutes les métadonnées — citations, canvas, tool use, fichiers attachés.

Complément à la solution console script : l'extension offre une UI persistante, la reprise d'export interrompue, et le skip automatique des conversations déjà exportées.

---

## Installation

**Chrome Web Store :**
```
https://chromewebstore.google.com/detail/bulk-chatgpt-export-all-d/jpgkcijdlkngndibgepnilffkkbkejdc
```

---

## Utilisation

1. Cliquer sur l'icône de l'extension dans Chrome
2. **Connect** → sélectionner l'onglet ChatGPT
3. Cliquer **Start Export**
4. L'extension exporte toutes les conversations + Projects automatiquement
5. Télécharger le fichier `.jsonl.gz` compressé

---

## Caractéristiques techniques

| Propriété | Valeur |
|---|---|
| **Éditeur** | Matt Brooks / brookssolutions.xyz |
| **Version** | 4.1.0 (mis à jour 2026-07-27) |
| **Format output** | JSONL (JSON Lines) + Gzip compression |
| **Compression** | 90%+ réduction de taille |
| **Resume** | Pause/reprise à tout moment |
| **Smart Skip** | Ignore les conversations déjà exportées |
| **Progress** | Tracking temps réel |
| **Privacy** | 100% local — aucun serveur externe |
| **Données capturées** | Messages complets, citations, tool use, canvas, DALL-E, uploads, métadonnées, model version, timestamps |

---

## Différences vs Script Console

| Critère | Script Console | Bulk Export Extension |
|---|---|---|
| **Installation** | Aucune | Extension Chrome |
| **Coût** | Gratuit | Payant (acheté) |
| **Output** | JSON + MD + HTML | JSONL.gz |
| **Resume** | Non | ✅ Oui |
| **Smart Skip** | Non | ✅ Oui |
| **Projects** | Partiel | ✅ Complet |
| **Métadonnées** | Basiques | ✅ Complètes |
| **Usage idéal** | Export ponctuel rapide | Export massif / récurrent |

**Stratégie recommandée :**
- **Script console** → export ponctuel, urgent, sans installation
- **Bulk Export Extension** → export complet récurrent, grands volumes, avec Projects

---

## Intégration KAP

Après export :
1. Décompresser le `.jsonl.gz` : `gunzip export.jsonl.gz`
2. Envoyer le JSONL à Manus
3. Manus parse → génère factsheets Python pur (0 token LLM)
4. Push dans `KAP/01_SOURCES/chatgpt/`
5. Mise à jour `SOURCE-MATRIX.md`

---

## Notes

- Format JSONL = 1 ligne JSON par conversation → compatible Python/Pandas/jq
- Gzip compression = fichiers très légers même pour 1000+ conversations
- Smart Skip = idéal pour les exports incrémentaux (delta hebdomadaire)

---

*Formalisé dans YOS Toolbox — 2026-07-28*
