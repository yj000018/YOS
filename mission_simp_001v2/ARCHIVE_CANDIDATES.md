---
id: ARCHIVE_CANDIDATES
title: Y-OS Archive Candidates — 34 Modules
date: 2026-06-14
tags: [archive, simplification, reduction]
---

# Archive Candidates

> **Archive = move to /archive/, preserve in Git, remove from active runtime/**  
> Nothing is deleted. Everything is recoverable. Git is the safety net.

---

## Immediate Archive (Zero Risk, < 2h total)

| Module | Reason | Effort |
|:---|:---|:---|
| kg_compiler_v3 | Superseded by v4 | 5min |
| gemini_benchmark_runner_v1 | One-time validation, done | 5min |
| legacy_lineage_recovery_engine_v1 | One-time use, mission complete | 5min |
| lineage_canvas_generator_v1 | Merge into dashboard_generator | 5min |
| lineage_dashboard_generator_v1 | Merge into dashboard_generator | 5min |
| provider_observability_dashboard_v1 | Merge into dashboard_generator | 5min |
| executive_advisor_dashboard_v1 | Merge into dashboard_generator | 5min |
| semantic_relationship_inference_v1 | Part of KGC, not standalone | 5min |
| organizational_alert_engine_v1 | Low signal/noise | 5min |
| weekly_review_generator_v1 | Not weekly use | 5min |
| strategic_memory_engine_v1 | ODT covers this | 5min |
| simulation_memory_engine_v1 | ODT covers this | 5min |
| odt_live_update_engine_v1 | Rarely triggered | 5min |
| checkpoint_rollback_engine_v1 | Rarely triggered | 5min |
| artifact_supersession_engine_v1 | Rarely triggered | 5min |

**Total: 15 modules, ~75 minutes**

---

## Experimental Layer Archive (Move to /experimental/)

| Module | Layer | Effort |
|:---|:---|:---|
| executive_simulation_engine_v1 | Simulation | 2min |
| scenario_modeling_engine_v1 | Simulation | 2min |
| impact_propagation_engine_v1 | Simulation | 2min |
| counterfactual_engine_v1 | Simulation | 2min |
| decision_comparison_engine_v1 | Simulation | 2min |
| simulation_governance_v1 | Simulation | 2min |
| odt_time_machine_v1 | Time Machine | 2min |
| organizational_snapshot_engine_v1 | Time Machine | 2min |
| temporal_reconstruction_engine_v1 | Time Machine | 2min |
| snapshot_diff_engine_v1 | Time Machine | 2min |
| organizational_timeline_generator_v1 | Time Machine | 2min |
| historical_navigation_dashboard_v1 | Time Machine | 2min |
| evolution_analysis_engine_v1 | Time Machine | 2min |
| event_observability_v1 | Events | 2min |

**Total: 14 modules, ~30 minutes**

---

## Merge Candidates (Archive after merge)

| Module | Merge Into | Effort |
|:---|:---|:---|
| gemini_runtime_validation_v1 | provider_router_v2 | 2h |
| validation_queue_v1 | output_validator_v2 | 1h |
| lineage_validation_engine_v1 | output_validator_v2 | 1h |
| lineage_review_registry_v1 | artifact_registry_v3 | 1h |
| event_lineage_tracker_v1 | execution_trace_logger_v2 | 1h |
| provider_cost_optimizer_v1 | cost_tracker_v2 | 1h |
| recommendation_prioritization_engine_v1 | strategic_rec_v2 | 1h |
| roadmap_generation_engine_v1 | strategic_rec_v2 | 1h |
| organizational_observability_engine_v1 | system_health_monitor_v2 | 2h |

**Total: 9 modules, ~11h**

---

## Summary

| Action | Modules | Effort |
|:---|---:|:---|
| Immediate archive | 15 | 75 min |
| Move to /experimental/ | 14 | 30 min |
| Archive after merge | 9 | 11h |
| **Total** | **38** | **~13h** |

**Result: 71 → 33 active modules (54% reduction)**
