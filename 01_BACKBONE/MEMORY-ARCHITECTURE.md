# YOS — Memory Architecture
> Version: 1.0 | Date: 2026-07-29 | Owner: Yannick Jolliet / Y-OS

---

## 1. Principes fondamentaux

Le système mémoire de Y-OS est **multi-couche, multi-LLM, et partiellement automatisé**. Chaque couche a un rôle distinct. La règle d'or :

- **Mettre** : au niveau le plus bas qui couvre le scope requis
- **Lire** : au niveau le plus haut disponible automatiquement, puis descendre si besoin
- **Jamais dupliquer** entre couches sauf pour le mirroring explicite (Project Instructions ← Fact Sheet)

---

## 2. Cartographie des couches mémoire

| # | Couche | Stockage | Scope | Injection | Géré par |
|---|--------|----------|-------|-----------|----------|
| 1 | **Custom Instructions** | Manus Settings/Profile | Universel, toutes sessions | Auto, permanent | Manuel (canonique, stable) |
| 2 | **KM Entries UPPERCASE** | Manus Settings/Knowledge | Universel transversal | Auto, toutes sessions | `km-consolidator` |
| 3 | **KM Entries lowercase** | Manus Settings/Knowledge | Delta quotidien | Auto, toutes sessions | Manus auto |
| 4 | **Project Instructions** | Manus Settings/Project | Projet Manus uniquement | Auto, sessions projet | Script `project-sync` |
| 5 | **Project Fact Sheet** | YOS/Git + Notion | Tous LLMs, source de vérité | Manuel (Context Pack) | `km-consolidator` + user |
| 6 | **Context Pack (CP)** | Git + transfert | Cross-LLM, one-shot | Manuel copy-paste | skill `continuity-pack` |
| 7 | **Mem0** | Mem0 API (cloud) | Cross-session, cross-LLM | Auto query session start | `session-synthesis` |
| 8 | **Notion Memory Hub** | Notion y-World | Archive structurée longue durée | Manuel (hydratation) | `session-synthesis` |
| 9 | **KAP Corpus** | YOS/Git KAP/ | Sources brutes, deep context | Manuel (deep retrieval) | `km-consolidator` |

---

## 3. Règles de mise (où stocker)

```
Universel + stable + court → Custom Instructions (limite ~3000 chars)
Universel + évolutif + thématique → KM Entry UPPERCASE
Projet-spécifique + tous LLMs → Project Fact Sheet (Git)
Projet-spécifique + Manus uniquement → Project Instructions (mirror auto de Fact Sheet)
Session à archiver → Notion Memory Hub + Mem0 (toujours les deux)
Contexte à transférer entre LLMs → Context Pack (généré depuis Fact Sheet)
Source brute à absorber → KAP Corpus (Git)
```

---

## 4. Règles de lecture (où chercher)

### Injection automatique (sans action)
- Custom Instructions → injectées à chaque session Manus
- KM Entries (UPPERCASE + lowercase) → injectées à chaque session Manus
- Project Instructions → injectées si session liée au projet

### Retrieval actif (action requise)
- **Mem0** : `memory.search(topic, user_id='yannick', limit=10)` → en début de session sur thème connu
- **Notion** : hydratation via skill `hydrater` ou `project-hydration`
- **KAP Corpus** : lecture directe Git pour deep context
- **Context Pack** : généré via skill `continuity-pack`, copié manuellement vers autre LLM

---

## 5. Cycle de vie des KM Entries

```
Session Manus génère lowercase entries (auto, à la volée)
    ↓ accumulation
    ↓ km-consolidator détecte delta (nouvelles lowercase)
    ↓ identifie UPPERCASE cible par thème (SYS/ARC/GOV/DOM)
    ↓ fusionne : append simple OU réécriture densifiée
    ↓ si proche 2000 chars → compression maximale (même sens, moins de chars)
    ↓ supprime lowercase processées
    ↓ commit Git (YOS/KAP/03_SOURCES/manus-knowledge-entries/)
```

**Signal visuel :** `UPPERCASE` = consolidé pérenne. `lowercase` = delta non traité.

**Quota allocation :** 40 UPPERCASE max / 60 lowercase disponibles (ratio 40/60).

---

## 6. Mirroring Project Instructions ← Fact Sheet

```
Fact Sheet mise à jour (Git: YOS/projects/{name}/FACT-SHEET.md)
    ↓ script project-sync (background, automatique)
    ↓ lit Fact Sheet complète
    ↓ génère condensé ≤2800 chars (LLM compression)
    ↓ écrit dans Manus Project Instructions via Playwright
    ↓ log dans YOS/logs/project-sync.log
```

**Règle :** Project Instructions = miroir compressé de Fact Sheet. Jamais édité manuellement. Toujours régénéré depuis Fact Sheet.

---

## 7. Custom Instructions — rôle canonique

Les Custom Instructions sont la **Constitution** de Y-OS. Elles définissent :
- L'identité et la posture de l'agent
- Les règles non-négociables (K1-K12 condensées)
- Le style de communication
- Les pointeurs vers les systèmes (1P, Manus Secrets, Notion workspace)

**Limite :** ~3000 chars. **Stabilité :** très haute — ne changent que lors d'évolutions majeures de Y-OS.

**Ce qui ne va PAS dans Custom Instructions :** règles opérationnelles détaillées, listes de sources, configs projets → tout ça va dans KM Entries UPPERCASE.

---

## 8. Taxonomie KM Entries UPPERCASE

### SYS — Moteur (comportements fondamentaux)
```
SYS-01-CORE-EXECUTION      Autonomie, exécution, reporting
SYS-02-POLICIES            K7 financier, suppression, transfert données
SYS-03-CREDENTIALS         1P, Manus Secrets, auth agent
SYS-04-NETWORK-INFRA       K5 retry, serveurs, zero-touch
SYS-05-MEMORY-SYSTEM       Notion, Mem0, KAP, archivage
SYS-06-OUTPUT-FORMAT       MD, gate delivery, inter-LLM
SYS-07-TOOLS-ROUTING       LLM matrix, MCP routing, PIL, browser
```

### ARC — Architecture (modules, pipelines)
```
ARC-08-MODULES-SPEC        Modules yOS 1-20
ARC-09-3D-MINDMAP          Spline, TreeMap, UX 3D
ARC-10-CONTEXT-CONTINUITY  Inter-LLM, CP, contraintes
ARC-11-SOURCE-REGISTRY     Où trouver quoi (Git/Notion/Mem0/1P/Skills/MCPs)
ARC-12-KAP-PIPELINE        Sources, gate reports, versioning
```

### GOV — Gouvernance (décisions, résolution, coûts)
```
GOV-13-RESOLUTION-TREE     Arbre universel : clés/logins/CAPTCHA/accès bloqué
GOV-14-HOMEOSTASIS         Auto-nettoyage, checks périodiques, santé système
GOV-15-COST-GOVERNANCE     Crédits, modèle routing, estimation
GOV-16-ERROR-ESCALATION    4 niveaux, jamais bloquer silencieusement
GOV-17-SECURITY-WORKFLOW   CAPTCHA + secrets + auth + sync 1P
GOV-18-DECISION-FRAMEWORK  Audit→options→recommandation→validation
GOV-19-COMM-PREFERENCES    Tutoiement, dense, télégraphique, voix architecte
```

### DOM — Domaines thématiques
```
DOM-20-PERSONAL-CONTEXT    Livres, spirituel, identité, rôle
DOM-21-ARCHETYPES          Sources, traditions, chakra mapping
DOM-22-NOTIFICATIONS       Pushover, Telegram, multi-device
DOM-23-CODE-PRACTICES      GitHub, scripts, versioning, MVP
DOM-24-INFRA-ACCESS        Serveurs, MiniPC, Art TD, deployment
DOM-25-PROJECTS-META       P1-P4, ODYSSEY, ELYSIUM
DOM-26-FILE-MGMT           Consolidation, déduplication, migration
DOM-27-UX-PREFERENCES      Language, browser, input, color-coding
```

---

## 9. Diagramme de flux global

```
┌─────────────────────────────────────────────────────────┐
│                    SESSION MANUS                         │
│                                                         │
│  Auto-injecté:                                          │
│  ├── Custom Instructions (Constitution)                 │
│  ├── KM Entries UPPERCASE (SYS/ARC/GOV/DOM)            │
│  ├── KM Entries lowercase (delta non traité)            │
│  └── Project Instructions (si projet actif)            │
│                                                         │
│  Sur demande:                                           │
│  ├── Mem0 query (session start sur thème connu)         │
│  ├── Notion hydratation (skill hydrater)                │
│  └── KAP deep retrieval (Git direct)                   │
└─────────────────────────────────────────────────────────┘
         ↕ archivage                    ↕ transfer
┌──────────────────┐          ┌─────────────────────────┐
│  Notion Memory   │          │  Context Pack (CP)       │
│  Hub + Mem0      │          │  → ChatGPT / Claude /    │
│  (session cards) │          │    autre LLM             │
└──────────────────┘          └─────────────────────────┘
         ↕ source de vérité
┌──────────────────────────────────────────────────────────┐
│  YOS/Git                                                 │
│  ├── 01_BACKBONE/KAP/03_SOURCES/ (corpus brut)          │
│  ├── projects/{name}/FACT-SHEET.md (source de vérité)   │
│  └── skills/ (code réutilisable)                        │
└──────────────────────────────────────────────────────────┘
```

---

## 10. Maintenance & évolution

| Fréquence | Action | Outil |
|-----------|--------|-------|
| Chaque session | Query Mem0 sur thème connu | Auto (SYS-05) |
| Chaque archivage | Push Notion + Mem0 | `session-synthesis` |
| Hebdomadaire | Consolider lowercase → UPPERCASE | `km-consolidator` |
| Mensuel | Audit Custom Instructions | Manuel |
| Sur changement Fact Sheet | Sync → Project Instructions | Script `project-sync` |
| Sur nouvelle clé API | Sync → Manus Secrets + 1P | GOV-17 + script |
