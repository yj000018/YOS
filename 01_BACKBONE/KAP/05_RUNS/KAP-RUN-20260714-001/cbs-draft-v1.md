# CBS Draft v1 — yOS Architecture Knowledge Base
## KAP-RUN-20260714-001

**Status:** DRAFT — awaiting human validation
**Sources:** 15 MPR fragments + 10 Skills/cross-session fragments
**Claims:** 41 (38 Tier 1, 3 Tier 2)
**Thought Lines:** 6
**Date:** 2026-07-14

> ⚠️ This is a KAP-generated draft. It CANNOT be promoted to CANON without explicit human validation by Yannick. See §7 for open questions.

---

## §1 — yOS Backbone Architecture

yOS is a **cognitive operating system** — not a collection of isolated tools, but a living architecture for civilizational-scale cognitive work. Its operational layer is the **monorepo** (`github.com/yj000018/YOS`, branch `main`), organized around `01_BACKBONE/` as the canonical home for all backbone modules.

**The 5 constituted backbone modules:**

| Module | Full Name | Role |
|---|---|---|
| **MPM** | Manus Process Manager | Orchestration & execution of MPs |
| **KAP** | Knowledge Assimilation Pipeline | Knowledge absorption, synthesis, canon |
| **BUS** | Transport Substrate | Physical movement of packets between agents |
| **YARP** | YOS Agent Relay Protocol | Semantic definition of inter-agent communication |
| **AGENTS** | Agent Registry & Governance | Identity, capabilities, trust, routing, discovery |

**Canonical doctrine:**
```
yOS → KAP · MPM · YARP · AGENTS · BUS
YARP defines meaning. BUS moves packets.
JSON is primary. Markdown is audit.
Git is durable memory, not the protocol.
Everything important to yOS must be findable in one clear place.
```

---

## §2 — BUS (Transport Substrate)

BUS is the **physical transport layer** of yOS. It moves packets between agents without defining their meaning.

**Key facts:**
- Module: `01_BACKBONE/BUS/` — 62+ files, `bus.py` CLI v1.1.0 (14 commands)
- Canonical runtime: `/home/ubuntu/yos-bus-runtime` (persistent cross-session)
- Preferred backend: **direct-file** (no network dependency, ~43ms claim latency)
- MP resolution order: `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/` → `MPM/04_QUEUE/ready/` → `BUS/04_DOMAINS/mpm/inbox/`
- BUS lifecycle: `inbox → workspace → outbox → archive`
- 6 domain folders: general, mpm, kap, casatao, kosmos, yworld

**Backend classification:**

| Backend | Status |
|---|---|
| workspace_filesystem | production_ready ⭐ |
| git_repository | production_ready |
| manus_api | production_candidate |
| manus_workspace | candidate |
| google_drive | probe_required |
| mcp_bridge | probe_required (0 servers) |

**Key distinction:** `manus-upload-file` produces S3 CDN public URLs — this is NOT a workspace write mechanism.

---

## §3 — YARP (YOS Agent Relay Protocol)

YARP is the **semantic protocol layer** of yOS — defining what is communicated between agents, not how it is physically transported.

**Doctrine (immutable, v1.1.0):**
- YARP is to yOS what HTTP is to the Web
- YARP is transport-independent. Transports are adapters.
- YARP is independent of Manus, ChatGPT, Claude, Gemini, and all current transports
- YARP will outlive all current transports
- Agents are peers. JSON is primary. Markdown is audit.

**Structure:** `01_BACKBONE/YARP/` — 9 spec/governance files, 7 JSON schemas, 13 message types (3 families: Control, Capability, Execution), 8 transport adapters

**Transport adapters (production_ready):**
1. Manus API (task.sendMessage)
2. Workspace Filesystem (direct-file)

---

## §4 — AGENTS

AGENTS is the **identity and governance layer** of yOS.

**Doctrine (immutable, v1.0.0):**
- Agents have identities. Capabilities are declarative. Trust is explicit.
- No agent is globally privileged by default.
- Human operators are also agents.
- A capability declaration is a claim, not a proof.
- Permissions are bounded. Routing is capability-based.

**Registered agents (v1.0.0):**

| Agent | Role | Trust Level |
|---|---|---|
| yannick | Owner/Architect | T5 |
| manus | Executor/Co-pilot | T4 |
| chatgpt-ag | Architect & Guardian | T4 |
| claude | Analyst/Writer | T3 |
| gemini | Long-doc Processor | T3 |
| codex | Code Agent | T3 |

**Trust levels:** T0 (untrusted) → T5 (system/owner)

---

## §5 — KAP (Knowledge Assimilation Pipeline)

KAP is the **knowledge absorption layer** of yOS — transforming raw sources into canonical knowledge.

**Pipeline (4 phases):**
1. **Acquisition** — Surface detection → Metadata probe → Content extraction → Fragmentation
2. **Analysis** — Claim extraction → Thought Line seeding → Decision Thread extraction
3. **Human Validation** — Contradiction review → Thought Line validation (MANDATORY STOP)
4. **Synthesis** — CBS Authorization → Synthesis generation → Publication

**Critical rule:** Manus CANNOT self-promote claims to CANON. Human validation by Yannick is required at Phase 3 before any CBS promotion.

**Knowledge adapter stack:**

| Adapter | Status |
|---|---|
| workspace_filesystem | production_ready ⭐ |
| git_repository | production_ready |
| manus_api | production_candidate |
| openai_api | production_candidate |
| notion_api | production_candidate (connector disabled) |
| Consumer apps (ChatGPT.com, Claude.ai, etc.) | **unsupported** — permanent architectural constraint |

**Current backlog:**
- ChatGPT Bootstrap Pack + Current Pack: ACQUIRED, ready to process
- MPRs from 2026-07-05 session: ACQUIRED (processed in this run)
- 194 historical Manus sessions: CATALOGUED, not yet processed
- Notion workspace: PENDING (connector disabled)

---

## §6 — Manus API Connectivity

**Proven capabilities (via OpenAPI spec):**
- `task.create` — create new task with instructions
- `task.sendMessage` + `agent-default-main_task` — continue existing conversation
- `file.upload` — 3 methods: file_id (512MB), file_url (20MB), file_data (20MB)
- `structured_output_schema` → `structured_output_result` event — JSON result extraction
- Webhooks: task_created, task_stopped

**Best pattern:** Async Task Relay — `task.sendMessage` + `structured_output_schema` → MPR as JSON result. Eliminates manual bridge. Latency: 30-120s async.

**Constraints:**
- No direct workspace write via API — must relay through agent instruction
- Rate limit: 10/min
- Auth: `x-manus-api-key` header (API key not yet generated)

---

## §7 — Open Questions (Human Validation Required)

| OQ | Question | Impact |
|---|---|---|
| OQ-001 | Is the ELYSIUM/yOS/KAP trilogy accurate? Does it represent the intended full stack? | MEDIUM |
| OQ-002 | Should the 5-plane architecture (from Baseline v0.5) be promoted to HIGH confidence? | MEDIUM |
| OQ-003 | A&G decision protocol: implicit (MPR resend = acceptance) or explicit? | HIGH |
| OQ-004 | Should Mem0 and Notion connectors be enabled to complete the KAP pipeline? | HIGH |

---

## §8 — Infrastructure

| Resource | Status | Notes |
|---|---|---|
| `/home/ubuntu/` (Manus sandbox) | Persistent cross-session | Canonical operational path |
| `/home/ubuntu/yos-bus-runtime` | Active | BUS direct-file runtime |
| Git repo (main) | Active | Canonical durable memory |
| Cloud Computer (GCP, 1GB) | Active | Lightweight scripts only |
| N100 Lambda (physical) | Active | n8n, HA, Docker |
| Mem0 connector | Disabled | Needs enabling |
| Notion connector | Disabled | Needs enabling |
| Manus API key | Not generated | Needed for ChatGPT→Manus relay |

---

## §9 — CBS Promotion Summary

**Tier 1 (38 claims — ready for CBS after human validation):**
All BUS, YARP, AGENTS, KAP, API, INFRA, and core YOS claims with HIGH confidence.

**Tier 2 (3 claims — needs additional validation):**
- 5-plane architecture (Baseline v0.5)
- ELYSIUM/yOS/KAP trilogy
- yOS as civilizational infrastructure

**Pending human validation:** Yannick must review §7 open questions and confirm Tier 1 promotion before this CBS draft becomes CANON.
