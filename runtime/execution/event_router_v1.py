#!/usr/bin/env python3
"""
Module 3: Event Router v1 — Y-OS MISSION-022
Routes events to appropriate subsystem handlers.
"""
from __future__ import annotations
from event_bus_core_v1 import EventBusCore, YOSEvent


# ── Routing Table ─────────────────────────────────────────────────────────────
ROUTING_TABLE = {
    "MISSION_COMPLETED":          ["odt_update_engine", "graph_compiler", "dashboard_refresh"],
    "MISSION_STARTED":            ["odt_update_engine", "execution_trace"],
    "ADR_ACCEPTED":               ["graph_compiler", "kg_update", "dashboard_refresh"],
    "ADR_PROPOSED":               ["governance_review"],
    "ARTIFACT_CREATED":           ["artifact_registry", "lineage_tracker", "graph_compiler"],
    "ARTIFACT_VALIDATED":         ["artifact_registry", "dashboard_refresh"],
    "ARTIFACT_SUPERSEDED":        ["artifact_registry", "lineage_tracker"],
    "PROVIDER_FAILED":            ["failover_engine", "health_monitor", "dashboard_refresh"],
    "PROVIDER_DEGRADED":          ["health_monitor", "dashboard_refresh"],
    "PROVIDER_RECOVERED":         ["health_monitor", "dashboard_refresh"],
    "PROVIDER_SWITCHED":          ["lineage_tracker", "cost_tracker"],
    "PIPELINE_COMPLETED":         ["odt_update_engine", "artifact_registry"],
    "PIPELINE_CHECKPOINT":        ["checkpoint_engine"],
    "PIPELINE_ROLLBACK":          ["checkpoint_engine", "lineage_tracker"],
    "GOVERNANCE_APPROVED":        ["dashboard_refresh", "artifact_registry"],
    "GOVERNANCE_REJECTED":        ["governance_review", "execution_trace"],
    "CONSTITUTION_VIOLATION":     ["governance_review", "alert_engine"],
    "GRAPH_COMPILED":             ["dashboard_refresh", "odt_update_engine"],
    "GRAPH_QUALITY_UPDATED":      ["dashboard_refresh"],
    "GRAPH_ORPHAN_DETECTED":      ["kg_update", "alert_engine"],
    "MEMORY_SESSION_STORED":      ["odt_update_engine", "lineage_tracker"],
    "MEMORY_PIPELINE_COMPLETED":  ["dashboard_refresh"],
    "DASHBOARD_REFRESH_REQUESTED": ["dashboard_refresh"],
    "DASHBOARD_ALERT_RAISED":     ["alert_engine"],
}


class EventRouter:
    def __init__(self, bus: EventBusCore):
        self.bus = bus
        self.routing_log: list[dict] = []
        self._handlers: dict[str, list] = {}

    def register_handler(self, subsystem: str, handler) -> None:
        if subsystem not in self._handlers:
            self._handlers[subsystem] = []
        self._handlers[subsystem].append(handler)

    def route(self, event: YOSEvent) -> list[str]:
        """Route event to all registered subsystems. Returns list of subsystems notified."""
        targets = ROUTING_TABLE.get(event.event_type, [])
        notified = []
        for target in targets:
            handlers = self._handlers.get(target, [])
            for h in handlers:
                try:
                    h(event)
                except Exception:
                    pass
            notified.append(target)

        self.routing_log.append({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "targets": targets,
            "notified": notified,
            "timestamp": event.timestamp,
        })
        return notified

    def get_routing_table(self) -> dict:
        return ROUTING_TABLE

    def get_log(self) -> list[dict]:
        return self.routing_log
