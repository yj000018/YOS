# Tool Fact Sheet: Telegram Bot

## 1. Identité de l'Outil
- **Nom** : Telegram Bot API
- **Type** : Plateforme de messagerie / API
- **Rôle Y-OS** : Surface d'interaction universelle et notifications push multi-plateformes
- **Statut** : Standard Canonique (Règle Canon #4)

## 2. Cas d'Usage
- Envoyer des notifications push en temps réel à l'utilisateur (iOS, Android, Mac, PC).
- Informer du démarrage, du succès ou de l'échec des processus Y-OS (ex: MacLock).
- Canal d'interaction bidirectionnelle : permettre à l'utilisateur d'envoyer des commandes (ex: `/status`, `/stop`, `/approve`) pour contrôler Y-OS à distance.

## 3. Architecture & Intégration Y-OS
Le bot Telegram est le point d'entrée unique pour toutes les notifications sortantes de Y-OS, remplaçant les solutions comme ntfy.sh.

- **Bot Username** : `@yos_notif_bot`
- **Display Name** : "Y-OS Notifications"
- **Canal** : Chat direct avec Yannick (chat_id: `223132272`)
- **Stockage Token** : 1Password MAIN VAULT → `Telegram Bot — yOS-TELEGRAM-2026-03` (champ `credential`)

### Méthodes d'Envoi
L'API Telegram est simple et peut être appelée depuis n'importe quel nœud (Sandbox, CC, N100, Mac).

**Via cURL (Universel) :**
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage" \
     -d "chat_id=223132272&text=Hello&parse_mode=HTML"
```

**Via Python (`yos_lock.py`) :**
Le module `yos_lock.py` intègre nativement l'envoi de notifications lors de l'acquisition et de la libération d'un verrou Mac.
```python
from yos_lock import MacLock

# Envoie une notif au démarrage, et une notif silencieuse à la fin
with MacLock("Tâche", notify=True):
    pass
```

**Envoi standalone (CLI) :**
```bash
python3 /tmp/yos_lock.py notify "Message personnalisé"
```

## 4. Configuration & Déploiement

### Récupération du Token
Le token n'est jamais hardcodé dans les scripts publics. Il doit être récupéré via 1Password CLI ou injecté via les secrets de l'environnement Manus.

### Formatage des Messages
Y-OS utilise le `parse_mode=HTML` pour formater les messages.
- Utiliser `<b>` pour le gras, `<i>` pour l'italique.
- Inclure des émojis fonctionnels (✅, ❌, 🔒, ⚠️) pour une lecture rapide.

## 5. Limitations & Contraintes
- **Dépendance Cloud** : Nécessite un accès internet et dépend de l'infrastructure de Telegram (non self-hostable).
- **Sécurité** : Les messages transitent par les serveurs Telegram. Ne pas envoyer de données hautement sensibles (mots de passe en clair, clés privées) via ce canal.

## 6. Décisions Stratégiques Associées
- **Telegram vs ntfy.sh** : Telegram a été choisi car il permet une interaction bidirectionnelle (l'utilisateur peut répondre), contrairement à ntfy.sh qui est unidirectionnel. De plus, Telegram est déjà installé sur tous les appareils de l'utilisateur, réduisant la friction d'adoption. ntfy.sh a été éliminé.
- **Complémentarité xbar** : Telegram gère les notifications push volatiles et l'interaction, tandis que xbar gère l'état permanent visible sur le Mac.

## References
[1] AGENTS.md - Règle Canon #4 (Y-OS Notification & Interaction Stack)
