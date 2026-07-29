---
name: yos-cop
description: "Cognitive Operating Protocol (COP) — Mécanique systématique de navigation Y-OS pour gérer les idées périphériques, les blocages techniques, et les nouvelles pistes sans se disperser. Use when: a new idea emerges during a session that is not the main objective, a technical workaround has been found and should be generalized, a proof-of-concept is validated and needs parking before industrialization, or the user says 'documente ca', 'parque ce projet', 'on reviendra dessus'."
---

# Cognitive Operating Protocol (COP)

## Quand activer ce protocole

Activer COP dès qu'une des conditions suivantes est vraie :
- Une idée périphérique émerge pendant une session dont ce n'est pas l'objectif principal.
- Un blocage technique a été contourné (workaround trouvé) — la solution mérite d'être généralisée.
- Un PoC tactique est validé mais demande un lourd effort d'industrialisation.
- L'utilisateur dit "parque ça", "on reviendra dessus", "documente les acquis".

## Le Cycle COP en 5 Étapes

### 1. CONTOURNER
Trouver le chemin de moindre résistance. Ne pas s'acharner sur le blocage principal.
- Ex: OAuth impossible en headless → utiliser un Test Token permanent.
- Règle : 2 tentatives max sur la même approche, puis pivoter.

### 2. GÉNÉRALISER
Extraire le modèle universel du cas particulier. Chaque solution tactique doit produire un pattern stratégique.
- Ex: "Connecter Raindrop" → modèle universel "3 couches par source externe" (Auth / Maintenance / Delta).
- Poser la question : "Si on faisait la même chose pour Pinterest, GitHub Stars, Pocket — qu'est-ce qui serait identique ?"

### 3. DOCUMENTER
Écrire les acquis dans un fichier Markdown structuré. Inclure :
- Ce qui a fonctionné (et pourquoi).
- Les impasses rencontrées (pour ne pas les répéter).
- L'architecture généralisée.
- Le coût (tokens LLM, temps, complexité).
- Le code/script produit (chemin vers le fichier).

### 4. PARQUER
**Action proactive de l'agent** — ne pas attendre que l'utilisateur le demande.
- Créer une fiche projet `[PARQUÉ]` avec le format défini ci-dessous.
- Annoncer clairement : "J'ai parqué ce projet. On peut reprendre quand tu veux."
- Revenir immédiatement à l'objectif principal de la session.

### 5. RÉACTIVER
Au retour sur un thème parqué :
- Rechercher dans Mem0 : `memory.search("nom_du_projet", user_id="yannick")`
- Charger la fiche projet depuis Notion ou le repo Git Y-OS.
- Reprendre exactement là où on s'est arrêté, sans refaire les erreurs documentées.

## Format Livrable de Parking

```markdown
# [PARQUÉ] Nom du Projet

**Date de parking :** YYYY-MM-DD
**Contexte d'origine :** (session où l'idée a émergé)
**Priorité :** Basse / Moyenne / Haute

## Acquis Tactiques
(Ce qui a été validé dans cette session)

## Architecture Universelle
(Le modèle généralisé extrait du cas particulier)

## Fiche Technique
(Tokens, endpoints, credentials, scripts produits)

## Impasses à Éviter
(Ce qui n'a pas marché et pourquoi)

## Roadmap de Réactivation
- [ ] Étape 1 : ...
- [ ] Étape 2 : ...
```

## Mécanique d'Escalade des Règles

Voir `references/rule_hierarchy.md` pour la pyramide complète des 5 niveaux (L1→L5) et les critères d'escalade.

**Règle rapide :**
- Règle utilisée dans 3 sessions différentes → escalader en L2 (Knowledge Entry / Skill)
- Règle dont l'absence cause des erreurs systématiques → escalader en L1 (Custom Instructions)
- Ne jamais saturer le L1 — il reste un index philosophique, pas un manuel.
