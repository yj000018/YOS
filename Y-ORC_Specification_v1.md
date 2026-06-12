# Y-ORC Specification v1

**Generated:** 2026-06-12
**Status:** MVP

## 1. Objective

Create the first operational orchestration engine of Y-OS.
Y-ORC transforms a raw mission and its context into a structured **Mission Pack**.
Y-ORC does NOT execute work. Y-ORC does NOT replace agents. Y-ORC does NOT perform reasoning for agents.

## 2. Architecture Layers

Y-OS is structured in 4 layers:

| Layer | Name | Components | Role |
|---|---|---|---|
| **Layer 1** | Foundation | Y-REG, Y-MEM, Y-CTX, Y-ID, Y-LOG | Data, state, and context |
| **Layer 2** | Orchestration | **Y-ORC** | Transforms Mission → Mission Pack |
| **Layer 3** | Organization | COO, Architect, Developer, Strategist, HR, PA | Agents / Roles (Decision & Strategy) |
| **Layer 4** | Execution | Workflows, Skills, Automations, Tools | Execution and action |

## 3. Data Model

### Inputs
- **Mission**: Raw text description of the objective.
- **Context Pack**: Data from Y-CTX (relevant memory, project state, constraints).
- **Capabilities Graph**: Data from Y-REG (available skills, agents, workflows).

### Outputs
- **Mission Pack**: A structured JSON object defining the execution plan.

## 4. Mission Pack Schema

```json
{
  "mission_id": "string (UUID)",
  "objective": "string",
  "complexity": "enum (Simple | Medium | Advanced)",
  "recommended_workflow": "string (workflow_slug | null)",
  "recommended_agents": ["string (agent_slug)"],
  "required_capabilities": ["string (capability_slug)"],
  "constraints": ["string"],
  "success_criteria": ["string"],
  "validation_rules": ["string"]
}
```

## 5. Complexity Classification Rules

Y-ORC classifies mission complexity to determine routing:

| Complexity | Criteria | Routing Impact |
|---|---|---|
| **Simple** | Single capability required. Clear input/output. No state mutation outside of isolated files. | Direct to Skill / Automation. No agent required. |
| **Medium** | 2-4 capabilities required. Multi-step but linear. Minor state mutation (e.g., Notion update). | Direct to Workflow. PA or Specialist Agent monitoring. |
| **Advanced** | 5+ capabilities or unknown capabilities. Branching logic. Strategic decisions required. Heavy state mutation. | Route to COO Agent for decomposition. |

## 6. Recommended Workflow Selection Logic

1. Extract `required_capabilities` from the Mission.
2. Query Y-REG for workflows that expose or aggregate these capabilities.
3. If a single workflow covers >80% of required capabilities, recommend it.
4. If multiple workflows match, recommend the one with the highest historical success rate (via Y-LOG, future).
5. If no workflow matches, return `null` (Agent must build a custom plan).

## 7. Recommended Agent Selection Logic

1. Analyze `required_capabilities` and `complexity`.
2. Query Y-REG for Agents that own or aggregate the required capabilities.
3. **If Complexity == Advanced**: Always recommend `agent--coo` (or equivalent) as primary.
4. **If Complexity == Medium**: Recommend the Specialist Agent owning the primary capability.
5. **If Complexity == Simple**: Recommend `agent--pa` or direct tool execution.

## 8. Implementation Plan

1. Build `yorc.py` (Python CLI).
2. Implement Y-REG integration (fetch capabilities, agents, workflows).
3. Implement LLM-based Context Analysis (extract required capabilities from Mission).
4. Implement rule-based Classification & Selection (Complexity, Workflow, Agent).
5. Generate Mission Pack JSON.
