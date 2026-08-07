#!/bin/bash
# ============================================================
# Y-OS Android Provisioning Framework — Core Script
# Version : 1.0 — 2026-08-07
# Usage   : ./yos-android-provision.sh --ip <IP:PORT> --id <AND-XXX> --profile <PROFILE> [--phases P2,P3,P4,P5]
# Profiles: primary_phone | creative_tablet | watch | media_tv | family_tablet
# ============================================================

set -euo pipefail

# ─── Couleurs ───────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
OK="${GREEN}✅${NC}"; WARN="${YELLOW}⚠️${NC}"; ERR="${RED}❌${NC}"; INFO="${CYAN}ℹ️${NC}"

# ─── Defaults ───────────────────────────────────────────────
ADB_HOST=""
DEVICE_ID=""
PROFILE=""
PHASES="P2,P3,P4,P5"
TELEGRAM_TOKEN="8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
CHAT_ID="223132272"
REPO_DIR="/home/ubuntu/yos-repo"
SCRIPTS_DIR="/home/ubuntu/yos/android/provision"
LOG_FILE="/home/ubuntu/yos/android/logs/provision_$(date +%Y%m%d_%H%M%S).log"

# ─── Parse args ─────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case $1 in
        --ip)     ADB_HOST="$2"; shift 2 ;;
        --id)     DEVICE_ID="$2"; shift 2 ;;
        --profile) PROFILE="$2"; shift 2 ;;
        --phases) PHASES="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

[[ -z "$ADB_HOST" ]] && { echo -e "${ERR} --ip requis"; exit 1; }
[[ -z "$DEVICE_ID" ]] && { echo -e "${ERR} --id requis"; exit 1; }
[[ -z "$PROFILE" ]] && { echo -e "${ERR} --profile requis"; exit 1; }

ADB="adb -s $ADB_HOST"
mkdir -p "$(dirname $LOG_FILE)"

# ─── Helpers ────────────────────────────────────────────────
log() { echo -e "$1" | tee -a "$LOG_FILE"; }
adb_run() { $ADB shell "$@" 2>/dev/null || true; }
notify() {
    curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}&text=$1&parse_mode=HTML" > /dev/null 2>&1
}
phase_in() { echo "$PHASES" | grep -q "$1"; }

# ─── Vérification ADB ───────────────────────────────────────
check_adb() {
    log "\n${BLUE}=== Vérification ADB ===${NC}"
    if ! $ADB shell echo OK 2>/dev/null | grep -q OK; then
        log "${ERR} ADB non joignable sur $ADB_HOST"
        exit 1
    fi
    MODEL=$(adb_run getprop ro.product.model)
    ANDROID=$(adb_run getprop ro.build.version.release)
    log "${OK} ADB connecté — $MODEL (Android $ANDROID)"
}

# ─── P2 : Debloat ───────────────────────────────────────────
phase_p2_debloat() {
    log "\n${BLUE}=== P2 — Purification (Debloat) ===${NC}"

    # Apps universelles à supprimer (tous profils sauf watch/media_tv)
    UNIVERSAL_REMOVE=(
        # IA doublons
        "com.microsoft.copilot"
        "com.poe.android"
        "com.scaleup.chatai"
        "com.jetkite.gemmy"
        "com.hubx.imagination"
        "ai.inflection.pi"
        "ai.perplexity.comet"
        # Shopping agressif
        "com.einnovation.temu"
        "com.alibaba.aliexpresshd"
        # Streaming doublons
        "com.amazon.mp3"
        "tv.pluto.android"
        # Gadgets inutiles
        "com.ucapan.tahunbaru.lengkap.app.ultraios"
        "com.innosq.soundtypeai"
        "com.chancevisionai.app"
        "app.aworld"
        # Samsung bloat
        "com.samsung.android.bixby.ondevice.itit"
        "com.samsung.android.bixby.ondevice.dede"
        "com.samsung.android.nmt.apps.t2t.languagepack.ende"
        "com.samsung.android.nmt.apps.t2t.languagepack.enit"
        "com.samsung.SMT.lang_de_de_l01"
        "com.samsung.SMT.lang_it_it_g01"
        "com.samsung.SMT.lang_it_it_l01"
        "com.samsung.android.tvplus"
        "com.samsung.android.voc"
        "com.samsung.android.homemode"
        "com.samsung.android.themedesigner"
        "com.samsung.ecomm.global.gbr"
        "com.sec.android.app.kidshome"
        "com.samsung.android.app.tips"
        # Google bloat
        "com.google.android.apps.googleassistant"
        "com.google.android.apps.labs.language.tailwind"
        "com.google.android.safetycore"
        "com.google.android.contactkeys"
    )

    # Apps spécifiques primary_phone à supprimer
    PHONE_REMOVE=(
        "com.samsung.android.game.gamehome"
        "com.samsung.android.themestore"
        "com.alohamobile.browser"
        "com.chrome.beta"
        "com.chrome.dev"
        "com.sec.android.app.sbrowser.beta"
    )

    # Apps spécifiques creative_tablet à supprimer
    TABLET_REMOVE=(
        "com.gameloft.android.ANMP.GloftA8HM"
        "com.gameloft.android.ANMP.GloftA9HM"
        "com.lilithgame.roc.gp"
        "com.proximabeta.aoemobile"
        "com.samsung.android.game.gamehome"
    )

    REMOVE_LIST=("${UNIVERSAL_REMOVE[@]}")
    [[ "$PROFILE" == "primary_phone" ]] && REMOVE_LIST+=("${PHONE_REMOVE[@]}")
    [[ "$PROFILE" == "creative_tablet" ]] && REMOVE_LIST+=("${TABLET_REMOVE[@]}")

    REMOVED=0; SKIPPED=0
    for pkg in "${REMOVE_LIST[@]}"; do
        if $ADB shell pm list packages | grep -q "^package:${pkg}$"; then
            $ADB shell pm uninstall --user 0 "$pkg" > /dev/null 2>&1 && \
                log "  🗑️  Supprimé : $pkg" && ((REMOVED++)) || \
                log "  ${WARN} Échec suppression : $pkg"
        else
            ((SKIPPED++))
        fi
    done
    log "${OK} Debloat terminé — $REMOVED supprimés, $SKIPPED absents"
}

# ─── P3 : Silence ───────────────────────────────────────────
phase_p3_silence() {
    log "\n${BLUE}=== P3 — Silence (Anti-Bruit) ===${NC}"

    # Désactiver notifications apps sociales/spam
    SILENCE_APPS=(
        "com.facebook.katana"
        "com.facebook.stella"
        "com.instagram.android"
        "com.amazon.mp3"
        "tv.pluto.android"
        "com.samsung.android.themestore"
        "com.samsung.android.game.gamehome"
    )

    for pkg in "${SILENCE_APPS[@]}"; do
        if $ADB shell pm list packages | grep -q "^package:${pkg}$"; then
            $ADB shell cmd appops set "$pkg" POST_NOTIFICATION deny 2>/dev/null || true
            log "  🔕 Silencé : $pkg"
        fi
    done

    # Paramètres système
    adb_run settings put global heads_up_notifications_enabled 1
    adb_run settings put secure lock_screen_show_notifications 1
    log "${OK} Paramètres notifications configurés"

    # Exemption batterie pour apps critiques
    BATTERY_EXEMPT=(
        "com.tailscale.ipn.android"
        "io.homeassistant.companion.android"
        "com.pushover.Pushover"
    )
    for pkg in "${BATTERY_EXEMPT[@]}"; do
        if $ADB shell pm list packages | grep -q "^package:${pkg}$"; then
            adb_run dumpsys deviceidle whitelist "+$pkg" 2>/dev/null || true
            log "  🔋 Exempté batterie : $pkg"
        fi
    done
    log "${OK} Silence terminé"
}

# ─── P4 : Base Apps & Config ────────────────────────────────
phase_p4_config() {
    log "\n${BLUE}=== P4 — Base Config ===${NC}"

    # Paramètres universels
    log "  Configuration paramètres système..."
    adb_run settings put global animator_duration_scale 0.5
    adb_run settings put global transition_animation_scale 0.5
    adb_run settings put global window_animation_scale 0.5
    log "  ${OK} Animations accélérées (0.5x)"

    # Adaptive Battery
    adb_run settings put global adaptive_battery_management_enabled 1
    log "  ${OK} Adaptive Battery activé"

    # Désactiver son clavier
    adb_run settings put system sound_effects_enabled 0
    log "  ${OK} Sons système désactivés"

    # Profil-specific
    case "$PROFILE" in
        primary_phone)
            log "  ${INFO} Profil primary_phone — config spécifique..."
            adb_run settings put system screen_off_timeout 120000  # 2 min
            adb_run settings put global stay_on_while_plugged_in 0
            ;;
        creative_tablet)
            log "  ${INFO} Profil creative_tablet — config spécifique..."
            adb_run settings put system screen_off_timeout 600000  # 10 min
            adb_run settings put global stay_on_while_plugged_in 2  # Rester allumé sur secteur
            ;;
        media_tv)
            log "  ${INFO} Profil media_tv — config spécifique..."
            adb_run settings put system screen_off_timeout 1800000  # 30 min
            ;;
        family_tablet)
            log "  ${INFO} Profil family_tablet — config spécifique..."
            adb_run settings put system screen_off_timeout 300000  # 5 min
            ;;
    esac

    log "${OK} Config système terminée"
    log ""
    log "  ${INFO} Apps à installer manuellement (Play Store) :"
    case "$PROFILE" in
        primary_phone|creative_tablet)
            log "    1. Tailscale — CRITIQUE (ADB remote)"
            log "    2. Claude"
            log "    3. ChatGPT"
            log "    4. Perplexity"
            log "    5. Obsidian"
            log "    6. Notion"
            log "    7. Home Assistant (quand N100 prêt)"
            log "    8. Telegram"
            log "    9. Brave Browser"
            ;;
        watch)
            log "    1. Galaxy Wearable (sur téléphone compagnon)"
            log "    2. HA Companion Wear (quand N100 prêt)"
            ;;
        media_tv)
            log "    1. Home Assistant (Android TV Remote)"
            ;;
    esac
}

# ─── P5 : Monitoring ────────────────────────────────────────
phase_p5_monitoring() {
    log "\n${BLUE}=== P5 — Monitoring & Fleet ===${NC}"

    # Snapshot packages initial
    SNAP_DIR="/home/ubuntu/yos/android/snapshots"
    mkdir -p "$SNAP_DIR"
    SNAP_FILE="$SNAP_DIR/${DEVICE_ID}_packages_latest.json"
    TODAY=$(date +%Y-%m-%d)

    PKGS=$($ADB shell pm list packages -3 2>/dev/null | sed 's/package://g' | sort)
    PKG_COUNT=$(echo "$PKGS" | wc -l)
    echo "{\"device_id\":\"$DEVICE_ID\",\"date\":\"$TODAY\",\"count\":$PKG_COUNT,\"packages\":$(echo "$PKGS" | python3 -c 'import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')}" > "$SNAP_FILE"
    log "${OK} Snapshot initial : $PKG_COUNT apps → $SNAP_FILE"

    # Métriques santé
    BAT=$(adb_run dumpsys battery | grep -A 20 "Current Battery Service state" | grep "level:" | head -1 | awk '{print $2}')
    MODEL=$(adb_run getprop ro.product.model)
    ANDROID=$(adb_run getprop ro.build.version.release)

    log "${OK} Snapshot santé : bat=${BAT}%, apps=$PKG_COUNT"

    # Notif Telegram
    notify "🎉 <b>$DEVICE_ID ($MODEL) — Provisioning terminé</b>

📋 Profil : $PROFILE
🤖 Android $ANDROID
🔋 Batterie : ${BAT}%
📱 Apps tierces : $PKG_COUNT
📅 Date : $TODAY

Phases exécutées : $PHASES
Prochaine étape : Installer Tailscale + apps manuelles"

    log "${OK} Notif Telegram envoyée"
    log ""
    log "${INFO} Prochaine étape manuelle :"
    log "  → Mettre à jour health_probe.py avec : \"$DEVICE_ID\": {\"adb_host\": \"$ADB_HOST\"}"
    log "  → Mettre à jour drift_packages.py avec le même"
}

# ─── MAIN ───────────────────────────────────────────────────
log "\n${CYAN}╔══════════════════════════════════════════════════╗${NC}"
log "${CYAN}║  Y-OS Android Provisioning — $DEVICE_ID          ${NC}"
log "${CYAN}║  Profil: $PROFILE — Phases: $PHASES   ${NC}"
log "${CYAN}╚══════════════════════════════════════════════════╝${NC}"

check_adb
phase_in "P2" && phase_p2_debloat
phase_in "P3" && phase_p3_silence
phase_in "P4" && phase_p4_config
phase_in "P5" && phase_p5_monitoring

log "\n${GREEN}╔══════════════════════════════════════════════════╗${NC}"
log "${GREEN}║  ✅ Provisioning $DEVICE_ID terminé              ${NC}"
log "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
log "Log complet : $LOG_FILE"
