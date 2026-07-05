# BUS Runtime: nas

**Status:** optional
**Versioned:** no

---

## Overview

NAS/N100/local network filesystem transport. Optional local network backend.

---

## Configuration

```bash
export YOS_BUS_RUNTIME_ROOT=/mnt/nas/yos-bus-runtime
```

---

## Limitations

- Requires NAS mount and local network access.
- Not accessible outside local network without VPN.
- Not version-controlled.
- Do not depend on NAS as primary transport.
