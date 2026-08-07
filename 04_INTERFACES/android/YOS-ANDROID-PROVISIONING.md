# Y-OS Android Provisioning Framework

Ce framework définit la procédure universelle et automatisée pour intégrer tout nouveau device Android dans la flotte Y-OS. Il garantit que chaque appareil passe par un pipeline standardisé de purification, de configuration et d'intégration avant d'être considéré comme opérationnel.

---

## 1. Architecture des Phases (P0 → P5)

Le pipeline est divisé en 6 phases séquentielles. Chaque phase doit être complétée avant de passer à la suivante.

| Phase | Nom | Description | Mode d'exécution |
|---|---|---|---|
| **P0** | **Enrôlement & OOBE** | Décision MDM (COPE/BYOD/None), déballage, connexion WiFi, activation Developer Options et Wireless Debugging. | Manuel (Yannick) |
| **P1** | **Pairing & Identity** | Connexion ADB initiale via WiFi local ou Tailscale, création de la fiche device (`AND-XXX`), ajout au registre. | Automatique (Manus/CC) |
| **P2** | **Purification (Debloat)** | Suppression des bloatwares constructeur, désactivation des apps redondantes (IA, browsers, gadgets). | Automatique (Script) |
| **P3** | **Silence (Anti-Bruit)** | Désactivation des notifications non critiques, configuration du mode DND, exemption batterie pour les apps critiques. | Automatique (Script) |
| **P4** | **Base Apps & Config** | Installation des applications Y-OS standard (Tailscale, HA Companion, Obsidian, Claude, etc.) et configuration des paramètres système. | Mixte (Script + Manuel) |
| **P5** | **Monitoring & Fleet** | Ajout du device dans `health_probe.py` et `drift_packages.py`, snapshot initial, activation des alertes Telegram. | Automatique (Manus/CC) |

---

## 2. Profils par Device

Bien que le pipeline P0→P5 soit universel, son contenu exact varie selon le type d'appareil. Le framework utilise des **Profils** pour adapter l'exécution.

### Profils standards

1. **`primary_phone`** (ex: Fold 7)
   - MDM: COPE recommandé (ou Baseline légère)
   - Apps: Suite complète (Productivité, IA, Communication)
   - Télémétrie: Complète (ADB + HA)
   - Notifications: Strictement filtrées

2. **`creative_tablet`** (ex: Tab S11)
   - MDM: Baseline légère
   - Apps: Création, Prise de notes, IA
   - Télémétrie: Complète (ADB)
   - Notifications: Silenciées au maximum

3. **`watch`** (ex: Watch Ultra 2)
   - MDM: N/A
   - Apps: HA Companion Wear, Galaxy Wearable
   - Télémétrie: HA proxy via téléphone
   - Notifications: N/A (géré par téléphone)

4. **`media_tv`** (ex: Google TV)
   - MDM: N/A
   - Apps: Streaming uniquement
   - Télémétrie: HA (Android TV Remote)
   - Notifications: Désactivées

5. **`family_tablet`** (ex: Tab A)
   - MDM: BYOD ou Profil restreint
   - Apps: Divertissement, Éducation
   - Télémétrie: Basique (ADB)
   - Notifications: Standards

---

## 3. Registre des Devices (Hardware Registry)

Chaque appareil est enregistré dans `00_META/HARDWARE-REGISTRY.md` et possède une fiche détaillée dans `04_INTERFACES/android/fleet/AND-XXX-MODEL.md`.

**Nomenclature ID :** `AND-001`, `AND-002`, etc.

---

## 4. Implémentation : `yos-android-provision.sh`

Le cœur du framework est le script `yos-android-provision.sh` déployé sur le Cloud Computer. Ce script exécute les phases P2, P3, P4 (partiel) et P5 de manière automatisée, en fonction du profil spécifié.

**Usage :**
```bash
./yos-android-provision.sh --ip 100.x.x.x --id AND-002 --profile primary_phone
```
