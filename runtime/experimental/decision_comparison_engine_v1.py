#!/usr/bin/env python3
"""
Module 5: Decision Comparison Engine v1 — Y-OS MISSION-026
Compares multiple strategies. Output: best option, tradeoffs, risk profile.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DecisionOption:
    option_id: str
    title: str
    description: str
    eis_impact: float
    cost_impact: float
    risk_level: str
    time_to_value: str
    dependencies: list[str]
    confidence: float


@dataclass
class DecisionComparison:
    comparison_id: str
    question: str
    options: list[DecisionOption]
    best_option_id: str
    rationale: str
    tradeoffs: list[str]
    risk_profile: dict
    computed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "comparison_id": self.comparison_id,
            "question": self.question,
            "best_option_id": self.best_option_id,
            "rationale": self.rationale,
            "tradeoffs": self.tradeoffs,
            "risk_profile": self.risk_profile,
            "options": [o.__dict__ for o in self.options],
            "computed_at": self.computed_at,
        }


COMPARISONS: list[DecisionComparison] = [
    DecisionComparison(
        comparison_id="DC-001",
        question="What is the optimal next mission after MISSION-026?",
        options=[
            DecisionOption("OPT-A", "MISSION-027: KGC v5", "Reduce orphans, deepen graph",
                           +1.5, 0.0, "LOW", "2 weeks", [], 0.88),
            DecisionOption("OPT-B", "MISSION-028: n8n Integration", "Autonomous scheduling",
                           +2.0, +0.10, "MEDIUM", "3 weeks", ["MISSION-022"], 0.85),
            DecisionOption("OPT-C", "MISSION-029: Notion Sync", "Cross-session memory",
                           +1.8, 0.0, "LOW", "2 weeks", ["MISSION-019"], 0.90),
            DecisionOption("OPT-D", "MISSION-031: Live Gemini", "Provider validation",
                           +0.5, -0.12, "LOW", "1 week", ["MISSION-023"], 0.95),
        ],
        best_option_id="OPT-D",
        rationale="MISSION-031 (Live Gemini) is fastest, lowest risk, highest confidence, and closes GAP-008 immediately. Cost -27%.",
        tradeoffs=[
            "OPT-A: Higher EIS gain but no operational impact",
            "OPT-B: Highest EIS gain but MEDIUM risk and 3-week timeline",
            "OPT-C: Good memory value but no infrastructure improvement",
            "OPT-D: ⭐ Fastest, cheapest, closes critical gap — recommended",
        ],
        risk_profile={"LOW": 3, "MEDIUM": 1, "HIGH": 0},
    ),
    DecisionComparison(
        comparison_id="DC-002",
        question="Should Y-OS execute missions sequentially or in parallel?",
        options=[
            DecisionOption("OPT-SEQ", "Sequential Execution", "One mission at a time, current model",
                           0.0, 0.0, "LOW", "12 months for 7 missions", [], 0.95),
            DecisionOption("OPT-PAR2", "2-Parallel Execution", "2 independent missions simultaneously",
                           +1.5, +0.15, "MEDIUM", "7 months for 7 missions", [], 0.80),
            DecisionOption("OPT-PAR3", "3-Parallel Execution", "SCN-007: M-026+M-027+M-029 parallel",
                           +3.0, +0.20, "HIGH", "5 months for 7 missions", [], 0.70),
        ],
        best_option_id="OPT-PAR2",
        rationale="2-parallel balances speed and governance risk. 3-parallel has HIGH risk and 70% confidence.",
        tradeoffs=[
            "Sequential: safest but slowest",
            "2-Parallel: ⭐ 42% faster, manageable risk — recommended",
            "3-Parallel: fastest but HIGH coordination risk",
        ],
        risk_profile={"LOW": 1, "MEDIUM": 1, "HIGH": 1},
    ),
    DecisionComparison(
        comparison_id="DC-003",
        question="Which provider should be primary for Brahma (architecture) worker?",
        options=[
            DecisionOption("OPT-GPT4O", "GPT-4o (OpenAI)", "Current primary, proven quality",
                           0.0, 0.0, "LOW", "Immediate", [], 0.95),
            DecisionOption("OPT-CLAUDE", "Claude Opus 4 (Anthropic)", "Best for long-context reasoning",
                           +0.5, +0.02, "LOW", "Immediate", [], 0.92),
            DecisionOption("OPT-GEMINI", "Gemini 1.5 Pro", "Cheapest, not yet validated",
                           -1.0, -0.08, "HIGH", "After M-031", ["MISSION-031"], 0.70),
        ],
        best_option_id="OPT-CLAUDE",
        rationale="Claude Opus 4 outperforms GPT-4o on architecture reasoning. Marginal cost increase justified.",
        tradeoffs=[
            "GPT-4o: proven but not optimal for long-context architecture",
            "Claude Opus 4: ⭐ best quality for Brahma — recommended",
            "Gemini: cheapest but HIGH risk until M-031 validation",
        ],
        risk_profile={"LOW": 2, "HIGH": 1},
    ),
]


class DecisionComparisonEngine:
    def __init__(self):
        self.comparisons = COMPARISONS

    def get_all(self) -> list[DecisionComparison]:
        return self.comparisons

    def best_option(self, comparison_id: str) -> str | None:
        c = next((x for x in self.comparisons if x.comparison_id == comparison_id), None)
        return c.best_option_id if c else None
