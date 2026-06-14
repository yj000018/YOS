# Y-OS Simple Mental Model

> **One page. Five domains. One loop.**

---

## The Loop

```
CAPTURE → MEMORY → CONTEXT → EXECUTION → REVIEW
```

This is Y-OS. Everything else is optional.

---

## The 5 Domains

```
┌─────────────────────────────────────────────────────────┐
│                      Y-OS CORE                          │
│                                                         │
│  1. CAPTURE          What happened this session?        │
│     session_delta    → structured delta                 │
│                                                         │
│  2. MEMORY           What do we know?                   │
│     artifact_registry → typed, versioned artifacts      │
│     context_cache    → fast retrieval                   │
│                                                         │
│  3. CONTEXT          What does this worker need?        │
│     context_compiler → typed context pack               │
│     ccr_runtime      → mode + provider selection        │
│     payload_builder  → LLM-ready payload                │
│                                                         │
│  4. EXECUTION        Do the work.                       │
│     live_worker      → LLM call                         │
│     validator        → output integrity                 │
│     lakshmi          → governance                       │
│     provider_registry → 3 providers                     │
│                                                         │
│  5. REVIEW           Is Y-OS healthy?                   │
│     (weekly, not daily)                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## What Is Not In This Model

- ODT → Plugin 1 (activate monthly)
- Strategic Engine → Plugin 2 (activate monthly)
- Simulation → Plugin 3 (activate on demand)
- Dashboards → Plugin 4 (activate on demand)

---

## One-Line Summary

> Y-OS captures what happened, remembers what matters, compiles the right context, executes with the right provider, and reviews its own health.

---

## Rebuild in 3 Days

| Day | Modules |
|---|---|
| Day 1 | context_compiler · ccr_runtime · payload_builder · live_worker |
| Day 2 | artifact_registry · session_delta · output_validator · lakshmi |
| Day 3 | context_cache · provider_registry |

**Y-OS is operational in 3 days. Everything else is enhancement.**
