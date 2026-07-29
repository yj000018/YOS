# Task Routing Protocol (TRP) — Y-OS

> **Version** : 1.0.0 | **Date** : 2026-07-29
> **Statut** : Actif — source de vérité pour toute décision de routing de tâche dans Y-OS.

Ce protocole définit l'arbre de décision que Manus (ou tout agent Y-OS) doit appliquer **avant d'exécuter une tâche**, qu'elle soit déclenchée par l'utilisateur, par un agent, ou programmatiquement.

---

## 1. Arbre de Décision Principal

```
TÂCHE REÇUE
     │
     ▼
[1] TAILLE & COMPLEXITÉ
     ├── Petite (< 5 min, < 3 itérations, pas de dépendances) ──► INLINE (dans la session courante)
     └── Grande (> 5 min, itérations multiples, dépendances) ──► [2]
     
[2] PERTINENCE CONTEXTUELLE
     ├── Continuité naturelle de la session courante ──► INLINE (poursuivre ici)
     └── Digression ou thème orthogonal ──► [3]
     
[3] SESSION EXISTANTE ?
     ├── Oui — session dédiée à ce thème existe ──► RESUME (prompt de reprise + handoff)
     └── Non ──► [4]
     
[4] SPÉCIALISATION LLM ?
     ├── LLM spécialisé clairement supérieur (ex: Claude pour prose, Gemini pour long doc) ──► [5]
     └── Manus suffit ──► NEW SESSION (nouvelle session Manus)
     
[5] ORCHESTRATION NÉCESSAIRE ?
     ├── Oui — Manus orchestre et délègue via MPM/API ──► ORCHESTRATED (Manus → LLM cible)
     └── Non — aller directement dans le LLM ──► DIRECT (ouvrir Claude/GPT/Gemini directement)
```

---

## 2. Les 5 Modes de Routing

| Mode | Déclencheur | Action | Exemple |
|------|-------------|--------|---------|
| **INLINE** | Tâche petite ou continuité naturelle | Exécuter dans la session courante sans interruption | Corriger un champ `title` → `name` pendant un chantier API |
| **INLINE-CLOSE** | Digression petite mais utile | Exécuter, committer, fermer le sujet | Tester 5 endpoints API pendant une session Knowledge |
| **NEW SESSION** | Tâche grande, thème orthogonal, Manus suffit | Créer une nouvelle session Manus avec un prompt de contexte | Chantier de découverte API complet |
| **RESUME** | Session dédiée existante | Générer un prompt de reprise + handoff vers la session existante | Reprendre FUSION pour une synthèse de sessions |
| **DIRECT** | LLM spécialisé clairement supérieur, pas d'orchestration nécessaire | Ouvrir directement Claude/GPT/Gemini avec le contexte | Prose ELYSIUM → Claude directement |
| **ORCHESTRATED** | LLM spécialisé + orchestration Manus nécessaire | Manus prépare le prompt MPM et délègue via API | Analyse long doc → Gemini via MPM |

---

## 3. Critères de Décision Détaillés

### 3.1 Évaluation de la Taille

| Indicateur | Petite | Grande |
|------------|--------|--------|
| Durée estimée | < 5 min | > 5 min |
| Nombre d'itérations | ≤ 3 | > 3 |
| Dépendances externes | Aucune | Oui (API, fichiers, LLMs) |
| Risque de side effects | Nul | Présent |
| Nombre de fichiers modifiés | ≤ 2 | > 2 |

### 3.2 Sélection du LLM Cible

| Tâche | LLM Recommandé | Raison |
|-------|----------------|--------|
| Prose narrative / ELYSIUM | Claude (Anthropic) | Meilleur en écriture longue |
| Long document / analyse > 100K tokens | Gemini | Fenêtre de contexte maximale |
| Vision / analyse image | GPT-5 | Meilleur en multimodal |
| Recherche web temps réel | Perplexity / Grok | Web grounding |
| Code complexe / refactoring | Claude / GPT-5 | Raisonnement code |
| Orchestration générale | Manus | Outil + mémoire + Git |

### 3.3 Routing Inter-Session

Avant de créer une nouvelle session, vérifier via `session.v1.SessionService/ListSessions` si une session pertinente existe déjà :
- Chercher par titre ou thème dans les 100 dernières sessions.
- Si trouvée et récente (< 7 jours) : générer un **prompt de reprise** avec le contexte actuel.
- Si trouvée mais ancienne (> 7 jours) : créer une nouvelle session avec référence à l'ancienne.

---

## 4. Prompt de Reprise Standard

Quand le mode est **RESUME**, générer ce prompt pour la session cible :

```
REPRISE DE SESSION — [TITRE]
Contexte de la session précédente : [résumé en 3 lignes]
Décision de routing : [pourquoi on reprend ici]
Tâche à poursuivre : [description précise]
Fichiers/données à reprendre : [liste]
```

---

## 5. Intégration avec Y-OS

- **Déclencheur automatique** : Ce protocole doit être appliqué par Manus à chaque nouvelle tâche reçue, avant toute exécution.
- **Lien MPM** : Les modes ORCHESTRATED et RESUME s'appuient sur `01_BACKBONE/MPM/` pour le transport inter-LLM.
- **Lien Sessions API** : Le routing inter-session utilise `session.v1.SessionService/ListSessions` (endpoint interne validé — voir `manus-api/internal/INTERNAL-API-REFERENCE.md`).
- **Lien Skills** : Le skill `tool-router` couvre le routing des outils. Ce protocole couvre le routing des **tâches** (plus haut niveau).

---

## 6. Note de Maintenance

Ce protocole est vivant. À enrichir lors de chaque découverte :
- Nouveau LLM disponible → ajouter dans la table 3.2.
- Nouveau pattern de routing identifié → ajouter dans les modes (section 2).
- Nouvelle capacité de session API → mettre à jour section 3.3.

*Voir aussi* : `TOOL-MAINTENANCE-PROTOCOL.md` · `01_BACKBONE/ROUTING/routing-rules.md` · `01_BACKBONE/MPM/`
