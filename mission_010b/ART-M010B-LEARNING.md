---
id: yos-art-m010b-learning
title: ART-M010B-LEARNING
type: learning_report
status: ACCEPTED
mission: MISSION-010B
date: '2026-06-13'
owner: Saraswati
parent: '[[03_Missions_MOC]]'
related_missions:
- '[[mission_010b]]'
tags:
- '#accepted'
- '#artifact'
- '#memory'
- '#yos'
aliases:
- MISSION-010B
source_branch: y-os-doctrine
canonical: true
implements:
- '[[Context_Pack]]'
executed_by:
- '[[Saraswati]]'
---

# Saraswati Learning Report

# MISSION-010B Learning Extraction

## 1. Diminishing Returns Threshold

**Returns diminish sharply after ~620 tokens (Config B)**. The jump from 503→623 tokens yields +1.8 quality points. Every subsequent addition yields less quality per token, with Config F achieving only +0.4 improvement at 2.5x the token cost.

## 2. Session History as Noise Source

**Yes, session history introduces noise in structured benchmarks.** Config F vs D: adding 173 session tokens *decreased* quality by 1.0 points. Session history likely contains conversational artifacts, corrections, and tangential context that dilute signal density. This confirms session history serves *continuity* not *quality*.

## 3. Context Pack vs Canonical Memory

**Context Pack alone nearly matches combined approaches.** Config B (87.8) outperforms Config D (87.4) despite D having both sources. The Context Pack's curated, pre-structured format delivers higher signal density than raw canonical memory. However, Canonical Memory may provide value for *edge cases* not captured in Context Packs.

## 4. Minimum Viable Context for Y-OS Production

**Recommended: Context Pack Only (~620 tokens) as baseline**, with Canonical Memory as optional enhancement for complex queries. Session history should be used *only* for multi-turn continuity, not injected by default.

## 5. ADR Update: Key Learning

> **Context quality trumps context quantity.** Pre-structured Context Packs achieve 87.8 quality at 140.9 ROI—outperforming all combinations. Default injection strategy should be: Context Pack → Canonical Memory (conditional) → Session History (multi-turn only).

---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Saraswati]]
- **implements:** [[Context_Pack]]
