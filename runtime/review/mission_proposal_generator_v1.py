#!/usr/bin/env python3
"""
Module 4: Mission Proposal Generator v1 — Y-OS MISSION-025
Generates future mission proposals (MISSION-026+) from gap analysis and recommendations.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class MissionProposal:
    mission_id: str
    title: str
    objective: str
    expected_impact: str
    dependencies: list[str]
    estimated_effort: str   # LOW / MEDIUM / HIGH / VERY_HIGH
    confidence: float
    category: str
    gap_ids: list[str]
    priority_rank: int = 0
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "mission_id": self.mission_id,
            "title": self.title,
            "objective": self.objective,
            "expected_impact": self.expected_impact,
            "dependencies": self.dependencies,
            "estimated_effort": self.estimated_effort,
            "confidence": self.confidence,
            "category": self.category,
            "gap_ids": self.gap_ids,
            "priority_rank": self.priority_rank,
            "generated_at": self.generated_at,
        }


PROPOSALS: list[MissionProposal] = [
    MissionProposal(
        mission_id="MISSION-026",
        title="Executive Simulation Layer",
        objective="Build causal simulation engine: 'If we change X, what happens to Y?' — closes the cognitive loop.",
        expected_impact="CRITICAL — enables strategic decision-making with quantified risk",
        dependencies=["MISSION-025"],
        estimated_effort="HIGH",
        confidence=0.97,
        category="SIMULATION",
        gap_ids=["GAP-001"],
        priority_rank=1,
    ),
    MissionProposal(
        mission_id="MISSION-027",
        title="KGC v5 — Semantic Depth Pass",
        objective="Reduce orphan rate <3%, add concept-to-concept edges, ADR supersession chains, LLM-based Lakshmi.",
        expected_impact="HIGH — Graph Quality 100 → 108+, EIS +3–5",
        dependencies=["MISSION-021", "MISSION-025"],
        estimated_effort="MEDIUM",
        confidence=0.92,
        category="GRAPH",
        gap_ids=["GAP-002", "GAP-004", "GAP-011", "GAP-012", "GAP-013"],
        priority_rank=2,
    ),
    MissionProposal(
        mission_id="MISSION-028",
        title="n8n Integration — Autonomous Mission Scheduling",
        objective="Connect Event Bus to n8n: webhook triggers, scheduled missions, external system integration.",
        expected_impact="HIGH — autonomous execution, eliminates manual triggers",
        dependencies=["MISSION-022", "MISSION-025"],
        estimated_effort="HIGH",
        confidence=0.85,
        category="AUTOMATION",
        gap_ids=["GAP-003", "GAP-015", "GAP-016"],
        priority_rank=3,
    ),
    MissionProposal(
        mission_id="MISSION-029",
        title="Notion ODT Sync + Cross-Session Memory",
        objective="Sync ODT Registry to Notion, implement Mem0 for strategic decisions, archive y-os-doctrine.",
        expected_impact="HIGH — cross-session continuity, CEO-accessible dashboard",
        dependencies=["MISSION-019", "MISSION-025"],
        estimated_effort="MEDIUM",
        confidence=0.90,
        category="MEMORY",
        gap_ids=["GAP-018", "GAP-019", "GAP-020"],
        priority_rank=4,
    ),
    MissionProposal(
        mission_id="MISSION-030",
        title="Constitutional Amendment Protocol",
        objective="Define formal amendment process for Y-OS Constitution v1. Governed evolution without breaking invariants.",
        expected_impact="MEDIUM — governance resilience, long-term constitutional evolution",
        dependencies=["MISSION-006", "MISSION-025"],
        estimated_effort="LOW",
        confidence=0.88,
        category="GOVERNANCE",
        gap_ids=["GAP-010"],
        priority_rank=5,
    ),
    MissionProposal(
        mission_id="MISSION-031",
        title="Live Gemini Integration + Provider Budget Enforcement",
        objective="Validate live Gemini API calls, implement budget_enforcer_v1 with configurable limits.",
        expected_impact="HIGH — true 3-provider resilience, K2 rule enforcement",
        dependencies=["MISSION-023", "MISSION-025"],
        estimated_effort="LOW",
        confidence=0.95,
        category="PROVIDERS",
        gap_ids=["GAP-008", "GAP-009"],
        priority_rank=6,
    ),
    MissionProposal(
        mission_id="MISSION-032",
        title="Dashboard Exporter — Static HTML + Semantic Search",
        objective="Export all Dataview dashboards to static HTML. Implement vector search over corpus.",
        expected_impact="MEDIUM — accessibility without Obsidian, natural language queries",
        dependencies=["MISSION-015", "MISSION-021"],
        estimated_effort="MEDIUM",
        confidence=0.80,
        category="OBSERVABILITY",
        gap_ids=["GAP-002", "GAP-017"],
        priority_rank=7,
    ),
]


class MissionProposalGenerator:
    def __init__(self):
        self.proposals = PROPOSALS

    def generate_all(self) -> list[MissionProposal]:
        return self.proposals

    def top_n(self, n: int = 5) -> list[MissionProposal]:
        return sorted(self.proposals, key=lambda p: p.priority_rank)[:n]
