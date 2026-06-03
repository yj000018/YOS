---
name: archive
description: >-
  Guides the full closure and archiving protocol for a Manus session. Use when
  the user chooses to archive (options 3 or 4 from summary), or explicitly asks
  to archive, close, or clore the session. Executes 4 sequential steps —
  Notion export via Chrome extension, confirmation, manual title rename, system archiving.
---

# Archive Skill

Session closure protocol. Sequential. No step can be skipped.

## Rules
- Guide each step explicitly. Wait for user confirmation before moving to the next.
- Generate the suggested title before anything else — the user needs it upfront.
- For auto-archiving steps, execute directly. For manual steps, give exact copy-paste instructions.
- Output MUST be rendered directly in the chat — NO triple-backtick code block wrapping.

---

## Execution Protocol

When triggered, output the following directly in the chat:

#############
🗄️ PROTOCOLE D'ARCHIVAGE
#############

**Avant de commencer — titre suggéré pour cette session :**

> 📋 **COPIER-COLLER CE TITRE** (tu le renommeras à l'étape 3) :
>
> `[[ [DOMAINE] Sujet principal — Résultat ou décision clé (YYYY-MM-DD) (archived) ]]`

*(Générer le titre selon le contenu réel de la session. Format : domaine entre crochets, sujet dense, date du jour.)*

---

==============
ÉTAPE 1 — EXPORT NOTION (Manuel)
==============

🔌 **Via l'extension Chrome "ChatGPT to Notion"**

1. Ouvre la conversation dans le navigateur web (Manus web app)
2. Clique sur l'icône de l'extension **ChatGPT to Notion** dans la barre Chrome
3. Sélectionne la base de données Notion cible (ex : `Sessions Y-OS`)
4. Lance l'export — attends la confirmation de l'extension

✅ Une fois l'export confirmé par l'extension → réponds **"ok"** pour passer à l'étape 2.

---

==============
ÉTAPE 2 — MARQUEUR DE FIN (Manuel)
==============

📌 **Ajoute ce marqueur en toute fin de cette conversation** (copier-coller) :

`####### ARCHIVED #######`

*(Saut de ligne avant et après. Ce marqueur signale visuellement que la session est close.)*

✅ Une fois le marqueur ajouté → réponds **"ok"** pour passer à l'étape 3.

---

==============
ÉTAPE 3 — RENOMMAGE DU TITRE (Manuel)
==============

✏️ **Renomme manuellement le titre de cette session** avec le titre suggéré en haut de ce protocole.

Format attendu : `[[ [DOMAINE] Sujet — Résultat clé (YYYY-MM-DD) (archived) ]]`

*(Dans Manus : clique sur le titre de la session → modifie → valide.)*

✅ Une fois renommé → réponds **"ok"** pour passer à l'étape 4.

---

==============
ÉTAPE 4 — ARCHIVAGE SYSTÈME (Auto)
==============

🤖 Manus exécute automatiquement après confirmation de l'étape 3.

**Type Knowledge Source** :
1. Lire le template `/home/ubuntu/skills/summary/templates/exec_summary.md`
2. Générer et sauvegarder `/home/ubuntu/exec_summary_{session_id}.md`
3. Lancer : `python3.11 /home/ubuntu/yos/mmm/scripts/yos_archive_pipeline.py --session-text "$(cat /home/ubuntu/exec_summary_{session_id}.md)" --title "[Titre]"`

**Type Tâche Terminée** :
1. Générer le JSON : `cat current_conversation.txt | python3 /home/ubuntu/skills/summary/scripts/generate_summary.py > summary_data.json`
2. Lancer : `python /home/ubuntu/skills/memory-manager/scripts/archive_conversation.py summary_data.json`

---

Une fois l'étape 4 complétée, confirmer à l'utilisateur :

#############
✅ SESSION ARCHIVÉE
#############
- 📄 Export Notion : confirmé (étape 1)
- 🏷️ Marqueur de fin : apposé (étape 2)
- ✏️ Titre renommé : [[ titre ]] (étape 3)
- 🤖 Archivage système : exécuté (étape 4)

## Tone
Direct. Calm. Precise. French unless session is in another language.
