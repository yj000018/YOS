---
id: yos-artifact-routing-model-v1
title: Artifact Routing Model v1
type: artifact
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Manus Y-OS
tags:
- '#artifact'
- '#memory'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# 6. Artifact-Centric Routing Model v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Context
As Y-OS prepares for the development of Y-ORC (Y-OS Orchestrator), a fundamental architectural decision must be made regarding how work is routed through the organization.

## Evaluation: Agent-to-Agent vs. Artifact-Centric

### Model A: Agent-to-Agent Routing
In this model, Krishna finishes thinking and directly calls a function or API to wake up Ganesha, passing the context in the payload.
- **Pros:** Fast, synchronous.
- **Cons:** Brittle. If Ganesha crashes, the context is lost. Difficult to audit. Forces agents to know about each other's specific APIs and availability.

### Model B: Artifact-Centric Routing (State Change)
In this model, Krishna writes a Strategy Brief to the Artifact Layer (e.g., Notion or a database) and changes its state to `Ready For Review`. Y-ORC monitors the Artifact Layer. Seeing the state change, Y-ORC wakes up Ganesha and points him to the artifact.
- **Pros:** Extremely resilient. Agents are fully decoupled. Perfect audit trail. Allows asynchronous execution (Ganesha can process it tomorrow without Krishna waiting).
- **Cons:** Slightly higher latency (requires a database/Notion write and read).

## Recommendation

**Y-ORC must be built using Model B: Artifact-Centric Routing.**

Routing work via Artifact State Changes aligns perfectly with the core hypothesis of the Artifact Layer. Agents should not talk to agents. Agents should talk to artifacts.

**The Routing Logic:**
`If [Artifact Type] changes state to [Ready For Review], then invoke [Consumer Agent] with [Artifact URI].`

This makes Y-OS a true state machine, capable of infinite scalability, pause/resume functionality, and perfect memory retention.
