# Artifact Lifecycle Operations v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## End-to-End Example: Strategy to Design

This illustrates the exact sequence of operations in the Registry during a handoff.

### Phase 1: Strategy Creation
1. Krishna creates a Strategy Brief.
   - `create_artifact(type='Strategy Brief', producer='Krishna', consumer='Ganesha', uri='...')`
   - State: **Draft**
2. Krishna finishes the brief.
   - `submit_for_review(ART-001)`
   - State: **Ready For Review**

### Phase 2: Planning Handoff
3. Ganesha runs his *Consumer Inbox Query* and finds `ART-001`.
4. Ganesha reviews the Strategy Brief.
5. Ganesha approves the brief.
   - `accept_artifact(ART-001)`
   - State: **Accepted**
6. Ganesha begins writing the Execution Plan.
   - `create_artifact(type='Execution Plan', producer='Ganesha', consumer='Brahma', parent_id='ART-001', uri='...')`
   - State: **Draft** (This is `ART-002`)
7. Ganesha finishes the Execution Plan.
   - `submit_for_review(ART-002)`
   - State: **Ready For Review**
8. Ganesha marks the Strategy Brief as consumed.
   - `consume_artifact(ART-001)`
   - State: **Consumed**

### Phase 3: Rejection Scenario
9. Brahma runs his *Consumer Inbox Query* and finds `ART-002`.
10. Brahma reviews the Execution Plan and finds it technically impossible.
11. Brahma rejects the plan.
    - `reject_artifact(ART-002, reason='Requires quantum computing.')`
    - State: **Rejected**
12. Ganesha runs his *Producer Rework Query*, sees the rejection, and creates a new Draft to fix it.
