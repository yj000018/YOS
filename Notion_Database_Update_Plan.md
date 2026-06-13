---
id: yos-notion-database-update-plan
title: Notion Database Update Plan
type: unknown
status: ACCEPTED
date: '2026-06-13'
owner: Manus Y-OS
tags:
- '#accepted'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
executed_by:
- '[[Brahma]]'
---

# Notion Database Update Plan

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Context

The current Artifact Registry database (ID: `4ae2fa35-d24f-4c44-be88-dbb808ea14cd`) requires schema updates to support the v1.1 Lineage Model.

Because the Notion MCP uses SQL DDL (`ALTER TABLE`) which does not natively support complex Notion-specific properties like self-referencing Relations, Checkboxes, or specialized Rollups, this update plan defines exactly how the database must be modified.

## 2. Properties to Add / Modify

### 2.1. True Relations (Manual UI Setup Required)
The Notion API and MCP DDL cannot easily create self-referencing relations. These must be configured in the Notion UI:
* **Parent Artifact:** Type `Relation`, linked to `Y-OS Artifact Registry` (self), Sync both ways (Two-way relation).
* **Child Artifacts:** Automatically created as the inverse of Parent Artifact.
* **Previous Version:** Type `Relation`, linked to `Y-OS Artifact Registry` (self), Sync both ways.
* **Next Version:** Automatically created as the inverse of Previous Version.
* **Root Artifact:** Type `Relation`, linked to `Y-OS Artifact Registry` (self), One-way relation.

### 2.2. Standard Properties (Via MCP/API)
* **Mission Name:** Type `Text`
* **Ready For Review Date:** Type `Date`
* **Open Loop Flag:** Type `Checkbox`
* **Blocking Issue:** Type `Rich Text`
* **Related ADRs:** Type `Text`
* **Related Laws:** Type `Text`

### 2.3. Cleanup
* Delete the temporary text proxy columns `Parent Artifact ID` and `Child Artifact IDs` created during the MVP patch, once data is migrated to the true Relations.

## 3. Execution Strategy

Since Manus operates headlessly and the MCP DDL is limited, the execution strategy is:

1. **Phase 1: API Fallback**
   Manus will attempt to create the simple properties (Checkbox, Date, Text) using the Notion API/MCP.
2. **Phase 2: Relation Proxies**
   If true Relations cannot be created programmatically, Manus will continue to use the Text proxy columns (`Parent Artifact ID`) but enforce the lineage logic strictly in code (Python runtime).
3. **Phase 3: User Handoff**
   Manus will instruct the user to manually convert the proxy text columns into true self-referencing Relations in the Notion UI, as this is a known limitation of the Notion API.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
