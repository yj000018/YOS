---
id: yos-runtime-flow-diagram
title: Runtime Flow Diagram
type: runtime_spec
status: ACCEPTED
date: '2026-06-13'
owner: Manus Y-OS
parent: '[[05_Runtime_MOC]]'
tags:
- '#accepted'
- '#runtime'
- '#yos'
source_branch: y-os-doctrine
canonical: true
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
---

# Runtime Flow Diagram

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

```mermaid
sequenceDiagram
    participant Agent as Execution Agent
    participant Registry as Artifact Registry
    participant Graph as Mission Graph Engine
    participant OLE as Open Loop Engine
    participant Lakshmi as Lakshmi Runtime
    participant CEO as CEO

    Agent->>Registry: 1. Create/Update Artifact (Status, Parent_ID)
    Note over Registry: State Persisted
    
    Lakshmi->>Registry: 2. Fetch all active artifacts
    Registry-->>Lakshmi: Raw Artifact Data
    
    Lakshmi->>Graph: 3. Pass raw data
    Graph-->>Lakshmi: 4. Return Mission DAGs
    
    Lakshmi->>OLE: 5. Pass Mission DAGs
    OLE-->>Lakshmi: 6. Return Open Loops (Anomalies)
    
    Lakshmi->>Lakshmi: 7. Generate Dashboard State JSON
    Lakshmi->>Lakshmi: 8. Generate CEO Briefing (LLM or Deterministic)
    
    Lakshmi->>CEO: 9. Deliver CEO Briefing
    Lakshmi->>CEO: 10. Deliver Dashboard & Open Loops
```


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
