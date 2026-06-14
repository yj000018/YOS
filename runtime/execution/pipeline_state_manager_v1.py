#!/usr/bin/env python3
"""
Pipeline State Manager v1 — Y-OS
ADR-0045

Persists pipeline state to JSON + Markdown.
Tracks steps, artifacts, checkpoints, and rollback points.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json
import uuid


@dataclass
class PipelineStep:
    step_id: int
    worker: str
    capability: str
    status: str = "PENDING"   # PENDING | RUNNING | COMPLETED | FAILED | ROLLED_BACK
    artifact_id: str = ""
    context_pack_id: str = ""
    trace_id: str = ""
    started_at: str = ""
    completed_at: str = ""
    error: str = ""


@dataclass
class Checkpoint:
    checkpoint_id: str
    step_id: int
    worker: str
    pipeline_status_snapshot: str
    active_artifacts: list[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RollbackEvent:
    rollback_id: str
    trigger_step_id: int
    rollback_to_step_id: int
    reason: str
    failed_artifact_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PipelineStateManager:
    """Manages pipeline state persistence and lifecycle."""

    def __init__(self, mission_id: str, base_dir: Path):
        self.mission_id = mission_id
        self.base_dir = base_dir
        self.pipeline_id = f"PIPE-{uuid.uuid4().hex[:8].upper()}"
        self.status = "INITIALIZED"
        self.steps: list[PipelineStep] = []
        self.active_artifacts: list[str] = []
        self.parent_artifact_chain: list[str] = []
        self.checkpoints: list[Checkpoint] = []
        self.rollback_events: list[RollbackEvent] = []
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.completed_at = ""
        self._save()

    def add_step(self, step_id: int, worker: str, capability: str) -> PipelineStep:
        step = PipelineStep(step_id=step_id, worker=worker, capability=capability)
        self.steps.append(step)
        self._save()
        return step

    def start_step(self, step_id: int) -> None:
        step = self._get_step(step_id)
        if step:
            step.status = "RUNNING"
            step.started_at = datetime.now(timezone.utc).isoformat()
            self.status = "RUNNING"
            self._save()

    def complete_step(self, step_id: int, artifact_id: str, context_pack_id: str = "", trace_id: str = "") -> None:
        step = self._get_step(step_id)
        if step:
            step.status = "COMPLETED"
            step.artifact_id = artifact_id
            step.context_pack_id = context_pack_id
            step.trace_id = trace_id
            step.completed_at = datetime.now(timezone.utc).isoformat()
            if artifact_id and artifact_id not in self.active_artifacts:
                self.active_artifacts.append(artifact_id)
            if artifact_id and artifact_id not in self.parent_artifact_chain:
                self.parent_artifact_chain.append(artifact_id)
            self._save()

    def fail_step(self, step_id: int, error: str, artifact_id: str = "") -> None:
        step = self._get_step(step_id)
        if step:
            step.status = "FAILED"
            step.error = error[:200]
            step.completed_at = datetime.now(timezone.utc).isoformat()
            if artifact_id:
                step.artifact_id = artifact_id
            self.status = "FAILED"
            self._save()

    def create_checkpoint(self, step_id: int, worker: str) -> Checkpoint:
        cp = Checkpoint(
            checkpoint_id=f"CP-{self.pipeline_id}-STEP{step_id}",
            step_id=step_id,
            worker=worker,
            pipeline_status_snapshot=self.status,
            active_artifacts=list(self.active_artifacts),
        )
        self.checkpoints.append(cp)
        # Write checkpoint file
        cp_file = self.base_dir / "checkpoints" / f"{cp.checkpoint_id}.json"
        cp_file.write_text(json.dumps(asdict(cp), indent=2), encoding="utf-8")
        self.status = "CHECKPOINTED"
        self._save()
        return cp

    def record_rollback(self, trigger_step: int, rollback_to: int, reason: str, failed_artifact_id: str = "") -> RollbackEvent:
        rb = RollbackEvent(
            rollback_id=f"RB-{self.pipeline_id}-STEP{trigger_step}",
            trigger_step_id=trigger_step,
            rollback_to_step_id=rollback_to,
            reason=reason,
            failed_artifact_id=failed_artifact_id,
        )
        self.rollback_events.append(rb)
        # Write rollback event file
        rb_file = self.base_dir / "rollback_events" / f"{rb.rollback_id}.json"
        rb_file.write_text(json.dumps(asdict(rb), indent=2), encoding="utf-8")
        self.status = "ROLLED_BACK"
        self._save()
        return rb

    def complete_pipeline(self) -> None:
        self.status = "COMPLETED"
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self._save()

    def _get_step(self, step_id: int) -> Optional[PipelineStep]:
        for s in self.steps:
            if s.step_id == step_id:
                return s
        return None

    def _to_dict(self) -> dict:
        return {
            "pipeline_id": self.pipeline_id,
            "mission_id": self.mission_id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "current_step": next((s.step_id for s in self.steps if s.status == "RUNNING"), None),
            "completed_steps": [s.step_id for s in self.steps if s.status == "COMPLETED"],
            "failed_steps": [s.step_id for s in self.steps if s.status == "FAILED"],
            "active_artifacts": self.active_artifacts,
            "parent_artifact_chain": self.parent_artifact_chain,
            "steps": [asdict(s) for s in self.steps],
            "checkpoints": [asdict(c) for c in self.checkpoints],
            "rollback_events": [asdict(r) for r in self.rollback_events],
        }

    def _save(self) -> None:
        data = self._to_dict()
        # JSON
        json_file = self.base_dir / "pipeline_state.json"
        json_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        # Markdown
        md_lines = [
            "---",
            f"id: yos-pipeline-{self.pipeline_id.lower()}",
            f"title: Pipeline State — {self.mission_id}",
            f"type: pipeline_state",
            f"pipeline_id: {self.pipeline_id}",
            f"mission_id: {self.mission_id}",
            f"status: {self.status}",
            f"started_at: '{self.started_at}'",
            f"tags: ['#pipeline', '#yos', '#mission-018']",
            "---",
            "",
            f"# Pipeline State — {self.mission_id}",
            "",
            f"**Pipeline ID:** {self.pipeline_id}  ",
            f"**Status:** {self.status}  ",
            f"**Started:** {self.started_at}  ",
            f"**Completed:** {self.completed_at or 'In progress'}  ",
            "",
            "## Steps",
            "",
            "| Step | Worker | Capability | Status | Artifact |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for s in self.steps:
            md_lines.append(f"| {s.step_id} | {s.worker} | {s.capability} | {s.status} | {s.artifact_id or '—'} |")
        md_lines += [
            "",
            "## Active Artifacts",
            "",
        ]
        for a in self.active_artifacts:
            md_lines.append(f"- [[{a}]]")
        md_lines += [
            "",
            f"## Checkpoints: {len(self.checkpoints)}",
            f"## Rollback Events: {len(self.rollback_events)}",
        ]
        md_file = self.base_dir / "pipeline_state.md"
        md_file.write_text("\n".join(md_lines), encoding="utf-8")

    def summary(self) -> dict:
        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "total_steps": len(self.steps),
            "completed": len([s for s in self.steps if s.status == "COMPLETED"]),
            "failed": len([s for s in self.steps if s.status == "FAILED"]),
            "checkpoints": len(self.checkpoints),
            "rollback_events": len(self.rollback_events),
            "active_artifacts": len(self.active_artifacts),
        }
