#!/usr/bin/env python3
import json, subprocess, re

payload = {
    "parent": {"page_id": "37635e21-8cf8-8173-a3b2-f083d321382c"},
    "pages": [{
        "properties": {"title": "Y-ORC — Specification v1"},
        "content": (
            "# Y-ORC Specification v1\n\n"
            "Status: MVP | Layer: 2 — Orchestration | Date: 2026-06-12\n\n"
            "## Principle\n\n"
            "Y-ORC transforms Mission + Context Pack + Capabilities Graph into a Mission Pack.\n"
            "Y-ORC does NOT execute work. Y-ORC does NOT replace agents.\n\n"
            "## Y-OS Architecture Layers\n\n"
            "Layer 1 — Foundation: Y-REG, Y-MEM, Y-CTX, Y-ID, Y-LOG\n"
            "Layer 2 — Orchestration: Y-ORC (transforms Mission into Mission Pack)\n"
            "Layer 3 — Organization: COO, Architect, Developer, Strategist, HR, PA\n"
            "Layer 4 — Execution: Workflows, Skills, Automations, Tools\n\n"
            "## Mission Pack Schema\n\n"
            "mission_id, objective, complexity (Simple/Medium/Advanced),\n"
            "recommended_workflow, recommended_agents, required_capabilities,\n"
            "constraints, success_criteria, validation_rules\n\n"
            "## Complexity Rules\n\n"
            "Simple: 1 cap, clear I/O — direct to Skill/Automation\n"
            "Medium: 2-4 caps, linear — Workflow + PA/Specialist\n"
            "Advanced: 5+ caps, branching — COO Agent for decomposition\n\n"
            "## Test Results\n\n"
            "Mission: Develop REG\n"
            "Result: complexity=Medium, caps=[code-execution, web-development, github-integration, api-integration]\n\n"
            "Mission: Design full Y-OS orchestration architecture with multi-agent coordination\n"
            "Result: complexity=Advanced, caps=[context-assembly, memory-store-retrieve, design-creation, code-execution, session-archiving]\n\n"
            "## Y-OS Laws Applied\n\n"
            "Law 3: Agents use modules. Modules do not replace agents.\n"
            "Architecture Freeze v1: 9 core modules. No new modules without formal challenge.\n\n"
            "## Implementation\n\n"
            "File: /home/ubuntu/yreg/yorc.py\n"
            "Git commit: feat: Y-ORC MVP v1.0\n"
            "Supabase: reads yreg_objects (capabilities, agents, workflows)\n"
            "Fallback: Git/Markdown capability_map.json\n"
        )
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
    print(f"Output: {out[-300:]}")
