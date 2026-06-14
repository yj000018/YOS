#!/usr/bin/env python3
"""
Module 5: Organizational Timeline Generator v1 — Y-OS MISSION-024
Generates: Timeline_Missions.md, Timeline_ADRs.md, Timeline_Providers.md, Timeline_Evolution.md
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from odt_time_machine_v1 import ODTSnapshot, MISSION_HISTORY, ADR_HISTORY


class OrganizationalTimelineGenerator:
    def __init__(self, snapshots: list[ODTSnapshot]):
        self.snapshots = snapshots
        self.ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def generate_all(self, output_dir: Path) -> dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = {}
        paths["missions"] = self._gen_missions(output_dir / "Timeline_Missions.md")
        paths["adrs"] = self._gen_adrs(output_dir / "Timeline_ADRs.md")
        paths["providers"] = self._gen_providers(output_dir / "Timeline_Providers.md")
        paths["evolution"] = self._gen_evolution(output_dir / "Timeline_Evolution.md")
        return paths

    def _gen_missions(self, path: Path) -> Path:
        rows = ""
        for m in MISSION_HISTORY:
            rows += f"| {m['id']} | {m['title']} | {m['date']} | {m['phase']} |\n"
        content = f"""---
id: Timeline_Missions
title: 'Y-OS Mission Timeline'
type: timeline
generated_at: '{self.ts}'
tags: ['#timeline', '#missions', '#mission-024']
aliases: [Mission Timeline]
---

# Y-OS Mission Timeline

> **Generated:** {self.ts} | **Total Missions:** {len(MISSION_HISTORY)}

| Mission | Title | Date | Phase |
| :--- | :--- | :--- | :--- |
{rows}
## Semantic Links
- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
- **part_of:** [[Dashboard_Time_Machine]]
"""
        path.write_text(content, encoding="utf-8")
        return path

    def _gen_adrs(self, path: Path) -> Path:
        rows = ""
        for a in ADR_HISTORY:
            rows += f"| {a['id']} | {a['status']} | {a['date']} |\n"
        content = f"""---
id: Timeline_ADRs
title: 'Y-OS ADR Timeline'
type: timeline
generated_at: '{self.ts}'
tags: ['#timeline', '#adrs', '#mission-024']
aliases: [ADR Timeline]
---

# Y-OS ADR Timeline

> **Generated:** {self.ts} | **Total ADRs:** {len(ADR_HISTORY)}

| ADR | Status | Date |
| :--- | :--- | :--- |
{rows}
## Semantic Links
- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
"""
        path.write_text(content, encoding="utf-8")
        return path

    def _gen_providers(self, path: Path) -> Path:
        content = f"""---
id: Timeline_Providers
title: 'Y-OS Provider Evolution Timeline'
type: timeline
generated_at: '{self.ts}'
tags: ['#timeline', '#providers', '#mission-024']
aliases: [Provider Timeline]
---

# Y-OS Provider Evolution Timeline

> **Generated:** {self.ts}

| Period | Provider | Share | Status |
| :--- | :--- | :--- | :--- |
| M-001 → M-022A | OpenAI only | 100% | Mono-provider |
| M-023 | OpenAI | 42.9% | Diversified |
| M-023 | Anthropic | 28.6% | Active |
| M-023 | Gemini | 28.6% | Integrated |
| M-024 | OpenAI | 42.9% | Stable |
| M-024 | Anthropic | 28.6% | Stable |
| M-024 | Gemini | 28.6% | Stable |

## Semantic Links
- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
- **depends_on:** [[MISSION-023_Provider_Diversification]]
"""
        path.write_text(content, encoding="utf-8")
        return path

    def _gen_evolution(self, path: Path) -> Path:
        rows = ""
        for s in self.snapshots[::3]:  # Every 3rd snapshot for readability
            rows += f"| {s.mission_id} | {s.phase} | {s.missions_count} | {s.adrs_count} | {s.graph_quality} | {s.eis_score} |\n"
        content = f"""---
id: Timeline_Evolution
title: 'Y-OS Organizational Evolution Timeline'
type: timeline
generated_at: '{self.ts}'
tags: ['#timeline', '#evolution', '#mission-024']
aliases: [Evolution Timeline]
---

# Y-OS Organizational Evolution Timeline

> **Generated:** {self.ts}

| Mission | Phase | Missions | ADRs | Graph Quality | EIS |
| :--- | :--- | :--- | :--- | :--- | :--- |
{rows}
## Semantic Links
- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
- **produced_by:** [[evolution_analysis_engine_v1]]
"""
        path.write_text(content, encoding="utf-8")
        return path
