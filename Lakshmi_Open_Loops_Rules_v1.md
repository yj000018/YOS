---
id: yos-lakshmi-open-loops-rules-v1
title: Lakshmi Open Loops Rules v1
type: governance_report
status: ACCEPTED
date: '2026-06-13'
version: v1
owner: Lakshmi
parent: '[[04_Governance_MOC]]'
tags:
- '#accepted'
- '#governance'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Saraswati]]'
---

# Open Loops Detection Rules v1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Lineage Integrity Loops

| Rule ID | Name | Condition | Severity | Assignee |
|---|---|---|---|---|
| L-01 | Missing Parent | Artifact is not a Strategy Brief AND `Parent Artifact ID` is null. | P1 | Producer |
| L-02 | Missing Child | Artifact is `Consumed` AND `Child Artifact IDs` is empty AND Artifact is not Terminal. | P1 | Consumer |
| L-03 | Orphan Artifact | Artifact has no `Mission ID`. | P1 | Producer |

## 2. Velocity Loops

| Rule ID | Name | Condition | Severity | Assignee |
|---|---|---|---|---|
| V-01 | Stalled Review | Artifact is `Ready For Review` for > 48 hours. | P2 | Review Owner |
| V-02 | Stalled Execution | Artifact is `Accepted` for > 72 hours AND has no Children. | P2 | Consumer |
| V-03 | Abandoned Draft | Artifact is `Draft` for > 7 days. | P3 | Producer |
| V-04 | Stalled Rework | Artifact is `Rejected` for > 48 hours without a new version. | P2 | Producer |

## 3. Mission Health Loops

| Rule ID | Name | Condition | Severity | Assignee |
|---|---|---|---|---|
| M-01 | Blocked Mission | Mission Status is `Blocked`. | P1 | CEO / Ganesha |
| M-02 | Missing Learning | Mission Status is `Completed` but lacks a `Learning Report`. | P2 | Saraswati |


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Saraswati]]
