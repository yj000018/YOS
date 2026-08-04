#!/bin/bash
# ==============================================================================
# Y-OS ANDROID OPERATOR — GALAXY Z FOLD 7 SETUP SCRIPT
# ==============================================================================
# Objectif : Préparer le Galaxy Z Fold 7 (Android 16 / One UI 8) dès réception
# Exécution : Depuis le Mac local (via câble USB ou ADB WiFi local)
# Date : 2026-08-05
# ==============================================================================

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Y-OS: Galaxy Z Fold 7 Setup ===${NC}"

# Vérification ADB
if ! command -v adb &> /dev/null; then
    echo -e "${RED}Erreur: ADB non installé sur ce Mac. Installe-le via 'brew install android-platform-tools'${NC}"
    exit 1
fi

# Détection de l'appareil
DEVICE=$(adb devices | grep -w "device" | awk '{print $1}')
if [ -z "$DEVICE" ]; then
    echo -e "${RED}Erreur: Aucun appareil ADB détecté.${NC}"
    echo "1. Connecte le Fold 7 via USB ou pair-le via Wireless Debugging"
    echo "2. Accepte l'empreinte RSA sur l'écran du téléphone"
    exit 1
fi

echo -e "${GREEN}✅ Appareil détecté : $DEVICE${NC}"

# ==============================================================================
# 1. DEBLOAT (Suppression des apps inutiles Samsung / Bloatware)
# ==============================================================================
echo -e "\n${BLUE}--- Étape 1 : Debloat Samsung ---${NC}"

# Liste des apps à désinstaller (bloatware classique)
REMOVE=(
    "com.microsoft.copilot"
    "com.samsung.android.bixby.wakeup"
    "com.samsung.android.bixby.agent"
    "com.samsung.android.bixby.visionui"
    "com.samsung.android.app.spage" # Samsung Free/O
    "com.sec.android.app.kidshome" # Kids Mode
    "com.samsung.android.tvplus"
    "com.samsung.ecomm.global.gbr" # Samsung Shop
    "com.samsung.android.themedesigner"
    "com.samsung.android.voc" # Samsung Members
    "com.sec.android.app.sbrowser.beta"
    "com.microsoft.appmanager" # Link to Windows (si non utilisé)
    "com.facebook.katana" # Facebook (si non désiré)
    "com.facebook.system"
    "com.facebook.appmanager"
    "com.facebook.services"
)

for pkg in "${REMOVE[@]}"; do
    echo "Suppression de $pkg..."
    adb -s "$DEVICE" uninstall --user 0 "$pkg" 2>/dev/null || echo "  -> Non installé ou échec"
done

# ==============================================================================
# 2. CONFIGURATION SYSTÈME (Settings)
# ==============================================================================
echo -e "\n${BLUE}--- Étape 2 : Configuration Système ---${NC}"

# Désactiver les animations (vitesse max)
adb -s "$DEVICE" shell settings put global window_animation_scale 0.0
adb -s "$DEVICE" shell settings put global transition_animation_scale 0.0
adb -s "$DEVICE" shell settings put global animator_duration_scale 0.0
echo "✅ Animations désactivées"

# Forcer le mode sombre
adb -s "$DEVICE" shell "cmd uimode night yes"
echo "✅ Mode sombre activé"

# ==============================================================================
# 3. INSTALLATION APPS Y-OS (via Play Store links pour le moment)
# ==============================================================================
echo -e "\n${BLUE}--- Étape 3 : Apps Y-OS à installer ---${NC}"
echo "Veuillez installer manuellement ces apps critiques depuis le Play Store :"
echo "1. Tailscale (com.tailscale.ipn)"
echo "2. Termux (com.termux) - via F-Droid de préférence"
echo "3. Home Assistant (io.homeassistant.companion.android)"
echo "4. Obsidian (md.obsidian)"
echo "5. Telegram (org.telegram.messenger)"

# ==============================================================================
# 4. PRÉPARATION TAILSCALE & ADB REMOTE
# ==============================================================================
echo -e "\n${BLUE}--- Étape 4 : Setup Tailscale & ADB Remote ---${NC}"
echo "Instructions pour finaliser la connexion avec le Cloud Computer :"
echo "1. Ouvre Tailscale sur le Fold 7, logge-toi, active le VPN."
echo "2. Note l'IP Tailscale (ex: 100.x.x.x)."
echo "3. Sur le Fold 7 : Paramètres -> Options Développeur -> Wireless Debugging -> ON."
echo "4. Ouvre Wireless Debugging -> Pair device with pairing code."
echo "5. Sur le Cloud Computer, lance :"
echo "   adb pair <IP_TAILSCALE>:<PORT> <CODE>"
echo "   adb connect <IP_TAILSCALE>:5555"

echo -e "\n${GREEN}=== Setup local terminé ===${NC}"
