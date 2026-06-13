---
id: yos-registry-schema-v1.1
title: Registry Schema v1.1
type: artifact
status: ACCEPTED
date: '2026-06-13'
version: v1.1
owner: Manus Y-OS
tags:
- '#accepted'
- '#artifact'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
---

# Registry Schema v1.1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Overview

The Artifact Registry Schema v1.1 extends the MVP schema to support the **Artifact Lineage Model v1** and runtime execution tracking for Lakshmi and Y-ORC.

## 2. Complete Field Dictionary

| Field Name | Type | Required | Description |
|---|---|---|---|
| **Artifact ID** | Title | Yes | Unique identifier (e.g., ART-E2E-001). |
| **Artifact Type** | Select | Yes | Strategy Brief, Execution Plan, Architecture Package, Build Artifact, Build Report, Delivery Report, Learning Report, Lakshmi Review. |
| **Mission ID** | Text | Yes | The overarching mission this artifact belongs to. |
| **Mission Name** | Text | No | Human-readable name of the mission. |
| **Producer** | Select | Yes | The agent who creates the artifact. |
| **Consumer** | Select | Yes | The agent who consumes the artifact next. |
| **Review Owner** | Select | Yes | The agent responsible for accepting/rejecting the artifact. |
| **Status** | Select | Yes | Draft, Ready For Review, Accepted, Rejected, Consumed, Superseded, Archived. |
| **Version** | Text | Yes | Version string (e.g., v1.0). |
| **Root Artifact** | Relation | No | Link to the Strategy Brief that initiated the mission. |
| **Parent Artifact** | Relation | No | Link to the immediate upstream artifact. |
| **Child Artifacts** | Relation | No | Link(s) to the immediate downstream artifact(s). |
| **Previous Version** | Relation | No | Link to the superseded version of this artifact (if reworked). |
| **Next Version** | Relation | No | Link to the new version of this artifact (if superseded). |
| **Created Date** | Date | Yes | Timestamp of creation. |
| **Updated Date** | Date | Yes | Timestamp of last modification. |
| **Ready For Review Date** | Date | No | Timestamp when status changed to Ready For Review. |
| **Accepted Date** | Date | No | Timestamp when status changed to Accepted. |
| **Consumed Date** | Date | No | Timestamp when status changed to Consumed. |
| **Archived Date** | Date | No | Timestamp when status changed to Archived. |
| **URI** | URL | Yes | Link to the actual artifact document. |
| **Acceptance Notes** | Rich Text | No | Notes provided by the Review Owner upon acceptance. |
| **Rejection Notes** | Rich Text | No | Notes provided by the Review Owner upon rejection. |
| **Open Loop Flag** | Checkbox | Yes | True if this artifact is currently blocking the mission. |
| **Blocking Issue** | Rich Text | No | Description of what is blocking progress. |
| **Related ADRs** | Text | No | Comma-separated list of relevant ADRs. |
| **Related Laws** | Text | No | Comma-separated list of relevant Y-OS Laws. |

## 3. Key Schema Changes from v1.0

1. **True Relations:** Parent/Child are upgraded from Text proxies to true Notion Relations.
2. **Versioning Lineage:** Added `Previous Version` and `Next Version` relations.
3. **Root Anchor:** Added `Root Artifact` to easily query all artifacts in a mission without recursive graph traversal.
4. **Runtime Flags:** Added `Open Loop Flag` and `Blocking Issue` to allow agents to explicitly signal bottlenecks without waiting for Lakshmi's timeout heuristics.
5. **State Timestamps:** Formalized `Ready For Review Date` to measure review latency accurately.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
