# BUS Runtime: blob-payload

**Status:** experimental_payload_only
**Versioned:** object-level
**Requires pointer:** yes

---

## Overview

Git blob payload storage. NOT a transport backend — payload storage only.

```
Git blob alone is not BUS.
Blob requires a pointer file to be discoverable.
```

---

## Pattern

```
1. Store large content as Git blob: git hash-object -w <file>
2. Record blob SHA in pointer file: inbox/domain/pointer-{id}.json
3. Commit pointer file to YOS Git.
4. Consumer reads pointer, fetches blob by SHA.
```

---

## Limitations

- Requires pointer for discoverability.
- Not suitable for fast transport.
- Experimental — not validated in production.
