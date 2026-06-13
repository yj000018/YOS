---
id: yos-ceo-briefing-standard-v1
title: CEO Briefing Standard v1
type: ceo_briefing
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Ganesha
related_adrs:
- '[[ADR-0014]]'
tags:
- '#artifact'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# CEO Briefing Standard v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Purpose
The CEO Briefing is the primary communication artifact from ECO (Lakshmi) to the CEO (Yannick). It is designed to be consumed in under 60 seconds, providing maximum signal with minimum noise.

## Standard Template

### 1. Executive Summary
- A 2-sentence synthesis of the current state of Y-OS. (e.g., "All execution pipelines are green. Mission Alpha is blocked awaiting your strategic approval.")

### 2. Decisions Required (Urgent)
- A bulleted list of items requiring immediate CEO input to unblock the Operational Value Chain.
- Format: `[Artifact Name] - [Blocker Description] - [Action Required]`

### 3. Actions Required (Non-Urgent)
- Items the CEO needs to do, but which are not currently blocking active execution.

### 4. Mission Status Highlights
- **Completed:** Missions delivered since the last briefing.
- **At Risk:** Missions exceeding time/cost budgets or failing governance.
- **On Track:** Brief confirmation of major ongoing work.

### 5. Cost & Health Anomalies
- Only included if there is a deviation from baseline (e.g., "Token spend spiked 400% on Hanuman during Mission Beta").

### 6. Recommendations
- Lakshmi's synthesized advice based on observation (e.g., "Recommend pausing Mission Gamma until ADR-0014 is resolved").
