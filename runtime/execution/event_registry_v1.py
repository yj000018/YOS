#!/usr/bin/env python3
"""
Module 2: Event Registry v1 — Y-OS MISSION-022
Registers all event types across 10 categories.
"""
from __future__ import annotations
import json
from pathlib import Path

EVENT_REGISTRY = {
    "MISSION": [
        "MISSION_STARTED", "MISSION_COMPLETED", "MISSION_FAILED", "MISSION_PAUSED",
    ],
    "ADR": [
        "ADR_PROPOSED", "ADR_ACCEPTED", "ADR_SUPERSEDED", "ADR_DEPRECATED",
    ],
    "ARTIFACT": [
        "ARTIFACT_CREATED", "ARTIFACT_VALIDATED", "ARTIFACT_SUPERSEDED",
        "ARTIFACT_ARCHIVED", "ARTIFACT_LINEAGE_UPDATED",
    ],
    "WORKER": [
        "WORKER_ASSIGNED", "WORKER_COMPLETED", "WORKER_FAILED", "WORKER_RETRIED",
    ],
    "PROVIDER": [
        "PROVIDER_HEALTHY", "PROVIDER_DEGRADED", "PROVIDER_FAILED",
        "PROVIDER_RECOVERED", "PROVIDER_SWITCHED",
    ],
    "PIPELINE": [
        "PIPELINE_STARTED", "PIPELINE_STEP_COMPLETED", "PIPELINE_COMPLETED",
        "PIPELINE_CHECKPOINT", "PIPELINE_ROLLBACK",
    ],
    "GOVERNANCE": [
        "GOVERNANCE_REVIEW_STARTED", "GOVERNANCE_APPROVED", "GOVERNANCE_REJECTED",
        "GOVERNANCE_WARNING", "CONSTITUTION_VIOLATION",
    ],
    "GRAPH": [
        "GRAPH_NODE_ADDED", "GRAPH_EDGE_ADDED", "GRAPH_COMPILED",
        "GRAPH_QUALITY_UPDATED", "GRAPH_ORPHAN_DETECTED",
    ],
    "MEMORY": [
        "MEMORY_SESSION_STORED", "MEMORY_CONTEXT_LOADED", "MEMORY_DELTA_COMPUTED",
        "MEMORY_PIPELINE_COMPLETED",
    ],
    "DASHBOARD": [
        "DASHBOARD_REFRESH_REQUESTED", "DASHBOARD_UPDATED", "DASHBOARD_ALERT_RAISED",
    ],
}

ALL_EVENT_TYPES = [et for types in EVENT_REGISTRY.values() for et in types]


class EventRegistry:
    def __init__(self):
        self.registry = EVENT_REGISTRY

    def get_all_types(self) -> list[str]:
        return ALL_EVENT_TYPES

    def get_category(self, event_type: str) -> str:
        for cat, types in self.registry.items():
            if event_type in types:
                return cat
        return "UNKNOWN"

    def is_valid(self, event_type: str) -> bool:
        return event_type in ALL_EVENT_TYPES

    def to_json(self) -> dict:
        return {
            "total_event_types": len(ALL_EVENT_TYPES),
            "categories": len(self.registry),
            "registry": self.registry,
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")
