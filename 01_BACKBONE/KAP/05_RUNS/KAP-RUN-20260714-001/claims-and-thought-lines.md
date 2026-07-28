# KAP Claims + Thought Lines
## KAP-RUN-20260714-001 / Phase C

**Sources:** SF-MPR-001..015 + SF-SKILLS-001..010
**Extracted:** 2026-07-14
**Status:** DRAFT — awaiting human validation before CBS promotion

---

## CLAIMS

### Domain: BUS

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-BUS-001 | BUS transports MPM packets. MPM executes them. | SF-MPR-001, SF-MPR-002 | HIGH |
| CL-BUS-002 | Direct-file backend is the preferred BUS runtime (no network dependency) | SF-MPR-001, SF-MPR-003 | HIGH |
| CL-BUS-003 | `/home/ubuntu/yos-bus-runtime` is the canonical persistent BUS runtime path | SF-MPR-003 | HIGH |
| CL-BUS-004 | MP resolution order: `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/` → `MPM/04_QUEUE/ready/` → `BUS/04_DOMAINS/mpm/inbox/` | SF-MPR-001 | HIGH |
| CL-BUS-005 | `bus.py` v1.1.0 has 14 commands including `write`, `ingest`, `latest-report`, `report-pointer` | SF-MPR-004 | HIGH |
| CL-BUS-006 | BUS lifecycle: inbox → workspace → outbox → archive | SF-MPR-002, SF-MPR-004 | HIGH |
| CL-BUS-007 | Workspace filesystem = production_ready backend. MCP bridge = probe_required. | SF-MPR-005, SF-MPR-006 | HIGH |
| CL-BUS-008 | `manus-upload-file` produces S3 CDN URLs — not a workspace write mechanism | SF-MPR-005 | HIGH |

### Domain: YARP

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-YARP-001 | YARP defines meaning. BUS moves packets. | SF-MPR-008, SF-MPR-009, SF-MPR-012 | HIGH |
| CL-YARP-002 | YARP is transport-independent. Transports are adapters. | SF-MPR-008, SF-MPR-009 | HIGH |
| CL-YARP-003 | JSON is primary. Markdown is audit/human-readable. | SF-MPR-008, SF-MPR-012 | HIGH |
| CL-YARP-004 | Git is durable memory, not the protocol. | SF-MPR-008, SF-MPR-015 | HIGH |
| CL-YARP-005 | YARP is independent of Manus, ChatGPT, and all current transports. It will outlive them. | SF-MPR-009 | HIGH |
| CL-YARP-006 | YARP is to yOS what HTTP is to the Web. | SF-MPR-009 | HIGH |
| CL-YARP-007 | 13 message types across 3 families: Control, Capability, Execution | SF-MPR-008 | HIGH |

### Domain: AGENTS

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-AGENTS-001 | Agents have identities. Capabilities are declarative. Trust is explicit. | SF-MPR-010 | HIGH |
| CL-AGENTS-002 | No agent is globally privileged by default. | SF-MPR-010 | HIGH |
| CL-AGENTS-003 | Human operators are also agents. | SF-MPR-010 | HIGH |
| CL-AGENTS-004 | A capability declaration is a claim, not a proof. | SF-MPR-010, SF-MPR-012 | HIGH |
| CL-AGENTS-005 | 6 agents registered: chatgpt-ag, manus, claude, gemini, codex, yannick | SF-MPR-010 | HIGH |
| CL-AGENTS-006 | Trust levels: T0 (untrusted) → T5 (system/owner) | SF-MPR-010 | HIGH |

### Domain: KAP

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-KAP-001 | KAP pipeline = 4 phases: Acquisition → Analysis → Human Validation → Synthesis | SF-MPR-011, SF-SKILLS-002 | HIGH |
| CL-KAP-002 | Human validation is required before CBS promotion to CANON — Manus cannot self-promote | SF-MPR-011 | HIGH |
| CL-KAP-003 | Consumer apps (ChatGPT.com, Claude.ai) = unsupported programmatically — architectural constraint | SF-MPR-011 | HIGH |
| CL-KAP-004 | KAP stack: workspace_filesystem + git-repository (production_ready) + manus-api + openai-api + notion-api | SF-MPR-011 | HIGH |
| CL-KAP-005 | 19 knowledge adapters catalogued. 2 production_ready, 3 production_candidate, 1 candidate, 8 probe_required, 5 unsupported | SF-MPR-011 | HIGH |
| CL-KAP-006 | Mem0 connector = disabled. Notion connector = disabled. Both need enabling for full KAP pipeline. | SF-SKILLS-001, SF-SKILLS-009 | HIGH |

### Domain: MANUS API

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-API-001 | task.create, task.sendMessage, file.upload (3 methods) all proven via OpenAPI spec | SF-MPR-007 | HIGH |
| CL-API-002 | Best pattern: Async Task Relay — task.sendMessage + structured_output_schema → JSON result | SF-MPR-007 | HIGH |
| CL-API-003 | No direct workspace write via API — must relay through agent instruction | SF-MPR-007 | HIGH |
| CL-API-004 | Auth: x-manus-api-key header. Rate limit: 10/min. Latency: 30-120s async. | SF-MPR-007 | HIGH |
| CL-API-005 | agent-default-main_task = conversation continuation shortcut (no new task needed) | SF-MPR-007 | HIGH |

### Domain: INFRASTRUCTURE

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-INFRA-001 | `/home/ubuntu/` persists cross-session in Manus sandbox | SF-MPR-003, SF-SKILLS-008 | HIGH |
| CL-INFRA-002 | Cloud Computer (GCP, 1GB RAM) = lightweight scripts only. N100 Lambda = heavy services. | SF-SKILLS-008 | HIGH |
| CL-INFRA-003 | 194 historical Manus sessions not yet processed. Manus JWT required for collection. | SF-SKILLS-002, SF-SKILLS-009 | HIGH |

### Domain: YOS-CORE

| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| CL-YOS-001 | yOS = cognitive operating system. Manus = UI vivante centrale (co-pilot, not assistant). | SF-SKILLS-003 | HIGH |
| CL-YOS-002 | Everything important to yOS must be findable in one clear place. | SF-MPR-012, SF-MPR-013 | HIGH |
| CL-YOS-003 | Backbone: yOS → KAP · MPM · YARP · AGENTS · BUS | SF-MPR-009, SF-MPR-010 | HIGH |
| CL-YOS-004 | yOS has 5 architectural planes (from Baseline v0.5): Experience, Control, Cognitive, Knowledge, Growth | SF-MPR-015 | MEDIUM |
| CL-YOS-005 | Canon promotion requires evidence, not just assertion. | SF-MPR-015 | HIGH |
| CL-YOS-006 | ELYSIUM = civilizational ontology. yOS = operational layer. KAP = knowledge assimilation layer connecting both. | SF-SKILLS-010 | MEDIUM |

---

## THOUGHT LINES

### TL-001: BUS/YARP Separation of Concerns
**Seed:** "YARP defines meaning. BUS moves packets."
**Evidence:** CL-YARP-001, CL-BUS-001
**Thread:**
- YARP = semantic layer (what is communicated, why, how to interpret)
- BUS = physical transport layer (how packets move, where they go)
- This separation = fundamental architectural decision, not implementation detail
- Analogy: HTTP (YARP) over TCP/IP (BUS)
**Status:** STRONG — consistent across all YARP and BUS documents

### TL-002: Persistence and Durability
**Seed:** "Git is durable memory, not the protocol."
**Evidence:** CL-YARP-004, CL-INFRA-001, CL-BUS-003
**Thread:**
- Git = audit trail and durable storage, not the communication mechanism
- `/home/ubuntu/` = operational persistence (cross-session)
- Git repo = canonical persistence (cross-machine, cross-agent)
- Distinction: operational state (filesystem) vs canonical state (git)
**Status:** STRONG — consistent across BUS, YARP, MPM documents

### TL-003: Human Authority in KAP
**Seed:** "Human validation required before CBS promotion to CANON"
**Evidence:** CL-KAP-002, CL-YOS-005
**Thread:**
- KAP pipeline cannot self-promote claims to CANON
- Manus generates Source Fragments + Claims + Thought Lines
- Human (Yannick) validates before CBS promotion
- A&G (ChatGPT) validates gates before closure
- Both validation loops are non-negotiable
**Status:** STRONG — architectural principle

### TL-004: Agent Trust and Identity
**Seed:** "No agent is globally privileged by default."
**Evidence:** CL-AGENTS-001, CL-AGENTS-002, CL-AGENTS-003, CL-AGENTS-004
**Thread:**
- All agents (including Manus, ChatGPT, Yannick) are peers in YARP
- Trust is explicit, not inherited
- Capability declarations are claims — must be verified
- Human operators are agents too (T5 = owner level)
**Status:** STRONG — consistent across AGENTS and YARP documents

### TL-005: Connectivity Realism
**Seed:** "Consumer apps = unsupported programmatically — architectural constraint"
**Evidence:** CL-KAP-003, CL-API-003
**Thread:**
- ChatGPT.com, Claude.ai, Gemini.ai = no programmatic access
- This is a permanent architectural constraint, not a gap to fix
- Only API-accessible LLMs can be KAP sources
- ChatGPT API (via task.sendMessage) = only viable ChatGPT-to-Manus path
**Status:** STRONG — evidence-based constraint

### TL-006: yOS as Civilizational Infrastructure
**Seed:** "yOS = cognitive infrastructure for civilizational work"
**Evidence:** CL-YOS-001, CL-YOS-006, SF-SKILLS-010
**Thread:**
- yOS is not just a technical system
- ELYSIUM = civilizational ontology (the "what")
- yOS = cognitive OS (the "how to think and act")
- KAP = knowledge assimilation (the "what we know")
- This trilogy (ELYSIUM/yOS/KAP) = the full stack
**Status:** MEDIUM — needs more evidence from ELYSIUM documents

---

## OPEN QUESTIONS (for human validation)

1. **OQ-001:** Is TL-006 (civilizational trilogy) accurate? Does ELYSIUM/yOS/KAP represent the intended architecture?
2. **OQ-002:** Should CL-YOS-004 (5-plane architecture from Baseline v0.5) be promoted to HIGH confidence?
3. **OQ-003:** A&G decision protocol — implicit (MPR resend = acceptance) or explicit? (see OH-004)
4. **OQ-004:** Should Mem0 and Notion connectors be enabled to complete the KAP pipeline?

---

## CBS PROMOTION CANDIDATES

The following claims are candidates for CBS (Current Best Synthesis) promotion after human validation:

**Tier 1 — Ready for CBS (HIGH confidence, consistent evidence):**
- All CL-BUS-* (8 claims)
- All CL-YARP-* (7 claims)
- All CL-AGENTS-* (6 claims)
- CL-KAP-001, CL-KAP-002, CL-KAP-003, CL-KAP-004, CL-KAP-005
- CL-API-001, CL-API-002, CL-API-003, CL-API-004, CL-API-005
- CL-INFRA-001, CL-INFRA-002
- CL-YOS-001, CL-YOS-002, CL-YOS-003, CL-YOS-005

**Tier 2 — Needs validation (MEDIUM confidence):**
- CL-YOS-004 (5-plane architecture)
- CL-YOS-006 (ELYSIUM/yOS/KAP trilogy)
- TL-006 (civilizational infrastructure)

**Total claims: 41 | Tier 1: 38 | Tier 2: 3**
