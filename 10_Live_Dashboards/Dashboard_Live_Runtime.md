---
id: yos-dashboard-live-runtime
title: Y-OS Live Runtime Dashboard
type: dashboard
tags: ['#dashboard', '#runtime', '#yos']
---

# Y-OS Live Runtime Dashboard

> Powered by Dataview. Install the Dataview plugin to enable live queries.

## Active Pipelines

```dataview
TABLE status, steps, artifacts, total_tokens AS "Tokens", cost_usd AS "Cost"
FROM "mission_018"
WHERE type = "pipeline"
SORT started_at DESC
```

## Recent Executions (Last 10 Artifacts)

```dataview
TABLE worker, provider, tokens, validation_verdict AS "Validation", governance_verdict AS "Gov"
FROM "mission_017" OR "mission_018"
WHERE type = "artifact"
SORT created_at DESC
LIMIT 10
```

## Validation Status

```dataview
TABLE validation_verdict, governance_verdict, worker, mission_id
FROM ""
WHERE type = "artifact"
SORT created_at DESC
```

## Governance Status

```dataview
TABLE governance_verdict, worker, mission_id
FROM ""
WHERE governance_verdict != null
SORT created_at DESC
```

## Related

- [[odt_registry]]
- [[system_health_report]]
- [[YOS_Organizational_Digital_Twin]]


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]