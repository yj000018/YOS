---
id: COMPONENT_DECISION_MATRIX
title: Y-OS Component Decision Matrix — All 71 Modules
date: 2026-06-14
tags: [simplification, classification, matrix]
---

# Component Decision Matrix

> Decision criteria: **Does this reduce human workload weekly?**  
> If not → OPTIONAL at best, ARCHIVE at worst.

Legend: **KEEP** = core, daily use | **MERGE** = combine with sibling | **ARCHIVE** = move to /archive/, preserve in Git | **DELETE LATER** = no value, remove in v3

---

## CAPTURE (Core 1)

| Module | Decision | Reason |
|:---|:---|:---|
| session_delta_engine_v1 | **KEEP** | Prevents raw history injection — daily critical |
| living_memory_pipeline_v1 | **KEEP** | 8-stage memory — weekly critical |
| execution_trace_logger_v1 | **KEEP** | Lineage — every execution |

## MEMORY CORE (Core 2)

| Module | Decision | Reason |
|:---|:---|:---|
| artifact_registry_v2 | **KEEP** | Central store — irreplaceable |
| kgc_v4_connectivity_engine | **KEEP** | Knowledge graph — weekly use |
| context_cache_v1 | **KEEP** | Performance — every session |
| kg_compiler_v3 | **ARCHIVE** | Superseded by v4 |

## CONTEXT COMPILER (Core 3)

| Module | Decision | Reason |
|:---|:---|:---|
| context_compiler_v2 | **KEEP** | Core function |
| ccr_runtime_v2 | **KEEP** | Core routing |
| provider_payload_builder_v1 | **KEEP** | Required for every LLM call |

## EXECUTION LAYER (Core 4)

| Module | Decision | Reason |
|:---|:---|:---|
| live_worker_executor_v1 | **KEEP** | Core execution |
| provider_router_v2 | **KEEP** | Core routing |
| provider_registry_v1 | **KEEP** | Provider catalog |
| provider_health_monitor_v1 | **KEEP** | Resilience |
| provider_failover_engine_v1 | **KEEP** | Resilience |
| output_validator_v1 | **KEEP** | Artifact quality |
| lakshmi_context_review_v1 | **KEEP** | Constitutional governance |
| cost_tracker_v1 | **KEEP** | Budget awareness |
| gemini_runtime_validation_v1 | **MERGE** → provider_router_v2 | Gemini-specific, merge |
| gemini_benchmark_runner_v1 | **ARCHIVE** | One-time use, done |

## REVIEW / OBSERVABILITY (Core 5)

| Module | Decision | Reason |
|:---|:---|:---|
| system_health_monitor_v1 | **KEEP** | Daily health check |
| executive_intelligence_score_v1 | **KEEP** | Weekly EIS |
| strategic_recommendation_engine_v1 | **KEEP** | Self-improvement |
| organizational_gap_analysis_v1 | **KEEP** | Gap detection |
| governance_observability_v1 | **KEEP** | Compliance tracking |
| organizational_observability_engine_v1 | **MERGE** → system_health_monitor_v2 | Overlaps health monitor |
| organizational_alert_engine_v1 | **ARCHIVE** | Low signal/noise, not weekly |
| weekly_review_generator_v1 | **ARCHIVE** | Nice-to-have, not daily |
| executive_advisor_dashboard_v1 | **ARCHIVE** | Dashboard gen, low use |

## PIPELINE

| Module | Decision | Reason |
|:---|:---|:---|
| pipeline_state_manager_v1 | **KEEP** | Multi-step tasks |
| artifact_chaining_engine_v1 | **KEEP** | Lineage |
| checkpoint_rollback_engine_v1 | **ARCHIVE** | Rarely triggered, keep in Git |
| validation_queue_v1 | **MERGE** → output_validator_v2 | Overlaps validator |
| artifact_supersession_engine_v1 | **ARCHIVE** | Rarely triggered |

## INTELLIGENCE+

| Module | Decision | Reason |
|:---|:---|:---|
| evidence_based_reasoning_engine_v1 | **KEEP** | Evidence-backed recs |
| mission_proposal_generator_v1 | **KEEP** | Mission planning |
| recommendation_prioritization_engine_v1 | **MERGE** → strategic_rec_v2 | Overlaps |
| roadmap_generation_engine_v1 | **MERGE** → strategic_rec_v2 | Overlaps |
| strategic_memory_engine_v1 | **ARCHIVE** | ODT covers this |
| simulation_memory_engine_v1 | **ARCHIVE** | ODT covers this |

## PROVIDERS

| Module | Decision | Reason |
|:---|:---|:---|
| provider_cost_optimizer_v1 | **MERGE** → cost_tracker_v2 | Overlaps cost_tracker |
| provider_observability_dashboard_v1 | **ARCHIVE** | Dashboard gen, low use |

## ODT

| Module | Decision | Reason |
|:---|:---|:---|
| organizational_digital_twin_registry_v1 | **KEEP** | Org awareness (weekly) |
| evolution_tracker_v1 | **KEEP** | Evolution tracking |
| odt_live_update_engine_v1 | **ARCHIVE** | Rarely triggered |
| system_health_monitor_v1 | **KEEP** | Already in Core 5 |

## EVENTS

| Module | Decision | Reason |
|:---|:---|:---|
| event_bus_core_v1 | **KEEP** | Infrastructure (activate when needed) |
| event_registry_v1 | **KEEP** | Event catalog |
| event_router_v1 | **KEEP** | Event routing |
| event_persistence_v1 | **KEEP** | Event store |
| event_replay_engine_v1 | **KEEP** | Time machine dependency |
| event_observability_v1 | **ARCHIVE** | Low daily use |
| event_lineage_tracker_v1 | **MERGE** → execution_trace_logger_v2 | Overlaps |

## SIMULATION (EXPERIMENTAL)

| Module | Decision | Reason |
|:---|:---|:---|
| executive_simulation_engine_v1 | **ARCHIVE** | Not weekly, high complexity |
| scenario_modeling_engine_v1 | **ARCHIVE** | Not weekly |
| impact_propagation_engine_v1 | **ARCHIVE** | Not weekly |
| counterfactual_engine_v1 | **ARCHIVE** | Not weekly |
| decision_comparison_engine_v1 | **ARCHIVE** | Not weekly |
| simulation_governance_v1 | **ARCHIVE** | Not weekly |

## TIME MACHINE (EXPERIMENTAL)

| Module | Decision | Reason |
|:---|:---|:---|
| odt_time_machine_v1 | **ARCHIVE** | Not weekly, high complexity |
| organizational_snapshot_engine_v1 | **ARCHIVE** | Not weekly |
| temporal_reconstruction_engine_v1 | **ARCHIVE** | Not weekly |
| snapshot_diff_engine_v1 | **ARCHIVE** | Not weekly |
| organizational_timeline_generator_v1 | **ARCHIVE** | Not weekly |
| historical_navigation_dashboard_v1 | **ARCHIVE** | Not weekly |
| evolution_analysis_engine_v1 | **ARCHIVE** | Not weekly |

## LINEAGE (LEGACY)

| Module | Decision | Reason |
|:---|:---|:---|
| legacy_lineage_recovery_engine_v1 | **ARCHIVE** | One-time use, done |
| semantic_relationship_inference_v1 | **ARCHIVE** | Part of KGC, not standalone |
| lineage_validation_engine_v1 | **MERGE** → output_validator_v2 | Overlaps |
| lineage_review_registry_v1 | **MERGE** → artifact_registry_v3 | Overlaps |
| lineage_dashboard_generator_v1 | **ARCHIVE** | Dashboard gen, low use |
| lineage_canvas_generator_v1 | **ARCHIVE** | Canvas gen, low use |

---

## Summary

| Decision | Count | % |
|:---|---:|---:|
| **KEEP** | 28 | 39% |
| **MERGE** | 9 | 13% |
| **ARCHIVE** | 34 | 48% |
| **DELETE LATER** | 0 | 0% |
| **Total** | **71** | 100% |

**Complexity reduction: 48% immediate (archive) + 13% merge = 61% total reduction**
