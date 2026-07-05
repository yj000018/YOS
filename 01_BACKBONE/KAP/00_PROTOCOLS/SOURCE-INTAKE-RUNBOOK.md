# SOURCE-INTAKE-RUNBOOK

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Source Channel Intake (L0)

1. Verify the channel is not already in `SOURCE-CHANNEL-REGISTRY.md`.
2. Assign next `CH-XXX` ID.
3. Define default scope (`yos`, `youniverse`, `both`).
4. Define default mode (`AUTO_CRON`, `AUTO_HOOK`, `SEMI_AUTO`, `MANUAL`).
5. Update `SOURCE-CHANNEL-REGISTRY.md`.

## 2. Source Instance Intake (L1)

1. Verify the instance belongs to a registered Channel.
2. Assign next `<CHANNELCODE>-XXX` ID (e.g., `GIT-042`).
3. Verify access credentials exist.
4. Update `SOURCE-INSTANCE-REGISTRY.md`.

## 3. Source Object Intake (L2)

1. A Source Object is a discrete file, page, repo, or session.
2. Run Metadata-Only Pilot (see `METADATA-PILOT-RUNBOOK.md`).
3. Assign next `SO-<CHANNELCODE>-<INSTANCESEQ>-<OBJECTSEQ>` ID.
4. Update `SOURCE-OBJECT-REGISTRY.md`.
5. Update `KAP-SOURCE-MATRIX.md` status to `METADATA_ACQUIRED`.

## 4. Source Fragment Intake (L3)

1. **Prerequisite:** Source Object must be registered.
2. **Prerequisite:** Content Pilot gate must be approved.
3. Extract bounded content snippet (max context window safe).
4. Assign next `SF-<CHANNELCODE>-<INSTANCESEQ>-<OBJECTSEQ>-<FRAGMENTSEQ>` ID.
5. Set `canonical_status` (e.g., `candidate_evidence`, `historical_source`).
6. Update `SOURCE-FRAGMENT-REGISTRY.md`.

## 5. Required Metadata for Intake

- Title / Name
- Source System
- Created / Modified Date
- Observed Date
- Path / URL (mutable, not identity)
- Scope tag

## 6. Blockers & Human Review Triggers

**Block Intake IF:**
- Credentials missing or require exposing secrets.
- Scope is exclusively `youniverse` (deferred to Phase 2).
- Content boundary is unclear (e.g., infinite scroll without pagination).

**Trigger Human Review IF:**
- Source contains potentially sensitive personal/financial data.
- Source Instance mapping is ambiguous (e.g., unknown legacy repo).

## 7. Example Intake Flow

1. User points to new GitHub repo `yj000018/new-app`.
2. Channel `CH-001` (Git) exists.
3. Instance `GIT-042` created in `SOURCE-INSTANCE-REGISTRY.md`.
4. Metadata scan finds `README.md`.
5. Object `SO-GIT-042-0001` created in `SOURCE-OBJECT-REGISTRY.md`.
6. Content extraction authorized.
7. Fragment `SF-GIT-042-0001-001` (Architecture section) created in `SOURCE-FRAGMENT-REGISTRY.md`.
