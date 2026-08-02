# Tool Fact Sheet: xbar

## 1. Identité de l'Outil
- **Nom** : xbar
- **Type** : Utilitaire macOS (Barre de menu)
- **Rôle Y-OS** : Indicateur visuel permanent pour les processus actifs sur le Mac (Mac Lock)
- **Statut** : Standard Canonique (Règle Canon #4)

## 2. Cas d'Usage
- Afficher l'état d'activité de Y-OS directement dans la barre de menu macOS.
- Prévenir la fermeture accidentelle du Mac lorsqu'un processus critique (ex: CDP, extraction Keychain) est en cours d'exécution.
- Lister les processus actifs, leur PID, leur nœud d'exécution, et l'heure de démarrage.
- Détecter les verrous fantômes (zombies) si un processus a planté sans libérer le verrou.

## 3. Architecture & Intégration Y-OS
xbar exécute des scripts placés dans un dossier spécifique et affiche leur sortie standard (stdout) dans la barre de menu.

- **Dossier des plugins** : `~/Library/Application Support/xbar/plugins/`
- **Plugin Y-OS** : `yos_status.10s.sh` (Refresh toutes les 10 secondes)
- **Lock file** : `/tmp/yos_mac_lock.json` et `/tmp/yos_locks/*.json`
- **Gestionnaire Python** : `04_INTERFACES/xbar-plugins/yos_lock.py`

### États Visuels
| État | Affichage Barre de Menu | Signification |
|---|---|---|
| Inactif | `⚫ Y-OS` | Aucun processus en cours. Le Mac peut être fermé. |
| Actif | `🔒 Y-OS (N actif)` | *N* processus en cours. **Ne pas fermer le Mac.** |
| Zombie | `⚠️ Y-OS (zombie)` | Un fichier lock existe, mais le PID associé est mort. |

## 4. Configuration & Déploiement

### Déploiement du Plugin
Le script `yos_status.10s.sh` doit être exécutable et placé dans le dossier des plugins xbar.

```bash
# Exemple de script yos_status.10s.sh
#!/bin/bash
LOCK_DIR="/tmp/yos_locks"
LEGACY_LOCK="/tmp/yos_mac_lock.json"
# ... (logique de vérification des PID et formatage de la sortie xbar) ...
```

### Utilisation via Python (`yos_lock.py`)
L'interface standard pour Y-OS est d'utiliser le context manager `MacLock` :

```python
from yos_lock import MacLock

with MacLock("Nom de la tâche", node="Mac+CDP"):
    # Le verrou est actif, xbar affiche 🔒 Y-OS
    pass
# Le verrou est libéré automatiquement
```

## 5. Limitations & Contraintes
- **macOS Uniquement** : xbar ne fonctionne que sur Mac. Pour les notifications multi-plateformes, Y-OS utilise Telegram.
- **Lecture Seule** : xbar est un indicateur visuel. Il ne permet pas d'interaction bidirectionnelle complexe (contrairement à Telegram).
- **Dépendance PID** : La détection de zombie repose sur la vérification de l'existence du PID (`kill -0 <pid>`). Cela fonctionne bien pour les processus locaux, mais nécessite une gestion rigoureuse si les processus sont détachés.

## 6. Décisions Stratégiques Associées
- **xbar vs SwiftBar** : xbar a été choisi comme standard Y-OS car il était déjà installé sur la machine cible, évitant l'installation de dépendances supplémentaires, et dispose d'une communauté open-source plus large. SwiftBar a été éliminé.
- **Complémentarité Telegram** : xbar sert pour la visibilité immédiate et permanente sur le Mac. Telegram sert pour les notifications push et l'interaction sur tous les appareils (iOS, Android, etc.).

## References
[1] AGENTS.md - Règle Canon #4 (Y-OS Notification & Interaction Stack)
