---
id: yos-adr-0015-architectural-layer-corrections
title: ADR-0015 Architectural Layer Corrections
type: adr
status: ACCEPTED
date: '2026-06-12'
owner: Brahma
parent: '[[02_ADR_MOC]]'
related_adrs:
- '[[ADR-0014]]'
tags:
- '#accepted'
- '#adr'
- '#memory'
- '#yos'
aliases:
- Architectural Layer Corrections
source_branch: y-os-doctrine
canonical: true
---

# ADR-0015: Architectural Layer Corrections

**Status:** Accepted
**Date:** 2026-06-12
**Author:** CEO (Yannick) / CODO (Saraswati)

## Context
Following the formalization of the Y-OS Org Map v2 (ADR-0014), an external architectural review identified two structural modeling errors. The Capability Layer incorrectly included organizational roles (Ganesha, Brahma, Hanuman), and the Memory Layer was defined by specific tool implementations (Notion, Git) rather than its core functions. These representational errors blurred the line between the enduring architecture of the system and its transient implementations.

## Decision
We formally adopt the v1.1 Architectural Corrections, updating the Layer Architecture Diagram to version 2.1.

Specifically, we mandate the following structural definitions:

1.  **Capability Layer:** Must exclusively contain replaceable execution substrates (e.g., Manus, Claude, MCP Servers, APIs). Roles are explicitly removed from this layer, as roles *consume* capabilities but are not capabilities themselves.
2.  **Memory Layer:** Must be defined by its four functional sub-layers (Capture, Recall, Canonical Memory, Archive). Specific tools (e.g., Notion, mem0, Obsidian) are recognized only as current implementations, not as architectural components.

Furthermore, we formally elevate the following statement to a foundational architectural principle, preserving it verbatim:

> **Roles are organizational interfaces.**
> **Layers are the enduring architecture.**

## Rationale
-   **Separation of Concerns:** Clearly distinguishing between who is responsible (Roles), what connects them (Artifacts), what does the work (Capabilities), and where knowledge lives (Memory) creates a cleaner, more resilient system model.
-   **Implementation Independence:** Defining the Memory Layer functionally ensures that future tool migrations (e.g., moving from Notion to a custom database) are treated as operational updates rather than architectural redesigns.
-   **Governance Clarity:** Removing roles from the Capability Layer reinforces that roles are governance structures, not software models.

## Consequences
-   The Layer Architecture Diagram v2.1 supersedes the previous version defined in ADR-0014.
-   All existing ADRs, Laws (including #10 and #11), roles, artifacts, and the Operational Value Chain are preserved without modification.
-   Future architectural discussions must strictly adhere to the principle that layers define functions, while tools and agents are transient implementations.
