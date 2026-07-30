# Y-OS Architecture Baseline v0.5
## 05 — Concept Lineage and Supersession

**Status:** Working historical map pending raw ARCH transcripts and source-wave verification.

---

# 1. Purpose

This document preserves how Y-OS concepts evolved. It prevents accidental duplication, premature renaming, loss of rationale, and silent re-creation of rejected modules.

A lineage entry may be:

- `RENAMED`
- `SPLIT`
- `MERGED`
- `SUPERSEDED`
- `HISTORICAL`
- `ACTIVE`
- `UNRESOLVED`

---

# 2. Cockpit lineage

```text
OpenWebUI
→ Y-Menu / yOS Client
→ Manus as current primary experience cockpit
→ Y-Nexus UI as future sovereign cockpit
```

Interpretation:

- OpenWebUI = technical multi-model cockpit candidate;
- Y-Menu = Y-OS shell/navigation concept;
- yOS Client = broader cross-LLM client concept;
- Manus = current preferred user-facing orchestration environment;
- Y-Nexus UI = future sovereign system interface.

**Status:** Not a simple replacement chain. These may remain distinct layers.

---

# 3. Orchestration lineage

```text
Dispatcher / Intent Analyzer / Mission Builder
→ Y-ORC umbrella
→ CRT + ART + Context Pack + Workflow Planning + Routing
→ Y-Nexus Control Plane hosting Y-ORC runtime
```

Recovered canonical formula:

```text
Y-ORC = CRT + ART + Workflow Planning + Routing
```

Current reconciliation:

- Y-Nexus = sovereign control boundary;
- Y-ORC = orchestration runtime;
- CRT = cognitive routing;
- ART = action/resource routing;
- Dispatcher, Intent Analyzer, and Mission Builder = Y-ORC subfunctions unless independent implementation evidence exists.

---

# 4. Context lineage

```text
Context Builder
→ Y-CTX
→ CCR / Context Compiler Runtime
```

Current reconciliation:

- Y-CTX decides relevance and context policy;
- CCR compiles provider-ready runtime payloads;
- Context Packs are the durable portable product.

---

# 5. Collection lineage

```text
Universal Collector
→ multi-provider LLM collector concepts
→ browser-profile / Playwright collector
→ ARCH Collector
```

ARCH Collector broadens earlier collector concepts into:

- historical recovery;
- continuous delta capture;
- source completeness;
- attachment and artifact capture;
- append-only preservation;
- multi-provider adapters.

```text
ARCH Collector
→ ARCH Archaeology
```

This is a functional split, not a rename:

- Collector acquires and preserves;
- Archaeology interprets history and lineage.

---

# 6. Perception lineage

```text
Photo Intelligence Engine
→ Perception Intelligence Engine
```

The former photo domain becomes a vertical application or perceptual specialization using PIE. PIE itself becomes universal ingress.

---

# 7. Memory lineage

```text
Memory OS
→ Y-MEM umbrella
→ episodic + semantic + procedural + working memory
→ Memory Gateway / Unified Memory API
→ distributed architecture across KAP, ARCH, Context, and storage substrates
```

Recovered memory functions and components:

- episodic memory;
- semantic memory;
- procedural memory;
- working memory;
- Recall;
- mem0;
- Obsidian/Git;
- Memory Gateway;
- Unified Memory API;
- Context Packs.

**Open:** Whether Y-MEM remains an active umbrella or becomes a historical abstraction spanning KAP, ARCH, Context, and storage systems.

---

# 8. Knowledge lineage

```text
Memory graph / semantic memory
→ K-cards and canonical semantic layer
→ KAP knowledge architecture
→ KAP Graph and provider adapters
```

KAP must remain separate from general reasoning.

---

# 9. Registry lineage

```text
Tool Intelligence registry
→ activable-object registry
→ Y-REG
```

Y-REG evolved toward a central registry for:

- tools;
- capabilities;
- agents;
- skills;
- prompts;
- workflows;
- services;
- runtime resources.

**Open:** Exact boundary with Growth performance metadata and Artifact identity.

---

# 10. Reader and client lineage

```text
yOS Client
├── general cross-LLM client concept
└── yOS Client for Obsidian
       → Y-OS Reader
       → yMD-OBS Reader
```

Exact final names and implementation sequence require repository verification.

---

# 11. Reasoning lineage

Recovered candidate names:

```text
KRE
RIE
RISE
```

**Status:** unresolved. No final name may be selected without a dedicated decision and source review.

---

# 12. Action lineage

```text
Intention
→ Agency
→ ART routing
→ ACT execution
```

These must not be collapsed:

- Intention = chosen objective and commitment;
- Agency = capacity and decision to act;
- ART = route selection;
- ACT = execution/effectuation.

ACT naming and exact runtime scope remain open.

---

# 13. Growth lineage

```text
Feedback loop
→ Learning loop
→ self-learning Y-OS
→ Y-CAP + Y-DEV + Y-REG lifecycle
→ Capability Registry / performance memory
→ Growth Plane candidate
```

Existing concepts converging here:

- Y-CAP;
- Y-DEV;
- Y-REG lifecycle;
- evaluation;
- performance memory;
- routing calibration;
- skill evolution;
- pruning;
- promotion and rollback;
- Saraswati / learning role;
- Memory Lifecycle;
- cognitive graph evolution;
- LMP / daily distillation concepts.

**Important:** Growth should consolidate existing functions rather than multiply modules.

---

# 14. Validation lineage

```text
Y-VAL proposal
→ rejected as standalone v1 module
→ validation gates embedded in Y-ORC / Y-DEV
→ governed promotion and rollback in Growth
```

Y-VAL remains in the historical record to prevent accidental re-creation.

---

# 15. Storage lineage

Recovered sequence:

1. Notion as structured workspace/documentation.
2. Desire to migrate away from Notion.
3. Obsidian + Git selected as canonical/local/versioned core.
4. Supabase proposed as runtime cache/state.
5. Notion retained because a working documentation system should not be disrupted prematurely.

Current role hypothesis:

```text
Git = versioned implementation truth
Obsidian = local human-readable knowledge interface
Notion = active documentation/workspace/staging
Supabase = runtime cache/state
ARCH = immutable evidence
KAP = canonical structured knowledge
```

This is a role separation, not necessarily a single replacement event.

---

# 16. Ecosystem lineage

Concepts requiring careful separation:

```text
KOSMOS = ontological and philosophical summit
Y-OS = cognitive operating system
Memory OS = memory lifecycle subsystem
YOUniverse = private/meta ecosystem
Y World = public ecosystem expression
Universe = personal data and identity substrate candidate
YSpace = separate concept requiring recovery
Chronicles = historical and reflexive bridge
```

---

# 17. Historical organizational roles

Recovered OVC mapping:

- Krishna — strategy;
- Ganesha — execution plan;
- Brahma — architecture;
- Hanuman — build;
- Lakshmi — visibility;
- Saraswati — learning.

These are operational roles, not modules. They may map onto current planes and agents but must not be treated as system components without explicit evidence.

---

# 18. Lineage rules

1. A newer name does not automatically erase an older architecture.
2. Supersession requires explicit evidence.
3. Historical concepts remain searchable.
4. Rejected modules remain recorded.
5. Merges and splits require rationale.
6. Canon promotion requires source-backed ownership and interfaces.
7. Similar names are not separate modules unless their responsibilities differ materially.
8. Missing evidence produces an `OPEN` item, not an invented component.
