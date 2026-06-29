#!/usr/bin/env python3
"""
handoff_packet_builder.py — yOS Continuity Core Phase 1
Build a Handoff Packet for LLM-to-LLM or agent-to-agent transfer.

A Handoff Packet = Context Pack + routing instructions + confirmation policy.
Every handoff must make the next actor able to act without guessing.

Handoff Packet fields:
  - context_pack (embedded or referenced)
  - from_actor / to_actor
  - handoff_mode
  - task_class
  - confirmation_policy
  - do_not_list
  - expected_output
  - success_criteria
  - blockers
  - next_step_if_blocked

Usage:
  python3 handoff_packet_builder.py --from manus --to chatgpt --project PROJECT [--tier T1_standard]
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from context_pack_generator import generate_pack, CANONICAL_TIERS
from routing_matrix_loader import load_routing_matrix, get_continuity_defaults, get_task_class_defaults

ACTOR_PROFILES = {
    "manus": {"role": "executor", "capabilities": ["code", "web", "file_ops", "browser", "parallel"]},
    "chatgpt": {"role": "chief_architect", "capabilities": ["architecture", "design", "review", "MPM"]},
    "claude": {"role": "prose_writer", "capabilities": ["book_prose", "long_form", "analysis"]},
    "gemini": {"role": "long_doc_processor", "capabilities": ["long_context", "document_analysis"]},
    "founder": {"role": "authority", "capabilities": ["decision", "approval", "governance"]},
    "n8n": {"role": "automation", "capabilities": ["workflow", "scheduling", "integration"]},
}


def build_handoff_packet(
    from_actor: str,
    to_actor: str,
    project_data: dict,
    tier: str = "T1_standard",
    task_class: str = "default",
    do_not_list: list = None,
    blockers: list = None,
    next_step_if_blocked: str = "",
    embed_pack: bool = True
) -> dict:
    """Build a complete Handoff Packet."""

    try:
        matrix = load_routing_matrix()
        routing_defaults = get_continuity_defaults(matrix=matrix)
        tc_defaults = get_task_class_defaults(task_class, matrix)
    except SystemExit:
        routing_defaults = {}
        tc_defaults = {}

    now_iso = datetime.now(timezone.utc).isoformat()
    packet_id = f"handoff_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    # Determine handoff mode
    handoff_mode = routing_defaults.get("default_handoff_mode", "standard_context_pack")
    if tier == "T2_full_lineage":
        handoff_mode = "full_lineage_pack"
    elif tier == "T3_emergency_recovery":
        handoff_mode = "emergency_recovery_pack"
    elif tier == "T0_nano":
        handoff_mode = "nano_pack"

    # Confirmation policy
    confirmation_policy = routing_defaults.get("default_confirmation_policy", "inform_only")
    if to_actor == "founder":
        confirmation_policy = "confirm_always"
    elif handoff_mode in ("full_lineage_pack", "emergency_recovery_pack"):
        confirmation_policy = "confirm_on_escalation"

    # Build packet
    packet = {
        "packet_id": packet_id,
        "generated_at": now_iso,
        "from_actor": from_actor,
        "to_actor": to_actor,
        "from_actor_profile": ACTOR_PROFILES.get(from_actor, {}),
        "to_actor_profile": ACTOR_PROFILES.get(to_actor, {}),
        "handoff_mode": handoff_mode,
        "tier": tier,
        "task_class": task_class,
        "primary_llm": tc_defaults.get("primary_llm", ""),
        "confirmation_policy": confirmation_policy,
        "do_not_list": do_not_list or project_data.get("constraints", []),
        "expected_output": project_data.get("expected_output", ""),
        "success_criteria": project_data.get("success_criteria", ""),
        "blockers": blockers or project_data.get("project_state", {}).get("blockers", "none"),
        "next_step_if_blocked": next_step_if_blocked or "Escalate to Founder",
        "next_action": project_data.get("next_action", ""),
        "context_pack_embedded": None,
        "context_pack_reference": None,
    }

    if embed_pack:
        pack_content = generate_pack(project_data, tier, routing_defaults)
        packet["context_pack_embedded"] = pack_content
    else:
        packet["context_pack_reference"] = project_data.get("shared_pack_uri", "")

    return packet


def format_handoff_packet_md(packet: dict) -> str:
    """Format handoff packet as Markdown."""
    lines = [
        f"# Handoff Packet — {packet['packet_id']}",
        f"Generated: {packet['generated_at']}",
        "",
        "## Routing",
        f"From: {packet['from_actor']} ({packet['from_actor_profile'].get('role', '')})",
        f"To:   {packet['to_actor']} ({packet['to_actor_profile'].get('role', '')})",
        f"Handoff Mode: {packet['handoff_mode']}",
        f"Tier: {packet['tier']}",
        f"Task Class: {packet['task_class']}",
        f"Primary LLM: {packet['primary_llm']}",
        f"Confirmation Policy: {packet['confirmation_policy']}",
        "",
        "## DO-NOT List",
    ]
    for item in (packet["do_not_list"] or []):
        lines.append(f"  - {item}")

    lines += [
        "",
        "## Task",
        f"Next Action: {packet['next_action']}",
        f"Expected Output: {packet['expected_output']}",
        f"Success Criteria: {packet['success_criteria']}",
        "",
        "## Blockers",
        f"Blockers: {packet['blockers']}",
        f"If Blocked: {packet['next_step_if_blocked']}",
        "",
    ]

    if packet.get("context_pack_embedded"):
        lines += [
            "## Embedded Context Pack",
            "```",
            packet["context_pack_embedded"][:500] + "\n... [truncated — full pack embedded]",
            "```",
        ]
    elif packet.get("context_pack_reference"):
        lines.append(f"Context Pack Reference: {packet['context_pack_reference']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="yOS Handoff Packet Builder")
    parser.add_argument("--from", dest="from_actor", default="manus")
    parser.add_argument("--to", dest="to_actor", default="chatgpt")
    parser.add_argument("--project", default="yos")
    parser.add_argument("--tier", default="T1_standard", choices=CANONICAL_TIERS)
    parser.add_argument("--task-class", default="architecture")
    parser.add_argument("--input-json", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.input_json and args.input_json.exists():
        project_data = json.loads(args.input_json.read_text())
    else:
        project_data = {"project": args.project}

    packet = build_handoff_packet(
        args.from_actor, args.to_actor, project_data,
        tier=args.tier, task_class=args.task_class
    )

    if args.json:
        output = json.dumps(packet, indent=2)
    else:
        output = format_handoff_packet_md(packet)

    if args.output:
        args.output.write_text(output)
        print(f"Handoff packet written: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
