#!/usr/bin/env python3
"""
Module 2: Organizational Snapshot Engine v1 — Y-OS MISSION-024
Generates snapshots for missions, ADRs, workers, providers, artifacts, graph, ODT.
"""
from __future__ import annotations
import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from odt_time_machine_v1 import ODTSnapshot, MISSION_HISTORY, ADR_HISTORY

# EIS evolution (approximate from mission reports)
EIS_EVOLUTION = {
    "MISSION-001": 0.0, "MISSION-005": 30.0, "MISSION-009": 45.0,
    "MISSION-012B": 55.0, "MISSION-013": 65.0, "MISSION-015": 72.0,
    "MISSION-017": 78.0, "MISSION-019": 85.0, "MISSION-020": 87.5,
    "MISSION-021": 95.3, "MISSION-022A": 95.3, "MISSION-023": 95.3,
    "MISSION-022": 95.3, "MISSION-024": 96.0,
}

GRAPH_QUALITY_EVOLUTION = {
    "MISSION-013": 65.0, "MISSION-013B": 70.0, "MISSION-014": 75.0,
    "MISSION-015": 82.0, "MISSION-019": 90.8, "MISSION-020": 90.8,
    "MISSION-021": 100.0, "MISSION-022A": 100.0, "MISSION-023": 100.0,
    "MISSION-022": 100.0, "MISSION-024": 100.0,
}

WORKER_COUNTS = {
    "MISSION-001": 0, "MISSION-003": 2, "MISSION-005": 4,
    "MISSION-009": 5, "MISSION-016": 6, "MISSION-017": 6,
    "MISSION-018": 6, "MISSION-024": 6,
}

ARTIFACT_COUNTS = {
    "MISSION-001": 0, "MISSION-013": 5, "MISSION-015": 12,
    "MISSION-017": 16, "MISSION-018": 22, "MISSION-019": 28,
    "MISSION-020": 34, "MISSION-021": 40, "MISSION-022": 50,
    "MISSION-024": 55,
}


def _interpolate(history: dict, mission_id: str, default: float) -> float:
    """Get value from history dict, interpolating from nearest past key."""
    if mission_id in history:
        return history[mission_id]
    # Find last known value before this mission
    missions_order = [m["id"] for m in MISSION_HISTORY]
    try:
        idx = missions_order.index(mission_id)
    except ValueError:
        return default
    for i in range(idx - 1, -1, -1):
        if missions_order[i] in history:
            return history[missions_order[i]]
    return default


class OrganizationalSnapshotEngine:
    def __init__(self):
        self.snapshots: list[ODTSnapshot] = []

    def generate_all(self) -> list[ODTSnapshot]:
        """Generate a snapshot for each mission in history."""
        missions_order = [m["id"] for m in MISSION_HISTORY]
        adrs_by_date: dict[str, int] = {}
        adr_count = 6  # Starting ADR count

        for i, mission in enumerate(MISSION_HISTORY):
            mid = mission["id"]
            # Increment ADR count at key missions
            adr_increments = {
                "MISSION-005": 2, "MISSION-005C": 1, "MISSION-006": 1,
                "MISSION-009": 2, "MISSION-012B": 1, "MISSION-013": 1,
                "MISSION-013B": 1, "MISSION-014": 1, "MISSION-015": 1,
                "MISSION-016": 1, "MISSION-017": 1, "MISSION-018": 1,
                "MISSION-019": 1, "MISSION-020": 1, "MISSION-021A": 1,
                "MISSION-021": 1, "MISSION-022A": 1, "MISSION-023": 1,
                "MISSION-022": 1, "MISSION-024": 1,
            }
            adr_count += adr_increments.get(mid, 0)

            snap = ODTSnapshot(
                snapshot_id=f"SNAP-{mid}",
                timestamp=mission["date"] + "T00:00:00+00:00",
                mission_id=mid,
                missions_count=i + 1,
                adrs_count=adr_count,
                workers_count=int(_interpolate(WORKER_COUNTS, mid, 0)),
                artifacts_count=int(_interpolate(ARTIFACT_COUNTS, mid, 0)),
                graph_quality=_interpolate(GRAPH_QUALITY_EVOLUTION, mid, 0.0),
                eis_score=_interpolate(EIS_EVOLUTION, mid, 0.0),
                phase=mission["phase"],
                lineage=[m["id"] for m in MISSION_HISTORY[:i]],
                metrics={
                    "mission_index": i + 1,
                    "phase": mission["phase"],
                    "adr_count": adr_count,
                },
            )
            self.snapshots.append(snap)

        return self.snapshots

    def save(self, path: Path) -> None:
        data = {
            "total_snapshots": len(self.snapshots),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "snapshots": [s.to_dict() for s in self.snapshots],
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
