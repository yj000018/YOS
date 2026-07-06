# Open Hypotheses

> **Source Gate:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE
> **Type:** Open, unresolved hypotheses requiring A&G synthesis
> **Status:** v1.0.0

---

## OH-001 — The Pre-Monorepo History

**Hypothesis:** There is a rich discovery history in kap-control-plane, yos-cognitive-os, and other legacy repos that predates 2026-07-05.

**Evidence:** The monorepo was created on 2026-07-05 via PR merge. The legacy repos existed before. The MIGRATION-INDEX.md references kap-control-plane as the bootstrap runtime.

**Unknown:** What discoveries were made in the pre-monorepo era? What architectural decisions were made and then reversed? What vocabulary was used before the current vocabulary?

**Required action:** Future CHRONICLES gate to excavate kap-control-plane and yos-cognitive-os.

---

## OH-002 — The KOSMOS Definition

**Hypothesis:** KOSMOS is formally defined somewhere — in Notion, in a legacy repo, or in session transcripts.

**Evidence:** Yannick's role is "Architect of New Society & Enlightened Humanity". The BUS domain registry includes `kosmos`. The session context references "l'Œuvre".

**Unknown:** Is KOSMOS formally defined? What is its relationship to yOS? Is it a project, a vision, a system, or all three?

**Required action:** A&G synthesis of KOSMOS definition.

---

## OH-003 — The ELYSIUM Connection

**Hypothesis:** ELYSIUM (referenced in Manus skills as a book/prose project) is part of the Œuvre.

**Evidence:** The `elysium-prose-orchestration` skill exists in Manus. It references "FSD Controlled Mode" and "ELYSIUM book".

**Unknown:** What is ELYSIUM? How does it relate to KOSMOS and yOS? Is it a creative work, a technical work, or both?

**Required action:** A&G synthesis of ELYSIUM definition.

---

## OH-004 — The A&G Decision Protocol

**Hypothesis:** There is a formal A&G decision protocol that I have not yet seen.

**Evidence:** Every MPR is marked `executed_awaiting_architect_guardian_review`. The A&G sends back MPRs but no explicit decision files. The workflow is unclear.

**Unknown:** What is the formal A&G decision protocol? What does "accepted" look like? What does "rejected" look like? Is the re-sending of the MPR an implicit acceptance?

**Required action:** A&G to clarify the decision protocol.

---

## OH-005 — The N100 Lambda Integration

**Hypothesis:** The N100 Lambda (physical MiniPC) will become a key node in the yOS architecture.

**Evidence:** AGENTS.md on the cloud computer references the N100 Lambda as the target for n8n, Home Assistant, Docker services. The cloud computer is explicitly limited to lightweight scripts.

**Unknown:** When will the N100 be connected? What BUS backend will it use? Will it have its own AGENTS identity?

**Required action:** Future gate to connect N100 Lambda to yOS.

---

## OH-006 — The MCP Server Setup

**Hypothesis:** A filesystem MCP server on Manus would enable direct ChatGPT → BUS inbox writes.

**Evidence:** manus-mcp-cli is available. 0 MCP servers currently configured. The connectivity census classified MCP as `candidate`.

**Unknown:** Can a filesystem MCP server be configured on Manus? Would it enable ChatGPT to write directly to /home/ubuntu/yos-bus-runtime/inbox/mpm/?

**Required action:** MPM-{DATE}-YOS-BUS-MCP-SERVER-SETUP-GATE

---

## OH-007 — The Webhook Last-Mile

**Hypothesis:** Manus webhooks can push MPR notifications to ChatGPT, eliminating the need for ChatGPT to poll GitHub.

**Evidence:** Manus API supports task_stopped webhook. The connectivity census classified webhooks as `production_candidate`.

**Unknown:** Can ChatGPT receive webhooks? What endpoint? What authentication?

**Required action:** MPM-{DATE}-YOS-BUS-WEBHOOK-LAST-MILE-GATE

---

## OH-008 — The Reflex Architecture Activation

**Hypothesis:** The BUS reflex architecture can be activated to enable automatic MP processing without human relay.

**Evidence:** bus-reflex-architecture.md exists. The reflex architecture is defined but not activated.

**Unknown:** What triggers the reflex? How does it interact with the Manus agent loop? What is the failure mode?

**Required action:** MPM-{DATE}-YOS-BUS-REFLEX-ACTIVATION-GATE
