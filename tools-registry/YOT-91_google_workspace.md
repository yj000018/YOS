---
tool_id: YOT-91
tool_name: "Google Workspace"
tool_type: "MCP Connector"
category: "Productivity Suite"
status: "Production"
pricing: "Paid"
source_type: "Officiel"
source_url: "https://developers.google.com/workspace"
auth_credentials: "OAuth"
tags: ["google", "workspace", "drive", "docs", "sheets", "slides", "productivity"]
created_date: "2026-08-07"
---
# 🟢 YOT-91 — Google Workspace
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Productivity Suite |
| **Statut** | Production |
| **Pricing** | Paid |
| **Source** | Officiel |
| **Auth** | OAuth |
| **URL** | https://developers.google.com/workspace |
## Business Value
Intègre l'écosystème Google Workspace directement dans Y-OS, permettant l'automatisation et la gestion fluide des documents, feuilles de calcul et présentations. Cela accélère considérablement les flux de travail collaboratifs et la gestion de l'information.
## Capabilities
- Accès et gestion de Google Drive (fichiers, dossiers)
- Création et édition de Google Docs
- Manipulation de données dans Google Sheets
- Génération et modification de Google Slides
- Interaction via l'interface en ligne de commande `gws`
## Dependencies
- Compte Google Workspace actif
- Authentification OAuth configurée
- CLI `gws` installé et configuré
## Known Limits & Bugs
- Les limites de quota de l'API Google Workspace s'appliquent.
- Certaines fonctionnalités avancées de formatage peuvent ne pas être entièrement supportées via l'API.
## Workarounds & Lessons
- Utiliser `rclone` comme solution de repli pour la synchronisation en masse ou le téléchargement/téléversement de fichiers binaires volumineux.
- Toujours vérifier les permissions OAuth si l'accès à certains fichiers est refusé.
