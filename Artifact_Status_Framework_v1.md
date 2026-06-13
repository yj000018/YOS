---
id: yos-artifact-status-framework-v1
title: Artifact Status Framework v1
type: artifact
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Manus Y-OS
tags:
- '#artifact'
- '#yos'
source_branch: y-os-doctrine
canonical: true
executed_by:
- '[[Saraswati]]'
---

# 3. Artifact Status Framework v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Purpose
To standardize the state machine of all Y-OS artifacts, enabling programmatic routing and clear governance.

## Standard States

1. **Draft:** 
   - *Definition:* The artifact is actively being created by the Producer.
   - *Action:* No downstream agent may consume or act upon this artifact.

2. **Ready For Review:**
   - *Definition:* The Producer has completed the artifact and submitted it to the Consumer.
   - *Action:* The Consumer must evaluate the artifact against the Acceptance Criteria.

3. **Accepted:**
   - *Definition:* The Consumer has validated the artifact. It is now official and immutable.
   - *Action:* The Consumer begins their phase of the Operational Value Chain using this artifact as input.

4. **Rejected:**
   - *Definition:* The Consumer found the artifact deficient, ambiguous, or in violation of constraints.
   - *Action:* The artifact is returned to the Producer with a mandatory Rejection Note. State reverts to Draft.

5. **Superseded:**
   - *Definition:* A newer version of this artifact has been Accepted.
   - *Action:* This version is retained for historical record but must not be used for active execution.

6. **Archived:**
   - *Definition:* The Operational Value Chain for this mission is complete.
   - *Action:* The artifact is moved to cold storage (Y-MEM) for future Learning and context hydration.

## Additional State Evaluated: "Blocked"
*Evaluation:* Should an artifact have a "Blocked" state? 
*Decision:* No. An artifact itself is never blocked; the *process* of creating it is blocked. If a Producer is blocked, they escalate via their communication contracts. The artifact remains in "Draft" until the block is resolved.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Saraswati]]
