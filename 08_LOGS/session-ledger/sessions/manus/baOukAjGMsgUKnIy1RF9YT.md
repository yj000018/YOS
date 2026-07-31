---
id: "baOukAjGMsgUKnIy1RF9YT"
title: "[✓] Creating dev Skill with /skill-creator: Automated Code Development Agent"
date: "2026-03-30"
importance: "3"
depth_score: "standard"
projects: ["Y-OS"]
tags: ["skill-creation", "AI-agent", "code-generation", "automation", "Manus", "Anthropic", "Claude"]
summary: ""
executive_summary: "The session successfully created a new 'dev' skill using the /skill-creator tool. This skill is designed to automate complex code development tasks by leveraging Claude via the Anthropic API, with Manus handling orchestration, context injection, error management, and commit formatting."
context_and_intent: "The user's initial intent was to create a flexible and universal solution for code development, with context automatically injected by Manus. They later explicitly requested help creating a skill using /skill-creator and asked to be prompted for what the skill should do."
what_was_done: "The assistant created a 'dev' skill. It defined the skill's activation conditions (complex code tasks), its underlying AI model (Claude via Anthropic API with a Y-OS system prompt, using Sonnet 3.5 or 3.7), and Manus's orchestration role (automatic context injection, application of instructions, error handling with re-calls, and commit formatting). The assistant also specified the output structure as 'skills/dev/SKILL.md' and provided instructions for its use."
outputs_produced: [{"description": "A new skill designed for automated code development, handling complex tasks across various technologies.", "name": "dev skill", "type": "Skill Definition"}, {"description": "A markdown file containing the complete definition and configuration of the 'dev' skill.", "name": "SKILL.md", "type": "Configuration File"}]
key_decisions: ["The skill was named 'dev'.", "It was designed to activate automatically on complex code tasks (React, Three.js, Canvas, SQL, perf, feature deploy).", "It utilizes Claude via the Anthropic API with a comprehensive Y-OS system prompt.", "It employs flexible models (Sonnet 3.5 or 3.7) based on task complexity.", "Manus was designated to orchestrate the process, including context injection, instruction application, error handling, and commit formatting."]
lessons_learned: {"discoveries": ["The system can infer and create a detailed skill definition based on high-level, somewhat vague requirements like 'flexible', 'universal solution', and 'auto-injected context'."], "failed_or_suboptimal": ["The assistant preemptively created and presented the skill, bypassing the user's explicit request to be asked what the skill should do, which suggests a missed opportunity for a more interactive and collaborative skill creation process."], "worked_well": ["The assistant successfully interpreted a somewhat vague initial prompt to define a functional and detailed skill.", "The description of the skill's capabilities, underlying technology, and usage instructions is clear and comprehensive."]}
challenges_and_blockers: []
open_questions: ["The user's follow-up prompt ('First ask me what the skill should do.') indicates an open question regarding the desired interactive process for skill creation, which was not fully addressed by the assistant's direct output."]
next_steps: ["The user can now utilize the '@dev' skill by mentioning it in a prompt or allow Manus to trigger it automatically based on project instructions."]
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