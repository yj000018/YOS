#!/usr/bin/env python3
"""
Module 6: Simulation Memory Engine v1 — Y-OS MISSION-026
Stores simulations, predictions, actual outcomes for future calibration.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class PredictionStatus(str, Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    REFUTED = "REFUTED"
    EXPIRED = "EXPIRED"


@dataclass
class SimulationRecord:
    record_id: str
    simulation_id: str
    scenario_id: str
    prediction: str
    predicted_value: float | str | bool
    actual_value: float | str | bool | None
    status: PredictionStatus
    confidence: float
    calibration_error: float | None
    notes: str
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "simulation_id": self.simulation_id,
            "scenario_id": self.scenario_id,
            "prediction": self.prediction,
            "predicted_value": self.predicted_value,
            "actual_value": self.actual_value,
            "status": self.status.value,
            "confidence": self.confidence,
            "calibration_error": self.calibration_error,
            "notes": self.notes,
            "recorded_at": self.recorded_at,
        }


class SimulationMemoryEngine:
    def __init__(self):
        self.registry: list[SimulationRecord] = []
        self._counter = 0

    def record(
        self,
        simulation_id: str,
        scenario_id: str,
        prediction: str,
        predicted_value: float | str | bool,
        confidence: float,
        notes: str = "",
    ) -> SimulationRecord:
        self._counter += 1
        rec = SimulationRecord(
            record_id=f"SREC-{self._counter:04d}",
            simulation_id=simulation_id,
            scenario_id=scenario_id,
            prediction=prediction,
            predicted_value=predicted_value,
            actual_value=None,
            status=PredictionStatus.PENDING,
            confidence=confidence,
            calibration_error=None,
            notes=notes,
        )
        self.registry.append(rec)
        return rec

    def validate(self, record_id: str, actual_value: float | str | bool) -> SimulationRecord:
        for rec in self.registry:
            if rec.record_id == record_id:
                rec.actual_value = actual_value
                rec.status = PredictionStatus.VALIDATED
                if isinstance(rec.predicted_value, (int, float)) and isinstance(actual_value, (int, float)):
                    rec.calibration_error = round(abs(float(actual_value) - float(rec.predicted_value)), 4)
                return rec
        raise ValueError(f"Record {record_id} not found")

    def calibration_score(self) -> float:
        validated = [r for r in self.registry if r.status == PredictionStatus.VALIDATED and r.calibration_error is not None]
        if not validated:
            return 1.0
        avg_error = sum(r.calibration_error for r in validated) / len(validated)
        return round(max(0.0, 1.0 - avg_error / 10.0), 3)

    def summary(self) -> dict:
        by_status = {}
        for r in self.registry:
            by_status.setdefault(r.status.value, 0)
            by_status[r.status.value] += 1
        return {
            "total_records": len(self.registry),
            "by_status": by_status,
            "calibration_score": self.calibration_score(),
        }

    def to_registry(self) -> list[dict]:
        return [r.to_dict() for r in self.registry]
