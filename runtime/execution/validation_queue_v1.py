#!/usr/bin/env python3
"""
Validation Queue v1 — Y-OS
ADR-0045

Synchronous validation queue for artifact outputs.
Supports CRITICAL / NORMAL / LOW priority.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json
from collections import deque


PRIORITY_ORDER = {"CRITICAL": 0, "NORMAL": 1, "LOW": 2}


@dataclass
class ValidationQueueItem:
    item_id: str
    artifact_id: str
    artifact_type: str
    content: str
    lineage: dict
    provider: str
    model: str
    context_pack_id: str
    priority: str = "NORMAL"   # CRITICAL | NORMAL | LOW
    status: str = "QUEUED"     # QUEUED | PROCESSING | DONE | FAILED
    verdict: str = ""
    enqueued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    processed_at: str = ""


class ValidationQueue:
    """Synchronous validation queue with priority support."""

    def __init__(self, validator, base_dir: Path):
        self.validator = validator
        self.base_dir = base_dir
        self._queue: list[ValidationQueueItem] = []
        self._processed: list[ValidationQueueItem] = []

    def enqueue(
        self,
        artifact_id: str,
        artifact_type: str,
        content: str,
        lineage: dict,
        provider: str,
        model: str,
        context_pack_id: str,
        priority: str = "NORMAL",
    ) -> ValidationQueueItem:
        item = ValidationQueueItem(
            item_id=f"VQ-{artifact_id}",
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            content=content,
            lineage=lineage,
            provider=provider,
            model=model,
            context_pack_id=context_pack_id,
            priority=priority,
        )
        self._queue.append(item)
        # Sort by priority
        self._queue.sort(key=lambda x: PRIORITY_ORDER.get(x.priority, 1))
        return item

    def process_all(self) -> list[dict]:
        """Process all queued items synchronously."""
        results = []
        while self._queue:
            item = self._queue.pop(0)
            item.status = "PROCESSING"
            val_result = self.validator.validate(
                artifact_id=item.artifact_id,
                content=item.content,
                artifact_type=item.artifact_type,
                lineage=item.lineage,
                provider=item.provider,
                model=item.model,
                context_pack_id=item.context_pack_id,
            )
            item.verdict = val_result.verdict
            item.status = "DONE" if val_result.passed else "FAILED"
            item.processed_at = datetime.now(timezone.utc).isoformat()
            self._processed.append(item)

            # Write validation report
            report_file = self.base_dir / "validation_queue" / f"vq_{item.artifact_id}.md"
            report_file.write_text(val_result.to_markdown(), encoding="utf-8")
            results.append({
                "artifact_id": item.artifact_id,
                "priority": item.priority,
                "verdict": item.verdict,
                "passed": val_result.passed,
            })
        return results

    def summary(self) -> dict:
        all_items = self._processed
        passed = sum(1 for i in all_items if i.status == "DONE")
        failed = sum(1 for i in all_items if i.status == "FAILED")
        pass_rate = round(passed / len(all_items) * 100, 1) if all_items else 0.0
        return {
            "total": len(all_items),
            "passed": passed,
            "failed": failed,
            "pass_rate_pct": pass_rate,
            "verdicts": {i.artifact_id: i.verdict for i in all_items},
        }

    def save_report(self, output_path: Path) -> None:
        summary = self.summary()
        lines = [
            "---",
            "id: yos-validation-queue-mission-018",
            "title: Validation Queue Report — MISSION-018",
            "type: validation_queue_report",
            "mission_id: MISSION-018",
            f"pass_rate: {summary['pass_rate_pct']}%",
            "tags: ['#validation', '#yos', '#mission-018']",
            "---",
            "",
            "# Validation Queue Report — MISSION-018",
            "",
            f"**Total Items:** {summary['total']}  ",
            f"**Passed:** {summary['passed']}  ",
            f"**Failed:** {summary['failed']}  ",
            f"**Pass Rate:** {summary['pass_rate_pct']}%  ",
            "",
            "## Results",
            "",
            "| Artifact | Priority | Verdict | Passed |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for item in self._processed:
            ok = "✅" if item.status == "DONE" else "❌"
            lines.append(f"| {item.artifact_id} | {item.priority} | {item.verdict} | {ok} |")
        lines.append("")
        lines.append("---")
        lines.append("*Validation Queue v1 — Y-OS*")
        output_path.write_text("\n".join(lines), encoding="utf-8")
