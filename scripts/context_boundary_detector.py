#!/usr/bin/env python3
"""
context_boundary_detector.py — yOS Continuity Core Phase 1
Detect when a Context Pack is required at a boundary.

Boundary types:
  llm_boundary, tool_boundary, agent_boundary, session_boundary,
  mission_boundary, phase_boundary, authority_boundary, governance_gate,
  recovery_event, model_switch, tool_switch, drift_recovery

Usage:
  python3 context_boundary_detector.py --task-request "..." [--current-state '{}']
"""

import json
import sys
import argparse
from pathlib import Path

BOUNDARY_TYPES = [
    "llm_boundary", "tool_boundary", "agent_boundary", "session_boundary",
    "mission_boundary", "phase_boundary", "authority_boundary", "governance_gate",
    "recovery_event", "model_switch", "tool_switch", "drift_recovery"
]

BOUNDARY_KEYWORDS = {
    "llm_boundary": ["switch llm", "change model", "use claude", "use gpt", "use gemini", "handoff to llm"],
    "tool_boundary": ["switch tool", "use tool", "handoff to tool", "run script"],
    "agent_boundary": ["handoff to agent", "delegate to", "pass to manus", "pass to chatgpt"],
    "session_boundary": ["new session", "fresh session", "start session", "close session"],
    "mission_boundary": ["new mission", "start mission", "mission boundary", "next mission"],
    "phase_boundary": ["next phase", "phase boundary", "start phase", "new phase"],
    "authority_boundary": ["chief architect", "founder", "authority boundary", "governance gate"],
    "governance_gate": ["governance gate", "gate review", "approval required", "gate check"],
    "recovery_event": ["recovery", "reconstruct", "drift recovery", "context lost", "corrupted"],
    "model_switch": ["switch model", "change model", "use different model"],
    "tool_switch": ["switch tool", "use different tool"],
    "drift_recovery": ["drift", "context drift", "session drift", "off track"],
}

DEPTH_RECOMMENDATION = {
    "llm_boundary": "standard",
    "tool_boundary": "minimal",
    "agent_boundary": "standard",
    "session_boundary": "standard",
    "mission_boundary": "full_lineage",
    "phase_boundary": "standard",
    "authority_boundary": "full_lineage",
    "governance_gate": "full_lineage",
    "recovery_event": "emergency_recovery",
    "model_switch": "standard",
    "tool_switch": "minimal",
    "drift_recovery": "emergency_recovery",
}

HANDOFF_RECOMMENDATION = {
    "llm_boundary": "standard_context_pack",
    "tool_boundary": "nano_pack",
    "agent_boundary": "standard_context_pack",
    "session_boundary": "standard_context_pack",
    "mission_boundary": "full_lineage_pack",
    "phase_boundary": "standard_context_pack",
    "authority_boundary": "full_lineage_pack",
    "governance_gate": "full_lineage_pack",
    "recovery_event": "emergency_recovery_pack",
    "model_switch": "standard_context_pack",
    "tool_switch": "nano_pack",
    "drift_recovery": "emergency_recovery_pack",
}


def detect_boundary(task_request: str, current_state: dict = None) -> dict:
    """Detect boundary type from task request text and current state."""
    text_lower = task_request.lower()
    detected = []
    confidence_map = {}

    for boundary_type, keywords in BOUNDARY_KEYWORDS.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            detected.append(boundary_type)
            confidence_map[boundary_type] = "medium" if len(matches) == 1 else "high"

    # Check current_state for explicit boundary declarations
    if current_state:
        declared = current_state.get("boundary_type")
        if declared and declared in BOUNDARY_TYPES:
            if declared not in detected:
                detected.append(declared)
            confidence_map[declared] = "high"

    if not detected:
        return {
            "boundary_detected": False,
            "boundary_types": [],
            "confidence": "none",
            "requires_context_pack": False,
            "recommended_depth": None,
            "recommended_handoff_mode": None,
            "advisory": "No boundary detected — context pack not required"
        }

    primary = detected[0]
    return {
        "boundary_detected": True,
        "boundary_types": detected,
        "primary_boundary": primary,
        "confidence": confidence_map.get(primary, "low"),
        "requires_context_pack": True,
        "recommended_depth": recommend_context_pack_depth(detected),
        "recommended_handoff_mode": recommend_handoff_mode(detected),
        "advisory": None
    }


def requires_context_pack(boundary_result: dict) -> bool:
    """Return True if a context pack is required."""
    return boundary_result.get("requires_context_pack", False)


def classify_boundary_type(task_request: str) -> list:
    """Return list of detected boundary types."""
    result = detect_boundary(task_request)
    return result.get("boundary_types", [])


def recommend_handoff_mode(boundary_types: list) -> str:
    """Recommend handoff mode based on most severe boundary type."""
    severity_order = [
        "recovery_event", "drift_recovery", "governance_gate", "authority_boundary",
        "mission_boundary", "full_lineage", "session_boundary", "agent_boundary",
        "llm_boundary", "model_switch", "phase_boundary", "tool_boundary", "tool_switch"
    ]
    for bt in severity_order:
        if bt in boundary_types:
            return HANDOFF_RECOMMENDATION.get(bt, "standard_context_pack")
    return "standard_context_pack"


def recommend_context_pack_depth(boundary_types: list) -> str:
    """Recommend context pack depth based on most severe boundary type."""
    severity_order = [
        "recovery_event", "drift_recovery", "governance_gate", "authority_boundary",
        "mission_boundary", "session_boundary", "agent_boundary", "llm_boundary",
        "model_switch", "phase_boundary", "tool_boundary", "tool_switch"
    ]
    for bt in severity_order:
        if bt in boundary_types:
            return DEPTH_RECOMMENDATION.get(bt, "standard")
    return "standard"


def main():
    parser = argparse.ArgumentParser(description="yOS Context Boundary Detector")
    parser.add_argument("--task-request", default="", help="Task description")
    parser.add_argument("--current-state", default="{}", help="JSON current state")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    current_state = json.loads(args.current_state)
    result = detect_boundary(args.task_request, current_state)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Boundary Detected:      {result['boundary_detected']}")
        if result["boundary_detected"]:
            print(f"Boundary Types:         {result['boundary_types']}")
            print(f"Confidence:             {result['confidence']}")
            print(f"Requires Context Pack:  {result['requires_context_pack']}")
            print(f"Recommended Depth:      {result['recommended_depth']}")
            print(f"Recommended Handoff:    {result['recommended_handoff_mode']}")
        else:
            print(f"Advisory:               {result['advisory']}")


if __name__ == "__main__":
    main()
