# SKILL: yos-notif

## Description
Module standard Y-OS pour l'envoi de notifications à l'utilisateur.
Utilise Telegram (`@yos_notif_bot`) comme canal unique de notification push.

## Implémentation du Y-OS Module Standard

### 1. Architecture & Rôle
- **Objectif** : Fournir une interface unique pour envoyer des messages à Yannick depuis n'importe quel nœud.
- **Périmètre** : Ne gère que l'envoi (push). La réception de commandes est gérée par un autre composant.
- **Dépendances** : Accès internet (API Telegram).

### 2. Exécution & Code-Interface
- **Auto-launch** : Appelé automatiquement par `yos_lock.py` (MacLock) et via l'AUTO-TRIGGER du Kernel.
- **On-request** : Utilisable dans tout script Python via `from yos_notif import send_notif`.
- **Manuel** : `python3 yos_notif.py "Mon message" SUCCESS`

### 3. Interfaces
- **Entrées** : Appels de fonctions Python ou CLI.
- **Sorties** : API Telegram (`api.telegram.org`).

### 4. Référentiels
- **Code source** : `04_INTERFACES/telegram/yos_notif.py`
- **Secrets** : Token stocké dans 1Password (`yOS-TELEGRAM-2026-03`).

### 5. Maintenance
- Si le token change, mettre à jour 1Password ET `yos_notif.py`.

### 6. Logs
- Affiche les erreurs sur `stdout` (`[YOS NOTIF] Erreur...`).

## Comment utiliser ce skill
1. Importer la fonction dans tes scripts Python :
   ```python
   import sys
   sys.path.append('/home/ubuntu/yos/github_yos/04_INTERFACES/telegram')
   from yos_notif import send_notif, NotifLevel

   send_notif("Tâche terminée", level=NotifLevel.SUCCESS, title="Backup")
   ```
2. Si tu as besoin d'informer l'utilisateur d'un événement asynchrone ou d'une fin de traitement long, utilise ce module plutôt que d'attendre dans le chat.
