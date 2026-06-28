# Context Pack Schema v2.1 (yOS Adaptation)

This schema adapts the CCR Runtime v2.1 Context Pack for the yOS Orchestration Core, integrating canonical fields and approved Manus proposals (Tiering, Checksum, CAP, Staleness).

## 1. Base Mandatory Fields

* `context_pack_id`
* `schema_version`
* `compiler_version`
* `freshness_timestamp`
* `mission_id`
* `target_worker`
* `target_capability`
* `target_provider`
* `target_model`
* `parent_artifact_id`
* `source_artifact_manifest`
* `mission_objective`
* `current_state`
* `relevant_decisions`
* `relevant_adrs`
* `relevant_laws`
* `relevant_doctrine`
* `open_loops`
* `active_constraints`
* `known_risks`
* `missing_context`
* `expected_output_artifact`
* `success_criteria`
* `output_format`
* `token_budget`
* `compression_level`
* `human_override_status`
* `governance_risk_score`
* `governance_verdict`

## 2. yOS / ELYSIUM Specific Fields

* `continuity_type`
* `session_mode`
* `canonical_memory_mode`
* `context_pack_depth` (Supports Tiering: `minimal` [T0], `standard` [T1], `full_lineage` [T2], `emergency_recovery` [T3])
* `session_continuity_mode`
* `handoff_mode`
* `confirmation_policy`
* `enforcement_level`
* `routing_matrix_version`
* `llm_matrix_rule_id`
* `chief_architect_review_required`
* `founder_confirmation_required`
* `qc_debt_status`
* `legacy_unverified_sources`
* `previous_response_id_allowed`
* `previous_response_id_used`
* `session_rotation_reason`
* `boundary_trigger`
* `downstream_application`

## 3. Integrated Canonical Enhancements (Manus Proposals)

### 3.1 Checksum / Integrity Metadata
Ensures the Context Pack is not silently truncated.
* `pack_checksum` (SHA-256)
* `pack_field_count`
* `pack_byte_size`
*(Note: Checksum is verified by runtime/script; LLM acknowledgment is declarative only. Runtime verification is authoritative.)*

### 3.2 Constraint Acknowledgment Protocol (CAP)
Validates handoff by ensuring the receiving LLM acknowledges constraints.
* `cap_required` (boolean)
* `cap_min_constraints` (integer)
* `cap_verified` (boolean/pending)

### 3.3 Staleness Detection
Defines policies based on `task_class`.
* `staleness_policy` (`strict`, `standard`, `relaxed`, `none`)
* `staleness_max_age_hours` (integer)
* `staleness_action` (`advisory`, `warning`, `blocking`, `hard_stop`)

### 3.4 Shared Pack Generic Backend
Replaces strict Notion dependency with a generic backend approach.
* `shared_pack_uri` (string)
* `shared_pack_backend` (`git`, `notion`, `registry`, `local`, `other`)

## 4. Phase 2 / Advanced Features (Deferred)
The following fields are reserved for future advanced design and are **not** part of the current MVP:
* Prompt Caching (`cache_eligible`, `cache_ttl_hours`, `cache_key`)
* Semantic Diff (`delta_mode`, `delta_fields`)
* Pack Forking (`fork_id`, `fork_parent_pack_id`, `agent_scope`, `fork_merge_policy`)
* Pack Quality Score (`pack_quality_score`, `pack_quality_evaluator`)
