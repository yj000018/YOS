---
id: yos-mission-021a
title: 'MISSION-021A: Roadmap Architecture Review — MISSION-021→026'
type: mission
status: PASSED
date: '2026-06-14'
owner: Brahma
adr: '[[ADR-0048]]'
tags: ['#mission', '#passed', '#yos', '#roadmap', '#architecture', '#mission-021a']
aliases:
  - MISSION-021A
  - Roadmap Architecture Review
source_branch: y-os-doctrine
canonical: true
---

# MISSION-021A: Roadmap Architecture Review — PASSED ✅

**Question:** Is the proposed sequence 021→022→023→024→025→026 architecturally optimal?

**Answer: NO — the sequence is sub-optimal. Revised sequence proposed below.**

---

## Mission Analysis — 6 Missions

---

### MISSION-021 — Semantic Connectivity Layer (KGC v4)

| Field | Value |
| :--- | :--- |
| **Objective** | Reduce orphan rate 34.7% → <15% via body wikilinks pass. Raise EIS Graph Quality 47.9 → 80+. |
| **Architectural Role** | **Foundation layer** — improves graph traversability for ALL subsequent missions. M-024 (Time Machine) and M-025 (Strategic Engine) both depend on high-quality graph connectivity to reason over the corpus. |
| **Dependencies** | M-020 (Observability metrics to measure improvement) |
| **Outputs** | `kg_compiler_v4.py`, enriched body wikilinks, ADR-0049, EIS Graph Quality ≥ 80 |
| **Risks** | Body edits must remain additive — no doctrine rewrite. Risk: over-linking creates noise. |
| **Required Prerequisites** | M-020 (EIS baseline), M-019 (ODT Registry) |
| **Optional Prerequisites** | None |

---

### MISSION-022 — Live Event Bus

| Field | Value |
| :--- | :--- |
| **Objective** | Replace manual ODT update triggers with a real-time event bus. Any mission/artifact/ADR event auto-propagates through the ODT. |
| **Architectural Role** | **Infrastructure layer** — enables all subsequent missions to operate continuously rather than on-demand. M-025 (Strategic Engine) and M-026 (Simulation) require live state to reason correctly. |
| **Dependencies** | M-021 (clean graph as event payload), M-020 (ODT Live Update Engine as base) |
| **Outputs** | `event_bus_v1.py`, event schema, webhook handlers, `event_log.jsonl` |
| **Risks** | In-process event bus only (no external broker like Kafka/Redis without persistent VM). Risk: events lost on sandbox hibernation. |
| **Required Prerequisites** | M-020 (ODT Live Update Engine) |
| **Optional Prerequisites** | M-021 (graph quality improves event payload richness) |

**Critical Note:** M-022 does NOT require M-021 as a hard dependency. The event bus works on any graph quality. M-021 improves the *content* of events but not the *mechanism*. These can be parallelized.

---

### MISSION-023 — Provider Diversification

| Field | Value |
| :--- | :--- |
| **Objective** | Add Gemini worker. Reduce OpenAI dependence from 73% → <50%. Implement provider routing logic. |
| **Architectural Role** | **Resilience layer** — decouples Y-OS from single-provider risk. Required before M-025 (Strategic Engine) which will make many LLM calls. |
| **Dependencies** | M-022 (event bus to route provider selection events), M-016 (CCR Runtime v2 as base) |
| **Outputs** | `provider_router_v1.py`, Gemini worker, updated `model_registry.json`, provider health monitor |
| **Risks** | Gemini API key not in Manus Secrets — requires configuration. Google AI SDK install needed. |
| **Required Prerequisites** | M-016 (CCR Runtime v2), M-020 (cost tracker) |
| **Optional Prerequisites** | M-022 (event bus for provider health events) |

**Critical Note:** M-023 does NOT require M-022 as a hard dependency. Provider routing works without an event bus. M-022 enriches it but is not blocking.

---

### MISSION-024 — ODT Time Machine

| Field | Value |
| :--- | :--- |
| **Objective** | Replay the complete Y-OS evolution M-013 → present. Navigate any historical state. Compute delta between any two snapshots. |
| **Architectural Role** | **Historical intelligence layer** — enables M-025 (Strategic Engine) to reason over historical patterns, not just current state. The Time Machine is the memory substrate for strategic reasoning. |
| **Dependencies** | M-021 (high-quality graph for each snapshot), M-019 (evolution tracker as data source), M-020 (observability metrics per snapshot) |
| **Outputs** | `time_machine_v1.py`, snapshot registry, delta engine, `evolution_timeline.json`, Canvas time map |
| **Risks** | Historical snapshots are reconstructed from Git history — not live-captured. Fidelity depends on commit granularity. |
| **Required Prerequisites** | M-019 (evolution tracker), M-021 (graph quality for meaningful snapshots) |
| **Optional Prerequisites** | M-022 (event bus for real-time snapshot triggers) |

---

### MISSION-025 — Strategic Recommendation Engine

| Field | Value |
| :--- | :--- |
| **Objective** | Y-OS analyzes its own state and proposes the next missions autonomously. Replaces human roadmap authoring. |
| **Architectural Role** | **Cognitive autonomy layer** — the first mission where Y-OS reasons about its own future. Requires: high-quality graph (M-021), live state (M-022), multi-provider LLM (M-023), historical patterns (M-024). |
| **Dependencies** | M-021 (graph quality), M-023 (multi-provider for diverse reasoning), M-024 (historical patterns) |
| **Outputs** | `strategic_recommendation_engine_v1.py`, `strategic_recommendations.md`, self-generated mission specs |
| **Risks** | Circular reasoning risk — Y-OS may recommend missions that perpetuate its own biases. Lakshmi governance required. |
| **Required Prerequisites** | M-021, M-023, M-024 |
| **Optional Prerequisites** | M-022 (live state improves recommendation freshness) |

---

### MISSION-026 — Executive Simulation Layer

| Field | Value |
| :--- | :--- |
| **Objective** | "If we change X, what happens to Y?" — causal simulation over the ODT. Counterfactual reasoning. |
| **Architectural Role** | **Simulation layer** — the most advanced capability. Requires all prior layers: graph (M-021), live events (M-022), multi-provider (M-023), historical baselines (M-024), strategic context (M-025). |
| **Dependencies** | M-021 through M-025 (all) |
| **Outputs** | `simulation_engine_v1.py`, counterfactual reports, scenario canvas maps |
| **Risks** | Simulation validity depends on causal model quality — requires explicit causal graph encoding. |
| **Required Prerequisites** | M-021, M-022, M-023, M-024, M-025 |
| **Optional Prerequisites** | None |

---

## Dependency Analysis

### Hard Dependencies (blocking)

```
M-020 → M-021 (EIS baseline required)
M-020 → M-022 (ODT Live Update Engine as base)
M-016 → M-023 (CCR Runtime v2 as base)
M-021 → M-024 (graph quality for meaningful snapshots)
M-021 → M-025 (graph quality for strategic reasoning)
M-023 → M-025 (multi-provider for diverse reasoning)
M-024 → M-025 (historical patterns for strategy)
M-021 + M-022 + M-023 + M-024 + M-025 → M-026
```

### Soft Dependencies (enriching, not blocking)

```
M-021 → M-022 (richer event payloads)
M-022 → M-023 (event bus for provider health)
M-022 → M-025 (live state for fresher recommendations)
```

---

## Sequence Optimality Verdict

### Proposed Sequence: 021→022→023→024→025→026

**VERDICT: SUB-OPTIMAL**

**Problem 1 — M-022 and M-023 are independent of each other and of M-021.**
The proposed sequence forces M-022 to wait for M-021 (unnecessary) and M-023 to wait for M-022 (unnecessary). Both can start after M-020.

**Problem 2 — M-024 is blocked only by M-021, not by M-022 or M-023.**
Placing M-024 after M-023 adds 2 unnecessary missions of latency on the critical path to Time Machine.

**Problem 3 — M-025 requires M-021 + M-023 + M-024 but NOT M-022 as a hard dependency.**
The proposed sequence delays M-025 by 1 mission unnecessarily.

---

## Revised Sequence — Architecturally Optimal

### Option A: Pure Sequential (safe, no parallelism)

```
M-021 → M-023 → M-022 → M-024 → M-025 → M-026
```

Rationale:
- M-021 first: graph quality improves all downstream payloads
- M-023 before M-022: provider routing is more foundational than event bus
- M-022 after M-023: event bus now routes provider health events correctly
- M-024 after M-021: graph quality ready for meaningful snapshots
- M-025 after M-021 + M-023 + M-024: all hard dependencies met
- M-026 last: requires all prior layers

**Saves 1 mission of unnecessary latency on critical path.**

### Option B: Parallel Tracks (faster, requires parallel execution)

```
Track A: M-021 → M-024 → M-025 → M-026
Track B: M-023 → M-022 (parallel to Track A after M-021)
Merge: M-025 waits for Track B completion before executing
```

**Saves 2 missions of latency on critical path to M-025.**

### ⭐ Recommendation: Option A (Pure Sequential)

Manus executes sequentially. Option A is optimal for sequential execution.

---

## Critical Path Analysis

### Critical Path to each target

| Target | Critical Path | Length |
| :--- | :--- | :--- |
| **Digital Thread** (live graph) | M-021 → M-022 | 2 missions |
| **Time Machine** | M-021 → M-024 | 2 missions |
| **Strategic Engine** | M-021 → M-023 → M-024 → M-025 | 4 missions |
| **Executive Simulation** | M-021 → M-023 → M-022 → M-024 → M-025 → M-026 | 6 missions |

### Fastest Paths

**Fastest to Digital Thread:** M-021 → M-022 (skip M-023 if provider diversification not needed first)

**Fastest to Time Machine:** M-021 → M-024 (M-022 and M-023 are NOT on critical path to Time Machine)

**Fastest to Strategic Engine:** M-021 → M-023 → M-024 → M-025 (M-022 is soft dependency only)

**Fastest to Executive Simulation:** Full sequence required — M-026 has hard dependencies on all 5 prior missions.

---

## Capability Graph

| Capability | Provided By | Required By |
| :--- | :--- | :--- |
| High-quality graph traversal | M-021 | M-024, M-025, M-026 |
| Real-time event propagation | M-022 | M-025 (soft), M-026 |
| Multi-provider LLM routing | M-023 | M-025, M-026 |
| Historical state replay | M-024 | M-025, M-026 |
| Strategic self-reasoning | M-025 | M-026 |
| Causal simulation | M-026 | — |

---

## Execution Order — Final Recommendation

| Order | Mission | Rationale |
| :--- | :--- | :--- |
| 1 | **M-021** | Foundation — graph quality unlocks everything |
| 2 | **M-023** | Resilience — provider diversification before heavy LLM use |
| 3 | **M-022** | Infrastructure — event bus now routes provider health correctly |
| 4 | **M-024** | Intelligence — Time Machine on clean graph |
| 5 | **M-025** | Autonomy — Strategic Engine with full context |
| 6 | **M-026** | Simulation — requires all prior layers |

**Revised sequence: 021 → 023 → 022 → 024 → 025 → 026**

---

## Semantic Links

- **depends_on:** [[MISSION-020]]
- **produces:** [[ADR-0048]]
- **governed_by:** [[Governance_Determinism]]
- **adr:** [[ADR-0048]]
