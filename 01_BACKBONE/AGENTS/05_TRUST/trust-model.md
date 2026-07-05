# Trust Model

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Trust Principle

```
No agent receives corpus mutation, secret access, or automation deployment permission by default.
All permissions must be explicitly granted.
All trust levels must be explicitly declared.
Trust is not inherited from vendor or runtime.
```

---

## Trust Level Summary

| Level | Name | Key Permission | Assigned |
|---|---|---|---|
| T0 | untrusted | none | unknown agents |
| T1 | read_only | read | gemini, codex |
| T2 | sandboxed_write | write_runtime | claude |
| T3 | runtime_operator | write_git + execute_code | manus |
| T4 | canonical_writer | modify_corpus | (none yet) |
| T5 | guardian_approved | all | chatgpt-ag, yannick-jolliet |

---

## Trust Elevation

Trust level may be elevated only by:
1. A dedicated MPM marathon gate with `guardian_required: true`
2. Explicit approval by a T5 agent (guardian_approved)

Trust level may NOT be elevated by:
- Sprint or run gates
- Implicit session behavior
- Vendor claims

---

## Trust and YARP

YARP messages include `sender_trust_level` in the envelope.
Receivers MUST validate sender trust level before processing.
Messages from agents below required trust level MUST be rejected with `NACK`.
