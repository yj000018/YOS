# BUS Runtime: git

**Status:** fallback
**Versioned:** yes

---

## Definition

Git backend = durable fallback transport.
It is reliable and auditable but slower.
It requires commits for path-addressable file writes.
It may trigger ChatGPT/GitHub action confirmations.
It must not be the preferred fast transport if `direct_file` or `manus_cloud` is available.

---

## Git Contents API

```
Git contents API create/update file = versioned commit.
Git blob = payload object, not discoverable queue.
Blob requires pointer; therefore blob alone is not BUS.
```

---

## Transport Pattern

```
Producer:
  1. Write packet file to 01_BACKBONE/BUS/04_DOMAINS/{domain}/inbox/
  2. git add && git commit && git push

Consumer:
  1. git pull (or GitHub API read)
  2. Read packet from inbox/
  3. Claim: move to workspace/ + commit + push
  4. Execute
  5. Write result to outbox/ + commit + push
```

---

## When to Use

- No `$YOS_BUS_RUNTIME_ROOT` configured.
- Durable audit trail required.
- Message must survive machine failures.
- Receiving agent can only access Git (e.g., ChatGPT via GitHub API).
