---
id: yos-lakshmi-mission-graph-engine
title: Lakshmi Mission Graph Engine
type: governance_report
status: ACCEPTED
date: '2026-06-13'
owner: Lakshmi
parent: '[[04_Governance_MOC]]'
tags:
- '#accepted'
- '#governance'
- '#lineage'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Mission Graph Engine

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Concept

The Mission Graph Engine reconstructs the state of a mission not by looking at a single field, but by traversing the artifact lineage.

## 2. Input Data

A flat list of normalized `Artifact` dictionaries parsed from the Notion Registry.

Required keys per artifact:
*   `id` (Name)
*   `mission_id`
*   `status`
*   `parent_id`
*   `child_ids` (list or comma-separated string)

## 3. Processing Logic

1.  **Group:** Group all artifacts by `mission_id`.
2.  **Identify Roots:** Find artifacts where `parent_id` is null or empty. (Should be Strategy Briefs).
3.  **Identify Terminals:** Find artifacts where `child_ids` is empty.
4.  **Determine Phase:** The "Current Phase" of the mission is determined by the `Artifact Type` of the most recently updated active artifact (Draft or Review) or the most recently Accepted artifact if none are active.
5.  **Determine Health:** 
    *   Red: If any P1 Open Loops exist for the mission.
    *   Yellow: If any P2 Open Loops exist.
    *   Green: Otherwise.

## 4. Output

A dictionary of `Mission` objects containing the reconstructed graph and computed metadata, ready for the Dashboard Data Model.
