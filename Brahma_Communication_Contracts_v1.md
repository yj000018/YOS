# Communication Contracts: Design Phase

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Purpose
To formalize the inputs and outputs surrounding the Chief Architect (Brahma) to ensure zero information loss and strict adherence to the Operational Value Chain.

---

## 1. Handoff: COO (Ganesha) → Brahma

**Purpose:** Initiate the Design Phase.

**Required Input Package:**
- Execution Plan (Timeline, resources).
- Strategy Brief (The "Why" and "What").
- Explicit constraints (Budget, tech stack limits).

**Acceptance Criteria (Brahma accepts):**
- The objective is clear.
- The constraints are not mutually exclusive (e.g., "build it in 1 hour but make it perfectly scalable").
- The Strategy Brief is included (Brahma cannot design blindly from an Execution Plan alone).

**Rejection Criteria (Brahma rejects):**
- Missing Strategy Brief.
- Contradictory constraints.
- Insufficient time allocated for the design phase.

---

## 2. Handoff: Brahma → Lead Developer (Hanuman)

**Purpose:** Initiate the Build Phase.

**Required Input Package:**
- Architecture Package (following the official standard).
- Relevant ADRs.

**Acceptance Criteria (Hanuman accepts):**
- The Architecture Package is complete (no "TBD" sections for core components).
- The defined interfaces are unambiguous.
- The required technologies are available in the sandbox/environment.

**Rejection Criteria (Hanuman rejects):**
- Ambiguous data models or API contracts.
- Reliance on unavailable tools.
- Logical contradictions in the system design.

---

## 3. Feedback Loop: Hanuman → COO (Ganesha)

**Purpose:** Conclude the Build Phase and initiate Validation.

**Required Input Package:**
- Functional Code / Built Artifact.
- Build Report (Noting any minor deviations from the Architecture Package).

**Acceptance Criteria (Ganesha accepts):**
- The artifact runs without fatal errors.
- The artifact passes the Architectural Acceptance Criteria defined by Brahma.

**Rejection Criteria (Ganesha rejects):**
- The artifact fails to run.
- Hanuman unilaterally altered the architecture without Brahma's approval (violates governance).
