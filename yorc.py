#!/usr/bin/env python3
"""
Y-ORC MVP v1.0 — Y-OS Orchestration Engine
Transforms: Mission + Context Pack + Capabilities Graph → Mission Pack
Architecture: Layer 2 (Orchestration) — reads Layer 1, feeds Layer 3.
"""

import json, re, subprocess, uuid, glob, os, sys
from datetime import datetime

PROJECT_ID = "zcgqqzlxzcxkswwlbxhc"

# ─── Supabase Query ────────────────────────────────────────────────────────────
def supabase_query(sql):
    payload = {"project_id": PROJECT_ID, "query": sql}
    cmd = ["manus-mcp-cli", "tool", "call", "execute_sql",
           "--server", "supabase", "--input", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    m = re.search(r'\[\{.*?\}\]', out, re.DOTALL)
    if m:
        try: return json.loads(m.group())
        except: pass
    files = sorted(glob.glob(os.path.expanduser('~/.mcp/tool-results/*execute_sql*')))
    if files:
        with open(files[-1]) as f: content = f.read()
        m = re.search(r'\[\{.*?\}\]', content, re.DOTALL)
        if m:
            try: return json.loads(m.group())
            except: pass
    return []

# ─── Y-REG: Fetch capabilities, agents, workflows ─────────────────────────────
def fetch_registry():
    caps = supabase_query(
        "SELECT slug, name, module_owner, description FROM yreg_objects WHERE type='capability' AND status='active';"
    )
    agents = supabase_query(
        "SELECT slug, name, description FROM yreg_objects WHERE type='agent' AND status='active';"
    )
    workflows = supabase_query(
        "SELECT slug, name, description FROM yreg_objects WHERE type='workflow' AND status='active';"
    )
    skills = supabase_query(
        "SELECT slug, name, description, tags FROM yreg_objects WHERE type='skill' AND status='active';"
    )
    return {
        "capabilities": caps,
        "agents": agents,
        "workflows": workflows,
        "skills": skills,
    }

# ─── Fallback: load from Git/Markdown ─────────────────────────────────────────
def fetch_registry_fallback():
    """Load capabilities from capability_map.json if Supabase unavailable."""
    cap_file = os.path.join(os.path.dirname(__file__), "capability_map.json")
    if os.path.exists(cap_file):
        with open(cap_file) as f:
            cap_map = json.load(f)
        caps = [{"slug": k, "name": v["name"], "module_owner": v["module"], "description": ""}
                for k, v in cap_map["capabilities"].items()]
    else:
        caps = []
    return {"capabilities": caps, "agents": [], "workflows": [], "skills": []}

# ─── Complexity Classification ─────────────────────────────────────────────────
def classify_complexity(mission_text, required_caps):
    """
    Rules:
    - Simple: 1 cap, clear I/O, no state mutation
    - Medium: 2-4 caps, linear, minor state mutation
    - Advanced: 5+ caps, branching, strategic decisions
    """
    n = len(required_caps)
    text_lower = mission_text.lower()

    # Advanced signals
    advanced_signals = [
        "architecture", "design", "strategy", "plan", "system", "build",
        "develop", "create", "implement", "orchestrate", "coordinate",
        "multiple", "complex", "integrate", "migrate", "refactor"
    ]
    medium_signals = [
        "update", "modify", "add", "configure", "setup", "sync",
        "generate", "export", "publish", "analyze"
    ]
    simple_signals = [
        "get", "fetch", "list", "show", "display", "search", "find",
        "check", "verify", "read", "lookup"
    ]

    adv_score = sum(1 for s in advanced_signals if s in text_lower)
    med_score = sum(1 for s in medium_signals if s in text_lower)
    sim_score = sum(1 for s in simple_signals if s in text_lower)

    if n >= 5 or adv_score >= 2:
        return "Advanced"
    elif n >= 2 or med_score >= 1 or adv_score == 1:
        return "Medium"
    else:
        return "Simple"

# ─── Mission Intent Synonyms ──────────────────────────────────────────────────
MISSION_SYNONYMS = {
    "develop": ["code-execution", "web-development", "github-integration", "api-integration",
                "testing-validation", "deployment-automation"],
    "build": ["code-execution", "web-development", "deployment-automation"],
    "create": ["code-execution", "web-development", "text-generation"],
    "design": ["code-execution", "context-assembly", "workflow-planning"],
    "reg": ["registry-lookup", "object-registration", "relation-traversal"],
    "registry": ["registry-lookup", "object-registration", "relation-traversal"],
    "memory": ["memory-store-retrieve", "session-archiving", "cross-session-recall"],
    "search": ["web-search", "registry-lookup", "semantic-search"],
    "analyze": ["data-analysis", "context-assembly", "relevance-scoring"],
    "write": ["text-generation", "technical-writing", "document-generation"],
    "automate": ["workflow-automation", "n8n-workflow-execution", "automation-scheduling"],
    "publish": ["notion-integration", "web-development", "document-generation"],
    "orchestrate": ["mission-pack-generation", "agent-routing", "workflow-planning"],
    "plan": ["workflow-planning", "mission-pack-generation", "context-assembly"],
    "sync": ["memory-synchronization", "workflow-automation", "api-integration"],
    "image": ["image-generation", "media-generation"],
    "video": ["video-generation", "media-generation"],
    "audio": ["audio-generation", "text-to-speech"],
    "slide": ["slide-generation", "document-generation"],
    "scrape": ["web-scraping", "web-search"],
    "deploy": ["deployment-automation", "web-development"],
}

# ─── Capability Extraction from Mission ───────────────────────────────────────
def extract_required_capabilities(mission_text, registry):
    """
    Hybrid matching: keyword overlap + synonym expansion.
    Returns list of capability slugs.
    """
    text_lower = mission_text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))
    stop = {"the", "a", "an", "of", "for", "and", "or", "in", "to", "is", "are", "by", "with", "do", "not"}
    words -= stop

    # Build cap lookup
    cap_by_slug = {c["slug"]: c for c in registry["capabilities"]}

    matched = {}

    # Pass 1: direct keyword overlap
    for cap in registry["capabilities"]:
        cap_words = set(re.findall(r'\b\w+\b', (cap["name"] + " " + cap.get("description", "")).lower()))
        cap_words -= stop
        overlap = words & cap_words
        if len(overlap) >= 1 and len(cap_words) <= 4:
            matched[cap["slug"]] = (cap["name"], len(overlap) + 1)
        elif len(overlap) >= 2:
            matched[cap["slug"]] = (cap["name"], len(overlap))

    # Pass 2: synonym expansion
    for word in words:
        if word in MISSION_SYNONYMS:
            for cap_slug in MISSION_SYNONYMS[word]:
                if cap_slug in cap_by_slug and cap_slug not in matched:
                    matched[cap_slug] = (cap_by_slug[cap_slug]["name"], 1)
                elif cap_slug in cap_by_slug:
                    # Boost existing match
                    existing_name, existing_score = matched[cap_slug]
                    matched[cap_slug] = (existing_name, existing_score + 1)

    # Sort by score, take top 8
    sorted_caps = sorted(matched.items(), key=lambda x: -x[1][1])
    return [{"slug": s, "name": n} for s, (n, _) in sorted_caps[:8]]

# ─── Workflow Selection ────────────────────────────────────────────────────────
def select_workflow(required_caps, registry):
    """Select best matching workflow from Y-REG."""
    if not registry["workflows"]:
        return None
    cap_slugs = {c["slug"] for c in required_caps}
    # Simple heuristic: match workflow name/description against cap names
    best = None
    best_score = 0
    for wf in registry["workflows"]:
        wf_words = set(re.findall(r'\b\w+\b', (wf["name"] + " " + wf.get("description", "")).lower()))
        cap_words = set()
        for c in required_caps:
            cap_words |= set(re.findall(r'\b\w+\b', c["name"].lower()))
        score = len(wf_words & cap_words)
        if score > best_score:
            best_score = score
            best = wf["slug"]
    return best if best_score >= 2 else None

# ─── Agent Selection ──────────────────────────────────────────────────────────
def select_agents(complexity, required_caps, registry):
    """Select recommended agents based on complexity and capabilities."""
    agents_out = []

    if complexity == "Advanced":
        # Always include COO for advanced missions
        coo = next((a for a in registry["agents"] if "coo" in a["slug"].lower()), None)
        if coo:
            agents_out.append(coo["slug"])
        # Add Architect if design/architecture involved
        arch = next((a for a in registry["agents"] if "architect" in a["slug"].lower()), None)
        if arch:
            agents_out.append(arch["slug"])

    elif complexity == "Medium":
        # Match agents to primary capability module
        primary_cap = required_caps[0] if required_caps else None
        if primary_cap:
            # Find agent whose description matches primary cap
            for agent in registry["agents"]:
                if any(w in agent.get("description", "").lower()
                       for w in re.findall(r'\b\w+\b', primary_cap["name"].lower())):
                    agents_out.append(agent["slug"])
                    break
        if not agents_out:
            pa = next((a for a in registry["agents"] if "pa" in a["slug"].lower()), None)
            if pa:
                agents_out.append(pa["slug"])

    else:  # Simple
        pa = next((a for a in registry["agents"] if "pa" in a["slug"].lower()), None)
        if pa:
            agents_out.append(pa["slug"])

    return agents_out if agents_out else ["agent--manus"]

# ─── Success Criteria Generation ──────────────────────────────────────────────
def generate_success_criteria(mission_text, complexity, required_caps):
    criteria = [f"Mission objective achieved: {mission_text[:100]}"]
    if required_caps:
        criteria.append(f"All {len(required_caps)} required capabilities exercised")
    if complexity == "Advanced":
        criteria.append("Deliverables reviewed and validated by COO Agent")
        criteria.append("No architectural violations (Architecture Freeze v1)")
    elif complexity == "Medium":
        criteria.append("Output matches expected format and quality")
    criteria.append("No unresolved blockers or open issues")
    return criteria

# ─── Validation Rules ─────────────────────────────────────────────────────────
def generate_validation_rules(complexity):
    rules = ["Output must be complete and non-empty"]
    if complexity in ("Medium", "Advanced"):
        rules.append("All required capabilities must be addressed")
        rules.append("Constraints must be respected")
    if complexity == "Advanced":
        rules.append("Architecture Freeze v1: no new core modules without formal challenge")
        rules.append("Agents use modules — modules do not replace agents (Law #3)")
        rules.append("COO Agent must validate before execution")
    return rules

# ─── Main: Generate Mission Pack ──────────────────────────────────────────────
def generate_mission_pack(mission_text, context_pack=None, constraints=None, verbose=True):
    """
    Core Y-ORC function.
    Input: mission_text (str), context_pack (dict), constraints (list)
    Output: Mission Pack (dict)
    """
    if verbose:
        print(f"\n{'='*60}")
        print(f"  Y-ORC v1.0 — Mission Pack Generator")
        print(f"{'='*60}")
        print(f"  Mission: {mission_text}")
        print(f"  Loading Y-REG...")

    # Load registry (Supabase with Git fallback)
    registry = fetch_registry()
    if not registry["capabilities"]:
        if verbose: print("  [Fallback] Using Git/Markdown registry...")
        registry = fetch_registry_fallback()

    if verbose:
        print(f"  Registry loaded: {len(registry['capabilities'])} caps, "
              f"{len(registry['agents'])} agents, {len(registry['workflows'])} workflows")

    # Extract required capabilities
    required_caps = extract_required_capabilities(mission_text, registry)
    if verbose:
        print(f"  Required capabilities: {[c['name'] for c in required_caps]}")

    # Classify complexity
    complexity = classify_complexity(mission_text, required_caps)
    if verbose: print(f"  Complexity: {complexity}")

    # Select workflow
    workflow = select_workflow(required_caps, registry)
    if verbose: print(f"  Recommended workflow: {workflow or 'None (custom plan needed)'}")

    # Select agents
    agents = select_agents(complexity, required_caps, registry)
    if verbose: print(f"  Recommended agents: {agents}")

    # Build Mission Pack
    mission_pack = {
        "mission_id": str(uuid.uuid4()),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "objective": mission_text,
        "complexity": complexity,
        "recommended_workflow": workflow,
        "recommended_agents": agents,
        "required_capabilities": [c["slug"] for c in required_caps],
        "required_capabilities_detail": required_caps,
        "constraints": constraints or [],
        "success_criteria": generate_success_criteria(mission_text, complexity, required_caps),
        "validation_rules": generate_validation_rules(complexity),
        "context_pack_summary": context_pack.get("summary", "") if context_pack else "",
        "source": "Y-ORC v1.0",
        "registry_source": "supabase" if registry["capabilities"] and
                           any(c.get("module_owner") for c in registry["capabilities"]) else "git-fallback"
    }

    return mission_pack

# ─── CLI ──────────────────────────────────────────────────────────────────────
def print_mission_pack(mp):
    print(f"\n{'='*60}")
    print(f"  MISSION PACK — {mp['mission_id'][:8]}...")
    print(f"{'='*60}")
    print(f"  Objective:    {mp['objective']}")
    print(f"  Complexity:   {mp['complexity']}")
    print(f"  Workflow:     {mp['recommended_workflow'] or 'None (custom)'}")
    print(f"  Agents:       {', '.join(mp['recommended_agents'])}")
    print(f"  Capabilities: {', '.join(mp['required_capabilities'][:5])}{'...' if len(mp['required_capabilities'])>5 else ''}")
    print(f"\n  Success Criteria:")
    for c in mp['success_criteria']:
        print(f"    ✓ {c}")
    print(f"\n  Validation Rules:")
    for r in mp['validation_rules']:
        print(f"    • {r}")
    print(f"\n  Source: {mp['source']} | Registry: {mp['registry_source']}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Default test case
    mission = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Develop REG"
    context = {"summary": "Y-OS project. Y-REG MVP already built. Architecture Freeze v1 active."}
    constraints = ["Architecture Freeze v1 active — no new core modules",
                   "Agents use modules — modules do not replace agents"]

    mp = generate_mission_pack(mission, context_pack=context, constraints=constraints)
    print_mission_pack(mp)

    # Save to file
    out_file = f"/home/ubuntu/yreg/mission_pack_{mp['mission_id'][:8]}.json"
    with open(out_file, "w") as f:
        json.dump(mp, f, indent=2)
    print(f"  Saved: {out_file}")
