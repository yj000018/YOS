# DECISION-THREAD-RECONSTRUCTION-RUNBOOK

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Prerequisites for Reconstruction

A Decision Thread can only be reconstructed when there is clear evidence of a choice being made between alternatives. This evidence must be grounded in registered Claims or Source Fragments. Do not invent rationale or alternatives that are not explicitly present in the source material.

## 2. Preserving the Complete Context

When reconstructing a decision, the final outcome is only one part of the thread. It is equally important to document the rejected options and the rationale behind the final choice. This prevents historical amnesia and explains *why* the architecture is the way it is.

## 3. Active vs. Historical Decisions

Decisions must be clearly marked as either `active` (currently governing the system) or `historical` (superseded by a newer decision). A decision should only be marked as `active` if it is supported by the most recent, validated Claims.

## 4. Identifying Supersession

If a new Decision Thread clearly overrides an older one, the older thread must be updated to `superseded` status, and a formal link must be established between the two threads. This maintains the chronological integrity of the architecture.

## 5. Required Linkages

Every Decision Thread must include explicit links to the underlying evidence. This includes `claim_ids`, `source_fragment_ids`, and references to specific Git commits or Gate Reports where the decision was formalized.

## 6. Review Triggers

Reconstructing a major architectural decision (e.g., changing the primary repository structure or altering the source intake pipeline) always requires Guardian Architect review before the Decision Thread can be marked as `validated`.
