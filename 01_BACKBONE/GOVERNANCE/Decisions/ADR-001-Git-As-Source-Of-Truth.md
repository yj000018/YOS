# ADR-001: Git as Source of Truth

**Date:** 2026-06-03  
**Status:** Accepted  
**Decided by:** YOS Governance

---

## Context

YOS needs a single, durable, version-controlled source of truth for all content — code, agents, decisions, automations, and vault metadata.

## Decision

Git (GitHub: `yj000018/YOS`) is the canonical source of truth for YOS.

All content must ultimately live in Git. Human editing happens in Obsidian, but syncs to Git.

## Consequences

- All agents must read from and write to Git
- Obsidian vault (Y-WORLD) is a human-readable layer on top of Git content
- No content is authoritative unless committed and pushed
- Conflict resolution: Git history wins
