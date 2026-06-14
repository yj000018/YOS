#!/usr/bin/env python3
"""
Checkpoint and Rollback Engine v1 — Y-OS
ADR-0045

Creates checkpoints before each worker execution.
Rollback is logical (never deletes artifacts).
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json


@dataclass
class CheckpointRecord:
    checkpoint_id: str
    pipeline_id: str
    step_id: int
    worker: str
    active_artifacts_snapshot: list[str]
    pipeline_status: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RollbackRecord:
    rollback_id: str
    pipeline_id: str
    trigger_step_id: int
    rollback_to_checkpoint_id: str
    reason: str
    failed_artifact_id: str
    artifacts_preserved: list[str]  # All artifacts preserved (never deleted)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CheckpointRollbackEngine:
    """Manages checkpoints and logical rollbacks."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.checkpoints: list[CheckpointRecord] = []
        self.rollbacks: list[RollbackRecord] = []

    def create_checkpoint(
        self,
        pipeline_id: str,
        step_id: int,
        worker: str,
        active_artifacts: list[str],
        pipeline_status: str,
    ) -> CheckpointRecord:
        cp = CheckpointRecord(
            checkpoint_id=f"CKPT-{pipeline_id}-S{step_id}",
            pipeline_id=pipeline_id,
            step_id=step_id,
            worker=worker,
            active_artifacts_snapshot=list(active_artifacts),
            pipeline_status=pipeline_status,
        )
        self.checkpoints.append(cp)
        cp_file = self.base_dir / "checkpoints" / f"{cp.checkpoint_id}.json"
        cp_file.write_text(json.dumps(asdict(cp), indent=2), encoding="utf-8")
        return cp

    def get_latest_checkpoint(self, before_step: int) -> Optional[CheckpointRecord]:
        """Get the most recent checkpoint before a given step."""
        candidates = [c for c in self.checkpoints if c.step_id < before_step]
        return candidates[-1] if candidates else (self.checkpoints[0] if self.checkpoints else None)

    def perform_logical_rollback(
        self,
        pipeline_id: str,
        trigger_step_id: int,
        reason: str,
        all_artifacts: list[str],
        failed_artifact_id: str = "",
    ) -> RollbackRecord:
        """Perform logical rollback — never deletes artifacts."""
        target_cp = self.get_latest_checkpoint(trigger_step_id)
        rollback_to_id = target_cp.checkpoint_id if target_cp else "INITIAL"

        rb = RollbackRecord(
            rollback_id=f"RB-{pipeline_id}-S{trigger_step_id}",
            pipeline_id=pipeline_id,
            trigger_step_id=trigger_step_id,
            rollback_to_checkpoint_id=rollback_to_id,
            reason=reason,
            failed_artifact_id=failed_artifact_id,
            artifacts_preserved=list(all_artifacts),  # ALL artifacts preserved
        )
        self.rollbacks.append(rb)
        rb_file = self.base_dir / "rollback_events" / f"{rb.rollback_id}.json"
        rb_file.write_text(json.dumps(asdict(rb), indent=2), encoding="utf-8")

        # Write rollback Markdown
        md = (
            f"---\n"
            f"id: yos-rollback-{rb.rollback_id.lower()}\n"
            f"title: Rollback Event — {rb.rollback_id}\n"
            f"type: rollback_event\n"
            f"rollback_id: {rb.rollback_id}\n"
            f"pipeline_id: {pipeline_id}\n"
            f"trigger_step: {trigger_step_id}\n"
            f"rollback_to: {rollback_to_id}\n"
            f"artifacts_preserved: {len(all_artifacts)}\n"
            f"tags: ['#rollback', '#yos', '#mission-018']\n"
            f"---\n\n"
            f"# Rollback Event — {rb.rollback_id}\n\n"
            f"**Trigger Step:** {trigger_step_id}  \n"
            f"**Rollback To:** {rollback_to_id}  \n"
            f"**Reason:** {reason}  \n"
            f"**Failed Artifact:** {failed_artifact_id or 'None'}  \n\n"
            f"## Artifacts Preserved (never deleted)\n\n"
        )
        for a in all_artifacts:
            md += f"- [[{a}]]\n"
        md += "\n---\n*Checkpoint/Rollback Engine v1 — Y-OS*\n"
        (self.base_dir / "rollback_events" / f"{rb.rollback_id}.md").write_text(md, encoding="utf-8")
        return rb

    def count_checkpoints(self) -> int:
        return len(self.checkpoints)

    def count_rollbacks(self) -> int:
        return len(self.rollbacks)
