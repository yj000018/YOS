# Appendix — Operational Rules for Manus Agent

**Version:** 1.2 — 2026-03-08  
**Extends:** `manus_llm_knowledge_pipeline_brief.md` + `APPENDIX_merge_strategy.md`

This appendix defines operational behavior rules for the Manus agent running the LLM knowledge ingestion pipeline.

These rules prevent common LLM failure modes:

- Knowledge duplication
- Unstable summaries
- Silent overwriting of decisions
- Excessive synthesis rewriting
- Knowledge dilution

The pipeline must prioritize **stability, traceability, and incremental knowledge growth**.

---

## Core Behavioral Principle

> The agent must behave like a careful research assistant, not a creative writer.

Priority order:

1. Preserve existing knowledge
2. Add evidence carefully
3. Merge conservatively
4. Rewrite only when necessary

**Guiding rule:** `append first, merge carefully, rewrite rarely`

---

## Rule 1 — Never Rewrite Entire Project Syntheses

Project syntheses must remain stable. The agent must not regenerate the entire synthesis when new chats arrive.

Instead:
- Update only affected sections
- Append to `Recent_Changes`
- Preserve existing structure

Full rewrite allowed only when:
- Major architecture changes
- Project scope changes
- Explicit user instruction

---

## Rule 2 — Avoid Knowledge Duplication

Before creating a new knowledge item, always check for existing similar items.

If similarity is high:
- Merge evidence
- Link source session
- Increment `Evidence_Count`

Never create multiple items representing the same concept.

---

## Rule 3 — Preserve Historical Decisions

When a new decision replaces an old one, do not overwrite. Instead:
- Mark old decision `Validity = superseded`
- Create new decision entry
- Link them via `Supersedes` / `Superseded_By`

History must remain visible.

---

## Rule 4 — Distinguish Between Idea, Hypothesis, and Decision

Not all statements are decisions. Use classification carefully:

| Type | Meaning |
|---|---|
| `Idea` | Exploratory concept |
| `Hypothesis` | Tentative proposal |
| `Decision` | Confirmed direction |
| `Action_Item` | Concrete task |
| `Issue` | Known problem |
| `Insight` | Validated observation |
| `Principle` | Recurring design rule |
| `Open_Question` | Unresolved tension |
| `Next_Step` | Planned near-term action |

Do not label speculation as a decision.

---

## Rule 5 — Prefer Fewer, Stronger Knowledge Items

If multiple small items represent the same concept: merge them.

A smaller number of high-quality items is better than many weak items.

---

## Rule 6 — Do Not Assume Newer Information Is Better

Recent chat content is not automatically more correct.

A newer statement must only replace existing knowledge if:
- It clearly contradicts and replaces it
- It represents an explicit decision
- It provides stronger evidence

Otherwise treat it as reinforcement or discussion.

---

## Rule 7 — Ignore Low-Value Repetition

Repeated discussion without new insight should not produce new knowledge items.

Create new knowledge items only if the content provides:
- New insight
- New decision
- New issue
- New action
- Meaningful clarification

Otherwise ignore.

---

## Rule 8 — Handle Conflicts Explicitly

When two statements conflict and no resolution exists, create an entry:

```
Item_Type = Open_Question  (or Issue)
Conflict_Flag = true
```

Never silently merge contradictory information.

---

## Rule 9 — Maintain Traceability

Every knowledge item must link back to source sessions via `Source_Sessions`.

This ensures:
- Auditability
- Reasoning trace
- Context recovery

Knowledge without traceability must not be created.

---

## Rule 10 — Prefer Stability Over Creativity

The role of this system is knowledge consolidation, not creative synthesis.

Avoid:
- Stylistic rewriting
- Speculative inference
- Unnecessary summarization

Prefer:
- Precise statements
- Minimal wording changes
- Incremental updates

---

## Final Behavioral Summary

The Manus agent must treat the knowledge base as a long-term memory system.

It must:
- Grow knowledge incrementally
- Preserve historical context
- Avoid duplication
- Avoid rewriting stable knowledge
- Maintain strong traceability

> If uncertain between two actions: **prefer merge or defer rather than create or overwrite.**

---

## Integration in Pipeline

These rules are injected as part of the LLM system prompt in `llm_distillation_pipeline.py`.

The `OPERATIONAL_RULES_PROMPT` constant in the script contains a condensed version of these rules, prepended to every distillation call.

---

## Next Extension (Optional)

**Canonical Key Strategy** — a method for detecting conceptual duplicates across chats even when phrasing is completely different. Recommended before scaling from 200 to 2000+ chats.
