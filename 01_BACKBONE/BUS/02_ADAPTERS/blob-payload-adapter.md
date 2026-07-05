# BUS Blob Payload Adapter

**Status:** experimental_payload_only
**Versioned:** object-level
**Requires pointer:** yes

---

## Overview

The blob payload adapter uses Git blob objects to store large payload content. It is NOT a transport backend — it is a payload storage mechanism only.

---

## Critical Distinction

```
Git file (path-addressable) = discoverable queue entry = BUS.
Git blob (SHA-only) = payload storage = NOT BUS without a pointer.
Blob alone is not BUS.
```

A Git blob stores content but is only addressable by its SHA. Without a pointer file in the repository, no agent can discover it as a BUS message.

---

## Use Case

Use blob payload when:
- The payload is too large for inline storage.
- The payload must be stored in Git for durability.
- A pointer file will be created to make it discoverable.

---

## Pattern

```
1. Store large content as Git blob: git hash-object -w <file>
2. Record the blob SHA in a pointer file: inbox/domain/pointer-{id}.json
3. Commit the pointer file to YOS Git.
4. Consumer reads pointer, fetches blob by SHA.
```

---

## Limitations

- Requires a pointer file for discoverability.
- Not suitable for fast transport (requires commit).
- Experimental — not validated in production.
- Do not use as primary BUS transport.
