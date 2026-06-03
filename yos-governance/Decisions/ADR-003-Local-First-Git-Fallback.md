# ADR-003: Local-First, Git Fallback Routing

**Date:** 2026-06-03  
**Status:** Accepted  
**Decided by:** YOS Governance

---

## Context

Agents (especially Claude) operate in two modes depending on Mac availability.

## Decision

Routing principle:

| Condition | Mode |
|-----------|------|
| Mac open / local repo reachable | Local-first: pull → edit → commit → push |
| Mac closed / local repo unavailable | GitHub-first: operate via GitHub API |

## Consequences

- Always `git pull --rebase` before local edits
- Always commit + push after local edits
- GitHub API is universal fallback — no local dependency required
- This allows agents to operate 24/7 regardless of Mac state
