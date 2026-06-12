#!/usr/bin/env python3
"""
Y-COO MVP v1.0 — Y-OS Chief Operating Officer Agent
Layer 3 — Organization

Consumes: Mission Pack (from Y-ORC)
Produces: Execution Plan

COO does NOT execute work.
COO decides, coordinates, and delegates.
"""

import json, uuid, sys, os, re
from datetime import datetime

# ─── Agent Profiles ───────────────────────────────────────────────────────────
AGENT_PROFILES = {
    "research": {
        "triggers": ["web-search", "semantic-search", "data-analysis", "web-scraping",
                     "relevance-scoring", "cross-session-recall"],
        "primary": "agent--researcher",
        "secondary": "agent--pa",
        "label": "Research-heavy"
    },
    "development": {
        "triggers": ["code-execution", "web-development", "api-integration",
                     "deployment-automation", "testing-validation", "github-integration"],
        "primary": "agent--architect",
        "secondary": "agent--developer",
        "label": "Development-heavy"
    },
    "strategy": {
        "triggers": ["mission-pack-generation", "workflow-planning", "gap-analysis",
                     "context-pack-generation", "agent-routing"],
        "primary": "agent--strategist",
        "secondary": "agent--coo",
        "label": "Strategy-heavy"
    },
    "organization": {
        "triggers": ["namespace-management", "object-registration", "relation-traversal",
                     "execution-history"],
        "primary": "agent--hr",
        "secondary": "agent--pa",
        "label": "Organization-heavy"
    },
    "execution": {
        "triggers": ["text-generation", "notion-integration", "document-generation",
                     "technical-writing", "memory-store-retrieve", "session-archiving"],
        "primary": "agent--pa",
        "secondary": None,
        "label": "Execution-heavy"
    },
    "design": {
        "triggers": ["design-creation", "image-generation", "media-generation",
                     "slide-generation"],
        "primary": "agent--architect",
        "secondary": "agent--developer",
        "label": "Design-heavy"
    }
}

# ─── Profile Detection ─────────────────────────────────────────────────────────
def detect_profiles(required_capabilities):
    """Detect which agent profiles are triggered by the required capabilities."""
    scores = {p: 0 for p in AGENT_PROFILES}
    for cap_slug in required_capabilities:
        for profile_name, profile in AGENT_PROFILES.items():
            if cap_slug in profile["triggers"]:
                scores[profile_name] += 1
    # Return profiles sorted by score (highest first), filter out 0
    return [(p, scores[p]) for p in sorted(scores, key=lambda x: -scores[x]) if scores[p] > 0]

# ─── Agent Selection ──────────────────────────────────────────────────────────
def select_agents(mission_pack, profiles):
    """Select agents based on profiles and complexity."""
    complexity = mission_pack.get("complexity", "Medium")
    recommended = mission_pack.get("recommended_agents", [])

    agents = []
    seen = set()

    # Always include COO for Advanced
    if complexity == "Advanced":
        agents.append("agent--coo")
        seen.add("agent--coo")

    # Add agents from detected profiles
    for profile_name, score in profiles[:3]:  # Top 3 profiles
        profile = AGENT_PROFILES[profile_name]
        primary = profile["primary"]
        secondary = profile["secondary"]
        if primary and primary not in seen:
            agents.append(primary)
            seen.add(primary)
        if secondary and secondary not in seen and complexity in ("Medium", "Advanced"):
            agents.append(secondary)
            seen.add(secondary)

    # Add recommended agents from Y-ORC if not already included
    for agent in recommended:
        if agent not in seen:
            agents.append(agent)
            seen.add(agent)

    # Fallback
    if not agents:
        agents = ["agent--pa"]

    return agents

# ─── Execution Sequence Generator ─────────────────────────────────────────────
def generate_sequence(mission_pack, agents, profiles):
    """Generate step-by-step execution sequence."""
    complexity = mission_pack.get("complexity", "Medium")
    objective = mission_pack.get("objective", "")
    caps = mission_pack.get("required_capabilities", [])
    sequence = []
    step = 1

    if complexity == "Simple":
        # Single agent, direct execution
        agent = agents[0] if agents else "agent--pa"
        sequence.append({
            "step": step,
            "agent": agent,
            "action": f"Execute: {objective}",
            "dependencies": [],
            "capabilities": caps[:3]
        })

    elif complexity == "Medium":
        # Sequential: first agent prepares, second executes, PA validates
        if len(agents) >= 2:
            sequence.append({
                "step": 1,
                "agent": agents[0],
                "action": f"Prepare and plan: {objective[:80]}",
                "dependencies": [],
                "capabilities": caps[:2]
            })
            sequence.append({
                "step": 2,
                "agent": agents[1] if len(agents) > 1 else agents[0],
                "action": f"Execute primary work: {objective[:80]}",
                "dependencies": [1],
                "capabilities": caps[2:5]
            })
            sequence.append({
                "step": 3,
                "agent": "agent--pa",
                "action": "Validate output and finalize deliverables",
                "dependencies": [2],
                "capabilities": ["text-generation"]
            })
        else:
            sequence.append({
                "step": 1,
                "agent": agents[0],
                "action": f"Execute: {objective}",
                "dependencies": [],
                "capabilities": caps
            })

    else:  # Advanced
        # Multi-agent: COO → Strategist/Architect → Developer → PA → Review
        sequence.append({
            "step": 1,
            "agent": "agent--coo",
            "action": "Decompose mission and assign sub-tasks to agents",
            "dependencies": [],
            "capabilities": ["mission-pack-generation", "agent-routing"]
        })
        if "agent--architect" in agents:
            sequence.append({
                "step": 2,
                "agent": "agent--architect",
                "action": f"Design architecture and specifications for: {objective[:60]}",
                "dependencies": [1],
                "capabilities": [c for c in caps if c in ["design-creation", "code-execution",
                                                           "api-integration", "context-assembly"]][:3]
            })
        if "agent--developer" in agents:
            sequence.append({
                "step": 3,
                "agent": "agent--developer",
                "action": "Implement according to architecture specifications",
                "dependencies": [2] if "agent--architect" in agents else [1],
                "capabilities": [c for c in caps if c in ["code-execution", "web-development",
                                                           "deployment-automation", "testing-validation"]][:3]
            })
        if "agent--researcher" in agents:
            sequence.append({
                "step": 2 if "agent--architect" not in agents else len(sequence) + 1,
                "agent": "agent--researcher",
                "action": "Research and gather required information",
                "dependencies": [1],
                "capabilities": [c for c in caps if c in ["web-search", "data-analysis",
                                                           "semantic-search"]][:3]
            })
        # Final review step
        sequence.append({
            "step": len(sequence) + 1,
            "agent": "agent--coo",
            "action": "Review all deliverables against success criteria and validate",
            "dependencies": [s["step"] for s in sequence[1:]],
            "capabilities": ["mission-pack-generation"]
        })

    return sequence

# ─── Delegation Plan ──────────────────────────────────────────────────────────
def generate_delegation_plan(complexity, agents, profiles):
    """Generate human-readable delegation plan."""
    if not profiles:
        return f"Direct delegation to {agents[0] if agents else 'agent--pa'}."

    top_profile = profiles[0][0] if profiles else "execution"
    label = AGENT_PROFILES[top_profile]["label"]

    if complexity == "Simple":
        return (f"Mission classified as {label}. "
                f"Direct delegation to {agents[0] if agents else 'agent--pa'}. "
                "No intermediate review required.")
    elif complexity == "Medium":
        agent_list = " → ".join(agents[:3])
        return (f"Mission classified as {label}. "
                f"Sequential delegation: {agent_list}. "
                "PA validates final output before delivery.")
    else:
        return (f"Mission classified as Advanced ({label}). "
                f"COO coordinates {len(agents)} agents in structured sequence. "
                "Architect validates design before Developer builds. "
                "COO reviews all deliverables before final delivery.")

# ─── Review Requirements ──────────────────────────────────────────────────────
def generate_review_requirements(complexity, mission_pack):
    reviews = []
    if complexity in ("Medium", "Advanced"):
        reviews.append("All deliverables must match success criteria defined in Mission Pack")
    if complexity == "Advanced":
        reviews.append("Architecture review by Architect Agent before implementation")
        reviews.append("COO final validation before delivery to user")
    reviews.append("No Architecture Freeze v1 violations (9 core modules, no new modules)")
    return reviews

# ─── Escalation Conditions ────────────────────────────────────────────────────
def generate_escalation_conditions(mission_pack):
    caps = mission_pack.get("required_capabilities", [])
    conditions = [
        "Capability not found in Y-REG → Escalate to agent--strategist (Y-CAP gap analysis)",
        "Agent fails step 3 times → Escalate to COO for workflow redesign",
        "Module bypass attempt detected → Escalate to Human (Architecture Freeze violation)",
    ]
    if len(caps) > 6:
        conditions.append("Capability overload (>6 caps) → COO decomposes into sub-missions")
    return conditions

# ─── Main: Generate Execution Plan ────────────────────────────────────────────
def generate_execution_plan(mission_pack, verbose=True):
    """
    Core COO function.
    Input: Mission Pack (dict from Y-ORC)
    Output: Execution Plan (dict)
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"  Y-COO v1.0 — Execution Plan Generator")
        print(f"{'='*60}")
        print(f"  Mission: {mission_pack.get('objective', '?')}")
        print(f"  Complexity: {mission_pack.get('complexity', '?')}")
        print(f"  Capabilities: {mission_pack.get('required_capabilities', [])}")

    caps = mission_pack.get("required_capabilities", [])
    profiles = detect_profiles(caps)

    if verbose:
        print(f"  Profiles detected: {[f'{p}({s})' for p, s in profiles[:3]]}")

    agents = select_agents(mission_pack, profiles)
    sequence = generate_sequence(mission_pack, agents, profiles)
    delegation = generate_delegation_plan(mission_pack.get("complexity", "Medium"), agents, profiles)
    reviews = generate_review_requirements(mission_pack.get("complexity", "Medium"), mission_pack)
    escalations = generate_escalation_conditions(mission_pack)

    execution_plan = {
        "execution_id": str(uuid.uuid4()),
        "generated_at": datetime.now().isoformat() + "Z",
        "mission_id": mission_pack.get("mission_id", ""),
        "objective": mission_pack.get("objective", ""),
        "complexity": mission_pack.get("complexity", "Medium"),
        "selected_agents": agents,
        "selected_workflow": mission_pack.get("recommended_workflow"),
        "selected_capabilities": caps,
        "execution_sequence": sequence,
        "delegation_plan": delegation,
        "review_requirements": reviews,
        "escalation_conditions": escalations,
        "expected_deliverables": mission_pack.get("success_criteria", []),
        "source": "Y-COO v1.0",
        "mission_pack_source": mission_pack.get("source", "Y-ORC")
    }

    return execution_plan

# ─── Print Execution Plan ─────────────────────────────────────────────────────
def print_execution_plan(ep):
    print(f"\n{'='*60}")
    print(f"  EXECUTION PLAN — {ep['execution_id'][:8]}...")
    print(f"{'='*60}")
    print(f"  Objective:    {ep['objective']}")
    print(f"  Complexity:   {ep['complexity']}")
    print(f"  Agents:       {', '.join(ep['selected_agents'])}")
    print(f"  Workflow:     {ep['selected_workflow'] or 'None (custom)'}")
    print(f"  Capabilities: {', '.join(ep['selected_capabilities'][:5])}{'...' if len(ep['selected_capabilities'])>5 else ''}")
    print(f"\n  Execution Sequence:")
    for step in ep['execution_sequence']:
        deps = f" [after {step['dependencies']}]" if step['dependencies'] else ""
        print(f"    Step {step['step']}: [{step['agent']}] {step['action'][:70]}{deps}")
    print(f"\n  Delegation: {ep['delegation_plan']}")
    print(f"\n  Review Requirements:")
    for r in ep['review_requirements']:
        print(f"    ✓ {r}")
    print(f"\n  Escalation Conditions:")
    for e in ep['escalation_conditions']:
        print(f"    ⚠ {e}")
    print(f"\n  Source: {ep['source']}")
    print(f"{'='*60}\n")

# ─── CLI ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Accept mission text or mission pack JSON file
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        with open(sys.argv[1]) as f:
            mission_pack = json.load(f)
        print(f"  Loaded Mission Pack: {sys.argv[1]}")
    else:
        # Generate mission pack via Y-ORC first
        mission_text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Build a new capability for Y-OS"
        print(f"  Generating Mission Pack via Y-ORC for: '{mission_text}'...")

        # Import and call Y-ORC
        sys.path.insert(0, os.path.dirname(__file__))
        from yorc import generate_mission_pack
        context = {"summary": "Y-OS project. Architecture Freeze v1 active. Layer 1+2 complete."}
        constraints = ["Architecture Freeze v1 active — no new core modules",
                       "Agents use modules — modules do not replace agents"]
        mission_pack = generate_mission_pack(mission_text, context_pack=context,
                                             constraints=constraints, verbose=True)

    # Generate Execution Plan
    ep = generate_execution_plan(mission_pack)
    print_execution_plan(ep)

    # Save
    out_file = f"/home/ubuntu/yreg/execution_plan_{ep['execution_id'][:8]}.json"
    with open(out_file, "w") as f:
        json.dump(ep, f, indent=2)
    print(f"  Saved: {out_file}")
