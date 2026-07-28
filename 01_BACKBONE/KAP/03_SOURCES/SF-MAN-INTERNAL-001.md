# SF-MAN-INTERNAL-001 — Manus Internal Memory Extract

**Source ID:** SF-MAN-INTERNAL-001
**Channel:** CH-007 (LLM Internal — Manus)
**Extracted:** 2026-07-28T00:30:43Z
**Type:** HEURISTIC_CONTEXT — extracted from active session context, system prompt, and accumulated knowledge
**Status:** ACQUIRED
**Coverage:** User profile, active projects, skills vault, architecture decisions, services

---

> **Note:** This is NOT verbatim session content. This is structured extraction of what Manus knows
> from: (1) the user profile injected in system prompt, (2) the project context, (3) the skills vault,
> (4) the architecture decisions made in this session, (5) cross-session knowledge from memory entries.
> For verbatim session content, see SF-MEM0-001 (Mem0) and future SF-MANUS-SESSION-* files.

---

## Yannick Jolliet — User Profile

**Name:** Yannick Jolliet
**Email:** yannick.jolliet@gmail.com
**GitHub:** yj000018
**Timezone:** Europe/Paris (GMT+2)
**Language:** French (working), English (system)
**Role:** Architect of New Society & Enlightened Humanity

### Vision & Identity
- Architect of cognitive systems (Y-OS / YOS = cognitive operating system)
- Thinks in living architectures, not isolated tools
- Long-term reasoning with humanist, non-anxious vision oriented toward human evolution
- Refuses fear narratives, approximations, conceptual bullshit

### Mode of Thinking
- Structure > prose
- Prefers: models, cartographies, protocols, flows
- Accepts poetry only if structured and useful
- Hates: repetitions, banalities, generic GPT responses

### Relationship to AI
- Does not want an "assistant" AI
- Wants an AI operator / cognitive co-pilot that:
  - Understands intention
  - Anticipates
  - Structures
  - Executes or prepares execution
- Manus is the central living UI, capable of thinking + acting + developing

### Non-negotiable Rules
- Never invent
- Never waste time
- Never hide uncertainty
- Say clearly "I don't know / not reliable"
- Fidelity > comfort
- If too big → split, never compress

### Routing Rules (Y-OS)
- Memory: Notion (structured) + Mem0 (cross-session)
- Code/Repos: GitHub MCP (PAT)
- Search: Perplexity → synthesis, Firecrawl → extraction, Exa → semantic
- LLM: Anthropic → default, Gemini → long docs, GPT-5 → vision, Grok → X/web
- Automation: n8n → complex, Zapier → fast
- Project: Linear → dev, Notion → global
- Design: Canva, Figma Context
- DB: Supabase, Airtable

### K-Rules (Execution Rules)
- K1: Maximum autonomy — explore alternatives before asking
- K2: Spending — never without explicit authorization
- K3: Secrets — Manus Secrets + 1Password only, never manual copy-paste
- K4: Network errors — immediate retry ×2, then 1 min, then 5 min
- K5: Large volumes — systematic split, never compress

---

## Active Projects

### Y-OS (YOS) — Cognitive Operating System
- **Status:** Active, core project
- **Description:** A cognitive operating system for Yannick — a living architecture that connects all tools, agents, memory, and workflows
- **Repo:** github.com/yj000018/YOS (yos-monorepo)
- **Key modules:** MPM, KAP, BUS, YARP, AGENTS, CHRONICLES
- **Backbone:** 01_BACKBONE/ with 5 constituted modules
- **Current phase:** Infrastructure complete, KAP pipeline first run in progress

### ELYSIUM
- **Status:** Active
- **Description:** Literary work / book project — societal transformation, 12 pillars of civilization mapped to 7 chakras
- **Related:** ELYSIUM prose orchestration skill, multi-LLM workflow (Claude API + ChatGPT review)
- **Books:** 'PRÉCIPITATION', 'OneSHIFT'

### KOSMOS
- **Status:** Active
- **Description:** Cosmic architecture / civilization project — connected to Y-OS as the "why" behind the system
- **Relation to yOS:** yOS is the operational layer; KOSMOS is the philosophical/civilizational framework

### KAP (Knowledge Assimilation Pipeline)
- **Status:** Infrastructure complete, first pipeline run in progress
- **Description:** Pipeline for absorbing all knowledge sources (sessions, repos, Notion, Mem0, etc.) into structured GitHub artifacts
- **Sources:** 19 adapters catalogued, 2 production_ready (workspace + git)

### CasaTao
- **Status:** Active
- **Description:** Habitat/living space project — a place aligned with Yannick's values

### Y-World
- **Status:** Active
- **Description:** Notion workspace — primary structured memory store (1300+ pages)

### Cloud Computer (GCP VM)
- **Status:** Active
- **IP:** 34.148.90.222
- **Role:** Scripts légers, batches Python, traces, rendus Excalidraw/Mermaid
- **Constraint:** 1GB RAM — no heavy services

### N100 Lambda
- **Status:** Planned
- **Description:** Physical MiniPC Ubuntu — n8n, Home Assistant, Docker, 24/7 services
- **Prerequisite:** Connect as "My Computer" via Manus desktop client

---

## Skills Vault (81 skills)

All skills available in this Manus session:

- `.skill_versions.json`
- `archive`
- `automation-and-scheduling`
- `back-to-chat`
- `builtin-llm-models`
- `complex-webapp-builder`
- `continuity-pack`
- `cost`
- `credit-optimizer`
- `dev`
- `elysium-prose-orchestration`
- `eta`
- `excel-generator`
- `fast-navigation`
- `file-organizer`
- `finance-pro-playbooks`
- `fransai-basic`
- `game-dev`
- `github-gem-seeker`
- `gws-best-practices`
- `harpa-grid`
- `html-video-production`
- `hydrater`
- `imagegen`
- `internet-skill-finder`
- `km-consolidator`
- `llm-router`
- `manim-animator`
- `manus-api`
- `manus-config`
- `manus-pptx`
- `mem0-sync`
- `memoriser`
- `memory-manager`
- `memory-pipeline`
- `music-prompter`
- `persistent-computing`
- `program-os-orchestrator`
- `project-hydration`
- `project-synthesis`
- `prompt-optimizer`
- `read-special-images`
- `request-optimizer`
- `session-navigator`
- `session-synthesis`
- `session-synthesizer`
- `skill-creator`
- `status`
- `stock-analysis`
- `summary`
- `task-manager`
- `tool-router`
- `tools-registry`
- `trace-excalidraw`
- `tts-prompter`
- `typst-pdf-maker`
- `video-generator`
- `webapp-factory`
- `webdev-custom-dockerfile`
- `webdev-data-api`
- `webdev-file-storage`
- `webdev-image-generation`
- `webdev-llm-integration`
- `webdev-manus-oauth`
- `webdev-maps-integration`
- `webdev-owner-notifications`
- `webdev-periodic-updates`
- `webdev-readme-fullstack`
- `webdev-readme-mobile`
- `webdev-readme-mobile-backend`
- `webdev-readme-static`
- `webdev-ssr-conversion`
- `webdev-voice-transcription`
- `y-menu`
- `yos-cleanmyapps`
- `yos-helpdesk`
- `yos-mac-bridge`
- `yos-mmm`
- `yos-optimizer`
- `yos-voice`
- `ytools`

---

## Architecture Decisions (Session 2026-07-05 to 2026-07-28)

### BUS Module
- BUS is the operational transport substrate — not the protocol itself
- Direct-file backend is production_ready at /home/ubuntu/yos-bus-runtime
- Git fallback is always available
- bus.py CLI v1.1.0 — 14 commands

### YARP Protocol
- YARP defines meaning; BUS moves packets
- JSON is primary; Markdown is audit
- Git is durable memory, not the protocol
- 13 message types across 3 families (Control, Capability, Execution)
- 7 JSON schemas validated

### AGENTS Module
- No agent is globally privileged by default
- Trust is explicit (T0→T5 levels)
- Capabilities are declarative, not proven
- 6 agents registered: chatgpt-ag, manus, claude, gemini, codex, yannick

### MPM (Manus Program Manager)
- 20 gates executed in this session
- All gates committed to main branch
- Ready queue: CLEAN (0 MPs pending)
- A&G review: 20 MPRs awaiting ChatGPT A&G decision

### KAP Pipeline
- 19 adapters catalogued
- Best backend: workspace_filesystem (/home/ubuntu/yos-bus-runtime)
- Fallback chain: filesystem → git → api_task → webhook → connector → mcp → blob
- First pipeline run: KAP-RUN-20260714-001 (4 files: source-fragments-mprs, source-fragments-skills, claims-and-thought-lines, cbs-draft-v1)

### Connectivity
- Manus API: task.create + sendMessage + file.upload — proven
- Workspace filesystem: cross-session persistent — proven
- Mem0: 100+ memories — active
- Notion: connector enabled (1300+ pages)
- GitHub PAT: [REDACTED-PAT-PREFIX] — expired (needs renewal)

### Canonical Rules
- All connectors can be activated without prior authorization (canon rule, 2026-07-28)
- Bootstrap Pack + Current Pack = ChatGPT A&G structured exports (in GitHub)
- ChatGPT parallel sessions: export via Chrome extension (JSON + MD double format)
- Notion: export via native ZIP or API (connector now enabled)

---

## Known Services & Access (Non-sensitive references)

| Service | Status | Notes |
|---|---|---|
| GitHub (yj000018/YOS) | Active | PAT expired — needs renewal |
| Mem0 | Active | API key in env MEM0_API_KEY |
| Manus API | Active | Key in memory |
| Notion (Y-World) | Active | Connector enabled |
| OpenAI | Active | Via Manus proxy |
| Claude API | Active | Key in memory |
| HeyGen API | Active | Key in memory |
| GCP VM (34.148.90.222) | Active | 1GB RAM — scripts only |
| N100 Lambda | Planned | Not yet connected |

---

## Extraction Metadata

| Field | Value |
|---|---|
| Extraction method | Manual structured extraction from session context |
| Session date | 2026-07-05 to 2026-07-28 |
| Gates covered | 20 MPM gates |
| Confidence | HIGH for architecture decisions, MEDIUM for project status |
| Gaps | No verbatim session content, no historical sessions pre-2026-07-05 |
| Next step | Merge with SF-MEM0-001 and SF-GH-* for full picture |
