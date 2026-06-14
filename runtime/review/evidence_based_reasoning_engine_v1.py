#!/usr/bin/env python3
"""
Module 3: Evidence-Based Reasoning Engine v1 — Y-OS MISSION-025
Hard constraint: No recommendation without evidence.
Sources: missions, ADRs, artifacts, events, metrics, dashboards.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from strategic_recommendation_engine_v1 import StrategicRecommendation


@dataclass
class EvidenceRecord:
    recommendation_id: str
    evidence_count: int
    evidence_items: list[str]
    sources: list[str]
    validated: bool
    validation_reason: str

    def to_dict(self) -> dict:
        return {
            "recommendation_id": self.recommendation_id,
            "evidence_count": self.evidence_count,
            "evidence_items": self.evidence_items,
            "sources": self.sources,
            "validated": self.validated,
            "validation_reason": self.validation_reason,
        }


SOURCE_MAP = {
    "ADR": "ADR Registry (ADR-0006 → ADR-0054)",
    "M-": "Mission Registry (M-001 → M-025)",
    "ART-": "Artifact Registry",
    "Event Bus": "Event Registry (44 event types)",
    "EIS": "Executive Intelligence Score Dashboard",
    "Graph Quality": "Graph Quality Dashboard",
    "provider": "Provider Registry (3 providers)",
    "cost": "Cost Tracker",
    "Lakshmi": "Governance Review Registry",
    "Constitution": "Y-OS Constitution v1",
    "kg_semantic": "Knowledge Graph v4 (4,056 edges)",
    "orphan": "Graph Quality Audit (M-021)",
    "Notion": "Notion Memory (MCP)",
    "n8n": "n8n Routing Playbook",
    "K2": "Y-OS Operating Rules",
}


class EvidenceBasedReasoningEngine:
    def validate_all(self, recommendations: list[StrategicRecommendation]) -> list[EvidenceRecord]:
        records = []
        for rec in recommendations:
            sources = []
            for ev in rec.evidence:
                for key, source in SOURCE_MAP.items():
                    if key.lower() in ev.lower() and source not in sources:
                        sources.append(source)
            validated = len(rec.evidence) >= 2
            reason = (
                f"✅ {len(rec.evidence)} evidence items from {len(sources)} sources"
                if validated
                else f"❌ Insufficient evidence: {len(rec.evidence)} items"
            )
            records.append(EvidenceRecord(
                recommendation_id=rec.recommendation_id,
                evidence_count=len(rec.evidence),
                evidence_items=rec.evidence,
                sources=sources if sources else ["Corpus analysis"],
                validated=validated,
                validation_reason=reason,
            ))
        return records

    def coverage_rate(self, records: list[EvidenceRecord]) -> float:
        if not records:
            return 0.0
        return round(sum(1 for r in records if r.validated) / len(records) * 100, 1)
