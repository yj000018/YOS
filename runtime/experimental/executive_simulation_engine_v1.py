#!/usr/bin/env python3
"""
Module 1: Executive Simulation Engine v1 — Y-OS MISSION-026
Runs organizational simulations: current_state + proposed_change → predicted_future_state
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import math


class SimulationStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class OrgState:
    """Snapshot of key Y-OS organizational metrics."""
    graph_quality: float = 100.0
    eis_score: float = 96.0
    mission_lineage: float = 100.0
    orphan_rate: float = 7.1
    provider_openai_pct: float = 42.9
    provider_anthropic_pct: float = 28.6
    provider_gemini_pct: float = 28.6
    active_workers: int = 6
    total_missions: int = 25
    total_adrs: int = 54
    total_artifacts: int = 22
    monthly_cost_usd: float = 0.45
    governance_compliance: float = 96.8
    event_bus_active: bool = True
    notion_sync: bool = False
    semantic_search: bool = False
    simulation_layer: bool = False

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def delta(self, other: "OrgState") -> dict:
        result = {}
        for k, v in self.__dict__.items():
            ov = getattr(other, k, v)
            if v != ov:
                result[k] = {"before": v, "after": ov, "delta": ov - v if isinstance(v, (int, float)) else "changed"}
        return result


@dataclass
class SimulationResult:
    simulation_id: str
    scenario_id: str
    proposed_change: str
    initial_state: OrgState
    predicted_state: OrgState
    confidence: float
    risk_level: str
    key_impacts: list[str]
    warnings: list[str]
    status: SimulationStatus
    computed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "simulation_id": self.simulation_id,
            "scenario_id": self.scenario_id,
            "proposed_change": self.proposed_change,
            "initial_state": self.initial_state.to_dict(),
            "predicted_state": self.predicted_state.to_dict(),
            "state_delta": self.initial_state.delta(self.predicted_state),
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "key_impacts": self.key_impacts,
            "warnings": self.warnings,
            "status": self.status.value,
            "computed_at": self.computed_at,
        }


class ExecutiveSimulationEngine:
    """
    Deterministic simulation engine.
    Each scenario type has a known impact model derived from Y-OS history.
    """

    def __init__(self):
        self._sim_counter = 0

    def _next_id(self, scenario_id: str) -> str:
        self._sim_counter += 1
        return f"SIM-{scenario_id}-{self._sim_counter:03d}"

    def run(
        self,
        scenario_id: str,
        proposed_change: str,
        current_state: OrgState,
        impact_model: dict,
        confidence: float = 0.85,
        warnings: list[str] | None = None,
    ) -> SimulationResult:
        predicted = OrgState(**current_state.to_dict())

        for attr, delta in impact_model.items():
            if hasattr(predicted, attr):
                current_val = getattr(predicted, attr)
                if isinstance(current_val, bool):
                    setattr(predicted, attr, bool(delta))
                elif isinstance(current_val, (int, float)):
                    setattr(predicted, attr, round(current_val + delta, 2))

        key_impacts = [
            f"{k}: {current_state.to_dict().get(k, '?')} → {predicted.to_dict().get(k, '?')}"
            for k in impact_model
            if k in current_state.to_dict()
        ]

        # Risk: high if EIS drops or governance drops
        eis_delta = predicted.eis_score - current_state.eis_score
        gov_delta = predicted.governance_compliance - current_state.governance_compliance
        risk = "LOW"
        if eis_delta < -5 or gov_delta < -5:
            risk = "HIGH"
        elif eis_delta < -2 or gov_delta < -2:
            risk = "MEDIUM"

        return SimulationResult(
            simulation_id=self._next_id(scenario_id),
            scenario_id=scenario_id,
            proposed_change=proposed_change,
            initial_state=current_state,
            predicted_state=predicted,
            confidence=confidence,
            risk_level=risk,
            key_impacts=key_impacts,
            warnings=warnings or [],
            status=SimulationStatus.COMPLETED,
        )
