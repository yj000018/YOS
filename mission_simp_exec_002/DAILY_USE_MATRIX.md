# Daily Use Matrix

> **Rule: daily/weekly = may be CORE | monthly = optional | rare/one-time = archive/experimental**

---

| Module | Expected Usage | Classification | Notes |
|---|---|---|---|
| `context_compiler_v2` | **daily** | CORE | Every session |
| `ccr_runtime_v2` | **daily** | CORE | Every dispatch |
| `provider_payload_builder_v1` | **daily** | CORE | Every LLM call |
| `live_worker_executor_v1` | **daily** | CORE | Every execution |
| `output_validator_v1` | **daily** | CORE | Every output |
| `lakshmi_context_review_v1` | **daily** | CORE | Every context pack |
| `artifact_registry_v2` | **daily** | CORE | Every artifact |
| `session_delta_engine_v1` | **daily** | CORE | Every session end |
| `context_cache_v1` | **daily** | CORE | Every context lookup |
| `provider_registry_v1` | **daily** | CORE | Every provider call |
| `provider_router_v2` | **daily** | OPTIONAL | Useful but replaceable |
| `cost_tracker_v1` | **weekly** | OPTIONAL | Budget review |
| `execution_trace_logger_v1` | **weekly** | OPTIONAL | Debugging |
| `provider_failover_engine_v1` | **weekly** | OPTIONAL | On failure events |
| `provider_health_monitor_v1` | **weekly** | OPTIONAL | Health checks |
| `living_memory_pipeline_v1` | **weekly** | OPTIONAL | Memory automation |
| `pipeline_state_manager_v1` | **weekly** | OPTIONAL | Multi-step pipelines |
| `artifact_chaining_engine_v1` | **weekly** | OPTIONAL | Lineage tracking |
| `validation_queue_v1` | **weekly** | OPTIONAL | Batch validation |
| `governance_observability_v1` | **weekly** | OPTIONAL | Compliance review |
| `system_health_monitor_v1` | **weekly** | OPTIONAL | Health dashboard |
| `kgc_v4_connectivity_engine` | **monthly** | OPTIONAL | Graph enrichment |
| `lineage_review_registry_v1` | **monthly** | OPTIONAL | Lineage audit |
| `event_bus_core_v1` | **monthly** | OPTIONAL | Event infrastructure |
| `event_registry_v1` | **monthly** | OPTIONAL | Event types |
| `event_router_v1` | **monthly** | OPTIONAL | Event routing |
| `event_persistence_v1` | **monthly** | OPTIONAL | Event storage |
| `event_replay_engine_v1` | **monthly** | OPTIONAL | Event replay |
| `event_lineage_tracker_v1` | **monthly** | OPTIONAL | Event lineage |
| `gemini_runtime_validation_v1` | **monthly** | OPTIONAL | Provider validation |
| `lineage_validation_engine_v1` | **monthly** | OPTIONAL | Lineage validation |
| `provider_cost_optimizer_v1` | **monthly** | OPTIONAL | Cost optimization |
| `strategic_recommendation_engine_v1` | **monthly** | OPTIONAL INTELLIGENCE | Strategic review |
| `organizational_gap_analysis_v1` | **monthly** | OPTIONAL INTELLIGENCE | Gap analysis |
| `evidence_based_reasoning_engine_v1` | **monthly** | OPTIONAL INTELLIGENCE | Evidence |
| `mission_proposal_generator_v1` | **monthly** | OPTIONAL INTELLIGENCE | Proposals |
| `recommendation_prioritization_engine_v1` | **monthly** | OPTIONAL INTELLIGENCE | Prioritization |
| `roadmap_generation_engine_v1` | **monthly** | OPTIONAL INTELLIGENCE | Roadmap |
| `executive_intelligence_score_v1` | **monthly** | OPTIONAL INTELLIGENCE | EIS scoring |
| `organizational_observability_engine_v1` | **monthly** | OPTIONAL INTELLIGENCE | Org analysis |
| `evolution_tracker_v1` | **rare** | ARCHIVE | Superseded |

---

## Summary

| Frequency | Count | Status |
|---|---|---|
| daily | 10 | CORE |
| weekly | 11 | OPTIONAL |
| monthly | 19 | OPTIONAL / OPTIONAL INTELLIGENCE |
| rare | 1 | ARCHIVE |
