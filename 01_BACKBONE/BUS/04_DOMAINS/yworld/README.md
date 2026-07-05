# BUS Domain: yworld

**Domain:** `yworld`
**Purpose:** yWorld project domain — transport of yWorld-related tasks, artifacts, and decisions.
**Status:** active
**Legacy:** Absorbs `yac` domain from `yj000018/yos-bus` (yac = legacy alias for yworld).

Use this domain for all yWorld project inter-agent messages.

## Legacy Note

The `yac` domain from the old `yos-bus` repository is mapped to `yworld`. If you encounter references to `yac`, treat them as `yworld`.

## Lifecycle Folders

For fast transport, use `$YOS_BUS_RUNTIME_ROOT/inbox/yworld/`, etc.
For Git-backed durable transport, commit to `01_BACKBONE/BUS/04_DOMAINS/yworld/`.
