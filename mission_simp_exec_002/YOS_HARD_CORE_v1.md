# Y-OS Hard Core v1

> **If this disappears, Y-OS stops being Y-OS.**

---

## Decision

**7 core modules. 5 domains. Maximum 10 — achieved at 7.**

---

## The 7 Hard Core Modules

### 1. `context_compiler_v2` — CONTEXT
| Field | Value |
|---|---|
| Purpose | Assemble the right context for each worker from memory artifacts |
| Why indispensable | Without it, workers receive raw history or nothing — Y-OS loses its core value proposition |
| Input | Session state, artifact registry, worker identity, mode |
| Output | Typed Context Pack |
| Domain | context/ |
| Rebuild priority | **DAY 1** |

---

### 2. `ccr_runtime_v2` — CONTEXT
| Field | Value |
|---|---|
| Purpose | Route each request to the correct mode (B/D/E) and provider |
| Why indispensable | Without routing, context packs cannot be dispatched — execution is blind |
| Input | Worker profile, task type, session state |
| Output | Mode selection, provider selection |
| Domain | context/ |
| Rebuild priority | **DAY 1** |

---

### 3. `live_worker_executor_v1` — EXECUTION
| Field | Value |
|---|---|
| Purpose | Execute real LLM calls with context packs, capture outputs as artifacts |
| Why indispensable | The actual cognitive work happens here — everything else supports this |
| Input | Context Pack, provider payload |
| Output | Raw LLM response, artifact candidate |
| Domain | execution/ |
| Rebuild priority | **DAY 1** |

---

### 4. `artifact_registry_v2` — MEMORY
| Field | Value |
|---|---|
| Purpose | Store, version, and retrieve all Y-OS outputs as typed artifacts |
| Why indispensable | Without persistent artifact storage, Y-OS has no memory across sessions |
| Input | Raw output, metadata, lineage |
| Output | Registered artifact with ID, type, version |
| Domain | memory/ |
| Rebuild priority | **DAY 2** |

---

### 5. `session_delta_engine_v1` — CAPTURE
| Field | Value |
|---|---|
| Purpose | Extract structured delta from each session (decisions, artifacts, state changes) |
| Why indispensable | Without session capture, memory is never updated — Y-OS cannot learn from its own history |
| Input | Raw session content |
| Output | Session delta (7 structured fields) |
| Domain | capture/ |
| Rebuild priority | **DAY 2** |

---

### 6. `output_validator_v1` — EXECUTION
| Field | Value |
|---|---|
| Purpose | Validate every LLM output before it becomes a registered artifact |
| Why indispensable | Without validation, artifacts may be empty, malformed, or hallucinated — registry integrity collapses |
| Input | Raw LLM output, expected schema |
| Output | VALID / INVALID verdict, structured artifact |
| Domain | execution/ |
| Rebuild priority | **DAY 2** |

---

### 7. `lakshmi_context_review_v1` — EXECUTION
| Field | Value |
|---|---|
| Purpose | Governance hook — review every context pack before dispatch and every artifact before registration |
| Why indispensable | Without governance, Y-OS can inject raw history, expose secrets, or violate the Constitution |
| Input | Context Pack or Artifact |
| Output | APPROVE / REJECT / WARN with risk score |
| Domain | execution/ |
| Rebuild priority | **DAY 3** |

---

## What Is NOT Core

| Module | Why excluded |
|---|---|
| `provider_router_v2` | Useful but a simple dict lookup can substitute on day 1 |
| `cost_tracker_v1` | Important but not existential |
| `kgc_v4_connectivity_engine` | Graph enrichment — valuable, not daily-critical |
| `system_health_monitor_v1` | Observability — optional layer |
| `strategic_recommendation_engine_v1` | Intelligence plugin — not core |
| All event bus modules (5) | Infrastructure convenience, not core |
| All review/ intelligence modules | Optional intelligence layer |

---

## Summary

```
CORE = 7 modules
DOMAINS = 5
DAILY OPERATION = fully supported
CONSTITUTION COMPLIANCE = preserved (Lakshmi in core)
REBUILD TIME = 3 days
```
