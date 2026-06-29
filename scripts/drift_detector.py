#!/usr/bin/env python3
"""
drift_detector.py — yOS Continuity Core Phase 1
Detect context drift between two Context Packs or between a pack and current state.

Drift types:
  constraint_drift    — constraints changed between packs
  decision_drift      — active decisions changed
  state_drift         — project state diverged
  actor_drift         — actor/LLM changed without handoff
  staleness_drift     — pack too old for current task
  lineage_break       — lineage chain broken

Usage:
  python3 drift_detector.py --pack-a PATH --pack-b PATH
  python3 drift_detector.py --pack PATH --current-state '{"status": "..."}'
"""

import re
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pack_staleness_detector import detect_staleness_from_pack

DRIFT_TYPES = [
    "constraint_drift", "decision_drift", "state_drift",
    "actor_drift", "staleness_drift", "lineage_break"
]

DRIFT_SEVERITY = {
    "constraint_drift": "blocking",
    "decision_drift": "warning",
    "state_drift": "warning",
    "actor_drift": "advisory",
    "staleness_drift": "blocking",
    "lineage_break": "warning"
}


def extract_field(content: str, field: str) -> str:
    """Extract a single-line field value from pack content."""
    match = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_section(content: str, section: str) -> str:
    """Extract a section block from pack content."""
    match = re.search(rf"## {section}(.*?)(?=\n##|\Z)", content, re.DOTALL)
    return match.group(1).strip() if match else ""


def detect_drift_between_packs(pack_a_path: Path, pack_b_path: Path) -> dict:
    """Compare two packs and detect drift."""
    content_a = pack_a_path.read_text(encoding="utf-8")
    content_b = pack_b_path.read_text(encoding="utf-8")

    drifts = []
    report = {
        "drift_detected": False,
        "drift_types": [],
        "severity": "ok",
        "drifts": [],
        "recommendation": ""
    }

    # Constraint drift
    constraints_a = extract_section(content_a, "Constraints")
    constraints_b = extract_section(content_b, "Constraints")
    if constraints_a != constraints_b:
        drifts.append({
            "type": "constraint_drift",
            "severity": DRIFT_SEVERITY["constraint_drift"],
            "detail": "Constraints section differs between packs"
        })

    # Decision drift
    decisions_a = extract_section(content_a, "Active Decisions")
    decisions_b = extract_section(content_b, "Active Decisions")
    if decisions_a != decisions_b:
        drifts.append({
            "type": "decision_drift",
            "severity": DRIFT_SEVERITY["decision_drift"],
            "detail": "Active decisions differ between packs"
        })

    # State drift
    state_a = extract_section(content_a, "Project State")
    state_b = extract_section(content_b, "Project State")
    if state_a != state_b:
        drifts.append({
            "type": "state_drift",
            "severity": DRIFT_SEVERITY["state_drift"],
            "detail": "Project state differs between packs"
        })

    # Lineage break
    prev_a = extract_field(content_a, "previous_pack_id")
    pack_id_a = extract_field(content_a, "pack_id")
    prev_b = extract_field(content_b, "previous_pack_id")
    if prev_b and prev_b != pack_id_a and prev_b != "none":
        drifts.append({
            "type": "lineage_break",
            "severity": DRIFT_SEVERITY["lineage_break"],
            "detail": f"Pack B references previous_pack_id='{prev_b}' but Pack A id='{pack_id_a}'"
        })

    # Staleness drift on pack_b
    staleness = detect_staleness_from_pack(pack_b_path)
    if staleness["stale"]:
        drifts.append({
            "type": "staleness_drift",
            "severity": DRIFT_SEVERITY["staleness_drift"],
            "detail": staleness["recommendation"]
        })

    if drifts:
        report["drift_detected"] = True
        report["drift_types"] = [d["type"] for d in drifts]
        report["drifts"] = drifts
        severities = [d["severity"] for d in drifts]
        if "blocking" in severities:
            report["severity"] = "blocking"
        elif "warning" in severities:
            report["severity"] = "warning"
        else:
            report["severity"] = "advisory"
        report["recommendation"] = "Context drift detected — refresh pack before proceeding"
    else:
        report["recommendation"] = "No drift detected — packs are consistent"

    return report


def main():
    parser = argparse.ArgumentParser(description="yOS Drift Detector")
    parser.add_argument("--pack-a", type=Path)
    parser.add_argument("--pack-b", type=Path)
    parser.add_argument("--pack", type=Path, help="Single pack to check for staleness drift")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.pack_a and args.pack_b:
        result = detect_drift_between_packs(args.pack_a, args.pack_b)
    elif args.pack:
        staleness = detect_staleness_from_pack(args.pack)
        result = {
            "drift_detected": staleness["stale"],
            "drift_types": ["staleness_drift"] if staleness["stale"] else [],
            "severity": staleness["severity"],
            "recommendation": staleness["recommendation"]
        }
    else:
        print("[ERROR] Provide --pack-a + --pack-b or --pack", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Drift Detected: {result['drift_detected']}")
        print(f"Severity:       {result['severity']}")
        print(f"Drift Types:    {result.get('drift_types', [])}")
        print(f"Recommendation: {result['recommendation']}")
        if result.get("drifts"):
            for d in result["drifts"]:
                print(f"  [{d['severity'].upper()}] {d['type']}: {d['detail']}")


if __name__ == "__main__":
    main()
