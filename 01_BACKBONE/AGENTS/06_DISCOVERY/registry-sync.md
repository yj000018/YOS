# Registry Sync

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Registry Sync Principle

```
Git is the source of truth for all AGENTS registries.
Registry changes require a dedicated MPM gate with guardian_required: true.
No agent may self-register or self-elevate trust level.
```

---

## Sync Policy

| Registry | Update Frequency | Gate Required |
|---|---|---|
| agents.json | On new agent registration | marathon (guardian_required) |
| capabilities.json | On capability validation | sprint or run |
| transports.json | On transport validation | sprint or run |
| trust-levels.json | On trust level change | marathon (guardian_required) |

---

## Sync Invariants

- JSON is source of truth
- Markdown views are generated from JSON
- No manual edits to registries without a corresponding MP gate
- Registry version must be incremented on every update

---

## Future: Automated Sync

Phase 2 goal: automated registry sync via `bus.py` and YARP `CAPABILITY_RESPONSE` messages.
