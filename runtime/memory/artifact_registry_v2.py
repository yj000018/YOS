#!/usr/bin/env python3
"""
Artifact Registry v2 — Y-OS
ADR-0044

Registers artifacts as Markdown + JSON with stable IDs, lineage, and status tracking.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import hashlib
import json
import uuid


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


@dataclass
class ArtifactRecord:
    artifact_id: str
    mission_id: str
    artifact_type: str          # Worker Output | Governance Review | Learning Report | CEO Briefing | Execution Trace
    worker: str
    capability: str
    provider: str
    model: str
    parent_context_pack_id: str
    parent_artifact_ids: list[str]
    status: str                 # CREATED | VALIDATED | FAILED | SUPERSEDED
    created_at: str
    lineage: dict
    content_hash: str
    content_preview: str        # First 200 chars
    content_path: str           # Relative path to .md file
    validation_verdict: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def to_markdown_header(self) -> str:
        """Generate YAML frontmatter for the artifact file."""
        tags_str = ", ".join(f"'{t}'" for t in self.tags)
        parent_ids_str = "\n".join(f"  - '{p}'" for p in self.parent_artifact_ids) or "  []"
        return (
            f"---\n"
            f"id: {self.artifact_id.lower()}\n"
            f"title: '{self.artifact_type} — {self.mission_id} / {self.worker}'\n"
            f"type: {self.artifact_type.lower().replace(' ', '_')}\n"
            f"artifact_id: {self.artifact_id}\n"
            f"mission_id: {self.mission_id}\n"
            f"worker: {self.worker}\n"
            f"capability: {self.capability}\n"
            f"provider: {self.provider}\n"
            f"model: {self.model}\n"
            f"parent_context_pack_id: {self.parent_context_pack_id}\n"
            f"parent_artifact_ids:\n{parent_ids_str}\n"
            f"status: {self.status}\n"
            f"created_at: '{self.created_at}'\n"
            f"content_hash: {self.content_hash}\n"
            f"validation_verdict: {self.validation_verdict}\n"
            f"tags: [{tags_str}]\n"
            f"---\n\n"
        )


class ArtifactRegistryV2:
    """Manages artifact registration, status updates, and index."""

    def __init__(self, artifacts_dir: Path, registry_file: Path):
        self.artifacts_dir = artifacts_dir
        self.registry_file = registry_file
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self._registry: dict[str, ArtifactRecord] = {}
        self._load_existing()

    def _load_existing(self):
        if self.registry_file.exists():
            try:
                data = json.loads(self.registry_file.read_text(encoding="utf-8"))
                for item in data.get("artifacts", []):
                    rec = ArtifactRecord(**item)
                    self._registry[rec.artifact_id] = rec
            except Exception:
                pass

    def _save_registry(self):
        data = {
            "schema_version": "2.0",
            "mission_id": "MISSION-017",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_artifacts": len(self._registry),
            "artifacts": [r.to_dict() for r in self._registry.values()],
        }
        self.registry_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def register(
        self,
        artifact_id: str,
        mission_id: str,
        artifact_type: str,
        worker: str,
        capability: str,
        provider: str,
        model: str,
        content: str,
        parent_context_pack_id: str = "",
        parent_artifact_ids: Optional[list[str]] = None,
        lineage: Optional[dict] = None,
        tags: Optional[list[str]] = None,
    ) -> ArtifactRecord:
        """Register an artifact and write it to disk."""
        now = datetime.now(timezone.utc).isoformat()
        content_hash = _sha256(content)
        content_preview = content[:200].replace("\n", " ")
        filename = f"{artifact_id}.md"
        content_path = str(self.artifacts_dir / filename)

        record = ArtifactRecord(
            artifact_id=artifact_id,
            mission_id=mission_id,
            artifact_type=artifact_type,
            worker=worker,
            capability=capability,
            provider=provider,
            model=model,
            parent_context_pack_id=parent_context_pack_id,
            parent_artifact_ids=parent_artifact_ids or [],
            status="CREATED",
            created_at=now,
            lineage=lineage or {},
            content_hash=content_hash,
            content_preview=content_preview,
            content_path=content_path,
            tags=tags or ["#artifact", "#yos", f"#{worker.lower()}"],
        )

        # Write artifact Markdown file
        full_content = record.to_markdown_header() + content
        Path(content_path).write_text(full_content, encoding="utf-8")

        # Write artifact JSON
        json_path = self.artifacts_dir / f"{artifact_id}.json"
        json_path.write_text(record.to_json(), encoding="utf-8")

        self._registry[artifact_id] = record
        self._save_registry()
        return record

    def update_status(self, artifact_id: str, status: str, validation_verdict: str = "") -> Optional[ArtifactRecord]:
        """Update artifact status."""
        if artifact_id not in self._registry:
            return None
        rec = self._registry[artifact_id]
        rec.status = status
        if validation_verdict:
            rec.validation_verdict = validation_verdict
        self._save_registry()
        return rec

    def get(self, artifact_id: str) -> Optional[ArtifactRecord]:
        return self._registry.get(artifact_id)

    def list_all(self) -> list[ArtifactRecord]:
        return list(self._registry.values())

    def count(self) -> int:
        return len(self._registry)

    def summary(self) -> dict:
        records = self.list_all()
        return {
            "total": len(records),
            "by_status": {
                "CREATED": sum(1 for r in records if r.status == "CREATED"),
                "VALIDATED": sum(1 for r in records if r.status == "VALIDATED"),
                "FAILED": sum(1 for r in records if r.status == "FAILED"),
                "SUPERSEDED": sum(1 for r in records if r.status == "SUPERSEDED"),
            },
            "by_worker": {
                w: sum(1 for r in records if r.worker == w)
                for w in set(r.worker for r in records)
            },
            "by_provider": {
                p: sum(1 for r in records if r.provider == p)
                for p in set(r.provider for r in records)
            },
        }
