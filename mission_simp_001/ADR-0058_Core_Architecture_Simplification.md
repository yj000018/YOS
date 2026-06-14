---
id: ADR-0058
title: Core Architecture Simplification — Y-OS v2
status: ACCEPTED
date: 2026-06-14
deciders: [Brahma, Lakshmi, Ganesha]
supersedes: []
governed_by: [CONSTITUTION/Y-OS_Constitution_v1.md]
tags: [simplification, architecture, core, reduction]
---

# ADR-0058 — Core Architecture Simplification (Y-OS v2)

## Context

After MISSION-013 through MISSION-031 (19 missions), Y-OS has accumulated:
- **71 runtime modules** across 14 functional groups
- **53 ADRs**, **36 mission directories**, **26 canvas maps**, **17 dashboards**
- **548 Markdown files** in the corpus

Only **28% of modules are used daily**. The architecture has grown organically, accumulating experimental layers, one-time tools, and duplicate functionality. Conceptual complexity is HIGH. Navigation burden is HIGH.

MISSION-SIMP-001 was commissioned to reduce Y-OS to the smallest viable architecture that preserves the core vision.

## Decision

**Adopt Core Architecture v2** — 27 modules, 7 layers — as the canonical Y-OS platform.

All other modules are classified as OPTIONAL or EXPERIMENTAL and moved to separate layers that can be activated on demand.

Execute the Simplification Backlog (SIMP-001 through SIMP-020) over 3–4 days.

## Core Architecture v2

```
L1 ROUTING (5)       — ccr_runtime · context_compiler · provider_router
                        provider_registry · provider_payload_builder
L2 EXECUTION (4)     — live_worker_executor · output_validator
                        artifact_registry · lakshmi_context_review
L3 MEMORY (4)        — session_delta · execution_trace_logger
                        cost_tracker · context_cache
L4 PIPELINE (4)      — pipeline_state_manager · artifact_chaining
                        provider_health_monitor · provider_failover
L5 OBSERVABILITY (4) — system_health_monitor · executive_intelligence_score
                        governance_observability · org_observability_engine
L6 INTELLIGENCE (4)  — strategic_recommendation · gap_analysis
                        evidence_reasoning · mission_proposal_generator
L7 KNOWLEDGE (2)     — kgc_v4_connectivity · living_memory_pipeline
```

**Optional layers:**
- L8 EVENTS (7 modules) — real-time triggers
- L9 ODT (4 modules) — organizational awareness
- L10 EXPERIMENTAL (11 modules) — simulation + time machine

## Consequences

### Positive
- 62% reduction in core module count (71 → 27)
- 27% immediate reduction via sunset/merge (71 → 52)
- 100% of CORE modules are daily-use
- Clear separation: platform vs optional layers
- Rebuild test: Y-OS core can be rebuilt in 7 days
- Cognitive navigation: 8 canonical canvas maps (vs 26)
- Dashboard clarity: 6 canonical dashboards (vs 17)

### Negative
- Merge work required (~25h effort)
- Experimental modules need explicit activation
- Some one-time tools lose visibility (archived, not deleted)

### Neutral
- All doctrine preserved (Constitution, ADRs, Missions)
- No files deleted — only archived or merged
- GitHub history preserved

## Governance Review

**Lakshmi — APPROVE**

| Article | Check | Status |
|:---|:---|:---|
| Art. 1 — Artifact Primacy | All artifacts preserved | ✅ |
| Art. 2 — Preservation | No deletion, only archival | ✅ |
| Art. 3 — Derivation Transparency | Merge lineage documented | ✅ |
| Art. 4 — Human Override | Human approval required for each SIMP action | ✅ |
| Art. 5 — Governance Before Autonomy | ADR approved before execution | ✅ |

**Risk Score: 5/100 — APPROVE**

**Ganesha — ADOPT**

Execute SIMP-001 through SIMP-020 in order. Start with quick wins (SIMP-001, SIMP-005, SIMP-006, SIMP-015, SIMP-016) — total effort: 90 minutes, zero risk.

## Simplification Roadmap

### Phase 1 — Quick Wins (90 min, zero risk)
- SIMP-001: ARCHIVE kg_compiler_v3
- SIMP-005: ARCHIVE legacy_lineage_recovery
- SIMP-006: ARCHIVE gemini_benchmark_runner
- SIMP-015: MOVE simulation → /experimental/
- SIMP-016: MOVE time_machine → /experimental/

### Phase 2 — Merges (1 day)
- SIMP-002: MERGE 4 dashboard generators
- SIMP-003: MERGE validation modules
- SIMP-004: MERGE cost tracking
- SIMP-010: MERGE lineage tracking
- SIMP-011: MERGE registries

### Phase 3 — Structure (1 day)
- SIMP-017: FLATTEN runtime/ by layer
- SIMP-018: CONSOLIDATE canvas maps → 8
- SIMP-019: CONSOLIDATE dashboards → 6
- SIMP-020: ARCHIVE mission_001–012 dirs

### Phase 4 — Intelligence Merges (1 day)
- SIMP-007: MERGE gemini_runtime_validation
- SIMP-008: MERGE memory engines
- SIMP-009: MERGE intelligence modules
- SIMP-012–014: DEPRECATE low-value modules

**Total: ~25h effort. Achievable in 3–4 days.**
