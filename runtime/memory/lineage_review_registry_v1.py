#!/usr/bin/env python3
"""
Module 4: Lineage Review Registry v1 — Y-OS MISSION-022A
Produces mission_lineage_registry_v2.json with confidence scoring.
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import asdict
from semantic_relationship_inference_v1 import CandidateEdge
from legacy_lineage_recovery_engine_v1 import LegacyMission


class LineageReviewRegistry:
    def __init__(self):
        self.registry: dict = {}

    def build(self, legacy_missions: list[LegacyMission],
              edges: list[CandidateEdge]) -> dict:
        # Group edges by source mission
        edges_by_source: dict[str, list[CandidateEdge]] = {}
        for e in edges:
            if e.source not in edges_by_source:
                edges_by_source[e.source] = []
            edges_by_source[e.source].append(e)

        for m in legacy_missions:
            m_edges = edges_by_source.get(m.mission_id, [])
            adr_edges = [e for e in m_edges if e.relationship_type in ("implements", "references")
                         and "ADR-" in e.target]
            dep_edges = [e for e in m_edges if e.relationship_type == "depends_on"]
            concept_edges = [e for e in m_edges if e.relationship_type == "produces"]
            gov_edges = [e for e in m_edges if e.relationship_type == "governed_by"]

            self.registry[m.mission_id] = {
                "mission_id": m.mission_id,
                "title": m.title,
                "mission_num": m.mission_num,
                "is_legacy": True,
                "total_inferred_edges": len(m_edges),
                "adr_links": [{"target": e.target, "rel": e.relationship_type,
                                "confidence": e.confidence_score,
                                "band": e.confidence_band,
                                "review_required": e.human_review_required,
                                "reason": e.inference_reason}
                               for e in adr_edges],
                "dependencies": [{"target": e.target, "rel": e.relationship_type,
                                   "confidence": e.confidence_score,
                                   "band": e.confidence_band}
                                  for e in dep_edges],
                "concepts_produced": [e.target for e in concept_edges],
                "governance": [e.target for e in gov_edges],
                "has_adr_link": len(adr_edges) > 0,
                "lineage_complete": len(adr_edges) > 0 or len(dep_edges) > 0,
            }

        return self.registry

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.registry, indent=2), encoding="utf-8")

    def compute_coverage(self) -> float:
        if not self.registry:
            return 0.0
        with_lineage = sum(1 for v in self.registry.values() if v["lineage_complete"])
        return with_lineage / len(self.registry) * 100
