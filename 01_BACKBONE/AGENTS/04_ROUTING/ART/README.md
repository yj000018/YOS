# ART — Agent Routing Table

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Definition

The Agent Routing Table (ART) is the canonical lookup table for routing tasks to agents based on capability, trust level, and availability.

**ART is a submodule of AGENTS/04_ROUTING.** It is not a standalone module.

---

## ART Schema

```json
{
  "task_type": "string",
  "required_capabilities": ["capability_id"],
  "required_trust_level": "T0-T5",
  "preferred_agent": "agent_id",
  "fallback_agents": ["agent_id"],
  "routing_policy": "capability_match | trust_match | availability"
}
```

---

## Current ART (v1.0.0)

| Task Type | Required Capabilities | Min Trust | Preferred Agent | Fallback |
|---|---|---|---|---|
| MP execution | execution + coding + filesystem | T3 | manus | none |
| Architectural design | reasoning + planning | T2 | chatgpt-ag | claude |
| A&G review | reasoning + planning | T4 | chatgpt-ag | yannick-jolliet |
| Code review | coding + reasoning | T2 | claude | chatgpt-ag |
| Long-doc analysis | reasoning + vision | T1 | gemini | claude |
| Knowledge assimilation | reasoning + memory | T2 | manus | claude |

---

## ART and YARP

ART routing decisions are encoded in YARP `EXECUTE_MP` messages as `target_agent` field.

If `target_agent` is not specified, the ART is consulted at runtime.
