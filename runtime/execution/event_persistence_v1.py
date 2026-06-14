#!/usr/bin/env python3
"""
Module 4: Event Persistence v1 — Y-OS MISSION-022
Append-only event store. Supports replay, audit, reconstruction.
"""
from __future__ import annotations
import json
from pathlib import Path
from event_bus_core_v1 import YOSEvent


class EventPersistence:
    def __init__(self, store_path: Path):
        self.store_path = store_path
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            self.store_path.write_text("", encoding="utf-8")

    def append(self, event: YOSEvent) -> None:
        """Append event as JSONL line (append-only)."""
        with self.store_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    def load_all(self) -> list[dict]:
        """Load all events from store."""
        events = []
        for line in self.store_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return events

    def count(self) -> int:
        return len(self.load_all())

    def filter_by_type(self, event_type: str) -> list[dict]:
        return [e for e in self.load_all() if e.get("event_type") == event_type]

    def filter_since(self, since_ts: str) -> list[dict]:
        return [e for e in self.load_all() if e.get("timestamp", "") >= since_ts]
