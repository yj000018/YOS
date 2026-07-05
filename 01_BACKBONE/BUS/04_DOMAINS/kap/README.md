# BUS Domain: kap

**Domain:** `kap`
**Purpose:** Knowledge Assimilation Pipeline domain — transport of KAP tasks, source ingestion requests, and knowledge artifacts.
**Status:** active

Use this domain for KAP-related inter-agent messages: source ingestion requests, knowledge extraction tasks, and processed knowledge artifacts.

## Lifecycle Folders

For fast transport, use `$YOS_BUS_RUNTIME_ROOT/inbox/kap/`, etc.
For Git-backed durable transport, commit to `01_BACKBONE/BUS/04_DOMAINS/kap/`.
