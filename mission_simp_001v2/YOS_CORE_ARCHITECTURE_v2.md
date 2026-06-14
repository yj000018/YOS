---
id: YOS_CORE_ARCHITECTURE_v2
title: Y-OS Core Architecture v2 — Radical Simplification
status: ADOPTED
date: 2026-06-14
supersedes: YOS_SYSTEM_ARCHITECTURE_v1.md
tags: [architecture, core, simplification, v2]
---

# Y-OS Core Architecture v2

> **A Personal Cognitive Operating System. Not a platform. Not a framework. A daily tool.**

---

## The True Center of Gravity

Y-OS exists to answer one question:

> *How do I think better, remember more, and act with less friction — every day?*

Everything else is optional infrastructure.

The center of gravity is the **cognitive loop**:

```
CAPTURE → REMEMBER → COMPILE → EXECUTE → REVIEW
```

This loop is Y-OS. Everything else serves this loop or is overhead.

---

## The 5 Core Modules

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   1. CAPTURE                                                    │
│      Input: ideas, sessions, notes, artifacts, events           │
│      → session_delta_engine + living_memory_pipeline            │
│                                                                 │
│   2. MEMORY CORE                                                │
│      Store: artifacts, context, lineage, knowledge graph        │
│      → artifact_registry + kgc_v4_connectivity                  │
│                                                                 │
│   3. CONTEXT COMPILER                                           │
│      Assemble: right context for right worker, right moment     │
│      → context_compiler_v2 + ccr_runtime_v2                     │
│                                                                 │
│   4. EXECUTION LAYER                                            │
│      Run: workers, providers, governance, cost                  │
│      → live_worker_executor + provider_router + lakshmi         │
│                                                                 │
│   5. REVIEW / OBSERVABILITY                                     │
│      See: health, quality, gaps, recommendations                │
│      → system_health_monitor + strategic_recommendation         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Mapping — 5 Cores → Existing Modules

### 1. CAPTURE
| Module | Role | Status |
|:---|:---|:---|
| session_delta_engine_v1 | Compress session → delta | KEEP |
| living_memory_pipeline_v1 | 8-stage memory ingestion | KEEP |
| execution_trace_logger_v1 | Trace every execution | KEEP |

### 2. MEMORY CORE
| Module | Role | Status |
|:---|:---|:---|
| artifact_registry_v2 | Store all artifacts | KEEP |
| kgc_v4_connectivity_engine | Knowledge graph | KEEP |
| context_cache_v1 | Cache compiled contexts | KEEP |

### 3. CONTEXT COMPILER
| Module | Role | Status |
|:---|:---|:---|
| context_compiler_v2 | Compile context packs | KEEP |
| ccr_runtime_v2 | Route to correct mode | KEEP |
| provider_payload_builder_v1 | Format per provider | KEEP |

### 4. EXECUTION LAYER
| Module | Role | Status |
|:---|:---|:---|
| live_worker_executor_v1 | Call LLM APIs | KEEP |
| provider_router_v2 | Select provider | KEEP |
| provider_registry_v1 | Provider catalog | KEEP |
| provider_health_monitor_v1 | Health check | KEEP |
| provider_failover_engine_v1 | Failover | KEEP |
| output_validator_v1 | Validate artifacts | KEEP |
| lakshmi_context_review_v1 | Constitutional governance | KEEP |
| cost_tracker_v1 | Track cost | KEEP |

### 5. REVIEW / OBSERVABILITY
| Module | Role | Status |
|:---|:---|:---|
| system_health_monitor_v1 | Health score | KEEP |
| executive_intelligence_score_v1 | EIS | KEEP |
| strategic_recommendation_engine_v1 | Self-improvement | KEEP |
| organizational_gap_analysis_v1 | Gap detection | KEEP |

---

## What Is NOT Core

Everything else is **optional infrastructure** — valuable when needed, invisible when not.

| Layer | Modules | Activate when... |
|:---|:---|:---|
| Pipeline | pipeline_state_manager + artifact_chaining + checkpoint_rollback | Multi-step tasks |
| Events | event_bus_core + 6 event_* | Real-time automation |
| ODT | odt_registry + evolution_tracker | Organizational review |
| Simulation | 6 sim_* modules | Strategic "what-if" |
| Time Machine | 5 time_* modules | Historical replay |
| Intelligence+ | mission_proposal + evidence_reasoning | Mission planning |

---

## Complexity Reduction

| Dimension | Before | After | Delta |
|:---|---:|---:|---:|
| Core modules (daily use) | 20 | **20** | same, but now explicit |
| Total modules | 71 | **20 core + 51 optional** | clarity +100% |
| Canvas maps | 26 | **3 canonical** | -88% |
| Dashboards | 17 | **3 canonical** | -82% |
| Conceptual layers | 14 | **5** | -64% |

---

## The 3 Canonical Dashboards

1. `Dashboard_Executive_Cockpit.md` — daily status
2. `Dashboard_Graph_Quality.md` — corpus health
3. `Dashboard_Providers.md` — provider health

## The 3 Canonical Canvas Maps

1. `YOS_Organizational_Digital_Twin.canvas` — system overview
2. `YOS_Digital_Thread.canvas` — mission → artifact chain
3. `YOS_Cognitive_Loop.canvas` — the 5-module loop (new)

---

## Daily Y-OS Workflow

```
Morning:  CAPTURE (session delta from yesterday)
          → MEMORY CORE (artifacts stored)
          → REVIEW (health check, gaps)

Session:  CONTEXT COMPILER (assemble pack)
          → EXECUTION LAYER (worker runs)
          → CAPTURE (artifact registered)

Weekly:   REVIEW (EIS, strategic recommendations)
          → MEMORY CORE (knowledge graph updated)
```

This is Y-OS. This is all that needs to run daily.
