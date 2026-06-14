# Y-OS Rebuild Test Matrix

> **Rule: Would this module be rebuilt in the first 7 days if Y-OS had to be recreated from zero?**
> Allowed: `YES_CORE` | `NO_OPTIONAL` | `NO_ARCHIVE`

---

## Results

| Module | Domain | Rebuild Answer | Reason |
|---|---|---|---|
| `context_compiler_v2` | context | **YES_CORE** | Day 1 — core value |
| `ccr_runtime_v2` | context | **YES_CORE** | Day 1 — routing |
| `provider_payload_builder_v1` | context | **YES_CORE** | Day 1 — LLM interface |
| `live_worker_executor_v1` | execution | **YES_CORE** | Day 1 — execution |
| `output_validator_v1` | execution | **YES_CORE** | Day 2 — integrity |
| `lakshmi_context_review_v1` | execution | **YES_CORE** | Day 3 — governance |
| `artifact_registry_v2` | memory | **YES_CORE** | Day 2 — memory |
| `session_delta_engine_v1` | capture | **YES_CORE** | Day 2 — capture |
| `context_cache_v1` | memory | **YES_CORE** | Day 3 — performance |
| `provider_registry_v1` | execution | **YES_CORE** | Day 3 — provider config |
| `provider_router_v2` | execution | NO_OPTIONAL | Week 1 — simple dict first |
| `provider_failover_engine_v1` | execution | NO_OPTIONAL | Week 2 — resilience |
| `provider_health_monitor_v1` | execution | NO_OPTIONAL | Week 2 — monitoring |
| `provider_cost_optimizer_v1` | execution | NO_OPTIONAL | Week 2 — cost control |
| `cost_tracker_v1` | execution | NO_OPTIONAL | Week 1 — useful not critical |
| `execution_trace_logger_v1` | capture | NO_OPTIONAL | Week 1 — debugging |
| `living_memory_pipeline_v1` | capture | NO_OPTIONAL | Week 2 — automation |
| `pipeline_state_manager_v1` | execution | NO_OPTIONAL | Week 2 — pipeline |
| `artifact_chaining_engine_v1` | execution | NO_OPTIONAL | Week 2 — lineage |
| `kgc_v4_connectivity_engine` | memory | NO_OPTIONAL | Week 3 — graph enrichment |
| `lineage_review_registry_v1` | memory | NO_OPTIONAL | Week 3 — lineage |
| `validation_queue_v1` | execution | NO_OPTIONAL | Week 2 — queue |
| `gemini_runtime_validation_v1` | execution | NO_OPTIONAL | Week 2 — provider-specific |
| `lineage_validation_engine_v1` | execution | NO_OPTIONAL | Week 3 — lineage |
| `event_bus_core_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `event_registry_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `event_router_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `event_persistence_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `event_replay_engine_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `event_lineage_tracker_v1` | execution | NO_OPTIONAL | Month 1 — infrastructure |
| `system_health_monitor_v1` | review | NO_OPTIONAL | Month 1 — observability |
| `executive_intelligence_score_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `governance_observability_v1` | review | NO_OPTIONAL | Month 1 — observability |
| `organizational_gap_analysis_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `evidence_based_reasoning_engine_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `mission_proposal_generator_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `recommendation_prioritization_engine_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `roadmap_generation_engine_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `strategic_recommendation_engine_v1` | review | NO_OPTIONAL | Month 2 — intelligence |
| `organizational_observability_engine_v1` | review | NO_OPTIONAL | Month 2 — observability |
| `evolution_tracker_v1` | review | NO_ARCHIVE | Superseded by time machine |

---

## Summary

| Verdict | Count | % |
|---|---|---|
| YES_CORE | **10** | 24% |
| NO_OPTIONAL | **30** | 73% |
| NO_ARCHIVE | **1** | 3% |
| **Total** | **41** | 100% |

**10 modules pass the 7-day rebuild test.**
