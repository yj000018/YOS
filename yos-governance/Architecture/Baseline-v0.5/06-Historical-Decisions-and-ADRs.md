# Y-OS Architecture Baseline v0.5
## 06 — Historical Decisions and ADR Candidates

## Existing repository decisions
1. Git as durable source of truth.
2. Obsidian as human interface.
3. Local-first with Git fallback.
4. Monorepo as initial Y-OS architecture.
5. Historical role allocation: ChatGPT architecture, Manus primary execution, Claude fallback.

## Recovered stable decisions
- Fresh/stateless agents must work from explicit Context Packs and artifacts.
- Y-CTX decides relevance; CCR compiles context.
- CRT routes cognition; ART routes agents, tools, APIs, MCPs, runtimes, and effectors.
- Durable outputs are Artifacts with lineage.
- Y-REG is not memory.
- PIE is universal perception.
- KAP does not own general reasoning.
- Y-VAL was rejected as standalone v1.
- Major native-UI work requires measurable advantage and ARCH recovery.
- Consolidation precedes invention.

## Working decisions requiring validation
- Five planes: Experience, Control, Cognitive, Knowledge, Growth.
- Y-Nexus hosts Y-ORC.
- Growth is a full plane.
- KAP belongs primarily to Knowledge with Cognitive interface.
- ARCH Collector belongs primarily to Knowledge with Perception interface.

## Explicitly open
- reasoning-module name;
- ACT definition;
- Y-MEM decomposition;
- standalone Artifact Registry;
- Y-Menu/Y-Nexus relationship;
- Y-COM;
- KGC;
- LMP;
- Universe/YOUniverse/Y World/YSpace boundaries.

## ADR template
Every ADR must include context, decision, alternatives, consequences, migration, rollback, evidence, impacted modules, status, date, and owner.
