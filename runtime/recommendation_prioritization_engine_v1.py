#!/usr/bin/env python3
"""
Module 5: Recommendation Prioritization Engine v1 — Y-OS MISSION-025
Ranks recommendations using: Impact, Urgency, Risk Reduction, Cost Reduction,
Strategic Leverage, Dependency Readiness.
"""
from __future__ import annotations
from dataclasses import dataclass
from strategic_recommendation_engine_v1 import StrategicRecommendation, Impact, Urgency


IMPACT_SCORE = {Impact.CRITICAL: 40, Impact.HIGH: 30, Impact.MEDIUM: 20, Impact.LOW: 10}
URGENCY_SCORE = {Urgency.IMMEDIATE: 30, Urgency.SHORT_TERM: 20, Urgency.MEDIUM_TERM: 10, Urgency.LONG_TERM: 5}

CATEGORY_LEVERAGE = {
    "RISK": 15,
    "STRATEGIC_GAP": 15,
    "OPPORTUNITY": 12,
    "BOTTLENECK": 10,
    "TECHNICAL_DEBT": 8,
    "GOVERNANCE": 8,
    "PERFORMANCE": 7,
    "ARCHITECTURE": 7,
}


@dataclass
class PriorityEntry:
    recommendation_id: str
    title: str
    rank: int
    priority_score: float
    impact_score: float
    urgency_score: float
    confidence_score: float
    leverage_score: float
    breakdown: dict

    def to_dict(self) -> dict:
        return {
            "rank": self.rank,
            "recommendation_id": self.recommendation_id,
            "title": self.title,
            "priority_score": self.priority_score,
            "breakdown": self.breakdown,
        }


class RecommendationPrioritizationEngine:
    def prioritize(self, recommendations: list[StrategicRecommendation]) -> list[PriorityEntry]:
        entries = []
        for rec in recommendations:
            imp = IMPACT_SCORE.get(rec.impact, 20)
            urg = URGENCY_SCORE.get(rec.urgency, 10)
            conf = rec.confidence * 15
            lev = CATEGORY_LEVERAGE.get(rec.category.value, 7)
            dep_ready = 5 if not rec.dependencies else 3
            total = round(imp + urg + conf + lev + dep_ready, 2)

            entries.append(PriorityEntry(
                recommendation_id=rec.recommendation_id,
                title=rec.title,
                rank=0,
                priority_score=total,
                impact_score=imp,
                urgency_score=urg,
                confidence_score=conf,
                leverage_score=lev,
                breakdown={
                    "impact": imp,
                    "urgency": urg,
                    "confidence": round(conf, 2),
                    "leverage": lev,
                    "dependency_readiness": dep_ready,
                    "total": total,
                },
            ))

        entries.sort(key=lambda e: e.priority_score, reverse=True)
        for i, e in enumerate(entries, 1):
            e.rank = i

        return entries

    def to_queue(self, entries: list[PriorityEntry]) -> list[dict]:
        return [e.to_dict() for e in entries]
