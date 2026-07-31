# Validation Prod — yos_memory (Git + Mem0)

Ce guide permet de valider le premier run réel du pipeline LMP v2 avec la nouvelle architecture mémoire `yos_memory` (Git + Mem0).

## Étape 1 : Installation des dépendances

Sur ton environnement principal (Mac ou N100) :

```bash
# Aller dans le repo YOS
cd /chemin/vers/YOS/yos-automations/scripts/yos-llm-pipeline

# Installer le SDK officiel Mem0
pip install mem0ai pyyaml
```

## Étape 2 : Configuration de l'environnement

Ajoute ces variables dans ton `.zshrc` ou `.bashrc` :

```bash
# Activer le miroir Git + Mem0 (pipeline_adapter)
export YOS_MEMORY_ADAPTER=1

# Configurer Mem0
export MEM0_API_KEY="m0-..."

# Indiquer le chemin du repo YOS (pour les écritures Git)
export YOS_MEMORY_GIT_REPO="/chemin/vers/YOS"
```

Recharge le shell : `source ~/.zshrc`

## Étape 3 : Exécution du premier run réel

Lance le pipeline normalement :

```bash
./run_pipeline.sh
```

## Étape 4 : Vérification des logs

Le pipeline doit afficher les logs habituels, **plus** les nouveaux logs de l'adapter :

```text
[yos_memory] YOS_MEMORY_ADAPTER is active.
...
[yos_memory] Session MPX-xxx archived to Git: /chemin/vers/YOS/00_META/SESSIONS/2026-07/MPX-xxx.md
[yos_memory] Session MPX-xxx pushed to Mem0 (event_id: ...)
```

## Étape 5 : Vérification des données

1. **Git** : Vérifie que le fichier Markdown a bien été créé dans `YOS/00_META/SESSIONS/2026-07/`.
2. **Mem0** : Vérifie le dashboard Mem0 (ou via API) que la mémoire a bien été ajoutée pour `user_id="yannick"`.
3. **Notion** : Vérifie que la page a bien été créée dans Notion (l'adapter est non-destructif, Notion continue de fonctionner en parallèle jusqu'à ce qu'on le débranche).

Si les 3 sont OK, l'architecture est validée en production ! 🎉
