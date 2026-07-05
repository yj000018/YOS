# BUS Runtime: google-drive

**Status:** fallback
**Versioned:** no

---

## Overview

Cloud synced folder transport. Use when `direct_file` is not available and multiple machines need shared BUS access.

---

## Configuration

```bash
export YOS_BUS_RUNTIME_ROOT="/path/to/google-drive-sync/yos-bus-runtime"
```

---

## Limitations

- Sync latency: not real-time (seconds to minutes).
- Requires Google Drive for Desktop or equivalent.
- Not accessible to agents without Google Drive access.
- Not version-controlled.
