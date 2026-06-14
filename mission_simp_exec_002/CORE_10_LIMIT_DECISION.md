# Core 10-Module Limit Decision

> **Rule: Maximum 10 active CORE modules. Everything else is optional or archived.**

---

## The 10 Core Modules

| # | Module | Current Status | New Status | Reason |
|---|---|---|---|---|
| 1 | `context_compiler_v2` | context/ | **CORE** | Assembles context — the core value |
| 2 | `ccr_runtime_v2` | context/ | **CORE** | Routes requests — without it, blind dispatch |
| 3 | `provider_payload_builder_v1` | context/ | **CORE** | Formats payloads for LLMs — required for any call |
| 4 | `live_worker_executor_v1` | execution/ | **CORE** | Executes LLM calls — the actual work |
| 5 | `output_validator_v1` | execution/ | **CORE** | Validates outputs — registry integrity |
| 6 | `lakshmi_context_review_v1` | execution/ | **CORE** | Governance — Constitutional compliance |
| 7 | `artifact_registry_v2` | memory/ | **CORE** | Stores artifacts — persistent memory |
| 8 | `session_delta_engine_v1` | capture/ | **CORE** | Captures session state — memory update |
| 9 | `context_cache_v1` | memory/ | **CORE** | Caches context — performance |
| 10 | `provider_registry_v1` | execution/ | **CORE** | Registers providers — configuration |

**Total: 10 modules. Limit: 10. ✅**

---

## Everything Else → Optional or Archive

| Category | Count | Modules |
|---|---|---|
| OPTIONAL INFRASTRUCTURE | 9 | provider_router, failover, health, cost, trace, living_memory, pipeline, chaining, validation_queue |
| OPTIONAL INTELLIGENCE | 10 | strategic_rec, gap_analysis, evidence, proposals, prioritization, roadmap, EIS, org_obs, governance_obs, gemini_validation |
| OPTIONAL EVENTS | 6 | event_bus, registry, router, persistence, replay, lineage |
| OPTIONAL GRAPH | 2 | kgc_v4, lineage_review_registry |
| OPTIONAL LINEAGE | 2 | lineage_validation, event_lineage_tracker |
| ARCHIVE | 1 | evolution_tracker |

---

## Promotion Rules (ADR-SIMP-002)

A module may be promoted from OPTIONAL to CORE only if it passes ALL 4 tests:

1. **Weekly use test** — used at least once per week
2. **Workload reduction test** — demonstrably reduces human effort
3. **7-day rebuild test** — would be rebuilt in first 7 days
4. **One-in / one-out test** — adding it requires removing another
