#!/usr/bin/env python3
"""
yos_monitor.py — Y-OS Universal Task Monitor v1.0
==================================================
Monitore n'importe quelle tâche longue et envoie des notifications iOS
progressives via ntfy.sh avec intervalles adaptatifs selon la durée estimée.

Usage:
  # Surveiller un fichier de sortie (render, export, download...)
  python3 yos_monitor.py --task "Render BirthTimeline" \
    --output /path/to/output.mp4 \
    --duration 300 \
    --log /tmp/render.log

  # Surveiller un PID
  python3 yos_monitor.py --task "Build Docker" \
    --pid 12345 \
    --duration 600

  # Surveiller un log avec pattern de progression
  python3 yos_monitor.py --task "Remotion Render" \
    --log /tmp/render.log \
    --progress-pattern "Rendered (\\d+)/(\\d+)" \
    --duration 420

Config ntfy (une seule fois):
  export YOS_NTFY_TOPIC="yos-alerts"
  export YOS_NTFY_SERVER="https://ntfy.sh"  # ou self-hosted
  export YOS_NTFY_TOKEN=""  # optionnel si topic privé
"""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from typing import Optional


# ─── CONFIG ────────────────────────────────────────────────────────────────────

NTFY_SERVER = os.environ.get("YOS_NTFY_SERVER", "https://ntfy.sh")
NTFY_TOPIC  = os.environ.get("YOS_NTFY_TOPIC", "yos-alerts")
NTFY_TOKEN  = os.environ.get("YOS_NTFY_TOKEN", "")

# Intervalle adaptatif selon durée estimée (secondes)
INTERVAL_TABLE = [
    (0,      120,   0),      # < 2 min  → fin uniquement
    (120,    600,   120),    # 2–10 min → toutes les 2 min
    (600,    1800,  300),    # 10–30 min → toutes les 5 min
    (1800,   7200,  900),    # 30 min–2h → toutes les 15 min
    (7200,   28800, 1800),   # 2h–8h → toutes les 30 min
    (28800,  float('inf'), 3600),  # > 8h → toutes les heures
]


# ─── NTFY ──────────────────────────────────────────────────────────────────────

def send_ntfy(
    title: str,
    message: str,
    priority: str = "default",
    tags: str = "",
    actions: str = "",
) -> bool:
    """Envoie une notification via ntfy.sh."""
    url = f"{NTFY_SERVER}/{NTFY_TOPIC}"
    headers = [
        f"Title: {title}",
        f"Priority: {priority}",
    ]
    if tags:
        headers.append(f"Tags: {tags}")
    if actions:
        headers.append(f"Actions: {actions}")
    if NTFY_TOKEN:
        headers.append(f"Authorization: Bearer {NTFY_TOKEN}")

    header_args = []
    for h in headers:
        header_args += ["-H", h]

    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "-X", "POST", url,
             "-d", message] + header_args,
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() in ("200", "201", "202")
    except Exception as e:
        print(f"[ntfy] Erreur: {e}", file=sys.stderr)
        return False


# ─── INTERVAL ──────────────────────────────────────────────────────────────────

def get_interval(estimated_duration: float) -> int:
    """Calcule l'intervalle de notification selon la durée estimée."""
    for low, high, interval in INTERVAL_TABLE:
        if low <= estimated_duration < high:
            return interval
    return 3600


def format_duration(seconds: float) -> str:
    """Formate une durée en string lisible."""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        m, s = divmod(int(seconds), 60)
        return f"{m}m{s:02d}s"
    else:
        h, rem = divmod(int(seconds), 3600)
        m = rem // 60
        return f"{h}h{m:02d}m"


# ─── PROGRESS EXTRACTORS ───────────────────────────────────────────────────────

def extract_progress_from_log(log_path: str, pattern: str) -> Optional[float]:
    """
    Extrait le pourcentage de progression depuis un fichier log.
    Pattern doit avoir 2 groupes: (current, total)
    Ex: "Rendered (\\d+)/(\\d+)"
    """
    try:
        result = subprocess.run(
            ["tail", "-20", log_path],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")
        for line in reversed(lines):
            m = re.search(pattern, line)
            if m:
                current = float(m.group(1))
                total = float(m.group(2))
                if total > 0:
                    return current / total
    except Exception:
        pass
    return None


def extract_eta_from_log(log_path: str) -> Optional[float]:
    """Extrait l'ETA depuis un log Remotion (time remaining: Xm Ys)."""
    try:
        result = subprocess.run(
            ["tail", "-5", log_path],
            capture_output=True, text=True, timeout=5
        )
        for line in reversed(result.stdout.split("\n")):
            m = re.search(r"time remaining:\s*(?:(\d+)m\s*)?(\d+)s", line)
            if m:
                minutes = int(m.group(1) or 0)
                seconds = int(m.group(2))
                return minutes * 60 + seconds
            m2 = re.search(r"time remaining:\s*(\d+)m\s*(\d+)s", line)
            if m2:
                return int(m2.group(1)) * 60 + int(m2.group(2))
    except Exception:
        pass
    return None


def is_pid_alive(pid: int) -> bool:
    """Vérifie si un PID est toujours actif."""
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def is_output_ready(output_path: str, min_size_bytes: int = 100_000) -> bool:
    """Vérifie si le fichier de sortie existe et a une taille minimale."""
    try:
        return os.path.getsize(output_path) >= min_size_bytes
    except (FileNotFoundError, OSError):
        return False


# ─── MAIN MONITOR ──────────────────────────────────────────────────────────────

def monitor(
    task_name: str,
    estimated_duration: float,
    output_path: Optional[str] = None,
    pid: Optional[int] = None,
    log_path: Optional[str] = None,
    progress_pattern: Optional[str] = None,
    min_output_size: int = 100_000,
) -> None:
    """
    Boucle principale de monitoring.
    Envoie des notifications progressives et une notification finale.
    """
    interval = get_interval(estimated_duration)
    start_time = time.time()
    last_notify = start_time
    notify_count = 0

    print(f"[yos_monitor] Démarrage: {task_name}")
    print(f"[yos_monitor] Durée estimée: {format_duration(estimated_duration)}")
    print(f"[yos_monitor] Intervalle notifications: {format_duration(interval) if interval else 'fin uniquement'}")
    print(f"[yos_monitor] ntfy: {NTFY_SERVER}/{NTFY_TOPIC}")

    # Notification de démarrage
    send_ntfy(
        title=f"⏳ {task_name}",
        message=f"Démarré — durée estimée: {format_duration(estimated_duration)}",
        priority="low",
        tags="hourglass_flowing_sand",
    )

    while True:
        time.sleep(10)
        elapsed = time.time() - start_time

        # ── Vérifier si terminé ──
        done = False
        if output_path and is_output_ready(output_path, min_output_size):
            done = True
        elif pid and not is_pid_alive(pid):
            done = True
        elif log_path and not output_path and not pid:
            # Pas de critère de fin explicite — on surveille juste le log
            pass

        if done:
            elapsed_str = format_duration(elapsed)
            size_str = ""
            if output_path:
                try:
                    size_mb = os.path.getsize(output_path) / 1024 / 1024
                    size_str = f" · {size_mb:.1f} MB"
                except Exception:
                    pass

            print(f"[yos_monitor] ✅ TERMINÉ en {elapsed_str}{size_str}")
            send_ntfy(
                title=f"✅ {task_name} — DONE",
                message=f"Terminé en {elapsed_str}{size_str}",
                priority="high",
                tags="white_check_mark,tada",
            )
            return

        # ── Notification de progression ──
        if interval > 0 and (time.time() - last_notify) >= interval:
            notify_count += 1
            progress_pct = None
            eta_str = ""

            # Extraire progression depuis log
            if log_path and progress_pattern:
                p = extract_progress_from_log(log_path, progress_pattern)
                if p is not None:
                    progress_pct = p * 100

            # Extraire ETA
            if log_path:
                eta_sec = extract_eta_from_log(log_path)
                if eta_sec is not None:
                    eta_str = f" · ETA: {format_duration(eta_sec)}"
                elif progress_pct is not None and progress_pct > 0:
                    remaining = elapsed / (progress_pct / 100) - elapsed
                    eta_str = f" · ETA: {format_duration(remaining)}"

            # Fallback estimation
            if progress_pct is None:
                if estimated_duration > 0:
                    progress_pct = min(99, (elapsed / estimated_duration) * 100)

            pct_str = f"{progress_pct:.0f}%" if progress_pct is not None else "?"
            elapsed_str = format_duration(elapsed)

            msg = f"{pct_str} · {elapsed_str} écoulé{eta_str}"
            print(f"[yos_monitor] 📊 {msg}")

            send_ntfy(
                title=f"📊 {task_name} — {pct_str}",
                message=msg,
                priority="low",
                tags="bar_chart",
            )
            last_notify = time.time()

        # ── Timeout de sécurité (3x la durée estimée) ──
        if estimated_duration > 0 and elapsed > estimated_duration * 3:
            print(f"[yos_monitor] ⚠️ Timeout — {format_duration(elapsed)} écoulé (3x durée estimée)")
            send_ntfy(
                title=f"⚠️ {task_name} — TIMEOUT",
                message=f"Durée dépassée: {format_duration(elapsed)} (estimé: {format_duration(estimated_duration)})",
                priority="urgent",
                tags="warning",
            )
            return


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Y-OS Universal Task Monitor — notifications iOS progressives via ntfy"
    )
    parser.add_argument("--task", required=True, help="Nom de la tâche (ex: 'Render BirthTimeline')")
    parser.add_argument("--duration", type=float, required=True,
                        help="Durée estimée en secondes (ex: 300 pour 5 min)")
    parser.add_argument("--output", help="Chemin du fichier de sortie attendu")
    parser.add_argument("--pid", type=int, help="PID du processus à surveiller")
    parser.add_argument("--log", help="Chemin du fichier log à surveiller")
    parser.add_argument("--progress-pattern",
                        help="Regex avec 2 groupes (current, total) ex: 'Rendered (\\d+)/(\\d+)'")
    parser.add_argument("--min-size", type=int, default=100_000,
                        help="Taille minimale du fichier de sortie en bytes (défaut: 100KB)")
    parser.add_argument("--ntfy-topic", help="Topic ntfy (override YOS_NTFY_TOPIC)")
    parser.add_argument("--ntfy-server", help="Serveur ntfy (override YOS_NTFY_SERVER)")

    args = parser.parse_args()

    # Override config si fourni
    if args.ntfy_topic:
        global NTFY_TOPIC
        NTFY_TOPIC = args.ntfy_topic
    if args.ntfy_server:
        global NTFY_SERVER
        NTFY_SERVER = args.ntfy_server

    monitor(
        task_name=args.task,
        estimated_duration=args.duration,
        output_path=args.output,
        pid=args.pid,
        log_path=args.log,
        progress_pattern=args.progress_pattern,
        min_output_size=args.min_size,
    )


if __name__ == "__main__":
    main()
