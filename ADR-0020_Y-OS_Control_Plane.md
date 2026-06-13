# ADR-0020: Y-OS Control Plane

**Status:** Accepted  
**Date:** 2026-06-13  
**Owner:** Chief Architect (Brahma)  

## Context
Y-OS has evolved from a theoretical organizational model into an executable system with the introduction of the Artifact Registry, Lineage Model, and Lakshmi Runtime. We need to formally define this new architectural layer to prevent confusion with future orchestration components (Y-ORC) and to establish the boundaries of observability.

## Decision
We formally define the **Y-OS Control Plane** as the operational governance layer of the system. 

The Control Plane consists of:
1.  Artifact Registry
2.  Artifact Lineage
3.  Mission Graph Engine
4.  Open Loop Engine
5.  Lakshmi Runtime
6.  CEO Briefing

The Control Plane is strictly observational and analytical. It reconstructs state and detects anomalies, but it does not execute work or trigger agents.

## Consequences
*   **Positive:** Establishes a clear separation of concerns between observability (Control Plane) and execution routing (Y-ORC).
*   **Positive:** Formalizes the concept of "Governance Signals" (Open Loops) as the primary output of the observability layer.
*   **Constraint:** Y-ORC must be designed to consume the state and signals provided by the Control Plane, rather than maintaining its own separate state machine. The Registry remains the single source of truth.
