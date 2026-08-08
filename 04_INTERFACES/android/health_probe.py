# TOKENS: Loaded from env vars NOTION_TOKEN and TELEGRAM_TOKEN (stored in /home/ubuntu/yos/.env on CC)
#!/usr/bin/env python3
"""
Y-OS Android Health Probe — P1
Collecte les métriques de santé de la flotte Android via ADB.
Cron : */15 * * * * (toutes les 15 minutes)
"""

import subprocess
import json
import datetime
import os
import sys

# Configuration flotte
# adb_host = None → device non encore configuré, skip silencieux
FLEET = {
    "AND-001": {
        "name": "Galaxy Tab S11",
        "adb_host": "100.89.158.44:5555",
        "role": "creative_tablet"
    },
    "AND-002": {
        "name": "Galaxy Z Fold 7",
        "adb_host": None,  # 🔜 À remplir à réception (IP Tailscale)
        "role": "primary_phone"
    },
    "AND-003": {
        "name": "Galaxy Watch Ultra 2",
        "adb_host": None,  # 🔜 Pas d'ADB direct — monitoring via AND-002 proxy + HA
        "role": "watch",
        "proxy": "AND-002"
    }
}

TELEGRAM_TOKEN = "${TELEGRAM_TOKEN}"
CHAT_ID = "223132272"
LOG_DIR = "/home/ubuntu/yos/android/logs"
STATE_FILE = "/home/ubuntu/yos/android/state.json"

# Notion Fleet DB
NOTION_TOKEN = "${NOTION_TOKEN}"
FLEET_DB_ID = "070971da-4ae4-4ace-96fc-5a9b2f5a930f"
# Map device_id → Notion page URL (peuplé au premier run)
NOTION_FLEET_PAGES = {
    "AND-001": "3b635e218cf8813eb0d1cfae041e12a2",
    "AND-002": "3b635e218cf881fa8c34e9809625854f",
    "AND-003": "3b635e218cf881ec8c8dc0b34ee8c697",
    "CC-001":  "3b635e218cf881b6a402e4e4fccd159f",
    "N100-001":"3b635e218cf881fa9e37f0a802acde83",
}

# Seuils d'alerte
THRESHOLDS = {
    "battery_p1": 10,   # % → alerte critique
    "battery_p2": 20,   # % → alerte attention
    "storage_p1": 92,   # % utilisé → critique
    "storage_p2": 85,   # % utilisé → attention
}

def adb(device_host, cmd):
    """Exécute une commande ADB et retourne stdout."""
    result = subprocess.run(
        ["adb", "-s", device_host, "shell"] + cmd.split(),
        capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip()

def get_battery(host):
    raw = subprocess.run(
        ["adb", "-s", host, "shell", "dumpsys", "battery"],
        capture_output=True, text=True, timeout=10
    ).stdout
    data = {}
    # Ne lire que le bloc "Current Battery Service state" (lignes indentées avec 2 espaces)
    in_current = False
    for line in raw.splitlines():
        if "Current Battery Service state" in line:
            in_current = True
            continue
        if in_current and line and not line.startswith(' ') and not line.startswith('\t'):
            break  # fin du bloc (ligne sans indentation = nouveau bloc)
        if in_current:
            try:
                if line.strip().startswith("level:") : data["level"] = int(line.split("level:")[1].strip())
                elif "status:" in line: data["status"] = int(line.split("status:")[1].strip())
                elif "temperature:" in line: data["temp_c"] = int(line.split("temperature:")[1].strip()) / 10
                elif "AC powered:" in line: data["ac"] = "true" in line
                elif "USB powered:" in line: data["usb"] = "true" in line
                elif "Wireless powered:" in line: data["wireless"] = "true" in line
            except: pass
    data["charging"] = data.get("ac") or data.get("usb") or data.get("wireless")
    return data

def get_storage(host):
    raw = adb(host, "df /data")
    # Format: Filesystem 1K-blocks Used Available Use% Mounted
    # Ex: /dev/block/dm-92 233775104 43900404 189743628  19% /data/user/0
    for line in raw.splitlines():
        if line.startswith('/dev') or '/data' in line:
            parts = line.split()
            if len(parts) >= 5:
                try:
                    total_kb = int(parts[1])
                    used_kb = int(parts[2])
                    free_kb = int(parts[3])
                    used_pct = int(parts[4].replace('%', ''))
                    return {
                        "used_pct": used_pct,
                        "total_gb": round(total_kb / 1024 / 1024, 1),
                        "used_gb": round(used_kb / 1024 / 1024, 1),
                        "free_gb": round(free_kb / 1024 / 1024, 1)
                    }
                except: pass
    return {}

def get_ram(host):
    raw = adb(host, "cat /proc/meminfo")
    data = {}
    for line in raw.splitlines():
        if "MemTotal:" in line: data["total_mb"] = int(line.split()[1]) // 1024
        if "MemAvailable:" in line: data["available_mb"] = int(line.split()[1]) // 1024
    if "total_mb" in data and "available_mb" in data:
        data["used_mb"] = data["total_mb"] - data["available_mb"]
        data["used_pct"] = round(data["used_mb"] / data["total_mb"] * 100)
    return data

def check_adb_connected(host):
    result = subprocess.run(
        ["adb", "-s", host, "shell", "echo", "OK"],
        capture_output=True, text=True, timeout=5
    )
    return result.returncode == 0 and "OK" in result.stdout

def send_telegram(message, level="P2"):
    import urllib.request, urllib.parse
    emoji = {"P1": "🔴", "P2": "🟠", "P3": "🟡", "OK": "✅"}.get(level, "ℹ️")
    text = f"{emoji} <b>yOS Android — {level}</b>\n\n{message}"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    try:
        urllib.request.urlopen(
            urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=data),
            timeout=10
        )
    except Exception as e:
        print(f"Telegram error: {e}")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def probe_device(device_id, config):
    host = config["adb_host"]
    name = config["name"]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Skip silencieux si device non encore configuré
    if host is None:
        print(f"  ⏸️  {device_id} ({name}) — non configuré, skip")
        return None
    
    result = {
        "device_id": device_id,
        "name": name,
        "timestamp": now,
        "adb_connected": False,
        "alerts": []
    }
    
    # Check ADB
    if not check_adb_connected(host):
        result["adb_connected"] = False
        result["alerts"].append({"level": "P1", "msg": f"{device_id} / ADB non joignable"})
        return result
    
    result["adb_connected"] = True
    
    # Batterie
    bat = get_battery(host)
    result["battery"] = bat
    level = bat.get("level", 100)
    charging = bat.get("charging", False)
    if not charging:
        if level <= THRESHOLDS["battery_p1"]:
            result["alerts"].append({"level": "P1", "msg": f"{device_id} / batterie critique {level}% non chargée"})
        elif level <= THRESHOLDS["battery_p2"]:
            result["alerts"].append({"level": "P2", "msg": f"{device_id} / batterie faible {level}% non chargée"})
    
    # Stockage
    sto = get_storage(host)
    result["storage"] = sto
    used_pct = sto.get("used_pct", 0)
    if used_pct >= THRESHOLDS["storage_p1"]:
        result["alerts"].append({"level": "P1", "msg": f"{device_id} / stockage critique {used_pct}% utilisé ({sto.get('free_gb', '?')} GB libres)"})
    elif used_pct >= THRESHOLDS["storage_p2"]:
        result["alerts"].append({"level": "P2", "msg": f"{device_id} / stockage {used_pct}% utilisé ({sto.get('free_gb', '?')} GB libres)"})
    
    # RAM
    result["ram"] = get_ram(host)
    
    return result

def update_notion_fleet(device_id, battery_pct, storage_pct, status):
    """Met à jour la fiche Fleet dans Notion pour un device."""
    page_id = NOTION_FLEET_PAGES.get(device_id)
    if not page_id:
        return
    import urllib.request, urllib.parse
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = json.dumps({
        "properties": {
            "Battery": {"number": battery_pct},
            "Storage Used": {"number": storage_pct},
            "Status": {"select": {"name": status}},
            "Last Sync": {"date": {"start": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")}}
        }
    }).encode()
    req = urllib.request.Request(
        url, data=payload, method="PATCH",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        print(f"  📊 Notion Fleet updated: {device_id} → {status} bat={battery_pct}% sto={storage_pct}%")
    except Exception as e:
        print(f"  ⚠️ Notion update error for {device_id}: {e}")

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    state = load_state()
    
    all_results = []
    for device_id, config in FLEET.items():
        print(f"Probing {device_id} ({config['name']})...")
        try:
            result = probe_device(device_id, config)
            if result is None:
                continue  # device non configuré, skip
            all_results.append(result)
            
            # Envoyer alertes (avec déduplication basique)
            for alert in result["alerts"]:
                alert_key = f"{device_id}_{alert['level']}_{alert['msg'][:30]}"
                last_sent = state.get(f"alert_{alert_key}", 0)
                cooldown = 3600 if alert["level"] == "P2" else 600  # 1h P2, 10min P1
                
                import time
                if time.time() - last_sent > cooldown:
                    send_telegram(alert["msg"], alert["level"])
                    state[f"alert_{alert_key}"] = time.time()
                    print(f"  → Telegram {alert['level']}: {alert['msg']}")
            
            # Log résultat
            bat = result.get("battery", {})
            sto = result.get("storage", {})
            status = "✅ OK" if result["adb_connected"] and not result["alerts"] else "⚠️ ALERT"
            print(f"  {status} | Bat: {bat.get('level','?')}% {'⚡' if bat.get('charging') else ''} | "
                  f"Storage: {sto.get('used_pct','?')}% | ADB: {'✅' if result['adb_connected'] else '❌'}")
            
            # Mettre à jour Notion Fleet
            notion_status = "Online" if result["adb_connected"] and not result["alerts"] else ("Warning" if result["alerts"] else "Offline")
            update_notion_fleet(
                device_id,
                bat.get("level", 0),
                sto.get("used_pct", 0),
                notion_status
            )
                  
        except Exception as e:
            print(f"  ❌ Erreur probe {device_id}: {e}")
    
    # Sauvegarder état + log JSON
    save_state(state)
    log_file = os.path.join(LOG_DIR, f"probe_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M')}.json")
    with open(log_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Garder seulement les 48 derniers logs (24h à 30min)
    logs = sorted([f for f in os.listdir(LOG_DIR) if f.startswith("probe_")])
    for old in logs[:-48]:
        os.remove(os.path.join(LOG_DIR, old))

if __name__ == "__main__":
    main()
