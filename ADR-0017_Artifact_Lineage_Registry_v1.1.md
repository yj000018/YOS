# ADR-0017: Artifact Lineage & Registry v1.1

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  

## 1. Context

The First End-to-End Y-OS Run (MISS-E2E-V1) successfully validated the Operational Value Chain and the artifact-centric routing model defined in ADR-0012.

However, the MVP Artifact Registry schema tracked artifacts as isolated nodes. While human operators can infer the relationships between a Strategy Brief and its resulting Execution Plan, automated systems (like Lakshmi Runtime and Y-ORC) require explicit, machine-readable causal links to function reliably.

Without explicit lineage, Y-ORC cannot determine what artifact triggered the current work, and Lakshmi cannot accurately detect broken chains or stalled missions.

## 2. Decision

We will upgrade the Artifact Registry to v1.1 by implementing the **Artifact Lineage Model v1**.

The core architectural decision is:
**Artifacts are not isolated documents; they are nodes in a directed acyclic graph (DAG) representing a Mission.**

The schema will be updated to include explicit `Parent Artifact`, `Child Artifacts`, `Root Artifact`, and versioning relations (`Previous Version`, `Next Version`).

## 3. Rationale

1. **System Autonomy:** Y-ORC needs explicit edges to traverse the graph and trigger the next agent.
2. **Executive Visibility:** Lakshmi needs the graph to detect "Broken Lineage" (accepted artifacts with no children).
3. **Organizational Learning:** Saraswati needs the graph to trace execution failures back to strategic ambiguities.
4. **Resilience:** If an agent fails, the state of the mission is fully recoverable from the lineage graph.

## 4. Consequences

### 4.1. Schema Impact
The Notion Database must be updated to support self-referencing Relations for Parent/Child and Previous/Next versioning.

### 4.2. Runtime Impact
*   **Lakshmi Runtime:** Must be updated to query the lineage graph to detect stalled missions and broken chains accurately.
*   **Y-ORC:** Will route based on the graph edges rather than just status changes. When an artifact is accepted, Y-ORC will look for its defined consumer to create the child artifact.

### 4.3. Complexity
This introduces a requirement for agents (or Y-ORC acting on their behalf) to explicitly link new artifacts to their parents upon creation. This slight increase in write complexity is vastly outweighed by the read reliability it provides to the entire system.
