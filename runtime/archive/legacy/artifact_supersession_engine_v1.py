#!/usr/bin/env python3
"""
Artifact Supersession Engine v1 — Y-OS
ADR-0045

Safely supersedes artifacts by marking old as SUPERSEDED and creating new version.
Never deletes artifacts.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json


@dataclass
class SupersessionRecord:
    supersession_id: str
    old_artifact_id: str
    new_artifact_id: str
    reason: str
    mission_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ArtifactSupersessionEngine:
    """Manages artifact supersession lifecycle."""

    def __init__(self, registry, base_dir: Path):
        self.registry = registry
        self.base_dir = base_dir
        self.supersessions: list[SupersessionRecord] = []

    def supersede(
        self,
        old_artifact_id: str,
        new_artifact_id: str,
        reason: str,
        mission_id: str = "MISSION-018",
    ) -> SupersessionRecord:
        """Mark old artifact as SUPERSEDED and record the supersession."""
        # Update old artifact status
        self.registry.update_status(old_artifact_id, "SUPERSEDED")

        record = SupersessionRecord(
            supersession_id=f"SUP-{old_artifact_id}->{new_artifact_id}",
            old_artifact_id=old_artifact_id,
            new_artifact_id=new_artifact_id,
            reason=reason,
            mission_id=mission_id,
        )
        self.supersessions.append(record)

        # Write supersession record
        sup_file = self.base_dir / f"supersession_{record.supersession_id.replace('>', '_')}.json"
        sup_file.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")
        return record

    def get_active_version(self, base_artifact_id: str) -> str:
        """Return the latest non-superseded version of an artifact."""
        # Find if this artifact was superseded
        for sup in self.supersessions:
            if sup.old_artifact_id == base_artifact_id:
                return self.get_active_version(sup.new_artifact_id)
        return base_artifact_id

    def count(self) -> int:
        return len(self.supersessions)
