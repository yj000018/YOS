---
id: "jHeC4WPRLQMcHBF2wx96YA"
title: "[✓] Problème d'installation/confirmation d'action sur iOS"
date: "2026-03-03"
importance: "3"
depth_score: "standard"
projects: ["Y-OS"]
tags: ["iOS", "browser", "UX", "bug", "payment", "Manus app", "flow interruption"]
summary: "User reports flow interruption on iOS due to Manus app's browser confirmation popup during payment, seeking a smoother experience."
executive_summary: "A user is frustrated by a persistent browser confirmation prompt on iOS during payment, which interrupts their workflow. They seek solutions to bypass this prompt, either by defaulting to the current browser, allowing a desktop switch, or permanently disabling the question."
context_and_intent: "The user is experiencing a recurring interruption during the iOS payment process where the assistant prompts them about browser usage. The user's intent is to streamline this process by either having the assistant automatically use the default browser, allowing a seamless switch to desktop, or providing an option to permanently disable the prompt."
what_was_done: "The user reported a persistent issue with the iOS payment flow being interrupted by a browser confirmation prompt. They articulated their frustration and proposed several potential solutions or asked for clarification on existing options to bypass or manage this interruption. The assistant acknowledged the issue and initiated a technical explanation."
outputs_produced: [{"description": "The assistant acknowledges the user's complaint and begins to explain the technical reality of the situation.", "name": "First Response", "type": "Assistant Message"}]
key_decisions: []
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": []}
challenges_and_blockers: ["Recurring interruption in the iOS payment flow due to a browser confirmation prompt.", "Disruption of user workflow and perceived inefficiency."]
open_questions: ["Does the user have any choice regarding the browser prompt?", "Can the user resume the process from a desktop?", "Is it possible for the assistant to automatically use the default browser on iOS without asking?", "Can the assistant be configured to never ask the browser question again?", "Can the assistant recommend switching to a desktop browser for speed, and would it make a difference?", "Does using the current iOS browser versus a desktop browser make a difference in the payment flow?"]
next_steps: ["Assistant to provide a technical explanation for the current behavior.", "Explore options for automatic default browser usage on iOS.", "Investigate possibility of a 'never ask again' option for the browser prompt.", "Evaluate if a desktop browser offers a significant performance advantage for payments."]
url: "https://manus.im/app/task/jHeC4WPRLQMcHBF2wx96YA"
---

# [✓] Problème d'installation/confirmation d'action sur iOS

| Field | Value |
|-------|-------|
| **Session ID** | `jHeC4WPRLQMcHBF2wx96YA` |
| **Date** | 2026-03-03 08:35 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/jHeC4WPRLQMcHBF2wx96YA](https://manus.im/app/sessions/jHeC4WPRLQMcHBF2wx96YA) |
| **Messages** | 3 user · 3 assistant · 12 total |

## Initial Prompt

Pardon, une bonne partie de mon message manquait. Je disais "Tu interromps toujours le flow sur la pay iOS en me demandant cette histoire de browser." Est-ce que j'ai un choix quelconque ? Je peux pas reprendre depuis le desktop ou et cetera. Je suis sur le browser. Donc, lorsque je suis sur iOS, est-ce qu'il y aurait une possibilité que tu ne me poses pas la question et que tu utilises directement le le default browser ? Parce que là, je te  pose des questions et tu as des retours totalement le flow.  au minimum si si je réponds pas pour passer sur le desktop dans les 10 secondes alors tu continues le default browser ou bien est-ce que je peux te donner l'ordre ne me pose plus jamais la question.  Ou bien est-ce que tu peux décider par toi-même et me recommander non, là ce serait tellement plus rapide avec le le browser desktop. Est-ce que ça ferait une différence que j'utilise le browser ici ou que je passe sur le desktop ?  J'ai mon flow qui est interrompu à chaque fois à cause de c

## First Response

Compris. Voici la réalité technique, sans détour.

**Ce qui se passe**

Cette interruption vient de Manus lui-même — pas de moi. Quand une tâche nécessite le browser, Manus affiche cette popup "Set up My Browser Extension" et **attend ta confirmation** avant de continuer. C'est un comportement système de l'app Manus, pas une décision que je prends.

**Tes options réelles**

| Option | Réalité |
|---|---|
| Cliquer "No, use default browser" | Ça débloque immédiatement. Manus continue avec le browser sandbox intégré. |
| Ignorer / ne pas répondre | Manus reste bloqué indéfiniment — il ne timeout pas automatiquement. |
| Me donner l'ordre "ne pose plus jamais la question" | Je ne contrôle pas cette popup — c'est l'UI Manus qui la génère. |
| Desktop vs iOS | Aucune différence fonctionnelle pour moi. Le browser que j'utilise est dans mon sandbox, pas sur ton appareil. |

**Ce que tu dois faire**

Quand cette popup apparaît : **clique "No, use default browser"**. C'est le seul déblocage pos

## Conversation Summary

> **User:** Pardon, une bonne partie de mon message manquait. Je disais "Tu interromps toujours le flow sur la pay iOS en me demandant cette histoire de browser." Est-ce que j'ai un choix quelconque ? Je peux pas reprendre depuis le desktop ou et cetera. Je suis sur le browser. Donc, lorsque je suis sur iOS, est-ce qu'il y aurait une possibilité que tu ne me poses pas la question et que tu utilises directement le le default browser ? Parce que là, je te  pose des questions et tu as des retours totalement le...

> **User:** continue

> **User:** Depuis la  Et je dois te faire confirmer la main. C'est aucun sens, je peux pas  Il y a d'autres personnes que je n'aime.  dans la part  Donc, je peux pas je peux pas installer

> **Manus:** Compris. Voici la réalité technique, sans détour.

**Ce qui se passe**

Cette interruption vient de Manus lui-même — pas de moi. Quand une tâche nécessite le browser, Manus affiche cette popup "Set up My Browser Extension" et **attend ta confirmation** avant de continuer. C'est un comportement système de l'app Manus, pas une décision que je prends.

**Tes options réelles**

| Option | Réalité |
|---|---|
| Cliquer "No, use default browser" | Ça débloque immédiatement. Manus continue avec le browser sandbox intégré. |
| Ignorer / ne pas répondre | Manus reste bloqué indéfiniment — il ne timeout pas automatiquement. |
| Me donner l'ordre "ne pose plus jamais la question" | Je ne contrôle pas cette popup — c'est l'UI Manus qui la génère. |
| Desktop vs iOS | Aucune différence fonctionnelle po...

> **Manus:** Je n'ai pas le contexte de la session précédente — chaque session Manus est indépendante.

Dis-moi : quelle était la tâche originale que tu voulais accomplir ? Je relance directement.

## Full Verbatim

<details>
<summary>Expand full conversation (6 messages)</summary>

**[1772527064111] MANUS:** Compris. Voici la réalité technique, sans détour.

**Ce qui se passe**

Cette interruption vient de Manus lui-même — pas de moi. Quand une tâche nécessite le browser, Manus affiche cette popup "Set up My Browser Extension" et **attend ta confirmation** avant de continuer. C'est un comportement système de l'app Manus, pas une décision que je prends.

**Tes options réelles**

| Option | Réalité |
|---|---|
| Cliquer "No, use default browser" | Ça débloque immédiatement. Manus continue avec le browser sandbox intégré. |
| Ignorer / ne pas répondre | Manus reste bloqué indéfiniment — il ne timeout pas automatiquement. |
| Me donner l'ordre "ne pose plus jamais la question" | Je ne contrôle pas cette popup — c'est l'UI Manus qui la génère. |
| Desktop vs iOS | Aucune différence fonctionnelle pour moi. Le browser que j'utilise est dans mon sandbox, pas sur ton appareil. |

**Ce que tu dois faire**

Quand cette popup apparaît : **clique "No, use default browser"**. C'est le seul déblocage pos...
**[1772527052095] USER:** Pardon, une bonne partie de mon message manquait. Je disais "Tu interromps toujours le flow sur la pay iOS en me demandant cette histoire de browser." Est-ce que j'ai un choix quelconque ? Je peux pas reprendre depuis le desktop ou et cetera. Je suis sur le browser. Donc, lorsque je suis sur iOS, est-ce qu'il y aurait une possibilité que tu ne me poses pas la question et que tu utilises directement le le default browser ? Parce que là, je te  pose des questions et tu as des retours totalement le flow.  au minimum si si je réponds pas pour passer sur le desktop dans les 10 secondes alors tu continues le default browser ou bien est-ce que je peux te donner l'ordre ne me pose plus jamais la question.  Ou bien est-ce que tu peux décider par toi-même et me recommander non, là ce serait tellement plus rapide avec le le browser desktop. Est-ce que ça ferait une différence que j'utilise le browser ici ou que je passe sur le desktop ?  J'ai mon flow qui est interrompu à chaque fois à cause de c...
**[1772527025082] MANUS:** Je n'ai pas le contexte de la session précédente — chaque session Manus est indépendante.

Dis-moi : quelle était la tâche originale que tu voulais accomplir ? Je relance directement.
**[1772527021499] USER:** continue
**[1772526960934] MANUS:** Je vois le screenshot — Manus te demande de confirmer l'installation de l'extension browser "My Browser Extension" sur desktop, ce qui bloque la tâche.

**Problème identifié :** La session précédente utilisait le skill `session-synthesizer` qui tente de scraper l'UI Manus via le browser. Il a besoin de l'extension desktop pour fonctionner, ce que tu ne peux pas installer depuis mobile.

**Options :**

1. **"No, use default browser"** — Clique ce bouton dans la session bloquée. Manus tentera de continuer sans l'extension (résultat incertain).
2. **Reprendre depuis desktop** — La tâche nécessite un accès browser desktop pour fonctionner correctement.
3. **Me dire l'objectif réel** — Qu'est-ce que tu voulais accomplir dans cette session ? Je peux relancer la tâche différemment, sans dépendance à l'extension.

Quelle était la tâche originale ?
**[1772526944660] USER:** Depuis la  Et je dois te faire confirmer la main. C'est aucun sens, je peux pas  Il y a d'autres personnes que je n'aime.  dans la part  Donc, je peux pas je peux pas installer



</details>