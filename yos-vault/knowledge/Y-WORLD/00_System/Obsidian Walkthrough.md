# Y-WORLD — Obsidian Walkthrough
### Guide complet pour débutant · Vault déjà déployé

---

## 0. Situation de départ

Ton vault Y-WORLD est **déjà prêt** sur ton Mac :
- 📁 `/Users/yannickjolliet/Y-WORLD/` — 62 fichiers, 20 dossiers
- ⚙️ Tous les plugins configurés (Dataview, Templater, QuickAdd, Tasks, Linter)
- 🎨 Thème, fonts, couleurs, hotkeys — tout écrit dans `.obsidian/`
- 🐙 Repo GitHub privé créé et synchronisé : `github.com/yj000018/Y-WORLD`

**Ce que tu dois faire** : ouvrir Obsidian et activer 2 choses.

---

## ÉTAPE 1 — Ouvrir le vault Y-WORLD

1. Lance **Obsidian**
2. Sur l'écran de démarrage → **"Open folder as vault"**
3. Navigue vers `/Users/yannickjolliet/Y-WORLD`
4. Clique **Open**

✅ Tu devrais voir `HOME.md` s'ouvrir automatiquement.

---

## ÉTAPE 2 — Activer les plugins communautaires

> Obsidian bloque les plugins tiers par défaut pour la sécurité.

1. `Cmd + ,` → **Settings**
2. Colonne gauche → **Community Plugins**
3. Clique **"Turn on community plugins"**
4. Clique **"Turn on"** dans la popup de confirmation

✅ Les 5 plugins déjà installés (Dataview, Templater, QuickAdd, Tasks, Linter) s'activent automatiquement.

---

## ÉTAPE 3 — Installer le thème Minimal

> Le thème définit l'apparence visuelle du vault.

1. `Cmd + ,` → **Appearance**
2. Section **Themes** → clique **"Manage"**
3. Dans la barre de recherche → tape `Minimal`
4. Clique **Install and use**

✅ Le vault passe en dark mode avec la palette indigo Y-WORLD.

---

## ÉTAPE 4 — Installer Obsidian Git

> Obsidian Git = backup automatique vers GitHub toutes les 60 minutes.

**Pourquoi tu ne le trouves pas** : le plugin s'appelle exactement **"Git"** dans le store (pas "Obsidian Git").

1. `Cmd + ,` → **Community Plugins** → **Browse**
2. Cherche : `Git` (juste "Git", pas "Obsidian Git")
3. Le plugin de **Vinzent03** → **Install** → **Enable**
4. Retourne dans **Community Plugins** → clique l'icône ⚙️ à droite de **Git**
5. Configure :
   - **Username** : `yj000018`
   - **Password/Token** : `REDACTED_GITHUB_PAT`
   - **Auto backup interval** : `60` (minutes)
   - **Auto backup after stop editing** : ON
   - **Pull updates on startup** : ON
   - **Push on backup** : ON

✅ Le vault se sauvegarde automatiquement sur GitHub toutes les heures.

---

## COMPRENDRE LA VALEUR — Ce que tu as maintenant

---

### 🗂️ La structure de dossiers

```
Y-WORLD/
├── 00_System/      ← Principes, config, règles du système
├── 01_Cockpit/     ← HOME.md, surfaces de travail quotidiennes
├── 02_Maps/        ← Cartes spatiales de chaque région
├── 03_Dashboards/  ← Tableaux de bord dynamiques
├── 04_Templates/   ← Modèles de notes (K-Card, Projet, etc.)
├── 05_Registries/  ← Registres d'outils et plugins
├── 06_Workflows/   ← Registre des automatisations
├── 07_Agent_Operations/ ← Manuel Manus, queue de tâches
├── 10_Inbox/       ← Zone de capture rapide (tout atterrit ici)
├── 20_Life/        ← Santé, routines, finances, voyages
├── 30_Knowledge/   ← Base de connaissance
├── 40_K-Cards/     ← Cartes de connaissance atomiques
├── 50_Projects/    ← Projets actifs, pausés, futurs
├── 60_Y-OS/        ← Couche cognitive AI
├── 70_CasaTAO/     ← Maison intelligente Sicile
├── 71_ARC_Anandaz/ ← Chalet Suisse
├── 80_Archetypes/  ← Grammaire symbolique universelle
├── 81_Y-Publishing/← Livres, produits de connaissance
├── 90_Reality_Interfaces/ ← Web, mobile, Y-WORLD.net
└── 99_Archive/     ← Projets terminés, archives
```

**Principe** : chaque dossier = une région de ta vie. Rien n'est perdu, tout est navigable.

---

### 🔌 La valeur de chaque plugin

| Plugin | Ce qu'il fait concrètement | Exemple d'usage |
| :--- | :--- | :--- |
| **Dataview** | Requêtes dynamiques sur tes notes (comme SQL sur markdown) | `03_Dashboards/Y-WORLD Dashboard.md` liste automatiquement tous tes projets actifs |
| **Templater** | Crée des notes avec des champs pré-remplis (date, domaine, etc.) | Quand tu crées une K-Card, le frontmatter YAML est automatiquement rempli |
| **QuickAdd** | Raccourcis clavier pour créer des notes au bon endroit | `Alt+K` → popup → tape le titre → K-Card créée dans `40_K-Cards/` |
| **Tasks** | Agrège toutes tes tâches `- [ ]` de tout le vault en un seul endroit | `03_Dashboards/Projects Dashboard.md` peut montrer toutes les tâches ouvertes |
| **Linter** | Formate automatiquement le YAML et le markdown à la sauvegarde | Pas de notes mal formatées, métadonnées toujours propres |
| **Obsidian Git** | Backup automatique sur GitHub | Toutes les 60 min, commit + push silencieux |

---

### 🗺️ La valeur des Maps

Ouvre `02_Maps/Y-WORLD ROOT MAP.md`.

Tu vois un diagramme Mermaid. C'est la **carte de contrôle spatiale** de Y-WORLD.

**Principe** : chaque nœud de la carte est un lien vers un vrai fichier. La carte n'est pas décorative — c'est une surface de navigation.

> Map node → Dashboard → Dossier → K-Cards → Workflows → Agents

---

### 📊 La valeur des Dashboards

Ouvre `03_Dashboards/Y-WORLD Dashboard.md`.

Tu vois des blocs `dataview`. Quand Dataview est activé, ces blocs deviennent des **tableaux dynamiques** qui lisent automatiquement les métadonnées de tes notes.

**Exemple** : le bloc suivant liste tous tes projets actifs en temps réel :
```
TABLE status, priority, review_date
FROM "50_Projects"
WHERE status = "active"
SORT priority DESC
```

Chaque fois que tu mets `status: active` dans un projet, il apparaît automatiquement dans le dashboard.

---

### 📋 La valeur des Templates

Ouvre `04_Templates/Template - K-Card.md`.

C'est le modèle d'une **K-Card** (Knowledge Card) — l'unité atomique de connaissance de Y-WORLD.

**Comment l'utiliser** :
1. Appuie `Alt+K`
2. Tape le titre de ta connaissance (ex: "Cognitive OS")
3. La note est créée dans `40_K-Cards/` avec tout le frontmatter pré-rempli
4. Tu remplis : Summary, Key Ideas, Use Cases, Related Nodes

**Valeur** : chaque K-Card est indexée, requêtable, linkable. En 6 mois tu as un graphe de connaissance vivant.

---

### 🔗 La valeur du Graph View

`Cmd + Shift + G` → **Graph View**

C'est la visualisation de tous les liens entre tes notes. Plus tu crées des liens (`[[nom de note]]`), plus le graphe devient riche et navigable.

Les couleurs que j'ai configurées :
- 🟢 **Vert** : System + Cockpit + Y-OS (infrastructure)
- ⚪ **Blanc** : Maps (orientation)
- 🔵 **Bleu** : Dashboards + K-Cards (connaissance)
- 🟠 **Orange** : Projects (exécution)

---

### ⌨️ Les raccourcis clavier actifs

| Raccourci | Action |
| :--- | :--- |
| `Alt + K` | Créer une K-Card dans `40_K-Cards/` |
| `Alt + P` | Créer un Projet dans `50_Projects/` |
| `Alt + N` | Créer un Daily Note dans `10_Inbox/` |
| `Cmd + Shift + G` | Ouvrir le Graph View |
| `Cmd + Shift + L` | Linter (formater la note active) |
| `Cmd + O` | Quick Switcher (naviguer entre notes) |
| `Cmd + P` | Command Palette (toutes les commandes) |
| `Cmd + ,` | Settings |

---

## WORKFLOW QUOTIDIEN RECOMMANDÉ

### Matin (2 min)
1. Ouvre Obsidian → `HOME.md` s'ouvre automatiquement
2. `Alt+N` → crée le Daily Note du jour
3. Définis 3 focus items

### Pendant la journée
- Capture rapide : toute idée → `10_Inbox/` (nouveau fichier)
- Connaissance importante → `Alt+K` → K-Card
- Nouveau projet → `Alt+P` → Project Note

### Soir (5 min)
- Vide l'Inbox : classe les notes capturées dans les bons dossiers
- Complète les tâches du Daily Note
- Git auto-backup s'est déjà fait tout seul

---

## PROCHAINES ÉTAPES (dans l'ordre)

1. ✅ Ouvrir le vault + activer community plugins
2. ✅ Installer thème Minimal
3. ✅ Installer plugin Git (chercher "Git" pas "Obsidian Git")
4. 🔜 Créer ta première K-Card (`Alt+K`)
5. 🔜 Créer ton premier projet (`Alt+P`)
6. 🔜 Explorer le Graph View (`Cmd+Shift+G`)
7. 🔜 Ouvrir `03_Dashboards/Y-WORLD Dashboard.md` et voir Dataview en action

---

## RÉSUMÉ EN UNE PHRASE

> Obsidian est ton cerveau externe. Y-WORLD est la structure de ce cerveau. Les plugins sont les neurones qui le font penser automatiquement.
