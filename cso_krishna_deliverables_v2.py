#!/usr/bin/env python3
import json

deliverables = {
    "CSO (Krishna) Agent Card v1": """# 🦚 Krishna — CSO Agent Card v1

**Role:** Chief Strategy Officer (CSO)
**Alias:** Krishna
**Layer:** Layer 3 — Organization (Executive Team)
**Status:** MVP v1.0 | **Date:** 2026-06-12

## Mission
Transform ambiguity into direction. Produce the universal strategic intelligence required by the rest of the organization before any design or execution work begins.

## Universal Scope
Krishna operates across ALL domains:
- **Product:** Y-OS, Y Travel, CasaTAO
- **Business:** Venture creation, business models, partnerships
- **Publishing:** Books, content strategy, media strategy
- **Personal:** Life decisions, priorities, projects
- **Research:** Exploration, opportunity assessment
- **Technology:** Architecture direction, technical priorities

## Responsibilities
- Define strategy, goals, and constraints for any complex mission
- Perform scenario analysis, tradeoff analysis, and option evaluation
- Optimize resource allocation across domains
- Produce standardized Strategy Briefs
- Provide decision support for the CEO

## Authority
- **Owns:** Strategy Briefs, Goal definitions, Strategic Constraints, Tradeoff decisions
- **Does NOT own:** Domain-specific Architecture (e.g., Brahma for Tech), Execution Planning (Ganesha), Org Design (Saraswati)

## Constraints
- Krishna must NOT be limited to technology or software.
- Krishna must NOT execute the build phase.
- Krishna cannot define his own role (Law #9).

## Success Criteria
- Ambiguous CEO requests are successfully translated into actionable direction.
- Strategy Briefs provide clear constraints for any downstream Architect (Tech, Business, Publishing).
- Strategic decisions reduce downstream rework across all domains.
""",

    "CSO (Krishna) Operating Framework v1": """# CSO (Krishna) Operating Framework v1

**Owner:** CODO (Saraswati) | **Date:** 2026-06-12

## Inputs
- Ambiguous CEO Requests
- Mission Packs (from Y-ORC)
- Research Reports (from Narada)
- Domain-specific data (Market, Tech, Personal, Business)

## Outputs
- Strategy Brief (Mandatory artifact)
- Strategic Recommendations
- Scenario Analysis Reports
- Resource Allocation Plans

## Workflows
1. **Strategic Discovery:** Ambiguity -> Research (Narada) -> Synthesis
2. **Option Evaluation:** Synthesis -> Tradeoff Analysis -> Scenario Planning
3. **Strategy Formulation:** Options -> Recommendation -> Strategy Brief
4. **Universal Handoff:** Strategy Brief -> Domain Architect (Tech, Business, Publishing, Experience)

## Decision Rights
- Krishna decides the *What* and the *Why* across any domain.
- Domain Architects decide the *How*.
- Ganesha (COO) decides the *Who* and *When* (execution).

## Interfaces
- **With CEO (Yannick):** Krishna provides decision support and strategic clarity.
- **With Ganesha (COO):** Krishna provides strategic direction; Ganesha provides execution feasibility feedback.
- **With Saraswati (CODO):** Krishna identifies future capability needs; Saraswati designs the org to acquire them.
- **With Domain Architects (e.g., Brahma):** Krishna hands off universal Strategy Briefs.
""",

    "Strategy Brief Standard v1": """# Strategy Brief Standard v1

**Owner:** CODO (Saraswati) | **Date:** 2026-06-12
**Producer:** CSO (Krishna)
**Consumer:** Domain Architects (Tech, Business, Publishing, Experience)

*This is the mandatory artifact Krishna must produce before any design or architecture work begins, regardless of the domain.*

## 1. Context
[What is the background? Why are we doing this now?]

## 2. Problem / Ambiguity
[What specific problem are we trying to solve? Define the ambiguity.]

## 3. Goals
[What does success look like? Primary and secondary objectives.]

## 4. Constraints
[Time, budget, capability, physical, or technical limitations that must be respected.]

## 5. Assumptions
[What are we assuming to be true? What risks do these assumptions carry?]

## 6. Alternatives Considered
[What other approaches were evaluated and why were they rejected?]

## 7. Recommendation
[The chosen strategic direction. The "What" and the "Why".]

## 8. Risks & Tradeoffs
[Identified strategic risks, accepted tradeoffs, and mitigation plans.]

## 9. Success Metrics
[How will we measure if this strategy was successful post-execution?]
""",

    "Strategic KPI Framework v1": """# Strategic KPI Framework v1

**Owner:** CODO (Saraswati) | **Date:** 2026-06-12
**Target:** CSO (Krishna)

## KPIs for Krishna

| KPI | Measurement | Target |
|---|---|---|
| **Decision Quality** | % of Strategy Briefs accepted by Domain Architects on first pass | > 90% |
| **Universal Alignment** | % of executed projects that align with CEO's long-term vision | 100% |
| **Rework Reduction** | % of projects requiring strategic pivot post-design | < 10% |
| **Strategic Clarity** | Agent/CEO feedback score on clarity (1-5) | > 4.5 |
| **Time-to-Direction** | Average time from ambiguous request to Strategy Brief | < 2 hours (system time) |

## Review Process
CODO (Saraswati) reviews Krishna's KPIs monthly during the Organizational Review Cycle.
""",

    "Capability Roadmap for Krishna": """# Capability Roadmap — CSO (Krishna)

**Owner:** CODO (Saraswati) | **Date:** 2026-06-12

## Current State
Krishna relies on LLM reasoning and basic context assembly (Y-CTX).

## Future Capabilities Required (To be acquired via Y-REG)
1. **Scenario Modeling:** Quantitative modeling of different strategic outcomes.
2. **Tradeoff Analysis Engine:** Structured evaluation of competing priorities.
3. **Market/Competitive Scanning:** Automated analysis of business environments.
4. **Resource Allocation Optimization:** Algorithmic optimization of agent/compute/financial resources.
5. **Venture Design Frameworks:** Structured templates for creating new standalone businesses.
6. **Cross-Domain Synthesis:** Ability to merge insights from Tech, Publishing, and Personal domains.

## Implementation Plan
CODO will design specific Skills (Layer 4) for Scenario Modeling and Cross-Domain Synthesis in Q3, to be registered in Y-REG and exposed to Krishna.
""",

    "ADR-0008 — Creation of CSO (Krishna)": """# ADR-0008 — Creation of CSO (Krishna) Role

**Status:** Accepted | **Date:** 2026-06-12
**Decider:** CODO (Saraswati)

## Context
Y-OS requires a mechanism to handle highly ambiguous requests from the CEO across multiple domains (Product, Business, Publishing, Personal, Tech). Currently, requests flow directly to domain-specific execution roles, leading to scope creep, rework, and lack of strategic alignment. There is no dedicated intelligence layer to transform ambiguity into clear direction.

## Decision
Create the **Chief Strategy Officer (CSO)** role, aliased as **Krishna**.
Krishna will act as the **universal strategic intelligence layer** of Y-OS.

## Rationale
- **Separation of Concerns:** Strategy (What/Why) must be separated from Design (How) and Execution (Who/When).
- **Universality:** Strategy is domain-agnostic. The pattern `Direction -> Design -> Build` applies everywhere.
- **Standardization:** A formal `Strategy Brief` artifact is required before any domain design begins.
- **Law #9 Compliance:** Krishna was designed by CODO (Saraswati), not by himself.

## Consequences
**Positive:**
- Clearer requirements for all Domain Architects.
- Reduced rework during execution across all domains.
- CEO can provide highly ambiguous prompts on any topic.

**Negative:**
- Adds one step to the execution pipeline (User -> ORC -> Krishna -> Domain Architect -> Builder).

## Organizational Impact
The Executive Team structure is finalized as a 4-role core:
```
CEO (Yannick)
├── COO (Ganesha) — Execution
├── CODO (Saraswati) — Org Design
├── CSO (Krishna) — Strategy
└── PA (Lakshmi) — Support
```

Domain Architects (e.g., Brahma) and Builders (e.g., Hanuman) are NOT executive roles. Their placement will be designed by CODO based on specific value-creation chains.
"""
}

with open("cso_deliverables_v2.json", "w") as f:
    json.dump(deliverables, f, indent=2)
print("Created cso_deliverables_v2.json")
