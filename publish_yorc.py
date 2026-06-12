#!/usr/bin/env python3
"""Publish Y-ORC deliverables to Notion."""
import json, subprocess, os

# Parent: System Architecture page
PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

SPEC_CONTENT = """# Y-ORC Specification v1

**Status:** MVP | **Layer:** 2 — Orchestration | **Generated:** 2026-06-12

## Principle

Y-ORC is the first component that transforms a raw **Question → Mission**.
It sits between Layer 1 (Foundation) and Layer 3 (Agents).

Y-ORC does NOT execute work.
Y-ORC does NOT replace agents.
Y-ORC does NOT perform reasoning for agents.

## Y-OS Architecture Layers

| Layer | Name | Components | Role |
|---|---|---|---|
| Layer 1 | Foundation | Y-REG, Y-MEM, Y-CTX, Y-ID, Y-LOG | Data, state, context |
| **Layer 2** | **Orchestration** | **Y-ORC** | **Transforms Mission → Mission Pack** |
| Layer 3 | Organization | COO, Architect, Developer, Strategist, HR, PA | Decision & Strategy |
| Layer 4 | Execution | Workflows, Skills, Automations, Tools | Action |

## Inputs

- **Mission**: Raw text description of the objective.
- **Context Pack** (Y-CTX): Relevant memory, project state, constraints.
- **Capabilities Graph** (Y-REG): Available skills, agents, workflows.

## Output: Mission Pack

```json
{
  "mission_id": "UUID",
  "objective": "string",
  "complexity": "Simple | Medium | Advanced",
  "recommended_workflow": "workflow_slug | null",
  "recommended_agents": ["agent_slug"],
  "required_capabilities": ["capability_slug"],
  "constraints": ["string"],
  "success_criteria": ["string"],
  "validation_rules": ["string"]
}
```

## Complexity Classification

| Complexity | Criteria | Routing |
|---|---|---|
| Simple | 1 cap, clear I/O, no state mutation | Direct to Skill/Automation |
| Medium | 2-4 caps, linear, minor state mutation | Workflow + PA/Specialist Agent |
| Advanced | 5+ caps, branching, strategic decisions | COO Agent for decomposition |

## Workflow Selection Logic

1. Extract required capabilities from Mission.
2. Query Y-REG for workflows covering these capabilities.
3. If single workflow covers >80% → recommend it.
4. If no match → return null (Agent builds custom plan).

## Agent Selection Logic

| Complexity | Primary Agent | Rationale |
|---|---|---|
| Advanced | COO | Strategic decomposition required |
| Medium | Specialist matching primary capability | Domain expertise |
| Simple | PA or direct execution | Minimal overhead |

## Y-OS Laws Applied

- **Law #3**: Agents use modules. Modules do not replace agents.
- **Architecture Freeze v1**: 9 core modules. No new modules without formal challenge.
"""

def create_page(parent_id, title, content):
    payload = json.dumps({
        "pages": [{
            "parent_id": parent_id,
            "title": title,
            "content": content[:8000]
        }]
    })
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", payload]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = result.stdout + result.stderr
    # Extract page URL
    import re
    m = re.search(r'https://[^\s"]+notion[^\s"]+', out)
    url = m.group() if m else "check Notion"
    print(f"  {'OK' if 'error' not in out.lower() else 'CHECK'}: {title} — {url}")
    return url

print("Publishing Y-ORC deliverables to Notion...")
create_page(PARENT_ID, "⚙️ Y-ORC — Specification v1", SPEC_CONTENT)
print("Done.")
