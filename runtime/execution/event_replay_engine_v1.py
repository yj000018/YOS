#!/usr/bin/env python3
"""
Module 5: Event Replay Engine v1 — Y-OS MISSION-022
Replay historical events to rebuild state, reconstruct timeline, simulate sequences.
Foundation for M-024 Time Machine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from event_persistence_v1 import EventPersistence


@dataclass
class ReplayResult:
    events_replayed: int
    state_reconstructed: dict
    timeline: list[dict]
    replay_duration_ms: float
    success: bool
    errors: list[str] = field(default_factory=list)


class EventReplayEngine:
    def __init__(self, persistence: EventPersistence):
        self.persistence = persistence
        self.replay_log: list[ReplayResult] = []

    def replay_all(self) -> ReplayResult:
        """Replay all events and reconstruct current state."""
        return self._replay(self.persistence.load_all())

    def replay_since(self, since_ts: str) -> ReplayResult:
        """Replay events since timestamp."""
        return self._replay(self.persistence.filter_since(since_ts))

    def replay_by_type(self, event_types: list[str]) -> ReplayResult:
        """Replay only specific event types."""
        events = [e for e in self.persistence.load_all()
                  if e.get("event_type") in event_types]
        return self._replay(events)

    def simulate_sequence(self, event_sequence: list[dict]) -> ReplayResult:
        """Simulate a custom event sequence (for Time Machine)."""
        return self._replay(event_sequence)

    def _replay(self, events: list[dict]) -> ReplayResult:
        start = datetime.now(timezone.utc)
        state: dict = {
            "missions": [], "adrs": [], "artifacts": [],
            "providers": {}, "graph_quality": None,
            "governance_approvals": 0, "dashboards_refreshed": 0,
        }
        timeline = []
        errors = []

        for event in events:
            try:
                et = event.get("event_type", "")
                payload = event.get("payload", {})

                if et == "MISSION_COMPLETED":
                    state["missions"].append(payload.get("mission_id", "unknown"))
                elif et == "ADR_ACCEPTED":
                    state["adrs"].append(payload.get("adr_id", "unknown"))
                elif et == "ARTIFACT_CREATED":
                    state["artifacts"].append(payload.get("artifact_id", "unknown"))
                elif et in ("PROVIDER_FAILED", "PROVIDER_RECOVERED", "PROVIDER_HEALTHY"):
                    pid = payload.get("provider_id", "unknown")
                    state["providers"][pid] = et
                elif et == "GRAPH_QUALITY_UPDATED":
                    state["graph_quality"] = payload.get("score")
                elif et == "GOVERNANCE_APPROVED":
                    state["governance_approvals"] += 1
                elif et == "DASHBOARD_UPDATED":
                    state["dashboards_refreshed"] += 1

                timeline.append({
                    "event_id": event.get("event_id"),
                    "event_type": et,
                    "timestamp": event.get("timestamp"),
                    "source": event.get("source"),
                })
            except Exception as e:
                errors.append(str(e))

        duration = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        result = ReplayResult(
            events_replayed=len(events),
            state_reconstructed=state,
            timeline=timeline,
            replay_duration_ms=round(duration, 2),
            success=len(errors) == 0,
            errors=errors,
        )
        self.replay_log.append(result)
        return result
