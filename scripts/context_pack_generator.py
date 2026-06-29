#!/usr/bin/env python3
"""
context_pack_generator.py — yOS Continuity Core Phase 1
Generate a Context Pack from a project state input.

Tiers:
  T0_nano              — ~500 tokens, identity + constraints + next action
  T1_standard          — ~2000 tokens, T0 + project state + active decisions + key artifacts
  T2_full_lineage      — ~8000 tokens, T1 + decision history + ADRs + lineage
  T3_emergency_recovery — full reconstruction pack

Usage:
  python3 context_pack_generator.py --project PROJECT --tier T1_standard [--output PATH]
  python3 context_pack_generator.py --input-json PATH --tier T0_nano
"""

import re
import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from routing_matrix_loader import load_routing_matrix, get_continuity_defaults

CANONICAL_TIERS = ["T0_nano", "T1_standard", "T2_full_lineage", "T3_emergency_recovery"]

TIER_SECTIONS = {
    "T0_nano": ["identity", "constraints", "next_action"],
    "T1_standard": ["identity", "constraints", "project_state", "active_decisions", "key_artifacts", "next_action"],
    "T2_full_lineage": ["identity", "constraints", "project_state", "active_decisions", "key_artifacts",
                        "decision_history", "adrs", "lineage", "next_action"],
    "T3_emergency_recovery": ["identity", "constraints", "project_state", "active_decisions", "key_artifacts",
                               "decision_history", "adrs", "lineage", "recovery_context",
                               "last_known_good_state", "next_action"]
}

TIER_DEPTH_MAP = {
    "T0_nano": "minimal",
    "T1_standard": "standard",
    "T2_full_lineage": "full_lineage",
    "T3_emergency_recovery": "emergency_recovery"
}


def generate_pack(project_data: dict, tier: str, routing_defaults: dict = None) -> str:
    """Generate a Context Pack string from project data."""
    if tier not in CANONICAL_TIERS:
        raise ValueError(f"Invalid tier: '{tier}'. Must be one of {CANONICAL_TIERS}")

    if routing_defaults is None:
        try:
            matrix = load_routing_matrix()
            routing_defaults = get_continuity_defaults(matrix=matrix)
        except SystemExit:
            routing_defaults = {}

    now_iso = datetime.now(timezone.utc).isoformat()
    pack_id = f"pack_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    depth = TIER_DEPTH_MAP[tier]

    sections = TIER_SECTIONS[tier]
    lines = []

    # Header
    lines += [
        f"# yOS Context Pack — {tier}",
        f"# Generated: {now_iso}",
        f"# Pack ID: {pack_id}",
        "",
        "## Metadata",
        f"pack_id: {pack_id}",
        f"pack_version: 2.1",
        f"tier: {tier}",
        f"context_pack_depth: {depth}",
        f"freshness_timestamp: {now_iso}",
        f"staleness_policy: {routing_defaults.get('default_staleness_policy', 'standard')}",
        f"session_mode: {routing_defaults.get('default_session_mode', 'stateless_context_pack_only')}",
        f"handoff_mode: {routing_defaults.get('default_handoff_mode', 'standard_context_pack')}",
        f"memory_backend: {project_data.get('memory_backend', 'notion | mem0 | git')}",
        f"shared_pack_uri: {project_data.get('shared_pack_uri', '')}",
        f"shared_pack_backend: {project_data.get('shared_pack_backend', 'git')}",
        f"canonical_memory: {project_data.get('canonical_memory', 'Notion + Mem0')}",
        f"cap_required: {routing_defaults.get('cap_required_by_default', 'true')}",
        f"cap_acknowledged: false",
        f"cap_acknowledged_by: <PENDING>",
        f"cap_acknowledged_at: <PENDING>",
        f"cap_constraints_hash: <PENDING>",
        f"pack_checksum: <COMPUTED_AFTER_FINALIZATION>",
        "",
    ]

    # Identity section (all tiers)
    if "identity" in sections:
        lines += [
            "## Identity",
            f"founder: {project_data.get('founder', 'Yannick')}",
            f"project: {project_data.get('project', '')}",
            f"program: {project_data.get('program', '')}",
            f"mission: {project_data.get('mission', '')}",
            f"current_phase: {project_data.get('current_phase', '')}",
            f"task_class: {project_data.get('task_class', 'default')}",
            "",
        ]

    # Constraints section (all tiers)
    if "constraints" in sections:
        constraints = project_data.get("constraints", [])
        lines += ["## Constraints (DO-NOT list)"]
        if constraints:
            for c in constraints:
                lines.append(f"  - {c}")
        else:
            lines.append("  - <No constraints specified>")
        lines.append("")

    # Project state (T1+)
    if "project_state" in sections:
        state = project_data.get("project_state", {})
        lines += [
            "## Project State",
            f"status: {state.get('status', 'unknown')}",
            f"milestone: {state.get('milestone', '')}",
            f"blockers: {state.get('blockers', 'none')}",
            f"last_completed: {state.get('last_completed', '')}",
            "",
        ]

    # Active decisions (T1+)
    if "active_decisions" in sections:
        decisions = project_data.get("active_decisions", [])
        lines += ["## Active Decisions"]
        if decisions:
            for d in decisions:
                lines.append(f"  - {d}")
        else:
            lines.append("  - <None>")
        lines.append("")

    # Key artifacts (T1+)
    if "key_artifacts" in sections:
        artifacts = project_data.get("key_artifacts", [])
        lines += ["## Key Artifacts"]
        if artifacts:
            for a in artifacts:
                lines.append(f"  - {a}")
        else:
            lines.append("  - <None>")
        lines.append("")

    # Decision history (T2+)
    if "decision_history" in sections:
        history = project_data.get("decision_history", [])
        lines += ["## Decision History"]
        if history:
            for h in history:
                lines.append(f"  - {h}")
        else:
            lines.append("  - <None>")
        lines.append("")

    # ADRs (T2+)
    if "adrs" in sections:
        adrs = project_data.get("adrs", [])
        lines += ["## ADRs"]
        if adrs:
            for adr in adrs:
                lines.append(f"  - {adr}")
        else:
            lines.append("  - <None>")
        lines.append("")

    # Lineage (T2+)
    if "lineage" in sections:
        lines += [
            "## Lineage",
            f"previous_pack_id: {project_data.get('previous_pack_id', 'none')}",
            f"lineage_chain: {project_data.get('lineage_chain', 'none')}",
            "",
        ]

    # Recovery context (T3 only)
    if "recovery_context" in sections:
        lines += [
            "## Recovery Context",
            f"recovery_trigger: {project_data.get('recovery_trigger', '')}",
            f"last_known_good_state: {project_data.get('last_known_good_state', '')}",
            f"recovery_instructions: {project_data.get('recovery_instructions', '')}",
            "",
        ]

    # Next action (all tiers)
    if "next_action" in sections:
        lines += [
            "## Next Action",
            f"next_action: {project_data.get('next_action', '')}",
            f"expected_output: {project_data.get('expected_output', '')}",
            f"success_criteria: {project_data.get('success_criteria', '')}",
            "",
        ]

    pack_content = "\n".join(lines)

    # Compute and inject checksum
    checksum = hashlib.sha256(
        pack_content.replace("pack_checksum: <COMPUTED_AFTER_FINALIZATION>",
                             "pack_checksum: <EXCLUDED_FOR_CHECKSUM>")
        .encode("utf-8")
    ).hexdigest()
    pack_content = pack_content.replace(
        "pack_checksum: <COMPUTED_AFTER_FINALIZATION>",
        f"pack_checksum: {checksum}"
    )

    return pack_content


def main():
    parser = argparse.ArgumentParser(description="yOS Context Pack Generator")
    parser.add_argument("--project", default="", help="Project name")
    parser.add_argument("--tier", default="T1_standard", choices=CANONICAL_TIERS)
    parser.add_argument("--input-json", type=Path, help="JSON file with project data")
    parser.add_argument("--output", type=Path, help="Output file path")
    args = parser.parse_args()

    if args.input_json and args.input_json.exists():
        project_data = json.loads(args.input_json.read_text())
    else:
        project_data = {"project": args.project}

    pack = generate_pack(project_data, args.tier)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(pack, encoding="utf-8")
        print(f"Pack written to: {args.output}")
    else:
        print(pack)


if __name__ == "__main__":
    main()
