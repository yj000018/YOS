---
id: yos-lakshmi-ceo-briefing-generator-v1
title: Lakshmi CEO Briefing Generator v1
type: governance_report
status: OFFICIAL
date: '2026-06-12'
version: v1
owner: Lakshmi
parent: '[[04_Governance_MOC]]'
tags:
- '#governance'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# CEO Briefing Generator v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
The CEO Briefing is a highly condensed, narrative summary generated daily by Lakshmi, designed to be read in under 60 seconds.

## Generation Pipeline

### Step 1: Data Extraction
Lakshmi extracts:
1. Artifacts that transitioned to `Accepted` or `Consumed` in the last 24h.
2. Artifacts currently `Rejected` or stalled (from Open Loops Engine).
3. Open Loops assigned to the CEO.

### Step 2: LLM Synthesis Prompt
The extracted data is passed to an LLM (e.g., Claude Opus) with the following system prompt:

> You are ECO (Lakshmi). Write the daily CEO Briefing for Yannick.
> Format strictly as:
> 1. **The Pulse:** One sentence summarizing organizational momentum.
> 2. **Victories:** Bullet points of artifacts accepted/consumed today.
> 3. **Frictions:** Bullet points of stalled/rejected artifacts.
> 4. **Your Actions:** What Yannick specifically needs to do today.
> Tone: Executive, calm, zero fluff.

### Step 3: Delivery
The generated text is published to the top of the Executive Dashboard and optionally pushed via webhook to the CEO's preferred communication channel.
