---
id: yos-organization-health-kpi-framework-v1
title: Organization Health KPI Framework v1
type: artifact
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Manus Y-OS
tags:
- '#artifact'
- '#yos'
source_branch: y-os-doctrine
canonical: true
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
- '[[Saraswati]]'
- '[[Hanuman]]'
---

# Organization Health KPI Framework v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Purpose
To define the metrics Lakshmi uses to monitor the operational health of Y-OS, ensuring the organization runs efficiently and adheres to its design.

## Key Performance Indicators

| KPI Name | Description | Target State | Escalation Trigger |
| :--- | :--- | :--- | :--- |
| **Artifact Velocity** | The average time an artifact spends in `Draft` or `Ready For Review`. | < 2 hours per phase. | Artifact stalled > 24 hours. |
| **Handoff Rejection Rate** | The percentage of artifacts rejected by the Consumer. | < 10% | > 20% rejection rate on a specific edge (e.g., Brahma → Hanuman). |
| **Execution Cost Variance** | The difference between Ganesha's estimated cost/tokens and Hanuman's actual build cost. | ± 15% | Actual cost > 150% of estimate. |
| **Governance Compliance** | The percentage of missions that strictly follow the OVC without bypassing phases. | 100% | Any bypass of Strategy or Design phases. |
| **Open Loop Resolution Time** | The average time it takes to close an item on the Open Loops Register. | < 48 hours for non-strategic items. | Items open > 7 days. |

## Monitoring Mechanism
Lakshmi continuously calculates these KPIs by parsing the metadata of the Artifact Layer. Anomalies are surfaced on the ECO Dashboard and included in the CEO Briefing.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **executed_by:** [[Hanuman]]
- **governed_by:** [[Lakshmi_Governance]]
