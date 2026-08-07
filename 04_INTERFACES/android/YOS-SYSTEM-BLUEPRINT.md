# Y-OS Android System Blueprint

**Document d'Architecture** — *Configuration système optimale pour un power user Y-OS sur Android 16 (Samsung One UI 8).*

---

## 1. Philosophie Y-OS

Le blueprint système Y-OS vise à transformer un appareil Android grand public en un **outil de production silencieux, réactif et prévisible**.
- **Zéro distraction :** Sons système désactivés, haptique désactivée, notifications masquées sur l'écran de verrouillage.
- **Vitesse maximale :** Animations réduites à 0.5x, pas d'effets de transition inutiles.
- **Contrôle total :** Options développeur actives, ADB activé en permanence, écran qui ne s'éteint pas en charge.

---

## 2. Configuration Système (Automatisée via ADB)

Le script `yos-android-system-config.sh` applique automatiquement ces 22 paramètres via la commande `adb shell settings put`.

### Affichage (Display)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `screen_brightness_mode` | `1` | Luminosité adaptative activée. |
| `screen_off_timeout` | `600000` | 10 minutes. Les tablettes sont des outils de travail, l'écran ne doit pas s'éteindre pendant la réflexion. |
| `animator_duration_scale` | `0.5` | Animations 2x plus rapides. Sensation de réactivité immédiate. |
| `transition_animation_scale` | `0.5` | Transitions 2x plus rapides. |
| `window_animation_scale` | `0.5` | Fenêtres 2x plus rapides. |

### Son et Haptique (Sound & Haptics)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `haptic_feedback_enabled` | `0` | Désactivé. Pas de vibration parasite lors de la frappe ou navigation. |
| `sound_effects_enabled` | `0` | Désactivé. Pas de "clic" système. Silence absolu. |

### Batterie (Battery)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `adaptive_battery_management` | `1` | Activé. L'OS gère les apps en arrière-plan. |
| `low_power` | `0` | Power saver désactivé par défaut pour des performances maximales. |

### Sécurité et Confidentialité (Security)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `lock_screen_show_notifications` | `1` | Afficher les notifications sur l'écran de verrouillage. |
| `lock_screen_allow_private_notifications` | `0` | Masquer le contenu privé. Seule l'icône de l'app est visible. |

### Options Développeur (Developer)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `development_settings_enabled` | `1` | Requis pour le contrôle Y-OS. |
| `adb_enabled` | `1` | Requis pour le pipeline Y-OS (Tailscale → ADB). |
| `stay_on_while_plugged_in` | `2` | L'écran reste allumé en charge (idéal pour les dashboards ou sessions de travail prolongées). |

### Réseau (Network)
| Paramètre | Valeur | Raison Y-OS |
|---|---|---|
| `wifi_sleep_policy` | `2` | NEVER. Le WiFi ne se coupe jamais en veille (requis pour ADB over Tailscale permanent). |

---

## 3. Actions Manuelles (Non Automatisables)

Certains paramètres critiques ne sont pas accessibles via ADB sans root. Ils doivent être configurés manuellement lors du déballage d'un nouvel appareil (OOBE).

1. **Mode Sombre :** Paramètres → Affichage → Mode sombre.
2. **Protection Batterie :** Paramètres → Batterie → Battery protection (limite la charge à 85% pour préserver la durée de vie).
3. **Biométrie :** Paramètres → Sécurité et confidentialité → Biométrie (Empreinte + Reconnaissance faciale).
4. **Wireless Debugging :** Paramètres → Options développeur → Wireless debugging (Activé).

---

## 4. Déploiement

Pour appliquer ce blueprint sur un nouveau device (ex: Fold 7) :

```bash
# Sur le Cloud Computer
cd /home/ubuntu/yos/android/provision
./yos-android-system-config.sh 100.X.Y.Z:5555
```

Le script vérifie chaque paramètre et affiche un résumé des succès et erreurs. Il pousse également automatiquement le blueprint Nova Launcher (`yos_nova_poweruser_v1.novabackup`) dans le dossier Téléchargements de l'appareil.
