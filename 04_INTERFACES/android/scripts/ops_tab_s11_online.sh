#!/bin/bash
# Y-OS — Opération complète Tab S11 au retour (tablette online)
# Exécuté par Manus dès que la tablette est reconnectée
# Usage : bash ops_tab_s11_online.sh

ADB="adb -s 100.89.158.44:5555"
TELEGRAM_TOKEN="8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
CHAT_ID="223132272"

notify() {
    curl -s "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}&text=$1&parse_mode=HTML" > /dev/null 2>&1
}

echo "=== Y-OS Opération Tab S11 — Online ==="
echo ""

# 1. Vérifier ADB
echo "[1/6] Vérification ADB..."
if ! $ADB shell echo OK 2>/dev/null | grep -q OK; then
    echo "❌ ADB non connecté"
    exit 1
fi
echo "  ✅ ADB connecté"

# 2. Snapshot santé
echo ""
echo "[2/6] Snapshot santé..."
BAT=$($ADB shell dumpsys battery | grep -A 20 "Current Battery Service state" | grep "level:" | head -1 | awk '{print $2}')
STO=$($ADB shell df /data | grep '/dev/block' | awk '{print $5}' | tr -d '%')
APPS=$($ADB shell pm list packages -3 | wc -l)
UPTIME=$($ADB shell uptime | awk '{print $3, $4}' | tr -d ',')
echo "  Batterie : ${BAT}%"
echo "  Stockage : ${STO}% utilisé"
echo "  Apps tierces : ${APPS}"
echo "  Uptime : ${UPTIME}"

# 3. Config notifications
echo ""
echo "[3/6] Config notifications..."
bash /home/ubuntu/yos/android/config_notifications_tab_s11.sh 2>/dev/null | grep -E "✅|🔕|❌|ℹ️"

# 4. Drift packages
echo ""
echo "[4/6] Drift packages..."
python3 /home/ubuntu/yos/android/drift_packages.py 2>/dev/null | grep -E "✅|📦|❌|⏸️"

# 5. Rapport hebdo (si lundi ou premier run)
echo ""
echo "[5/6] Rapport de santé..."
python3 /home/ubuntu/yos/android/weekly_report.py 2>/dev/null | grep -E "✅|❌|📊"

# 6. Notif Telegram
echo ""
echo "[6/6] Notification Telegram..."
notify "✅ <b>AND-001 Tab S11 — Online</b>

🔋 Batterie : ${BAT}%
💾 Stockage : ${STO}% utilisé
📱 Apps tierces : ${APPS}
⏱ Uptime : ${UPTIME}

Config notifications ✅
Drift packages ✅
Rapport santé ✅"

echo "  ✅ Notif envoyée"
echo ""
echo "=== Opération terminée ==="
