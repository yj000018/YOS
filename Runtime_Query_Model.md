---
id: yos-runtime-query-model
title: Runtime Query Model
type: runtime_spec
status: ACCEPTED
date: '2026-06-13'
owner: Manus Y-OS
parent: '[[05_Runtime_MOC]]'
tags:
- '#accepted'
- '#lineage'
- '#runtime'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Runtime Query Model

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Context

Lakshmi and Y-ORC require specific, optimized queries to interact with the Artifact Registry. This document defines the canonical query patterns required by the runtime engines.

## 2. Query Definitions

### `get_all_active_missions()`
Retrieves all unique `Mission ID`s where at least one artifact is not `Archived` or `Superseded`.
**Usage:** Used by Lakshmi to build the Mission Control dashboard.

### `get_artifact_chain(mission_id)`
Retrieves all artifacts matching the given `Mission ID`, sorted by `Created Date`.
**Usage:** Used to reconstruct the full lineage graph of a specific mission.

### `get_pending_reviews()`
Retrieves all artifacts where `Status` = `Ready For Review`.
**Usage:** Used by Lakshmi's Open Loops Engine to detect review bottlenecks.

### `get_stalled_artifacts(threshold_hours)`
Retrieves artifacts where `Updated Date` is older than `threshold_hours` AND `Status` is not `Archived`, `Consumed`, or `Superseded`.
**Usage:** Used by Lakshmi to detect execution bottlenecks.

### `get_open_loops()`
Retrieves all artifacts where `Open Loop Flag` = `True`.
**Usage:** Used by Lakshmi to populate the CEO Action Queue.

### `get_broken_lineage()`
Retrieves all artifacts where `Status` = `Accepted` AND `Child Artifacts` is empty AND `Artifact Type` is not a terminal type (e.g., Learning Report).
**Usage:** Used by Y-ORC to detect when an agent has failed to pick up the next step in the chain.

### `get_recently_accepted_artifacts(hours)`
Retrieves artifacts where `Accepted Date` is within the last `hours`.
**Usage:** Used by Lakshmi to populate the "Victories" section of the CEO Briefing.

### `get_artifacts_missing_required_fields()`
Retrieves artifacts that violate the Validation Rules (e.g., missing `Mission ID`, or `Rejected` without `Rejection Notes`).
**Usage:** Used by Saraswati (CODO) for organizational health audits.
