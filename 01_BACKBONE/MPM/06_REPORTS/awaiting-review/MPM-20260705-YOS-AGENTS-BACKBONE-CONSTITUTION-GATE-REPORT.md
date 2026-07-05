# MPR — MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## STATUS BLOCK

```
MP_ID:                           MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE
MODE:                            marathon
STATUS:                          executed_awaiting_a_g_review
COMMIT:                          0385844
BRANCH:                          main
EXECUTED_AT:                     2026-07-05T19:00:00Z
EXECUTOR:                        Manus
GUARDIAN_REQUIRED:               true
```

---

## Deliverables

### New Module: `01_BACKBONE/AGENTS/` — 35 files

| Folder | Files | Description |
|---|---|---|
| `00_SPEC/` | 4 | CONSTITUTION, LIFECYCLE, ROLES, CAPABILITY-MODEL |
| `01_REGISTRY/` | 4 | agents.json, capabilities.json, transports.json, trust-levels.json |
| `02_IDENTITIES/` | 6 | chatgpt.md, manus.md, claude.md, gemini.md, codex.md, template |
| `03_CAPABILITIES/` | 8 | reasoning, coding, vision, filesystem, api, memory, planning, execution |
| `04_ROUTING/` | 5 | ART/README, CRT/README, routing-rules, capability-selection, model-selection |
| `05_TRUST/` | 4 | trust-model, permissions, authentication, execution-boundaries |
| `06_DISCOVERY/` | 3 | discovery-protocol, capability-query, registry-sync |
| Root | 1 | README.md |

### Patched Files

| File | Change |
|---|---|
| `YARP/00_SPEC/YARP-SPEC-v1.md` | §7 renamed + §8 AGENTS integration added |

---

## Core Doctrine (AGENT-CONSTITUTION.md v1.0.0)

```
Agents have identities.
Agents expose capabilities.
Capabilities are declarative.
Trust is explicit.
Permissions are bounded.
Routing is capability-based.
Discovery is protocolized.
No agent is globally privileged by default.
Human operators are also agents.
```

---

## Agent Registry (v1.0.0)

| Agent | Type | Trust | Primary Roles |
|---|---|---|---|
| chatgpt-ag | llm | T5 | architect, guardian |
| manus | llm+executor | T3 | executor, orchestrator |
| claude | llm | T2 | architect, reviewer |
| gemini | llm | T1 | reviewer, assimilator |
| codex | llm+executor | T1 | executor |
| yannick-jolliet | human | T5 | operator, guardian |

---

## Capability Matrix (proven status)

| Capability | chatgpt-ag | manus | claude | gemini | codex |
|---|---|---|---|---|---|
| reasoning | proven | proven | proven | proven | candidate |
| planning | proven | proven | proven | candidate | candidate |
| coding | proven | proven | proven | candidate | proven |
| vision | proven | proven | candidate | proven | unknown |
| filesystem | unsupported | **proven** | unsupported | unsupported | candidate |
| api | candidate | **proven** | unknown | unknown | candidate |
| memory | candidate | **proven** | unknown | unknown | unknown |
| execution | unsupported | **proven** | unsupported | unsupported | candidate |

---

## Validation

```
AGENTS_FILES:                    35/35 created
JSON_SCHEMAS_VALID:              12/12 PASS
BUS_VALIDATE:                    PASS
MPM_VALIDATE:                    PASS_WITH_WARNINGS (4x stale_running — pre-existing)
YARP_SPEC_PATCHED:               yes (§7 + §8)
READY_QUEUE:                     CLEAN (0 MPs)
```

---

## Backbone Architecture (Updated)

```
                 yOS
                  │
 ┌────────────────┼────────────────┐
 │                │                │
 KAP             MPM             YARP
Knowledge     Orchestration     Communication
Assimilation  & Execution       Between Agents
 │                │                │
 └────────────────┼────────────────┘
                  │
               AGENTS
  Identity · Capabilities · Trust · Routing
                  │
                 BUS
      Runtime / Transport Substrate
```

---

## Next Gates

1. `MPM-{DATE}-YOS-YARP-PHASE2-VALIDATION-GATE` — live test ChatGPT → task.sendMessage → BUS → MPM → RESULT JSON
2. `MPM-{DATE}-YOS-AGENTS-TRUST-ELEVATION-GATE` — elevate Claude to T3 after validation
3. `MPM-{DATE}-YOS-AGENTS-CANONICAL-DESIGNATION-GATE` — promote AGENTS candidate → canonical
