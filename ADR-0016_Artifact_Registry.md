---
id: yos-adr-0016-artifact-registry
title: ADR-0016 Artifact Registry
type: adr
status: ACCEPTED
date: '2026-06-12'
owner: Brahma
parent: '[[02_ADR_MOC]]'
related_adrs:
- '[[ADR-0012]]'
tags:
- '#accepted'
- '#adr'
- '#lineage'
- '#yos'
aliases:
- Artifact Registry
source_branch: y-os-doctrine
canonical: true
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
---

# ADR-0016: Artifact Registry

**Status:** Accepted
**Date:** 2026-06-12
**Author:** Chief Architect (Brahma)

## Context
ADR-0012 established that Y-OS is an artifact-centric organization where agents communicate via persistent artifacts rather than direct agent-to-agent messaging. To operationalize this, a concrete system of record is required to track the existence, state, and lineage of all artifacts.

## Decision
We formally adopt the **Artifact Registry MVP** as the canonical system of record for all Y-OS artifacts.

The MVP will be implemented using a Notion Database with a strict schema including: Artifact ID, Type, Mission ID, Producer, Consumer, Status, Version, Dates, Lineage (Parent/Child), URI, and Notes.

We mandate the strict use of the 7-state Artifact State Machine: `Draft`, `Ready For Review`, `Accepted`, `Rejected`, `Consumed`, `Superseded`, and `Archived`.

## Rationale
- **Single Source of Truth:** Centralizing artifact metadata prevents "lost work" and ensures all roles have a unified view of the system state.
- **Decoupled Architecture:** Storing URIs rather than raw content in the Registry allows Y-OS to handle artifacts of any size or format (code, PDFs, videos) without bloating the database.
- **Foundation for Orchestration:** The standardized State Machine and Query Model provide the exact programmatic hooks required to build Y-ORC (the event-driven orchestrator) in the future.

## Consequences
- No artifact is considered official unless it exists in the Artifact Registry.
- Agents must be programmed (or prompted) to query the Registry for their inputs and log their outputs in the Registry.
- The ECO (Lakshmi) will rely entirely on the Registry to generate the Executive Dashboard and Open Loops Register.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
