# Current Best Knowledge Protocol

## 1. Definition
The Current Best Synthesis (CBS) represents the system's most accurate, up-to-date understanding of a concept, architecture, or domain, derived from all underlying Thought Lines and Decision Threads.

## 2. Properties
- **Derived, Not Primary:** CBS is a projection. The source of truth remains the raw fragments, thought lines, and decisions.
- **Ephemeral:** CBS can be regenerated at any time if the underlying data changes or if the synthesis algorithm improves.
- **Actionable:** AI agents and human operators use CBS for day-to-day operations without needing to read the entire history.

## 3. Generation Rules
1. **Trigger:** CBS is updated only when a Thought Line or Decision Thread reaches a stable `MERGED` or `ACCEPTED` state, and the `CURRENT-BEST-KNOWLEDGE-GATE` authorizes synthesis.
2. **Exclusion:** Contradictory or contested claims are excluded from the main CBS body and moved to an "Unresolved" section.
3. **Traceability:** Every statement in the CBS MUST link back to the specific Claim or Decision Thread that supports it.

## 4. Format
CBS documents are stored in Markdown, optimized for both human readability and LLM context injection. They include a header with the last update timestamp and the primary Thought Line IDs.
