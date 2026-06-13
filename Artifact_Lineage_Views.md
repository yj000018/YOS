---
id: yos-artifact-lineage-views
title: Artifact Lineage Views
type: artifact
status: ACCEPTED
date: '2026-06-13'
owner: Manus Y-OS
tags:
- '#accepted'
- '#artifact'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Artifact Lineage Views

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Overview

To make the Artifact Registry useful for human executives (CEO) and ECO (Lakshmi), the database must expose specific views that leverage the new Lineage Model.

## 2. Required Views

### 2.1. Mission Artifact Chain (Kanban)
* **Type:** Board
* **Group by:** `Mission ID`
* **Sub-group by:** `Status`
* **Sort:** `Created Date` (Ascending)
* **Visible Properties:** `Artifact Type`, `Producer`, `Consumer`, `Open Loop Flag`
* **Purpose:** Visualizes the full flow of a mission from left to right.

### 2.2. Active Lineage (List)
* **Type:** List
* **Filter:** `Status` is NOT `Archived` AND `Status` is NOT `Superseded`
* **Sort:** `Mission ID`, then `Created Date`
* **Visible Properties:** `Parent Artifact`, `Child Artifacts`, `Status`
* **Purpose:** Shows the current causal chain of active missions.

### 2.3. Broken Lineage (Table)
* **Type:** Table
* **Filter:** `Status` = `Accepted` AND `Child Artifacts` is empty AND `Artifact Type` is NOT `Learning Report` (or other terminal types).
* **Purpose:** Identifies artifacts that have been accepted but have not triggered the next step in the value chain. Critical for Y-ORC.

### 2.4. Pending Review (Board)
* **Type:** Board
* **Group by:** `Review Owner`
* **Filter:** `Status` = `Ready For Review`
* **Visible Properties:** `Ready For Review Date`, `Producer`
* **Purpose:** Shows exactly who is blocking the pipeline.

### 2.5. Open Loops (Table)
* **Type:** Table
* **Filter:** `Open Loop Flag` = `True`
* **Visible Properties:** `Blocking Issue`, `Review Owner`, `Consumer`
* **Purpose:** The primary data source for Lakshmi's Executive Dashboard.

### 2.6. Superseded Artifacts (Table)
* **Type:** Table
* **Filter:** `Status` = `Superseded`
* **Visible Properties:** `Next Version`, `Rejection Notes`
* **Purpose:** Historical audit trail of rework and architectural pivots.
