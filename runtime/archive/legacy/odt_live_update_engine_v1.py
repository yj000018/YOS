#!/usr/bin/env python3
"""
ODT Live Update Engine v1 — Y-OS
ADR-0047

Automatically updates the Digital Twin when:
- Mission completes
- ADR accepted
- Pipeline executes
- Artifact registered
- Governance review completed

Flow: Mission → Registry Update → Graph Update → Dashboard Update → Canvas Update → ODT Refresh
Generates: odt_update_log.jsonl

Requirements: Fully additive, no destructive updates, Git traceable, idempotent.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class UpdateEvent:
    event_id: str
    event_type: str   # mission_complete | adr_accepted | pipeline_executed | artifact_registered | governance_reviewed
    source: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: dict = field(default_factory=dict)
    result: str = "PENDING"   # PENDING | APPLIED | SKIPPED | FAILED
    idempotent_key: str = ""


@dataclass
class UpdateResult:
    event_id: str
    steps_executed: list[str]
    registry_updated: bool
    graph_updated: bool
    dashboard_updated: bool
    canvas_updated: bool
    odt_refreshed: bool
    result: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ODTLiveUpdateEngine:
    """Processes update events and propagates changes through the ODT layers."""

    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.log_path = corpus_root / "mission_020" / "odt_update_log.jsonl"
        self._applied_keys: set[str] = set()
        self._load_applied_keys()

    def _load_applied_keys(self) -> None:
        if self.log_path.exists():
            for line in self.log_path.read_text().splitlines():
                try:
                    entry = json.loads(line)
                    if entry.get("result") == "APPLIED" and entry.get("idempotent_key"):
                        self._applied_keys.add(entry["idempotent_key"])
                except Exception:
                    pass

    def _log(self, event: UpdateEvent) -> None:
        self.log_path.parent.mkdir(exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event)) + "\n")

    def process_event(self, event: UpdateEvent) -> UpdateResult:
        """Process a single update event through all ODT layers."""
        steps = []

        # Idempotency check
        if event.idempotent_key and event.idempotent_key in self._applied_keys:
            event.result = "SKIPPED"
            self._log(event)
            return UpdateResult(
                event_id=event.event_id, steps_executed=["idempotency_check:SKIPPED"],
                registry_updated=False, graph_updated=False,
                dashboard_updated=False, canvas_updated=False, odt_refreshed=False,
                result="SKIPPED",
            )

        # Step 1: Registry Update
        try:
            self._update_registry(event)
            steps.append("registry_update:OK")
            registry_updated = True
        except Exception as e:
            steps.append(f"registry_update:FAILED:{e}")
            registry_updated = False

        # Step 2: Graph Update (mark as dirty, full recompile on next run)
        try:
            dirty_flag = self.corpus_root / ".kg_dirty"
            dirty_flag.write_text(f"{event.event_id}\n{event.timestamp}\n")
            steps.append("graph_update:DIRTY_FLAG_SET")
            graph_updated = True
        except Exception as e:
            steps.append(f"graph_update:FAILED:{e}")
            graph_updated = False

        # Step 3: Dashboard Update (touch timestamp)
        try:
            ts_file = self.corpus_root / "10_Live_Dashboards" / ".last_update"
            ts_file.parent.mkdir(exist_ok=True)
            ts_file.write_text(f"{event.timestamp}\n{event.event_id}\n")
            steps.append("dashboard_update:TIMESTAMP_UPDATED")
            dashboard_updated = True
        except Exception as e:
            steps.append(f"dashboard_update:FAILED:{e}")
            dashboard_updated = False

        # Step 4: Canvas Update (touch timestamp)
        try:
            ts_file = self.corpus_root / "08_Visual_Maps" / ".last_update"
            ts_file.parent.mkdir(exist_ok=True)
            ts_file.write_text(f"{event.timestamp}\n{event.event_id}\n")
            steps.append("canvas_update:TIMESTAMP_UPDATED")
            canvas_updated = True
        except Exception as e:
            steps.append(f"canvas_update:FAILED:{e}")
            canvas_updated = False

        # Step 5: ODT Refresh (write refresh marker)
        try:
            refresh_file = self.corpus_root / "mission_020" / "odt_refresh_marker.json"
            refresh_data = {
                "last_event": event.event_id,
                "event_type": event.event_type,
                "source": event.source,
                "timestamp": event.timestamp,
                "steps": steps,
            }
            refresh_file.write_text(json.dumps(refresh_data, indent=2))
            steps.append("odt_refresh:MARKER_WRITTEN")
            odt_refreshed = True
        except Exception as e:
            steps.append(f"odt_refresh:FAILED:{e}")
            odt_refreshed = False

        event.result = "APPLIED"
        if event.idempotent_key:
            self._applied_keys.add(event.idempotent_key)
        self._log(event)

        return UpdateResult(
            event_id=event.event_id, steps_executed=steps,
            registry_updated=registry_updated, graph_updated=graph_updated,
            dashboard_updated=dashboard_updated, canvas_updated=canvas_updated,
            odt_refreshed=odt_refreshed, result="APPLIED",
        )

    def _update_registry(self, event: UpdateEvent) -> None:
        """Append event to registry change log."""
        change_log = self.corpus_root / "mission_020" / "registry_change_log.jsonl"
        change_log.parent.mkdir(exist_ok=True)
        with change_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "event_id": event.event_id,
                "event_type": event.event_type,
                "source": event.source,
                "timestamp": event.timestamp,
                "payload": event.payload,
            }) + "\n")

    def simulate_mission_complete(self, mission_id: str) -> UpdateResult:
        """Simulate a mission completion event."""
        event = UpdateEvent(
            event_id=f"EVT-{mission_id}-COMPLETE",
            event_type="mission_complete",
            source=mission_id,
            payload={"mission_id": mission_id, "status": "PASSED"},
            idempotent_key=f"mission_complete:{mission_id}",
        )
        return self.process_event(event)

    def simulate_adr_accepted(self, adr_id: str) -> UpdateResult:
        event = UpdateEvent(
            event_id=f"EVT-{adr_id}-ACCEPTED",
            event_type="adr_accepted",
            source=adr_id,
            payload={"adr_id": adr_id, "status": "ACCEPTED"},
            idempotent_key=f"adr_accepted:{adr_id}",
        )
        return self.process_event(event)

    def simulate_artifact_registered(self, artifact_id: str) -> UpdateResult:
        event = UpdateEvent(
            event_id=f"EVT-{artifact_id}-REGISTERED",
            event_type="artifact_registered",
            source=artifact_id,
            payload={"artifact_id": artifact_id},
            idempotent_key=f"artifact_registered:{artifact_id}",
        )
        return self.process_event(event)
