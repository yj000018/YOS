# BUS NAS Adapter

**Status:** optional
**Versioned:** no
**Requires Git commit for transport:** no

---

## Overview

The NAS adapter uses a NAS (Network Attached Storage) or N100/local network filesystem as the transport backend. It is an optional local network transport.

---

## Configuration

Set the runtime root to a NAS mount path:

```bash
export YOS_BUS_RUNTIME_ROOT=/mnt/nas/yos-bus-runtime
```

---

## Use Case

Use when:
- A NAS is available on the local network.
- Multiple machines on the same network need shared BUS access.
- Low latency local network transport is preferred over cloud sync.

---

## Limitations

- Requires NAS to be mounted and accessible.
- Not accessible outside the local network without VPN.
- Not version-controlled.
- Reliability depends on NAS uptime.

---

## Note

Do not depend on NAS/N100 as the primary transport. Use `direct_file` on local disk as primary and NAS as an optional shared transport.
