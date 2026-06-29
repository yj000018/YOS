#!/usr/bin/env python3
"""
enforcement_checker.py — yOS Continuity Core Phase 1
Enforce all continuity rules against a Context Pack.

Runs all 10 enforcement rules from CONTINUITY_ENFORCEMENT_PROTOCOL.md:
  E01: Context Pack Required at Boundary
  E02: CAP Validation
  E03: Staleness Check
  E04: Checksum Integrity
  E05: Session Mode Compliance
  E06: Constraint Acknowledgment
  E07: Routing Matrix Compliance
  E08: Memory Backend Declared
  E09: Handoff Completeness
  E10: Escalation Threshold

Usage:
  python3 enforcement_checker.py --pack PATH [--task-request TEXT]
"""

import re
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pack_staleness_detector import detect_staleness_from_pack
from context_pack_checksum_verifier import verify_pack_checksum
from cap_validator import validate_cap

ENFORCEMENT_RULES = [
    "E01_context_pack_required",
    "E02_cap_validation",
    "E03_staleness_check",
    "E04_checksum_integrity",
    "E05_session_mode_compliance",
    "E06_constraint_acknowledgment",
    "E07_routing_matrix_compliance",
    "E08_memory_backend_declared",
    "E09_handoff_completeness",
    "E10_escalation_threshold"
]

REQUIRED_FIELDS = [
    "pack_id", "pack_version", "tier", "context_pack_depth",
    "freshness_timestamp", "staleness_policy", "session_mode",
    "handoff_mode", "cap_required", "cap_acknowledged",
    "pack_checksum", "memory_backend", "canonical_memory"
]

ALLOWED_SESSION_MODES = {"stateless_context_pack_only", "previous_response_id", "live_session_stateful", "hybrid"}


def run_enforcement(pack_path: Path, task_request: str = "") -> dict:
    """Run all enforcement rules against a pack. Returns full enforcement report."""
    content = pack_path.read_text(encoding="utf-8")

    report = {
        "pack_path": str(pack_path),
        "enforcement_passed": True,
        "blocking_violations": [],
        "hard_stops": [],
        "warnings": [],
        "rule_results": {}
    }

    def add_violation(rule, severity, message):
        report["rule_results"][rule] = {"severity": severity, "message": message}
        if severity == "hard_stop":
            report["hard_stops"].append(f"[{rule}] {message}")
            report["enforcement_passed"] = False
        elif severity == "blocking":
            report["blocking_violations"].append(f"[{rule}] {message}")
            report["enforcement_passed"] = False
        elif severity in ("warning", "advisory"):
            report["warnings"].append(f"[{rule}] {message}")
        else:
            report["rule_results"][rule] = {"severity": "ok", "message": message}

    # E01: Context Pack Required at Boundary
    if not pack_path.exists():
        add_violation("E01_context_pack_required", "hard_stop", "Context pack file missing")
    else:
        add_violation("E01_context_pack_required", "ok", "Context pack present")

    # E02: CAP Validation
    cap_result = validate_cap(pack_path)
    if not cap_result["cap_valid"]:
        add_violation("E02_cap_validation", cap_result.get("severity", "blocking"),
                      f"CAP invalid: {cap_result.get('violations', [])}")
    else:
        add_violation("E02_cap_validation", "ok", "CAP valid (declarative acknowledgment present)")

    # E03: Staleness Check
    staleness = detect_staleness_from_pack(pack_path)
    if staleness["stale"]:
        add_violation("E03_staleness_check", staleness["action"], staleness["recommendation"])
    else:
        add_violation("E03_staleness_check", "ok", staleness["recommendation"])

    # E04: Checksum Integrity
    checksum_result = verify_pack_checksum(pack_path)
    if not checksum_result["verified"]:
        add_violation("E04_checksum_integrity", "blocking", checksum_result["message"])
    else:
        add_violation("E04_checksum_integrity", "ok", "Checksum verified (authoritative)")

    # E05: Session Mode Compliance
    mode_match = re.search(r"session_mode:\s*['\"]?([^\n'\"]+)['\"]?", content)
    if mode_match:
        mode = mode_match.group(1).strip()
        if mode not in ALLOWED_SESSION_MODES:
            add_violation("E05_session_mode_compliance", "blocking",
                          f"session_mode='{mode}' not in allowed set {sorted(ALLOWED_SESSION_MODES)}")
        else:
            add_violation("E05_session_mode_compliance", "ok", f"session_mode='{mode}' valid")
    else:
        add_violation("E05_session_mode_compliance", "warning", "session_mode field missing from pack")

    # E06: Constraint Acknowledgment
    constraints_section = re.search(r"## Constraints.*?(?=##|\Z)", content, re.DOTALL)
    if constraints_section:
        add_violation("E06_constraint_acknowledgment", "ok", "Constraints section present")
    else:
        add_violation("E06_constraint_acknowledgment", "warning", "Constraints section missing from pack")

    # E07: Routing Matrix Compliance
    tier_match = re.search(r"tier:\s*['\"]?([^\n'\"]+)['\"]?", content)
    if tier_match:
        tier = tier_match.group(1).strip()
        valid_tiers = {"T0_nano", "T1_standard", "T2_full_lineage", "T3_emergency_recovery"}
        if tier in valid_tiers:
            add_violation("E07_routing_matrix_compliance", "ok", f"tier='{tier}' valid")
        else:
            add_violation("E07_routing_matrix_compliance", "blocking",
                          f"tier='{tier}' not in canonical set {sorted(valid_tiers)}")
    else:
        add_violation("E07_routing_matrix_compliance", "warning", "tier field missing from pack")

    # E08: Memory Backend Declared
    mem_match = re.search(r"memory_backend:\s*['\"]?([^\n'\"]+)['\"]?", content)
    if mem_match and mem_match.group(1).strip():
        add_violation("E08_memory_backend_declared", "ok",
                      f"memory_backend='{mem_match.group(1).strip()}' declared")
    else:
        add_violation("E08_memory_backend_declared", "advisory", "memory_backend not declared — using default")

    # E09: Handoff Completeness
    required_present = []
    required_missing = []
    for field in ["next_action", "expected_output", "success_criteria"]:
        if re.search(rf"{field}:\s*\S", content):
            required_present.append(field)
        else:
            required_missing.append(field)
    if required_missing:
        add_violation("E09_handoff_completeness", "warning",
                      f"Handoff fields missing: {required_missing}")
    else:
        add_violation("E09_handoff_completeness", "ok", "All handoff fields present")

    # E10: Escalation Threshold
    escalation_keywords = ["emergency_recovery", "T3", "governance_gate", "authority_boundary"]
    found_escalation = [kw for kw in escalation_keywords if kw in content]
    if found_escalation:
        add_violation("E10_escalation_threshold", "advisory",
                      f"Escalation markers found: {found_escalation} — confirm_on_escalation policy applies")
    else:
        add_violation("E10_escalation_threshold", "ok", "No escalation markers")

    return report


def main():
    parser = argparse.ArgumentParser(description="yOS Enforcement Checker")
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--task-request", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.pack.exists():
        print(f"[ERROR] Pack not found: {args.pack}", file=sys.stderr)
        sys.exit(1)

    report = run_enforcement(args.pack, args.task_request)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        status = "✅ PASSED" if report["enforcement_passed"] else "❌ FAILED"
        print(f"Enforcement: {status}")
        if report["hard_stops"]:
            print("HARD STOPS:")
            for h in report["hard_stops"]:
                print(f"  🛑 {h}")
        if report["blocking_violations"]:
            print("BLOCKING:")
            for b in report["blocking_violations"]:
                print(f"  ⛔ {b}")
        if report["warnings"]:
            print("WARNINGS:")
            for w in report["warnings"]:
                print(f"  ⚠️  {w}")
        print("\nRule Results:")
        for rule, result in report["rule_results"].items():
            icon = "✅" if result["severity"] == "ok" else ("🛑" if result["severity"] == "hard_stop" else "⚠️")
            print(f"  {icon} {rule}: {result['message'][:80]}")

    if not report["enforcement_passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
