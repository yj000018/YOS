# Future Architecture Notes

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Context
This document captures validated architectural concepts that are scheduled for implementation in Y-OS v2. They are documented here to guide future development but are not active in v1.

## 1. Y-ORC (Y-OS Orchestrator)
Currently, agents are invoked manually or via simple sequential scripts. In v2, Y-ORC will be introduced as the central event-driven orchestrator.

## 2. Artifact-Centric Routing
Y-ORC will route work based on Artifact State Changes.
- *Example:* When Krishna changes the state of `Strategy Brief` to `Accepted`, Y-ORC detects the event and automatically invokes Ganesha.

## 3. Event-Driven Execution
The entire system moves from synchronous (Agent A calls Agent B and waits) to asynchronous (Agent A writes an artifact, Y-ORC wakes up Agent B).

## 4. State Machine Governance
CODO will encode the Y-OS Laws directly into Y-ORC. If an artifact violates a rule (e.g., Hanuman tries to deliver directly to CEO, bypassing Ganesha), Y-ORC will reject the state transition programmatically.

## 5. Agents as Plugins
In v2, the concept of an "Agent" becomes a replaceable plugin within the Capability Layer. The Layers remain the enduring architecture. Krishna could be replaced by a specialized fine-tuned model without altering the Executive Layer or the Artifact Layer.
