---
id: yos-artifact-schema-v1.1-patch
title: Artifact Schema v1.1 Patch
type: artifact
status: OFFICIAL
date: '2026-06-12'
version: v1.1
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
- '[[Lakshmi]]'
- '[[Hanuman]]'
---

# Artifact Schema v1.1 (Patch)

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
Following the review of the Artifact Registry MVP, two structural omissions were identified that prevent ECO (Lakshmi) from accurately measuring state transition delays and properly routing review requests.

## Schema Additions

The following properties are formally added to the Artifact Schema:

| Field | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| **Review Owner** | Select | The specific role responsible for reviewing the artifact when it is in the `Ready For Review` state. This may differ from the Consumer (e.g., Brahma produces for Hanuman, but Hanuman is also the Review Owner to accept the architecture). | Yes |
| **Accepted Date** | Date | Timestamp when the artifact transitioned to `Accepted`. Used to measure review delay. | No (Auto-filled on transition) |
| **Consumed Date** | Date | Timestamp when the artifact transitioned to `Consumed`. Used to measure execution delay. | No (Auto-filled on transition) |
| **Archived Date** | Date | Timestamp when the artifact transitioned to `Archived`. | No (Auto-filled on transition) |

## Impact on Artifact Registry
The Notion Database will be updated to include these four new properties. The Artifact API Model is implicitly updated to populate these timestamp fields during state transitions.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Hanuman]]
- **governed_by:** [[Lakshmi_Governance]]
