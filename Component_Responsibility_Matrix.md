# Component Responsibility Matrix

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

| Component | Primary Responsibility | Input | Output |
| :--- | :--- | :--- | :--- |
| **Artifact Registry** | Persist artifact metadata and state | Agent outputs (via API) | Raw artifact data |
| **Artifact Lineage** | Maintain parent/child relationships | Registry writes | Navigable tree |
| **Mission Graph Engine** | Reconstruct full mission state from lineage | Registry data | Directed Acyclic Graph (DAG) |
| **Open Loop Engine** | Evaluate DAG against governance rules | Mission DAG | Open Loop Signals (P1, P2, P3) |
| **Lakshmi Runtime** | Orchestrate visibility generation | DAG + Open Loops | Dashboard State |
| **Briefing Generator** | Synthesize human-readable executive summary | Dashboard State | CEO Briefing |
| **Y-ORC (Future)** | Route work based on state changes | Registry State + Open Loops | Agent Triggers |
