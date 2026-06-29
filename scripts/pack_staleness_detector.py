#!/usr/bin/env python3
"""
pack_staleness_detector.py — yOS Continuity Core Phase 1
Determine whether a Context Pack is too old for its task_class / policy.

Policies:
  strict:   max 4h  → hard_stop
  standard: max 24-72h → warning/blocking
  relaxed:  max 7d  → advisory
  none:     no check

Usage:
  python3 pack_staleness_detector.py --pack PATH [--policy strict]
  python3 pack_staleness_detector.py --timestamp ISO8601 --policy standard
"""

import re
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

POLICY_MAX_HOURS = {
    "strict": 4,
    "standard": 48,
    "relaxed": 168,  # 7 days
    "none": None
}

POLICY_ACTION = {
    "strict": "hard_stop",
    "standard": "blocking",
    "relaxed": "advisory",
    "none": "none"
}

TASK_CLASS_POLICY = {
    "book_prose": "standard",
    "architecture": "strict",
    "code_generation": "standard",
    "research": "relaxed",
    "data_analysis": "standard",
    "vision_image": "relaxed",
    "translation": "relaxed",
    "conversation": "none",
    "default": "standard"
}


def detect_staleness(freshness_timestamp: str, staleness_policy: str = "standard") -> dict:
    """
    Check if a pack is stale given its freshness_timestamp and policy.
    Returns result dict with severity and recommendation.
    """
    if staleness_policy == "none":
        return {
            "stale": False,
            "severity": "none",
            "action": "none",
            "age_hours": None,
            "max_age_hours": None,
            "recommendation": "No staleness check — policy=none"
        }

    try:
        ts = datetime.fromisoformat(freshness_timestamp.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return {
            "stale": True,
            "severity": "blocking",
            "action": "blocking",
            "age_hours": None,
            "max_age_hours": POLICY_MAX_HOURS.get(staleness_policy),
            "recommendation": f"Cannot parse freshness_timestamp: '{freshness_timestamp}' — treat as stale"
        }

    now = datetime.now(timezone.utc)
    age = now - ts
    age_hours = age.total_seconds() / 3600
    max_hours = POLICY_MAX_HOURS.get(staleness_policy, 48)

    if max_hours is None:
        return {
            "stale": False,
            "severity": "none",
            "action": "none",
            "age_hours": round(age_hours, 2),
            "max_age_hours": None,
            "recommendation": "No staleness check — policy=none"
        }

    stale = age_hours > max_hours
    action = POLICY_ACTION.get(staleness_policy, "warning") if stale else "none"

    return {
        "stale": stale,
        "severity": action if stale else "ok",
        "action": action,
        "age_hours": round(age_hours, 2),
        "max_age_hours": max_hours,
        "recommendation": (
            f"Pack is {round(age_hours, 1)}h old — exceeds {max_hours}h limit for policy '{staleness_policy}'. "
            "Refresh required." if stale else
            f"Pack is {round(age_hours, 1)}h old — within {max_hours}h limit for policy '{staleness_policy}'. OK."
        )
    }


def detect_staleness_from_pack(pack_path: Path) -> dict:
    """Read freshness_timestamp and staleness_policy from a pack file and check."""
    content = pack_path.read_text(encoding="utf-8")

    ts_match = re.search(r"freshness_timestamp:\s*['\"]?([^'\"\n]+)['\"]?", content)
    policy_match = re.search(r"staleness_policy:\s*['\"]?([a-z_]+)['\"]?", content)

    freshness_timestamp = ts_match.group(1).strip() if ts_match else None
    staleness_policy = policy_match.group(1).strip() if policy_match else "standard"

    if not freshness_timestamp:
        return {
            "stale": True,
            "severity": "blocking",
            "action": "blocking",
            "age_hours": None,
            "max_age_hours": None,
            "recommendation": "freshness_timestamp missing from pack — treat as stale"
        }

    return detect_staleness(freshness_timestamp, staleness_policy)


def get_policy_for_task_class(task_class: str) -> str:
    return TASK_CLASS_POLICY.get(task_class, "standard")


def main():
    parser = argparse.ArgumentParser(description="yOS Pack Staleness Detector")
    parser.add_argument("--pack", type=Path, help="Path to context pack file")
    parser.add_argument("--timestamp", help="ISO8601 freshness timestamp")
    parser.add_argument("--policy", default="standard", choices=list(POLICY_MAX_HOURS.keys()))
    parser.add_argument("--task-class", default="default", help="Task class for policy lookup")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.pack:
        result = detect_staleness_from_pack(args.pack)
    elif args.timestamp:
        policy = args.policy or get_policy_for_task_class(args.task_class)
        result = detect_staleness(args.timestamp, policy)
    else:
        print("[ERROR] Provide --pack or --timestamp", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Stale:          {result['stale']}")
        print(f"Severity:       {result['severity']}")
        print(f"Action:         {result['action']}")
        print(f"Age (hours):    {result['age_hours']}")
        print(f"Max Age (hours):{result['max_age_hours']}")
        print(f"Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    main()
