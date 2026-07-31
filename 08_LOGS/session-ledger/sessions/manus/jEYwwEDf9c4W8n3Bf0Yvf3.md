---
id: "jEYwwEDf9c4W8n3Bf0Yvf3"
title: "Ajouter un dossier à 'Mon Ordinateur' dans Manus"
date: "2026-07-05"
importance: "3"
depth_score: "standard"
projects: ["Y-OS", "Manus"]
tags: ["gestion de fichiers", "accès local", "Mac", "filesystem", "configuration", "Mac Bridge"]
summary: ""
executive_summary: "The user inquired about Manus's access to their Mac. The assistant confirmed existing access, listed already exposed folders, and provided clear instructions on how to add new local folders, explaining the underlying mechanism and potential uses."
context_and_intent: "The user's intent was to understand if Manus had access to their Mac and implicitly, how to manage or add folders. They were likely trying to add a new folder or confirm existing setup."
what_was_done: "The assistant analyzed the user's current Manus configuration, identified existing Mac access and exposed folders, provided step-by-step instructions to add a new local folder, explained the technical mechanism (Mac Bridge), and outlined potential actions Manus could perform with these folders."
outputs_produced: [{"description": "Assistant confirmed that the user's MacBook-Air-7.local was connected with filesystem access.", "name": "Confirmation of existing Mac access", "type": "Information"}, {"description": "Provided a list of folders Manus already had access to, including root, Desktop, Documents, Downloads, yannickjolliet, CloudMounter-OneDrive4, CloudMounter-pCLOUD, and TO BE OUT-STORED.", "name": "List of exposed folders", "type": "Information"}, {"description": "Step-by-step guide on how to add a new local folder in Manus ('+ Add local folder' -> select folder).", "name": "Instructions for adding a local folder", "type": "Guide"}, {"description": "Clarified how Manus accesses folders via the Mac Bridge (skill `yos-mac-bridge`) or if mounted in the sandbox.", "name": "Explanation of access mechanism", "type": "Information"}, {"description": "Listed actions Manus can perform with accessible folders: read, write, index, or automate.", "name": "Capabilities list", "type": "Information"}]
key_decisions: ["The assistant implicitly decided to provide both confirmation of the existing setup and instructions for adding new folders, anticipating the user's likely next step."]
lessons_learned: {"discoveries": ["Manus can detect and list already configured filesystem access and exposed folders.", "Manus accesses local folders via a 'Mac Bridge' (skill `yos-mac-bridge`) or if the folder is mounted in the sandbox."], "failed_or_suboptimal": ["The user's second message 'c' indicates a potential break in communication or an incomplete thought, suggesting the conversation might have ended prematurely or with an unresolved user intent."], "worked_well": ["The assistant quickly understood the user's implicit need despite a vague initial prompt.", "The assistant provided relevant context by confirming existing setup and listing accessible folders.", "The assistant gave clear, actionable, step-by-step instructions for adding new local folders.", "The explanation of Manus's capabilities with accessible folders (read, write, index, automate) was helpful."]}
challenges_and_blockers: ["The user's initial prompt was a question about access, indicating a potential lack of clarity on their part regarding Manus's capabilities or interface.", "The second user message 'c' is incomplete, suggesting a potential communication issue or interruption."]
open_questions: ["\"Quel dossier tu veux utiliser pour quoi ?\" (What folder do you want to use for what purpose?) - This question from the assistant remains unanswered in the transcript."]
next_steps: ["The user needs to follow the provided instructions to add a new folder.", "The user needs to specify their exact use case for the folders, as prompted by the assistant's open question."]
url: "https://manus.im/app/task/jEYwwEDf9c4W8n3Bf0Yvf3"
---

# Ajouter un dossier à "Mon Ordinateur" dans Manus

| Field | Value |
|-------|-------|
| **Session ID** | `jEYwwEDf9c4W8n3Bf0Yvf3` |
| **Date** | 2026-07-05 10:52 UTC |
| **Project** | Gz25LHGt5xFF4hEghRYUQL |
| **URL** | [https://manus.im/app/sessions/jEYwwEDf9c4W8n3Bf0Yvf3](https://manus.im/app/sessions/jEYwwEDf9c4W8n3Bf0Yvf3) |
| **Messages** | 2 user · 2 assistant · 8 total |

## Initial Prompt

maiSsi manus a acces a mon mac!

## First Response

## Vu — tu as déjà tout configuré 👀

Je vois dans ton screenshot :

- **MacBook-Air-7.local** connecté avec accès filesystem
- Dossiers déjà exposés : `/`, Desktop, Documents, Downloads, yannickjolliet, CloudMounter-OneDrive4, CloudMounter-pCLOUD, TO BE OUT-STORED

### Pour ajouter un nouveau dossier local

Clique sur **"+ Add local folder"** en haut du menu → sélectionne le dossier sur ton Mac → il apparaît dans la liste.

C'est tout. Manus y accède ensuite via le **Mac Bridge** (skill `yos-mac-bridge`) ou directement si le dossier est monté dans le sandbox.

---

### Ce que je peux faire avec ces dossiers

| Dossier visible | Usage possible |
|---|---|
| `/` (root) | Accès complet au filesystem Mac |
| `TO BE OUT-STORED` | Archivage, tri, migration |
| `CloudMounter-*` | OneDrive, pCLOUD via mount |
| `Desktop / Documents` | Fichiers courants |

**Quel dossier tu veux utiliser pour quoi ?** Je peux lire, écrire, indexer, ou automatiser dessus.

## Conversation Summary

> **User:** maiSsi manus a acces a mon mac!

> **User:** comment ajouter un dossier/local drive dans "my computer" dans manus pour donenr acces a manus

> **Manus:** ## Vu — tu as déjà tout configuré 👀

Je vois dans ton screenshot :

- **MacBook-Air-7.local** connecté avec accès filesystem
- Dossiers déjà exposés : `/`, Desktop, Documents, Downloads, yannickjolliet, CloudMounter-OneDrive4, CloudMounter-pCLOUD, TO BE OUT-STORED

### Pour ajouter un nouveau dossier local

Clique sur **"+ Add local folder"** en haut du menu → sélectionne le dossier sur ton Mac → il apparaît dans la liste.

C'est tout. Manus y accède ensuite via le **Mac Bridge** (skill `yos-mac-bridge`) ou directement si le dossier est monté dans le sandbox.

---

### Ce que je peux faire avec ces dossiers

| Dossier visible | Usage possible |
|---|---|
| `/` (root) | Accès complet au filesystem Mac |
| `TO BE OUT-STORED` | Archivage, tri, migration |
| `CloudMounter-*` | OneDrive, pCLOUD...

> **Manus:** ## Accès fichiers locaux dans Manus — État des lieux

**Réponse directe : ce n'est pas possible nativement aujourd'hui.**

Manus tourne dans un sandbox cloud isolé — il n'a pas accès direct à ton système de fichiers local (Mac/PC). Voici les options réelles :

---

### 🗂️ Ce qui existe dans "My Computer" (sandbox Manus)

Le sandbox Manus a son propre filesystem à `/home/ubuntu/`. C'est un disque éphémère cloud, **pas** ton disque local.

---

### ✅ Options pour donner accès à tes fichiers locaux

| Option | Méthode | Effort | Persistance |
|---|---|---|---|
| **1. Upload manuel** | Glisser-déposer dans le chat | Faible | Session uniquement |
| **2. Google Drive** | Connecteur GWS intégré (`gws` CLI + rclone) | Faible | ✅ Permanent |
| **3. GitHub** | Repo clonable via `gh` CLI | Moyen | ✅ ...

## Full Verbatim

<details>
<summary>Expand full conversation (4 messages)</summary>

**[1783248779886] MANUS:** ## Vu — tu as déjà tout configuré 👀

Je vois dans ton screenshot :

- **MacBook-Air-7.local** connecté avec accès filesystem
- Dossiers déjà exposés : `/`, Desktop, Documents, Downloads, yannickjolliet, CloudMounter-OneDrive4, CloudMounter-pCLOUD, TO BE OUT-STORED

### Pour ajouter un nouveau dossier local

Clique sur **"+ Add local folder"** en haut du menu → sélectionne le dossier sur ton Mac → il apparaît dans la liste.

C'est tout. Manus y accède ensuite via le **Mac Bridge** (skill `yos-mac-bridge`) ou directement si le dossier est monté dans le sandbox.

---

### Ce que je peux faire avec ces dossiers

| Dossier visible | Usage possible |
|---|---|
| `/` (root) | Accès complet au filesystem Mac |
| `TO BE OUT-STORED` | Archivage, tri, migration |
| `CloudMounter-*` | OneDrive, pCLOUD via mount |
| `Desktop / Documents` | Fichiers courants |

**Quel dossier tu veux utiliser pour quoi ?** Je peux lire, écrire, indexer, ou automatiser dessus.
**[1783248769224] USER:** maiSsi manus a acces a mon mac!
**[1783248747556] MANUS:** ## Accès fichiers locaux dans Manus — État des lieux

**Réponse directe : ce n'est pas possible nativement aujourd'hui.**

Manus tourne dans un sandbox cloud isolé — il n'a pas accès direct à ton système de fichiers local (Mac/PC). Voici les options réelles :

---

### 🗂️ Ce qui existe dans "My Computer" (sandbox Manus)

Le sandbox Manus a son propre filesystem à `/home/ubuntu/`. C'est un disque éphémère cloud, **pas** ton disque local.

---

### ✅ Options pour donner accès à tes fichiers locaux

| Option | Méthode | Effort | Persistance |
|---|---|---|---|
| **1. Upload manuel** | Glisser-déposer dans le chat | Faible | Session uniquement |
| **2. Google Drive** | Connecteur GWS intégré (`gws` CLI + rclone) | Faible | ✅ Permanent |
| **3. GitHub** | Repo clonable via `gh` CLI | Moyen | ✅ Permanent |
| **4. Dropbox MCP** | Connecteur Dropbox activé | Faible | ✅ Permanent |
| **5. NAS/SMB via tunnel** | bore.pub + SSH depuis ton Mac | Élevé | Manuel |
| **6. My Browser** | Accès aux ses...
**[1783248730153] USER:** comment ajouter un dossier/local drive dans "my computer" dans manus pour donenr acces a manus



</details>