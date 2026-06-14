#!/usr/bin/env python3
"""
Artifact Chaining Engine v1 — Y-OS
ADR-0045

Creates parent-child links between artifacts and validates chain integrity.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json


@dataclass
class ChainLink:
    parent_artifact_id: str
    child_artifact_id: str
    relationship: str = "produces"   # produces | validates | supersedes
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ArtifactChainingEngine:
    """Manages artifact parent-child relationships and chain integrity."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.chain: list[ChainLink] = []
        self.artifact_order: list[str] = []  # Ordered list of artifact IDs

    def add_link(self, parent_id: str, child_id: str, relationship: str = "produces") -> ChainLink:
        link = ChainLink(parent_artifact_id=parent_id, child_artifact_id=child_id, relationship=relationship)
        self.chain.append(link)
        if parent_id not in self.artifact_order:
            self.artifact_order.append(parent_id)
        if child_id not in self.artifact_order:
            self.artifact_order.append(child_id)
        return link

    def validate_chain_integrity(self) -> dict:
        """Validate that the chain is complete and each artifact has a parent."""
        issues = []
        # Check each artifact (except the first) has a parent
        for i, art_id in enumerate(self.artifact_order[1:], 1):
            has_parent = any(link.child_artifact_id == art_id for link in self.chain)
            if not has_parent:
                issues.append(f"{art_id} has no parent link")

        # Check no cycles (simple: each artifact appears as child at most once)
        child_counts = {}
        for link in self.chain:
            child_counts[link.child_artifact_id] = child_counts.get(link.child_artifact_id, 0) + 1
        for art_id, count in child_counts.items():
            if count > 3:  # Allow multiple parents (Saraswati consumes 2)
                issues.append(f"{art_id} has {count} parent links — possible cycle")

        integrity_score = 100 if not issues else max(0, 100 - len(issues) * 20)
        return {
            "valid": len(issues) == 0,
            "integrity_score": integrity_score,
            "chain_length": len(self.artifact_order),
            "links": len(self.chain),
            "issues": issues,
        }

    def save(self) -> None:
        """Write chain to JSON and Markdown."""
        data = {
            "schema_version": "1.0",
            "mission_id": "MISSION-018",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "chain_length": len(self.artifact_order),
            "artifact_order": self.artifact_order,
            "links": [asdict(l) for l in self.chain],
            "integrity": self.validate_chain_integrity(),
        }
        (self.base_dir / "artifact_chain.json").write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )

        # Markdown
        integrity = self.validate_chain_integrity()
        md_lines = [
            "---",
            "id: yos-artifact-chain-mission-018",
            "title: Artifact Chain — MISSION-018",
            "type: artifact_chain",
            "mission_id: MISSION-018",
            f"integrity_score: {integrity['integrity_score']}",
            "tags: ['#artifact-chain', '#yos', '#mission-018']",
            "---",
            "",
            "# Artifact Chain — MISSION-018",
            "",
            f"**Chain Length:** {len(self.artifact_order)}  ",
            f"**Links:** {len(self.chain)}  ",
            f"**Integrity Score:** {integrity['integrity_score']}/100  ",
            f"**Valid:** {'✅ YES' if integrity['valid'] else '❌ NO'}  ",
            "",
            "## Chain Sequence",
            "",
        ]
        for i, art_id in enumerate(self.artifact_order):
            arrow = "→ " if i > 0 else ""
            md_lines.append(f"{arrow}[[{art_id}]]")
        md_lines += [
            "",
            "## Links",
            "",
            "| Parent | Child | Relationship |",
            "| :--- | :--- | :--- |",
        ]
        for link in self.chain:
            md_lines.append(f"| [[{link.parent_artifact_id}]] | [[{link.child_artifact_id}]] | {link.relationship} |")
        (self.base_dir / "artifact_chain.md").write_text("\n".join(md_lines), encoding="utf-8")
