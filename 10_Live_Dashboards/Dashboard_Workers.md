---
id: yos-dashboard-workers
title: Y-OS Workers Dashboard
type: dashboard
tags: ['#dashboard', '#workers', '#yos']
---

# Y-OS Workers Dashboard

## Worker Registry

| Worker | Capability | Provider | Model | Executions | Artifacts | Tokens |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Brahma | architecture | openai | gpt-4o | 2 | 2 | 1,957 |
| Hanuman | build | openai | gpt-4o-mini | 2 | 2 | 1,595 |
| Saraswati | learning | anthropic | claude-opus-4 | 2 | 2 | 2,601 |
| Lakshmi | governance | openai | gpt-4o | 2 | 2 | 1,809 |
| Ganesha | reporting | openai | gpt-4o | 1 | 1 | 1,054 |
| CEO | directive | human | human | 1 | 1 | 0 |

## Provider Usage

```dataview
TABLE provider, model, tokens, validation_verdict
FROM ""
WHERE type = "artifact"
GROUP BY provider
```

## Artifact Production by Worker

```dataview
TABLE worker, mission_id, artifact_type, tokens
FROM ""
WHERE type = "artifact"
SORT worker ASC
```

## Related

- [[odt_registry]]
- [[Dashboard_Live_Runtime]]
- [[Dashboard_Economics]]


## Semantic Links

- **reports_to:** [[lmp_canonicalize_MISSION-016-C]], [[lmp_compile_MISSION-016-C]], [[lmp_inject_MISSION-016-C]]