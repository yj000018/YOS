# Communication Contracts: Build Phase

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Purpose
To formalize the inputs and outputs surrounding the Lead Developer (Hanuman) to ensure zero information loss and strict adherence to the Operational Value Chain.

---

## 1. Handoff: Brahma → Hanuman

**Purpose:** Initiate the Build Phase.

**Required Input Package:**
- Architecture Package (following the official standard).
- Relevant ADRs.
- (Implicit) Execution Mandate from COO.

**Acceptance Criteria (Hanuman accepts):**
- The Architecture Package is complete (no "TBD" sections for core components).
- The defined interfaces are unambiguous.
- The required technologies are available in the sandbox/environment.

**Rejection Criteria (Hanuman rejects):**
- Ambiguous data models or API contracts.
- Reliance on unavailable tools.
- Logical contradictions in the system design.

---

## 2. Clarification Loop: Hanuman ↔ Brahma

**Purpose:** Resolve technical blockers during the build without breaking architecture.

**Required Input (from Hanuman):**
- Specific architectural ambiguity or runtime failure directly related to the design.

**Required Output (from Brahma):**
- Clarification or formal Design Amendment (ADR update).

**Constraint:** Hanuman must not guess or invent architecture. If the blueprint is flawed, Brahma must fix the blueprint.

---

## 3. Handoff: Hanuman → COO (Ganesha)

**Purpose:** Conclude the Build Phase and initiate Validation.

**Required Input Package:**
- Functional Code / Built Artifact.
- Build Report (Noting any minor deviations from the Architecture Package).

**Acceptance Criteria (Ganesha accepts):**
- The artifact runs without fatal errors.
- The artifact passes the Architectural Acceptance Criteria defined by Brahma.
- The Build Report is complete.

**Rejection Criteria (Ganesha rejects):**
- The artifact fails to run.
- Hanuman unilaterally altered the architecture without Brahma's approval (violates governance).
- Missing or incomplete Build Report.
