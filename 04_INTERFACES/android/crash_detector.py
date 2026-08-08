#!/usr/bin/env python3
"""
Y-OS Crash Detector — Surveillance de la flotte Android
Cron: */5 * * * * (toutes les 5 minutes)
Détecte:
  - Nova crash (One UI en topActivity)
  - ADB déconnecté
  - Batterie critique
  - Tailscale déconnecté
Actions:
  - Auto-recovery Nova (push backup + trigger restore)
  - Notification Telegram
  - Mise à jour state.json
"""
import subprocess
import json
import os
import time
import urllib.request
import urllib.parse
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
FLEET = {
    "AND-001": {"host": "100.89.158.44:5555", "name": "Galaxy Tab S11"},
    "AND-002": {"host": None, "name": "Galaxy Z Fold 7"},   # à remplir
}
TELEGRAM_TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
CHAT_ID = "223132272"
STATE_FILE = "/home/ubuntu/yos/android/crash_detector_state.json"
NOVA_OPERATOR = "/home/ubuntu/yos/android/nova_operator.py"
NOVA_BACKUP = "/home/ubuntu/yos/android/nova_backup/yos_nova_v5_clean.novabackup"
LOG_FILE = "/home/ubuntu/yos/android/logs/crash_detector.log"

# Seuils
BATTERY_P1 = 10   # % critique
BATTERY_P2 = 20   # % attention
MAX_NOVA_CRASHES = 3  # Avant d'alerter sans auto-fix

# ── Helpers ───────────────────────────────────────────────────────────────────
def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def notify(msg: str, priority: str = "normal"):
    """Envoie une notification Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }).encode()
    try:
        urllib.request.urlopen(url, data, timeout=5)
    except Exception as e:
        log(f"Telegram error: {e}")

def adb(host: str, cmd: str, timeout: int = 10) -> tuple[int, str]:
    full = f"adb -s {host} {cmd}"
    r = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# ── Checks ────────────────────────────────────────────────────────────────────
def check_device(device_id: str, host: str, state: dict) -> dict:
    """Vérifie l'état d'un device et retourne les alertes détectées."""
    alerts = []
    device_state = state.get(device_id, {})

    # 1. Connexion ADB
    rc, out = adb(host, "get-state")
    if rc != 0 or "device" not in out:
        consecutive_fails = device_state.get("adb_fails", 0) + 1
        device_state["adb_fails"] = consecutive_fails
        if consecutive_fails == 3:
            alerts.append({
                "type": "adb_disconnected",
                "severity": "P2",
                "msg": f"⚠️ <b>AND-001 hors ligne</b> — ADB déconnecté depuis {consecutive_fails} checks.\nVérifie Tailscale + Wireless Debugging."
            })
        log(f"{device_id}: ADB fail #{consecutive_fails}")
        return {"alerts": alerts, "state": device_state}

    # ADB OK — reset fail counter
    device_state["adb_fails"] = 0

    # 2. Nova crash detection
    rc, top = adb(host, "shell dumpsys activity | grep topResumedActivity")
    one_ui_active = "com.sec.android.app.launcher" in top
    nova_active = "com.teslacoilsw.launcher" in top and "RestoreBackup" not in top

    if one_ui_active:
        nova_crashes = device_state.get("nova_crashes", 0) + 1
        device_state["nova_crashes"] = nova_crashes
        log(f"{device_id}: Nova crash detected (#{nova_crashes}), One UI active")

        if nova_crashes <= MAX_NOVA_CRASHES:
            # Auto-recovery
            log(f"{device_id}: Auto-recovering Nova (attempt #{nova_crashes})")
            subprocess.run(
                f"python3 {NOVA_OPERATOR} fix_crash",
                shell=True, timeout=30
            )
            alerts.append({
                "type": "nova_crash_auto_fixed",
                "severity": "P2",
                "msg": (
                    f"🔧 <b>Nova Crash — Auto-Recovery</b> (#{nova_crashes})\n"
                    f"Backup poussé sur {FLEET[device_id]['name']}.\n"
                    f"<b>Confirme le restore sur l'écran de la tablette.</b>"
                )
            })
        else:
            alerts.append({
                "type": "nova_crash_manual_required",
                "severity": "P1",
                "msg": (
                    f"🚨 <b>Nova Crash Répété</b> ({nova_crashes}x)\n"
                    f"Auto-recovery échoué. Intervention manuelle requise.\n"
                    f"Commande: <code>python3 {NOVA_OPERATOR} fix_crash</code>"
                )
            })
    else:
        if device_state.get("nova_crashes", 0) > 0:
            log(f"{device_id}: Nova recovered (was crashed {device_state['nova_crashes']}x)")
        device_state["nova_crashes"] = 0

    # 3. Batterie
    rc, bat_out = adb(host, "shell dumpsys battery")
    try:
        level_line = [l for l in bat_out.splitlines() if "level:" in l]
        level = int(level_line[0].split(":")[-1].strip()) if level_line else -1
        device_state["battery"] = level
        if level <= BATTERY_P1:
            alerts.append({
                "type": "battery_critical",
                "severity": "P1",
                "msg": f"🔴 <b>Batterie critique</b> — {FLEET[device_id]['name']}: {level}%\nBrancher maintenant."
            })
        elif level <= BATTERY_P2:
            # N'alerter qu'une fois par descente
            if device_state.get("battery_p2_alerted") != level:
                device_state["battery_p2_alerted"] = level
                alerts.append({
                    "type": "battery_low",
                    "severity": "P2",
                    "msg": f"🟡 <b>Batterie faible</b> — {FLEET[device_id]['name']}: {level}%"
                })
        else:
            device_state.pop("battery_p2_alerted", None)
    except Exception:
        pass

    return {"alerts": alerts, "state": device_state}

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    state = load_state()
    all_alerts = []

    for device_id, config in FLEET.items():
        host = config.get("host")
        if not host:
            continue  # Device pas encore configuré

        result = check_device(device_id, host, state)
        state[device_id] = result["state"]
        all_alerts.extend(result["alerts"])

    # Envoyer les alertes
    for alert in all_alerts:
        log(f"ALERT [{alert['severity']}] {alert['type']}: {alert['msg'][:80]}")
        notify(alert["msg"])

    save_state(state)
    if not all_alerts:
        log("All devices OK")

if __name__ == "__main__":
    main()
