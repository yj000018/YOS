#!/usr/bin/env python3
"""Publish all 6 Saraswati deliverables to Notion"""
import json, subprocess, re

PARENT_ID = "37635e21-8cf8-8173-a3b2-f083d321382c"

def notion_create(title, content):
    payload = {
        "parent": {"page_id": PARENT_ID},
        "pages": [{"properties": {"title": title}, "content": content}]
    }
    cmd = ["manus-mcp-cli", "tool", "call", "notion-create-pages",
           "--server", "notion", "--input", json.dumps(payload)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = r.stdout + r.stderr
    m = re.search(r'https://app\.notion\.com/p/[a-f0-9]+', out)
    return m.group(0) if m else f"ERR: {out[-80:]}"

pages = [
    ("🌸 Saraswati — Executive Team v2", """# Executive Team v2

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12 | **Status:** v1.0

## Principle

The organization must be designed before it is populated.
Saraswati is the Meta-Architect of the Organization — not an HR role.

## Role Definitions

| Role | Mission | Inputs | Outputs | KPIs |
|---|---|---|---|---|
| COO (Ganesha) | Run the organization | Mission Pack | Execution Plan | Mission success rate, Time to execution |
| CODO (Saraswati) | Improve the organization | Execution Feedback, Lessons Learned | Org Improvements, Training Plans | Capability growth, Process efficiency |
| Strategist (Krishna) | Define strategy | Objective, Market Data | Strategy Brief | Strategy viability, Forecast accuracy |
| Architect (Brahma) | Design systems | Strategy Brief | Technical Spec | System scalability, Defect rate |
| Developer (Hanuman) | Build systems | Technical Spec | Code, Build Report | Code quality, Delivery speed |
| Researcher (Narada) | Gather information | Query | Research Report | Data accuracy, Source credibility |
| PA (Lakshmi) | Support operations | Admin Request | Action Completed | Response time, Task completion |

## Escalation Rules

All escalations flow upward: Specialist → COO → CEO (Yannick).
CODO escalates organizational blockers directly to CEO.

## Architecture Consistency

Law #3: Agents use modules. Modules do not replace agents.
Law #7: COO executes. CODO improves.
"""),

    ("🌸 Saraswati — Role Governance Framework v1", """# Role Governance Framework v1

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12

## How Roles Are Created

1. Need identified by CODO via Org Review Workflow
2. Role Card drafted by CODO
3. Reviewed by COO
4. Approved by CEO (Yannick)
5. Registered in Y-REG

## How Roles Are Modified

1. CODO detects performance gap or scope change
2. Updated Role Card proposed
3. COO validates operational impact
4. CEO approves if structural change
5. Y-REG updated

## How Roles Are Retired

1. CODO identifies role as fully automatable by Layer 1 modules
2. Transition plan drafted
3. CEO approves retirement
4. Role archived in Y-REG (status: archived)

## Ownership Model

CODO owns all Role Cards, Agent Cards, and Organizational Mapping.
COO owns Execution Plans and Mission Assignments.
"""),

    ("🌸 Saraswati — Communication Contracts v1", """# Communication Contracts v1

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12

## Principle

Every role pair with a regular handoff must have a defined Communication Contract.

## Contracts

| From | Output | To | Quality Criteria | Failure Mode |
|---|---|---|---|---|
| Strategist | Strategy Brief | Architect | Must include constraints, scale, success criteria | Architect rejects: missing scope |
| Architect | Technical Spec | Developer | Must include API contracts, data models, test criteria | Developer blocks: ambiguous spec |
| Developer | Build Report | COO | Must include test results, deployment status, known issues | COO escalates: incomplete report |
| Researcher | Research Report | Strategist | Must include sources, confidence level, date | Strategist rejects: unverified data |
| COO | Mission Pack | All Agents | Must include objective, complexity, constraints, success criteria | Agent blocks: unclear mission |
| CODO | Org Review Report | COO + CEO | Must include findings, recommendations, priority | No action taken: report ignored |

## Format Standards

All outputs must be structured documents (Markdown), not free text.
All handoffs must reference the originating Mission ID.
"""),

    ("🌸 Saraswati — Competency Framework v1", """# Competency Framework v1 (Capability Ownership Matrix)

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12

## Per-Role Competency Map

| Role | Current Competencies | Required Competencies | Gap | Development Roadmap |
|---|---|---|---|---|
| COO | Delegation, Routing, Prioritization | Conflict Resolution, Capacity Planning | Medium | Monthly COO Review with CODO |
| CODO | Org Design, Role Definition | Quantitative KPI Analysis | Low | Integrate Y-LOG data |
| Strategist | Analysis, Planning | Data-Driven Forecasting | Medium | Integrate Y-MEM historical data |
| Architect | System Design, Patterns | Security Architecture, Cost Optimization | Medium | Security training Q3 |
| Developer | Python, API, Deployment | Automated Testing, Performance Profiling | High | Testing framework Q2 |
| Researcher | Web Research, Synthesis | Structured Data Analysis | Low | Y-REG capability expansion |
| PA | Scheduling, Routing | Proactive Anticipation | Low | Context-aware prompting |

## Capability Gaps Identified

- Automated Testing (Developer — High priority)
- Performance Profiling (Developer — Medium)
- Data Cleansing (Researcher — Low)
- Quantitative KPI Analysis (CODO — Low)
"""),

    ("🌸 Saraswati — Organizational KPI Framework v1", """# Organizational KPI Framework v1

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12

## KPI Categories

| Category | KPI | Measurement | Target |
|---|---|---|---|
| Role Effectiveness | Task completion rate per agent | % missions completed without escalation | >90% |
| Communication Quality | Handoff rejection rate | % handoffs rejected by receiving agent | <5% |
| Execution Quality | Defect rate post-delivery | Bugs found after Developer delivery | <2 per mission |
| Learning Effectiveness | New capabilities acquired | Count per month via Y-REG | >2/month |
| Capability Growth | Y-REG object count | Total registered capabilities | +10% per quarter |
| Organizational Health | Agent utilization balance | COO bottleneck index | <30% COO load |

## Review Cadence

- Weekly: COO operational metrics
- Monthly: CODO organizational review
- Quarterly: CEO strategic review

## Bottleneck Alert

Current: COO overloaded with routing decisions.
Recommendation: Delegate routing to Y-ORC. COO focuses on exceptions only.
"""),

    ("🌸 Saraswati — Continuous Evolution Engine v1", """# Continuous Evolution Engine v1

**Owner:** Saraswati (CODO) | **Date:** 2026-06-12

## The Loop

```
Mission → Execution → Feedback → Learning
→ Organizational Improvement → Capability Expansion → Better Execution → Mission
```

This loop is permanent and never stops.

## Trigger Conditions

- After every Advanced Mission
- Monthly scheduled review
- When bottleneck detected (COO load > 70%)
- When handoff rejection rate > 5%

## Inputs

- Mission Reports (from COO)
- Execution Reports (from all agents)
- Failures and Bottlenecks (from Y-LOG)
- Agent Feedback (from all roles)

## Outputs

- Role Updates (to Y-REG)
- KPI Updates (to KPI Framework)
- Capability Recommendations (to Y-CAP)
- Training Recommendations (to Role Cards)
- Process Improvements (to Communication Contracts)

## Three Levels of Evolution

| Level | Question | Owner | Output |
|---|---|---|---|
| Knowledge | What do we know? | Y-MEM | Knowledge |
| Capability | What can we do? | Y-REG | Capabilities |
| Organizational | How should we operate? | CODO | Org improvements |

## Y-OS Law #8

The goal is not only to solve problems.
The goal is to continuously improve the organization that solves problems.
""")
]

urls = {}
for title, content in pages:
    print(f"Creating: {title[:50]}...")
    url = notion_create(title, content)
    urls[title] = url
    print(f"  → {url}")

print("\n=== ALL DELIVERABLES PUBLISHED ===")
for t, u in urls.items():
    print(f"{t[:50]}: {u}")

with open("saraswati_notion_urls.json", "w") as f:
    json.dump(urls, f, indent=2)
