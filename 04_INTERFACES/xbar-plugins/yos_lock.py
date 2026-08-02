#!/usr/bin/env python3
"""
yos_lock.py — Y-OS Mac Lock Manager + Telegram Notifier
Used by Manus to register/unregister active processes on the Mac.

Usage:
  from yos_lock import MacLock

  with MacLock("ChatGPT extraction", node="Mac+CDP"):
      # ... do work ...
      pass  # lock auto-released on exit, Telegram notified

  # Or manual:
  lock = MacLock("My task")
  lock.acquire()
  # ... work ...
  lock.release()
"""

import json
import os
import time
import uuid
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

LOCK_DIR = Path("/tmp/yos_locks")
LEGACY_LOCK = Path("/tmp/yos_mac_lock.json")

# Telegram config — Y-OS Notifications bot (@yos_notif_bot)
TELEGRAM_BOT_TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo"
TELEGRAM_CHAT_ID = "223132272"
TELEGRAM_ENABLED = True  # Set to False to disable notifications


def _send_telegram(text: str, silent: bool = False) -> bool:
    """Send a Telegram message. Returns True on success."""
    if not TELEGRAM_ENABLED:
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_notification": str(silent).lower(),
        }).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"[YOS LOCK] Telegram error: {e}")
        return False


class MacLock:
    def __init__(self, task: str, node: str = "Mac", notify: bool = True):
        self.task = task
        self.node = node
        self.notify = notify
        self.lock_id = str(uuid.uuid4())[:8]
        self.lock_path = LOCK_DIR / f"yos_{self.lock_id}.json"
        self.pid = os.getpid()

    def acquire(self):
        LOCK_DIR.mkdir(exist_ok=True)
        started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = {
            "pid": self.pid,
            "task": self.task,
            "node": self.node,
            "started_at": started_at,
            "lock_id": self.lock_id,
        }
        # Write individual lock
        self.lock_path.write_text(json.dumps(payload, indent=2))
        # Also write legacy single lock for backward compat
        LEGACY_LOCK.write_text(json.dumps(payload, indent=2))
        print(f"[YOS LOCK] Acquired: {self.task} (PID {self.pid})")

        # Telegram notification
        if self.notify:
            msg = (
                f"🔒 <b>Y-OS — Process démarré</b>\n\n"
                f"<b>Tâche :</b> {self.task}\n"
                f"<b>Nœud :</b> {self.node}\n"
                f"<b>PID :</b> {self.pid}\n"
                f"<b>Démarré :</b> {started_at}\n\n"
                f"⚠️ <i>Ne pas fermer le Mac tant que ce process est actif.</i>"
            )
            _send_telegram(msg)
        return self

    def release(self, success: bool = True, summary: str = ""):
        ended_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if self.lock_path.exists():
            self.lock_path.unlink()
        # Clean legacy lock only if it's ours
        if LEGACY_LOCK.exists():
            try:
                data = json.loads(LEGACY_LOCK.read_text())
                if data.get("lock_id") == self.lock_id:
                    LEGACY_LOCK.unlink()
            except Exception:
                pass
        print(f"[YOS LOCK] Released: {self.task}")

        # Telegram notification
        if self.notify:
            status_icon = "✅" if success else "❌"
            status_text = "Terminé avec succès" if success else "Terminé avec erreur"
            msg = (
                f"{status_icon} <b>Y-OS — Process terminé</b>\n\n"
                f"<b>Tâche :</b> {self.task}\n"
                f"<b>Nœud :</b> {self.node}\n"
                f"<b>Statut :</b> {status_text}\n"
                f"<b>Terminé :</b> {ended_at}\n"
            )
            if summary:
                msg += f"\n<b>Résumé :</b> {summary}"
            msg += "\n\n<i>Mac peut être fermé si aucun autre process actif.</i>"
            _send_telegram(msg, silent=True)  # silent on release (no sound)

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        summary = str(exc_val) if exc_val else ""
        self.release(success=success, summary=summary)


# CLI usage: python3 yos_lock.py acquire "Task name" [node]
#            python3 yos_lock.py release [lock_id]
#            python3 yos_lock.py status
#            python3 yos_lock.py notify "message"
if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "acquire":
        task = sys.argv[2] if len(sys.argv) > 2 else "Unknown task"
        node = sys.argv[3] if len(sys.argv) > 3 else "Mac"
        lock = MacLock(task, node)
        lock.acquire()
        print(f"Lock ID: {lock.lock_id}")

    elif cmd == "release":
        lock_id = sys.argv[2] if len(sys.argv) > 2 else None
        if lock_id:
            p = LOCK_DIR / f"yos_{lock_id}.json"
            if p.exists():
                p.unlink()
                print(f"Released lock {lock_id}")
            else:
                print(f"Lock {lock_id} not found")
        else:
            # Release all
            for f in LOCK_DIR.glob("*.json"):
                f.unlink()
            if LEGACY_LOCK.exists():
                LEGACY_LOCK.unlink()
            print("All locks released")

    elif cmd == "notify":
        # Send a standalone Telegram notification
        message = sys.argv[2] if len(sys.argv) > 2 else "Y-OS notification"
        ok = _send_telegram(f"📢 <b>Y-OS</b>\n\n{message}")
        print(f"Telegram: {'sent' if ok else 'failed'}")

    elif cmd == "status":
        locks = list(LOCK_DIR.glob("*.json")) if LOCK_DIR.exists() else []
        if LEGACY_LOCK.exists() and LEGACY_LOCK not in locks:
            locks.append(LEGACY_LOCK)
        if not locks:
            print("No active Y-OS locks.")
        else:
            for f in locks:
                try:
                    d = json.loads(f.read_text())
                    pid = d.get("pid", "?")
                    alive = "ALIVE" if (os.path.exists(f"/proc/{pid}") or os.system(f"kill -0 {pid} 2>/dev/null") == 0) else "DEAD"
                    print(f"[{alive}] {d.get('task')} | PID {pid} | {d.get('started_at')} | {d.get('node')}")
                except Exception as e:
                    print(f"Error reading {f}: {e}")
