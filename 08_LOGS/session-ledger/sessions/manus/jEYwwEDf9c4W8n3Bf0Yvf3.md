---
session_id: jEYwwEDf9c4W8n3Bf0Yvf3
title: "Ajouter un dossier à 'Mon Ordinateur' dans Manus"
date: 2026-07-05 10:52 UTC
url: https://manus.im/app/sessions/jEYwwEDf9c4W8n3Bf0Yvf3
project_id: Gz25LHGt5xFF4hEghRYUQL
user_messages: 2
assistant_messages: 2
total_messages: 8
processed: true
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
