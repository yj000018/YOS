# BUS Runtime: manus-cloud

**Status:** probe_required
**Versioned:** no

---

## Overview

This backend is promising but requires probing before production use.

Do not assert this backend is production-ready unless tested.

---

## Required Probe Questions

1. Does Manus have a stable persistent workspace across sessions?
2. Can Manus read/write a known inbox path without Git?
3. Can ChatGPT or another bridge write into that Manus-accessible path?
4. Can the same conversation or future Manus task access the same path?
5. Is file latency substantially faster than Git commit/push?
6. What are the reliability and access boundaries?

---

## Current Status

`status: probe_required`

This backend will be activated only after a dedicated probe gate confirms all questions above.

---

## Activation Gate

To activate, create and execute:

```
MPM-{DATE}-YOS-BUS-MANUS-CLOUD-PROBE-GATE
```
