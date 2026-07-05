# CRT — Cognitive Routing Table

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Definition

The Cognitive Routing Table (CRT) is the canonical lookup table for routing cognitive tasks to LLMs based on task type, context window requirements, cost, and quality requirements.

**CRT is a submodule of AGENTS/04_ROUTING.** It is not a standalone module.

---

## CRT Schema

```json
{
  "cognitive_task_type": "string",
  "preferred_model": "agent_id",
  "fallback_model": "agent_id",
  "context_window_required": "number",
  "cost_tier": "low | medium | high",
  "quality_requirement": "standard | high | critical",
  "routing_notes": "string"
}
```

---

## Current CRT (v1.0.0)

| Cognitive Task | Preferred | Fallback | Context | Cost | Quality |
|---|---|---|---|---|---|
| MP authoring / architecture | chatgpt-ag | claude | 128K | high | critical |
| Code generation + execution | manus | codex | 128K | medium | high |
| Long-document analysis | gemini | claude | 2M | medium | high |
| Code review | claude | chatgpt-ag | 200K | medium | high |
| Image/screenshot analysis | chatgpt-ag | gemini | 128K | medium | standard |
| Knowledge synthesis | manus | claude | 128K | medium | high |
| A&G review | chatgpt-ag | yannick-jolliet | 128K | high | critical |

---

## CRT and ART Relationship

- ART routes by agent identity and trust level
- CRT routes by cognitive task type and model characteristics
- Both are consulted for complex routing decisions
- ART takes precedence for trust-gated operations
