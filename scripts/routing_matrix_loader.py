#!/usr/bin/env python3
"""
routing_matrix_loader.py — yOS Continuity Core Phase 1
Load task-class defaults and continuity defaults from LLM_AND_TOOL_ROUTING_MATRIX.md.

Canonical Source:
  YOS/core/orchestration/registries/LLM_AND_TOOL_ROUTING_MATRIX.md

Usage:
  python3 routing_matrix_loader.py --matrix PATH [--task-class CLASS] [--validate]
"""

import re
import sys
import json
import argparse
from pathlib import Path

CANONICAL_MATRIX_PATH = Path(__file__).parent.parent / "core/orchestration/registries/LLM_AND_TOOL_ROUTING_MATRIX.md"

ALLOWED_SESSION_MODES = {"stateless_context_pack_only", "previous_response_id", "live_session_stateful", "hybrid"}
ALLOWED_CANONICAL_MEMORY_MODES = {"required", "auto_if_high_risk", "disabled"}
ALLOWED_CONTEXT_PACK_DEPTHS = {"minimal", "standard", "full_lineage", "emergency_recovery"}
ALLOWED_SESSION_CONTINUITY_MODES = {"none", "previous_response_id", "live_session"}
ALLOWED_HANDOFF_MODES = {"standard_context_pack", "full_lineage_pack", "emergency_recovery_pack", "nano_pack", "none"}
ALLOWED_CONFIRMATION_POLICIES = {"inform_only", "confirm_on_escalation", "confirm_always"}
ALLOWED_ENFORCEMENT_LEVELS = {"advisory", "warning", "blocking", "hard_stop"}
ALLOWED_STALENESS_POLICIES = {"strict", "standard", "relaxed", "none"}
ALLOWED_TIERS = {"T0_nano", "T1_standard", "T2_full_lineage", "T3_emergency_recovery"}

TASK_CLASSES = [
    "book_prose", "architecture", "code_generation", "research",
    "data_analysis", "vision_image", "translation", "conversation", "default"
]

CONTINUITY_FIELDS = [
    "default_session_mode", "default_canonical_memory_mode", "default_context_pack_depth",
    "default_session_continuity_mode", "default_handoff_mode", "default_confirmation_policy",
    "default_enforcement_level", "auto_escalation_allowed", "default_context_pack_tier",
    "default_staleness_policy", "cap_required_by_default"
]


def load_routing_matrix(path: Path = None) -> dict:
    """Load and parse the routing matrix from Markdown."""
    matrix_path = path or CANONICAL_MATRIX_PATH
    if not matrix_path.exists():
        print(f"[HARD_STOP] Canonical routing matrix missing: {matrix_path}", file=sys.stderr)
        sys.exit(2)

    content = matrix_path.read_text(encoding="utf-8")
    result = {
        "task_classes": {},
        "continuity_defaults": {},
        "tier_mapping": {},
        "crt_modes": {},
        "raw_path": str(matrix_path),
        "parse_warnings": []
    }

    # Parse task class table (Section 3)
    task_table_match = re.search(
        r"## 3\. LLM Routing Matrix by Task Class.*?\n(\|.*?\n)+",
        content, re.DOTALL
    )
    if task_table_match:
        rows = re.findall(r"^\| `?(\w+)`? \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|",
                          task_table_match.group(0), re.MULTILINE)
        for row in rows:
            tc = row[0].strip()
            if tc in TASK_CLASSES:
                result["task_classes"][tc] = {
                    "primary_llm": row[1].strip(),
                    "fallback_llm": row[2].strip(),
                    "context_window": row[3].strip(),
                    "output_window": row[4].strip(),
                    "latency": row[5].strip(),
                    "cost_risk": row[6].strip(),
                    "qc_requirement": row[7].strip()
                }
    else:
        result["parse_warnings"].append("Section 3 task class table not found — using empty defaults")

    # Parse continuity defaults table (Section 5)
    cont_table_match = re.search(
        r"## 5\. Continuity Core Default Fields.*?\n(\|.*?\n)+",
        content, re.DOTALL
    )
    if cont_table_match:
        rows = re.findall(r"^\| `?([a-z_]+)`? \| `?([^|]+?)`? \|",
                          cont_table_match.group(0), re.MULTILINE)
        for field, value in rows:
            f = field.strip()
            v = value.strip().strip("`")
            if f in CONTINUITY_FIELDS:
                result["continuity_defaults"][f] = v
    else:
        result["parse_warnings"].append("Section 5 continuity defaults table not found")

    # Parse tier mapping
    tier_match = re.search(r"### Context Pack Tier Mapping.*?\n(\|.*?\n)+", content, re.DOTALL)
    if tier_match:
        rows = re.findall(r"^\| `?([A-Z0-9_a-z]+)`? \| `?([a-z_]+)`? \|",
                          tier_match.group(0), re.MULTILINE)
        for tier, depth in rows:
            t = tier.strip()
            d = depth.strip()
            if t in ALLOWED_TIERS:
                result["tier_mapping"][t] = d

    return result


def get_task_class_defaults(task_class: str, matrix: dict = None) -> dict:
    """Return routing defaults for a given task class."""
    if matrix is None:
        matrix = load_routing_matrix()
    tc = matrix["task_classes"]
    if task_class in tc:
        return tc[task_class]
    if "default" in tc:
        return tc["default"]
    return {"primary_llm": "Claude 3.7 Sonnet", "fallback_llm": "GPT-4o", "qc_requirement": "General Sanity Check"}


def get_continuity_defaults(task_class: str = None, matrix: dict = None) -> dict:
    """Return continuity defaults (task_class not yet used for per-class overrides in Phase 1)."""
    if matrix is None:
        matrix = load_routing_matrix()
    return dict(matrix.get("continuity_defaults", {}))


def validate_continuity_enums(defaults: dict) -> list:
    """Validate continuity defaults against allowed enum values. Returns list of violations."""
    violations = []
    checks = {
        "default_session_mode": ALLOWED_SESSION_MODES,
        "default_canonical_memory_mode": ALLOWED_CANONICAL_MEMORY_MODES,
        "default_context_pack_depth": ALLOWED_CONTEXT_PACK_DEPTHS,
        "default_session_continuity_mode": ALLOWED_SESSION_CONTINUITY_MODES,
        "default_handoff_mode": ALLOWED_HANDOFF_MODES,
        "default_confirmation_policy": ALLOWED_CONFIRMATION_POLICIES,
        "default_enforcement_level": ALLOWED_ENFORCEMENT_LEVELS,
        "default_staleness_policy": ALLOWED_STALENESS_POLICIES,
        "default_context_pack_tier": ALLOWED_TIERS,
    }
    for field, allowed in checks.items():
        val = defaults.get(field)
        if val and val not in allowed:
            violations.append(f"ENUM_VIOLATION: {field}='{val}' not in {sorted(allowed)}")
    return violations


def report_missing_fields(matrix: dict = None) -> list:
    """Report missing continuity fields in the loaded matrix."""
    if matrix is None:
        matrix = load_routing_matrix()
    defaults = matrix.get("continuity_defaults", {})
    missing = [f for f in CONTINUITY_FIELDS if f not in defaults]
    return missing


def main():
    parser = argparse.ArgumentParser(description="yOS Routing Matrix Loader")
    parser.add_argument("--matrix", type=Path, default=CANONICAL_MATRIX_PATH, help="Path to routing matrix MD")
    parser.add_argument("--task-class", default="default", help="Task class to query")
    parser.add_argument("--validate", action="store_true", help="Validate continuity enums")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    matrix = load_routing_matrix(args.matrix)

    if args.validate:
        defaults = get_continuity_defaults(matrix=matrix)
        violations = validate_continuity_enums(defaults)
        missing = report_missing_fields(matrix)
        if violations:
            print("[VIOLATIONS]")
            for v in violations:
                print(f"  {v}")
        else:
            print("[OK] All continuity enums valid")
        if missing:
            print(f"[MISSING FIELDS] {missing}")
        if matrix["parse_warnings"]:
            print(f"[WARNINGS] {matrix['parse_warnings']}")
        return

    tc_defaults = get_task_class_defaults(args.task_class, matrix)
    cont_defaults = get_continuity_defaults(args.task_class, matrix)

    output = {
        "task_class": args.task_class,
        "routing": tc_defaults,
        "continuity": cont_defaults,
        "tier_mapping": matrix["tier_mapping"],
        "parse_warnings": matrix["parse_warnings"]
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Task Class: {args.task_class}")
        print(f"Primary LLM: {tc_defaults.get('primary_llm', 'unknown')}")
        print(f"Fallback LLM: {tc_defaults.get('fallback_llm', 'unknown')}")
        print(f"Context Pack Depth: {cont_defaults.get('default_context_pack_depth', 'standard')}")
        print(f"Staleness Policy: {cont_defaults.get('default_staleness_policy', 'standard')}")
        print(f"CAP Required: {cont_defaults.get('cap_required_by_default', 'true')}")
        if matrix["parse_warnings"]:
            print(f"Warnings: {matrix['parse_warnings']}")


if __name__ == "__main__":
    main()
