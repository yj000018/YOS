---
id: yos-lakshmi-dashboard-data-model-v1
title: Lakshmi Dashboard Data Model v1
type: governance_report
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Lakshmi
parent: '[[04_Governance_MOC]]'
tags:
- '#governance'
- '#yos'
source_branch: y-os-doctrine
canonical: true
executed_by:
- '[[Brahma]]'
---

# Dashboard Data Model v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
The Executive Dashboard requires a structured data model synthesized from the raw Artifact Registry.

## Data Model Structure

### 1. Global Metrics
- `active_missions`: Count of unique `Mission ID` where not all artifacts are `Archived`.
- `artifacts_in_draft`: Count of artifacts in `Draft`.
- `artifacts_in_review`: Count of artifacts in `Ready For Review`.
- `artifacts_rejected`: Count of artifacts in `Rejected`.

### 2. Mission Control (Array)
For each active Mission:
- `mission_id`: String
- `current_phase`: Deduced from the latest Accepted artifact type (e.g., if Execution Plan is Accepted but Architecture Package is Draft, phase is "Design").
- `bottleneck_role`: The `Review Owner` of the oldest artifact in `Ready For Review`, OR the `Producer` of the oldest artifact in `Draft`/`Rejected`.
- `health_status`: Green (moving), Yellow (stalled > 24h), Red (rejected or stalled > 72h).

### 3. Action Queue (Array)
- Filtered specifically for `Review Owner == 'CEO'` or `Producer == 'CEO'`.
- Categorized by: Decisions Required, Approvals Pending, Strategy Required.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
