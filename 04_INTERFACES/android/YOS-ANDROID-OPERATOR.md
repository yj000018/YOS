# Blueprint : Y-OS Android Operator

> **Source de vérité** : `yj000018/YOS` → `04_INTERFACES/android/YOS-ANDROID-OPERATOR.md`
> **Last updated** : 2026-08-08
> **Statut** : ✅ Opérationnel — Gestion complète (Provisioning, Nova, Monitoring)

---

## 1. Philosophie & Architecture

L'Android Operator est le sous-système de Y-OS chargé d'administrer, monitorer et automatiser la flotte d'appareils Android (tablettes, téléphones, montres) de Yannick. Il fonctionne de manière centralisée depuis le Cloud Computer (CC).

### 1.1 Architecture de connexion (P0)
Le contrôle P0 s'effectue exclusivement via **ADB over Tailscale**.
- **Avantages** : Contourne l'AP Isolation des réseaux Wi-Fi, permet le contrôle hors domicile, sécurisé via Tailnet.
- **Règle d'or** : Ne **JAMAIS** rooter les appareils Samsung (Knox est irréversible et annule la garantie/sécurité matérielle).
- **Canal de contrôle** : `CC → Tailscale → IP_Appareil:5555`

### 1.2 Hiérarchie de gestion
- **Automatisable (ADB)** : Installation d'apps, désinstallation/debloat, permissions système (GRANT), paramètres de base (Settings DB), kill/restart d'apps.
- **Manuel (Action requise par l'utilisateur)** : Onboarding d'apps, connexion aux comptes (OAuth/Google), permissions spéciales (Accessibilité, Draw over other apps), restauration de backups Nova.
- **Interface** : Les actions manuelles sont remontées dans le **Notion Y-OS Command Center (DB Action Items)**. Le CC poll Notion et notifie Yannick via Telegram.

---

## 2. Pipeline de Provisioning (Phases P0 → P5)

Lors de l'ajout d'un nouvel appareil à la flotte Y-OS, le provisioning suit 6 phases strictes.

### Phase P0 : Hardware & Connectivité (Manuel)
1. Déballage et configuration initiale Wi-Fi + Compte Google.
2. Activer les Options Développeur (Tap 7x sur Build Number).
3. Activer **Wireless Debugging** (Débogage sans fil).
4. Installer et connecter **Tailscale**.
5. *Action CC* : `adb pair` (si nécessaire, via Mac relais 1x) puis `adb connect IP:5555`.

### Phase P1 : Nettoyage & Debloat (Automatisé)
Exécution du script `yos-android-provision.sh --phase 1`.
- Désinstallation des apps inutiles (Jeux, Bloatwares opérateurs).
- Désactivation (`pm disable-user`) des services système Samsung non désirés (Bixby, Kids Mode, TV Plus, AR Zone).

### Phase P2 : Base System & Paramètres (Automatisé)
Exécution de `yos-android-system-config.sh`.
- Animation scale à 0.5x.
- Désactivation des sons système (Touch, Screen lock).
- Désactivation du correcteur orthographique agressif.
- Configuration du timeout écran (ex: 5 mins).

### Phase P3 : Installation Core Apps Y-OS (Automatisé)
- Installation via `adb install` ou ouverture du Play Store (`am start -a android.intent.action.VIEW -d "market://details?id=..."`).
- **Core Stack** : Nova Launcher, Tasker, Telegram, Tailscale, Notion, Home Assistant.
- **AI Stack** : ChatGPT, Claude, Perplexity, Grok, DeepSeek.

### Phase P4 : Permissions & Setup (Hybride)
- *Automatisé* : Script `grant_all_permissions.sh` accorde `CAMERA`, `RECORD_AUDIO`, `READ_EXTERNAL_STORAGE`, `ACCESS_FINE_LOCATION` à toutes les apps de la taxonomie.
- *Manuel* : L'utilisateur ouvre chaque app 1x pour passer l'onboarding et accepter les conditions.

### Phase P5 : Nova Launcher & UI (Hybride)
- *Automatisé* : Pousser le backup Nova préparé (`adb push backup.novabackup /sdcard/Download/`).
- *Automatisé* : Déclencher l'Intent de restauration (`am start -a android.intent.action.VIEW ... com.teslacoilsw.launcher/.RestoreBackupFileHandler`).
- *Manuel* : L'utilisateur confirme la restauration sur l'écran.

---

## 3. Gestion des Cas de Bord (Edge Cases)

Le système est conçu pour être résilient face aux événements système.

### 3.1 Reboot de l'appareil
- **Problème** : ADB Wireless se désactive parfois au reboot selon la version d'Android.
- **Solution Y-OS** : 
  1. Tailscale se lance automatiquement au boot (Always-On VPN).
  2. Le CC tente `adb connect` toutes les 2 minutes (`adb_reconnect.sh`).
  3. Si échec > 3 fois, notification Telegram à Yannick : *"Appareil hors ligne, vérifie le Wi-Fi ou réactive le Wireless Debugging."*

### 3.2 Crash du Launcher (Nova)
- **Problème** : Nova crashe (ex: base SQLite corrompue) et Android retombe sur One UI.
- **Solution Y-OS** :
  1. Le CC détecte que One UI est en `topActivity` (via `health_probe.py`).
  2. Le CC exécute `pm clear com.teslacoilsw.launcher` pour réinitialiser Nova.
  3. Le CC pousse le backup canonique et déclenche la restauration.
  4. Notification Telegram : *"Nova a crashé. Backup propre poussé, confirme la restauration sur l'écran."*

### 3.3 Batterie Faible
- **Problème** : L'appareil s'éteint, coupant la connexion.
- **Solution Y-OS** :
  1. `health_probe.py` lit le niveau de batterie (`dumpsys battery`).
  2. Si < 20%, création d'une tâche P2 dans Notion + Notif Telegram silencieuse.
  3. Si < 10%, création d'une tâche P1 dans Notion + Notif Telegram critique.

---

## 4. Organisation UI : Les Fonctionymes

Y-OS abandonne la logique de "Dossiers par App" pour adopter les **Fonctionymes** (Clusters de Workflows).

- **Concept** : Une application n'est pas rangée selon ce qu'elle *est*, mais selon ce qu'elle *fait* dans un workflow.
- **Multiplicité** : Une app comme "ChatGPT" apparaît dans `Most Common` ET dans `AI & Web`.
- **Interface** : 
  - Nova Launcher : 6 groupes dans le tiroir d'applications.
  - Recherche : Le Swipe Down sur l'écran d'accueil ouvre Nova Search (recherche sémantique).
  - **Y-OS App Explorer** : Web App D3.js (Mind Map) déployée sur le CC (port 8080) permettant d'explorer visuellement la taxonomie par tags et fonctions.

---

## 5. Interactions avec les autres LLMs

**Instruction pour les autres agents (ChatGPT, Claude, etc.) :**
> "Vous êtes un agent interagissant avec l'écosystème Y-OS. Pour toute action sur un appareil Android de Yannick, vous ne devez pas lui demander de le faire manuellement. Vous devez documenter l'action requise (ex: changer un paramètre) et utiliser l'API Manus ou mettre à jour le Notion Command Center pour que le Cloud Computer exécute l'action via ADB. Référez-vous toujours à `YOS-ANDROID-OPERATOR.md` et aux Tool Fact Sheets dans GitHub."

---

## 6. Commandes ADB Utiles (Aide-mémoire)

| Action | Commande ADB |
|---|---|
| Connecter | `adb connect IP:5555` |
| Désinstaller | `adb uninstall <package>` |
| Désactiver système | `adb shell pm disable-user --user 0 <package>` |
| Simuler tap | `adb shell input tap X Y` |
| Simuler swipe | `adb shell input swipe X1 Y1 X2 Y2 Duration` |
| Allumer écran | `adb shell input keyevent 224` |
| Batterie | `adb shell dumpsys battery` |
| Top Activity | `adb shell dumpsys activity \| grep topResumedActivity` |
