# yOS MPM — Mega Prompt Manager

**System name:** `yOS MPM — Mega Prompt Manager`
**Module path:** `YOS/01_BACKBONE/MPM/`
**Status:** Migrated from bootstrap — active

---

## Purpose

MPM is the yOS Backbone protocol for inter-LLM orchestration. It provides:

- Mega Prompt packet transport between LLMs (Manus, ChatGPT, Claude, Gemini, Perplexity)
- Execution queue management (drafts → ready → running → executed → reviewed)
- Architect & Guardian review workflow
- Adapter protocols for each LLM
- Execution ledger (JSON-first, MD as generated view)

## What belongs here

Protocols, schemas, adapters, templates, queue, ledger, reports, and archive for the MPM system.

## What does NOT belong here

KAP-specific run history, application code, knowledge content, or project-specific gates.

## Bootstrap Origin

MPM was originally developed in `kap-control-plane` (private bootstrap repo). Universal runtime assets have been copied here. The bootstrap repo remains operational. See `BOOTSTRAP-ORIGIN.md`.

## Canonical Command

```
MP                          → auto-run next safe ready MP
MP sprint: <mission>        → fast bounded task
MP run: <mission>           → controlled standard task
MP marathon: <mission>      → long multi-worker task
MP queue                    → show queue
MP status                   → show ledger summary
```

## Structure

```
MPM/
├── 00_PROTOCOLS/   ← status lifecycle, command taxonomy, safety, collision rules, adapters protocols
├── 01_SCHEMAS/     ← frontmatter schema (JSON), ledger schema (JSON)
├── 02_ADAPTERS/    ← per-LLM adapters (Manus, ChatGPT, Claude, Gemini, Perplexity, Generic)
├── 03_TEMPLATES/   ← sprint, run, marathon templates
├── 04_QUEUE/       ← drafts / ready / running / executed / reviewed / blocked / superseded
├── 05_LEDGER/      ← execution ledger JSON (source of truth)
├── 06_REPORTS/     ← awaiting-review / reviewed / archived
└── 99_ARCHIVE/     ← historical MPMs
```

---

*yOS MPM v1.0.0 — Migrated 2026-07-05*
