# Routing Rules

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Rule Hierarchy

1. **Trust gate** — if task requires T4+, only T4/T5 agents may be selected
2. **Capability match** — agent must have all required capabilities at `proven` or `candidate` status
3. **ART lookup** — consult Agent Routing Table for preferred agent
4. **CRT lookup** — consult Cognitive Routing Table for model selection
5. **Availability** — if preferred agent unavailable, use fallback chain
6. **Human escalation** — if no agent meets criteria, escalate to human operator (T5)

---

## Routing Invariants

- No agent may be selected for a task requiring capabilities it has declared `unsupported`
- No agent below T3 may execute code or write to Git
- No agent below T4 may approve canonical gates
- No agent below T5 may access secrets or deploy automation

---

## Fallback Chain (Default)

```
chatgpt-ag (T5) → yannick-jolliet (T5) → manus (T3) → claude (T2) → gemini (T1)
```

For execution tasks:
```
manus (T3) → [no fallback — human escalation required]
```
