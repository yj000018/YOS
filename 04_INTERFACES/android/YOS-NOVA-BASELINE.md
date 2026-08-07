# Y-OS Nova Launcher — Baseline Power User

**Document d'Architecture** — *Configuration optimale de Nova Launcher Prime pour la flotte Android Y-OS (Tab S11, Fold 7).*

---

## 1. Philosophie Y-OS pour le Launcher

Le launcher n'est pas un espace de stockage d'icônes, c'est un **hub d'action cognitif**.
- **Zéro friction :** Tout doit être accessible en 1 geste.
- **Search-First :** On ne cherche pas une app visuellement, on la cherche par fonction (Nova Search + Sesame).
- **Densité maximale :** Sur tablette et Fold, l'espace écran doit être exploité (grilles 8x8 et 9x9).
- **Déploiement flotte :** La configuration doit être packagée dans un `.novabackup` déployable via ADB sur tout nouveau device.

---

## 2. Configuration Baseline v1

Cette configuration est encodée dans `yos_nova_poweruser_v1.novabackup`.

### Grilles et Affichage
| Paramètre | Valeur | Raison |
|---|---|---|
| **Desktop Grid** | `9x9 subgrid` | Densité maximale pour écran 12" |
| **Drawer Grid** | `8x8` | Vue globale sans scroll excessif |
| **Scroll Effect** | `None` | Transitions instantanées (zéro délai d'animation) |
| **Drawer Style** | `Vertical` | Scroll naturel |
| **Weather Units** | `Celsius` | Localisation CH |

### Gestes (Gestures) — Le cœur du hub d'action
| Geste | Action Y-OS |
|---|---|
| **Swipe Down** | `Nova Search` (Recherche universelle) |
| **Swipe Up** | `App Drawer` (Tiroir d'apps) |
| **Home Button** | `Nova Search` |
| **Pinch Out** | `Recent Apps` (Multitasking) |
| **Double Tap** | *(Réservé pour Tasker : Screen Lock ou Y-OS Voice)* |

### Comportements (Booleans)
- ✅ `drawer_infinite_scroll` : Scroll infini
- ✅ `drawer_predictive_apps` : Apps prédictives en haut du tiroir
- ✅ `drawer_show_keyboard_by_default` : Clavier auto dans le tiroir (Search-First)
- ❌ `drawer_smart_folders` : Désactivé (génère du désordre non contrôlé)
- ❌ `auto_add_shortcuts` : Désactivé (l'écran d'accueil reste propre)

---

## 3. Plugins et Écosystème Nova

Pour transformer Nova en véritable interface Y-OS, ces plugins sont recommandés :

### 1. Nova Google Companion
- **Rôle :** Ajoute le panneau Google Discover (swipe left sur l'écran d'accueil).
- **Installation :** Sideload APK obligatoire (pas sur Play Store).
- **Statut Y-OS :** *Optionnel* (dépend de la préférence pour le flux Google).

### 2. Sesame (Universal Search) / Nova Search
- **Rôle :** Recherche fonctionnelle (tags) et deep links (ex: "WhatsApp Yannick").
- **Intégration :** Natif dans Nova.
- **Statut Y-OS :** **Critique**. Rendu obsolète par l'abandon de Sesame, mais Nova Search natif prend le relais.

### 3. Tasker + AutoShortcut
- **Rôle :** Assigner des tâches Tasker complexes aux gestes Nova (ex: swipe up sur l'icône Notion = créer une nouvelle note).
- **Statut Y-OS :** **Critique** (cf. session Tasker).

### 4. KWGT (Kustom Widget Maker)
- **Rôle :** Créer des widgets dynamiques pilotés par Y-OS (ex: dashboard de la flotte Android, status du Cloud Computer).
- **Statut Y-OS :** Recommandé pour l'écran d'accueil.

---

## 4. Déploiement sur un nouveau device (ex: Fold 7)

Le fichier `yos_nova_poweruser_v1.novabackup` est stocké sur le Cloud Computer.
Pour l'appliquer sur un nouveau device :

```bash
# 1. Pousser le backup
adb push yos_nova_poweruser_v1.novabackup /sdcard/Download/

# 2. Restaurer via Nova (nécessite confirmation tactile)
adb shell am start \
  -a android.intent.action.VIEW \
  -d "file:///sdcard/Download/yos_nova_poweruser_v1.novabackup" \
  -t "application/octet-stream" \
  -n com.teslacoilsw.launcher/.NovaShortcutHandler
```

*Note : La création de dossiers dans le tiroir n'est pas incluse dans ce backup de base, car elle dépend des apps indexées. Elle est gérée par la stratégie de catégorisation Y-OS (Search-First).*
