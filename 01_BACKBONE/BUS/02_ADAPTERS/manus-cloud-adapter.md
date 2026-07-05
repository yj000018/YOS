# BUS Manus Cloud Adapter

**Status:** probe_required
**Versioned:** no
**Requires Git commit for transport:** no

---

## Overview

The Manus cloud adapter would use Manus's persistent online workspace as a fast, non-versioned transport backend. This backend is promising but requires probing before production use.

---

## Probe Questions

Before marking this adapter as production-ready, the following must be answered:

1. Does Manus have a stable persistent workspace across sessions?
2. Can Manus read/write a known inbox path without Git?
3. Can ChatGPT or another bridge write into that Manus-accessible path?
4. Can the same conversation or future Manus task access the same path?
5. Is file latency substantially faster than Git commit/push?
6. What are the reliability and access boundaries?

---

## Current Status

**Do not assert this backend is production-ready until probed.**

Mark: `status: probe_required`.

---

## Activation Gate

To activate this adapter, create and execute:

```
MPM-{DATE}-YOS-BUS-MANUS-CLOUD-PROBE-GATE
```

This gate must:
- Answer all probe questions above.
- Validate read/write access from both Manus and ChatGPT.
- Measure latency vs. Git adapter.
- Get A&G approval before marking as active.
