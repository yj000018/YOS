# Task Routing Table (TRT) — Y-OS

> **Version** : 1.1.0 | **Date** : 2026-07-29
> **Statut** : Actif — source de vérité pour toute décision de routing de tâche dans Y-OS.
> **Anciennement** : `TASK-ROUTING-PROTOCOL.md` (renommé pour cohérence avec ART/CRT).

Ce document définit l'arbre de décision que tout agent Y-OS doit appliquer **avant d'exécuter une tâche**, qu'elle soit déclenchée par l'utilisateur, par un agent, ou programmatiquement. Il couvre le routing **intra-session, inter-session, inter-LLM et inter-outils**.

---

## 1. Architecture : TRT dans le Système Y-OS

```
┌─────────────────────────────────────────────────────┐
│              Y-OS ORCHESTRATION CORE                │
│  (méta-orchestrateur — appelle les 3 moteurs)       │
├──────────────┬──────────────────┬───────────────────┤
│     TRT      │       ART        │       CRT         │
│ Task Routing │ Autonomous       │ Continuity &      │
│ Table        │ Reasoning Thread │ Recovery Thread   │
│              │                  │                   │
│ QUAND/OÙ/    │ COMMENT          │ COMMENT           │
│ QUEL LLM ?   │ RAISONNER ?      │ REPRENDRE ?       │
│ (pré-session)│ (intra-session)  │ (inter-session)   │
└──────────────┴──────────────────┴───────────────────┘
         │              │                  │
         └──────────────┴──────────────────┘
                        │
                 TASK LEDGER
         (log cross-LLM, cross-session)
```

Les trois moteurs sont **complémentaires, non fusionnables**. Le Y-OS Orchestration Core les appelle dans l'ordre : TRT → ART → CRT. Le **Task Ledger** est la mémoire partagée qui alimente les trois.

---

## 2. Arbre de Décision TRT

```
TÂCHE REÇUE
     │
     ▼
[0] CONSULTER LE TASK LEDGER
     └── Existe-t-il une tâche similaire déjà traitée ou en cours ?
         ├── Oui → voir mode RESUME ou PARALLEL
         └── Non → [1]
     
[1] TAILLE & COMPLEXITÉ
     ├── Petite (< 5 min, ≤ 3 itérations, 0 dépendances) ──► INLINE
     └── Grande ──► [2]
     
[2] CONTINUITÉ CONTEXTUELLE
     ├── Continuité naturelle de la session courante ──► INLINE
     └── Digression ou thème orthogonal ──► [3]
     
[3] SESSION EXISTANTE (tous LLMs) ?
     ├── Oui — session dédiée dans n'importe quel LLM ──► RESUME
     └── Non ──► [4]
     
[4] CONTRAINTE OUTIL ?
     ├── Outil requis accessible uniquement depuis un LLM spécifique ──► TARGET-LLM (pour l'outil)
     └── Pas de contrainte outil ──► [5]
     
[5] SPÉCIALISATION COGNITIVE ?
     ├── LLM spécialisé clairement supérieur ──► [6]
     └── Y-OS/Manus suffit ──► NEW SESSION (Manus)
     
[6] ORCHESTRATION NÉCESSAIRE ?
     ├── Oui — Manus orchestre et délègue via MPM ──► ORCHESTRATED
     └── Non — aller directement ──► DIRECT (ouvrir le LLM cible)
```

---

## 3. Les 7 Modes de Routing

| Mode | Déclencheur | Action | Exemple |
|------|-------------|--------|---------|
| **INLINE** | Petite tâche ou continuité naturelle | Exécuter dans la session courante | Corriger un champ API pendant un chantier |
| **INLINE-CLOSE** | Digression petite mais utile | Exécuter, committer, fermer le sujet | Tester 5 endpoints API pendant une session Knowledge |
| **NEW SESSION** | Grande tâche, Y-OS/Manus suffit | Nouvelle session Manus + log dans Task Ledger | Chantier API Discovery |
| **RESUME** | Session existante (tout LLM) liée au thème | Prompt de reprise + handoff | Reprendre une session Claude sur ELYSIUM |
| **TARGET-LLM** | Outil requis accessible uniquement depuis un LLM | Ouvrir ce LLM pour l'outil, pas pour la cognition | Connecteur X uniquement dans GPT → y aller |
| **DIRECT** | LLM spécialisé + pas d'orchestration nécessaire | Ouvrir directement le LLM cible | Prose ELYSIUM → Claude directement |
| **ORCHESTRATED** | LLM spécialisé + Manus orchestre | Manus prépare le prompt MPM et délègue | Analyse 200K tokens → Gemini via MPM |

---

## 4. Sélection du LLM Cible

| Tâche | LLM Recommandé | Raison |
|-------|----------------|--------|
| Prose narrative / ELYSIUM | Claude (Anthropic) | Meilleur en écriture longue |
| Long document / analyse > 100K tokens | Gemini | Fenêtre de contexte maximale |
| Vision / analyse image | GPT-5 | Meilleur en multimodal |
| Recherche web temps réel | Perplexity / Grok | Web grounding |
| Code complexe / refactoring | Claude / GPT-5 | Raisonnement code |
| Orchestration générale + outils + Git | Manus (Y-OS) | Outil + mémoire + Git + Skills |
| Connecteur MCP spécifique | LLM qui a le connecteur | Contrainte outil |

---

## 5. Task Ledger — Log Cross-LLM

Le Task Ledger est le registre central de toutes les tâches Y-OS, indépendamment du LLM qui les exécute. Il est stocké dans Git : `YOS/08_LOGS/task-ledger/`.

### 5.1 Structure d'une entrée

```yaml
# YOS/08_LOGS/task-ledger/YYYY-MM-DD_TASK-ID.yaml
id: TRT-2026-07-29-001
title: "Chantier API Discovery Manus"
status: pending  # pending | running | done | blocked | delegated
llm: manus       # manus | claude | gpt | gemini | perplexity | grok
session_id: "iEMtCBXfxbmHaihbQ94hn4"  # UID de session si applicable
created: 2026-07-29T16:55:00Z
updated: 2026-07-29T16:55:00Z
theme: ["api", "manus", "discovery"]
parent_task: null  # ID de la tâche parente si sous-tâche
depends_on: []
output: null  # chemin vers le livrable si terminé
routing_mode: NEW SESSION
notes: "Continuer depuis INTERNAL-API-REFERENCE.md section 'À Explorer'"
```

### 5.2 Convention de nommage

`YYYY-MM-DD_TRT-NNN.yaml` — séquentiel par jour.

### 5.3 Consultation avant routing

Avant toute décision de routing, Manus doit :
1. Lister les entrées `status: running` ou `status: pending` dans `08_LOGS/task-ledger/`.
2. Chercher une correspondance thématique avec la tâche courante.
3. Si trouvé → mode RESUME avec le `session_id` et le `llm` de l'entrée.

---

## 6. Prompt de Reprise Standard (mode RESUME)

```
REPRISE DE SESSION — [TITRE]
LLM cible : [manus | claude | gpt | gemini]
Session ID : [uid si Manus, ou description si autre LLM]
Task Ledger ID : [TRT-YYYY-MM-DD-NNN]

Contexte de la session précédente :
[résumé en 3 lignes]

Décision de routing :
[pourquoi on reprend ici et pas ailleurs]

Tâche à poursuivre :
[description précise]

Fichiers/données à reprendre :
[liste avec chemins Git]
```

---

## 7. Intégration Y-OS

| Composant | Lien |
|-----------|------|
| **ART** | `01_BACKBONE/AGENTS/04_ROUTING/ART/README.md` |
| **CRT** | `01_BACKBONE/AGENTS/04_ROUTING/CRT/README.md` |
| **MPM** | `01_BACKBONE/MPM/` — transport inter-LLM |
| **Task Ledger** | `08_LOGS/task-ledger/` — log cross-LLM |
| **Sessions API** | `session.v1.SessionService/ListSessions` (interne validé) |
| **Tool Router** | `yos-agents/manus/yos-skills/tool-router/SKILL.md` |

---

## 8. Maintenance

À enrichir lors de chaque découverte :
- Nouveau LLM disponible → ajouter dans la table 4.
- Nouveau connecteur MCP exclusif → documenter la contrainte outil.
- Nouveau pattern de routing → ajouter dans les modes (section 3).
- Chaque tâche déléguée → créer une entrée Task Ledger.

*Voir aussi* : `TOOL-MAINTENANCE-PROTOCOL.md` · `01_BACKBONE/ROUTING/routing-rules.md`
