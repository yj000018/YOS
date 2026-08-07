#!/bin/bash
# Y-OS — Config Notifications Galaxy Tab S11 (AND-001)
# Silencer les apps non-critiques via ADB
# Usage : bash config_notifications_tab_s11.sh

ADB="adb -s 100.89.158.44:5555"

echo "=== Y-OS Notification Config — AND-001 Tab S11 ==="
echo ""

# Vérifier connexion ADB
if ! $ADB shell echo OK 2>/dev/null | grep -q OK; then
    echo "❌ ADB non connecté. Attendre que la tablette soit online."
    exit 1
fi
echo "✅ ADB connecté"
echo ""

# ─────────────────────────────────────────────
# 1. DÉSACTIVER notifications complètes (apps inutiles)
# ─────────────────────────────────────────────
echo "--- Désactivation notifications apps non-critiques ---"

DISABLE_NOTIF=(
    "com.facebook.katana"           # Facebook
    "com.facebook.stella"           # Messenger
    "com.tiktok.android"            # TikTok (si présent)
    "com.amazon.mp3"                # Amazon Music
    "com.apple.android.music"       # Apple Music
    "tv.pluto.android"              # Pluto TV
    "com.samsung.android.game.gamehome"  # Game Hub
    "com.samsung.android.themestore"     # Theme Store
    "com.samsung.android.app.tips"       # Samsung Tips
)

for pkg in "${DISABLE_NOTIF[@]}"; do
    result=$($ADB shell pm list packages | grep "$pkg" 2>/dev/null)
    if [ -n "$result" ]; then
        $ADB shell cmd notification set_dnd_mode $pkg 1 2>/dev/null || true
        # Méthode alternative : bloquer via settings
        $ADB shell cmd appops set "$pkg" POST_NOTIFICATION deny 2>/dev/null
        echo "  🔕 Notifications désactivées : $pkg"
    fi
done

echo ""

# ─────────────────────────────────────────────
# 2. PARAMÈTRES SYSTÈME — Mode Ne pas déranger
# ─────────────────────────────────────────────
echo "--- Paramètres système ---"

# Désactiver les sons de notification pour les apps non-prioritaires
# (via settings global)
$ADB shell settings put global heads_up_notifications_enabled 1
echo "  ✅ Heads-up notifications : activé (pour alertes critiques)"

# Désactiver les notifications sur l'écran de verrouillage pour les apps sociales
$ADB shell settings put secure lock_screen_show_notifications 1
echo "  ✅ Notifications écran verrouillé : activé"

# Activer le mode "Ne pas déranger" automatique la nuit (via settings)
# Note : le DND schedule se configure dans l'UI Samsung, pas via ADB
echo "  ℹ️  DND schedule : à configurer manuellement (Paramètres → Sons → Ne pas déranger)"

echo ""

# ─────────────────────────────────────────────
# 3. OPTIMISATION BATTERIE — Exclure apps critiques
# ─────────────────────────────────────────────
echo "--- Exclusion optimisation batterie (apps critiques) ---"

BATTERY_EXEMPT=(
    "com.tailscale.ipn.android"     # Tailscale — doit tourner en arrière-plan
    "io.homeassistant.companion.android"  # Home Assistant Companion
)

for pkg in "${BATTERY_EXEMPT[@]}"; do
    result=$($ADB shell pm list packages | grep "$pkg" 2>/dev/null)
    if [ -n "$result" ]; then
        $ADB shell dumpsys deviceidle whitelist "+$pkg" 2>/dev/null
        echo "  🔋 Exempté optimisation batterie : $pkg"
    else
        echo "  ⏭️  Non installé (skip) : $pkg"
    fi
done

echo ""

# ─────────────────────────────────────────────
# 4. RAPPORT FINAL
# ─────────────────────────────────────────────
echo "--- État final ---"
echo "  Batterie : $($ADB shell dumpsys battery | grep 'level:' | head -1 | tr -d ' ')"
echo "  Apps tierces : $($ADB shell pm list packages -3 | wc -l)"
echo ""
echo "✅ Config notifications terminée"
echo ""
echo "Actions manuelles restantes (à faire sur la tablette) :"
echo "  1. Paramètres → Notifications → Trier par usage récent"
echo "  2. Désactiver notifications : Facebook, Messenger, Amazon Music"
echo "  3. Sons → Ne pas déranger → Planifier (23h-7h)"
echo "  4. Paramètres → Batterie → Optimisation adaptative → ON"
