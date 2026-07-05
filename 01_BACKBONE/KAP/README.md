# KAP — Knowledge Absorption Pipeline

**System name:** `KAP — Knowledge Absorption Pipeline`
**Module path:** `YOS/01_BACKBONE/KAP/`
**Status:** Scaffolded — active backbone module

---

## Purpose

KAP is the yOS Backbone protocol for absorbing, processing, and canonicalizing knowledge from multiple sources (Obsidian, GDrive, Notion, GitHub, Manus outputs). It provides:

- Architecture-before-absorption doctrine
- Source quarantine and fingerprinting protocols
- Metadata inventory gates
- Bounded extraction gates
- Merge planning gates
- Evolutionary knowledge merge architecture
- Claim, thought line, decision thread, and impasse schemas

## What belongs here

Protocols, schemas, pipelines, gates, registries, run reports, and archive for the KAP system.

## What does NOT belong here

Application code, knowledge content (that goes in `05_KNOWLEDGE_DOMAINS/`), MPM runtime, or project-specific work unrelated to knowledge absorption.

## Key Rule

**KAP is a backbone module, not a project.**

```
Correct:   YOS/01_BACKBONE/KAP/
Incorrect: YOS/07_PROJECTS/KAP/
```

## Bootstrap Origin

KAP was originally developed across two bootstrap repos:
- `kap-control-plane` — control plane, gates, reports
- `yos-cognitive-os` — architecture, schemas, registries

Both remain operational. See `KAP-MODULE-MAP.md`.

## Structure

```
KAP/
├── 00_PROTOCOLS/   ← architecture docs, claim/thought-line/decision models, runbooks
├── 01_SCHEMAS/     ← JSON schemas (source_fragment, claim, thought_line, decision_thread, etc.)
├── 02_PIPELINES/   ← pipeline definitions
├── 03_GATES/       ← gate definitions and protocols
├── 04_REGISTRIES/  ← thought-line, decision-thread, impasse, synthesis-status registries
├── 05_RUNS/        ← execution run history
├── 06_REPORTS/     ← gate reports
└── 99_ARCHIVE/     ← historical KAP runs
```

---

*KAP v1.0.0 — Scaffolded 2026-07-05*
