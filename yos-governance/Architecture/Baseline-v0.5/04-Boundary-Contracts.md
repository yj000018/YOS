# Y-OS Architecture Baseline v0.5
## 04 — Boundary Contracts

**Status:** Working contracts pending runtime and source verification.

---

# 1. Contract principles

1. Every capability has one primary owner.
2. Cross-plane systems expose explicit interfaces rather than implicit overlap.
3. Inputs, outputs, state, provenance, and failure modes must be visible.
4. Stateless operation must remain possible through explicit artifacts and Context Packs.
5. No module may silently absorb another module's responsibilities.

---

# 2. Manus ↔ Y-Nexus

## Manus provides
- user intention;
- source files;
- project context;
- mission requests;
- human preferences;
- validation and approval feedback.

## Y-Nexus provides
- Job ID;
- accepted scope;
- execution state;
- plan;
- routed cognition and action resources;
- artifacts;
- costs;
- audit trail;
- recovery references.

## Boundary
Manus is the experience orchestrator, not the canonical system of record.

---

# 3. Y-Nexus ↔ Y-ORC

## Y-Nexus owns
- identity of jobs;
- policy;
- permissions;
- budget;
- runtime state;
- observability;
- user-visible status.

## Y-ORC owns
- orchestration plans;
- route sequencing;
- mission decomposition;
- CRT/ART invocation;
- Mission Pack construction.

## Boundary
Y-Nexus governs orchestration; Y-ORC performs orchestration.

---

# 4. Y-ORC ↔ CRT

## Request to CRT
- task objective;
- cognitive requirements;
- context envelope;
- quality target;
- latency target;
- cost ceiling;
- privacy/locality constraints;
- evaluation criteria.

## CRT returns
- selected model or ensemble;
- reasoning strategy;
- depth/effort;
- fallback route;
- confidence and assumptions;
- estimated cost and latency.

## Boundary
CRT chooses cognition. It does not select tools or execute actions.

---

# 5. Y-ORC ↔ ART

## Request to ART
- required capability;
- execution environment;
- input artifact references;
- expected output contract;
- permissions;
- human-validation requirements.

## ART returns
- selected worker or agent;
- tools;
- APIs;
- MCP servers;
- runtime;
- effectors;
- fallback route;
- execution constraints.

## Boundary
ART routes action resources. It does not choose cognitive models except where an agent bundle explicitly requires one and CRT has approved it.

---

# 6. Y-CTX ↔ CCR

## Y-CTX owns
- relevance policy;
- source selection;
- freshness;
- priority;
- sensitivity;
- requested Context Pack mode.

## CCR owns
- assembly;
- normalization;
- compression;
- token budgeting;
- provider formatting;
- session delta integration;
- payload generation.

## Boundary
Y-CTX decides what belongs. CCR decides how it is compiled.

---

# 7. Y-REG ↔ ART

## Y-REG provides
- capability identity;
- availability;
- maturity;
- version;
- interfaces;
- dependencies;
- ownership;
- policy tags.

## ART provides
- invocation history;
- execution results;
- failures;
- environment observations;
- runtime availability changes.

## Boundary
Y-REG describes what exists. ART chooses what to use.

---

# 8. PIE ↔ KAP

## PIE provides
- observations;
- normalized perceptual signals;
- source metadata;
- confidence;
- temporal context;
- evidence references.

## KAP provides
- resolved entities;
- canonical identities;
- structured knowledge;
- provenance links;
- knowledge-status decisions.

## Boundary
PIE perceives. KAP structures knowledge. PIE must not silently promote observations to canon.

---

# 9. KAP ↔ Reasoning

## KAP provides
- relevant knowledge;
- provenance;
- uncertainty;
- contradictions;
- graph relationships;
- canonical and non-canonical status.

## Reasoning provides
- inferences;
- hypotheses;
- synthesis;
- plans;
- explanations;
- questions requiring more evidence.

## Boundary
KAP owns knowledge representation. Reasoning owns inference and judgment.

---

# 10. Reasoning ↔ Intention

## Reasoning provides
- candidate conclusions;
- alternatives;
- risks;
- forecasts;
- recommended actions.

## Intention provides
- selected objectives;
- priorities;
- commitment level;
- constraints;
- success criteria.

## Boundary
Reasoning describes what may be true or effective. Intention commits the system toward a goal.

---

# 11. Intention ↔ Agency

## Intention provides
- desired outcome;
- priorities;
- values and policy constraints;
- acceptable trade-offs.

## Agency provides
- selected means;
- delegation choices;
- execution commitments;
- escalation needs.

## Boundary
Intention chooses what should be pursued. Agency chooses how to mobilize action.

---

# 12. Agency ↔ ART ↔ ACT

## Agency
Functional decision to act.

## ART
Selects agents, resources, tools, APIs, MCPs, runtimes, and effectors.

## ACT
Executes through the selected resources and returns outcome evidence.

## Boundary
Agency is a cognitive/systemic function. ART is routing. ACT is execution.

---

# 13. ARCH Collector ↔ PIE

## ARCH Collector provides
- raw source events;
- immutable archives;
- source metadata;
- completeness status;
- attachment inventory;
- hashes;
- deltas.

## PIE provides
- perceptual normalization;
- signal interpretation;
- observation schemas;
- confidence.

## Working boundary
ARCH Collector preserves source fidelity. PIE converts source material into perceptual observations.

---

# 14. ARCH Collector ↔ ARCH Archaeology

## Collector provides
- raw conversations;
- files;
- artifacts;
- timestamps;
- branches;
- extraction metadata;
- completeness.

## Archaeology provides
- architecture atoms;
- decisions;
- concept lineage;
- naming history;
- contradictions;
- supersession candidates;
- Chronicle material.

## Boundary
Collector acquires. Archaeology interprets history.

---

# 15. ARCH Archaeology ↔ KAP

## Archaeology provides
- traceable candidate statements;
- entity candidates;
- decision candidates;
- historical relations;
- conflicts;
- confidence.

## KAP provides
- identity resolution;
- canonical entities;
- structured graph;
- provenance-backed status;
- publication.

## Boundary
Archaeology reconstructs. KAP canonizes.

---

# 16. Growth ↔ CRT / ART

## CRT and ART provide
- route decisions;
- costs;
- latency;
- success/failure;
- quality scores;
- fallback usage;
- human corrections.

## Growth provides
- calibration updates;
- performance memory;
- route recommendations;
- experiment proposals;
- deprecation warnings.

## Boundary
Growth may recommend and promote through gates. It may not silently alter production routing.

---

# 17. Growth ↔ Y-REG

## Growth provides
- maturity changes;
- benchmark results;
- reliability history;
- promotion/deprecation decisions;
- lifecycle status.

## Y-REG provides
- capability identity;
- current version;
- contracts;
- dependencies;
- ownership;
- availability.

## Boundary
Growth evaluates lifecycle. Y-REG records the current registered state.

---

# 18. Git ↔ KAP ↔ ARCH

## Git
Versioned implementation and durable architecture artifacts.

## ARCH
Raw evidence and lineage.

## KAP
Canonical structured knowledge.

## Boundary
- Git answers: what was versioned and implemented?
- ARCH answers: what sources and historical evidence exist?
- KAP answers: what is currently structured and considered valid knowledge?

---

# 19. Failure contract

Every major cross-module call should eventually emit:

- request ID;
- Job ID;
- source artifact IDs;
- selected route;
- start/end timestamps;
- result artifact IDs;
- status;
- error classification;
- retries/fallbacks;
- human intervention;
- cost;
- provenance.

---

# 20. Open contract questions

1. Is ACT a standalone runtime or an umbrella over multiple executors?
2. Does Y-REG store performance directly or through Growth projections?
3. Where is Artifact identity canonically registered?
4. Does KAP publish Context Pack-ready views or only knowledge graph queries?
5. Does MOP include authentication and authorization or only mission semantics?
6. Which component owns human approval workflows?
7. How are cross-provider session identities normalized?
