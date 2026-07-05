# BUS Google Drive Adapter

**Status:** fallback
**Versioned:** no
**Requires Git commit for transport:** no

---

## Overview

The Google Drive adapter uses a synced Google Drive folder as the transport backend. It is a cloud-synced fallback when direct file transport is not available.

---

## Configuration

Set the runtime root to a Google Drive synced folder path:

```bash
export YOS_BUS_RUNTIME_ROOT=/path/to/google-drive-sync/yos-bus-runtime
```

On macOS with Google Drive for Desktop:
```bash
export YOS_BUS_RUNTIME_ROOT="/Users/yannick/Google Drive/My Drive/yos-bus-runtime"
```

---

## Advantages

- Cloud-synced: accessible from multiple machines.
- No Git commit required for transport.
- Reasonably fast sync (seconds to minutes).

---

## Limitations

- Sync latency: not real-time, depends on Google Drive sync speed.
- Requires Google Drive for Desktop or equivalent sync client.
- Not accessible to agents without Google Drive access.
- Not version-controlled (no history unless explicitly archived to Git).

---

## Use Case

Use when:
- `$YOS_BUS_RUNTIME_ROOT` direct file is not available.
- Multiple machines need shared BUS access.
- Git transport is too slow or unavailable.
