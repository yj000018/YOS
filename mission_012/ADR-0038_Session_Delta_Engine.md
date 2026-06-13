---
id: yos-adr-0038-session-delta-engine
title: ADR-0038 Session Delta Engine
type: adr
status: ACCEPTED
mission: MISSION-012
date: '2026-06-13'
owner: Brahma
parent: '[[03_Missions_MOC]]'
related_missions:
- '[[mission_012]]'
constitutional_articles:
- 'Article I: Artifact Primacy'
- 'Article V: Governance Before Autonomy'
tags:
- '#accepted'
- '#adr'
- '#ccr'
- '#session-delta'
- '#yos'
aliases:
- Session Delta Engine
- MISSION-012
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Session_Delta]]'
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Governance_Before_Autonomy]]'
---

# ADR-0038: Session Delta Engine

## Status
Accepted

## Context
MISSIONS 010-011 validated that raw session history degrades context quality and ROI. CCR Runtime v2 established the need for a Session Delta layer, but the specific architecture, schema, and lifecycle of this engine were undefined. We need a structured mechanism to preserve ephemeral session state (decisions, open questions, constraints) without accumulating conversational noise.

## Decision
We adopt the Session Delta Engine v1 architecture.

Key mandates:
1. **Incremental State:** Session history is replaced by a continuously updated YAML state object (the Delta).
2. **Event-Driven Compression:** State elements are flushed from the Delta the moment they are formalized into an Artifact.
3. **Archive Escalation:** Raw historical archives are never injected by default; they are accessible only via explicit capability escalation.
4. **Dual Purpose:** The final Session Delta serves as the permanent Archive Summary upon mission completion.

## Consequences
- **Positive:** Guarantees O(1) context growth for session history, regardless of conversation length. Eliminates hallucination risks associated with obsolete conversational paths. Provides a structured restart state for paused missions.
- **Negative:** Requires a dedicated state-patching mechanism (Phase 2) which introduces a minor background compute cost per turn.

## Compliance
- **Article I (Artifact Primacy):** Maintained. Delta flushes state into artifacts.
- **Article V (Governance Before Autonomy):** Maintained. Structured state allows deterministic governance checks on open questions and constraints.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Governance_Before_Autonomy]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Session_Delta]]
