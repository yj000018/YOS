#!/usr/bin/env python3
"""
Module 4: Snapshot Diff Engine v1 — Y-OS MISSION-024
Compare Mission A→B, ADR X→Y, ODT State T1→T2. Metrics: added, removed, modified, impact score.
"""
from __future__ import annotations
from dataclasses import dataclass
from odt_time_machine_v1 import ODTSnapshot


@dataclass
class SnapshotDiff:
    from_id: str
    to_id: str
    added_missions: int
    added_adrs: int
    added_artifacts: int
    delta_graph_quality: float
    delta_eis: float
    phase_changed: bool
    from_phase: str
    to_phase: str
    impact_score: float

    def to_dict(self) -> dict:
        return {
            "from": self.from_id,
            "to": self.to_id,
            "added_missions": self.added_missions,
            "added_adrs": self.added_adrs,
            "added_artifacts": self.added_artifacts,
            "delta_graph_quality": self.delta_graph_quality,
            "delta_eis": self.delta_eis,
            "phase_changed": self.phase_changed,
            "from_phase": self.from_phase,
            "to_phase": self.to_phase,
            "impact_score": self.impact_score,
        }


class SnapshotDiffEngine:
    def compare(self, snap_a: ODTSnapshot, snap_b: ODTSnapshot) -> SnapshotDiff:
        added_m = snap_b.missions_count - snap_a.missions_count
        added_a = snap_b.adrs_count - snap_a.adrs_count
        added_art = snap_b.artifacts_count - snap_a.artifacts_count
        dq = round(snap_b.graph_quality - snap_a.graph_quality, 1)
        de = round(snap_b.eis_score - snap_a.eis_score, 1)
        phase_changed = snap_a.phase != snap_b.phase

        # Impact score: weighted sum of changes
        impact = (
            added_m * 5 +
            added_a * 3 +
            added_art * 2 +
            abs(dq) * 1.5 +
            abs(de) * 1.0 +
            (20 if phase_changed else 0)
        )

        return SnapshotDiff(
            from_id=snap_a.snapshot_id,
            to_id=snap_b.snapshot_id,
            added_missions=added_m,
            added_adrs=added_a,
            added_artifacts=added_art,
            delta_graph_quality=dq,
            delta_eis=de,
            phase_changed=phase_changed,
            from_phase=snap_a.phase,
            to_phase=snap_b.phase,
            impact_score=round(impact, 1),
        )

    def compare_sequence(self, snapshots: list[ODTSnapshot]) -> list[SnapshotDiff]:
        diffs = []
        for i in range(1, len(snapshots)):
            diffs.append(self.compare(snapshots[i - 1], snapshots[i]))
        return diffs
