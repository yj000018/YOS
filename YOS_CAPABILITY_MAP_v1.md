---
id: YOS_CAPABILITY_MAP_v1
title: 'Y-OS Capability Map v1'
type: capability_map
status: ACTIVE
date: '2026-06-14'
mission: MISSION-026A
tags:
  - '#capability'
  - '#architecture'
  - '#yos'
---

# Y-OS Capability Map v1

**Generated:** 2026-06-14 | **Mission:** MISSION-026A | **Total:** 28 capabilities

---

## Classification Summary

| Classification | Count | Description |
| :--- | :--- | :--- |
| **CORE** | 10 | Non-negotiable — system fails without these |
| **IMPORTANT** | 10 | High value — significant degradation if absent |
| **OPTIONAL** | 5 | Useful — graceful degradation if absent |
| **EXPERIMENTAL** | 3 | Proposed or deferred — not yet operational |

---

## CORE Capabilities

| ID | Capability | Mission | Owner | Usage | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CAP-001 | Constitutional Governance | M-001→M-012 | Lakshmi | every_session | 10/10 |
| CAP-002 | ADR Decision Registry | M-001→M-026A | Brahma | every_mission | 10/10 |
| CAP-003 | Knowledge Graph Compilation (KGC v4) | M-013→M-021 | Brahma | per_mission | 9/10 |
| CAP-004 | CCR Context Routing (MODE-B/D/E) | M-016 | Brahma | every_execution | 9/10 |
| CAP-005 | Live Worker Execution | M-017 | Hanuman | every_execution | 9/10 |
| CAP-006 | Multi-Worker Pipeline Orchestration | M-018 | Brahma | per_pipeline | 9/10 |
| CAP-007 | Artifact Registry & Lineage | M-017 | Lakshmi | every_execution | 9/10 |
| CAP-008 | Governance Review (Lakshmi) | M-016 | Lakshmi | every_execution | 10/10 |
| CAP-009 | Git Version Control | M-013 | Brahma | every_mission | 9/10 |
| CAP-010 | Obsidian Knowledge Navigation | M-013→M-015 | Saraswati | daily | 8/10 |

## IMPORTANT Capabilities

| ID | Capability | Mission | Owner | Usage | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CAP-011 | Provider Diversification & Routing | M-023 | Brahma | every_execution | 8/10 |
| CAP-012 | Event Bus (44 types, 24 rules) | M-022 | Brahma | per_event | 7/10 |
| CAP-013 | Organizational Digital Twin | M-019 | Ganesha | per_mission | 8/10 |
| CAP-014 | System Observability & EIS | M-020 | Lakshmi | continuous | 8/10 |
| CAP-015 | ODT Time Machine | M-024 | Brahma | on_demand | 7/10 |
| CAP-016 | Strategic Recommendation Engine | M-025 | Ganesha | per_review | 8/10 |
| CAP-017 | Executive Simulation Layer | M-026 | Ganesha | per_decision | 8/10 |
| CAP-018 | Living Memory Pipeline | M-016 | Saraswati | per_session | 7/10 |
| CAP-019 | Semantic Connectivity Layer (KGC v4) | M-021 | Brahma | per_mission | 7/10 |
| CAP-020 | Legacy Lineage Recovery | M-022A | Brahma | on_demand | 6/10 |

## OPTIONAL Capabilities

| ID | Capability | Mission | Owner | Usage | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CAP-021 | Dataview Dashboards (14) | M-015→M-026 | Saraswati | on_demand | 6/10 |
| CAP-022 | Canvas Visual Maps (25) | M-015→M-026 | Saraswati | on_demand | 5/10 |
| CAP-023 | Concept Nodes (39) | M-014→M-015 | Saraswati | on_demand | 6/10 |
| CAP-024 | Provider Cost Optimizer | M-023 | Lakshmi | per_execution | 6/10 |
| CAP-025 | Weekly Review Generator | M-020 | Ganesha | weekly | 5/10 |

## EXPERIMENTAL Capabilities

| ID | Capability | Mission | Owner | Usage | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CAP-026 | Excalidraw Visual Maps | M-015 (deferred) | Saraswati | never | 4/10 |
| CAP-027 | Notion ODT Sync | M-025 (proposed) | Brahma | never | 7/10 |
| CAP-028 | Live Gemini API Validation | M-031 (proposed) | Brahma | never | 7/10 |

---

## Semantic Links

- **governed_by:** [[Y-OS_Constitution_v1]]
- **produced_by:** [[MISSION-026A_Architecture_Freeze]]
- **references:** [[YOS_SYSTEM_ARCHITECTURE_v1]]
