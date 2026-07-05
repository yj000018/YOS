# BUS Git Adapter

**Status:** fallback
**Versioned:** yes
**Requires Git commit for transport:** yes

---

## Overview

The Git adapter uses the canonical YOS Git repository (`yj000018/YOS`) as the transport backend. It is reliable and auditable but slower than direct file transport due to the commit/push cycle.

---

## When to Use

Use the Git adapter when:
- No `$YOS_BUS_RUNTIME_ROOT` is configured.
- Durable audit trail is required.
- The message must survive machine failures.
- The receiving agent can only access Git (e.g., ChatGPT via GitHub API).

---

## Transport Mechanism

```
Producer writes file to: 01_BACKBONE/BUS/04_DOMAINS/{domain}/inbox/
Producer commits and pushes to: yj000018/YOS @ main
Consumer reads via: GitHub API or local git pull
Consumer claims by: moving file to workspace/ and committing
```

---

## Limitations

- Requires a commit and push for each message.
- Slower than direct file transport.
- May trigger GitHub Actions if configured.
- Git blob alone is not BUS — requires a pointer file to be discoverable.

---

## Git Blob vs. Git File

```
Git file (path-addressable) = discoverable queue entry.
Git blob (SHA-only) = payload storage, NOT discoverable without a pointer.
Blob alone is not BUS.
```

---

## Durable Canonicalization

All BUS messages that need to be durably preserved must eventually be committed to YOS Git. The Git adapter handles this automatically. For direct_file transport, the agent must explicitly commit the artifact after execution.
