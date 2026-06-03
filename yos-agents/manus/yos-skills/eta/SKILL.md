---
name: eta
description: Estimated Time of Arrival — analyse toutes les tâches en cours dans la session et produit une estimation en minutes + heure de fin pour chaque tâche et pour l'ensemble. Utiliser quand l'utilisateur demande "ETA", "combien de temps", "à quelle heure tu finis", "time estimate", "quand c'est prêt", ou veut savoir quand les tâches en cours seront terminées.
---

# ETA Skill

Génère une estimation temporelle structurée de toutes les tâches en cours ou pending dans la session.

## Workflow

### 1. Extraire les tâches

Lire le plan de tâches actuel (task_plan) et identifier :
- Toutes les phases **pending** et **in_progress**
- Leur complexité estimée selon la grille ci-dessous

### 2. Mapper la complexité

| Complexité | Minutes | Exemples |
|------------|---------|----------|
| `low` | 2 min | Edit simple, recherche rapide, checkpoint |
| `medium` | 8 min | Modification multi-fichiers, recherche modérée, archivage Notion |
| `high` | 20 min | Réécriture composant, build complexe, génération CMS |
| `xl` | 45 min | Feature complète, refactor multi-fichiers, pipeline complet |

### 3. Générer l'estimation via le script

Construire un JSON des tâches et passer au script :

```bash
echo '[{"name": "...", "complexity": "high", "status": "in_progress"}, ...]' \
  | python3 /home/ubuntu/skills/eta/scripts/estimate.py
```

Statuts valides : `pending`, `in_progress`, `done`

### 4. Présenter le résultat

Afficher la sortie du script directement dans le chat. Format :

```
⏱ ETA — généré à 14:32

  🔄 Tâche A  [high · 20min]  → 14:52
  ⏳ Tâche B  [medium · 8min]  → 15:00
  ✅ Tâche C  (done)

📍 Total : 28 min — Fin estimée : 15:00
```

## Règles

- Baser l'estimation sur le plan de tâches réel de la session, jamais sur une liste inventée.
- Les tâches `done` s'affichent avec ✅ et 0 min.
- L'heure de fin est calculée depuis `datetime.now()` — toujours à jour.
- Si aucune tâche active : indiquer "Aucune tâche en cours."
- Ne pas calculer mentalement — toujours utiliser le script.
