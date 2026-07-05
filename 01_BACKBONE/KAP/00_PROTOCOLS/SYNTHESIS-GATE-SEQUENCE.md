# Synthesis Gate Sequence

> Y-OS / KAP Cognitive Architecture
> Gate: SYNTHESIS-GATE-SEQUENCE-GATE
> Status: ACTIVE

---

## 1. Overview
The Synthesis Gate Sequence defines the strict, authorized progression from raw, unverified source fragments to a validated Current Best Synthesis. No step may be skipped, and synthesis cannot occur without explicit Guardian Architect approval at specific checkpoints.

## 2. The Sequence

### Phase 1: Acquisition & Mapping (Pre-Synthesis)
1. **SOURCE-SURFACE-DETECTION-GATE:** Identify boundaries of a knowledge source.
2. **METADATA-PROBE-GATE:** Extract metadata without reading content.
3. **CONTENT-EXTRACTION-GATE:** Pull raw content into quarantine.
4. **FRAGMENTATION-GATE:** Break raw content into atomic Source Fragments.

### Phase 2: Claim & Thread Generation (Analysis)
5. **CLAIM-EXTRACTION-GATE:** AI analyzes Source Fragments and generates atomic Claims.
6. **THOUGHT-LINE-SEEDING-GATE:** AI groups related Claims into candidate Thought Lines.
7. **DECISION-THREAD-EXTRACTION-GATE:** AI identifies historical decisions and maps them to the Decision Thread Model.

### Phase 3: Human Review & Validation (The Choke Point)
8. **CONTRADICTION-REVIEW-GATE:** Human reviews flagged contradictions and impasses.
9. **THOUGHT-LINE-VALIDATION-GATE:** Human approves the structure and maturity of candidate Thought Lines.
10. **DECISION-VALIDATION-GATE:** Human confirms the current validity of extracted decisions.

### Phase 4: Synthesis Generation
11. **CURRENT-BEST-KNOWLEDGE-AUTHORIZATION-GATE:** Human explicitly issues an MPM authorizing the generation of a Current Best Synthesis for specific, validated Thought Lines.
12. **SYNTHESIS-GENERATION-GATE:** AI generates the CBS Markdown document.
13. **SYNTHESIS-PUBLICATION-GATE:** Human reviews the generated CBS and authorizes its publication to the active control plane.

## 3. Enforcement
- An AI agent MUST halt execution and request an MPM before proceeding past any gate in Phase 3 or Phase 4.
- Attempting to generate a CBS without passing Gate 11 is a critical architecture violation.
