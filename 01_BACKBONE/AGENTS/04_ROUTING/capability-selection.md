# Capability Selection

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Selection Algorithm

```
1. Parse task requirements → extract required capabilities
2. Filter agents: keep only those with all required capabilities at proven|candidate
3. Apply trust filter: remove agents below required trust level
4. Rank by: proven > candidate, higher trust > lower trust
5. Select top-ranked agent
6. If tie: consult ART preferred_agent
```

---

## Capability Composition Examples

| Task | Required Capabilities | Best Agent |
|---|---|---|
| Execute MP | execution + coding + filesystem + planning | manus |
| Write MP | reasoning + planning | chatgpt-ag |
| Review MPR | reasoning | chatgpt-ag |
| Analyze screenshot | vision + reasoning | chatgpt-ag |
| Long-doc synthesis | reasoning + memory | gemini |
| Code + test | coding + execution | manus |
