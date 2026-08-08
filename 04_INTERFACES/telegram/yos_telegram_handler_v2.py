#!/usr/bin/env python3
"""
Y-OS Telegram Handler v2 — Interface interactive complète
Bot: @yos_notif_bot | Authorized: Yannick (chat_id: 223132272)

Commands:
  /start         — Welcome
  /help          — All commands
  /status        — Y-OS processes
  /health        — CC health (RAM, disk, crons)
  /android       — Android fleet status
  /nova          — Nova Launcher status + actions
  /nova fix      — Fix Nova crash (auto-recovery)
  /nova restore  — Push canonical backup + trigger restore
  /nova add <pkg> <group_id>  — Add app to group
  /reconnect     — Force ADB reconnect on all devices
  /crons         — Delta crons status
  /stop <id>     — Stop a process
  /approve <id>  — Approve a pending task

Deploy on CC:
  pm2 restart yos-telegram
"""
import logging
import os
import json
import glob
import subprocess
import sys
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
AUTHORIZED_CHAT_ID = 223132272
LOCK_DIR = "/tmp/yos_locks"
APPROVAL_DIR = "/tmp/yos_approvals"
LEDGER_DIR = "/home/ubuntu/yos/ledger"
LOG_DIR = "/home/ubuntu/yos/ledger/logs"
ANDROID_DIR = "/home/ubuntu/yos/android"
NOVA_OPERATOR = f"{ANDROID_DIR}/nova_operator.py"
ADB_RECONNECT = "/home/ubuntu/yos/adb_reconnect.sh"
FLEET = {
    "AND-001": {"host": "100.89.158.44:5555", "name": "Galaxy Tab S11"},
    "AND-002": {"host": None, "name": "Galaxy Z Fold 7 (à venir)"},
    "AND-003": {"host": None, "name": "Galaxy Watch Ultra 2 (à venir)"},
}

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
os.makedirs(LOCK_DIR, exist_ok=True)
os.makedirs(APPROVAL_DIR, exist_ok=True)

# ── Auth ──────────────────────────────────────────────────────────────────────
async def check_auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("🚫 Unauthorized.")
        return False
    return True

def run(cmd: str, timeout: int = 15) -> str:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return "⏱ Timeout"
    except Exception as e:
        return f"Error: {e}"

def adb(host: str, cmd: str) -> tuple[int, str]:
    r = subprocess.run(f"adb -s {host} {cmd}", shell=True, capture_output=True, text=True, timeout=10)
    return r.returncode, (r.stdout + r.stderr).strip()

# ── /start ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    await update.message.reply_html(
        "🧠 <b>Y-OS Operator</b> — v2.0\n\n"
        "Je surveille et contrôle ta flotte Android + le Cloud Computer.\n\n"
        "/help — Toutes les commandes\n"
        "/android — État de la flotte\n"
        "/nova — Gérer Nova Launcher"
    )

# ── /help ─────────────────────────────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    await update.message.reply_html(
        "<b>Y-OS Commands v2:</b>\n\n"
        "<b>Android:</b>\n"
        "/android — État flotte (batterie, ADB, Nova)\n"
        "/nova — Status Nova Launcher\n"
        "/nova fix — Réparer Nova crash\n"
        "/nova restore — Pousser backup + restore\n"
        "/nova add &lt;pkg&gt; &lt;group_id&gt; — Ajouter app\n"
        "/reconnect — Forcer reconnexion ADB\n\n"
        "<b>CC:</b>\n"
        "/health — RAM, disk, crons\n"
        "/crons — État des pipelines delta\n"
        "/status — Processus Y-OS actifs\n\n"
        "<b>Actions:</b>\n"
        "/stop &lt;task_id&gt; — Arrêter un processus\n"
        "/approve &lt;task_id&gt; — Approuver une tâche"
    )

# ── /android ──────────────────────────────────────────────────────────────────
async def android(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    lines = ["📱 <b>Android Fleet Status:</b>\n"]
    for dev_id, cfg in FLEET.items():
        host = cfg.get("host")
        name = cfg["name"]
        if not host:
            lines.append(f"⏳ <b>{dev_id}</b> — {name} (not configured)\n")
            continue
        rc, state = adb(host, "get-state")
        if rc != 0 or "device" not in state:
            lines.append(f"❌ <b>{dev_id}</b> — {name}\n  ADB: offline\n")
            continue
        # Battery
        _, bat = adb(host, "shell dumpsys battery | grep level")
        try:
            level = int(bat.split(":")[-1].strip())
            bat_icon = "🔴" if level < 10 else "🟡" if level < 20 else "🟢"
            bat_str = f"{bat_icon} {level}%"
        except Exception:
            bat_str = "?"
        # Nova
        _, top = adb(host, "shell dumpsys activity | grep topResumedActivity")
        nova_ok = "com.teslacoilsw.launcher" in top
        one_ui = "com.sec.android.app.launcher" in top
        nova_str = "✅ Nova" if nova_ok else ("⚠️ One UI" if one_ui else "❓")
        lines.append(
            f"✅ <b>{dev_id}</b> — {name}\n"
            f"  ADB: online | Battery: {bat_str} | Launcher: {nova_str}\n"
        )
    await update.message.reply_html("\n".join(lines))

# ── /nova ─────────────────────────────────────────────────────────────────────
async def nova(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    args = context.args or []
    subcmd = args[0] if args else "status"

    if subcmd == "status" or subcmd == "":
        out = run(f"python3 {NOVA_OPERATOR} status")
        await update.message.reply_html(f"<b>Nova Status:</b>\n<code>{out}</code>")

    elif subcmd == "fix":
        await update.message.reply_html("🔧 <b>Nova Fix</b> — Lancement de l'auto-recovery...")
        out = run(f"python3 {NOVA_OPERATOR} fix_crash", timeout=30)
        await update.message.reply_html(
            f"<code>{out}</code>\n\n"
            "⚠️ <b>Confirme le restore sur l'écran de la tablette.</b>"
        )

    elif subcmd == "restore":
        await update.message.reply_html("🔄 <b>Nova Restore</b> — Push du backup canonique...")
        out = run(f"python3 {NOVA_OPERATOR} push_restore", timeout=30)
        await update.message.reply_html(
            f"<code>{out}</code>\n\n"
            "⚠️ <b>Confirme le restore sur l'écran de la tablette.</b>"
        )

    elif subcmd == "add":
        if len(args) < 3:
            await update.message.reply_html("Usage: /nova add &lt;package&gt; &lt;group_id&gt;\nGroupes: 1=Common, 2=AI, 3=Office, 4=Photo, 5=Tools, 6=Sys")
            return
        pkg, gid = args[1], args[2]
        await update.message.reply_html(f"➕ Ajout de <code>{pkg}</code> au groupe {gid}...")
        out = run(f"python3 {NOVA_OPERATOR} add_app {pkg} {gid}", timeout=30)
        await update.message.reply_html(f"<code>{out}</code>")

    else:
        await update.message.reply_html(
            "Sous-commandes Nova:\n"
            "/nova — status\n"
            "/nova fix — réparer crash\n"
            "/nova restore — pousser backup\n"
            "/nova add &lt;pkg&gt; &lt;group_id&gt; — ajouter app"
        )

# ── /reconnect ────────────────────────────────────────────────────────────────
async def reconnect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    await update.message.reply_html("🔄 <b>ADB Reconnect</b> — Forçage...")
    out = run(f"bash {ADB_RECONNECT}", timeout=20)
    await update.message.reply_html(f"<code>{out[:500]}</code>")

# ── /health ───────────────────────────────────────────────────────────────────
async def health(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    lines = ["💻 <b>Cloud Computer Health:</b>\n"]
    lines.append(f"<b>RAM:</b>\n<code>{run('free -h')}</code>\n")
    lines.append(f"<b>Disk:</b>\n<code>{run('df -h / | tail -1')}</code>\n")
    lines.append(f"<b>PM2:</b>\n<code>{run('pm2 list --no-color | tail -10')}</code>\n")
    cron_count = len([l for l in run("crontab -l").splitlines() if l.strip() and not l.startswith("#")])
    lines.append(f"<b>Crons actifs:</b> {cron_count}")
    await update.message.reply_html("\n".join(lines))

# ── /status ───────────────────────────────────────────────────────────────────
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    lock_files = glob.glob(os.path.join(LOCK_DIR, "*.json"))
    if not lock_files:
        await update.message.reply_text("⚫ Aucun processus Y-OS actif.")
        return
    lines = ["🔒 <b>Processus Y-OS actifs:</b>\n"]
    for lf in lock_files:
        try:
            with open(lf) as f:
                d = json.load(f)
            task_id = os.path.basename(lf).replace(".json", "")
            pid = d.get("pid", "?")
            alive = False
            try:
                os.kill(int(pid), 0)
                alive = True
            except Exception:
                pass
            icon = "🟢" if alive else "⚠️ zombie"
            lines.append(f"{icon} <code>{task_id}</code> — PID {pid} — {d.get('task_name', '?')}\n")
        except Exception as e:
            lines.append(f"⚠️ {os.path.basename(lf)}: {e}\n")
    await update.message.reply_html("\n".join(lines))

# ── /stop ─────────────────────────────────────────────────────────────────────
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    if not context.args:
        await update.message.reply_html("Usage: /stop &lt;task_id&gt;")
        return
    task_id = context.args[0]
    lock_file = os.path.join(LOCK_DIR, f"{task_id}.json")
    if not os.path.exists(lock_file):
        await update.message.reply_html(f"❌ Task <code>{task_id}</code> introuvable.")
        return
    try:
        with open(lock_file) as f:
            d = json.load(f)
        pid = d.get("pid")
        if pid:
            os.kill(int(pid), 9)
        os.remove(lock_file)
        await update.message.reply_html(f"✅ <code>{task_id}</code> arrêté.")
    except Exception as e:
        await update.message.reply_html(f"❌ Erreur: {e}")

# ── /approve ──────────────────────────────────────────────────────────────────
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    if not context.args:
        await update.message.reply_html("Usage: /approve &lt;task_id&gt;")
        return
    task_id = context.args[0]
    approval_file = os.path.join(APPROVAL_DIR, f"{task_id}.approved")
    with open(approval_file, "w") as f:
        f.write(f"Approved at {datetime.now(timezone.utc).isoformat()}\n")
    await update.message.reply_html(f"✅ Tâche <code>{task_id}</code> approuvée.")

# ── /crons ────────────────────────────────────────────────────────────────────
async def crons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context): return
    cron_map = {
        "delta_manus": "02:00 UTC",
        "delta_raindrop": "03:00 UTC",
        "delta_fireflies_plaud": "03:30 UTC",
        "delta_chatgpt": "04:00 UTC",
        "adb_reconnect": "*/2 min",
        "crash_detector": "*/5 min",
        "health_probe": "*/15 min",
        "drift_packages": "06:00 UTC",
        "weekly_report": "Mon 07:00 UTC",
    }
    lines = ["📅 <b>Crons Y-OS:</b>\n"]
    for script, schedule in cron_map.items():
        log_file = os.path.join(LOG_DIR, f"{script}.log")
        if not os.path.exists(log_file):
            log_file = f"/home/ubuntu/yos/android/logs/{script}.log"
        last = "jamais"
        icon = "❓"
        if os.path.exists(log_file):
            try:
                r = subprocess.run(["tail", "-3", log_file], capture_output=True, text=True, timeout=3)
                tail = r.stdout.strip()
                if tail:
                    last = tail.split("\n")[-1][:40]
                    icon = "✅" if "ERROR" not in last.upper() and "FAIL" not in last.upper() else "❌"
            except Exception:
                pass
        lines.append(f"{icon} <b>{script}</b> [{schedule}]\n  <code>{last}</code>\n")
    await update.message.reply_html("\n".join(lines))

# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("crons", crons))
    app.add_handler(CommandHandler("health", health))
    app.add_handler(CommandHandler("android", android))
    app.add_handler(CommandHandler("nova", nova))
    app.add_handler(CommandHandler("reconnect", reconnect))
    logger.info("Y-OS Telegram Handler v2 started — polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, timeout=60)

if __name__ == "__main__":
    main()
