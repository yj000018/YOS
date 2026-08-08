#!/usr/bin/env python3
"""
Y-OS Nova Operator — Gestion complète de Nova Launcher via ADB
Usage:
  python3 nova_operator.py status
  python3 nova_operator.py push_restore [backup_path]
  python3 nova_operator.py add_app <package> <group_id>
  python3 nova_operator.py add_group <group_id> <group_name>
  python3 nova_operator.py set_gesture <gesture> <action>
  python3 nova_operator.py backup_pull [output_path]
  python3 nova_operator.py fix_crash
"""
import subprocess
import sqlite3
import zipfile
import shutil
import os
import sys
import re
import json
import time
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
ADB_TARGET = "100.89.158.44:5555"
NOVA_PKG = "com.teslacoilsw.launcher"
NOVA_MAIN = f"{NOVA_PKG}/.NovaLauncher"
NOVA_RESTORE_HANDLER = f"{NOVA_PKG}/.RestoreBackupFileHandler"
BACKUP_DIR = "/home/ubuntu/yos/android/nova_backup"
CANONICAL_BACKUP = os.path.join(BACKUP_DIR, "yos_nova_v5_clean.novabackup")
DEVICE_BACKUP_PATH = "/sdcard/Download/yos_nova_v5_clean.novabackup"
TELEGRAM_TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
CHAT_ID = "223132272"

# ── Gesture mapping ───────────────────────────────────────────────────────────
GESTURE_MAP = {
    "swipe_down": "gesture_swipe_down",
    "swipe_up": "gesture_swipe_up",
    "swipe_left": "gesture_swipe_left",
    "swipe_right": "gesture_swipe_right",
    "double_tap": "gesture_double_tap",
    "pinch": "gesture_pinch",
}
GESTURE_ACTIONS = {
    "nova_search": "5",
    "notifications": "1",
    "app_drawer": "2",
    "none": "0",
    "assistant": "6",
    "recents": "7",
}

# ── ADB helpers ───────────────────────────────────────────────────────────────
def adb(cmd: str, timeout: int = 10) -> tuple[int, str, str]:
    full_cmd = f"adb -s {ADB_TARGET} {cmd}"
    r = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

def adb_ok() -> bool:
    rc, out, _ = adb("get-state")
    return rc == 0 and out == "device"

def notify(msg: str):
    import urllib.request, urllib.parse
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
    try:
        urllib.request.urlopen(url, data, timeout=5)
    except Exception:
        pass

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

# ── Nova state ────────────────────────────────────────────────────────────────
def nova_status() -> dict:
    """Retourne l'état complet de Nova sur l'appareil."""
    if not adb_ok():
        return {"connected": False, "error": "ADB not connected"}

    # Version
    rc, out, _ = adb(f"shell dumpsys package {NOVA_PKG} | grep versionName")
    version = out.split("=")[-1].strip() if "=" in out else "unknown"

    # Top activity
    rc, top, _ = adb("shell dumpsys activity | grep topResumedActivity")
    is_nova_active = NOVA_PKG in top
    is_one_ui = "com.sec.android.app.launcher" in top

    # Backup sur device
    rc, ls, _ = adb(f"shell ls /sdcard/Download/*.novabackup 2>/dev/null")
    backups = [b.strip() for b in ls.splitlines() if b.strip()] if rc == 0 else []

    return {
        "connected": True,
        "version": version,
        "active": is_nova_active,
        "one_ui_fallback": is_one_ui,
        "backups_on_device": backups,
        "canonical_backup_exists": os.path.exists(CANONICAL_BACKUP),
    }

# ── Backup edit ───────────────────────────────────────────────────────────────
def load_backup(backup_path: str) -> tuple[str, str]:
    """Extrait le backup dans /tmp et retourne (extract_dir, db_path)."""
    extract_dir = "/tmp/nova_operator_edit"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)
    with zipfile.ZipFile(backup_path) as z:
        z.extractall(extract_dir)
    db_path = None
    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            if f.endswith(".db"):
                db_path = os.path.join(root, f)
                break
    if not db_path:
        raise FileNotFoundError("nova.db not found in backup")
    return extract_dir, db_path

def save_backup(extract_dir: str, output_path: str):
    """Re-zippe le dossier édité en backup."""
    if os.path.exists(output_path):
        os.remove(output_path)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                fp = os.path.join(root, file)
                zout.write(fp, os.path.relpath(fp, extract_dir))

def edit_xml(extract_dir: str, key: str, value: str, val_type: str = "string"):
    """Modifie nova.xml pour un paramètre donné."""
    xml_path = os.path.join(extract_dir, "nova.xml")
    with open(xml_path, "r") as f:
        xml = f.read()
    if val_type == "string":
        pattern = f'<string name="{key}">[^<]*</string>'
        replacement = f'<string name="{key}">{value}</string>'
        if re.search(pattern, xml):
            xml = re.sub(pattern, replacement, xml)
        else:
            xml = xml.replace("</map>", f'    <string name="{key}">{value}</string>\n</map>')
    elif val_type == "boolean":
        pattern = f'<boolean name="{key}" value="[^"]*"'
        replacement = f'<boolean name="{key}" value="{value}"'
        if re.search(pattern, xml):
            xml = re.sub(pattern, replacement, xml)
        else:
            xml = xml.replace("</map>", f'    <boolean name="{key}" value="{value}" />\n</map>')
    with open(xml_path, "w") as f:
        f.write(xml)

# ── Push & Restore ────────────────────────────────────────────────────────────
def push_and_trigger_restore(backup_path: str, device_path: str = None) -> bool:
    """
    Push le backup sur l'appareil et déclenche le RestoreBackupFileHandler.
    L'utilisateur doit confirmer sur l'écran (1 tap).
    """
    if device_path is None:
        device_path = f"/sdcard/Download/{os.path.basename(backup_path)}"

    log(f"Pushing {backup_path} → {device_path}")
    rc, out, err = adb(f"push {backup_path} {device_path}", timeout=30)
    if rc != 0:
        log(f"Push failed: {err}")
        return False

    log("Triggering RestoreBackupFileHandler...")
    # Force Nova au premier plan
    adb(f"shell am force-stop {NOVA_PKG}")
    time.sleep(1)
    adb(f"shell am start -n {NOVA_MAIN}")
    time.sleep(2)

    # Déclencher le restore
    rc, out, err = adb(
        f'shell am start -a android.intent.action.VIEW '
        f'-t "application/vnd.novalauncher.backup" '
        f'-d "file://{device_path}" '
        f'{NOVA_RESTORE_HANDLER}'
    )
    if rc != 0:
        log(f"Restore trigger failed: {err}")
        return False

    log("Restore dialog triggered — user must confirm on screen")
    return True

# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_status():
    s = nova_status()
    if not s["connected"]:
        print(f"❌ ADB not connected: {s.get('error')}")
        return
    print(f"Nova version: {s['version']}")
    print(f"Nova active: {'✅' if s['active'] else '❌'}")
    print(f"One UI fallback: {'⚠️ YES' if s['one_ui_fallback'] else '✅ No'}")
    print(f"Backups on device: {s['backups_on_device']}")
    print(f"Canonical backup exists: {'✅' if s['canonical_backup_exists'] else '❌'}")

def cmd_push_restore(backup_path: str = None):
    if backup_path is None:
        backup_path = CANONICAL_BACKUP
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_path}")
        return
    if not adb_ok():
        print("❌ ADB not connected")
        return
    ok = push_and_trigger_restore(backup_path)
    if ok:
        notify("🔄 <b>Nova Restore</b> — Backup poussé. <b>Confirme sur l'écran de la tablette.</b>")
        print("✅ Restore triggered. Confirm on tablet screen.")
    else:
        print("❌ Restore failed")

def cmd_add_app(package: str, group_id: int):
    """Ajoute une app à un groupe Nova dans le backup canonique."""
    if not os.path.exists(CANONICAL_BACKUP):
        print(f"❌ Canonical backup not found: {CANONICAL_BACKUP}")
        return

    # Récupérer le composant principal de l'app
    rc, out, _ = adb(f"shell dumpsys package {package} | grep -A1 'android.intent.action.MAIN'")
    # Chercher le nom de l'activité
    rc2, comp_out, _ = adb(
        f"shell cmd package resolve-activity --brief -a android.intent.action.MAIN "
        f"-c android.intent.category.LAUNCHER {package}"
    )
    component = None
    for line in comp_out.splitlines():
        if "/" in line and package in line:
            component = line.strip()
            break
    if not component:
        # Fallback: format générique
        component = f"{package}/.MainActivity"
        log(f"Warning: using fallback component {component}")

    # Valider le composant (pas de caractères spéciaux)
    if not re.match(r'^[a-zA-Z0-9._/$]+$', component):
        print(f"❌ Invalid component URI: {component}")
        return

    nova_comp = f"{component}#-1"

    # Éditer le backup
    extract_dir, db_path = load_backup(CANONICAL_BACKUP)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Vérifier que le groupe existe
    c.execute("SELECT title FROM drawer_groups WHERE _id=?", (group_id,))
    row = c.fetchone()
    if not row:
        print(f"❌ Group {group_id} not found in backup")
        conn.close()
        return

    # Ajouter l'app
    c.execute("INSERT OR IGNORE INTO appgroups (groupId, component, modified) VALUES (?, ?, 0)",
              (group_id, nova_comp))
    conn.commit()
    count = c.rowcount
    conn.close()

    if count == 0:
        print(f"ℹ️ App {package} already in group {group_id} ({row[0]})")
    else:
        print(f"✅ Added {package} to group {group_id} ({row[0]})")

    # Sauvegarder et pousser
    save_backup(extract_dir, CANONICAL_BACKUP)
    cmd_push_restore()

def cmd_add_group(group_id: int, group_name: str):
    """Ajoute un nouveau groupe dans le backup canonique."""
    if not os.path.exists(CANONICAL_BACKUP):
        print(f"❌ Canonical backup not found: {CANONICAL_BACKUP}")
        return

    extract_dir, db_path = load_backup(CANONICAL_BACKUP)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO drawer_groups 
                 (_id, title, category_id, groupType, tabOrder, tabColor, flags, modified) 
                 VALUES (?, ?, '', 'folder', ?, 4280391914, 0, 0)""",
              (group_id, group_name, group_id))
    conn.commit()
    conn.close()
    save_backup(extract_dir, CANONICAL_BACKUP)
    print(f"✅ Group {group_id} '{group_name}' added to backup")
    cmd_push_restore()

def cmd_set_gesture(gesture: str, action: str):
    """Change un geste Nova dans le backup canonique."""
    if gesture not in GESTURE_MAP:
        print(f"❌ Unknown gesture: {gesture}. Options: {list(GESTURE_MAP.keys())}")
        return
    if action not in GESTURE_ACTIONS:
        print(f"❌ Unknown action: {action}. Options: {list(GESTURE_ACTIONS.keys())}")
        return
    if not os.path.exists(CANONICAL_BACKUP):
        print(f"❌ Canonical backup not found: {CANONICAL_BACKUP}")
        return

    extract_dir, db_path = load_backup(CANONICAL_BACKUP)
    edit_xml(extract_dir, GESTURE_MAP[gesture], GESTURE_ACTIONS[action], "string")
    save_backup(extract_dir, CANONICAL_BACKUP)
    print(f"✅ Gesture '{gesture}' set to '{action}'")
    cmd_push_restore()

def cmd_backup_pull(output_path: str = None):
    """Pull le backup actuel depuis la tablette."""
    if output_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(BACKUP_DIR, f"pulled_{ts}.novabackup")
    if not adb_ok():
        print("❌ ADB not connected")
        return
    # Déclencher un backup depuis Nova (via Intent)
    rc, _, _ = adb(f"shell am broadcast -a com.teslacoilsw.launcher.BACKUP "
                   f"--es path /sdcard/Download/nova_auto_backup.novabackup")
    time.sleep(3)
    # Pull
    rc, out, err = adb(f"pull /sdcard/Download/nova_auto_backup.novabackup {output_path}", timeout=30)
    if rc == 0:
        print(f"✅ Backup pulled to {output_path}")
    else:
        print(f"❌ Pull failed: {err}")

def cmd_fix_crash():
    """Répare Nova après un crash : clear data + push backup + trigger restore."""
    if not adb_ok():
        print("❌ ADB not connected")
        return
    log("Fixing Nova crash...")
    adb(f"shell am force-stop {NOVA_PKG}")
    time.sleep(1)
    adb(f"shell pm clear {NOVA_PKG}")
    time.sleep(2)
    adb(f"shell am start -n {NOVA_MAIN}")
    time.sleep(3)
    adb(f"shell cmd package set-home-activity {NOVA_MAIN}")
    cmd_push_restore()
    notify("🔧 <b>Nova Fix</b> — Data cleared + backup poussé. <b>Confirme le restore sur l'écran.</b>")

# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "status":
        cmd_status()
    elif cmd == "push_restore":
        cmd_push_restore(args[0] if args else None)
    elif cmd == "add_app":
        if len(args) < 2:
            print("Usage: nova_operator.py add_app <package> <group_id>")
            sys.exit(1)
        cmd_add_app(args[0], int(args[1]))
    elif cmd == "add_group":
        if len(args) < 2:
            print("Usage: nova_operator.py add_group <group_id> <group_name>")
            sys.exit(1)
        cmd_add_group(int(args[0]), " ".join(args[1:]))
    elif cmd == "set_gesture":
        if len(args) < 2:
            print("Usage: nova_operator.py set_gesture <gesture> <action>")
            sys.exit(1)
        cmd_set_gesture(args[0], args[1])
    elif cmd == "backup_pull":
        cmd_backup_pull(args[0] if args else None)
    elif cmd == "fix_crash":
        cmd_fix_crash()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
