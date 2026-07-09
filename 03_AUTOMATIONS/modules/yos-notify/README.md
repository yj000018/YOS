# yOS-Notify — Module de notification universel

> Module fondamental de Y-OS. Couche de notification multi-canal appelable depuis n'importe quel script, module ou app du stack yOS.

---

## Canaux supportés

| Canal | Plateforme | App à installer |
|---|---|---|
| **Pushover** | iOS, iPadOS, macOS, Android, Ubuntu | Voir liens ci-dessous |
| **Telegram** | iOS, iPadOS, macOS, Android, Ubuntu | Telegram natif |

---

## Installation des apps

### Pushover (canal principal — push natif)

| Plateforme | Lien | Notes |
|---|---|---|
| **iOS / iPadOS** | [App Store — Pushover](https://apps.apple.com/app/pushover-notifications/id506088175) | $4.99 une fois — inclut toutes les plateformes |
| **macOS** | [Pushover Desktop](https://pushover.net/clients/desktop) | Gratuit avec le compte |
| **Android** | [Google Play — Pushover](https://play.google.com/store/apps/details?id=net.superblock.pushover) | Gratuit avec le compte |
| **Ubuntu / N100** | Via script Python (voir ci-dessous) | Pas d'app nécessaire |

**Compte :** `yannick.jolliet@gmail.com` — login sur [pushover.net](https://pushover.net)

### Telegram (canal secondaire)

Bot : **@Ytravel2_bot** (nom affiché : "Manus-notif")
Chat ID : `223132272`

---

## Deep link iOS natif — Manus

URL scheme confirmé : `tech.butterfly.app://app/{task_id}`

Ouvre directement l'app Manus iOS sur le bon thread (sans passer par Safari).

App Manus iOS : [App Store — Manus](https://apps.apple.com/app/manus-ai-agent-automation/id6740909540)

---

## Credentials (stockés dans `~/.yos/config/notify.json` et `~/.manus/secrets/yos_secrets.env`)

| Clé | Valeur |
|---|---|
| `PUSHOVER_APP_TOKEN` | `ataj78gnkgokj3pn1rdstkvuztzuoa` |
| `PUSHOVER_USER_KEY` | `u7av8hq2zazt8gdqssqft9coof6eu3` |
| `PUSHOVER_EMAIL` | `yannick.jolliet@gmail.com` |
| `TELEGRAM_BOT_TOKEN` | `8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo` |
| `TELEGRAM_BOT_USERNAME` | `@Ytravel2_bot` |
| `TELEGRAM_CHAT_ID` | `223132272` |

---

## Usage

### Python (depuis n'importe quel script yOS)

```python
import sys
sys.path.insert(0, '/home/ubuntu/.yos/modules')
from yos_notify.yos_notify import notify, task_done

# Notification simple
notify("Titre", "Message", channel="pushover")
notify("Titre", "Message", channel="telegram")
notify("Titre", "Message", channel="both")

# Tâche longue terminée (format standardisé yOS)
task_done(
    task_name="DWPose Rigging — eYa",
    success=True,
    next_step="Ouvrir eya_dwpose.stretch dans Stretchy Studio",
    task_id="zrkMu8YuWmC9xCqWONH6sL",   # → deep link natif iOS
    duration="14m 22s",
    channel="pushover"   # ou "both"
)
```

### CLI (bash / terminal)

```bash
yos-notify "Titre" "Message"
yos-notify "Titre" "Message" --channel telegram
yos-notify "Titre" "Message" --channel both --device ios
```

### Depuis le N100

```bash
# Copier le module sur le N100 (une fois)
scp -r ~/.yos/modules/yos_notify user@n100:/opt/yos/modules/

# Utilisation
python3 -c "
import sys; sys.path.insert(0, '/opt/yos/modules')
from yos_notify.yos_notify import task_done
task_done('Tâche N100', True, task_id='THREAD_ID', duration='5m')
"
```

---

## Paramètres `task_done()`

| Paramètre | Type | Description |
|---|---|---|
| `task_name` | str | Nom de la tâche |
| `success` | bool | True = succès, False = échec |
| `next_step` | str | Ce qu'il faut faire ensuite |
| `task_id` | str | ID du thread Manus → deep link natif iOS |
| `manus_url` | str | URL directe (prioritaire sur task_id) |
| `duration` | str | Durée ex: "14m 22s" |
| `channel` | str | "pushover" (défaut) / "telegram" / "both" |

---

## Résolution d'URL (priorité)

1. `manus_url` explicite → utilisé tel quel
2. `task_id` → `tech.butterfly.app://app/{task_id}` (deep link natif iOS)
3. Env var `MANUS_TASK_ID` → même pattern
4. Fallback → `https://manus.im/app` (liste des sessions)

---

## Règle yOS — tâches longues

**Toute tâche > 2 minutes** doit se terminer par un appel `task_done()` avec `task_id` du thread courant.

- Succès → priorité normale Pushover
- Échec → priorité haute Pushover (son différent sur iOS)

---

## Structure du module

```
yos_notify/
├── yos_notify.py      # Module principal
├── __init__.py        # Exports
├── install.sh         # Installeur CLI
└── README.md          # Ce fichier
```

Config : `~/.yos/config/notify.json`
Logs : `~/.yos/logs/notify.log`
