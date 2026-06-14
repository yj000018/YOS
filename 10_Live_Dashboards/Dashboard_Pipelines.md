---
id: yos-dashboard-pipelines
title: Y-OS Pipelines Dashboard
type: dashboard
tags: ['#dashboard', '#pipelines', '#yos']
---

# Y-OS Pipelines Dashboard

## Pipeline Registry

| Pipeline | Mission | Status | Steps | Artifacts | Checkpoints | Rollbacks | Tokens | Cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PIPE-5C15BA64 | [[MISSION-018]] | COMPLETED | 6 | 6 | 6 | 1 | 4,836 | $0.074135 |

## Pipeline Checkpoints

```dataview
TABLE pipeline_id, step, status
FROM "mission_018/checkpoints"
SORT step ASC
```

## Rollback Events

```dataview
TABLE pipeline_id, step, artifacts_preserved
FROM "mission_018/rollback_events"
```

## Validation Queue

```dataview
TABLE artifact_id, verdict, worker
FROM "mission_018/validation_queue"
SORT verdict ASC
```

## Related

- [[pipeline_state]]
- [[odt_registry]]
- [[ODT_Pipeline_Flow]]
