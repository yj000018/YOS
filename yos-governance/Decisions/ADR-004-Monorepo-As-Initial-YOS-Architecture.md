# ADR-004: Monorepo as Initial YOS Architecture

**Date:** 2026-06-03  
**Status:** Accepted  
**Decided by:** YOS Governance

---

## Context

YOS has grown into 31 fragmented repositories. Navigation, cross-linking, and governance are difficult across separate repos.

## Decision

Consolidate into a single monorepo: `yj000018/YOS`.

Structure:
```
YOS/
├── yos-governance/
├── yos-vault/
├── yos-agents/
├── yos-automations/
├── yos-apps/
├── yos-related/
└── archive/
```

## Consequences

- All active YOS modules live under one roof
- Cross-module references become simple relative paths
- Git history is preserved via subtree or copy with provenance notes
- Original repos are NOT deleted — they remain as source of record
- Future: may split back into packages if monorepo grows unwieldy
