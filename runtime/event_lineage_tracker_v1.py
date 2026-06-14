#!/usr/bin/env python3
"""
Module 7: Event Lineage Tracker v1 — Y-OS MISSION-022
Tracks: event → artifact, event → mission, event → ADR, event → dashboard, event → provider.
Maintains full traceability.
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from event_bus_core_v1 import YOSEvent


@dataclass
class LineageEdge:
    event_id: str
    event_type: str
    source_entity_type: str   # mission / adr / artifact / provider / dashboard
    source_entity_id: str
    target_entity_type: str
    target_entity_id: str
    relationship: str         # produced / triggered / updated / validated
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EventLineageTracker:
    def __init__(self):
        self.edges: list[LineageEdge] = []

    def track(self, event: YOSEvent) -> list[LineageEdge]:
        """Infer and record lineage edges from event."""
        new_edges = []
        et = event.event_type
        payload = event.payload

        # MISSION events
        if et == "MISSION_COMPLETED":
            mid = payload.get("mission_id", event.source)
            for adr in payload.get("adrs_produced", []):
                new_edges.append(LineageEdge(
                    event_id=event.event_id, event_type=et,
                    source_entity_type="mission", source_entity_id=mid,
                    target_entity_type="adr", target_entity_id=adr,
                    relationship="produced",
                ))
            for art in payload.get("artifacts_produced", []):
                new_edges.append(LineageEdge(
                    event_id=event.event_id, event_type=et,
                    source_entity_type="mission", source_entity_id=mid,
                    target_entity_type="artifact", target_entity_id=art,
                    relationship="produced",
                ))

        # ADR events
        elif et == "ADR_ACCEPTED":
            adr_id = payload.get("adr_id", event.source)
            mission = payload.get("mission_id", "unknown")
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="mission", source_entity_id=mission,
                target_entity_type="adr", target_entity_id=adr_id,
                relationship="validated",
            ))

        # ARTIFACT events
        elif et == "ARTIFACT_CREATED":
            art_id = payload.get("artifact_id", event.source)
            worker = payload.get("worker", "unknown")
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="worker", source_entity_id=worker,
                target_entity_type="artifact", target_entity_id=art_id,
                relationship="produced",
            ))

        # PROVIDER events
        elif et in ("PROVIDER_FAILED", "PROVIDER_SWITCHED"):
            pid = payload.get("provider_id", event.source)
            fallback = payload.get("fallback_provider", "unknown")
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="provider", source_entity_id=pid,
                target_entity_type="provider", target_entity_id=fallback,
                relationship="triggered",
            ))

        # GOVERNANCE events
        elif et == "GOVERNANCE_APPROVED":
            subject = payload.get("subject_id", event.source)
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="governance", source_entity_id="lakshmi",
                target_entity_type="artifact", target_entity_id=subject,
                relationship="validated",
            ))
            # Trigger dashboard update
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="governance", source_entity_id="lakshmi",
                target_entity_type="dashboard", target_entity_id="Dashboard_Executive_Cockpit",
                relationship="updated",
            ))

        # DASHBOARD events
        elif et == "DASHBOARD_UPDATED":
            dash_id = payload.get("dashboard_id", "unknown")
            new_edges.append(LineageEdge(
                event_id=event.event_id, event_type=et,
                source_entity_type="event", source_entity_id=event.event_id,
                target_entity_type="dashboard", target_entity_id=dash_id,
                relationship="updated",
            ))

        self.edges.extend(new_edges)
        return new_edges

    def get_lineage_for(self, entity_id: str) -> list[LineageEdge]:
        return [e for e in self.edges
                if e.source_entity_id == entity_id or e.target_entity_id == entity_id]

    def to_json(self) -> dict:
        return {
            "total_edges": len(self.edges),
            "edges": [
                {
                    "event_id": e.event_id,
                    "event_type": e.event_type,
                    "source": f"{e.source_entity_type}:{e.source_entity_id}",
                    "target": f"{e.target_entity_type}:{e.target_entity_id}",
                    "relationship": e.relationship,
                    "timestamp": e.timestamp,
                }
                for e in self.edges
            ],
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")
