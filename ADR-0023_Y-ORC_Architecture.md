---
id: yos-adr-0023-y-orc-architecture
title: ADR-0023 Y-ORC Architecture
type: adr
status: ACCEPTED
date: '2026-06-13'
owner: Brahma
parent: '[[02_ADR_MOC]]'
tags:
- '#accepted'
- '#adr'
- '#yos'
aliases:
- Y-ORC Architecture
source_branch: y-os-doctrine
canonical: true
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
---

# ADR-0023: Y-ORC Architecture

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  

## Purpose
Define how work moves through Y-OS and establish the execution coordination layer on top of the Control Plane.

## Decision
Y-ORC becomes the orchestration layer responsible for triggering execution based on registered state.

## Consequences
*   **Lakshmi remains read-only.**
*   **Control Plane remains governance.**
*   **Y-ORC becomes execution coordination.**
*   **Agents become pluggable workers.**


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
