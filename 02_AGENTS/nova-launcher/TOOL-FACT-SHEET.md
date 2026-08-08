# Tool Fact Sheet: Nova Launcher (Android)

## Overview
Nova Launcher Prime est le launcher Android canonique pour l'écosystème Y-OS. Il remplace One UI (Samsung) ou Pixel Launcher pour offrir une interface unifiée, hautement personnalisable et automatisable (partiellement) via ADB.

**Package:** `com.teslacoilsw.launcher`
**Activity principale:** `.NovaLauncher`
**Version de référence:** 8.x

## Capabilities & Limitations

| Feature | Automatisable via ADB? | Méthode |
|---|---|---|
| **Lancer Nova** | ✅ Oui | `am start -n com.teslacoilsw.launcher/.NovaLauncher` |
| **Définir par défaut** | ✅ Oui | `cmd package set-home-activity com.teslacoilsw.launcher/.NovaLauncher` |
| **Fermer/Tuer** | ✅ Oui | `am force-stop com.teslacoilsw.launcher` |
| **Effacer données (Reset)** | ✅ Oui | `pm clear com.teslacoilsw.launcher` |
| **Restaurer Backup (.novabackup)** | ⚠️ Partiel | Intent VIEW (nécessite clic manuel sur l'écran) |
| **Générer Backup** | ❌ Non | Action manuelle requise dans l'UI |
| **Modifier Layout/Groupes** | ⚠️ Indirect | Édition du `.novabackup` (SQLite + XML) sur le CC puis push |
| **Changer paramètres (Rotation, etc.)** | ⚠️ Indirect | Édition de `nova.xml` dans le `.novabackup` |

## Architecture d'un `.novabackup`

Un fichier `.novabackup` est une archive ZIP standard contenant :
1. `nova.db` : Base de données SQLite (layout, dossiers, groupes du tiroir).
2. `nova.xml` : Fichier XML des préférences (gestes, grilles, couleurs).
3. Fichiers d'icônes et autres assets.

### SQLite Database (`nova.db`)
- **`drawer_groups`** : Définit les dossiers dans le tiroir d'applications.
  - Colonnes clés : `_id` (int), `title` (string), `groupType` ('folder').
  - ⚠️ **CRITIQUE** : Ne **JAMAIS** utiliser d'emojis dans le champ `title`. Cela provoque une `java.net.URISyntaxException` au démarrage de Nova et fait crasher le launcher en boucle.
- **`appgroups`** : Assigne les applications aux dossiers du tiroir.
  - Colonnes clés : `groupId` (FK vers `drawer_groups._id`), `component` (string).
  - Format `component` : `package.name/activity.name#-1` (ex: `com.android.chrome/com.google.android.apps.chrome.Main#-1`).
  - ⚠️ **CRITIQUE** : L'URI du composant doit être parfaitement valide. Aucun caractère spécial ou espace.

### XML Preferences (`nova.xml`)
- Gestes : `<string name="gesture_swipe_down">5</string>` (5 = Nova Search)
- Rotation : `<boolean name="allow_rotation" value="true" />`

## Protocole de gestion automatisée (Y-OS Operator)

Puisque l'API de Nova ne permet pas l'édition live via ADB, Y-OS utilise un protocole "Offline Edit & Push" :

1. **Générer un backup de base** (Manuel sur tablette).
2. **Pull sur le Cloud Computer** : `adb pull /sdcard/Download/base.novabackup /tmp/`
3. **Édition programmatique (Python)** :
   - Dézipper.
   - Éditer `nova.db` via `sqlite3` (ajouter des groupes, assigner des apps).
   - Éditer `nova.xml` (changer les gestes, grilles).
   - Re-zipper.
4. **Push sur la tablette** : `adb push /tmp/edited.novabackup /sdcard/Download/`
5. **Déclencher la restauration** :
   ```bash
   adb shell am start -a android.intent.action.VIEW \
     -t "application/vnd.novalauncher.backup" \
     -d "file:///sdcard/Download/edited.novabackup" \
     com.teslacoilsw.launcher/.RestoreBackupFileHandler
   ```
6. **Action manuelle** : L'utilisateur clique sur "Restore" sur l'écran de la tablette.

## Cas de bord & Dépannage

### 1. Nova crashe en boucle (Écran noir ou retour sur One UI)
**Cause probable** : Un backup corrompu a été restauré (ex: emojis dans les noms de groupes SQLite, composant URI invalide).
**Résolution ADB** :
```bash
# 1. Effacer toutes les données corrompues (Reset usine Nova)
adb shell pm clear com.teslacoilsw.launcher
# 2. Relancer Nova proprement
adb shell am start -n com.teslacoilsw.launcher/.NovaLauncher
# 3. Redéfinir comme défaut
adb shell cmd package set-home-activity com.teslacoilsw.launcher/.NovaLauncher
# 4. Pousser un backup propre et demander restauration manuelle
```

### 2. Apps manquantes dans le tiroir ou les dossiers
**Cause probable** : Le nom de l'activité (`component`) a changé suite à une mise à jour de l'app, ou l'app n'est pas indexée.
**Résolution** :
- Vérifier le nom exact du composant : `adb shell dumpsys package <package_name> | grep -A1 "MAIN"`
- Re-générer le `.novabackup` avec le bon nom de composant.

### 3. Le geste Swipe Down ouvre les notifications au lieu de Nova Search
**Cause probable** : Paramètre écrasé ou non inclus dans le backup.
**Résolution** : Assurer que `nova.xml` contient `<string name="gesture_swipe_down">5</string>`.

## Règle de design Y-OS (Taxonomy)
Les applications doivent être organisées en "Fonctionymes" (groupes thématiques basés sur les workflows).
Une application "Most Common" (ex: ChatGPT) peut (et doit) apparaître à la fois dans le groupe `Most Common` et dans son groupe fonctionnel `AI and Web`. SQLite permet d'insérer plusieurs entrées dans `appgroups` pour le même `component` avec des `groupId` différents.
