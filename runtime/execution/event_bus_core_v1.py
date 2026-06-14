#!/usr/bin/env python3
"""
Module 1: Event Bus Core v1 — Y-OS MISSION-022
Central event backbone: publish, subscribe, replay, dead_letter_queue, persistence.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional
from collections import defaultdict


@dataclass
class YOSEvent:
    event_type: str
    source: str
    payload: dict
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = ""
    lineage: list[str] = field(default_factory=list)
    delivery_count: int = 0
    delivered: bool = False

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "source": self.source,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "lineage": self.lineage,
            "delivery_count": self.delivery_count,
            "delivered": self.delivered,
        }


class EventBusCore:
    def __init__(self, persistence=None):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._event_log: list[YOSEvent] = []
        self._dead_letter_queue: list[YOSEvent] = []
        self._persistence = persistence  # optional EventPersistence
        self.stats = {
            "published": 0,
            "delivered": 0,
            "failed": 0,
            "dlq_size": 0,
        }

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Register a handler for an event type. Supports wildcards '*'."""
        self._subscribers[event_type].append(handler)

    def publish(self, event: YOSEvent) -> int:
        """Publish event to all matching subscribers. Returns delivery count."""
        self._event_log.append(event)
        self.stats["published"] += 1

        # Persist
        if self._persistence:
            self._persistence.append(event)

        # Find handlers: exact match + wildcard
        handlers = (
            self._subscribers.get(event.event_type, []) +
            self._subscribers.get("*", [])
        )

        delivered = 0
        for handler in handlers:
            try:
                handler(event)
                delivered += 1
                self.stats["delivered"] += 1
            except Exception as e:
                event.delivery_count += 1
                if event.delivery_count >= 3:
                    self._dead_letter_queue.append(event)
                    self.stats["dlq_size"] += 1
                self.stats["failed"] += 1

        event.delivered = delivered > 0
        return delivered

    def replay(self, event_types: list[str] | None = None,
               since: str | None = None) -> list[YOSEvent]:
        """Replay events from log, optionally filtered by type or timestamp."""
        events = self._event_log
        if event_types:
            events = [e for e in events if e.event_type in event_types]
        if since:
            events = [e for e in events if e.timestamp >= since]
        return events

    def dead_letter_queue(self) -> list[YOSEvent]:
        return self._dead_letter_queue

    def get_log(self) -> list[YOSEvent]:
        return self._event_log

    def emit(self, event_type: str, source: str, payload: dict,
             correlation_id: str = "", lineage: list[str] | None = None) -> YOSEvent:
        """Convenience: create and publish event in one call."""
        event = YOSEvent(
            event_type=event_type,
            source=source,
            payload=payload,
            correlation_id=correlation_id,
            lineage=lineage or [],
        )
        self.publish(event)
        return event
