# ADR-0037: CCR Runtime v2 — Production Context Orchestration

## Status
Accepted

## Context
MISSIONS 001-010B validated that Context Packs compiled from artifacts outperform raw conversational history, and that Canonical Memory is the primary differentiator for organizational truth. However, raw session history was found to degrade quality and ROI. To scale Y-OS to production, we need a formalized Context Compiler Runtime (CCR) v2 that orchestrates these findings into an executable architecture.

## Decision
We adopt CCR Runtime v2 as the production context orchestration layer for Y-OS. 

Key architectural mandates:
1. **Raw session history is banned.** It is replaced by the structured Session Delta schema.
2. **MODE-B (Context Pack Only)** is the default production mode.
3. **MODE-D (Context Pack + Canonical Memory)** is reserved for governance, strategy, and constitutional capabilities.
4. **Git + Obsidian** is designated as the future canonical storage architecture, transitioning away from Notion as the primary registry.

## Consequences
- **Positive:** Token costs will decrease significantly while output quality increases. Hallucination risk drops due to the removal of session noise. The system becomes Git-native, enabling robust version control of organizational memory.
- **Negative:** Increased complexity in the Context Router layer. Requires immediate development of the Session Delta extraction logic.

## Compliance
- **Article I (Artifact Primacy):** Maintained. Context Packs are strictly derived from artifacts.
- **Article II (Preservation Principle):** Maintained. Git architecture ensures permanent preservation.
- **Article III (Derivation Transparency):** Maintained. Session Deltas and Context Packs explicitly log lineage.
