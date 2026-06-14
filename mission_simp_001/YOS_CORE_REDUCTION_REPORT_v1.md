---
id: MISSION-SIMP-001
title: Y-OS Core Reduction Audit
status: PASSED
date: 2026-06-14
owner: Brahma
adr: ADR-0058
tags: [simplification, architecture, reduction, core, audit]
---

# Y-OS Core Reduction Audit — MISSION-SIMP-001

## Mission Question

Can Y-OS be reduced to the smallest viable architecture that preserves the core vision, without adding new capabilities?

## Answer

**YES — 27% immediate reduction possible. 50%+ with full simplification.**

---

## A. Full Inventory

| Component Type | Count | Daily Use |
|:---|---:|---:|
| Runtime modules | 71 | 20 (28%) |
| ADRs | 53 | — |
| Mission directories | 36 | — |
| Dashboards | 17 | 3–4 |
| Canvas maps | 26 | 2–3 |
| Concept nodes | 39 | — |
| Total Markdown files | 548 | — |

**Key finding:** Only 28% of modules are used daily. 72% are infrastructure, one-time tools, or experimental layers.

---

## B. Capability Classification

### CORE — 12 modules (17%)
*Must exist. Used daily. Cannot be removed.*

| Module | Group | Purpose |
|:---|:---|:---|
| ccr_runtime_v2 | routing | Context Router — heart of Y-OS |
| context_compiler_v2 | routing | Context Pack compiler |
| provider_router_v2 | routing | Multi-provider routing |
| provider_registry_v1 | routing | Provider registry |
| provider_payload_builder_v1 | routing | Payload formatting |
| live_worker_executor_v1 | execution | Real LLM API calls |
| output_validator_v1 | execution | Artifact validation |
| artifact_registry_v2 | memory | Artifact storage |
| lakshmi_context_review_v1 | governance | Constitutional governance |
| session_delta_engine_v1 | memory | Prevents raw history injection |
| execution_trace_logger_v1 | observability | Execution lineage |
| cost_tracker_v1 | observability | Cost per call |

### IMPORTANT — 24 modules (34%)
*High value. Used regularly. Should exist but not daily-critical.*

Pipeline (5): pipeline_state_manager, artifact_chaining_engine, checkpoint_rollback_engine, validation_queue, context_cache

Memory (1): living_memory_pipeline

Providers (2): provider_health_monitor, provider_failover_engine

Graph (1): kgc_v4_connectivity_engine

ODT (3): organizational_digital_twin_registry, evolution_tracker, system_health_monitor

Observability (3): organizational_observability_engine, governance_observability, executive_intelligence_score

Intelligence (4): strategic_recommendation_engine, organizational_gap_analysis, evidence_based_reasoning_engine, mission_proposal_generator

Events (5): event_bus_core, event_registry, event_router, event_persistence, event_replay_engine

### OPTIONAL — 24 modules (34%)
*Nice-to-have. Low daily use. Candidates for merge or archive.*

Memory (2): strategic_memory_engine, simulation_memory_engine  
Providers (3): provider_cost_optimizer, provider_observability_dashboard, gemini_benchmark_runner  
Observability (2): organizational_alert_engine, weekly_review_generator  
ODT (1): odt_live_update_engine  
Intelligence (2): recommendation_prioritization_engine, roadmap_generation_engine  
Time (3): organizational_timeline_generator, historical_navigation_dashboard, evolution_analysis_engine  
Lineage (6): legacy_lineage_recovery, semantic_relationship_inference, lineage_validation, lineage_review_registry, lineage_dashboard_generator, lineage_canvas_generator  
Events (2): event_observability, event_lineage_tracker  
Artifacts (1): artifact_supersession_engine  
Providers (1): gemini_runtime_validation  
Exec (1): executive_advisor_dashboard  

### EXPERIMENTAL — 11 modules (15%)
*High complexity. Low daily use. Valuable but not core.*

Simulation (6): executive_simulation_engine, scenario_modeling_engine, impact_propagation_engine, counterfactual_engine, decision_comparison_engine, simulation_governance

Time Machine (5): odt_time_machine, organizational_snapshot_engine, temporal_reconstruction_engine, snapshot_diff_engine + event_replay_engine (shared)

---

## C. Duplicate & Overlap Analysis

| Group | Modules | Recommendation | Savings |
|:---|:---|:---|:---|
| Cost Tracking | cost_tracker + provider_cost_optimizer | MERGE → cost_tracker_v2 | 1 module |
| Validation | output_validator + validation_queue + lineage_validation | MERGE → validation_engine_v2 | 2 modules |
| Dashboard Generators | 4 separate generators | MERGE → dashboard_generator_v1 | 3 modules |
| Memory | strategic_memory + simulation_memory | MERGE → memory_engine_v2 | 2 modules |
| Lineage Tracking | execution_trace + event_lineage + lineage_validation | MERGE → lineage_tracker_v2 | 2 modules |
| KGC Versions | kg_compiler_v3 + kgc_v4 | ARCHIVE v3 (superseded) | 1 module |
| Gemini-Specific | gemini_runtime_validation + gemini_benchmark | MERGE into provider_router | 2 modules |
| Intelligence | strategic_rec + prioritization + roadmap_gen | MERGE → strategic_rec_v2 | 2 modules |
| Registry | lineage_review_registry | MERGE into artifact_registry | 1 module |

**Total potential savings: 16 modules via merge**

---

## D. Sunset Candidates — 19 modules

| Module | Reason | Risk |
|:---|:---|:---|
| kg_compiler_v3 | Superseded by v4 | LOW |
| gemini_benchmark_runner_v1 | One-time validation, done | LOW |
| gemini_runtime_validation_v1 | Merge into provider_router | LOW |
| simulation_memory_engine_v1 | ODT covers this | LOW |
| strategic_memory_engine_v1 | ODT + strategic_rec covers this | LOW |
| legacy_lineage_recovery_engine_v1 | One-time use, mission complete | LOW |
| lineage_canvas_generator_v1 | Merge into dashboard_generator | LOW |
| lineage_dashboard_generator_v1 | Merge into dashboard_generator | LOW |
| provider_observability_dashboard_v1 | Merge into dashboard_generator | LOW |
| executive_advisor_dashboard_v1 | Merge into dashboard_generator | LOW |
| event_lineage_tracker_v1 | Merge into execution_trace_logger | LOW |
| lineage_review_registry_v1 | Merge into artifact_registry | LOW |
| lineage_validation_engine_v1 | Merge into output_validator | LOW |
| provider_cost_optimizer_v1 | Merge into cost_tracker | LOW |
| recommendation_prioritization_engine_v1 | Merge into strategic_rec | LOW |
| roadmap_generation_engine_v1 | Merge into strategic_rec | LOW |
| organizational_alert_engine_v1 | Low signal/noise | MEDIUM |
| weekly_review_generator_v1 | Low daily use | LOW |
| odt_live_update_engine_v1 | Rarely triggered | MEDIUM |

**All 19 are LOW or MEDIUM risk. Zero CORE modules in this list.**

---

## E. Core Architecture v2

> **27 modules. 7 layers. Everything needed, nothing extra.**

```
┌─────────────────────────────────────────────────────────┐
│  L1 ROUTING (5)                                         │
│  ccr_runtime · context_compiler · provider_router       │
│  provider_registry · provider_payload_builder           │
├─────────────────────────────────────────────────────────┤
│  L2 EXECUTION (4)                                       │
│  live_worker_executor · output_validator                │
│  artifact_registry · lakshmi_context_review             │
├─────────────────────────────────────────────────────────┤
│  L3 MEMORY (4)                                          │
│  session_delta · execution_trace_logger                 │
│  cost_tracker · context_cache                           │
├─────────────────────────────────────────────────────────┤
│  L4 PIPELINE (4)                                        │
│  pipeline_state_manager · artifact_chaining             │
│  provider_health_monitor · provider_failover            │
├─────────────────────────────────────────────────────────┤
│  L5 OBSERVABILITY (4)                                   │
│  system_health_monitor · executive_intelligence_score   │
│  governance_observability · org_observability_engine    │
├─────────────────────────────────────────────────────────┤
│  L6 INTELLIGENCE (4)                                    │
│  strategic_recommendation · gap_analysis                │
│  evidence_reasoning · mission_proposal_generator        │
├─────────────────────────────────────────────────────────┤
│  L7 KNOWLEDGE (2)                                       │
│  kgc_v4_connectivity · living_memory_pipeline           │
└─────────────────────────────────────────────────────────┘

Optional layers (add when needed):
  L8 EVENTS         — 7 modules (real-time triggers)
  L9 ODT            — 4 modules (organizational awareness)
  L10 EXPERIMENTAL  — 11 modules (simulation + time machine)
```

**Core: 27 modules vs current 71 = 62% reduction in core footprint**

---

## F. Simplification Backlog — Prioritized by ROI

| ID | Action | Effort | ROI | Risk |
|:---|:---|:---|:---|:---|
| SIMP-001 | ARCHIVE kg_compiler_v3 | 30min | HIGH | LOW |
| SIMP-002 | MERGE 4 dashboard generators → dashboard_generator_v1 | 2h | HIGH | LOW |
| SIMP-003 | MERGE validation_queue + lineage_validation → output_validator_v2 | 2h | HIGH | LOW |
| SIMP-004 | MERGE cost_tracker + provider_cost_optimizer → cost_tracker_v2 | 1h | HIGH | LOW |
| SIMP-005 | ARCHIVE legacy_lineage_recovery | 10min | HIGH | LOW |
| SIMP-006 | ARCHIVE gemini_benchmark_runner | 10min | MEDIUM | LOW |
| SIMP-007 | MERGE gemini_runtime_validation → provider_router_v2 | 2h | MEDIUM | LOW |
| SIMP-008 | MERGE strategic_memory + simulation_memory → memory_engine_v2 | 2h | MEDIUM | LOW |
| SIMP-009 | MERGE recommendation_prioritization + roadmap_gen → strategic_rec_v2 | 2h | MEDIUM | LOW |
| SIMP-010 | MERGE event_lineage_tracker → execution_trace_logger_v2 | 1h | MEDIUM | LOW |
| SIMP-011 | MERGE lineage_review_registry → artifact_registry_v3 | 1h | MEDIUM | LOW |
| SIMP-012 | DEPRECATE organizational_alert_engine | 10min | MEDIUM | LOW |
| SIMP-013 | DEPRECATE weekly_review_generator | 10min | LOW | LOW |
| SIMP-014 | DEPRECATE odt_live_update_engine | 10min | LOW | MEDIUM |
| SIMP-015 | MOVE simulation layer → /experimental/ | 30min | HIGH | LOW |
| SIMP-016 | MOVE time_machine layer → /experimental/ | 30min | HIGH | LOW |
| SIMP-017 | FLATTEN runtime/ → group by layer | 2h | HIGH | LOW |
| SIMP-018 | CONSOLIDATE 26 canvas maps → 8 canonical | 2h | HIGH | LOW |
| SIMP-019 | CONSOLIDATE 17 dashboards → 6 canonical | 2h | HIGH | LOW |
| SIMP-020 | ARCHIVE mission_001→012 dirs → /archive/ | 1h | MEDIUM | LOW |

**Total effort: ~25h. Achievable in 3–4 days.**

---

## G. Rebuild Test — 7 Days

> If Y-OS had to be rebuilt from scratch, what would be rebuilt?

| Day | Layer | Modules | Rationale |
|:---|:---|:---|:---|
| 1 | Foundation | ccr_runtime, context_compiler, provider_router, provider_registry, provider_payload_builder | Without routing, nothing works |
| 2 | Execution + Gov | live_worker_executor, output_validator, artifact_registry, lakshmi_context_review | Without execution + governance, no artifacts |
| 3 | Memory | session_delta, execution_trace_logger, cost_tracker | Without memory, no continuity |
| 4 | Pipeline + Resilience | pipeline_state_manager, artifact_chaining, provider_health_monitor, provider_failover | Multi-step + failover |
| 5 | Observability | system_health_monitor, executive_intelligence_score, org_observability_engine | Without observability, no self-awareness |
| 6 | Intelligence | strategic_recommendation, gap_analysis, evidence_reasoning, mission_proposal_generator | Strategic autonomy |
| 7 | Knowledge | kgc_v4_connectivity, living_memory_pipeline | Corpus navigation + memory |

**Total: 27 modules in 7 days.**

### NOT rebuilt in 7 days (add in month 2):
- Event Bus (7 modules) — add when real-time triggers needed
- ODT Registry + Evolution (4 modules) — add for org awareness
- Simulation Layer (6 modules) — add for predictive capability
- Time Machine (5 modules) — add for historical replay
- All lineage-specific legacy modules (6 modules)
- All dashboard generator variants (4 modules)

**Conclusion:** 44 modules (62%) would NOT be rebuilt in the first 7 days. They represent valuable but non-essential capabilities.

---

## H. Architectural Debt Summary

| Debt Type | Count | Impact |
|:---|---:|:---|
| Superseded versions | 1 (kg_compiler_v3) | LOW — just archive |
| One-time use modules | 2 (legacy_lineage, gemini_benchmark) | LOW — archive |
| Duplicate functionality | 9 groups | MEDIUM — merge needed |
| Flat runtime/ directory | 71 files | HIGH — navigation burden |
| 26 canvas maps (too many) | 18 redundant | HIGH — cognitive overload |
| 17 dashboards (too many) | 11 redundant | HIGH — cognitive overload |
| Mission dirs 001–012 | 12 legacy dirs | MEDIUM — archive |

---

## I. Preservation of Y-OS Vision

The original Y-OS vision:
> *A cognitive operating system that routes cognition, preserves governance, builds memory, and enables organizational self-awareness.*

**Core Architecture v2 fully preserves this:**
- ✅ Routes cognition (L1 ROUTING)
- ✅ Preserves governance (L2 EXECUTION + Lakshmi)
- ✅ Builds memory (L3 MEMORY + L7 KNOWLEDGE)
- ✅ Enables self-awareness (L5 OBSERVABILITY + L6 INTELLIGENCE)

**Nothing in the Core Architecture v2 is new capability. It is the distillation of what already exists.**

---

## J. Metrics

| Metric | Current | Target | Reduction |
|:---|---:|---:|---:|
| Runtime modules | 71 | 27 (core) | 62% |
| After sunset/merge | 71 | 52 | 27% |
| Canvas maps | 26 | 8 | 69% |
| Dashboards | 17 | 6 | 65% |
| Conceptual complexity | HIGH | MEDIUM | ~40% |
| Daily-use modules | 20 (28%) | 27 (100% core) | +72% relevance |

---

## Governance

**Lakshmi: APPROVE — Score 5/100**  
No doctrine rewritten. No files deleted. No new capabilities added. Pure reduction.

**Ganesha: ADOPT**  
Execute SIMP-001 through SIMP-020 in order. Start with quick wins (SIMP-001, SIMP-005, SIMP-006, SIMP-015, SIMP-016).
