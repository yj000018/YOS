# Execution Boundaries

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Execution Boundary Principle

```
No agent may execute operations beyond its declared trust level and capability scope.
Execution boundaries are enforced at the routing layer, not the agent layer.
```

---

## Manus Execution Boundaries

| Operation | Allowed | Notes |
|---|---|---|
| Write to /home/ubuntu/ | ✅ | Persistent runtime |
| Write to /tmp/ | ✅ | Ephemeral |
| Execute Python/Node/bash | ✅ | Sandbox |
| Git commit + push | ✅ | GitHub PAT |
| Read Manus Secrets | ✅ | Via environment variables |
| Access 1Password | ❌ | Requires explicit instruction |
| Deploy automation (n8n) | ❌ | Requires T5 approval |
| Approve canonical gates | ❌ | Requires T4+ |

---

## ChatGPT (A&G) Execution Boundaries

| Operation | Allowed | Notes |
|---|---|---|
| Create MPs | ✅ | Core role |
| Approve MPRs | ✅ | Guardian role |
| Designate canonical gates | ✅ | T5 |
| Write to yOS filesystem | ❌ | No direct FS access |
| Execute code | ❌ | No direct execution |
| Access secrets | ✅ | Via explicit instruction to Manus |

---

## Boundary Violation Policy

- Boundary violations MUST be logged as YARP ERROR with code `E-TRUST-001`
- Violations MUST NOT be silently ignored
- Repeated violations trigger human escalation
