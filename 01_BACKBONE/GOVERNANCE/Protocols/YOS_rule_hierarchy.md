# ARCHITECTURE COGNITIVE Y-OS : Hiérarchie des Règles et Mécanique d'Escalade

> **ID:** YOS-ARCH-HIERARCHY
> **Type:** Core System Architecture
> **Statut:** Actif

---

## 1. La Pyramide Cognitive Y-OS (Les 5 Niveaux de Règles)

L'intelligence de Y-OS ne réside pas dans une seule énorme consigne, mais dans un système de **poupées russes cognitives**. Chaque niveau a une portée, un coût en contexte, et une cible précise.

| Niveau | Emplacement | Portée | Cible | Coût en Contexte | Exemple Typique |
|---|---|---|---|---|---|
| **L1. Constitution / Custom Instructions** | Prompt Système global (ChatGPT, Manus) | Universelle. Toujours active, toutes sessions. | Identité, posture, règles de sécurité absolues. | Très élevé (charge chaque prompt). | K1 (Autonomie), K9 (Optimisation), Posture d'Architecte. |
| **L2. Knowledge Entries / Skills** | RAG / Skills Manus injectés dynamiquement | Conditionnelle (activée selon l'intention). | Méthodes de travail réutilisables (K-Rules). | Moyen (injecté seulement si pertinent). | COP (Cognitive Operating Protocol), Règles Fransai. |
| **L3. Project Instructions** | Config Manus (Project Settings) | Limitée au projet en cours dans Manus. | Règles spécifiques à un environnement technique ou workflow local. | Faible (restreint au projet). | Règles de linting React, conventions de nommage du projet X. |
| **L4. Project Fact Sheet (Card)** | Notion / Mem0 (injecté au démarrage via Hydratation) | Limitée au contexte métier du projet. | Contexte métier, acteurs, objectifs, glossaire. | Faible (lu une fois au boot de session). | "Ce projet vise à consolider iOS avec le Universe." |
| **L5. Fichiers MD / Verbatim** | Système de fichiers / Git / Obsidian | Limitée à une tâche ou une feature spécifique. | Documentation technique, logs, PoC. | Nul (doit être explicitement lu via un outil). | `collector_the_universe_project.md`, specs d'API. |

---

## 2. Le "Self-Recursive COP" : La Mécanique d'Escalade

Le Cognitive Operating Protocol (COP) s'applique non seulement aux *projets* (comme Raindrop), mais aussi aux *règles elles-mêmes*.

Quand une règle naît, elle est d'abord locale (L5). Si elle s'avère excellente, le système doit **l'escalader**. Si elle devient obsolète, il doit la **rétrograder**.

### Le Pipeline d'Escalade d'une Règle :

1. **Génération (L5)** : On invente un workaround dans un fichier MD (ex: "Comment contourner l'OAuth Raindrop").
2. **Généralisation (L4/L3)** : On réalise que ça s'applique à tout le projet. On l'ajoute à la Fact Sheet ou aux Project Instructions.
3. **Formalisation (L2)** : La règle est tellement bonne qu'elle devient une méthode Y-OS. On en fait une Knowledge Entry / Skill (ex: "Le protocole COP").
4. **Sanctification (L1)** : La règle définit l'identité même de Y-OS. Elle monte dans la Constitution / Custom Instructions (ex: "Ne jamais demander d'aide avant d'avoir cherché un workaround").

### Le Déclencheur d'Escalade (Quand monter d'un niveau ?)

L'agent doit proposer l'escalade d'une règle quand :
- Elle est utilisée dans **3 sessions différentes** sur des projets différents (→ monte en L2).
- Son absence cause **systématiquement des erreurs** d'exécution (→ monte en L1).
- Elle définit un **comportement non négociable** pour Yannick (→ monte en L1).

---

## 3. Application au COP (Cognitive Operating Protocol)

**Où placer le COP actuellement ?**

Le COP est une mécanique de navigation. Ce n'est pas lié à un projet (L3/L4), ce n'est pas un simple fichier (L5). 

**Recommandation de placement :**
Le COP doit être placé en **L2 (Knowledge Entry / Agent Skill)**, avec un "pointeur" en **L1 (Custom Instructions)**.

**L1 (Custom Instructions) :**
> "Face à une nouvelle idée périphérique ou un blocage technique résolu, applique le *Cognitive Operating Protocol (COP)* : Contourner, Généraliser, Documenter, Parquer, Réactiver."

**L2 (Knowledge Entry / Skill 'yos-cop') :**
> (Le détail des 5 étapes, les formats de livrables de parking, l'intégration Mem0, comme défini dans `cognitive_operating_protocol.md`).

---

## 4. Règle d'Or de l'Hygiène Cognitive Y-OS

> **Ne jamais saturer le L1.** 
> Le L1 (Constitution) doit rester un index, une philosophie. Il doit pointer vers le L2 (Skills/Knowledge) pour l'exécution détaillée. Si le L1 devient trop lourd, l'agent perd en focus. L'escalade vers le L1 doit être rare et chirurgicale.
