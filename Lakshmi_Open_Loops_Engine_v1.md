---
id: yos-lakshmi-open-loops-engine-v1
title: Lakshmi Open Loops Engine v1
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
---

# Open Loops Engine v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
The Open Loops Engine is the core algorithmic component of Lakshmi. It scans the Artifact Registry to identify stalled work, missing handoffs, and governance violations.

## Detection Algorithms

### 1. The Review Bottleneck
- **Trigger:** Artifact Status == `Ready For Review`.
- **Condition:** `Current Date` - `Updated Date` > 24 hours.
- **Loop Created:** Type `Review`, Assigned to `Review Owner`.

### 2. The Execution Bottleneck
- **Trigger:** Artifact Status == `Accepted`.
- **Condition:** `Current Date` - `Accepted Date` > 48 hours AND no Child Artifact exists.
- **Loop Created:** Type `Execution`, Assigned to `Consumer`.

### 3. The Rework Bottleneck
- **Trigger:** Artifact Status == `Rejected`.
- **Condition:** `Current Date` - `Updated Date` > 24 hours.
- **Loop Created:** Type `Rework`, Assigned to `Producer`.

### 4. The Missing Strategy
- **Trigger:** Mission ID exists, but no `Strategy Brief` exists.
- **Condition:** Immediate.
- **Loop Created:** Type `Missing Artifact`, Assigned to `Krishna`.

## Output
The engine generates a list of Open Loop objects, which are written to the Open Loops Register Notion Database. When the underlying condition is resolved in the Artifact Registry, Lakshmi automatically closes the Open Loop.
