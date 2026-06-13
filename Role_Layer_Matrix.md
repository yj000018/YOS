---
id: yos-role-layer-matrix
title: Role Layer Matrix
type: unknown
status: OFFICIAL
date: '2026-06-12'
owner: Manus Y-OS
tags:
- '#memory'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Role-to-Layer Matrix

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Mapping Roles to Architectural Layers

| Role | Primary Layer | Secondary Layer | Focus |
| :--- | :--- | :--- | :--- |
| **CEO (Yannick)** | Executive Layer | - | Intent & Final Authority |
| **CSO (Krishna)** | Executive Layer | Artifact Layer | Strategy & Direction |
| **COO (Ganesha)** | Execution Layer | Capability Layer | Orchestration & Delivery |
| **Architect (Brahma)** | Design Layer | Capability Layer | System Design |
| **Developer (Hanuman)** | Build Layer | Capability Layer | Implementation |
| **CODO (Saraswati)** | Evolution Layer | Memory Layer | Governance & Learning |
| **ECO (Lakshmi)** | Visibility Layer | Artifact Layer | Observation & Reporting |

## The Capability Layer Distinction
Roles like Ganesha, Brahma, and Hanuman operate *within* the Capability Layer. They use underlying capabilities (LLMs, Python, shell scripts) to perform their work. If an underlying capability changes (e.g., upgrading from GPT-4 to Claude 3.5), the Role remains unchanged.
