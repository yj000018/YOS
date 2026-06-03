---
name: summary
description: Generates a structured strategic synthesis of the current session — reasoning thread, decisions, conclusions, and execution state. Use when the user asks "résumé", "synthèse", "summary", "fil rouge", or wants to understand the full arc of the session before archiving, continuing, or closing. Includes an Exec Summary and numbered actions for next steps. Replaces the former 'statut' skill.
---

# Summary Skill

Strategic synthesis. Full arc of the session. Highly structured with visual separators.

## Rules
- No preamble. Start directly with the first separator.
- Only report facts from the current session. Never invent.
- Focus on *why* decisions were made, not just *what* was done.
- Telegraphic where possible, but complete enough to reconstruct the session from scratch.
- Output MUST be rendered directly in the chat — NO triple-backtick code block wrapping.
- Respect the exact visual structure below.

## Output Format

Output the following structure directly as Markdown in the chat message (no code block):

==============
🧠 EXECUTIVE SUMMARY
==============
[1-2 phrases très denses : objectif ultime de la session + résultat majeur atteint.]

==============
📍 FIL ROUGE & RAISONNEMENT
==============
- 🏁 **DÉPART**         : [Intention initiale]
- 🔄 **PIVOT**          : [Changement de direction et *pourquoi*]
- 🎯 **ABOUTISSEMENT**  : [Où le raisonnement nous a menés]

==============
⚖️ DÉCISIONS & ACQUIS
==============
- ✅ [Décision 1 : formulation précise + raison]
- 📦 [Acquis 1 : ce qui est validé, produit, ou retenu]

==============
🚧 CHALLENGES & LIMITATIONS
==============
- 🛑 [Challenge 1 : description + impact]
*(Si aucun : "Aucun point de blocage majeur.")*

==============
⏳ ÉTAT D'EXÉCUTION (STATUS)
==============
- 🟢 **FAIT**    : [liste]
- 🟡 **PENDING** : [liste]
- 🔴 **BLOQUÉ**  : [liste + raison]

==============
💡 CONCLUSIONS
==============
[Ce qui a été appris, validé, ou résolu. Ce qui reste ouvert.]

#############
⏭️ SUITE & CLÔTURE
#############

1. 🚀 **POURSUIVRE**          : [Prochaine étape logique]
2. 🔍 **APPROFONDIR**         : [Aspect spécifique à creuser]
3. 🧠 **ARCHIVER KNOWLEDGE**  : Clôturer → Notion (référence permanente)
4. ✅ **ARCHIVER TÂCHE**      : Clôturer simplement pour référence
5. 🧩 **FUSIONNER**           : Identifier des sessions similaires pour fusion
6. 📋 **STATUS RAPIDE**       : Lancer la skill `status`

## Post-Choix : Intégration Écosystème

Si l'utilisateur répond par un numéro (3 à 5), exécuter le workflow correspondant.

### Protocole de Clôture Visuelle (Choix 3 ou 4 — OBLIGATOIRE)

Avant tout archivage, exécuter les trois étapes suivantes dans l'ordre :

**1. Générer un nouveau titre de session** selon la règle de nommage Y-OS :
- Format : `[DOMAINE] Sujet principal — Résultat ou décision clé (YYYY-MM-DD)`
- Exemples : `[Y-OS] Skills status/summary — Refonte & protocole clôture (2026-03-26)`
- Le titre doit être court, scannable, et archivable
- Afficher le titre suggéré en gras, encadré, avec instruction explicite :

> 📋 **TITRE SUGGÉRÉ — À copier-coller manuellement dans le champ de titre de la session :**
> 
> `[[ [DOMAINE] Sujet — Résultat clé (YYYY-MM-DD) (archived) ]]`

**2. Marqueur de fin de session** — Ajouter en toute fin du chat, avec saut de ligne avant et après :

####### ARCHIVED #######

---

### Choix 3 (Archiver Knowledge Source)
1. Appliquer le Protocole de Clôture Visuelle.
2. Générer l'exécutif summary depuis le template : `/home/ubuntu/skills/summary/templates/exec_summary.md`
3. Sauvegarder dans `/home/ubuntu/exec_summary_{session_id}.md`
4. Lancer : `python3.11 /home/ubuntu/yos/mmm/scripts/yos_archive_pipeline.py --session-text "$(cat /home/ubuntu/exec_summary_{session_id}.md)" --title "[Titre]"`

### Choix 4 (Archiver Tâche Terminée)
1. Appliquer le Protocole de Clôture Visuelle.
2. Générer le JSON de synthèse via : `cat current_conversation.txt | python3 /home/ubuntu/skills/summary/scripts/generate_summary.py > summary_data.json`
3. Lancer : `python /home/ubuntu/skills/memory-manager/scripts/archive_conversation.py summary_data.json`

### Choix 5 (Fusionner)
Appliquer le protocole `FUSION` de la skill `session-navigator`.

### Choix 6 (Status rapide)
Invoquer la skill `status` directement.

## Tone
Direct. Calm. Precise. Architect's voice. French unless session is in another language.
