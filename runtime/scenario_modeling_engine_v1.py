#!/usr/bin/env python3
"""
Module 2: Scenario Modeling Engine v1 — Y-OS MISSION-026
7 scenario types: Provider, Worker, Mission, Governance, Cost, Graph, Roadmap
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class ScenarioType(str, Enum):
    PROVIDER_CHANGE = "PROVIDER_CHANGE"
    WORKER_CHANGE = "WORKER_CHANGE"
    MISSION_CHANGE = "MISSION_CHANGE"
    GOVERNANCE_CHANGE = "GOVERNANCE_CHANGE"
    COST_CHANGE = "COST_CHANGE"
    GRAPH_CHANGE = "GRAPH_CHANGE"
    ROADMAP_CHANGE = "ROADMAP_CHANGE"


@dataclass
class Scenario:
    scenario_id: str
    scenario_type: ScenarioType
    title: str
    description: str
    proposed_change: str
    impact_model: dict      # attr → delta
    confidence: float
    rationale: str
    risks: list[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "scenario_type": self.scenario_type.value,
            "title": self.title,
            "description": self.description,
            "proposed_change": self.proposed_change,
            "impact_model": self.impact_model,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "risks": self.risks,
            "created_at": self.created_at,
        }


# 7 canonical scenarios derived from Y-OS strategic gaps (M-025)
SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="SCN-001",
        scenario_type=ScenarioType.PROVIDER_CHANGE,
        title="Gemini Becomes Primary Provider",
        description="OpenAI is deprecated. Gemini handles 70% of worker calls.",
        proposed_change="provider_openai_pct=10, provider_gemini_pct=70, provider_anthropic_pct=20",
        impact_model={
            "provider_openai_pct": -32.9,
            "provider_gemini_pct": +41.4,
            "provider_anthropic_pct": -8.6,
            "monthly_cost_usd": -0.12,   # Gemini cheaper
            "eis_score": -1.5,           # Transition risk
            "governance_compliance": -0.5,
        },
        confidence=0.82,
        rationale="Gemini pricing 40% lower. Risk: not live-tested (GAP-008).",
        risks=["Gemini not yet live-validated", "Worker prompt compatibility unknown"],
    ),
    Scenario(
        scenario_id="SCN-002",
        scenario_type=ScenarioType.WORKER_CHANGE,
        title="Add Vishnu Worker (Integration Specialist)",
        description="New worker Vishnu handles system integration tasks, reducing Hanuman overload.",
        proposed_change="active_workers=7, total_missions+1",
        impact_model={
            "active_workers": +1,
            "total_missions": +1,
            "eis_score": +1.2,
            "governance_compliance": +0.3,
        },
        confidence=0.88,
        rationale="Hanuman/build handles 40% of missions. Specialization reduces bottleneck.",
        risks=["New worker requires context pack design", "ADR required for new worker"],
    ),
    Scenario(
        scenario_id="SCN-003",
        scenario_type=ScenarioType.MISSION_CHANGE,
        title="Skip MISSION-027 (KGC v5), go directly to MISSION-028 (n8n)",
        description="Delay semantic depth pass. Prioritize automation integration.",
        proposed_change="orphan_rate stays 7.1%, n8n integration active",
        impact_model={
            "eis_score": -2.0,           # Graph quality stagnates
            "orphan_rate": +0.5,         # Slight degradation
            "governance_compliance": -1.0,
            "monthly_cost_usd": -0.05,   # n8n reduces manual overhead
        },
        confidence=0.75,
        rationale="n8n delivers operational value faster. Graph quality already at 100.",
        risks=["Orphan rate may increase without KGC v5", "EIS plateau risk"],
    ),
    Scenario(
        scenario_id="SCN-004",
        scenario_type=ScenarioType.GOVERNANCE_CHANGE,
        title="Implement Constitutional Amendment Protocol (MISSION-030)",
        description="Define formal amendment process. Constitution v1 becomes evolvable.",
        proposed_change="governance_compliance+2, total_adrs+1",
        impact_model={
            "governance_compliance": +2.0,
            "total_adrs": +1,
            "eis_score": +0.5,
        },
        confidence=0.92,
        rationale="FROZEN constitution limits Y-OS evolution. Amendment protocol enables controlled growth.",
        risks=["Amendment process could be misused without strict governance"],
    ),
    Scenario(
        scenario_id="SCN-005",
        scenario_type=ScenarioType.COST_CHANGE,
        title="Enforce $0.10/session Budget Cap",
        description="Hard budget limit per pipeline execution. Triggers provider downgrade.",
        proposed_change="monthly_cost_usd reduced by 30%, some workers use cheaper models",
        impact_model={
            "monthly_cost_usd": -0.135,
            "eis_score": -1.0,           # Cheaper models = slightly lower quality
            "governance_compliance": +1.0,  # K2 rule compliance
        },
        confidence=0.90,
        rationale="K2 rule: never spend without authorization. Budget enforcement closes GAP-009.",
        risks=["Quality degradation if budget too tight", "Brahma/architecture needs premium models"],
    ),
    Scenario(
        scenario_id="SCN-006",
        scenario_type=ScenarioType.GRAPH_CHANGE,
        title="KGC v5: Reduce Orphan Rate to <3%",
        description="Body wikilinks pass + concept-to-concept edges + ADR supersession chains.",
        proposed_change="orphan_rate=2.5, graph_quality=108",
        impact_model={
            "orphan_rate": -4.6,
            "graph_quality": +8.0,
            "eis_score": +1.5,
            "total_adrs": 0,
        },
        confidence=0.88,
        rationale="M-021 audit: 34 orphan files remain. KGC v5 closes the gap.",
        risks=["Body edits must remain additive", "Large corpus — risk of regression"],
    ),
    Scenario(
        scenario_id="SCN-007",
        scenario_type=ScenarioType.ROADMAP_CHANGE,
        title="Accelerate Roadmap: Execute M-026+M-027+M-029 in Parallel",
        description="Run simulation, graph depth, and Notion sync simultaneously.",
        proposed_change="3 missions in parallel, faster delivery, higher coordination cost",
        impact_model={
            "eis_score": +3.0,
            "orphan_rate": -4.6,
            "notion_sync": 1,
            "simulation_layer": 1,
            "monthly_cost_usd": +0.20,   # Parallel = more API calls
            "governance_compliance": -1.5,  # Coordination risk
        },
        confidence=0.70,
        rationale="Parallel execution reduces calendar time by ~60%. Risk: coordination overhead.",
        risks=["Dependency conflicts between missions", "Higher governance review burden"],
    ),
]


class ScenarioModelingEngine:
    def __init__(self):
        self.scenarios = SCENARIOS

    def get_all(self) -> list[Scenario]:
        return self.scenarios

    def get_by_type(self, t: ScenarioType) -> list[Scenario]:
        return [s for s in self.scenarios if s.scenario_type == t]

    def get_by_id(self, sid: str) -> Scenario | None:
        return next((s for s in self.scenarios if s.scenario_id == sid), None)
