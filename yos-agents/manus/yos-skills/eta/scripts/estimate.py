#!/usr/bin/env python3
"""
ETA Skill — Estimation engine
Reads a task list (JSON or plain text) and outputs ETA per task + total.

Usage: python estimate.py [tasks_json_file]
If no file provided, reads from stdin.

Task JSON format:
[
  {"name": "Task A", "complexity": "low|medium|high|xl", "status": "pending|in_progress|done"},
  ...
]

Complexity → minutes mapping (calibrated for Manus agent tasks):
  low    = 2 min   (simple file edit, quick search)
  medium = 8 min   (multi-step code change, moderate research)
  high   = 20 min  (full component rewrite, complex build)
  xl     = 45 min  (large feature, multi-file refactor)
"""

import json
import sys
from datetime import datetime, timedelta

COMPLEXITY_MINUTES = {
    "low": 2,
    "medium": 8,
    "high": 20,
    "xl": 45,
}

DEFAULT_COMPLEXITY = "medium"

def estimate(tasks: list[dict]) -> dict:
    now = datetime.now()
    results = []
    cumulative = 0

    for task in tasks:
        if task.get("status") == "done":
            results.append({
                "name": task["name"],
                "status": "done",
                "minutes": 0,
                "eta": "—",
            })
            continue

        complexity = task.get("complexity", DEFAULT_COMPLEXITY)
        minutes = COMPLEXITY_MINUTES.get(complexity, COMPLEXITY_MINUTES[DEFAULT_COMPLEXITY])
        cumulative += minutes
        eta_time = now + timedelta(minutes=cumulative)

        results.append({
            "name": task["name"],
            "status": task.get("status", "pending"),
            "complexity": complexity,
            "minutes": minutes,
            "cumulative_minutes": cumulative,
            "eta": eta_time.strftime("%H:%M"),
        })

    return {
        "tasks": results,
        "total_minutes": cumulative,
        "final_eta": (now + timedelta(minutes=cumulative)).strftime("%H:%M"),
        "generated_at": now.strftime("%H:%M"),
    }

def format_output(result: dict) -> str:
    lines = []
    lines.append(f"⏱ ETA — généré à {result['generated_at']}")
    lines.append("")

    for t in result["tasks"]:
        if t["status"] == "done":
            lines.append(f"  ✅ {t['name']}")
        else:
            icon = "🔄" if t["status"] == "in_progress" else "⏳"
            lines.append(f"  {icon} {t['name']}  [{t.get('complexity','?')} · {t['minutes']}min]  → {t['eta']}")

    lines.append("")
    lines.append(f"📍 Total : {result['total_minutes']} min — Fin estimée : {result['final_eta']}")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            tasks = json.load(f)
    else:
        tasks = json.load(sys.stdin)

    result = estimate(tasks)
    print(format_output(result))
