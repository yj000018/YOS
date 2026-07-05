# Model Selection

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Model Selection Criteria

| Criterion | Weight | Notes |
|---|---|---|
| Capability match | Critical | Must have required capabilities |
| Trust level | Critical | Must meet minimum trust requirement |
| Context window | High | Must accommodate task context size |
| Proven status | High | Prefer proven over candidate |
| Cost efficiency | Medium | Prefer lower cost when quality equivalent |
| Latency | Low | Prefer lower latency for interactive tasks |

---

## Model Selection Matrix

| Scenario | Model | Reason |
|---|---|---|
| MP execution (code + FS) | manus | Only proven executor with FS access |
| Architectural design | chatgpt-ag | T5 + proven reasoning + planning |
| A&G review | chatgpt-ag | T5 + guardian role |
| Long-document (>200K tokens) | gemini | 2M context window |
| Code review (no execution) | claude | Strong code review + 200K context |
| Vision + reasoning | chatgpt-ag | GPT-4V proven in yOS |
| Knowledge synthesis | manus | Proven memory + execution |

---

## Model Selection and YARP

Model selection is encoded in YARP `EXECUTE_MP.target_agent`.
If not specified, the routing engine applies this matrix at runtime.
