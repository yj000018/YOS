# YOS — Personal AI Operating System

> *A sovereign, modular, platform-agnostic AI operating system.*  
> *915 files. 1 monorepo. Infinite cognitive leverage.*

---

## Architecture

```
YOS/
├── yos-governance/     # Policies, ADRs, standards, schemas, decisions
├── yos-vault/          # Knowledge base — Obsidian vault (Y-WORLD)
├── yos-agents/         # AI agent definitions and tools
├── yos-automations/    # Scripts, userscripts, n8n, playbooks
├── yos-apps/           # Applications — Y-Family suite + prototypes
├── yos-related/        # Experiments, legacy, undecided
└── archive/            # Archived content
```

---

## Sections

### `yos-governance/`
The constitutional layer of YOS. Contains:
- **Manifest** — `policy-manifest.json` — canonical agent roles, routing mode, source of truth
- **Policies** — Agent Operations Policy (ChatGPT / Manus / Claude roles)
- **Decisions** — Repository Audit + 5 ADRs (Git, Obsidian, Local-First, Monorepo, Agent roles)

### `yos-vault/`
The human cognitive interface. Contains the full **Y-WORLD Obsidian vault** (289 files):
- `00_System` — Architecture, naming conventions, automation rules
- `01_Cockpit` — Daily operating surface, Manus control surface
- `02_Maps` / `03_Dashboards` — Cognitive maps and dashboards
- `04_Templates` — Agent, project, K-Card, workflow templates
- `10_Inbox` / `20_Life` / `30_Knowledge` — Personal knowledge base
- `40_K-Cards` — Knowledge cards (Obsidian PKM)
- `50_Projects` — Active projects
- `60_Y-OS` — Y-OS integrations and tooling nodes
- `70_CasaTAO` / `71_ARC_Anandaz` — Physical environments (Sicily / Swiss Alps)
- `80_Archetypes` / `81_Y-Publishing` — Creative and publishing layer
- `90_Reality_Interfaces` — AI systems, interfaces, deployment nodes

### `yos-agents/`
All AI agent tooling and skill definitions:
- `manus/yos-manus-client` — TamperMonkey client for manus.im
- `manus/manus-enhancer` — Brave extension + mobile userscript
- `manus/yos-skills` — 30+ Manus skill definitions (MDX): memoriser, hydrater, llm-router, skill-creator, video-generator, etc.
- `claude/` — Claude agent definitions *(pending)*
- `gpt/` — GPT agent definitions *(pending)*
- `routing/` — Multi-LLM routing logic *(pending)*

### `yos-automations/`
Automation layer — scripts, userscripts, pipelines:
- `scripts/yos-scripts` — YOS Hub: components registry, memory bridge, endpoint, monitor
- `scripts/yos-userscripts` — Auto-updatable TM/Gear Browser scripts
- `scripts/yos-cockpit` — Cognitive Cockpit (Brave ext + mobile)
- `scripts/yos-llm-pipeline` — LLM Knowledge Distillation Pipeline v1.2 (6-layer Knowledge OS)

### `yos-apps/`
Application suite:
- `y-family/y-menu` — Cognitive Orchestration Interface v0 (TypeScript, YAML menus)
- `y-family/daylog` — Daily logging PWA
- `prototypes/yos-voice-vision` — Voice + Vision interface (OpenAI Realtime + Gemini Live)
- `prototypes/youniverse` — 3D Cognitive OS (React + Three.js + R3F)
- `prototypes/one-galaxy` — ONE Galaxy 3D space navigator
- `prototypes/daylog-mvp` — DayLog MVP (HTML PWA)

### `yos-related/`
Experiments and undecided:
- `experiments/pulse-app` — GPT-Claude-Next.js-Sanity-Vercel demo
- `experiments/future-news-project` — Future News journal (TypeScript + Remotion)
- `experiments/remotion-project` — Remotion V1 video engine (13 sequences)
- `experiments/relevance-ai-workforce` — Relevance AI workforce config
- `undecided/casa-tao-nest` — Lovable prototype (4.4MB React app)
- `undecided/eia-awakening-petal` — Lovable prototype (TanStack + Cloudflare)
- `undecided/YMap` — Cognitive map placeholder
- `undecided/Y-Browser-Admin` — Browser admin placeholder

---

## Agent Roles

| Agent | Role |
|-------|------|
| **ChatGPT** | Architecture · Reasoning · Specifications |
| **Manus** | Primary execution operator |
| **Claude** | Fallback execution operator |

## Routing

| Mac state | Mode |
|-----------|------|
| Open | Local-first → `git pull --rebase` → edit → commit → push |
| Closed | GitHub-first via API |

## Source of Truth

**Git** — `yj000018/YOS`  
**Human Interface** — Obsidian (Y-WORLD vault)

---

## Stats

| Metric | Value |
|--------|-------|
| Total files | 915 |
| Total folders | 200+ |
| Repos consolidated | 22 |
| Repos deleted | 3 |
| ADRs | 5 |
| Agent skills | 30+ |
| Obsidian notes | 289 |

---

## Governance

All decisions documented in `yos-governance/Decisions/`:
- [ADR-001](yos-governance/Decisions/ADR-001-Git-As-Source-Of-Truth.md) — Git as Source of Truth
- [ADR-002](yos-governance/Decisions/ADR-002-Obsidian-As-Human-Interface.md) — Obsidian as Human Interface
- [ADR-003](yos-governance/Decisions/ADR-003-Local-First-Git-Fallback.md) — Local-First, Git Fallback
- [ADR-004](yos-governance/Decisions/ADR-004-Monorepo-As-Initial-YOS-Architecture.md) — Monorepo Architecture
- [ADR-005](yos-governance/Decisions/ADR-005-Manus-Primary-Claude-Fallback.md) — Manus Primary, Claude Fallback

---

*Last consolidated: 2026-06-04 — Claude (fallback execution operator)*
