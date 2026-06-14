#!/usr/bin/env python3
"""
Module 2: Semantic Relationship Inference v1 — Y-OS MISSION-022A
Infers typed relationships for legacy missions using multiple signals.
Confidence: HIGH >0.90, MEDIUM 0.75-0.90, LOW <0.75
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
from legacy_lineage_recovery_engine_v1 import LegacyMission


@dataclass
class CandidateEdge:
    source: str
    target: str
    relationship_type: str
    confidence_score: float
    confidence_band: str  # HIGH / MEDIUM / LOW
    inference_reason: str
    human_review_required: bool
    inferred_at: str = ""

    def __post_init__(self):
        if not self.inferred_at:
            self.inferred_at = datetime.now(timezone.utc).isoformat()
        if self.confidence_score >= 0.90:
            self.confidence_band = "HIGH"
            self.human_review_required = False
        elif self.confidence_score >= 0.75:
            self.confidence_band = "MEDIUM"
            self.human_review_required = True
        else:
            self.confidence_band = "LOW"
            self.human_review_required = True


# ── Semantic keyword maps ─────────────────────────────────────────────────────

ADR_TOPIC_MAP = {
    # ADR prefix → topic keywords
    "ADR-0006": ["codo", "chief", "officer"],
    "ADR-0007": ["evolution", "loop", "continuous"],
    "ADR-0009": ["operational", "value", "chain"],
    "ADR-0010": ["brahma", "architect", "architecture"],
    "ADR-0011": ["hanuman", "build", "executor"],
    "ADR-0012": ["artifact", "layer", "primacy"],
    "ADR-0013": ["lakshmi", "governance", "review"],
    "ADR-0014": ["org", "map", "organizational"],
    "ADR-0015": ["worker", "registry", "roles"],
    "ADR-0016": ["context", "pack", "injection"],
    "ADR-0017": ["session", "memory", "persistence"],
    "ADR-0018": ["model", "registry", "provider"],
    "ADR-0019": ["pipeline", "orchestration"],
    "ADR-0020": ["constitution", "governance", "principles"],
    "ADR-0021": ["artifact", "primacy", "preservation"],
    "ADR-0022": ["derivation", "transparency", "lineage"],
    "ADR-0023": ["human", "override", "control"],
    "ADR-0024": ["governance", "autonomy", "before"],
    "ADR-0025": ["ccr", "context", "router"],
    "ADR-0026": ["session", "delta", "compression"],
    "ADR-0027": ["worker", "specialization"],
    "ADR-0028": ["artifact", "registry", "versioning"],
    "ADR-0029": ["ccr", "runtime", "v1"],
    "ADR-0030": ["ccr", "runtime", "v1", "mission"],
}

MISSION_TOPIC_MAP = {
    # Mission prefix → topic keywords
    "MISSION-001": ["constitution", "founding", "principles"],
    "MISSION-002": ["worker", "roles", "brahma", "hanuman"],
    "MISSION-003": ["artifact", "layer", "primacy"],
    "MISSION-004": ["context", "pack", "ccr"],
    "MISSION-005": ["ccr", "runtime", "governance"],
    "MISSION-006": ["constitutional", "elevation"],
    "MISSION-007": ["org", "map", "structure"],
    "MISSION-008": ["session", "memory", "delta"],
    "MISSION-009": ["executable", "constitution"],
    "MISSION-010": ["context", "architecture"],
    "MISSION-011": ["ccr", "runtime", "v2"],
    "MISSION-012": ["session", "delta", "engine"],
    "MISSION-012A": ["storage", "audit", "persistence"],
    "MISSION-012B": ["living", "memory", "pipeline"],
}


class SemanticRelationshipInference:
    def __init__(self, root: Path, all_adrs: dict, all_missions: dict):
        self.root = root
        self.all_adrs = all_adrs  # prefix -> full_id
        self.all_missions = all_missions  # full_id -> file_path
        self.edges: list[CandidateEdge] = []
        self._edge_set: set[tuple] = set()

    def _add_edge(self, src: str, tgt: str, rel: str, conf: float, reason: str) -> bool:
        key = (src, tgt, rel)
        if key in self._edge_set:
            return False
        self._edge_set.add(key)
        edge = CandidateEdge(
            source=src, target=tgt, relationship_type=rel,
            confidence_score=conf, confidence_band="",
            inference_reason=reason, human_review_required=False,
        )
        self.edges.append(edge)
        return True

    def infer_all(self, legacy_missions: list[LegacyMission]) -> list[CandidateEdge]:
        for mission in legacy_missions:
            self._infer_for_mission(mission)
        return self.edges

    def _infer_for_mission(self, m: LegacyMission) -> None:
        body = m.body_text.lower()
        m_id = m.mission_id

        # ── 1. ADR references in body (HIGH confidence) ───────────────────────
        for adr_num in set(re.findall(r"ADR-(\d+)", m.body_text)):
            key = f"ADR-{int(adr_num):04d}"
            full_adr = self.all_adrs.get(key)
            if full_adr:
                self._add_edge(m_id, full_adr, "implements",
                               0.95, f"Explicit ADR-{adr_num} reference in body")

        # ── 2. Existing ADRs already found ────────────────────────────────────
        for adr_id in m.existing_adrs:
            self._add_edge(m_id, adr_id, "implements",
                           0.95, "Existing ADR reference (already in frontmatter)")

        # ── 3. Keyword-based ADR inference (MEDIUM confidence) ────────────────
        for adr_prefix, keywords in ADR_TOPIC_MAP.items():
            full_adr = self.all_adrs.get(adr_prefix)
            if not full_adr:
                continue
            matches = sum(1 for kw in keywords if kw in body)
            if matches >= 2:
                conf = min(0.88, 0.70 + matches * 0.05)
                self._add_edge(m_id, full_adr, "references",
                               conf, f"Keyword match ({matches}/{len(keywords)}): {keywords[:3]}")
            elif matches == 1:
                conf = 0.72
                self._add_edge(m_id, full_adr, "references",
                               conf, f"Single keyword match: {keywords[0]}")

        # ── 4. Mission sequential dependency (HIGH confidence) ────────────────
        # Each mission depends_on the previous one
        prev_num = int(m.mission_num) - 1
        if prev_num >= 1:
            prev_patterns = [
                f"MISSION-{prev_num:03d}",
                f"MISSION-0{prev_num:02d}",
                f"MISSION-{prev_num}",
            ]
            for prev_pat in prev_patterns:
                for full_id in self.all_missions:
                    if full_id.startswith(prev_pat):
                        self._add_edge(m_id, full_id, "depends_on",
                                       0.92, f"Sequential mission dependency (M-{prev_num}→M-{int(m.mission_num)})")
                        break

        # ── 5. Keyword-based mission dependency (MEDIUM confidence) ───────────
        for dep_prefix, keywords in MISSION_TOPIC_MAP.items():
            if dep_prefix == m_id[:len(dep_prefix)]:
                continue  # skip self
            matches = sum(1 for kw in keywords if kw in body)
            if matches >= 2:
                for full_id in self.all_missions:
                    if full_id.startswith(dep_prefix):
                        conf = min(0.87, 0.72 + matches * 0.04)
                        self._add_edge(m_id, full_id, "references",
                                       conf, f"Topic overlap ({matches} keywords): {keywords[:3]}")
                        break

        # ── 6. Constitution governance (HIGH confidence for all missions) ─────
        const_id = "Y-OS_Constitution_v1"
        if const_id in self.all_missions or any(
            "constitution" in fp.lower() for fp in self.all_missions.values()
        ):
            # Find constitution file
            for full_id in self.all_missions:
                if "constitution" in full_id.lower():
                    self._add_edge(m_id, full_id, "governed_by",
                                   0.95, "All Y-OS missions governed by Constitution")
                    break

        # ── 7. Wikilink extraction ─────────────────────────────────────────────
        wikilinks = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", m.body_text)
        for link in wikilinks:
            link_clean = link.strip()
            # Check if it's a mission
            if link_clean in self.all_missions:
                self._add_edge(m_id, link_clean, "references",
                               0.90, f"Explicit wikilink [[{link_clean}]]")
            # Check if it's an ADR
            adr_m = re.match(r"(ADR-\d+)", link_clean)
            if adr_m:
                full_adr = self.all_adrs.get(adr_m.group(1))
                if full_adr:
                    self._add_edge(m_id, full_adr, "implements",
                                   0.93, f"Explicit wikilink [[{link_clean}]]")

        # ── 8. Concept production (MEDIUM confidence) ─────────────────────────
        concept_keywords = {
            "Artifact_Primacy": ["artifact", "primacy", "preservation"],
            "CCR_Runtime": ["ccr", "context", "router", "runtime"],
            "Governance_Determinism": ["governance", "determinism", "lakshmi"],
            "Constitutional_Governance": ["constitution", "governance", "principles"],
            "Living_Memory": ["living", "memory", "pipeline"],
            "Session_Delta": ["session", "delta", "compression"],
        }
        for concept, kws in concept_keywords.items():
            matches = sum(1 for kw in kws if kw in body)
            if matches >= 2:
                self._add_edge(m_id, concept, "produces",
                               0.80, f"Concept keyword match ({matches}): {kws[:3]}")
