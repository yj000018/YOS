# PROJET : Collector the Universe — Sources Externes Y-OS

> **Statut :** Parqué — réactiver après consolidation iOS/CAP
> **Créé :** 2026-07-29
> **Contexte :** Pendant la phase iOS/CAP, on documente et teste les sources externes. Réactivation complète post-consolidation.

---

## Vision

Chaque source externe gravitant autour de Yannick (bookmarks, boards, stars, feeds...) est connectée à Y-OS via un **pipeline modulaire à 3 couches** :

1. **Connecteur** — accès à la source (auth, endpoint)
2. **Nettoyage** — maintenance qualité (tagging, dédup, normalisation)
3. **Acquisition delta** — ingestion incrémentale vers le Universe

> Ces sources définissent le **Universe** — tout ce qu'on sait sur Yannick, ses projets, ses intérêts.

---

## Architecture Universelle — Template Pipeline

```
SOURCE EXTERNE
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  COUCHE 1 — CONNECTEUR                                  │
│  Quoi : Auth + endpoint unique vers la source           │
│  Comment : OAuth2 / API Key / Test Token                │
│  Stockage : Manus Secrets + /home/ubuntu/.yos_secrets/  │
│  Réutilisé par : Couche 2 ET Couche 3                   │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  COUCHE 2 — NETTOYAGE / MAINTENANCE QUALITÉ             │
│  Quoi : Améliorer la qualité de la source elle-même     │
│  Mode : On-demand OU scheduled (automatique)            │
│  Opérations typiques :                                  │
│    • Tagging IA (classification LLM)                    │
│    • Déduplication (URLs, titres similaires)            │
│    • Normalisation (titres, métadonnées)                │
│    • Archivage / suppression des liens morts            │
│  Output : Source améliorée (pas d'ingestion vers Y-OS)  │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  COUCHE 3 — ACQUISITION DELTA → UNIVERSE                │
│  Quoi : Ingérer le nouveau contenu dans Y-OS            │
│  Mode : Scheduled (quotidien / hebdo)                   │
│  Opérations :                                           │
│    • Fetch delta depuis last_sync (curseur persisté)    │
│    • Enrichissement : résumé LLM + embedding            │
│    • Routing : Universe / Y-OS / Projet spécifique      │
│  Output : Notion | Mem0 | Vector DB                     │
└─────────────────────────────────────────────────────────┘
```

---

## Coût LLM des Pipelines

| Opération | Modèle | Tokens/run | Coût/run | Coût total (7127 signets) |
|---|---|---|---|---|
| Tagging (C2) | claude-haiku-4-5 | ~16K | ~$0.008 | ~$0.11 |
| Résumé (C3) | claude-haiku-4-5 | ~50K | ~$0.025 | ~$0.35 |
| Embedding (C3) | text-embedding | ~20K | ~$0.002 | ~$0.03 |

**Conclusion : NÉGLIGEABLE.** Tagger 7127 signets Raindrop = ~$0.11 total. Scheduled nightly = ~$0.008/nuit.

---

## Sources — État Actuel

| Source | Volume | C1 | C2 | C3 | Priorité |
|---|---|---|---|---|---|
| **Raindrop** | 7 127 signets | ✅ | ✅ Scheduled | ⬜ À faire | **P1** |
| GitHub Stars | ~500 repos | ⬜ | ⬜ | ⬜ | P2 |
| Pinterest | N/A | ⬜ | ⬜ | ⬜ | P2 |
| Pocket | N/A | ⬜ | ⬜ | ⬜ | P3 |
| Manus Sessions | ∞ | ✅ | ✅ | ✅ Mem0 | P1 ✅ |

---

## SOURCE 1 : Raindrop.io — Documentation Complète

### Identité

| Champ | Valeur |
|---|---|
| Type | Bookmarks / Favoris web |
| Volume | 7 127 signets |
| Non tagués | ~2 984 (après run 2026-07-29) |
| Fréquence update | Quotidien (ajouts manuels) |
| Valeur Y-OS | Intérêts, lectures, outils, inspirations de Yannick |

---

### COUCHE 1 — Connecteur Raindrop

**Auth :** Test Token permanent (ne jamais reset)

```
App Name      : Raindrop to yOS
Client ID     : 6a0da56f9a8b8816ae48f3f4
Client Secret : 8a97af79-842c-4517-bc2b-e15396cd930e
Test Token    : 98422e2a-e0bd-4e35-be68-9277f52caaac  ← PERMANENT
API Base      : https://api.raindrop.io/rest/v1
Auth Header   : Authorization: Bearer {test_token}
```

**Stockage :** `/home/ubuntu/.yos_secrets/raindrop.json`

**Endpoints principaux :**

```
GET  /user                                     → vérification auth
GET  /raindrops/0?search=notag:true&perpage=50 → signets non tagués
GET  /raindrops/0?perpage=50&page=N            → pagination complète
GET  /raindrops/0?sort=-created&perpage=50     → les plus récents (delta)
PUT  /raindrop/{id}                            → update tags/métadonnées
GET  /tags/0                                   → liste des tags existants
GET  /collections                              → collections/dossiers
```

**Contrainte API :** Max 50 items/page malgré `perpage=150`.

**Doc officielle :** https://developer.raindrop.io/

---

### COUCHE 2 — Nettoyage Raindrop

**Mode :** Automatique — Scheduled nightly (02h00 Europe/Zurich)

**Scheduled Task Manus :**
- Nom : "Raindrop — Tagging IA nuit (3 490 signets)"
- ID : `eUYJNyFHQbLLiR2C8AvSDC`
- Cron : `0 0 2 * * *` (02h00 chaque nuit)
- Mode : `full_auto`
- URL : https://manus.im/app#scheduled-tasks/eUYJNyFHQbLLiR2C8AvSDC

**Script :** `/home/ubuntu/raindrop_tagger.py`

**Ce que fait le nettoyage :**

1. Fetch 50 signets non tagués (`search=notag:true`)
2. Analyse titres + domaines avec `claude-haiku-4-5`
3. Attribue 1-3 tags pertinents par signet
4. Applique via `PUT /raindrop/{id}` avec `{"tags": [...]}`
5. Répète jusqu'à 10 lots (500 signets/run)
6. S'arrête automatiquement quand `count=0`

**Tags préférés :** ai, technology, finance, music, youtube, wellness, science, diy, lifestyle, shopping, design, art, travel, productivity, startup, business, health, education, programming, video, tool, research, social

**Fallback :** Si LLM échoue → règles domain-based (youtube→video, github→programming, amazon→shopping...)

**Résultats run initial (2026-07-29) :**
- 500 signets tagués
- 0 erreurs API
- Durée : ~25 minutes
- Coût LLM : ~$0.008

**Progression estimée :**

| Run | Date | Tagués | Restants |
|---|---|---|---|
| Run 1 | 2026-07-29 | 500 | ~2 984 |
| Run 2 | 2026-07-30 | 500 | ~2 484 |
| Run 3 | 2026-07-31 | 500 | ~1 984 |
| ... | ... | ... | ... |
| Run 7 | 2026-08-04 | 500 | ~0 |

---

### COUCHE 3 — Acquisition Delta Raindrop → Universe

**Statut :** À développer (post-consolidation iOS/CAP)

**Logique delta :**

```python
# Pseudocode — à implémenter dans raindrop_delta_sync.py
last_sync = load_cursor("raindrop_last_sync")  # ISO timestamp

# Fetch uniquement les nouveaux signets
new_bookmarks = GET /raindrops/0?sort=-created&perpage=50
# Filtrer ceux créés après last_sync
new_bookmarks = [bm for bm in new_bookmarks if bm.created > last_sync]

for bm in new_bookmarks:
    enriched = {
        "title": bm.title,
        "url": bm.link,
        "tags": bm.tags,
        "collection": bm.collection.title,
        "summary": llm_summarize(bm.title + " " + bm.excerpt),
        "source": "raindrop"
    }
    push_to_mem0(enriched, user_id="yannick")
    push_to_notion(enriched, db="Universe Knowledge")

save_cursor("raindrop_last_sync", now())
```

**Destination :** Mem0 (cross-session) + Notion Universe Knowledge DB

---

## Template Fiche Source (Réutilisable pour chaque nouvelle source)

```markdown
## SOURCE : {NOM}

### Identité
- Type : {Bookmarks / Social / Code / Feed / ...}
- Volume : ~{N} items
- Fréquence update : {quotidien / hebdo / ...}
- Valeur Y-OS : {ce que ça apporte à la connaissance de Yannick}

### COUCHE 1 — Connecteur
- Auth : {OAuth2 / API Key / Test Token}
- Token/Key : {référence fichier .yos_secrets}
- API Base : {URL}
- Doc : {URL documentation}
- Contraintes : {limites rate, pagination, etc.}

### COUCHE 2 — Nettoyage
- Mode : {Manuel / Scheduled}
- Si scheduled : {cron, ID task Manus}
- Script : {chemin fichier}
- Opérations : {liste des nettoyages effectués}
- Fréquence : {mensuel / hebdo / nightly}
- Dernière exécution : {date}
- Coût LLM estimé : {$/run}

### COUCHE 3 — Acquisition Delta
- Curseur : {type: timestamp / ID / etag}
- Script : {chemin fichier}
- Destination : {Mem0 / Notion / VectorDB}
- Fréquence : {quotidien / hebdo}
- Dernière sync : {date}
```

---

## Prochaines Étapes (Post-Consolidation iOS/CAP)

1. **Finir C2 Raindrop** — ~7 runs nightly automatiques → 0 non tagués
2. **Développer C3 Raindrop** — pipeline delta vers Mem0 + Notion Universe
3. **Créer module `source-connector`** — template universel Y-OS
4. **GitHub Stars (P2)** — PAT existant `ghp_PZalt6Au2hYRrmMnFR0XU0awfw2XXe3CT0FC`
5. **Pinterest (P2)** — OAuth2 + extraction boards visuels
6. **Dashboard sources** — état de toutes les sources, dernière sync, volume delta

---

## Relation avec Y-OS Global

```
Y-OS Knowledge Universe
        │
        ├── iOS / CAP (P1 — EN COURS)
        │     └── Consolidation, acquisition, delta
        │
        └── Sources Externes (CE PROJET — parqué)
              ├── Raindrop  ← C1✅ C2✅ C3⬜
              ├── GitHub Stars  ← ⬜⬜⬜
              ├── Pinterest  ← ⬜⬜⬜
              └── ...
```

---

*Script tagging : `/home/ubuntu/raindrop_tagger.py`*
*Secrets : `/home/ubuntu/.yos_secrets/raindrop.json`*
*Scheduled task : https://manus.im/app#scheduled-tasks/eUYJNyFHQbLLiR2C8AvSDC*
*Dernière mise à jour : 2026-07-29*
