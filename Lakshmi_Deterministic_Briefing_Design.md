---
id: yos-lakshmi-deterministic-briefing-design
title: Lakshmi Deterministic Briefing Design
type: governance_report
status: ACCEPTED
date: '2026-06-13'
owner: Lakshmi
parent: '[[04_Governance_MOC]]'
tags:
- '#accepted'
- '#governance'
- '#yos'
source_branch: y-os-doctrine
canonical: true
executed_by:
- '[[Brahma]]'
---

# Deterministic Briefing Design

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Purpose

To guarantee executive visibility even when LLM synthesis fails. This template is hardcoded in Python and populated directly from the Dashboard Data Model.

## 2. Template Structure

```text
================================================
LAKSHMI CEO BRIEFING (DETERMINISTIC FALLBACK)
================================================
Date: {YYYY-MM-DD HH:MM UTC}
Status: {System Health based on Open Loops: Green/Yellow/Red}

-- METRICS --
Total Missions: {X}
Active Missions: {X}
Blocked Missions: {X}
Completed Missions: {X}

-- OPEN LOOPS (ACTION REQUIRED) --
{List of P1/P2 open loops, formatted as:
* [Severity] Rule: Description (Mission: ID) -> Assignee: Role}
(If none: "Zero open loops detected.")

-- MISSION HEALTH --
{List of active/blocked missions, formatted as:
* Mission ID (Status) - Phase: {Current Phase}}

-- REQUIRED DECISIONS (CEO) --
{List of artifacts waiting for CEO review or open loops assigned to CEO}

================================================
Note: This briefing was generated deterministically due to LLM synthesis unavailability.
```

## 3. Trigger Conditions

The deterministic fallback is triggered if `generate_ceo_briefing_llm()` raises an exception, times out, or returns a string shorter than 50 characters (e.g., "LLM returned empty response").


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
