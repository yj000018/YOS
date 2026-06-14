#!/usr/bin/env python3
"""Generate 6 Dataview dashboards for MISSION-019 ODT."""

from pathlib import Path

DASH_DIR = Path(__file__).parent.parent / "10_Live_Dashboards"
DASH_DIR.mkdir(exist_ok=True)


def write(name: str, content: str) -> None:
    (DASH_DIR / f"{name}.md").write_text(content, encoding="utf-8")
    print(f"  ✅ {name}.md")


# 1. Dashboard_Live_Runtime
write("Dashboard_Live_Runtime", """---
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
""")

# 2. Dashboard_Workers
write("Dashboard_Workers", """---
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
""")

# 3. Dashboard_Pipelines
write("Dashboard_Pipelines", """---
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
""")

# 4. Dashboard_Artifacts
write("Dashboard_Artifacts", """---
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
""")

# 5. Dashboard_Economics
write("Dashboard_Economics", """---
id: yos-dashboard-economics
title: Y-OS Economics Dashboard
type: dashboard
tags: ['#dashboard', '#economics', '#yos']
---

# Y-OS Economics Dashboard

## Cost by Provider

| Provider | Calls | Tokens | Cost (USD) | Avg Latency |
| :--- | :--- | :--- | :--- | :--- |
| OpenAI | 8 | 6,412 | $0.120000 | 4,700ms |
| Anthropic | 2 | 2,601 | $0.030000 | 22,700ms |
| Human (CEO) | 1 | 0 | $0.000000 | — |
| **TOTAL** | **11** | **9,013** | **$0.150000** | — |

## Cost by Worker

| Worker | Tokens | Estimated Cost |
| :--- | :--- | :--- |
| Brahma | 1,957 | $0.039 |
| Hanuman | 1,595 | $0.008 |
| Saraswati | 2,601 | $0.030 |
| Lakshmi | 1,809 | $0.036 |
| Ganesha | 1,054 | $0.021 |
| CEO | 0 | $0.000 |

## Cost by Mission

| Mission | Tokens | Cost |
| :--- | :--- | :--- |
| [[MISSION-017]] | 4,297 | $0.076055 |
| [[MISSION-018]] | 4,836 | $0.074135 |

## Token Consumption Trend

```
M-013: 0 tokens (no LLM calls)
M-014: 0 tokens (no LLM calls)
M-015: 0 tokens (no LLM calls)
M-016: 0 tokens (no LLM calls)
M-017: 4,297 tokens → $0.076055
M-018: 4,836 tokens → $0.074135
TOTAL: 9,133 tokens → $0.150190
```

## Related

- [[odt_registry]]
- [[ODT_Economics]]
- [[Dashboard_Workers]]
""")

# 6. Dashboard_Governance
write("Dashboard_Governance", """---
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
""")

print(f"\n6 dashboards generated in {DASH_DIR}")
