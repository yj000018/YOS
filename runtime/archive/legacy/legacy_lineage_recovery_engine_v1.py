#!/usr/bin/env python3
"""
Module 1: Legacy Lineage Recovery Engine v1 — Y-OS MISSION-022A
Scans all legacy missions (pre-M013) and coordinates lineage recovery.
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


LEGACY_MISSION_PATTERN = re.compile(
    r"MISSION-0*(\d+)", re.IGNORECASE
)

# Missions that ARE legacy (pre-M013 = missions 001-012B)
LEGACY_THRESHOLD = 13


@dataclass
class LegacyMission:
    mission_id: str
    file_path: str
    title: str
    mission_num: float  # e.g. 12.5 for 012B
    body_text: str = ""
    existing_adrs: list[str] = field(default_factory=list)
    existing_deps: list[str] = field(default_factory=list)
    is_legacy: bool = True


class LegacyLineageRecoveryEngine:
    def __init__(self, root: Path):
        self.root = root
        self.legacy_missions: list[LegacyMission] = []
        self.all_adrs: dict[str, str] = {}   # prefix -> full node_id
        self.all_missions: dict[str, str] = {}  # id -> file_path

    def scan(self) -> int:
        """Scan corpus and identify legacy missions."""
        md_files = list(self.root.rglob("*.md"))

        # Build ADR lookup
        for f in md_files:
            stem = f.stem
            m = re.match(r"(ADR-\d+)", stem, re.IGNORECASE)
            if m:
                self.all_adrs[m.group(1)] = stem

        # Find all missions
        for f in md_files:
            stem = f.stem
            m = re.search(r"MISSION-0*(\d+)([A-Z]?)", stem, re.IGNORECASE)
            if m:
                num_str = m.group(1)
                suffix = m.group(2)
                try:
                    num = float(num_str) + (0.5 if suffix == "B" else
                                            0.1 if suffix == "A" else 0)
                    self.all_missions[stem] = str(f.relative_to(self.root))

                    if num < LEGACY_THRESHOLD:
                        rel = str(f.relative_to(self.root))
                        try:
                            body = f.read_text(encoding="utf-8", errors="ignore")
                        except Exception:
                            body = ""

                        # Extract existing ADR refs
                        existing_adrs = []
                        for adr_num in re.findall(r"ADR-(\d+)", body):
                            key = f"ADR-{int(adr_num):04d}"
                            full_id = self.all_adrs.get(key)
                            if full_id:
                                existing_adrs.append(full_id)

                        # Extract existing mission deps from frontmatter
                        existing_deps = re.findall(r"\[\[MISSION-[^\]]+\]\]", body)

                        title = stem
                        for line in body.split("\n")[:20]:
                            if line.startswith("# "):
                                title = line[2:].strip()[:80]
                                break

                        self.legacy_missions.append(LegacyMission(
                            mission_id=stem,
                            file_path=rel,
                            title=title,
                            mission_num=num,
                            body_text=body,
                            existing_adrs=list(set(existing_adrs)),
                            existing_deps=existing_deps,
                            is_legacy=True,
                        ))
                except ValueError:
                    pass

        # Sort by mission number
        self.legacy_missions.sort(key=lambda m: m.mission_num)
        return len(self.legacy_missions)
