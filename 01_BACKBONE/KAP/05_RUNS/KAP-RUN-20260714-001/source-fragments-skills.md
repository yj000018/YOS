# KAP Source Fragments — Skills Vault + Cross-Session Knowledge
## KAP-RUN-20260714-001 / Phase B

**Sources:**
- `/home/ubuntu/skills/` — 19 yOS-relevant skills scanned
- Manus cross-session knowledge (session memory, user profile, project context)
- Note: Mem0 (disabled connector) and Notion (disabled connector) not accessible

**Extracted:** 2026-07-14
**Evidence level:** 7/10 (operational documentation + cross-session memory)

---

## SF-SKILLS-001 — yOS Memory Architecture
**Source:** skills/memory-manager/SKILL.md + skills/mem0-sync/SKILL.md + skills/hydrater/SKILL.md
**Fragment:**
yOS uses a dual-memory architecture: Notion (primary structured store) + Mem0 (cross-session semantic search). Notion = "🧠 Manus Memory Hub" with 5 entry types (Conversation Archive, Projet/Thème, Connaissance Explicite, Préférence/Configuration, Résumé de Session). Mem0 = cross-session search via `user_id=yannick`.

**Key assertions:**
- Memory is NOT automatic — archiving is on-demand only
- Notion = structured memory (sessions, projects, knowledge)
- Mem0 = semantic cross-session search
- Hydration = loading context at session start from Notion/Mem0
- Sessions without "Check" prefix = not yet processed/archived

---

## SF-SKILLS-002 — yOS Session Processing Pipeline (LMP)
**Source:** skills/session-synthesis/SKILL.md + skills/memory-pipeline/SKILL.md + skills/session-synthesizer/SKILL.md
**Fragment:**
LMP (LLM Memory Pipeline) = collect → synthesize → archive → push to Mem0. Session synthesis uses Claude Sonnet via ANTHROPIC_API_KEY. Output: session card JSON → Notion → Mem0. Manus JWT required for session collection. Pipeline scripts at `/home/ubuntu/manus_pipeline/` (not yet initialized in this sandbox).

**Key assertions:**
- Session processing requires Manus JWT (browser extraction)
- Claude Sonnet = synthesis model
- Session cards = structured JSON with title, summary, ToC, key points, decisions, actions
- Sessions with "Check" prefix = already archived
- 194 historical Manus sessions = not yet processed in this sandbox

---

## SF-SKILLS-003 — yOS Execution Philosophy
**Source:** User profile + skills/yos-optimizer/SKILL.md + session memory
**Fragment:**
Yannick = Architect of New Society & Enlightened Humanity. yOS = cognitive operating system. Manus = UI vivante centrale (not an assistant — a cognitive co-pilot). Key rules: 100% autonomous execution, no invention, no time waste, no hidden uncertainty. Fidélité > confort.

**Key assertions:**
- yOS is a living architecture, not a collection of isolated tools
- Long-term humanist vision — not anxiety-driven
- Structure > prose. Models > narratives.
- Manus = operator/co-pilot, not assistant
- K1: Autonomous execution canon — explore all alternatives before asking

---

## SF-SKILLS-004 — yOS Tool Routing Architecture
**Source:** skills/tool-router/SKILL.md + user profile routing rules
**Fragment:**
Primary routing: Memory = Notion (structured) + Mem0 (cross-session). Code = GitHub MCP (PAT). Search = Perplexity (synthesis) + Firecrawl (extraction) + Exa (semantic). LLM = Anthropic (default) + Gemini (long docs) + GPT-5 (vision) + Grok (X/web). Automation = n8n (complex) + Zapier (fast). Project = Linear (dev) + Notion (global).

**Key assertions:**
- Tool routing is explicit and documented
- No tool should be used without checking tool-router first
- LLM routing: Anthropic = default for most tasks
- Memory routing: Notion = primary, Mem0 = cross-session

---

## SF-SKILLS-005 — yOS Projects (Active)
**Source:** User profile + session memory + project context
**Fragment:**
Active projects: KAP (Knowledge Assimilation Pipeline), yOS (Cognitive OS), ELYSIUM (Civilizational Ontology / Yworld), CASATAO, KOSMOS. Primary email: yannick.jolliet@gmail.com. GitHub: yannick-jolliet / yj000018. Timezone: Europe/Paris (GMT+2).

**Key assertions:**
- KAP = active, in first pipeline run
- ELYSIUM = civilizational ontology (formerly "Yworld")
- KOSMOS = related to yOS but definition not yet formalized (open hypothesis OH-002)
- CASATAO = active project (domain in BUS)

---

## SF-SKILLS-006 — yOS Backbone Modules (Current State)
**Source:** Session memory + git repo state
**Fragment:**
Backbone modules as of 2026-07-14: MPM (Manus Process Manager) · KAP (Knowledge Assimilation Pipeline) · BUS (transport substrate) · YARP (YOS Agent Relay Protocol) · AGENTS (identity/capability/trust/routing/discovery). Additional: ART, CRT, ROUTING, GOVERNANCE, MEMORY, SECURITY (scaffolded). Monorepo: github.com/yj000018/YOS (main branch).

**Key assertions:**
- 5 core backbone modules constituted
- 7+ additional modules scaffolded
- All modules follow same structure: 00_SPEC, 01_SCHEMAS, 02_ADAPTERS/PIPELINES, etc.
- Single commit per gate = canonical practice

---

## SF-SKILLS-007 — yOS A&G Review Process
**Source:** Session memory + MPR workflow observation
**Fragment:**
A&G = Architect & Guardian (ChatGPT role). Every gate produces an MPR. MPR goes to `awaiting-review/`. A&G reviews and sends decision. Current status: 21 MPRs awaiting A&G review. Decision format unclear — implicit acceptance (MPR resend) vs explicit (accepted/rejected/patched) not yet formalized. Open hypothesis OH-004.

**Key assertions:**
- A&G review is mandatory before gate is fully closed
- Current decision protocol = ambiguous (needs formalization)
- 21 MPRs awaiting review as of 2026-07-14
- Guardian = ChatGPT in current workflow

---

## SF-SKILLS-008 — yOS Persistent Infrastructure
**Source:** AGENTS.md (cloud-pc-8cd489il) + session memory
**Fragment:**
Cloud Computer (GCP VM, 1GB RAM): scripts Python légers, batches < 200MB. Manus Sandbox: éphémère, 512MB. N100 Lambda (physical MiniPC, 8-16GB): n8n, Home Assistant, Docker. `/home/ubuntu/` in Manus sandbox = persistent cross-session.

**Key assertions:**
- Manus sandbox = ephemeral but `/home/ubuntu/` persists
- Cloud Computer = lightweight scripts only (no Docker multi-container)
- N100 Lambda = heavy services (n8n, HA, Docker)
- yOS bus runtime: `/home/ubuntu/yos-bus-runtime` (persistent)

---

## SF-SKILLS-009 — yOS Knowledge Sources (Backlog)
**Source:** KAP adapter census + session memory
**Fragment:**
Knowledge sources backlog: 194 Manus sessions (not processed), Notion workspace (connector disabled), Obsidian vault (not yet scanned), ChatGPT Bootstrap Pack + Current Pack (ACQUIRED, ready to process), GitHub repos (archaeology phase pending).

**Key assertions:**
- ChatGPT Bootstrap + Current Pack = highest priority next KAP source
- Notion connector needs enabling for KAP pipeline
- Manus JWT needed for session collection
- GitHub archaeology = next major phase after ChatGPT consolidation

---

## SF-SKILLS-010 — yOS Spiritual/Civilizational Context
**Source:** User profile + session memory
**Fragment:**
Yannick's vision: Architect of New Society & Enlightened Humanity. Spiritual: Guru Swami Vishwananda, Hindu mysticism, Shiva Nataraja altar. Books: societal transformation, 12 pillars of civilization mapped to 7 chakras, 'PRÉCIPITATION', 'OneSHIFT'. ELYSIUM = civilizational ontology. yOS = cognitive OS for this mission.

**Key assertions:**
- yOS is not just a technical system — it's a cognitive infrastructure for civilizational work
- ELYSIUM = the philosophical/civilizational layer
- yOS = the operational layer
- KAP = the knowledge assimilation layer connecting both

---

## Summary

| SF ID | Source | Domain | Evidence Level |
|---|---|---|---|
| SF-SKILLS-001 | Memory skills | MEMORY | 7/10 |
| SF-SKILLS-002 | Session pipeline skills | KAP/MEMORY | 7/10 |
| SF-SKILLS-003 | User profile + yos-optimizer | YOS-CORE | 8/10 |
| SF-SKILLS-004 | tool-router | ROUTING | 7/10 |
| SF-SKILLS-005 | User profile + project context | PROJECTS | 8/10 |
| SF-SKILLS-006 | Session memory + git | BACKBONE | 9/10 |
| SF-SKILLS-007 | Session memory + MPR workflow | MPM/GOVERNANCE | 7/10 |
| SF-SKILLS-008 | AGENTS.md + session memory | INFRASTRUCTURE | 8/10 |
| SF-SKILLS-009 | KAP census + session memory | KAP | 8/10 |
| SF-SKILLS-010 | User profile | VISION | 7/10 |

**Total: 10 Source Fragments from Skills/Cross-Session source**

**Note:** Mem0 connector disabled — cross-session semantic search unavailable. Notion connector disabled — structured memory not accessible. Both need enabling for full KAP pipeline capability.
