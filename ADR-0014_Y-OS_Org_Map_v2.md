---
id: yos-adr-0014-y-os-org-map-v2
title: ADR-0014 Y-OS Org Map v2
type: adr
status: ACCEPTED
date: '2026-06-12'
version: v2
owner: Brahma
parent: '[[02_ADR_MOC]]'
tags:
- '#accepted'
- '#adr'
- '#memory'
- '#yos'
aliases:
- Y-OS Org Map v2
source_branch: y-os-doctrine
canonical: true
supersedes:
- '[[ADR-0014_Y-OS_Org_Map_v1]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
- '[[Saraswati]]'
- '[[Hanuman]]'
- '[[Krishna]]'
---

# ADR-0014: Y-OS Organizational Map v2

**Status:** Accepted
**Date:** 2026-06-12
**Author:** CEO (Yannick) / CODO (Saraswati)

## Context
Over the course of recent architectural sessions, Y-OS has formalized multiple roles (Brahma, Hanuman, Lakshmi), layers (Artifact Layer), and principles (Continuity Principle). These decisions are scattered across multiple ADRs and Agent Cards. To ensure architectural coherence and provide a single source of truth for future development, these concepts must be consolidated.

## Decision
We formally adopt the **Y-OS Org Map v2** as the canonical representation of the Y-OS v1 architecture.

This map consolidates:
1. The 6 official roles (Krishna, Ganesha, Brahma, Hanuman, Saraswati, Lakshmi).
2. The Operational Value Chain (Strategy → Planning → Design → Build → Delivery → Learning).
3. The Artifact Layer and its state machine.
4. The Layer Architecture (Executive, Artifact, Capability, Memory, Evolution).

## Rationale
- **Single Source of Truth:** Prevents architectural drift and contradictory interpretations of agent roles.
- **Onboarding:** Allows any new human or AI agent to understand the entire system by reading one master document.
- **Foundation for v2:** By clearly mapping the current state, we create a stable foundation for building Y-ORC and transitioning to an event-driven architecture.

## Consequences
- Any future changes to roles, reporting lines, or the Operational Value Chain must result in an update to the Y-OS Org Map.
- This document supersedes any older, informal diagrams or structural assumptions.
- No new roles or layers are introduced by this ADR; it is strictly a consolidation of validated decisions.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **executed_by:** [[Hanuman]]
- **executed_by:** [[Krishna]]
- **governed_by:** [[Lakshmi_Governance]]
- **supersedes:** [[ADR-0014_Y-OS_Org_Map_v1]]
