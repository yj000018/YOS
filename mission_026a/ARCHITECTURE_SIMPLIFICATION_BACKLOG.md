---
id: ARCHITECTURE_SIMPLIFICATION_BACKLOG
title: 'Architecture Simplification Backlog — MISSION-026A'
type: backlog
date: '2026-06-14'
mission: MISSION-026A
---

# Architecture Simplification Backlog

**Generated:** 2026-06-14 | **Mission:** MISSION-026A | **Total:** 20 opportunities

---

## Priority Matrix

| ID | Opportunity | Effort | Risk | Impact | Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SIMP-001 | Reorganize runtime/ into sub-packages | MEDIUM | LOW | HIGH | ⭐⭐⭐ |
| SIMP-002 | Unify governance into GovernanceEngine v1 | HIGH | MEDIUM | HIGH | ⭐⭐⭐ |
| SIMP-003 | DashboardFactory v1 (replace 5 generators) | MEDIUM | LOW | MEDIUM | ⭐⭐⭐ |
| SIMP-004 | CanvasFactory v1 (replace 4 scripts) | LOW | LOW | MEDIUM | ⭐⭐⭐ |
| SIMP-005 | Archive KGC v1/v2/v3 (keep only v4) | LOW | LOW | MEDIUM | ⭐⭐⭐ |
| SIMP-006 | MissionRunner base class | MEDIUM | LOW | MEDIUM | ⭐⭐ |
| SIMP-007 | LineageEngine v1 (consolidate 4 lineage systems) | HIGH | MEDIUM | HIGH | ⭐⭐⭐ |
| SIMP-008 | Provider plugin pattern (ProviderAdapter) | MEDIUM | LOW | MEDIUM | ⭐⭐ |
| SIMP-009 | Registry schema v1 + central index | LOW | LOW | MEDIUM | ⭐⭐ |
| SIMP-010 | Fix ADR-0017 ID collision | LOW | LOW | LOW | ⭐ |
| SIMP-011 | Add __init__.py to runtime/ | LOW | LOW | LOW | ⭐ |
| SIMP-012 | Remove __pycache__ from Git | LOW | LOW | LOW | ⭐ |
| SIMP-013 | Add .gitignore for *.pyc / __pycache__ | LOW | LOW | LOW | ⭐ |
| SIMP-014 | Budget cap enforcement in CostTracker | LOW | LOW | HIGH | ⭐⭐⭐ |
| SIMP-015 | CircuitBreaker in PipelineOrchestrator | MEDIUM | MEDIUM | HIGH | ⭐⭐⭐ |
| SIMP-016 | Consolidate run_mission_*.py test harness | MEDIUM | LOW | MEDIUM | ⭐⭐ |
| SIMP-017 | Deprecate art_runtime_v1, crt_runtime_v1, yorc_runtime_v1 | LOW | LOW | LOW | ⭐ |
| SIMP-018 | Add automated recovery hook to CheckpointRollback | MEDIUM | MEDIUM | HIGH | ⭐⭐⭐ |
| SIMP-019 | Validate Gemini API live (MISSION-031) | LOW | LOW | HIGH | ⭐⭐⭐ |
| SIMP-020 | Add Notion ODT Sync (MISSION-027 proposed) | HIGH | MEDIUM | HIGH | ⭐⭐ |

---

## Quick Wins (effort LOW, impact MEDIUM+)

1. **SIMP-004** — CanvasFactory v1 (1 day)
2. **SIMP-005** — Archive KGC v1/v2/v3 (2 hours)
3. **SIMP-009** — Registry schema + index (1 day)
4. **SIMP-012/013** — .gitignore cleanup (30 min)
5. **SIMP-014** — Budget cap enforcement (2 hours)
6. **SIMP-019** — Gemini live validation (1 day)

---

## Semantic Links

- **produced_by:** [[MISSION-026A_Architecture_Freeze]]
- **references:** [[COMPLEXITY_DEBT_REPORT]]
- **references:** [[ARCHITECTURAL_REDUNDANCY_REPORT]]
