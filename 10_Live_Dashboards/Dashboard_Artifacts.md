---
id: yos-dashboard-artifacts
title: Y-OS Artifacts Dashboard
type: dashboard
tags: ['#dashboard', '#artifacts', '#yos']
---

# Y-OS Artifacts Dashboard

## All Artifacts

| Artifact | Mission | Worker | Type | Tokens | Validation | Gov |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [[ART-M017-BRAHMA-ARCHITECTURE]] | MISSION-017 | Brahma | Architecture Note | 1,117 | VALID | APPROVE |
| [[ART-M017-HANUMAN-BUILD]] | MISSION-017 | Hanuman | Implementation Plan | 829 | VALID | APPROVE |
| [[ART-M017-SARASWATI-LEARNING]] | MISSION-017 | Saraswati | Learning Report | 1,358 | VALID | APPROVE |
| [[ART-M017-LAKSHMI-GOVERNANCE]] | MISSION-017 | Lakshmi | Governance Review | 993 | VALID | APPROVE |
| [[ART-M018-CEO-DIRECTIVE]] | MISSION-018 | CEO | CEO Directive | 0 | — | — |
| [[ART-M018-BRAHMA-ARCHITECTURE]] | MISSION-018 | Brahma | Architecture Note | 957 | VALID | APPROVE |
| [[ART-M018-HANUMAN-BUILD]] | MISSION-018 | Hanuman | Implementation Plan | 766 | VALID_W | APPROVE |
| [[ART-M018-SARASWATI-LEARNING]] | MISSION-018 | Saraswati | Learning Report | 1,243 | VALID | APPROVE |
| [[ART-M018-LAKSHMI-GOVERNANCE]] | MISSION-018 | Lakshmi | Governance Review | 816 | VALID | APPROVE |
| [[ART-M018-GANESHA-CEO-BRIEFING]] | MISSION-018 | Ganesha | CEO Briefing | 1,054 | VALID | APPROVE |

## Lineage Chains

```dataview
TABLE consumes_artifact, produces_artifact, mission_id
FROM ""
WHERE type = "artifact"
```

## Superseded Artifacts

```dataview
TABLE supersedes, status
FROM ""
WHERE supersedes != null
```

## Related

- [[odt_registry]]
- [[ODT_Artifact_Lineage]]
- [[Dashboard_Live_Runtime]]
