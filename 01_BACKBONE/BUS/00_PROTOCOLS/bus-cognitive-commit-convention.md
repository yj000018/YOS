# BUS Cognitive Commit Convention

**Version:** 1.0.0
**Status:** active
**Integrated from:** `yj000018/yos-bus` commit-cognitive-convention.md

---

## Purpose

Defines the Git commit message convention for all BUS-related commits in the YOS monorepo. Commits are cognitive artifacts — they must be readable by both humans and agents.

---

## Format

```
<verb> <module> <object> [<context>]
```

### Verbs

| Verb | Meaning |
|---|---|
| `Integrate` | Merge or fuse external content into YOS |
| `Create` | New file or module |
| `Patch` | Small targeted fix or update |
| `Update` | Broader update to existing content |
| `Archive` | Move to archive state |
| `Execute` | Run an MP or gate |
| `Validate` | Validation pass |
| `Refactor` | Structural change without functional change |

### Modules

`BUS`, `MPM`, `KAP`, `ART`, `CRT`, `MEMORY`, `ROUTING`, `GOVERNANCE`, `SECURITY`

### Examples

```
Integrate YOS BUS with MPM stream runtime
Create BUS domain mpm inbox/workspace/outbox/archive
Patch MPM fetch-and-run protocol with BUS-first input resolution
Update BUS runtime registry with direct_file preferred status
Execute MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE
```

---

## Rules

1. **One commit per MP execution.** Batch all writes from a single MP into one commit.
2. **Commit message must be human-readable.** No cryptic codes.
3. **Commit message must be agent-parseable.** Follow the verb/module/object pattern.
4. **Do not commit partial work.** A commit represents a complete, validated state.
5. **Commit hash must be patched into MPR and ledger** after the commit is made.

---

## Cognitive Commit Body (optional)

For marathon MPs, include a body:

```
<blank line>
MP: MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE
Mode: marathon
Workers: A B C D E + Coordinator
Files created: N
Files patched: N
MPR: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT.md
```

---

## Legacy Note

This convention integrates and supersedes `commit-cognitive-convention.md` from `yj000018/yos-bus`. The core verb/module/object pattern is preserved and extended.
