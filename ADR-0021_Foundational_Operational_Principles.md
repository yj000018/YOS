# ADR-0021: Foundational Operational Principles

**Status:** Accepted  
**Date:** 2026-06-13  
**Owner:** CODO (Saraswati)  

## Context
During the development of Y-OS v1, including the Artifact Layer, Artifact Registry, Lineage Model, and Lakshmi Runtime, a series of profound architectural realizations occurred. We discovered that Y-OS is fundamentally not an agent-centric system, but an artifact-centric system. To ensure that future development (such as Y-ORC) aligns with this philosophy, these discoveries must be formally codified into the permanent doctrine of Y-OS.

## Decision
We formally adopt the **Foundational Operational Principles** as first-class Y-OS doctrine. 

These principles dictate that:
1.  **Execution is transient; State is persistent.** (The Continuity Doctrine)
2.  **Y-OS is an Artifact-Centric System.** (The Architectural Inversion)
3.  **The Operational Chain is immutable:** Agents produce Artifacts -> Artifacts preserve State -> Registry records Truth -> Lineage preserves Causality -> Lakshmi provides Visibility -> Open Loops generate Governance Signals.

We also formally define the **Layer Model** (Execution, State, Truth, Causality, Visibility, Governance, Orchestration) as the canonical representation of the system's structure.

## Consequences
*   **Positive:** Provides a clear, philosophical North Star for all future Y-OS development.
*   **Positive:** Ensures that future engineers and architects understand *why* the system is designed this way, preventing regression into agent-centric anti-patterns.
*   **Positive:** Guarantees organizational continuity regardless of underlying technological shifts in the Capability Layer.
*   **Constraint:** Any future component (especially Y-ORC) must be designed to interact with the Artifact Registry and respect the Lineage Model, rather than bypassing them for direct agent-to-agent interaction.

## Recommendation for Integration
These principles should be linked directly from the `Y-OS_Vision_First_Principles.md` and the `Y-OS_Org_Map_v2.md` to ensure they are highly visible to anyone studying the system architecture.
