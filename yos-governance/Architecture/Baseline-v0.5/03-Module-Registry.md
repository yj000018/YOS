# Y-OS Architecture Baseline v0.5
## 03 — Module Registry

**Status:** Working registry. Every entry must later be verified against GitHub, Manus, Obsidian/Markdown, Notion, and ARCH transcripts.

---

# 1. Registry rules

Each module is described through:

- canonical or working name;
- aliases;
- plane;
- mission;
- ownership;
- non-ownership;
- inputs;
- outputs;
- dependencies;
- implementation status;
- source status;
- open questions.

No alias becomes a new module until a distinct responsibility is proven.

---

# 2. Experience Plane modules

## 2.1 Manus

**Plane:** Experience
**Status:** Operational external platform
**Mission:** Current preferred human cockpit and program-direction environment.

**Owns**
- conversational mission intake;
- long-running autonomous work;
- web and file interaction;
- deployment and deliverable presentation;
- human-facing orchestration experience.

**Does not own**
- canonical memory;
- architecture canon;
- system-routing truth;
- durable source-of-truth state.

**Canonical relation**
> Manus orchestrates the experience. Y-Nexus/ART orchestrates the system.

---

## 2.2 ChatGPT

**Plane:** Experience
**Status:** Operational external platform
**Mission:** Architecture, reasoning, synthesis, conversation, multimodal work, voice, and image generation.

**Strategic use**
- architecture definition;
- specifications;
- structured synthesis;
- contextual conversation;
- image generation/editing;
- voice and mobile interaction;
- Codex access where available.

**Constraint**
Major outputs require ARCH recovery and durable artifact creation.

---

## 2.3 Claude / Claude Code

**Plane:** Experience / execution interface
**Status:** Operational external platform
**Mission:** Long-context analysis, textual challenge, code review, second engineering path, and independent critique.

**Working doctrine**
- Claude Code challenges Codex or takes work where it is superior.
- Claude native UI is justified only by a measurable advantage and recoverability.

---

## 2.4 Gemini

**Plane:** Experience
**Status:** Operational external platform
**Mission:** Google-native multimodality, Workspace integration, video, and specialized visual capabilities.

---

## 2.5 Grok

**Plane:** Experience / Perception interface
**Status:** Operational external platform
**Mission:** Fast conversation, X-derived perception, heterodox reasoning, transformational and philosophical exploration.

---

## 2.6 OpenWebUI

**Plane:** Experience
**Status:** Historical/technical cockpit candidate
**Mission:** Self-hosted multi-model cockpit.

**Open**
Whether it remains a technical substrate for Y-Nexus or a superseded primary-cockpit concept.

---

## 2.7 Y-Menu

**Plane:** Experience
**Status:** Conceptually defined; archived repository exists
**Mission:** Y-OS shell/navigation and cognitive orchestration interface.

**Open**
Relationship to future Y-Nexus UI.

---

## 2.8 yOS Client

**Plane:** Experience
**Status:** Historical concept
**Mission:** General client layer across ChatGPT, Manus, Claude, Gemini, and future interfaces.

---

## 2.9 yOS Client for Obsidian / Y-OS Reader / yMD-OBS Reader

**Plane:** Experience / Knowledge boundary
**Status:** Materially specified; implementation evidence pending
**Mission:** Semantically interpret, display, navigate, and act on YMD, YMD-OBS, Markdown, and Obsidian content.

**Known subcomponents**
- yOS Startupizer;
- yMD-OBS Reader;
- yOS Panels;
- Visual Cockpit;
- Actions Layer;
- Plugin Packs.

---

## 2.10 Y-Nexus UI

**Plane:** Experience interface to Control
**Status:** Strategic target
**Mission:** Future sovereign Y-OS cockpit.

**Must expose**
- jobs;
- sessions;
- agents;
- costs;
- artifacts;
- context;
- status;
- approvals;
- source traceability.

---

# 3. Control Plane modules

## 3.1 Y-Nexus

**Plane:** Control
**Status:** Strategic target; implementation unverified
**Mission:** Sovereign control-plane boundary for jobs, policy, state, routing, permissions, budgets, and observability.

**Owns**
- Job identity;
- execution state;
- policy enforcement;
- budget and permission boundaries;
- orchestration interfaces;
- auditability;
- artifact handoff state.

**Does not own**
- canonical knowledge;
- raw source archive;
- model cognition itself.

---

## 3.2 Y-ORC

**Plane:** Control
**Status:** Strong historical canon; implementation claims exist
**Mission:** Operational orchestration runtime.

**Recovered formula**
```text
Y-ORC = CRT + ART + Workflow Planning + Routing
```

**Owns**
- intent-to-mission transformation;
- orchestration plans;
- route sequencing;
- Mission Pack construction;
- invocation of CRT and ART.

**Working placement**
Y-ORC is likely the orchestration runtime inside Y-Nexus.

---

## 3.3 CRT — Cognitive Routing Table

**Plane:** Control
**Status:** Strongly defined; runtime verification pending
**Mission:** Choose who thinks and how.

**Owns**
- model selection;
- ensemble selection;
- cognitive strategy;
- reasoning depth;
- debate, critique, and consensus patterns;
- cost/latency/quality trade-offs;
- privacy/locality constraints.

**Does not own**
- tools;
- effectors;
- action execution;
- context compilation.

---

## 3.4 ART — Agent & Resource Routing Table

**Plane:** Control
**Status:** Strongly defined; reportedly operational
**Mission:** Choose who or what acts and with which resources.

**Owns**
- agents and workers;
- non-LLM tools;
- APIs;
- MCP servers;
- browser and computer-use runtimes;
- CLI and local execution;
- SaaS tools;
- automations;
- effectors;
- human approval nodes.

**Does not own**
- model cognition selection;
- canonical knowledge;
- persistent result storage.

---

## 3.5 Y-CTX

**Plane:** Control
**Status:** Historical working canon
**Mission:** Determine what context is relevant.

**Owns**
- relevance policy;
- source scope;
- context priority;
- pack mode selection;
- freshness requirements.

---

## 3.6 CCR — Context Compiler Runtime

**Plane:** Control
**Status:** Implementation claims for v1/v2; verification pending
**Mission:** Compile provider-ready runtime context.

**Owns**
- context assembly;
- compression;
- token budgeting;
- FULL / COMPRESSED / MINIMAL variants;
- session delta integration;
- provider payload building;
- runtime packaging.

**Working distinction**
Y-CTX decides relevance. CCR compiles it.

---

## 3.7 MOP — Manus Orchestration Protocol

**Plane:** Control / Experience boundary
**Status:** Defined; partial implementation claimed
**Mission:** Standardize mission, artifact, state, and validation exchange between Manus and Y-OS.

**Working relation**
- MOP = protocol;
- Manus Bridge = adapter;
- Y-ORC = runtime;
- Y-Nexus = system boundary.

---

## 3.8 Manus Bridge

**Plane:** Control adapter
**Status:** Defined; implementation unverified
**Mission:** Connect Manus to Y-Nexus/Y-ORC through MOP.

---

## 3.9 Dispatcher / Intent Analyzer / Mission Builder

**Plane:** Control
**Status:** Recovered concepts; module boundaries unresolved
**Mission:** Analyze request intent, resolve complexity, construct a mission, and prepare execution.

**Anti-proliferation rule**
Treat as Y-ORC subfunctions until evidence proves independent services.

---

## 3.10 Y-REG

**Plane:** Control with Growth interface
**Status:** Strong historical canon; reportedly operational
**Mission:** Registry/catalogue of capabilities and activable objects.

**Owns**
- capability identity;
- aliases;
- type;
- version;
- maturity;
- availability;
- interface;
- dependency;
- owner;
- lifecycle status.

**Does not own**
- memory;
- semantic knowledge;
- raw conversations.

---

# 4. Cognitive Plane modules

## 4.1 PIE — Perception Intelligence Engine

**Plane:** Cognitive
**Status:** Current working canon
**Mission:** Universal perceptual ingress.

**Owns**
- observations from text, image, video, audio, OCR, sensors, APIs, web, and external systems;
- perceptual normalization;
- evidence signals;
- confidence metadata.

**Does not own**
- reasoning;
- canonization;
- knowledge promotion.

---

## 4.2 Knowledge function

**Plane:** Cognitive
**Status:** Canonical function
**Mission:** Make relevant structured knowledge available to cognition.

**Primary system interface**
KAP.

---

## 4.3 Reasoning module

**Plane:** Cognitive
**Status:** Required; final name open
**Historical candidates:** KRE, RIE, RISE
**Mission:** Inference, synthesis, judgment, planning, explanation, hypothesis formation.

---

## 4.4 Intention

**Plane:** Cognitive
**Status:** Canonical function; standalone-module status open
**Mission:** Transform understanding into goals, priorities, and commitments.

---

## 4.5 Agency

**Plane:** Cognitive
**Status:** Canonical function
**Mission:** Select and commit to actionable means.

**Important**
Agency is not identical to ART. Agency is the functional capacity; ART is a routing mechanism.

---

## 4.6 ACT

**Plane:** Cognitive / Execution boundary
**Status:** Open
**Mission:** Realize action through execution runtimes and effectors.

**Open questions**
- acronym expansion;
- relation to execution kernel;
- relation to browser/CLI/API/computer-use runtimes;
- where action result capture occurs.

---

## 4.7 Y-COM

**Plane:** Cognitive or Knowledge
**Status:** Recovered name; insufficient definition
**Mission:** Unknown pending source recovery.

---

## 4.8 Cognitive Graph / KGC

**Plane:** Cognitive / Knowledge boundary
**Status:** Implementation claims exist
**Mission:** Move from document graph to concept-level cognitive graph with typed relationships and navigation.

---

# 5. Knowledge Plane modules

## 5.1 Y-MEM

**Plane:** Knowledge
**Status:** Strong historical umbrella
**Mission:** Memory and continuity.

**Historical scope**
- episodic;
- semantic;
- procedural;
- working memory;
- retrieval;
- preferences;
- decisions;
- project history;
- sessions;
- documents;
- Context Packs.

**Open**
Whether Y-MEM remains an active umbrella or is decomposed across KAP, ARCH, Context, and storage systems.

---

## 5.2 Memory Gateway / Unified Memory API

**Plane:** Knowledge interface
**Status:** Architecturally defined
**Mission:** Unified access, routing, provenance, and retrieval across memory systems.

**Known interface candidates**
- OpenAPI;
- MCP;
- n8n webhooks.

---

## 5.3 Recall

**Plane:** Knowledge
**Status:** Historical component
**Mission:** Episodic/semantic ocean and source capture.

---

## 5.4 mem0

**Plane:** Knowledge
**Status:** Historical/tactical component
**Mission:** Memory service for extracted user/project memories.

---

## 5.5 KAP

**Plane:** Knowledge with Cognitive interface
**Status:** Current working canon; implementation partially verified through repository existence
**Mission:** Acquire, structure, resolve, and publish provenance-backed knowledge.

**Owns**
- knowledge acquisition;
- provenance;
- normalization;
- identity resolution;
- semantic relations;
- canonical knowledge graph;
- validated knowledge publication.

**Does not own**
- general reasoning;
- raw browser extraction;
- action routing.

---

## 5.6 ARCH Collector

**Plane:** Knowledge with Perception interface
**Status:** Designed; implementation pending/partial
**Mission:** Universal acquisition and preservation of LLM interactions, artifacts, attachments, versions, and deltas.

**Owns**
- source adapters;
- historical recovery;
- delta sync;
- immutable raw archive;
- completeness validation;
- source hashes;
- collection ledger.

---

## 5.7 ARCH Archaeology

**Plane:** Knowledge
**Status:** Designed
**Mission:** Reconstruct concept lineage, decisions, contradictions, supersessions, and historical emergence.

---

## 5.8 Source Ledger

**Plane:** Knowledge
**Status:** Required
**Mission:** Authoritative provenance registry.

**Minimum fields**
- source ID;
- provider;
- title;
- date;
- URI/path;
- hash;
- completeness;
- reliability;
- canonicality;
- destination;
- extraction status.

---

## 5.9 Artifact / Artifact Registry

**Plane:** Knowledge / Control boundary
**Status:** Artifact is canonical; standalone registry status open
**Mission:** Durable truth object and its identity/location metadata.

**Anti-proliferation rule**
Do not create a standalone registry until Y-REG, KAP, and Git responsibilities are audited.

---

## 5.10 Context Packs

**Plane:** Knowledge product consumed by Control
**Status:** Strong canon
**Modes:** FULL, COMPRESSED, MINIMAL
**Mission:** Explicit portable context for stateless or stateful agents.

---

## 5.11 Chronicles

**Plane:** Knowledge
**Status:** Canonical
**Mission:** Reflective, historical memory of how Y-OS and KOSMOS evolve and affect one another.

---

## 5.12 Git

**Plane:** Knowledge / implementation substrate
**Status:** Canonical source of durable implementation truth
**Mission:** Versioned code, architecture, ADRs, tests, and artifact history.

---

## 5.13 Obsidian

**Plane:** Knowledge / Experience interface
**Status:** Canonical human interface in existing repository governance
**Mission:** Human-readable local Markdown memory and graph navigation.

---

## 5.14 Notion

**Plane:** Knowledge / operational workspace
**Status:** Active, role unresolved
**Mission:** Documentation, structured operational pages, databases, staging, and publication.

---

## 5.15 Supabase

**Plane:** Knowledge/runtime infrastructure
**Status:** Historical candidate
**Mission:** Runtime cache/state, not philosophical source of truth.

---

## 5.16 Universe personal-data substrate

**Plane:** Knowledge
**Status:** Recovered concept requiring separation from YOUniverse/Y World
**Mission:** Personal Meta-Profile OS, Personal Data Vault, Life Knowledge Graph, AI Context Engine, and user-owned data layer.

---

# 6. Growth Plane modules and functions

## 6.1 Y-CAP — Capability Acquisition Protocol

**Plane:** Growth
**Status:** Explicitly validated historical concept
**Mission:** Acquire missing capabilities through discovery, evaluation, integration, and registration.

---

## 6.2 Y-DEV

**Plane:** Growth / implementation interface
**Status:** Explicit historical module
**Mission:** Build or adapt capabilities that do not yet exist.

**Recovered dependency**
Y-DEV had to precede development of Y-REG in one historical sequence.

---

## 6.3 Outcome Capture

**Plane:** Growth
**Status:** Required function
**Mission:** Record what was requested, executed, produced, failed, cost, and approved.

---

## 6.4 Evaluation

**Plane:** Growth
**Status:** Required function
**Mission:** Compare intended and actual outcomes across quality, reliability, cost, speed, and compliance.

---

## 6.5 Performance Memory

**Plane:** Growth
**Status:** Required function
**Mission:** Retain empirical performance history for models, agents, tools, workflows, and capabilities.

---

## 6.6 Routing Calibration

**Plane:** Growth
**Status:** Required function
**Mission:** Improve CRT and ART routing from observed outcomes.

---

## 6.7 Capability Lifecycle

**Plane:** Growth
**Status:** Required function
**Mission:** Manage discovery, trial, validation, promotion, maturity, deprecation, and retirement.

---

## 6.8 Experimentation and Promotion

**Plane:** Growth
**Status:** Required function
**Mission:** Test improvements safely and promote only through explicit gates.

---

## 6.9 Y-VAL

**Plane:** Historical proposal
**Status:** Rejected as standalone v1 module
**Decision:** Validation gates remain embedded in Y-ORC / Y-DEV and later Growth governance.

---

# 7. Cross-system roles

## 7.1 Codex

**Role:** Default engineering execution farm.

## 7.2 Claude Code

**Role:** Second engineer, challenger, long-text analyst, and code reviewer.

## 7.3 Manus

**Role:** Program direction and human-facing orchestration.

## 7.4 ChatGPT

**Role:** Architecture, synthesis, specification, and cognitive design.

## 7.5 n8n / Playwright / Home Assistant / APIs / MCPs

**Role:** ART-routable external tools and execution resources.

---

# 8. Registry completion rule

A module may be promoted to final canon only when:

1. its purpose is distinct;
2. its ownership is clear;
3. its aliases and lineage are mapped;
4. its interfaces are documented;
5. its implementation state is verified;
6. it does not duplicate another module;
7. its source evidence is recorded.
