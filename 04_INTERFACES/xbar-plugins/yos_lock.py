#!/usr/bin/env python3
"""
yos_lock.py — Y-OS Mac Lock Manager
Used by Manus to register/unregister active processes on the Mac.

Usage:
  from yos_lock import MacLock

  with MacLock("ChatGPT extraction", node="Mac+CDP"):
      # ... do work ...
      pass  # lock auto-released on exit

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
from datetime import datetime, timezone
from pathlib import Path

LOCK_DIR = Path("/tmp/yos_locks")
LEGACY_LOCK = Path("/tmp/yos_mac_lock.json")


class MacLock:
    def __init__(self, task: str, node: str = "Mac"):
        self.task = task
        self.node = node
        self.lock_id = str(uuid.uuid4())[:8]
        self.lock_path = LOCK_DIR / f"yos_{self.lock_id}.json"
        self.pid = os.getpid()

    def acquire(self):
        LOCK_DIR.mkdir(exist_ok=True)
        payload = {
            "pid": self.pid,
            "task": self.task,
            "node": self.node,
            "started_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "lock_id": self.lock_id,
        }
        # Write individual lock
        self.lock_path.write_text(json.dumps(payload, indent=2))
        # Also write legacy single lock for backward compat
        LEGACY_LOCK.write_text(json.dumps(payload, indent=2))
        print(f"[YOS LOCK] Acquired: {self.task} (PID {self.pid})")
        return self

    def release(self):
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

    def __enter__(self):
        return self.acquire()

    def __exit__(self, *args):
        self.release()


# CLI usage: python3 yos_lock.py acquire "Task name" [node]
#            python3 yos_lock.py release [lock_id]
#            python3 yos_lock.py status
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
