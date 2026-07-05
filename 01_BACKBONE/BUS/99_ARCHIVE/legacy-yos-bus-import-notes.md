# Legacy yos-bus Import Notes

**Import date:** 2026-07-05
**Import gate:** MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE
**Executed by:** Manus / A&G

---

## Source Repository

| Field | Value |
|---|---|
| Repository | `yj000018/yos-bus` |
| Visibility | private |
| Old HEAD | `245818d` |
| Last commit | 2026-06-30 |
| Status | **legacy/dormant** — do not delete remote |

---

## Concepts Integrated

The following concepts from `yos-bus` were integrated into `YOS/01_BACKBONE/BUS/`:

- **inbox → workspace → outbox → archive** lifecycle model
- **Domain-based routing** (general, yac, lakshmi, fcs, casatao)
- **Schemas** — task, artifact, decision, reflex (migrated to JSON from YAML)
- **Cognitive commit convention** (preserved in `00_PROTOCOLS/bus-cognitive-commit-convention.md`)
- **GitHub Actions / reflex architecture** (preserved in `00_PROTOCOLS/bus-reflex-architecture.md`)
- **Agent handoff rules** (preserved in `00_PROTOCOLS/bus-agent-handoff-protocol.md`)
- **BUS as shared operational memory and inter-agent bus** (doctrine preserved)
- **Foundational principle: GitHub-native cognitive backbone** (preserved in protocols)

---

## Updated Doctrine

The old `yos-bus` doctrine was correct as a GitHub-native cognitive backbone. It has been updated:

```
GitHub-native BUS remains valid as durable/auditable backend.
Direct file runtime is now required for fast non-versioned transport.
BUS is no longer GitHub-only.
```

---

## Domain Mapping

| Old Domain | New Domain | Notes |
|---|---|---|
| `general` | `general` | Direct mapping |
| `casatao` | `casatao` | Direct mapping |
| `yac` | `yworld` | Mapped to yworld domain (yac = legacy alias) |
| `lakshmi` | TBD | Recorded as legacy domain alias — decide later |
| `fcs` | archive/legacy | No current canonical domain — legacy alias |

No actual old task content was migrated (old repo had no live tasks at HEAD).

---

## Old Repo Structure (Reference)

```
yos-bus/
├── README.md
├── bus_manifest.yaml
├── agents/
├── docs/
│   ├── foundational-principles/
│   │   └── FP-001-github-native-cognitive-backbone.md
│   └── repository-specification.md
├── protocols/
│   ├── commit-cognitive-convention.md
│   ├── github-actions-reflex-architecture.md
│   └── yos-github-protocol-v0.1.md
├── schemas/
│   ├── artifact_schema.yaml
│   ├── decision_schema.yaml
│   ├── reflex_schema.yaml
│   └── task_schema.yaml
├── inbox/{general,yac,lakshmi,fcs,casatao}/
├── workspace/{general,yac,lakshmi,fcs,casatao}/
├── outbox/general/
└── archive/{general,yac,lakshmi,fcs,casatao}/
```

---

## Boundaries

- The `yj000018/yos-bus` remote repository was **not deleted**.
- No actual task content was migrated (none existed at HEAD).
- Schemas were converted from YAML to JSON for consistency with YOS JSON-first policy.
- The old repo is preserved as a historical reference.
