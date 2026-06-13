---
id: yos-relationship-to-y-orc
title: Relationship to Y-ORC
type: unknown
status: ACCEPTED
date: '2026-06-13'
owner: Manus Y-OS
tags:
- '#accepted'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Relationship to Y-ORC

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Distinction

The Control Plane and the Orchestrator (Y-ORC) are two distinct layers of the Y-OS architecture.

*   **Control Plane:** The sensory nervous system. It observes state, reconstructs reality, and detects anomalies. It is read-only regarding execution.
*   **Y-ORC:** The motor nervous system. It triggers actions, routes tasks to agents, and manages execution flow. It is read-write.

## 2. Current State vs Future State

**Current State (v1):** The Control Plane is fully operational. It provides visibility to the CEO via Lakshmi. However, execution handoffs (e.g., Krishna telling Ganesha to start planning) are manual or assumed.

**Future State (v2):** Y-ORC will be built *on top* of the Control Plane. 

## 3. The Orchestration Loop

When Y-ORC is implemented, the loop will be:

1.  Agent updates Artifact Registry.
2.  Control Plane detects state change (e.g., Status: "Draft" -> "Ready For Review").
3.  Control Plane emits event.
4.  **Y-ORC catches event.**
5.  **Y-ORC reads Registry to find `Review Owner`.**
6.  **Y-ORC triggers the Review Owner agent.**

## 4. Architectural Dependency

Y-ORC cannot exist without the Control Plane. Y-ORC requires a deterministic, observable state machine to function. By building the Artifact Registry, Lineage, and Open Loop Engine first, we have established the necessary foundation for automated orchestration.
