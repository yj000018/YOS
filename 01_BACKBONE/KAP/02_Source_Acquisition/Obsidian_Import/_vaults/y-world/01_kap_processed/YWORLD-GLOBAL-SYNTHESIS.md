# Y-WORLD Vault — Global Synthesis
> Source: `yj000018/Y-WORLD` | Generated: 2026-07-28 00:56
> 234 notes | 19 subsystems | Obsidian PKM vault

## What is Y-WORLD

Y-WORLD is Yannick Jolliet's **personal World Operating System** — an Obsidian PKM vault
structured as a cognitive interface to his life, projects, knowledge, agents, and symbolic systems.
It is organized into 10 core subsystems (mapped via spatial semantic maps) and serves as the
primary ontological layer above Y-OS (the AI cognitive OS).

## Architecture (10 Subsystems)

| # | Subsystem | Folder | Notes | Core Purpose |
|---|---|---|---|---|
| 1 | **Y-OS** | `60_Y-OS` | 26 | Cognitive OS config, routing tables, agent protocols |
| 2 | **Life** | `20_Life` | 17 | Personal routines, finance, health, travel |
| 3 | **Knowledge** | `30_Knowledge` + `40_K-Cards` | 44 | Semantic KB + atomized K-Cards |
| 4 | **Projects** | `50_Projects` | 7 | Active/paused/future initiatives |
| 5 | **CasaTAO** | `70_CasaTAO` | 13 | AI-native house automation (Sicily) |
| 6 | **ARC Anandaz** | `71_ARC_Anandaz` | 13 | Swiss chalet retreat planning |
| 7 | **Archetypes** | `80_Archetypes` | 14 | Universal symbolic grammar, dreams |
| 8 | **Y-Publishing** | `81_Y-Publishing` | 13 | Books, media, publishing engine |
| 9 | **AI Systems** | `90_Reality_Interfaces` | 25 | Web/mobile portal, AI systems map |
| 10 | **Reality Interfaces** | `90_Reality_Interfaces` | — | Physical maps, Y-WORLD.net |

## System Layer (Infrastructure)

| Folder | Notes | Role |
|---|---|---|
| `00_System` | 11 | Core config, principles, metadata schema |
| `01_Cockpit` | 5 | Daily entry points, HOME, command center |
| `02_Maps` | 11 | Spatial semantic maps (one per subsystem) |
| `03_Dashboards` | 11 | Dynamic status views, loop trackers |
| `04_Templates` | 8 | Note blueprints (K-Card, Project, etc.) |
| `06_Workflows` | 1 | n8n, automation, agent rules |
| `07_Agent_Operations` | 5 | Manus operating parameters, task queue |

## Key Architectural Principles

Based on `00_System/Y-WORLD Architecture.md` and `00_System/Y-WORLD Operating Principles.md`:

- **Spatial Semantic Architecture**: Each subsystem has a Map (02_Maps) + Dashboard (03_Dashboards)
- **K-Cards**: Atomized knowledge blocks in `40_K-Cards/` — the core knowledge primitive
- **Manus Integration**: `07_Agent_Operations/` defines Manus operating parameters and task queue
- **Obsidian Plugins**: dataview, breadcrumbs, templater, quickadd, tasks, obsidian-git, infranodus
- **GitHub Sync**: obsidian-git plugin auto-syncs to `yj000018/Y-WORLD` (private repo)

## Manus-Actionable Surface

Notes flagged `manus_actionable: true` across the vault:

- **00_System** (10 notes): Automation Safety Rules, Manus Operations, Metadata Schema, Naming Conventions, Obsidian OS Cockpit
- **01_Cockpit** (4 notes): Daily Operating Surface, HOME, Manus Control Surface, Y-WORLD Command Center
- **02_Maps** (11 notes): AI SYSTEMS MAP, ARC ANANDAZ MAP, ARCHETYPES MAP, CASATAO MAP, KNOWLEDGE MAP
- **03_Dashboards** (11 notes): AI Systems Dashboard, ARC Anandaz Dashboard, Archetypes Dashboard, CasaTAO Dashboard, Knowledge Dashboard
- **04_Templates** (7 notes): Template - Agent, Template - Daily Note, Template - Dashboard, Template - K-Card, Template - Map Node
- **05_Registries** (1 notes): Tool Registry
- **06_Workflows** (1 notes): Workflow Registry
- **07_Agent_Operations** (5 notes): Manus Change Log, Manus Commands, Manus Operating Manual, Manus Safety Checklist, Manus Task Queue
- **10_Inbox** (2 notes): 2026-05-28, 2026-05-29
- **20_Life** (1 notes): Life Log
- **30_Knowledge** (1 notes): Knowledge Log
- **50_Projects** (1 notes): Projects Log
- **60_Y-OS** (1 notes): Y-OS Log
- **70_CasaTAO** (1 notes): CasaTAO Log
- **71_ARC_Anandaz** (1 notes): ARC Anandaz Log
- **80_Archetypes** (1 notes): Archetypes Log
- **81_Y-Publishing** (1 notes): Y-Publishing Log
- **90_Reality_Interfaces** (1 notes): Y-WORLD.net Vision

## KAP Integration Status

| Item | Status |
|---|---|
| Raw vault cloned | ✅ `yj000018/Y-WORLD` → `/y-world-vault/` |
| Notes catalog (JSON) | ✅ `yworld-notes-catalog.json` (234 notes) |
| KAP Index (MD) | ✅ `YWORLD-KAP-INDEX.md` |
| Factsheets (19 folders) | ✅ `factsheets/*.md` |
| Global synthesis | ✅ This document |
| Pushed to KAP repo | ⏳ Pending commit |

## Next Steps for KAP Pipeline

1. **Deduplication**: Cross-reference Y-WORLD notes with Notion sessions already in KAP
2. **K-Cards extraction**: The `40_K-Cards/` folder contains 10 structured knowledge blocks — prime candidates for Mem0 injection
3. **Agent Operations**: `07_Agent_Operations/` contains Manus task queue and operating manual — sync with current Manus config
4. **Archetypes**: `80_Archetypes/` (14 notes) — feed into the Archetypes synthesis pipeline
5. **CasaTAO**: `70_CasaTAO/` (13 notes) — sync with Home Assistant / n8n automation layer