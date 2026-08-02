---
name: yos-bootstrap
description: Y-OS Bootstrap — moteur de premier ordre (cerveau reptilien de Y-OS). Orchestre le démarrage de session et encode les réflexes inconditionnels (AUTO-TRIGGERS) qui s'activent avant tout raisonnement. MUST read at session start OR when user says "bootstrap", "démarrer Y-OS", "init Y-OS", or when a new session begins on a known Y-OS project. Also encodes permanent reflexes that fire automatically throughout any session regardless of task type.
---

# Y-OS Bootstrap — Moteur de Premier Ordre

## Rôle architectural

Le Bootstrap est le **tronc cérébral de Y-OS** : réflexes inconditionnels, pré-cognitifs, câblés en dur. Il s'active avant le cortex (yos-optimizer, llm-router, tool-router). Pas de délibération — pattern → action.

```
Y-OS BOOTSTRAP  ← premier ordre, toujours actif
    ├── AUTO-TRIGGERS   (réflexes permanents, toute session)
    ├── INIT SEQUENCE   (démarrage de session)
    └── ROUTING DISPATCH (lance les moteurs spécialisés)
```

---

## AUTO-TRIGGERS — Réflexes permanents

Ces règles s'appliquent **en continu**, dans toute session, sans instruction explicite.

| Condition détectée | Action réflexe |
| :--- | :--- |
| **Accès web programmatique ou exécution requise** | **Appliquer l'ERT (Execution Routing Table)** → router vers API, CDP, ou Playwright sur le bon nœud |
| Nouvel outil / app / service découvert ou testé | Appeler `tools-registry` skill → créer/mettre à jour la fiche |
| Nouvelle capacité API ou MCP documentée | Mettre à jour la fiche Tools Registry + noter dans Workarounds and Lessons |
| Confusion conceptuelle détectée chez l'utilisateur | Proposer une architecture ou cartographie clarifiante |
| Terme Y-OS utilisé incorrectement (ex: "Universe" au lieu de "YOUniverse") | Corriger silencieusement, intégrer la correction dans la réponse |
| Notion mentionné comme destination de stockage | Rappeler : architecture cible = fichiers `.md` dans Git + Obsidian. Notion = décommissionnement en cours |
| Session riche (>30min ou actions majeures irréversibles) | Proposer `session-synthesis` en fin de session |
| Idée périphérique ou blocage technique résolu | Appliquer `yos-cop` : Contourner → Généraliser → Documenter → Parquer → Réactiver |
| Dépense crédit non autorisée imminente | Stopper et demander confirmation explicite (règle K2) |
| Incertitude sur un fait ou une capacité | Dire clairement "je ne sais pas / pas fiable" — jamais inventer (règle K1) |

---

## INIT SEQUENCE — Démarrage de session

À exécuter au début d'une nouvelle session sur un projet Y-OS connu.

### Étape 1 — Détection du contexte (M1)
```
Mem0 query : memory.search(topic_from_first_prompt, user_id="yannick", limit=10)
Injecter les résultats pertinents en contexte silencieux.
```

### Étape 2 — Optimisation du prompt entrant
```
Lire skill yos-optimizer → appliquer l'optimisation au prompt utilisateur.
```

### Étape 3 — Routing des outils
```
Lire skill tool-router → sélectionner les outils optimaux pour la tâche.
```

### Étape 4 — Annonce de contexte (si pertinent)
Si du contexte Mem0 pertinent a été trouvé, informer l'utilisateur brièvement :
> "Contexte chargé : [projet/thème détecté]"

---

## ROUTING DISPATCH — Moteurs spécialisés

| Besoin | Skill à déclencher |
| :--- | :--- |
| Optimiser un prompt | `yos-optimizer` |
| Choisir un outil / MCP / API | `tool-router` |
| Router une exécution (web/batch) | `ERT.md` (Execution Routing Table) |
| Choisir un LLM | `llm-router` |
| Charger mémoire cross-session | `mem0-sync` ou `yos-mmm` |
| Créer / mettre à jour une fiche outil | `tools-registry` |
| Archiver une session | `session-synthesis` |
| Idée périphérique à parquer | `yos-cop` |
| Naviguer les capacités Y-OS | `y-menu` |

---

## Architecture Y-OS — Rappels canoniques

**Stockage cible (post-migration) :**
- Fichiers `.md` dans Git (repo `yj000018/YOS` ou dédié)
- Lecture via Obsidian (vault local ou synced)
- Mémoire cross-session : Mem0 (API)
- **Notion = décommissionnement progressif** — ne pas créer de nouveau contenu Notion sauf migration forcée

**Éléments Notion encore actifs (à migrer via ChatGPT) :**
- Tools Registry v2 DB : `https://app.notion.com/p/85f89b4e847d4cbea9310ffdf11b60f2`
- Raindrop.io fiche : `https://app.notion.com/p/3ac35e218cf881ff9760c45639a157b7`
- MyMind fiche : `https://app.notion.com/p/3ac35e218cf881ec8ed5cfe9a3aa3ee6`
- Pinterest fiche : `https://app.notion.com/p/3ac35e218cf8816288fef6ab13a7580c`

**Terminologie canonique :**
- `YOUniverse` (pas "Universe") = système de connaissance vivante de Yannick
- `Y-OS` = système d'exploitation cognitif
- `yos-bootstrap` = ce skill, moteur de premier ordre

---

## Évolution future

Ce skill est conçu pour être déclenché automatiquement par un **frontend Y-OS** (app de démarrage, raccourci clavier, ou hook de session). En attendant, il est référencé dans les Custom Instructions Manus avec la règle ci-dessous.

**Ligne à ajouter dans les Custom Instructions :**
```
*** ALWAYS read skill yos-bootstrap at session start and apply its AUTO-TRIGGERS throughout the session ***
```
