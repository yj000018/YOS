# ADR-005: Manus as Primary, Claude as Fallback Execution Operator

**Date:** 2026-06-03  
**Status:** Accepted  
**Decided by:** YOS Governance

---

## Context

YOS requires a reliable execution operator for agentic tasks. Two capable agents are available: Manus and Claude.

## Decision

| Agent | Role | Condition |
|-------|------|-----------|
| ChatGPT | Architecture / reasoning / specifications | Always |
| Manus | Primary execution operator | When credits are available |
| Claude | Fallback execution operator | When Manus credits are exhausted or unavailable |

## Consequences

- Manus is preferred for execution tasks when available
- Claude activates automatically as fallback — no manual intervention needed
- Both agents must follow identical operating rules (local-first, git-as-truth)
- Handoffs between agents are documented in `yos-governance/Decisions/`
- Agent role assignments are stored in `yos-governance/Manifest/policy-manifest.json`
