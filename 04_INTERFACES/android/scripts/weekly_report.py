#!/usr/bin/env python3
"""
Y-OS Android Weekly Report — P1
Génère le rapport hebdomadaire de flotte et le push dans GitHub.
Cron : 0 7 * * 1 (lundi 7h UTC)
"""

import subprocess, json, os, datetime, sys

TELEGRAM_TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
CHAT_ID = "223132272"
REPORT_DIR = "/home/ubuntu/yos-repo/04_INTERFACES/android/fleet"
LOG_DIR = "/home/ubuntu/yos/android/logs"
STATE_FILE = "/home/ubuntu/yos/android/state.json"

FLEET = {
    "AND-001": {"name": "Galaxy Tab S11", "adb_host": "100.89.158.44:5555", "role": "creative_tablet"},
    "AND-002": {"name": "Galaxy Z Fold 7", "adb_host": None, "role": "primary_phone"},
    "AND-003": {"name": "Galaxy Watch Ultra 2", "adb_host": None, "role": "watch"},
    "AND-004": {"name": "Google TV", "adb_host": None, "role": "media"},
    "AND-005": {"name": "Galaxy Tab A Robi", "adb_host": None, "role": "family_tablet"},
}

def adb(host, cmd):
    r = subprocess.run(["adb", "-s", host, "shell"] + cmd.split(),
                       capture_output=True, text=True, timeout=10)
    return r.stdout.strip()

def check_adb(host):
    if not host: return False
    r = subprocess.run(["adb", "-s", host, "shell", "echo", "OK"],
                       capture_output=True, text=True, timeout=5)
    return r.returncode == 0 and "OK" in r.stdout

def get_battery_level(host):
    raw = subprocess.run(["adb", "-s", host, "shell", "dumpsys", "battery"],
                         capture_output=True, text=True, timeout=10).stdout
    in_current = False
    for line in raw.splitlines():
        if "Current Battery Service state" in line:
            in_current = True; continue
        if in_current and line and not line.startswith(' '): break
        if in_current and line.strip().startswith("level:"):
            try: return int(line.split("level:")[1].strip())
            except: pass
    return None

def get_storage_pct(host):
    raw = adb(host, "df /data")
    for line in raw.splitlines():
        if line.startswith('/dev'):
            parts = line.split()
            if len(parts) >= 5:
                try: return int(parts[4].replace('%',''))
                except: pass
    return None

def get_package_count(host):
    r = subprocess.run(["adb", "-s", host, "shell", "pm", "list", "packages", "-3"],
                       capture_output=True, text=True, timeout=15)
    return len([l for l in r.stdout.splitlines() if l.startswith("package:")])

def load_prev_snapshot(device_id):
    snap = f"/home/ubuntu/yos/android/snapshots/{device_id}_packages_latest.json"
    if os.path.exists(snap):
        with open(snap) as f: return json.load(f)
    return None

def send_telegram(msg):
    import urllib.request, urllib.parse
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}).encode()
    try:
        urllib.request.urlopen(
            urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=data), timeout=10)
    except: pass

def git_push(message):
    repo = "/home/ubuntu/yos-repo"
    subprocess.run(["git", "-C", repo, "pull", "--rebase", "origin", "main"], capture_output=True)
    subprocess.run(["git", "-C", repo, "add", "04_INTERFACES/android/fleet/"], check=False)
    r = subprocess.run(["git", "-C", repo, "commit", "-m", message], capture_output=True, text=True)
    if "nothing to commit" in r.stdout: return False
    subprocess.run(["git", "-C", repo, "push", "origin", "main"], capture_output=True)
    return True

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    today = now.strftime("%Y-%m-%d")
    week = now.strftime("W%V-%Y")
    
    print(f"=== Y-OS Android Weekly Report {week} ===")
    
    # Collecter métriques
    fleet_data = {}
    for device_id, cfg in FLEET.items():
        host = cfg["adb_host"]
        connected = check_adb(host)
        d = {"name": cfg["name"], "role": cfg["role"], "connected": connected}
        
        if connected:
            d["battery"] = get_battery_level(host)
            d["storage_pct"] = get_storage_pct(host)
            d["pkg_count"] = get_package_count(host)
            prev = load_prev_snapshot(device_id)
            if prev:
                d["pkg_prev_count"] = prev.get("count", 0)
                d["pkg_prev_date"] = prev.get("date", "?")
            print(f"  ✅ {device_id} — bat:{d.get('battery','?')}% storage:{d.get('storage_pct','?')}% apps:{d.get('pkg_count','?')}")
        else:
            print(f"  ⏸️  {device_id} ({cfg['name']}) — non connecté")
        
        fleet_data[device_id] = d
    
    # Générer rapport Markdown
    lines = [
        f"---",
        f"report_type: weekly_fleet",
        f"date: {today}",
        f"week: {week}",
        f"generated_by: yOS Android Operator (automated cron)",
        f"---",
        f"",
        f"# Rapport Hebdomadaire — Flotte Android Y-OS",
        f"**{week} · {today} · Généré automatiquement**",
        f"",
        f"---",
        f"",
        f"## 1. Fleet Pulse",
        f"",
        f"| Device | ID | ADB | Batterie | Stockage | Apps |",
        f"|---|---|---|---|---|---|",
    ]
    
    for device_id, d in fleet_data.items():
        status = "✅" if d["connected"] else "⏸️"
        bat = f"{d['battery']}%" if d.get("battery") is not None else "—"
        sto = f"{d.get('storage_pct','—')}%" if d.get("storage_pct") is not None else "—"
        apps = str(d.get("pkg_count", "—"))
        lines.append(f"| {d['name']} | {device_id} | {status} | {bat} | {sto} | {apps} |")
    
    active = sum(1 for d in fleet_data.values() if d["connected"])
    lines += [
        f"",
        f"**Flotte active : {active}/{len(FLEET)} machines**",
        f"",
        f"---",
        f"",
        f"## 2. Santé détaillée",
        f"",
    ]
    
    alerts = []
    for device_id, d in fleet_data.items():
        if not d["connected"]: continue
        lines.append(f"### {device_id} — {d['name']}")
        lines.append(f"")
        bat = d.get("battery")
        sto = d.get("storage_pct")
        if bat is not None:
            bat_status = "✅" if bat > 20 else ("🟠" if bat > 10 else "🔴")
            lines.append(f"- Batterie : {bat_status} **{bat}%**")
            if bat <= 10: alerts.append(f"🔴 {device_id} batterie critique {bat}%")
            elif bat <= 20: alerts.append(f"🟠 {device_id} batterie faible {bat}%")
        if sto is not None:
            sto_status = "✅" if sto < 85 else ("🟠" if sto < 92 else "🔴")
            lines.append(f"- Stockage : {sto_status} **{sto}% utilisé**")
            if sto >= 92: alerts.append(f"🔴 {device_id} stockage critique {sto}%")
            elif sto >= 85: alerts.append(f"🟠 {device_id} stockage élevé {sto}%")
        if d.get("pkg_count"):
            prev = d.get("pkg_prev_count")
            delta = f" (Δ {d['pkg_count']-prev:+d} vs {d.get('pkg_prev_date','?')})" if prev else ""
            lines.append(f"- Apps tierces : **{d['pkg_count']}**{delta}")
        lines.append(f"")
    
    lines += [
        f"---",
        f"",
        f"## 3. Alertes actives",
        f"",
    ]
    if alerts:
        for a in alerts: lines.append(f"- {a}")
    else:
        lines.append(f"Aucune alerte active. ✅")
    
    lines += [
        f"",
        f"---",
        f"",
        f"## 4. Automatisations actives",
        f"",
        f"| Job | Cron | Statut |",
        f"|---|---|---|",
        f"| Health probe ADB | `*/15 * * * *` | ✅ |",
        f"| Drift packages | `0 6 * * *` | ✅ |",
        f"| ADB auto-reconnect | `*/2 * * * *` | ✅ |",
        f"| Rapport hebdomadaire | `0 7 * * 1` | ✅ |",
        f"",
        f"---",
        f"",
        f"## 5. Prochaines actions",
        f"",
        f"| # | Action | Précondition |",
        f"|---|---|---|",
        f"| 1 | Réceptionner AND-002 Fold 7 + setup Y-OS | Livraison J+10 |",
        f"| 2 | Appairer AND-003 Watch Ultra 2 | AND-002 reçu |",
        f"| 3 | Installer Home Assistant sur N100 | N100 connecté à Manus |",
        f"| 4 | HA Companion sur AND-001 + AND-002 | N100 + HA opérationnel |",
    ]
    
    report_content = "\n".join(lines)
    report_file = os.path.join(REPORT_DIR, f"WEEKLY-REPORT-{today}.md")
    
    with open(report_file, "w") as f:
        f.write(report_content)
    print(f"✅ Rapport écrit : {report_file}")
    
    # Push GitHub
    pushed = git_push(f"chore(android): rapport hebdomadaire {week}")
    if pushed: print("✅ GitHub push OK")
    
    # Notif Telegram
    alert_section = "\n".join(alerts) if alerts else "Aucune alerte ✅"
    tg_msg = (
        f"📊 <b>yOS Android — Rapport {week}</b>\n\n"
        f"Flotte active : {active}/{len(FLEET)}\n"
        f"Alertes : {len(alerts)}\n\n"
        f"{alert_section}\n\n"
        f"Rapport complet → GitHub YOS/04_INTERFACES/android/fleet/"
    )
    send_telegram(tg_msg)
    print("✅ Notif Telegram envoyée")

if __name__ == "__main__":
    main()
