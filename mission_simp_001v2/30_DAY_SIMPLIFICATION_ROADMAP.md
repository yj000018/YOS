---
id: 30_DAY_SIMPLIFICATION_ROADMAP
title: Y-OS 30-Day Simplification Roadmap
date: 2026-06-14
tags: [roadmap, simplification, 30-day]
---

# 30-Day Simplification Roadmap

> **Goal: 71 → 28 active modules. 26 → 3 canvas maps. 17 → 3 dashboards.**  
> No new capabilities. No new missions. Pure reduction.

---

## Week 1 — Quick Wins (< 3h total)

**Objective:** Remove the obvious dead weight. Zero risk. Immediate clarity.

| Day | Task | Effort | Modules removed |
|:---|:---|:---|---:|
| 1 | Archive kg_compiler_v3 | 5min | 1 |
| 1 | Archive gemini_benchmark_runner_v1 | 5min | 1 |
| 1 | Archive legacy_lineage_recovery_engine_v1 | 5min | 1 |
| 2 | Move simulation layer → /experimental/ | 30min | 6 |
| 2 | Move time_machine layer → /experimental/ | 30min | 7 |
| 3 | Archive 4 dashboard generators → keep 1 | 30min | 3 |
| 3 | Archive strategic_memory + simulation_memory | 10min | 2 |
| 4 | Archive odt_live_update + checkpoint_rollback + artifact_supersession | 15min | 3 |
| 4 | Archive organizational_alert + weekly_review | 10min | 2 |
| 5 | Archive event_observability + lineage_canvas + lineage_dashboard | 15min | 3 |

**Week 1 result: 71 → 42 active modules (-41%)**

---

## Week 2 — Structure Cleanup (< 5h total)

**Objective:** Flatten runtime/, consolidate visual assets, archive legacy mission dirs.

| Day | Task | Effort |
|:---|:---|:---|
| 8 | Create runtime/core/, runtime/optional/, runtime/experimental/ | 1h |
| 9 | Move modules to correct layer folders | 1h |
| 10 | Consolidate 26 canvas maps → 3 canonical | 2h |
| 11 | Consolidate 17 dashboards → 3 canonical | 1h |
| 12 | Archive mission_001–012 dirs → /archive/missions/ | 30min |

**Week 2 result: Structure clear. Navigation burden -80%.**

---

## Week 3 — Merges (< 8h total)

**Objective:** Eliminate duplicate functionality via targeted merges.

| Day | Task | Effort | Modules saved |
|:---|:---|:---|---:|
| 15 | MERGE validation_queue + lineage_validation → output_validator_v2 | 2h | 2 |
| 16 | MERGE cost_tracker + provider_cost_optimizer → cost_tracker_v2 | 1h | 1 |
| 17 | MERGE event_lineage_tracker → execution_trace_logger_v2 | 1h | 1 |
| 18 | MERGE lineage_review_registry → artifact_registry_v3 | 1h | 1 |
| 19 | MERGE recommendation_prioritization + roadmap_gen → strategic_rec_v2 | 2h | 2 |

**Week 3 result: 42 → 35 active modules (-17%)**

---

## Week 4 — Intelligence Merges + Final Audit (< 5h total)

**Objective:** Merge remaining overlaps, run final audit, update docs.

| Day | Task | Effort | Modules saved |
|:---|:---|:---|---:|
| 22 | MERGE gemini_runtime_validation → provider_router_v2 | 2h | 1 |
| 23 | MERGE org_observability → system_health_monitor_v2 | 2h | 1 |
| 25 | Update YOS_SYSTEM_ARCHITECTURE_v1 → v2 | 1h | — |
| 26 | Update 00_Y-OS_Home.md with new structure | 30min | — |
| 28 | Run final audit: active module count, EIS, complexity score | 30min | — |
| 30 | Commit + push final simplified corpus | 30min | — |

**Week 4 result: 35 → 28 active modules**

---

## Final State — Day 30

| Metric | Start | Day 30 | Reduction |
|:---|---:|---:|---:|
| Active modules | 71 | **28** | **61%** |
| Canvas maps | 26 | **3** | **88%** |
| Dashboards | 17 | **3** | **82%** |
| Mission dirs (active) | 36 | **24** | **33%** |
| Conceptual layers | 14 | **5** | **64%** |

---

## Success Criteria

- [ ] Active modules ≤ 30
- [ ] All CORE modules daily-use
- [ ] 3 canonical canvas maps
- [ ] 3 canonical dashboards
- [ ] /experimental/ folder exists with simulation + time_machine
- [ ] /archive/ folder exists with all archived modules
- [ ] runtime/ organized by layer
- [ ] Simplicity Guardrail ADR committed
- [ ] No new capabilities added

---

## What Does NOT Change

- Constitution (FROZEN)
- All ADRs (preserved)
- All mission reports (preserved)
- All artifacts (preserved)
- GitHub history (preserved)
- Doctrine corpus (preserved)
- Knowledge graph (preserved)

**The corpus shrinks. The doctrine survives.**
