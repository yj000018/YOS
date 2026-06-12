---
id: protocol--ylog
type: protocol
name: Y-LOG
slug: ylog
status: active
visibility: public
version: "1.0"
description: Audit trail and operational history module. Receives events from Y-ORC after Mission Pack execution.
question: What happened?
produces: Audit records, operational history
consumes: Mission Pack execution events
equivalent_role: Auditor, Operations Recorder
tags: [core, audit, logging, deterministic, backend]
module_owner: Y-LOG
created_at: "2026-06-12"
---

# Y-LOG — Audit Module

Y-LOG is a system module (deterministic). It records what happened. It does not interpret.

## Responsibilities
- Record all Mission Pack executions (who, what, when, outcome)
- Maintain append-only audit trail
- Expose queryable operational history
- Support compliance, debugging, and retrospective analysis

## Non-Responsibilities
- Does not interpret events (agents)
- Does not store semantic memory (Y-MEM)
- Does not orchestrate (Y-ORC)

## Storage
Append-only table: `yreg_audit_log` in Supabase runtime cache.
Canonical backup: Git-tracked JSONL files in `/logs/`.
