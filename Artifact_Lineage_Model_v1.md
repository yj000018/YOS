---
id: yos-artifact-lineage-model-v1
title: Artifact Lineage Model v1
type: artifact
status: ACCEPTED
date: '2026-06-13'
version: v1
owner: Manus Y-OS
tags:
- '#accepted'
- '#artifact'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Artifact Lineage Model v1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Context & Purpose

The First End-to-End Y-OS Run (MISS-E2E-V1) proved that the Operational Value Chain works, but exposed a critical flaw in the Artifact Registry: **artifacts are tracked as isolated nodes, not as a connected graph.**

Without explicit lineage, it is impossible for the system (Y-ORC, Lakshmi, Saraswati) to programmatically reconstruct a mission, detect missing dependencies, or understand the impact of a rejected artifact.

This model formalizes how artifacts are connected into a **Mission Graph**.

## 2. The Lineage Principles

1. **Every artifact belongs to a Mission.** A Mission is a container, not an artifact itself.
2. **Lineage is immutable.** Once a relationship is established, it cannot be deleted (only superseded by a new version).
3. **Lineage is bidirectional.** If A is the parent of B, B is the child of A.
4. **Lineage is causal.** An artifact cannot be consumed until its parent is accepted.

## 3. The Lineage Dimensions

The Lineage Model operates across three dimensions:

### 3.1. Vertical Lineage (Causality)
This tracks the flow of intent down the Operational Value Chain.
* **Root Artifact:** The first artifact in a mission (always a Strategy Brief). It has no parent.
* **Parent Artifact:** The immediate upstream artifact that triggered the creation of the current artifact. (e.g., Execution Plan is the parent of Architecture Package).
* **Child Artifact(s):** The downstream artifacts generated as a direct result of consuming the current artifact.

### 3.2. Horizontal Lineage (Versioning)
This tracks the evolution of a specific artifact through rework cycles.
* **Previous Version:** If an artifact is rejected and rewritten, the new draft points to the rejected version as its "Previous Version".
* **Next Version:** The rejected version points to the new draft as its "Next Version".

### 3.3. Transversal Lineage (Context)
This tracks relationships outside the strict causal chain.
* **Related ADRs:** Architectural Decision Records that constrain or influence this artifact.
* **Related Laws:** Y-OS First Principles that apply to this artifact.

## 4. The Canonical Mission Graph

A healthy, completed mission forms the following linear graph:

```text
[Root] Strategy Brief (Krishna)
  └── [Child] Execution Plan (Ganesha)
        └── [Child] Architecture Package (Brahma)
              └── [Child] Build Artifact (Hanuman)
                    ├── [Child] Build Report (Hanuman)
                    └── [Child] Delivery Report (Ganesha)
                          └── [Child] Learning Report (Saraswati)
```

*(Note: Build Artifact and Build Report are siblings, both children of the Architecture Package. Delivery Report is a child of the Build Report.)*

## 5. System Implications

With explicit lineage:
* **Y-ORC** can trigger the next agent by finding the accepted artifact and checking if it has children. If not, it routes to the Consumer.
* **Lakshmi** can detect "Broken Lineage" (an accepted artifact with no children that is not a terminal report).
* **Saraswati** can trace a failure in the Build phase all the way back to an ambiguity in the Strategy Brief.
