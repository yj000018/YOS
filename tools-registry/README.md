---
title: Y-OS Tools Registry v2
last_updated: 2026-07-30
migrated_from: Notion (85f89b4e847d4cbea9310ffdf11b60f2)
source_of_truth: Git
---

# Y-OS Tools Registry v2

Registre canonique de tous les outils Y-OS. Source de vérité : ce repo Git.

> **Règle** : Tout nouvel outil découvert ou toute mise à jour de capacité → créer/mettre à jour le fichier `.md` correspondant ici. Ne jamais créer de contenu dans Notion.

## Index des fiches

| Tool ID | Nom | Catégorie | Statut | Fichier |
| :--- | :--- | :--- | :---: | :--- |
| YOT-71 | Raindrop.io | Memory / Knowledge | Production | [YOT-71_raindrop.md](./YOT-71_raindrop.md) |
| YOT-72 | MyMind | Design / Visual | Experimental | [YOT-72_mymind.md](./YOT-72_mymind.md) |
| YOT-73 | Pinterest | Design / Visual | À tester | [YOT-73_pinterest.md](./YOT-73_pinterest.md) |

## Convention de nommage

```
YOT-{id}_{slug}.md
```

- `YOT` = Y-OS Tool
- `{id}` = numéro séquentiel (prochain : YOT-74)
- `{slug}` = nom court en minuscules

## Frontmatter obligatoire

```yaml
---
tool_id: YOT-XX
tool_name: Nom de l'outil
tool_type: MCP Connector | API | App | CLI | ...
category: Memory / Knowledge | Design / Visual | Automation | ...
status: Production | Experimental | A tester | Décommissionné
pricing: Gratuit | Freemium | Payant
source_type: Officiel | Communauté | Interne
source_url: https://...
auth_credentials: OAuth | API Key | Session Cookie | ...
last_updated: YYYY-MM-DD
---
```

## Workflow de mise à jour

1. Nouvel outil découvert → créer `YOT-{n+1}_{slug}.md`
2. Nouvelle capacité API/MCP → mettre à jour la fiche existante
3. Outil décommissionné → changer `status: Décommissionné` + noter la raison
4. Commit message : `tools: update YOT-XX {nom} — {raison}`

## Migration Notion

Ce registry a été migré depuis Notion le 2026-07-30.
Pages Notion d'origine (à supprimer après validation) :
- Tools Registry v2 DB : `https://app.notion.com/p/85f89b4e847d4cbea9310ffdf11b60f2`
- Raindrop.io : `https://app.notion.com/p/3ac35e218cf881ff9760c45639a157b7`
- MyMind : `https://app.notion.com/p/3ac35e218cf881ec8ed5cfe9a3aa3ee6`
- Pinterest : `https://app.notion.com/p/3ac35e218cf8816288fef6ab13a7580c`
