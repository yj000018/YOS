---
title: Y-OS Governance Flow
type: visual_map
tags: ['#visual', '#governance', '#yos']
---

# Y-OS Governance Flow — Mermaid Fallback

*See [[YOS_Governance_Flow.canvas]] for interactive Canvas version.*

```mermaid
flowchart TD
    PROP["ADR Proposal\n(Brahma / any worker)"]
    PROP --> LAK["Lakshmi Review\n5 Articles × Risk Score"]
    LAK --> |Score ≤ 35| APP["APPROVE"]
    LAK --> |36–55| WARN["APPROVE WITH WARNING"]
    LAK --> |> 55 or blocking| REJ["REJECT"]
    APP --> CEO["CEO Recommendation\nGanesha"]
    WARN --> CEO
    CEO --> |ADOPT| ACCEPTED["ADR ACCEPTED\n(canonical)"]
    CEO --> |REJECT| REVISED["ADR REVISED\nor SUPERSEDED"]
    REJ --> REVISED
```


## Semantic Links

- **governed_by:** [[Y-OS_Constitution_v1]]
- **reviewed_by:** [[ADR-0044_Live_Worker_Execution_v1]], [[ADR-0045_Multi_Worker_Pipeline_Orchestration_v1]], [[ADR-0046_Organizational_Digital_Twin_Runtime_v1]], [[ADR-0047_Autonomous_Organizational_Observability]], [[ADR-0048_Roadmap_Architecture_Review]]