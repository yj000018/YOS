---
id: yos-artifact-api-model-v1
title: Artifact API Model v1
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
executed_by:
- '[[Brahma]]'
---

# Artifact API Model v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
While the MVP uses Notion, agents interact with it programmatically. This defines the conceptual API model for Artifact operations.

## Core Methods

### `create_artifact(type, mission_id, producer, consumer, uri, parent_id=None)`
- **Action:** Initializes a new artifact in `Draft` state.
- **Returns:** `Artifact ID`

### `submit_for_review(artifact_id)`
- **Action:** Changes state from `Draft` to `Ready For Review`.

### `accept_artifact(artifact_id, notes="")`
- **Action:** Changes state to `Accepted`. Populates `Acceptance Notes`.

### `reject_artifact(artifact_id, reason)`
- **Action:** Changes state to `Rejected`. Populates `Rejection Notes`.

### `consume_artifact(artifact_id)`
- **Action:** Changes state to `Consumed`. Called when the downstream artifact is successfully created.

### `supersede_artifact(artifact_id)`
- **Action:** Changes state to `Superseded`.

### `archive_mission_artifacts(mission_id)`
- **Action:** Changes all artifacts associated with `mission_id` to `Archived`.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
