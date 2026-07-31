---
id: baOukAjGMsgUKnIy1RF9YT
title: "[✓] Creating dev Skill with /skill-creator: Automated Code Development Agent"
date: "2026-03-30"
importance: 3
projects: ["Y-OS"]
tags: ["skill-creation", "AI-agent", "code-generation", "automation", "Manus", "Anthropic", "Claude"]
summary: ""
url: "https://manus.im/app/task/baOukAjGMsgUKnIy1RF9YT"
---

# [✓] Creating dev Skill with /skill-creator: Automated Code Development Agent

| Field | Value |
|-------|-------|
| **Session ID** | `baOukAjGMsgUKnIy1RF9YT` |
| **Date** | 2026-03-30 05:08 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/baOukAjGMsgUKnIy1RF9YT](https://manus.im/app/sessions/baOukAjGMsgUKnIy1RF9YT) |
| **Messages** | 2 user · 4 assistant · 10 total |

## Initial Prompt

1 flexible
2 sais pas faut sol assez universel 
3 contexte injecté auto par manus

## First Response

Skill `dev` validé et prêt.

**Ce qu'il fait :**
- S'active automatiquement sur les tâches code complexes (React, Three.js, Canvas, SQL, perf, feature deploy)
- Appelle Claude via l'API Anthropic avec un system prompt Y-OS complet (stack, règles, output format strict)
- Modèle flexible : Sonnet 3.5 ou 3.7 selon la complexité
- Manus orchestre : injecte le contexte projet automatiquement, applique les `[MANUS INSTRUCTIONS]` dans l'ordre, gère les erreurs avec re-call + stack trace, commite en `feat: <TASK SUMMARY>`

**Structure livrée :**
```
skills/dev/
└── SKILL.md  ← tout est ici, pas de ressources externes inutiles
```

Pour l'utiliser : `@dev [description de la tâche]` ou laisser Manus le déclencher automatiquement via les Project Instructions.

## Conversation Summary

> **User:** 1 flexible
2 sais pas faut sol assez universel 
3 contexte injecté auto par manus

> **User:** Help me create a skill together using /skill-creator. First ask me what the skill should do.

> **Manus:** Skill `dev` validé et prêt.

**Ce qu'il fait :**
- S'active automatiquement sur les tâches code complexes (React, Three.js, Canvas, SQL, perf, feature deploy)
- Appelle Claude via l'API Anthropic avec un system prompt Y-OS complet (stack, règles, output format strict)
- Modèle flexible : Sonnet 3.5 ou 3.7 selon la complexité
- Manus orchestre : injecte le contexte projet automatiquement, applique les `[MANUS INSTRUCTIONS]` dans l'ordre, gère les erreurs avec re-call + stack trace, commite en `feat: <TASK SUMMARY>`

**Structure livrée :**
```
skills/dev/
└── SKILL.md  ← tout est ici, pas de ressources externes inutiles
```

Pour l'utiliser : `@dev [description de la tâche]` ou laisser Manus le déclencher automatiquement via les Project Instructions.

> **Manus:** Clair. Je passe en construction directe.

## Full Verbatim

<details>
<summary>Expand full conversation (6 messages)</summary>

**[1774847538138] MANUS:** Skill `dev` validé et prêt.

**Ce qu'il fait :**
- S'active automatiquement sur les tâches code complexes (React, Three.js, Canvas, SQL, perf, feature deploy)
- Appelle Claude via l'API Anthropic avec un system prompt Y-OS complet (stack, règles, output format strict)
- Modèle flexible : Sonnet 3.5 ou 3.7 selon la complexité
- Manus orchestre : injecte le contexte projet automatiquement, applique les `[MANUS INSTRUCTIONS]` dans l'ordre, gère les erreurs avec re-call + stack trace, commite en `feat: <TASK SUMMARY>`

**Structure livrée :**
```
skills/dev/
└── SKILL.md  ← tout est ici, pas de ressources externes inutiles
```

Pour l'utiliser : `@dev [description de la tâche]` ou laisser Manus le déclencher automatiquement via les Project Instructions.
**[1774847440936] MANUS:** Clair. Je passe en construction directe.
**[1774847437878] USER:** 1 flexible
2 sais pas faut sol assez universel 
3 contexte injecté auto par manus
**[1774847355327] MANUS:** J'ai lu le document attaché. Le contenu est déjà très structuré — c'est clairement une spec de skill `@dev` : moteur de code Claude intégré dans Manus pour les projets Y-OS.

Avant de construire, trois questions précises :

**1. Modèle Claude**
Le doc spécifie `claude-sonnet-4-5`. Tu veux garder ce modèle exact, ou laisser la flexibilité de choisir entre sonnet/opus selon la complexité de la tâche ?

**2. Stack Y-OS**
La stack listée (React 19, Three.js, SQLite schema nodes/edges, design tokens) — c'est la stack universelle de tous tes projets, ou certains projets ont des stacks différentes ? Si oui, le skill doit-il gérer plusieurs profils de stack ?

**3. Contexte projet**
Le doc dit "Manus insère le contexte projet". Est-ce que tu veux que le skill aille chercher automatiquement les fichiers récents du projet (via shell/git), ou tu fournis toujours le contexte manuellement dans le prompt ?
**[1774847337406] MANUS:** Reading the skill-creator skill and the attached content first.
**[1774847333563] USER:** Help me create a skill together using /skill-creator. First ask me what the skill should do.



</details>
