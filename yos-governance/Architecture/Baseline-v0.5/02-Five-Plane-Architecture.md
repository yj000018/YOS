# Y-OS Architecture Baseline v0.5
## 02 — Five-Plane Architecture

**Status:** Strong working-canon candidate pending cross-source validation.

---

# 1. Why planes

The purpose of the plane model is to prevent all modules from appearing at the same conceptual level.

A plane groups modules that share:

- a common purpose;
- persistent responsibilities;
- coherent interfaces;
- a distinct source of truth;
- a distinct lifecycle.

The current best synthesis is a five-plane architecture:

```text
1. Experience Plane
2. Control Plane
3. Cognitive Plane
4. Knowledge Plane
5. Growth Plane
```

The planes are not a simple one-way stack. They form a governed loop.

```text
Experience
    ↓
Control
    ↓
Cognitive
    ↓
Knowledge
    ↓
Growth
    ↺ governed updates to every plane
```

---

# 2. Experience Plane

## Purpose

Provide human interaction, presentation, supervision, navigation, and vertical application interfaces.

## Known components and candidates

- Manus
- ChatGPT
- Claude
- Gemini
- Grok
- OpenWebUI
- Y-Menu
- yOS Client
- yOS Client for Obsidian
- Y-OS Reader
- yMD-OBS Reader
- Visual Cockpit
- future Y-Nexus UI
- vertical applications
- desktop interaction stack

## Current doctrine

- Manus is the preferred current human cockpit.
- Native LLM clients are specialized instruments, not canonical repositories.
- Y-Nexus is the future sovereign system interface.
- Obsidian remains a human-readable local knowledge interface.

## Experience Plane does not own

- routing truth;
- canonical memory;
- system policy;
- raw source archives;
- model cognition;
- durable implementation state.

---

# 3. Control Plane

## Purpose

Coordinate jobs, policies, permissions, budgets, context, routing, workflows, observability, and runtime state.

## Best current hierarchy

```text
Y-Nexus
├── Job and State Layer
├── Policy / Budget / Permission Layer
├── Observability
├── Y-ORC Runtime
│   ├── Intent Analysis
│   ├── Workflow Planning
│   ├── Mission Builder
│   ├── CRT
│   └── ART
├── Y-CTX
│   └── CCR
├── Y-REG interfaces
└── MOP / Manus Bridge
```

## Core functions

- convert user intent into a Y-OS Job;
- construct mission plans;
- select cognition strategy;
- select action resources;
- request relevant context;
- enforce policies and budgets;
- maintain runtime state;
- expose status and audit trails;
- coordinate human validation gates.

## Canonical formulas

```text
Y-ORC = CRT + ART + Workflow Planning + Routing
```

```text
CRT chooses who thinks and how.
ART chooses who or what acts and with which resources.
```

## Control Plane does not own

- canonical knowledge;
- raw source preservation;
- reasoning content itself;
- durable code history;
- uncontrolled self-modification.

---

# 4. Cognitive Plane

## Purpose

Transform reality and observations into knowledge-informed, intentional, actionable behavior.

## Cognitive spine

```text
Reality
→ Perception
→ Cognition
→ Agency
→ Action
```

## More detailed decomposition

```text
Reality
→ PIE / Perception
→ Knowledge
→ Reasoning
→ Intention
→ Agency
→ ACT / Action
→ Outcomes
```

## Known components

- PIE — Perception Intelligence Engine
- KAP cognitive interface
- Knowledge
- Reasoning
- Intention
- Agency
- ACT
- cognitive graph / KGC-related functions

## Key boundary principles

- Perception may be computationally complex without becoming reasoning.
- KAP structures knowledge but does not own general reasoning.
- ART is not identical to Agency.
- ACT is not yet fully defined and must not be prematurely renamed.

---

# 5. Knowledge Plane

## Purpose

Preserve sources, memory, artifacts, provenance, context products, structured knowledge, and historical lineage.

## Known components

- Y-MEM
- Memory Gateway
- Unified Memory API
- episodic memory
- semantic memory
- procedural memory
- working memory
- Recall
- mem0
- KAP
- KAP Graph
- K-card system
- ARCH Collector
- ARCH Archaeology
- Source Ledger
- Provenance Layer
- Artifact lineage
- Context Packs
- YMD / YMD-OBS
- Chronicles
- Git
- Obsidian
- Notion
- Supabase runtime cache
- Universe personal-data substrate

## Current role separation candidate

### Git

- implementation truth;
- versioned architecture artifacts;
- ADRs;
- code;
- tests;
- durable history.

### Obsidian

- local human-readable knowledge interface;
- graph navigation;
- canonical Markdown memory candidate.

### Notion

- active documentation and operational workspace;
- staging/publication role;
- not necessarily the canonical runtime core.

### Supabase

- runtime state/cache where appropriate;
- not the philosophical source of truth.

### ARCH

- evidence and history.

### KAP

- validated structured knowledge and provenance.

## Knowledge Plane does not own

- workflow orchestration;
- model selection;
- action execution;
- autonomous production routing;
- ungoverned promotion of hypotheses to canon.

---

# 6. Growth Plane

## Purpose

Observe outcomes, evaluate quality, learn from performance, evolve capabilities, and improve all other planes through governed change.

## Why Growth is likely a real plane

Growth owns persistent responsibilities that cannot be reduced to a decorative feedback arrow:

- outcome capture;
- evaluation;
- benchmark history;
- performance memory;
- CRT calibration;
- ART calibration;
- capability lifecycle;
- skill evolution;
- workflow improvement;
- experiment management;
- pruning and deprecation;
- promotion and rollback;
- architecture-evolution proposals.

## Existing concepts that may compose Growth

- Y-CAP — Capability Acquisition Protocol
- Y-DEV — Capability Development
- Y-REG lifecycle metadata
- Saraswati / learning role
- Memory Lifecycle
- Memory Routing Rules
- LMP / daily distillation concepts
- cognitive graph evolution
- self-learning Y-OS doctrine

## Growth loop

```text
Job
→ Cognition
→ Action
→ Outcome
→ Feedback
→ Evaluation
→ Learning
→ Capability Evolution
→ Routing Update
→ Next Job
```

## Governance boundary

Growth may:

- observe;
- propose;
- experiment;
- compare;
- recommend;
- promote through gates;
- roll back.

Growth may not:

- silently rewrite canon;
- modify identity without authorization;
- remove memory without recovery;
- change production routes without traceability;
- deploy architectural mutations without validation.

---

# 7. Cross-plane systems

Some systems legitimately span planes.

## KAP

- primary home: Knowledge Plane;
- cognitive interface: Knowledge formation and retrieval.

## ARCH Collector

- primary home: Knowledge Plane;
- perceptual interface: source acquisition and normalization.

## Y-REG

- primary home: Control Plane registry;
- Growth interface: lifecycle and performance metadata.

## Y-Nexus

- primary home: Control Plane;
- Experience interface: future sovereign UI.

## Y-OS Reader / yMD-OBS

- primary home: Experience Plane;
- Knowledge interface: semantic reading and navigation.

---

# 8. Main validation questions

1. Is Y-ORC definitively a runtime inside Y-Nexus?
2. Is Y-CTX a service/domain and CCR its runtime compiler?
3. Does Y-MEM remain an active umbrella or become a historical category?
4. Is KAP primarily Knowledge Plane with a Cognitive interface?
5. Is ARCH Collector an ingress application feeding PIE, or an independent source-preservation service?
6. Does Growth use existing Y-CAP/Y-DEV/Y-REG functions rather than creating new modules?
7. What is the exact boundary between Agency, ART, and ACT?
8. Which interface concept survives as the future sovereign cockpit: Y-Menu, Y-Nexus UI, or a composition?

---

# 9. Working-canon conclusion

The five-plane model is currently the clearest architecture for preserving complexity without flattening Y-OS into an undifferentiated module list.

It remains a **working canon** until GitHub, Manus, Obsidian/Markdown, Notion, and raw ARCH transcripts are reconciled.
