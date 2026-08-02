#!/usr/bin/env python3
"""
Y-OS Telegram Handler — Interactive command interface for Y-OS
Bot: @yos_notif_bot | Authorized: Yannick (chat_id: 223132272)

Commands:
  /start   — Welcome message
  /status  — List active Y-OS processes
  /stop    — Stop a process by task_id
  /approve — Approve a pending task
  /crons   — Delta crons status
  /health  — CC health (RAM, disk)
  /help    — All commands

Deploy on CC:
  pip install python-telegram-bot
  pm2 start yos_telegram_handler.py --name yos-telegram --interpreter python3
"""

import logging
import os
import json
import glob
import subprocess
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX"
AUTHORIZED_CHAT_ID = 223132272
LOCK_DIR = "/tmp/yos_locks"
APPROVAL_DIR = "/tmp/yos_approvals"
LEDGER_DIR = "/home/ubuntu/yos/ledger"
LOG_DIR = "/home/ubuntu/yos/ledger/logs"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Dirs ──────────────────────────────────────────────────────────────────────
os.makedirs(LOCK_DIR, exist_ok=True)
os.makedirs(APPROVAL_DIR, exist_ok=True)


# ── Auth guard ────────────────────────────────────────────────────────────────
async def check_auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        logger.warning(f"Unauthorized access from chat_id: {update.effective_chat.id}")
        await update.message.reply_text("🚫 Unauthorized.")
        return False
    return True


# ── /start ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    await update.message.reply_html(
        "🧠 <b>Y-OS Notifications</b> — opérationnel\n\n"
        "Je surveille les processus Y-OS en temps réel.\n"
        "Tape /help pour voir les commandes disponibles."
    )


# ── /help ─────────────────────────────────────────────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    await update.message.reply_html(
        "<b>Y-OS Commands:</b>\n\n"
        "/status — Processus actifs\n"
        "/stop &lt;task_id&gt; — Arrêter un processus\n"
        "/approve &lt;task_id&gt; — Approuver une tâche\n"
        "/crons — État des crons delta\n"
        "/health — Santé du Cloud Computer\n"
        "/help — Cette aide"
    )


# ── /status ───────────────────────────────────────────────────────────────────
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    lock_files = glob.glob(os.path.join(LOCK_DIR, "*.json"))
    if not lock_files:
        await update.message.reply_text("⚫ Aucun processus Y-OS actif.")
        return

    lines = ["🔒 <b>Processus Y-OS actifs :</b>\n"]
    for lf in lock_files:
        try:
            with open(lf) as f:
                d = json.load(f)
            task_id = os.path.basename(lf).replace(".json", "")
            pid = d.get("pid", "?")
            # Check if PID is still alive
            alive = False
            try:
                os.kill(int(pid), 0)
                alive = True
            except Exception:
                pass
            status_icon = "🟢" if alive else "⚠️ zombie"
            lines.append(
                f"{status_icon} <code>{task_id}</code>\n"
                f"  PID: <code>{pid}</code>\n"
                f"  Tâche: {d.get('task_name', '?')}\n"
                f"  Démarré: {d.get('started_at', '?')}\n"
                f"  Nœud: {d.get('node', '?')}\n"
            )
        except Exception as e:
            lines.append(f"⚠️ Erreur lecture {os.path.basename(lf)}: {e}\n")

    await update.message.reply_html("\n".join(lines))


# ── /stop ─────────────────────────────────────────────────────────────────────
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
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
            try:
                os.kill(int(pid), 9)
                await update.message.reply_html(f"✅ PID <code>{pid}</code> tué.")
            except ProcessLookupError:
                await update.message.reply_html(f"⚠️ PID <code>{pid}</code> déjà terminé.")
            except Exception as e:
                await update.message.reply_html(f"❌ Erreur kill PID <code>{pid}</code>: {e}")
        os.remove(lock_file)
        await update.message.reply_html(f"🗑️ Lock <code>{task_id}</code> supprimé.")
    except Exception as e:
        await update.message.reply_html(f"❌ Erreur: {e}")


# ── /approve ──────────────────────────────────────────────────────────────────
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    if not context.args:
        await update.message.reply_html("Usage: /approve &lt;task_id&gt;")
        return

    task_id = context.args[0]
    approval_file = os.path.join(APPROVAL_DIR, f"{task_id}.approved")
    try:
        with open(approval_file, "w") as f:
            f.write(f"Approved at {datetime.now(timezone.utc).isoformat()}\n")
        await update.message.reply_html(f"✅ Tâche <code>{task_id}</code> approuvée.")
    except Exception as e:
        await update.message.reply_html(f"❌ Erreur: {e}")


# ── /crons ────────────────────────────────────────────────────────────────────
async def crons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    cron_map = {
        "delta_manus": "02:00 UTC",
        "delta_raindrop": "03:00 UTC",
        "delta_fireflies_plaud": "03:30 UTC",
        "delta_chatgpt": "04:00 UTC",
    }
    lines = ["📅 <b>Delta Crons :</b>\n"]
    for script, schedule in cron_map.items():
        log_file = os.path.join(LOG_DIR, f"{script}.log")
        last_run = "jamais"
        last_status = "?"
        if os.path.exists(log_file):
            try:
                result = subprocess.run(
                    ["tail", "-5", log_file],
                    capture_output=True, text=True, timeout=5
                )
                tail = result.stdout.strip()
                if tail:
                    last_line = tail.split("\n")[-1]
                    last_run = last_line[:19] if len(last_line) > 19 else last_line
                    last_status = "✅" if "ERROR" not in last_line.upper() else "❌"
            except Exception:
                pass
        lines.append(f"{last_status} <b>{script}</b> — {schedule}\n  Dernier run: <code>{last_run}</code>\n")

    await update.message.reply_html("\n".join(lines))


# ── /health ───────────────────────────────────────────────────────────────────
async def health(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_auth(update, context):
        return
    lines = ["💻 <b>Cloud Computer Health :</b>\n"]

    # RAM
    try:
        r = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=5)
        lines.append(f"<b>RAM :</b>\n<code>{r.stdout.strip()}</code>\n")
    except Exception as e:
        lines.append(f"<b>RAM :</b> erreur — {e}\n")

    # Disk
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        lines.append(f"<b>Disk :</b>\n<code>{r.stdout.strip()}</code>\n")
    except Exception as e:
        lines.append(f"<b>Disk :</b> erreur — {e}\n")

    # Crontab active
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        cron_count = len([l for l in r.stdout.splitlines() if l.strip() and not l.startswith("#")])
        lines.append(f"<b>Crons actifs :</b> {cron_count}")
    except Exception:
        lines.append("<b>Crons :</b> non disponible")

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

    logger.info("Y-OS Telegram Handler started — polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, timeout=60)


if __name__ == "__main__":
    main()
