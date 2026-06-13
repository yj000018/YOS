---
id: protocol--ylog
title: protocol--ylog
type: protocol
status: active
date: '2026-06-13'
version: '1.0'
owner: Manus Y-OS
tags:
- core
- audit
- logging
- deterministic
- backend
source_branch: y-os-doctrine
canonical: true
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
