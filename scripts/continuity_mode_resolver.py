#!/usr/bin/env python3
"""
continuity_mode_resolver.py — yOS Continuity Core Phase 1
Resolve the correct context/session mode for a task.

Priority order:
  1. Explicit user instruction
  2. L3 / Chief Architect workflow
  3. Programmatic mission parameters
  4. Routing matrix defaults
  5. Manus proactive suggestion
  6. Runtime fallback rules

Usage:
  python3 continuity_mode_resolver.py --task-class architecture [--mission-params '{}']
"""

import json
import sys
import argparse
from pathlib import Path

# Add scripts dir to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))
from routing_matrix_loader import load_routing_matrix, get_continuity_defaults, ALLOWED_SESSION_MODES, ALLOWED_CONTEXT_PACK_DEPTHS

ESCALATION_KEYWORDS = [
    "architecture", "governance", "gate", "canonical", "recovery", "emergency",
    "full lineage", "high risk", "critical", "founder", "chief architect", "doctrine"
]

HEAVY_MODE_KEYWORDS = [
    "full_lineage", "emergency_recovery", "T2", "T3", "live_session_stateful"
]

CONFIRMATION_REQUIRED_MODES = {"live_session_stateful", "emergency_recovery"}


def resolve_mode(task_request: str, mission_params: dict = None, routing_defaults: dict = None) -> dict:
    """
    Resolve continuity mode from all priority sources.
    Returns resolution report dict.
    """
    report = {
        "resolved_session_mode": None,
        "resolved_context_pack_depth": None,
        "resolved_staleness_policy": None,
        "resolved_handoff_mode": None,
        "resolution_source": None,
        "escalation_detected": False,
        "confirmation_required": False,
        "confirmation_reason": None,
        "warnings": [],
        "mode_resolution_log": []
    }

    # Priority 1: Explicit user overrides in task_request text
    user_overrides = detect_explicit_user_overrides(task_request)
    if user_overrides:
        report["resolved_session_mode"] = user_overrides.get("session_mode")
        report["resolved_context_pack_depth"] = user_overrides.get("context_pack_depth")
        report["resolution_source"] = "explicit_user_instruction"
        report["mode_resolution_log"].append(f"P1 user override: {user_overrides}")

    # Priority 2 & 3: Mission params
    if mission_params:
        if not report["resolved_session_mode"] and "session_mode" in mission_params:
            val = mission_params["session_mode"]
            if val in ALLOWED_SESSION_MODES:
                report["resolved_session_mode"] = val
                report["resolution_source"] = "programmatic_mission_params"
                report["mode_resolution_log"].append(f"P3 mission param session_mode={val}")
            else:
                report["warnings"].append(f"Invalid session_mode in mission_params: '{val}'")

        if not report["resolved_context_pack_depth"] and "context_pack_depth" in mission_params:
            val = mission_params["context_pack_depth"]
            if val in ALLOWED_CONTEXT_PACK_DEPTHS:
                report["resolved_context_pack_depth"] = val
                report["mode_resolution_log"].append(f"P3 mission param context_pack_depth={val}")
            else:
                report["warnings"].append(f"Invalid context_pack_depth in mission_params: '{val}'")

    # Priority 4: Routing matrix defaults
    if routing_defaults is None:
        try:
            matrix = load_routing_matrix()
            routing_defaults = get_continuity_defaults(matrix=matrix)
        except SystemExit:
            routing_defaults = {}
            report["warnings"].append("Routing matrix unavailable — using hardcoded fallback defaults")

    if not report["resolved_session_mode"]:
        report["resolved_session_mode"] = routing_defaults.get("default_session_mode", "stateless_context_pack_only")
        report["resolution_source"] = report["resolution_source"] or "routing_matrix_defaults"
        report["mode_resolution_log"].append(f"P4 matrix default session_mode={report['resolved_session_mode']}")

    if not report["resolved_context_pack_depth"]:
        report["resolved_context_pack_depth"] = routing_defaults.get("default_context_pack_depth", "standard")
        report["mode_resolution_log"].append(f"P4 matrix default context_pack_depth={report['resolved_context_pack_depth']}")

    report["resolved_staleness_policy"] = routing_defaults.get("default_staleness_policy", "standard")
    report["resolved_handoff_mode"] = routing_defaults.get("default_handoff_mode", "standard_context_pack")

    # Escalation detection
    escalation = detect_escalation_triggers(task_request)
    if escalation:
        report["escalation_detected"] = True
        report["mode_resolution_log"].append(f"Escalation triggers detected: {escalation}")
        # Suggest escalation but do NOT silently escalate heavy modes
        if report["resolved_context_pack_depth"] in ("minimal", "standard"):
            report["warnings"].append(
                f"Escalation triggers detected ({escalation}) — consider upgrading to full_lineage. "
                "Confirmation required before escalating."
            )

    # Confirmation policy
    conf_result = apply_confirmation_policy(report["resolved_session_mode"])
    report["confirmation_required"] = conf_result["required"]
    report["confirmation_reason"] = conf_result["reason"]

    return report


def detect_explicit_user_overrides(text: str) -> dict:
    """Detect explicit session/context mode instructions in user text."""
    overrides = {}
    text_lower = text.lower()

    mode_map = {
        "stateless": "stateless_context_pack_only",
        "context pack only": "stateless_context_pack_only",
        "live session": "live_session_stateful",
        "stateful": "live_session_stateful",
        "previous_response_id": "previous_response_id",
    }
    for kw, mode in mode_map.items():
        if kw in text_lower:
            overrides["session_mode"] = mode
            break

    depth_map = {
        "t0": "minimal", "nano": "minimal",
        "t1": "standard", "standard pack": "standard",
        "t2": "full_lineage", "full lineage": "full_lineage",
        "t3": "emergency_recovery", "emergency recovery": "emergency_recovery",
    }
    for kw, depth in depth_map.items():
        if kw in text_lower:
            overrides["context_pack_depth"] = depth
            break

    return overrides


def detect_escalation_triggers(text: str) -> list:
    """Detect escalation trigger keywords in task text."""
    text_lower = text.lower()
    return [kw for kw in ESCALATION_KEYWORDS if kw in text_lower]


def apply_confirmation_policy(session_mode: str) -> dict:
    """Determine if confirmation is required for the resolved mode."""
    if session_mode in CONFIRMATION_REQUIRED_MODES:
        return {
            "required": True,
            "reason": f"Mode '{session_mode}' requires explicit confirmation before execution"
        }
    return {"required": False, "reason": None}


def produce_mode_resolution_report(report: dict) -> str:
    """Format resolution report as readable text."""
    lines = [
        "=== Continuity Mode Resolution Report ===",
        f"Resolved Session Mode:       {report['resolved_session_mode']}",
        f"Resolved Context Pack Depth: {report['resolved_context_pack_depth']}",
        f"Resolved Staleness Policy:   {report['resolved_staleness_policy']}",
        f"Resolved Handoff Mode:       {report['resolved_handoff_mode']}",
        f"Resolution Source:           {report['resolution_source']}",
        f"Escalation Detected:         {report['escalation_detected']}",
        f"Confirmation Required:       {report['confirmation_required']}",
    ]
    if report["confirmation_reason"]:
        lines.append(f"Confirmation Reason:         {report['confirmation_reason']}")
    if report["warnings"]:
        lines.append("Warnings:")
        for w in report["warnings"]:
            lines.append(f"  - {w}")
    lines.append("Resolution Log:")
    for entry in report["mode_resolution_log"]:
        lines.append(f"  {entry}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="yOS Continuity Mode Resolver")
    parser.add_argument("--task-class", default="default")
    parser.add_argument("--task-request", default="", help="Task description text")
    parser.add_argument("--mission-params", default="{}", help="JSON mission params")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    mission_params = json.loads(args.mission_params)
    report = resolve_mode(args.task_request, mission_params)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(produce_mode_resolution_report(report))


if __name__ == "__main__":
    main()
