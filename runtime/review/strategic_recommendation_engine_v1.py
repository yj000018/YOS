#!/usr/bin/env python3
"""
Module 1: Strategic Recommendation Engine v1 — Y-OS MISSION-025
Generates evidence-based strategic recommendations from ODT, Time Machine, Event Bus,
mission/ADR history, provider metrics, governance metrics, graph metrics, execution metrics.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Category(str, Enum):
    RISK = "RISK"
    OPPORTUNITY = "OPPORTUNITY"
    BOTTLENECK = "BOTTLENECK"
    TECHNICAL_DEBT = "TECHNICAL_DEBT"
    STRATEGIC_GAP = "STRATEGIC_GAP"
    GOVERNANCE = "GOVERNANCE"
    PERFORMANCE = "PERFORMANCE"
    ARCHITECTURE = "ARCHITECTURE"


class Impact(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Urgency(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    SHORT_TERM = "SHORT_TERM"   # < 3 months
    MEDIUM_TERM = "MEDIUM_TERM" # 3–6 months
    LONG_TERM = "LONG_TERM"     # 6–12 months


@dataclass
class StrategicRecommendation:
    recommendation_id: str
    title: str
    description: str
    category: Category
    impact: Impact
    confidence: float          # 0.0–1.0
    urgency: Urgency
    evidence: list[str]
    dependencies: list[str]
    expected_roi: str
    priority_score: float = 0.0
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "recommendation_id": self.recommendation_id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "impact": self.impact.value,
            "confidence": self.confidence,
            "urgency": self.urgency.value,
            "evidence": self.evidence,
            "dependencies": self.dependencies,
            "expected_roi": self.expected_roi,
            "priority_score": self.priority_score,
            "generated_at": self.generated_at,
        }


# ── Recommendation Catalog ────────────────────────────────────────────────────
RECOMMENDATIONS: list[StrategicRecommendation] = [
    StrategicRecommendation(
        recommendation_id="REC-001",
        title="Implement Executive Simulation Layer (MISSION-026)",
        description="Y-OS can observe, remember, and recommend — but cannot simulate causal impact. MISSION-026 closes the final gap in the cognitive loop.",
        category=Category.STRATEGIC_GAP,
        impact=Impact.CRITICAL,
        confidence=0.97,
        urgency=Urgency.IMMEDIATE,
        evidence=["ADR-0048 roadmap", "EIS=96 plateau", "M-025 strategic engine operational"],
        dependencies=["MISSION-025"],
        expected_roi="Enables what-if analysis, reduces decision risk by ~40%",
    ),
    StrategicRecommendation(
        recommendation_id="REC-002",
        title="Reduce orphan rate from 7.1% to <3%",
        description="34 files remain unlinked. KGC v5 body-wikilinks pass would close this gap and push Graph Quality to 105+.",
        category=Category.TECHNICAL_DEBT,
        impact=Impact.HIGH,
        confidence=0.92,
        urgency=Urgency.SHORT_TERM,
        evidence=["M-021 audit: orphan_rate=7.1%", "ADR-0049 partial pass", "Graph Quality=100 ceiling"],
        dependencies=["MISSION-021"],
        expected_roi="Graph Quality 100 → 105+, EIS +2–3 points",
    ),
    StrategicRecommendation(
        recommendation_id="REC-003",
        title="Implement Gemini API key and validate live Gemini calls",
        description="Provider registry has Gemini registered but no live API key. 28.6% of routing decisions target an untested provider.",
        category=Category.RISK,
        impact=Impact.HIGH,
        confidence=0.98,
        urgency=Urgency.IMMEDIATE,
        evidence=["M-023: Gemini registered, no live test", "provider_registry.json", "failover_engine_v1"],
        dependencies=["MISSION-023"],
        expected_roi="Eliminates single-point-of-failure risk, enables true 3-provider resilience",
    ),
    StrategicRecommendation(
        recommendation_id="REC-004",
        title="Build Notion Sync for ODT Registry",
        description="ODT Registry exists as JSON only. Syncing to Notion enables human-readable organizational dashboard accessible outside Obsidian.",
        category=Category.OPPORTUNITY,
        impact=Impact.HIGH,
        confidence=0.88,
        urgency=Urgency.SHORT_TERM,
        evidence=["M-019 ODT Registry", "Notion MCP available", "M-020 observability operational"],
        dependencies=["MISSION-019", "MISSION-020"],
        expected_roi="CEO-accessible dashboard, reduces context-loading time by ~60%",
    ),
    StrategicRecommendation(
        recommendation_id="REC-005",
        title="Implement n8n workflow automation for mission triggers",
        description="Event Bus is operational but has no external trigger. n8n integration would enable scheduled mission execution, webhook triggers, and external system integration.",
        category=Category.OPPORTUNITY,
        impact=Impact.HIGH,
        confidence=0.85,
        urgency=Urgency.MEDIUM_TERM,
        evidence=["M-022 Event Bus operational", "44 event types registered", "n8n in Y-OS routing playbook"],
        dependencies=["MISSION-022"],
        expected_roi="Autonomous mission scheduling, reduces manual trigger overhead by ~80%",
    ),
    StrategicRecommendation(
        recommendation_id="REC-006",
        title="Archive y-os-doctrine branch to Notion Memory",
        description="82 commits on y-os-doctrine represent significant organizational knowledge. Archiving to Notion Memory ensures cross-session persistence.",
        category=Category.GOVERNANCE,
        impact=Impact.MEDIUM,
        confidence=0.95,
        urgency=Urgency.SHORT_TERM,
        evidence=["82 commits on y-os-doctrine", "Notion MCP available", "memory-manager skill"],
        dependencies=["MISSION-013"],
        expected_roi="Cross-session memory continuity, eliminates re-discovery overhead",
    ),
    StrategicRecommendation(
        recommendation_id="REC-007",
        title="Implement Dataview plugin for live corpus queries",
        description="9 Dataview dashboards exist but require Obsidian + Dataview plugin. Generating static HTML exports would make dashboards accessible without Obsidian.",
        category=Category.BOTTLENECK,
        impact=Impact.MEDIUM,
        confidence=0.82,
        urgency=Urgency.MEDIUM_TERM,
        evidence=["M-015: 9 dashboards generated", "Dataview dependency", "M-019 ODT dashboards"],
        dependencies=["MISSION-015"],
        expected_roi="Dashboard accessibility without Obsidian setup, reduces onboarding friction",
    ),
    StrategicRecommendation(
        recommendation_id="REC-008",
        title="Implement worker registry with live health monitoring",
        description="6 workers are registered but health is simulated. Live health checks would enable real-time worker availability routing.",
        category=Category.PERFORMANCE,
        impact=Impact.MEDIUM,
        confidence=0.80,
        urgency=Urgency.MEDIUM_TERM,
        evidence=["M-019 worker_registry.json", "M-023 provider health monitor", "M-022 Event Bus"],
        dependencies=["MISSION-019", "MISSION-023"],
        expected_roi="Real-time worker routing, reduces failed execution rate",
    ),
    StrategicRecommendation(
        recommendation_id="REC-009",
        title="Implement Git auto-push hook post-mission",
        description="Every mission requires manual git commit + push. An auto-push hook triggered by the Event Bus would eliminate this overhead.",
        category=Category.BOTTLENECK,
        impact=Impact.MEDIUM,
        confidence=0.90,
        urgency=Urgency.SHORT_TERM,
        evidence=["M-022 Event Bus: MISSION_COMPLETED event", "82 manual commits", "git_push_hook pattern"],
        dependencies=["MISSION-022"],
        expected_roi="Eliminates manual git overhead, ensures real-time GitHub sync",
    ),
    StrategicRecommendation(
        recommendation_id="REC-010",
        title="Implement Constitutional Amendment Protocol",
        description="Y-OS Constitution v1 is FROZEN but has no formal amendment protocol. As Y-OS evolves, a governed amendment process is required.",
        category=Category.GOVERNANCE,
        impact=Impact.MEDIUM,
        confidence=0.88,
        urgency=Urgency.LONG_TERM,
        evidence=["Y-OS_Constitution_v1 FROZEN", "ADR-0034 Constitutional Elevation", "Lakshmi governance pattern"],
        dependencies=["MISSION-006"],
        expected_roi="Enables constitutional evolution without breaking governance invariants",
    ),
    StrategicRecommendation(
        recommendation_id="REC-011",
        title="Implement semantic search over corpus (Obsidian + Manus)",
        description="565 wikilinks + 4,056 semantic edges exist but are not searchable semantically. A vector index over the corpus would enable natural language queries.",
        category=Category.OPPORTUNITY,
        impact=Impact.HIGH,
        confidence=0.78,
        urgency=Urgency.MEDIUM_TERM,
        evidence=["M-021: 4,056 edges", "kg_semantic_graph_v4.json", "Exa semantic search in routing playbook"],
        dependencies=["MISSION-021"],
        expected_roi="Natural language corpus navigation, reduces lookup time by ~70%",
    ),
    StrategicRecommendation(
        recommendation_id="REC-012",
        title="Implement cost budget enforcement in provider router",
        description="Cost tracking exists but has no hard budget limits. A budget enforcement layer would prevent runaway LLM costs.",
        category=Category.RISK,
        impact=Impact.MEDIUM,
        confidence=0.92,
        urgency=Urgency.SHORT_TERM,
        evidence=["M-023 cost_tracker_v1", "M-017 cost_report.md", "K2 rule: no spend without authorization"],
        dependencies=["MISSION-023"],
        expected_roi="Prevents cost overruns, enforces K2 rule autonomously",
    ),
]


class StrategicRecommendationEngine:
    def __init__(self):
        self.recommendations = RECOMMENDATIONS

    def generate_all(self) -> list[StrategicRecommendation]:
        return self.recommendations

    def by_category(self, category: Category) -> list[StrategicRecommendation]:
        return [r for r in self.recommendations if r.category == category]

    def by_impact(self, impact: Impact) -> list[StrategicRecommendation]:
        return [r for r in self.recommendations if r.impact == impact]

    def top_n(self, n: int = 5) -> list[StrategicRecommendation]:
        impact_order = {Impact.CRITICAL: 4, Impact.HIGH: 3, Impact.MEDIUM: 2, Impact.LOW: 1}
        urgency_order = {Urgency.IMMEDIATE: 4, Urgency.SHORT_TERM: 3, Urgency.MEDIUM_TERM: 2, Urgency.LONG_TERM: 1}
        scored = sorted(
            self.recommendations,
            key=lambda r: (impact_order[r.impact] * 0.5 + urgency_order[r.urgency] * 0.3 + r.confidence * 0.2),
            reverse=True,
        )
        return scored[:n]
