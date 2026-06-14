#!/usr/bin/env python3
"""
Context Cache v1 — Y-OS
ADR-0045

Caches compiled Context Packs to avoid recompilation.
Never caches raw session history.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import hashlib


def _cache_key(mission_id: str, worker: str, capability: str, parent_artifact_hash: str, mode: str) -> str:
    raw = f"{mission_id}|{worker}|{capability}|{parent_artifact_hash}|{mode}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _artifact_hash(artifact_ids: list[str]) -> str:
    """Hash a list of artifact IDs to form a cache key component."""
    combined = "|".join(sorted(artifact_ids))
    return hashlib.sha256(combined.encode()).hexdigest()[:12]


@dataclass
class CacheEntry:
    cache_key: str
    mission_id: str
    worker: str
    capability: str
    mode: str
    parent_artifact_hash: str
    context_pack: object  # The compiled ContextPack object
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    hit_count: int = 0


class ContextCache:
    """In-memory cache for compiled Context Packs."""

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}
        self._hits = 0
        self._misses = 0

    def get(
        self,
        mission_id: str,
        worker: str,
        capability: str,
        parent_artifact_ids: list[str],
        mode: str,
    ) -> Optional[object]:
        """Return cached Context Pack or None."""
        parent_hash = _artifact_hash(parent_artifact_ids)
        key = _cache_key(mission_id, worker, capability, parent_hash, mode)
        entry = self._cache.get(key)
        if entry:
            entry.hit_count += 1
            self._hits += 1
            return entry.context_pack
        self._misses += 1
        return None

    def put(
        self,
        mission_id: str,
        worker: str,
        capability: str,
        parent_artifact_ids: list[str],
        mode: str,
        context_pack: object,
    ) -> str:
        """Store a compiled Context Pack in cache. Returns cache key."""
        parent_hash = _artifact_hash(parent_artifact_ids)
        key = _cache_key(mission_id, worker, capability, parent_hash, mode)
        self._cache[key] = CacheEntry(
            cache_key=key,
            mission_id=mission_id,
            worker=worker,
            capability=capability,
            mode=mode,
            parent_artifact_hash=parent_hash,
            context_pack=context_pack,
        )
        return key

    def summary(self) -> dict:
        return {
            "total_entries": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate_pct": round(self._hits / (self._hits + self._misses) * 100, 1)
            if (self._hits + self._misses) > 0 else 0.0,
        }
