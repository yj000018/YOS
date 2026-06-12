#!/usr/bin/env python3
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

content = (
    "# COO Agent Specification v1\n\n"
    "Status: MVP | Layer: 3 — Organization | Date: 2026-06-12\n\n"
    "## Role Definition\n\n"
    "Title: Chief Operating Officer\n"
    "Layer: 3 — Organization\n"
    "Mission: Ensure missions are executed efficiently by the right agents using the right modules.\n\n"
    "COO does NOT execute work.\n"
    "COO decides, coordinates, and delegates.\n\n"
    "## Modules Used (Law 3)\n\n"
    "COO uses: Y-ORC, Y-CTX, Y-REG, Y-MEM\n"
    "COO never replaces these modules.\n\n"
    "## Decision Matrix\n\n"
    "Research-heavy (web-search, data-analysis) → agent--researcher + agent--pa\n"
    "Development-heavy (code-execution, web-development) → agent--architect + agent--developer\n"
    "Strategy-heavy (workflow-planning, gap-analysis) → agent--strategist + agent--coo\n"
    "Organization-heavy (namespace-management, object-registration) → agent--hr + agent--pa\n"
    "Execution-heavy (text-generation, notion-integration) → agent--pa\n"
    "Design-heavy (design-creation, image-generation) → agent--architect + agent--developer\n\n"
    "## Execution Plan Schema\n\n"
    "execution_id, mission_id, objective, complexity,\n"
    "selected_agents, selected_workflow, selected_capabilities,\n"
    "execution_sequence (step, agent, action, dependencies),\n"
    "delegation_plan, review_requirements, escalation_conditions, expected_deliverables\n\n"
    "## Delegation Logic\n\n"
    "Simple: Direct delegation to single agent. No intermediate review.\n"
    "Medium: Sequential delegation to 2+ agents. PA validates final output.\n"
    "Advanced: Multi-agent coordination. COO orchestrates. Architect validates before Developer builds.\n\n"
    "## Escalation Rules\n\n"
    "Capability missing in Y-REG → Escalate to agent--strategist (Y-CAP)\n"
    "Agent fails step 3 times → Escalate to COO for workflow redesign\n"
    "Module bypass attempt → Escalate to Human (Architecture Freeze violation)\n"
    "Capability overload (>6 caps) → COO decomposes into sub-missions\n\n"
    "## Test Results\n\n"
    "Mission: Build a new capability for Y-OS\n"
    "ORC: complexity=Medium, caps=[code-execution, web-development]\n"
    "COO: agents=[architect, developer, pa], sequence=3 steps, profile=Development-heavy\n\n"
    "Mission: Design full Y-OS multi-agent coordination system\n"
    "ORC: complexity=Advanced, caps=[context-assembly, memory-store-retrieve, design-creation, code-execution, session-archiving]\n"
    "COO: agents=[coo, pa, architect, developer], sequence=4 steps, profile=Advanced\n\n"
    "## Y-OS Laws Applied\n\n"
    "Law 3: Agents use modules. Modules do not replace agents.\n"
    "Architecture Freeze v1: 9 core modules. No new modules without formal challenge.\n\n"
    "## Implementation\n\n"
    "File: /home/ubuntu/yreg/ycoo.py\n"
    "Git commit: feat: Y-COO MVP v1.0\n"
    "Integrates with: yorc.py (Y-ORC)\n"
)

payload = {
    "parent": {"page_id": PARENT_ID},
    "pages": [{
        "properties": {"title": "COO Agent — Specification v1"},
        "icon": "🎯",
        "content": content
    }]
}

cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
       "--server", "notion", "--input", json.dumps(payload)]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
out = result.stdout + result.stderr
m = re.search(r'"url"\s*:\s*"([^"]+)"', out)
if m:
    print(f"Created: {m.group(1)}")
else:
    print(f"Output: {out[-200:]}")
