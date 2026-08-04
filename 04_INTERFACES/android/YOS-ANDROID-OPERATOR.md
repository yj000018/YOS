# Y-OS Android Operator — Documentation Complète
> **Source de vérité** : `yj000018/YOS` → `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md`
> **Last updated** : 2026-08-05
> **Statut** : ✅ Opérationnel — Galaxy Tab S11 connectée via CC→Tailscale→ADB

---

## TL;DR — Ce qu'il faut savoir en 30 secondes

```
Manus → CC yos-cloud-operator (100.93.75.9) → Tailscale → Galaxy Tab S11 (100.89.158.44:5555)
```

**Commande de connexion depuis le CC :**
```bash
adb kill-server && adb start-server && adb connect 100.89.158.44:5555
```

**Vérification :**
```bash
adb devices
# → 100.89.158.44:5555  device  SM_X730
```

**Auto-reconnect** : cron `*/2 * * * *` → `/home/ubuntu/yos/adb_reconnect.sh` (CC)

---

## 1. Architecture globale

```
┌─────────────────────────────────────────────────────────────────┐
│  MANUS (orchestration)                                          │
│  session préfixée : cloud-pc-8cd489il:                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ shell tool (direct)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  CC — yos-cloud-operator                                        │
│  IP publique : 34.148.90.222                                    │
│  IP Tailscale : 100.93.75.9                                     │
│  ADB v1.0.41 : /usr/bin/adb                                     │
│  Cron auto-reconnect : */2 * * * *                              │
└────────────────────────┬────────────────────────────────────────┘
                         │ Tailscale (WireGuard overlay)
                         │ via DERP relay (pas de direct path
                         │ car AP Isolation sur WiFi local)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Galaxy Tab S11 — galaxy-tab-s11                                │
│  IP Tailscale : 100.89.158.44                                   │
│  ADB TCP port : 5555                                            │
│  Wireless Debugging : ON (port variable ~37000-45000)           │
│  Tailscale : connecté au tailnet tail7c87e1.ts.net              │
└─────────────────────────────────────────────────────────────────┘
```

### Pourquoi pas direct depuis le Mac ?
L'AP Isolation du routeur WiFi bloque les connexions TCP entre appareils du même réseau local (Mac ↔ Tablette). Le ping ICMP passe, TCP est bloqué. Le CC est sur internet (GCP) et passe via DERP relay Tailscale → bypass total de l'AP Isolation.

### Pourquoi pas ADB direct depuis le CC via Tailscale sans pairing ?
Android 16 bloque les connexions TCP entrantes sur l'interface Tailscale (`ts0`). Il faut un pairing initial depuis un appareil autorisé. Le CC a été appairé une fois et est listé dans "Paired devices" sur la tablette → connexion directe possible ensuite.

---

## 2. Inventaire des appareils Android Y-OS

| ID | Appareil | Modèle | IP Tailscale | Statut | Méthode ADB |
|---|---|---|---|---|---|
| AND-001 | Galaxy Tab S11 | SM-X730 | 100.89.158.44 | ✅ Opérationnel | CC → Tailscale → :5555 |
| AND-002 | Galaxy Z Fold 7 | SM-F956 | _à configurer_ | ⏳ Session dédiée | CC → Tailscale → :5555 |

---

## 3. Protocole de connexion ADB — Procédure complète

### 3.1 Connexion standard (tablette déjà appairée)

```bash
# Depuis le CC (session cloud-pc-8cd489il:)
adb kill-server
sleep 1
adb start-server
sleep 1
adb connect 100.89.158.44:5555
adb devices -l
```

**Résultat attendu :**
```
100.89.158.44:5555     device product:gts11wifieea model:SM_X730 device:gts11wifi
```

### 3.2 Pairing initial (nouvel appareil ou clé RSA perdue)

**Prérequis sur la tablette :**
1. Paramètres → Options développeur → Wireless debugging → **ON**
2. Wireless debugging → "Appairer l'appareil avec un code" → noter le **code 6 chiffres** et le **port**

**Depuis le CC :**
```bash
adb pair <IP_TAILSCALE>:<PORT_PAIRING> <CODE_6_CHIFFRES>
# Exemple : adb pair 100.89.158.44:40303 861885
```

**⚠️ IMPORTANT — ADB version sur le CC :**
- CC utilise ADB v1.0.41 (debian) — `adb pair` peut retourner "Unable to start pairing client"
- Si échec du pairing depuis le CC : utiliser le Mac comme relais pour le pairing initial (1 seule fois)
- Une fois appairé, `adb connect` fonctionne directement depuis le CC

**Pairing via Mac (fallback) :**
```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('bore.pub', port=22847, username='yannickjolliet', password='    ')
_, stdout, _ = ssh.exec_command('/opt/homebrew/bin/adb pair 100.89.158.44:<PORT> <CODE>')
print(stdout.read().decode())
```

### 3.3 Reconnexion après reboot tablette

```bash
# Le cron tourne automatiquement toutes les 2 min sur le CC
# Forcer manuellement :
bash /home/ubuntu/yos/adb_reconnect.sh

# Vérifier le log :
cat /home/ubuntu/yos/logs/adb_reconnect.log
```

---

## 4. Commandes ADB opérationnelles

### Informations système
```bash
ADB="adb -s 100.89.158.44:5555"

# Modèle / Android / SDK
$ADB shell getprop ro.product.model
$ADB shell getprop ro.build.version.release
$ADB shell getprop ro.build.version.sdk

# Batterie
$ADB shell dumpsys battery | grep -E "level|status|temperature" | head -5

# Uptime
$ADB shell uptime

# Stockage
$ADB shell df /data | tail -1
```

### Apps
```bash
# Lister apps tierces
$ADB shell pm list packages -3 | sort | sed 's/package://'

# Désinstaller une app
$ADB uninstall com.package.name

# Désactiver une app système (sans désinstaller)
$ADB shell pm disable-user --user 0 com.package.name

# Installer un APK
$ADB install /path/to/app.apk

# Lancer une app
$ADB shell monkey -p com.package.name 1
```

### Fichiers
```bash
# Screenshot
$ADB shell screencap /sdcard/screen.png
$ADB pull /sdcard/screen.png /tmp/screen.png

# Transfert fichier vers tablette
$ADB push /local/file.pdf /sdcard/Download/

# Transfert depuis tablette
$ADB pull /sdcard/Download/file.pdf /tmp/
```

### Contrôle UI
```bash
# Simuler tap (x, y)
$ADB shell input tap 540 960

# Simuler swipe
$ADB shell input swipe 540 1500 540 500 300

# Simuler touche physique
$ADB shell input keyevent 26   # Power
$ADB shell input keyevent 3    # Home
$ADB shell input keyevent 4    # Back
$ADB shell input keyevent 187  # Recents

# Saisir du texte
$ADB shell input text "hello"

# Allumer/éteindre écran
$ADB shell input keyevent 224  # Allumer
$ADB shell input keyevent 223  # Éteindre
```

### Notifications & monitoring
```bash
# Lire les notifications actives
$ADB shell dumpsys notification | grep "pkg=" | head -20

# Logs en temps réel
$ADB logcat -v time | grep -i error

# Processus actifs
$ADB shell ps -A | grep -v "S " | head -20
```

---

## 5. Ce que Manus peut faire avec l'Android Operator

| Capacité | Commande | Usage Y-OS |
|---|---|---|
| **Screenshot** | `screencap + pull` | Vérification visuelle état tablette |
| **Installer APK** | `adb install` | Déploiement apps sans Play Store |
| **Désinstaller apps** | `adb uninstall` | Nettoyage automatisé |
| **Lancer apps** | `monkey -p` | Automation workflows |
| **Transfert fichiers** | `push/pull` | Sync documents, PDFs, médias |
| **Contrôle UI** | `input tap/swipe/keyevent` | Automation UI complète |
| **Monitoring batterie** | `dumpsys battery` | Alertes Telegram si < 20% |
| **Logs système** | `logcat` | Debug apps |
| **Désactiver bloatware** | `pm disable-user` | Nettoyage Samsung |
| **Reboot** | `adb reboot` | Redémarrage à distance |
| **Notifications** | `dumpsys notification` | Lecture notifications |

---

## 6. Auto-reconnect — Architecture du cron

**Script** : `/home/ubuntu/yos/adb_reconnect.sh` (CC)
**Cron** : `*/2 * * * *` (toutes les 2 minutes)
**Logique** :
1. Vérifie si `100.89.158.44:5555` est dans `adb devices` avec statut `device`
2. Si oui → exit silencieux
3. Si non → `adb kill-server && adb start-server && adb connect 100.89.158.44:5555`
4. Si reconnexion réussie → notif Telegram `@yos_notif_bot` → chat_id `223132272`

**Log** : `/home/ubuntu/yos/logs/adb_reconnect.log`

**Conditions de déconnexion connues :**
- Reboot tablette (Wireless Debugging reste ON après reboot sur Android 16 ✅)
- Tailscale déconnecté sur tablette (ouvrir app Tailscale → reconnecter)
- ADB server crash sur CC (résolu par kill-server + start-server)

---

## 7. Leçons apprises — Pièges à éviter

| Piège | Symptôme | Solution |
|---|---|---|
| AP Isolation WiFi | Mac ne peut pas ping tablette en TCP | Passer par le CC (internet) |
| ADB v34 debian — pairing bug | "Unable to start pairing client" | Pairer depuis Mac (1x), puis CC fonctionne |
| Android 16 — TCP entrant bloqué sur ts0 | `adb connect` timeout depuis CC sans pairing | Pairing initial obligatoire depuis appareil autorisé |
| Tailscale déconnecté tablette | ping 0% depuis CC | Ouvrir app Tailscale sur tablette → reconnecter |
| Knox irréversible | — | NE PAS ROOTER — Knox = brick définitif |
| Port Wireless Debugging variable | Port change à chaque session Wireless Debug | Utiliser port 5555 (tcpip) — stable |
| Code pairing expire vite | "protocol fault" | Générer nouveau code < 30s avant usage |

---

## 8. Specs matérielles — Galaxy Tab S11

| Champ | Valeur |
|---|---|
| **Modèle** | Samsung Galaxy Tab S11 (SM-X730) |
| **Serial ADB** | R5GYB0AXSBY |
| **Android** | 16 / One UI 8.0 |
| **SDK** | 36 |
| **Knox** | 3.12 / API 39 |
| **IP WiFi locale** | 192.168.1.91 (DHCP stable) |
| **IP Tailscale** | 100.89.158.44 |
| **MagicDNS** | galaxy-tab-s11.tail7c87e1.ts.net |
| **ADB port** | 5555 (tcpip permanent) |
| **Apps tierces** | 190 |

---

## 9. Roadmap Android Y-OS

| Étape | Statut | Notes |
|---|---|---|
| Galaxy Tab S11 — ADB via CC→Tailscale | ✅ Opérationnel | Pipeline validé 2026-08-05 |
| Auto-reconnect cron | ✅ Actif | `*/2 * * * *` sur CC |
| Nettoyage apps tablette | ⏳ En cours | ~35 apps à supprimer |
| Galaxy Z Fold 7 — même pipeline | ⏳ Session dédiée | Même protocole que Tab S11 |
| MacBook Pro always-on — relais ADB permanent | ⏳ À réception | Remplace bore tunnel Mac Air |
| Monitoring batterie automatique (Telegram) | ⏳ À créer | Script cron CC → alerte si < 20% |
| Automation UI tablette (scénarios) | ⏳ À définir | input tap/swipe via ADB |

---

## 10. Fichiers clés sur le CC

| Fichier | Rôle |
|---|---|
| `/home/ubuntu/yos/adb_reconnect.sh` | Auto-reconnect ADB toutes les 2 min |
| `/home/ubuntu/yos/logs/adb_reconnect.log` | Log des reconnexions |
| `/usr/bin/adb` | ADB v1.0.41 (android-tools-adb) |

---

## Changelog

| Date | Action |
|---|---|
| 2026-08-03 | Tailscale installé sur Galaxy Tab S11 (100.89.158.44) |
| 2026-08-04 | Pipeline ADB validé via Mac relais (CC→SSH bore→Mac→adb 192.168.1.91:5555) |
| 2026-08-04 | Reboot tablette → AP Isolation découverte → pipeline Mac cassé |
| 2026-08-05 | **Pipeline final validé** : CC→Tailscale→100.89.158.44:5555 (bypass AP Isolation) |
| 2026-08-05 | Auto-reconnect cron installé sur CC |
| 2026-08-05 | Ce module DOC créé dans GitHub YOS |
