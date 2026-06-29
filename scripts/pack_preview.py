#!/usr/bin/env python3
"""
pack_preview.py — yOS Continuity Core Phase 1
Preview a Context Pack before injection into an LLM.

Shows: tier, session_mode, depth, staleness, CAP status, next_action, constraints count.
Warns before injecting expensive T2/T3 packs.

Usage:
  python3 pack_preview.py --pack PATH
  python3 pack_preview.py --pack PATH --full
"""

import re
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pack_staleness_detector import detect_staleness_from_pack

EXPENSIVE_TIERS = {"T2_full_lineage", "T3_emergency_recovery"}
EXPENSIVE_MODES = {"live_session_stateful", "emergency_recovery"}


def extract_field(content: str, field: str) -> str:
    match = re.search(rf"^{field}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "<not set>"


def count_constraints(content: str) -> int:
    section = re.search(r"## Constraints.*?(?=\n##|\Z)", content, re.DOTALL)
    if not section:
        return 0
    return len(re.findall(r"^\s+-\s+\S", section.group(0), re.MULTILINE))


def preview_pack(pack_path: Path, full: bool = False) -> dict:
    """Generate a preview summary of a Context Pack."""
    content = pack_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    tier = extract_field(content, "tier")
    session_mode = extract_field(content, "session_mode")
    depth = extract_field(content, "context_pack_depth")
    pack_id = extract_field(content, "pack_id")
    freshness = extract_field(content, "freshness_timestamp")
    staleness_policy = extract_field(content, "staleness_policy")
    cap_ack = extract_field(content, "cap_acknowledged")
    next_action = extract_field(content, "next_action")
    project = extract_field(content, "project")
    checksum = extract_field(content, "pack_checksum")
    handoff_mode = extract_field(content, "handoff_mode")

    staleness = detect_staleness_from_pack(pack_path)
    constraints_count = count_constraints(content)

    expensive = tier in EXPENSIVE_TIERS or session_mode in EXPENSIVE_MODES
    cap_pending = cap_ack in ("<PENDING>", "false", "False", "<not set>")

    warnings = []
    if expensive:
        warnings.append(f"⚠️  EXPENSIVE: tier={tier}, session_mode={session_mode} — confirm before injecting")
    if staleness["stale"]:
        warnings.append(f"⚠️  STALE: {staleness['recommendation']}")
    if cap_pending:
        warnings.append("⚠️  CAP NOT ACKNOWLEDGED — LLM must declare acknowledgment before execution")

    preview = {
        "pack_id": pack_id,
        "project": project,
        "tier": tier,
        "session_mode": session_mode,
        "context_pack_depth": depth,
        "handoff_mode": handoff_mode,
        "freshness_timestamp": freshness,
        "staleness_policy": staleness_policy,
        "stale": staleness["stale"],
        "staleness_age_hours": staleness.get("age_hours"),
        "cap_acknowledged": cap_ack,
        "cap_pending": cap_pending,
        "constraints_count": constraints_count,
        "next_action": next_action,
        "checksum_prefix": checksum[:16] if len(checksum) >= 16 else checksum,
        "total_lines": len(lines),
        "expensive": expensive,
        "warnings": warnings,
        "ready_to_inject": not expensive and not staleness["stale"] and not cap_pending
    }

    if full:
        preview["full_content"] = content

    return preview


def format_preview(preview: dict) -> str:
    ready = "✅ READY" if preview["ready_to_inject"] else "⚠️  REVIEW REQUIRED"
    lines = [
        f"=== Context Pack Preview — {preview['pack_id']} ===",
        f"Status:         {ready}",
        f"Project:        {preview['project']}",
        f"Tier:           {preview['tier']}",
        f"Session Mode:   {preview['session_mode']}",
        f"Depth:          {preview['context_pack_depth']}",
        f"Handoff Mode:   {preview['handoff_mode']}",
        f"Freshness:      {preview['freshness_timestamp']}",
        f"Age (hours):    {preview['staleness_age_hours']}",
        f"Stale:          {preview['stale']}",
        f"CAP Ack:        {preview['cap_acknowledged']}",
        f"Constraints:    {preview['constraints_count']}",
        f"Next Action:    {preview['next_action'][:80]}",
        f"Lines:          {preview['total_lines']}",
        f"Checksum:       {preview['checksum_prefix']}...",
    ]
    if preview["warnings"]:
        lines.append("\nWarnings:")
        for w in preview["warnings"]:
            lines.append(f"  {w}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="yOS Pack Preview")
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--full", action="store_true", help="Include full pack content")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.pack.exists():
        print(f"[ERROR] Pack not found: {args.pack}", file=sys.stderr)
        sys.exit(1)

    preview = preview_pack(args.pack, args.full)

    if args.json:
        print(json.dumps(preview, indent=2))
    else:
        print(format_preview(preview))


if __name__ == "__main__":
    main()
