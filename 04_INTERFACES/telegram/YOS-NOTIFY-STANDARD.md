# Y-OS Notification Standard (`yos-notify`)
> **Statut** : Actif
> **Date** : 2026-08-05
> **Contexte** : Règle Canon #4 (Telegram = surface d'interaction universelle)

## Objectif
Permettre à n'importe quel script, tâche cron, ou LLM (Manus, ChatGPT, Claude) opérant sur le Cloud Computer d'envoyer des notifications standardisées à Yannick via Telegram, sans avoir à manipuler des tokens API.

## Implémentation
L'utilitaire `yos-notify` est installé globalement sur le Cloud Computer (`/usr/local/bin/yos-notify`). Il encapsule l'appel API Telegram et le formatage Y-OS.

### Usage CLI (Scripts / Cron / Manus)

```bash
# Message simple
yos-notify "Tâche terminée avec succès"

# Avec source spécifiée (Recommandé)
yos-notify "Le debloat de la Tab S11 est terminé" --source "Manus"
yos-notify "Night pipeline terminé" --source "Cron"
yos-notify "Nouvelle PR détectée" --source "GitHub Monitor"

# Avec sauts de ligne
yos-notify "Erreur critique:\n- Serveur down\n- DB inaccessible" --source "Watchdog"
```

### Usage Python

```python
import subprocess

def notify_yannick(message, source="Script"):
    subprocess.run(["yos-notify", message, "--source", source])
```

## Formatage Automatique
L'utilitaire formate automatiquement le message avec le header standard Y-OS :
```
🤖 <b>[Source]</b>

[Message]
```
Il gère également l'échappement HTML requis par l'API Telegram.
