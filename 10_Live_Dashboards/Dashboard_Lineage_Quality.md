---
id: Dashboard_Lineage_Quality
title: 'Lineage Quality Dashboard — MISSION-022A'
type: dashboard
status: live
mission: MISSION-022A
generated_at: '2026-06-14 04:40 UTC'
tags:
  - '#dashboard'
  - '#lineage'
  - '#mission-022a'
aliases:
  - Lineage Quality Dashboard
---

# Lineage Quality Dashboard — MISSION-022A

> **Generated:** 2026-06-14 04:40 UTC  
> **Mission:** [[MISSION-022A_Legacy_Mission_Lineage_Recovery]]

---

## Coverage Metrics

| Metric | Before | After | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Mission Lineage Coverage** | 58.5% | **100.0%** | > 95% | ✅ PASS |
| **Legacy Missions Indexed** | — | **1** | 100% | ✅ |
| **Missions with Lineage** | — | **1** | — | — |
| **Remaining Gaps** | — | **0** | 0 | ✅ |
| **Total Inferred Edges** | — | **20** | — | — |
| **Validation Passed** | — | **YES** | YES | ✅ |

---

## Confidence Distribution

| Band | Count | % | Review Required |
| :--- | :--- | :--- | :--- |
| **HIGH** (≥ 0.90) | 2 | 10.0% | No |
| **MEDIUM** (0.75–0.90) | 9 | 45.0% | Yes |
| **LOW** (< 0.75) | 9 | 45.0% | Yes |

---

## Legacy Mission Status

| Mission | Lineage | ADR Links | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| MISSION-012A_Storage_Audit | Yes | 19 | 0 | ✅ Resolved |

---

## Navigation

- [[Mission_Lineage_Recovery]] — Recovery Canvas
- [[YOS_Mission_Lineage]] — Mission Lineage Canvas
- [[Dashboard_Graph_Quality]] — Graph Quality Dashboard
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-022A_Legacy_Mission_Lineage_Recovery]]
- **measured_by:** [[legacy_lineage_recovery_engine_v1]]
- **published_to:** [[00_Y-OS_Home]]
