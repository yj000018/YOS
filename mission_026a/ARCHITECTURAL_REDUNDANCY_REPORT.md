---
id: ARCHITECTURAL_REDUNDANCY_REPORT
title: 'Architectural Redundancy Report — MISSION-026A'
type: audit
date: '2026-06-14'
mission: MISSION-026A
---

# Architectural Redundancy Report

**Generated:** 2026-06-14 | **Mission:** MISSION-026A

---

## Summary

| Verdict | Count |
| :--- | :--- |
| KEEP | 2 |
| MERGE | 4 |
| DEPRECATE | 2 |

---

## Redundancies Identified

### RED-001 — DUPLICATED_COMPILER

**Verdict:** KEEP v4 only  
**Action:** `DEPRECATE v1/v2/v3 (keep as history)` | **Risk:** LOW | **Effort:** LOW

**Components:**
- kg_compiler_v1.py (M-013)
- kg_compiler_v2.py (M-015)
- kg_compiler_v3.py (M-019)
- kgc_v4_connectivity_engine.py (M-021)

### RED-002 — DUPLICATED_DASHBOARD_GENERATOR

**Verdict:** MERGE into single DashboardFactory  
**Action:** `MERGE` | **Risk:** MEDIUM | **Effort:** MEDIUM

**Components:**
- executive_advisor_dashboard_v1.py
- executive_simulation_dashboard_v1.py
- historical_navigation_dashboard_v1.py
- lineage_dashboard_generator_v1.py
- provider_observability_dashboard_v1.py

### RED-003 — DUPLICATED_LINEAGE_STRUCTURE

**Verdict:** Consolidate into single LineageRegistry  
**Action:** `MERGE` | **Risk:** LOW | **Effort:** MEDIUM

**Components:**
- mission_lineage_registry.json
- candidate_lineage_edges.json
- lineage_review_registry_v1.py
- event_lineage_tracker_v1.py

### RED-004 — DUPLICATED_GOVERNANCE_PATH

**Verdict:** Unify under GovernanceEngine v1  
**Action:** `MERGE` | **Risk:** MEDIUM | **Effort:** HIGH

**Components:**
- lakshmi_context_review_v1.py
- simulation_governance_v1.py
- lineage_validation_engine_v1.py
- output_validator_v1.py

### RED-005 — DUPLICATED_REGISTRY

**Verdict:** Keep all — different domains  
**Action:** `KEEP` | **Risk:** NONE | **Effort:** NONE

**Components:**
- odt_registry.json
- provider_registry.json
- simulation_registry.json
- event_registry.json
- capability_registry_v1.json

### RED-006 — DUPLICATED_CANVAS_GENERATOR

**Verdict:** MERGE into CanvasFactory  
**Action:** `MERGE` | **Risk:** LOW | **Effort:** LOW

**Components:**
- generate_canvas_019.py
- generate_visuals_021.py
- lineage_canvas_generator_v1.py
- executive_simulation_dashboard_v1.py (canvas)

### RED-007 — OVERLAPPING_HEALTH_MONITOR

**Verdict:** Keep all — different scopes (system/provider/org)  
**Action:** `KEEP` | **Risk:** NONE | **Effort:** NONE

**Components:**
- system_health_monitor_v1.py
- provider_health_monitor_v1.py
- organizational_observability_engine_v1.py

### RED-008 — UNUSED_MODULES

**Verdict:** DEPRECATE — superseded by CCR Runtime v2  
**Action:** `DEPRECATE` | **Risk:** LOW | **Effort:** LOW

**Components:**
- art_runtime_v1.py
- crt_runtime_v1.py
- yorc_runtime_v1.py (pre-M013 legacy)

---

## Semantic Links

- **produced_by:** [[MISSION-026A_Architecture_Freeze]]
