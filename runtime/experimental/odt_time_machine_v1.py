#!/usr/bin/env python3
"""
Module 1: ODT Time Machine v1 — Y-OS MISSION-024
Main temporal navigation engine: load_snapshot, replay_to_date, compare_snapshots, timeline_view.
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


# ── Y-OS Mission History (ground truth from corpus) ───────────────────────────
MISSION_HISTORY = [
    {"id": "MISSION-001", "title": "Y-OS Foundation", "date": "2025-01-01", "phase": "Foundation"},
    {"id": "MISSION-002", "title": "Constitution Draft", "date": "2025-01-15", "phase": "Foundation"},
    {"id": "MISSION-003", "title": "Worker Registry v1", "date": "2025-02-01", "phase": "Foundation"},
    {"id": "MISSION-004", "title": "Governance Framework", "date": "2025-02-15", "phase": "Foundation"},
    {"id": "MISSION-005", "title": "CCR Runtime v1", "date": "2025-03-01", "phase": "Runtime"},
    {"id": "MISSION-005C", "title": "Governance Determinism", "date": "2025-03-15", "phase": "Governance"},
    {"id": "MISSION-006", "title": "Constitutional Elevation", "date": "2025-04-01", "phase": "Governance"},
    {"id": "MISSION-007", "title": "Artifact Primacy", "date": "2025-04-15", "phase": "Artifacts"},
    {"id": "MISSION-008", "title": "Context Architecture", "date": "2025-05-01", "phase": "Context"},
    {"id": "MISSION-009", "title": "Executable Constitution", "date": "2025-05-15", "phase": "Governance"},
    {"id": "MISSION-010", "title": "Context Architecture v2", "date": "2025-06-01", "phase": "Context"},
    {"id": "MISSION-011", "title": "CCR Runtime v2 Design", "date": "2025-06-15", "phase": "Runtime"},
    {"id": "MISSION-012", "title": "Session Delta Engine", "date": "2025-07-01", "phase": "Memory"},
    {"id": "MISSION-012B", "title": "Living Memory Pipeline", "date": "2025-07-15", "phase": "Memory"},
    {"id": "MISSION-013", "title": "Knowledge Graph Compiler v1", "date": "2025-08-01", "phase": "Graph"},
    {"id": "MISSION-013B", "title": "Graph Quality Audit", "date": "2025-08-15", "phase": "Graph"},
    {"id": "MISSION-014", "title": "Cognitive Graph Architecture", "date": "2025-09-01", "phase": "Graph"},
    {"id": "MISSION-015", "title": "KGC v2 Visual Drill-Down", "date": "2025-09-15", "phase": "Graph"},
    {"id": "MISSION-016", "title": "CCR Runtime v2 Implementation", "date": "2025-10-01", "phase": "Runtime"},
    {"id": "MISSION-017", "title": "Live Worker Execution", "date": "2025-10-15", "phase": "Execution"},
    {"id": "MISSION-018", "title": "Multi-Worker Pipeline", "date": "2025-11-01", "phase": "Execution"},
    {"id": "MISSION-019", "title": "Organizational Digital Twin", "date": "2025-11-15", "phase": "ODT"},
    {"id": "MISSION-020", "title": "Autonomous Observability", "date": "2025-12-01", "phase": "ODT"},
    {"id": "MISSION-021A", "title": "Roadmap Architecture Review", "date": "2025-12-10", "phase": "Planning"},
    {"id": "MISSION-021", "title": "Semantic Connectivity Layer", "date": "2025-12-15", "phase": "Graph"},
    {"id": "MISSION-022A", "title": "Legacy Lineage Recovery", "date": "2026-01-01", "phase": "Graph"},
    {"id": "MISSION-023", "title": "Provider Diversification", "date": "2026-01-15", "phase": "Providers"},
    {"id": "MISSION-022", "title": "Live Event Bus", "date": "2026-02-01", "phase": "Events"},
    {"id": "MISSION-024", "title": "ODT Time Machine", "date": "2026-06-14", "phase": "ODT"},
]

ADR_HISTORY = [
    {"id": f"ADR-{str(i).zfill(4)}", "date": "2025-01-01", "status": "ACCEPTED"}
    for i in range(6, 53)
] + [{"id": "ADR-0053", "date": "2026-06-14", "status": "PROPOSED"}]


@dataclass
class ODTSnapshot:
    snapshot_id: str
    timestamp: str
    mission_id: str
    missions_count: int
    adrs_count: int
    workers_count: int
    artifacts_count: int
    graph_quality: float
    eis_score: float
    phase: str
    lineage: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp,
            "mission_id": self.mission_id,
            "missions_count": self.missions_count,
            "adrs_count": self.adrs_count,
            "workers_count": self.workers_count,
            "artifacts_count": self.artifacts_count,
            "graph_quality": self.graph_quality,
            "eis_score": self.eis_score,
            "phase": self.phase,
            "lineage": self.lineage,
            "metrics": self.metrics,
        }


class ODTTimeMachine:
    def __init__(self, snapshots: list[ODTSnapshot]):
        self.snapshots = sorted(snapshots, key=lambda s: s.timestamp)
        self._index = {s.snapshot_id: s for s in self.snapshots}

    def load_snapshot(self, snapshot_id: str) -> Optional[ODTSnapshot]:
        return self._index.get(snapshot_id)

    def replay_to_date(self, target_date: str) -> list[ODTSnapshot]:
        """Return all snapshots up to target_date."""
        return [s for s in self.snapshots if s.timestamp <= target_date]

    def compare_snapshots(self, snap_a: ODTSnapshot, snap_b: ODTSnapshot) -> dict:
        """Compare two snapshots and return diff."""
        return {
            "from": snap_a.snapshot_id,
            "to": snap_b.snapshot_id,
            "delta_missions": snap_b.missions_count - snap_a.missions_count,
            "delta_adrs": snap_b.adrs_count - snap_a.adrs_count,
            "delta_artifacts": snap_b.artifacts_count - snap_a.artifacts_count,
            "delta_graph_quality": round(snap_b.graph_quality - snap_a.graph_quality, 1),
            "delta_eis": round(snap_b.eis_score - snap_a.eis_score, 1),
            "phase_change": snap_a.phase != snap_b.phase,
            "from_phase": snap_a.phase,
            "to_phase": snap_b.phase,
        }

    def timeline_view(self) -> list[dict]:
        """Return chronological timeline of all snapshots."""
        return [
            {
                "snapshot_id": s.snapshot_id,
                "mission_id": s.mission_id,
                "timestamp": s.timestamp,
                "phase": s.phase,
                "missions": s.missions_count,
                "adrs": s.adrs_count,
                "graph_quality": s.graph_quality,
                "eis": s.eis_score,
            }
            for s in self.snapshots
        ]

    def get_phase_transitions(self) -> list[dict]:
        transitions = []
        prev = None
        for s in self.snapshots:
            if prev and prev.phase != s.phase:
                transitions.append({
                    "from_phase": prev.phase,
                    "to_phase": s.phase,
                    "at_mission": s.mission_id,
                    "timestamp": s.timestamp,
                })
            prev = s
        return transitions
