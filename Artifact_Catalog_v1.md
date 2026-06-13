---
id: yos-artifact-catalog-v1
title: Artifact Catalog v1
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
---

# 2. Artifact Catalog v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Official Y-OS Artifacts

| Artifact Name | Producer | Consumer | Purpose | Lifecycle Phase |
| :--- | :--- | :--- | :--- | :--- |
| **Strategy Brief** | CSO (Krishna) | COO (Ganesha) | Defines the "What" and "Why" of a mission. Establishes the ultimate success criteria. | Strategy |
| **Execution Plan** | COO (Ganesha) | Chief Architect (Brahma) | Defines the "When" and "Who". Allocates resources, sets timelines, and establishes operational constraints. | Execution Planning |
| **Architecture Package** | Chief Architect (Brahma) | Lead Developer (Hanuman) | Defines the "How". The structural blueprint, data models, and component interfaces required to build the system. | Design |
| **Build Artifact** | Lead Developer (Hanuman) | Target System / End User | The operational result (code, document, data structure). | Build |
| **Build Report** | Lead Developer (Hanuman) | COO (Ganesha) | Documents the build process, technical debt, deviations from architecture, and testing results. | Build |
| **Delivery Report** | COO (Ganesha) | CEO (Yannick) / CSO (Krishna) | Confirms operational deployment, validates against Strategy Brief, and closes the active execution loop. | Delivery |
| **Learning Report** | CODO (Saraswati) | Y-OS System (All Agents) | Analyzes the completed artifact chain to update Y-OS Laws, agent prompts, and operational frameworks. | Learning |

## Ownership Rules
- The **Producer** holds write access during the creation phase.
- Once transitioned to "Ready for Review", the artifact becomes read-only for the Producer.
- The **Consumer** holds the authority to Accept or Reject the artifact.
- Once "Accepted", the artifact is immutable. Any changes require a new version or an explicit amendment artifact (e.g., an ADR).
