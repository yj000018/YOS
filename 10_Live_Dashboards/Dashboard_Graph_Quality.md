---
id: Dashboard_Graph_Quality
title: 'Graph Quality Dashboard — Y-OS KGC v4'
type: dashboard
status: live
mission: MISSION-021
generated_at: '2026-06-14 04:26 UTC'
tags:
  - '#dashboard'
  - '#graph'
  - '#kgc-v4'
  - '#mission-021'
aliases:
  - Graph Quality Dashboard
---

# Graph Quality Dashboard — Y-OS KGC v4

> **Generated:** 2026-06-14 04:26 UTC  
> **Mission:** [[MISSION-021_Semantic_Connectivity_Layer]]  
> **Engine:** [[kgc_v4_connectivity_engine]]

---

## Core Metrics

| Metric | Before (M-020) | After (M-021) | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Orphan Rate** | 13.1% | **7.1%** | < 15% | ✅ PASS |
| **Orphan Count** | 65 | **35** | — | — |
| **Graph Quality Score** | 90.8 | **100** | > 80 | ✅ PASS |
| **Total Nodes** | 496 | **496** | — | — |
| **Total Edges** | 2118 | **4056** | — | — |
| **Connectivity Score** | 27.8% | **39.3%** | — | — |
| **Digital Thread Coverage** | 86.7% | **92.9%** | > 90% | ✅ PASS |
| **Lineage Coverage** | 0.0% | **58.5%** | > 95% | ⚠️ PARTIAL |
| **EIS Score** | 87.5 | **95.3** | > 92 | ✅ PASS |
| **Relationship Types** | 29 | **11** | — | — |

---

## Improvement Summary

| Metric | Delta |
| :--- | :--- |
| Orphans resolved | **30** |
| Edges added | **1938** |
| Files enriched (body wikilinks) | **21** |
| Digital Thread complete | **YES** |

---

## Test Results

| Test | Description | Result |
| :--- | :--- | :--- |
| A | Orphan Reduction < 15% | PASS |
| B | Graph Quality > 80 | PASS |
| C | Digital Thread ≥ 90% | PASS |
| D | Mission Lineage ≥ 95% | PARTIAL (lineage 58.5% < 95%) |
| E | Canvas Generation | PASS |
| F | Dashboard Generation | PASS |
| G | EIS > 92 | PASS |

---

## Dataview Queries

```dataview
TABLE orphan_rate, graph_quality_score, eis_score
FROM "mission_021"
WHERE type = "report"
SORT file.mtime DESC
```

```dataview
LIST
FROM "concepts"
WHERE is_orphan = false
SORT file.name ASC
```

---

## Navigation

- [[YOS_Digital_Thread]] — Digital Thread Canvas
- [[YOS_Mission_Lineage]] — Mission Lineage Canvas
- [[YOS_Artifact_Lineage]] — Artifact Lineage Canvas
- [[YOS_Graph_Health]] — Graph Health Canvas
- [[00_Y-OS_Home]] — Home MOC
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit

## Semantic Links

- **reports_to:** [[MISSION-021_Semantic_Connectivity_Layer]]
- **measured_by:** [[kgc_v4_connectivity_engine]]
- **published_to:** [[00_Y-OS_Home]]
