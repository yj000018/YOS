---
id: Dashboard_Event_Bus
title: 'Live Event Bus Dashboard — MISSION-022'
type: dashboard
status: live
mission: MISSION-022
generated_at: '2026-06-14 05:03 UTC'
tags:
  - '#dashboard'
  - '#event-bus'
  - '#mission-022'
aliases:
  - Event Bus Dashboard
---

# Live Event Bus Dashboard — MISSION-022

> **Generated:** 2026-06-14 05:03 UTC  
> **Mission:** [[MISSION-022_Live_Event_Bus]]

---

## Event Metrics

| Metric | Value |
| :--- | :--- |
| **Total Published** | 9 |
| **Total Delivered** | 19 |
| **Delivery Rate** | 211.1% |
| **Failed Deliveries** | 0 |
| **DLQ Size** | 0 |
| **Persisted Events** | 9 |

---

## Events by Category

| Category | Count |
| :--- | :--- |
| ADR | 1 |
| ARTIFACT | 1 |
| DASHBOARD | 1 |
| GOVERNANCE | 1 |
| GRAPH | 1 |
| MEMORY | 1 |
| MISSION | 1 |
| PIPELINE | 1 |
| PROVIDER | 1 |

---

## Routing Log (last 8)

| Event Type | Targets |
| :--- | :--- |
| MISSION_COMPLETED | odt_update_engine, graph_compiler, dashb |
| PROVIDER_FAILED | failover_engine, health_monitor, dashboa |
| ARTIFACT_CREATED | artifact_registry, lineage_tracker, grap |
| GOVERNANCE_APPROVED | dashboard_refresh, artifact_registry |
| ADR_ACCEPTED | graph_compiler, kg_update, dashboard_ref |
| GRAPH_QUALITY_UPDATED | dashboard_refresh |
| DASHBOARD_UPDATED |  |
| PIPELINE_COMPLETED | odt_update_engine, artifact_registry |

---

## Replay Engine

| Metric | Value |
| :--- | :--- |
| Events Replayed | 9 |
| Replay Duration | 0.0ms |
| State Reconstructed | ✅ |
| Missions | 1 |
| ADRs | 1 |
| Artifacts | 1 |

## Navigation

- [[Event_Bus_Architecture]] — Event Bus Canvas
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Providers]] — Provider Dashboard
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-022_Live_Event_Bus]]
- **published_to:** [[00_Y-OS_Home]]
