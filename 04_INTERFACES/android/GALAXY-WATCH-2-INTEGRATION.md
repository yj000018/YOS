# Y-OS Integration : Galaxy Watch 2 (Wear OS)
> **Statut** : Document d'architecture (Prêt pour réception J+3)
> **Date** : 2026-08-05

## Contexte
Contrairement aux tablettes (Tab S11) et téléphones (Fold 7) sous Android complet, la Galaxy Watch 2 tourne sous **Wear OS 5 / One UI Watch 7**. 
L'intégration Y-OS est différente car **Tailscale n'est pas disponible sur Wear OS**. L'accès ADB direct via internet depuis le Cloud Computer n'est donc pas possible nativement.

---

## 1. Méthodes de connexion ADB

### Option A : ADB via Wi-Fi local (Mac)
C'est la méthode la plus simple pour le setup initial ou le sideloading d'apps.
1. Connecter la montre au **même réseau Wi-Fi** que le Mac.
2. Sur la montre : `Paramètres > À propos de la montre > Logiciel > Tap 7x sur Version logicielle` (Active le mode dev).
3. `Paramètres > Options de développement > Débogage ADB (ON) > Débogage sans fil (ON)`.
4. Noter l'IP affichée (ex: `192.168.1.105:5555`).
5. Sur le Mac : `adb connect 192.168.1.105:5555`.

### Option B : ADB via Bluetooth (Relais via Fold 7)
Utile si pas de Wi-Fi. Le téléphone sert de pont.
1. Activer le débogage Bluetooth sur la montre.
2. Sur le téléphone (Fold 7), activer le débogage USB/Wireless.
3. Dans l'app Galaxy Wearable sur le téléphone, activer le relais de débogage.
4. Sur le Mac (connecté au téléphone) :
   ```bash
   adb forward tcp:4444 localabstract:/adb-hub
   adb connect 127.0.0.1:4444
   ```

### Option C : ADB via Câble (si supporté)
Certaines montres supportent un dock USB avec data, mais la plupart des modèles récents (Watch 4/5/6/7) utilisent la charge sans fil pure sans data pin. L'Option A (Wi-Fi) est le standard absolu pour Wear OS.

---

## 2. Stratégie Y-OS : Abstraction via Home Assistant (Recommandé ⭐)

Étant donné l'absence de Tailscale sur la montre, un contrôle ADB remote direct depuis le Cloud Computer est complexe et instable (nécessiterait de router le trafic via le téléphone en permanence).

**La solution canonique Y-OS pour la montre est l'intégration Home Assistant.**

### Pourquoi Home Assistant ?
- **Autonomie** : L'app Home Assistant Wear OS envoie les données directement au serveur HA (qui est accessible via le Cloud Computer).
- **Capteurs** : Remonte la batterie, le statut de charge, le podomètre, la détection de sommeil, et la localisation.
- **Actions** : Permet de déclencher des scripts Y-OS directement depuis le poignet (via des tuiles/complications HA).

### Setup Home Assistant Wear OS
1. Installer l'app Home Assistant sur la montre (via le Play Store de la montre).
2. Se connecter au serveur HA d'Anandaz.
3. Activer tous les capteurs (Sensors) dans l'app HA sur la montre.
4. Créer des "Tuiles" (Tiles) pour les actions rapides Y-OS (ex: "Log Idea", "Trigger Night Pipeline").

---

## 3. Données de Santé (Samsung Health)

Les données de santé (BPM, ECG, Sommeil profond) ne sont pas facilement accessibles via ADB.
- **Pipeline** : Montre → Samsung Health (Téléphone) → Google Health Connect → Home Assistant / API.
- L'intégration de ces données dans le KAP (Knowledge Acquisition Protocol) de Y-OS se fera en interrogeant l'API Home Assistant ou via un export programmé depuis le téléphone.

---

## Résumé des Actions à Réception
1. Appairer la montre avec le Galaxy Z Fold 7.
2. Activer le mode développeur sur la montre.
3. Connecter la montre au Wi-Fi local et utiliser `adb connect` depuis le Mac pour le setup initial (sideloading si nécessaire).
4. Installer **Home Assistant** sur la montre.
5. Configurer les capteurs et les tuiles HA.
6. Intégrer les entités de la montre dans les dashboards Y-OS via l'API HA.
