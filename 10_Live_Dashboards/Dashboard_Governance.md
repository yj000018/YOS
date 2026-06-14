---
id: yos-dashboard-governance
title: Y-OS Governance Dashboard
type: dashboard
tags: ['#dashboard', '#governance', '#yos']
---

# Y-OS Governance Dashboard

## Governance Verdicts

| Artifact | Mission | Verdict | Risk Score | Reviewer |
| :--- | :--- | :--- | :--- | :--- |
| ART-M017-BRAHMA-ARCHITECTURE | MISSION-017 | APPROVE | 3/100 | Lakshmi |
| ART-M017-HANUMAN-BUILD | MISSION-017 | APPROVE | 3/100 | Lakshmi |
| ART-M017-SARASWATI-LEARNING | MISSION-017 | APPROVE | 3/100 | Lakshmi |
| ART-M017-LAKSHMI-GOVERNANCE | MISSION-017 | APPROVE | 3/100 | Lakshmi |
| ART-M018-BRAHMA-ARCHITECTURE | MISSION-018 | APPROVE | 3/100 | Lakshmi |
| ART-M018-HANUMAN-BUILD | MISSION-018 | APPROVE | 3/100 | Lakshmi |
| ART-M018-SARASWATI-LEARNING | MISSION-018 | APPROVE | 3/100 | Lakshmi |
| ART-M018-LAKSHMI-GOVERNANCE | MISSION-018 | APPROVE | 3/100 | Lakshmi |
| ART-M018-GANESHA-CEO-BRIEFING | MISSION-018 | APPROVE | 3/100 | Lakshmi |

## ADR Governance Status

| ADR | Status | Mission | Lakshmi Score |
| :--- | :--- | :--- | :--- |
| [[ADR-0040]] | ACCEPTED | MISSION-013 | 18/100 |
| [[ADR-0041]] | ACCEPTED | MISSION-014 | 15/100 |
| [[ADR-0042]] | ACCEPTED | MISSION-015 | 18/100 |
| [[ADR-0043]] | ACCEPTED | MISSION-016 | 10/100 |
| [[ADR-0044]] | ACCEPTED | MISSION-017 | 8/100 |
| [[ADR-0045]] | ACCEPTED | MISSION-018 | 10/100 |
| [[ADR-0046]] | PROPOSED | MISSION-019 | — |

## Open Governance Issues

```dataview
TABLE governance_verdict, risk_score, mission_id
FROM ""
WHERE governance_verdict = "REJECT" OR governance_verdict = "APPROVE_WITH_WARNING"
```

## Constitutional Compliance

- Article I (Artifact Primacy): ✅ All outputs registered as artifacts
- Article II (Preservation Principle): ✅ No deletions, additive only
- Article III (Derivation Transparency): ✅ Full lineage tracked
- Article IV (Human Override): ✅ CEO directive as pipeline entry
- Article V (Governance Before Autonomy): ✅ Lakshmi pre/post reviews

## Related

- [[Y-OS_Constitution_v1]]
- [[Lakshmi]]
- [[ODT_Governance_System]]
