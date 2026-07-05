---
mp_id: MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE
packet_code: MPM
packet_type: Mega Prompt Manus
title: YOS BUS / MPM Fusion and Direct Runtime Gate
mode: marathon
status: ready_for_execution
target_llm: Manus
source_llm: ChatGPT / Architect & Guardian
created_by: ChatGPT / A&G
created_at: "2026-07-05T00:00:00Z"
executor: Manus
guardian_required: true
auto_run_eligible: true
risk_flags: []
canonical_mp_path: 01_BACKBONE/MPM/04_QUEUE/ready/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE.md
canonical_mpr_path: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT.md
log_pointer_path: 08_LOGS/mpm-reports/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT-POINTER.md
---

# MPM marathon - YOS BUS / MPM Fusion and Direct Runtime Gate

## 0. Mission

Implement the architectural fusion between the legacy `yos-bus` work and the current YOS/MPM runtime.

The objective is to create a clean, canonical, universal BUS module inside the YOS monorepo and define MPM as one specialized BUS stream/domain.

This gate must not run a full MPM transport test yet. It must implement the architecture, protocols, schemas, adapters, runtime registry, and bridge documents so that the next gate can test `MPM -> BUS inbox/mpm -> Manus MP -> MPR`.

## 1. Strategic decision

Adopt this canonical doctrine:

```text
BUS is universal.
MPM is one specialized stream/domain of BUS.
Git is durable memory, audit, and final persistence.
Git is not the fast transport bus.
Direct file runtime is the preferred fast transport layer when available.
```

The previous `yos-bus` repository was correct as a GitHub-native cognitive backbone, but it must now be integrated into the YOS monorepo as:

```text
YOS/01_BACKBONE/BUS/
```

The MPM-specific transport logic recently developed must not become a separate parallel transport system. It must be fused into BUS as the `mpm` stream.

## 2. Canonical YOS topology to preserve

Do not create a new repo.
Do not modify source corpus.
Do not move MPM out of `YOS/01_BACKBONE/MPM/`.
Create or update `YOS/01_BACKBONE/BUS/`.

Canonical active repo:

```text
yj000018/YOS @ main
```

Canonical backbone modules:

```text
01_BACKBONE/
├── BUS/
├── MPM/
├── KAP/
├── ART/
├── CRT/
├── MEMORY/
├── ROUTING/
├── GOVERNANCE/
└── SECURITY/
```

## 3. Legacy BUS source to integrate

The legacy `yos-bus` dump defines:

```text
yos-bus/
├── README.md
├── bus_manifest.yaml
├── agents/
├── docs/
│   ├── foundational-principles/
│   │   └── FP-001-github-native-cognitive-backbone.md
│   └── repository-specification.md
├── protocols/
│   ├── commit-cognitive-convention.md
│   ├── github-actions-reflex-architecture.md
│   └── yos-github-protocol-v0.1.md
├── schemas/
│   ├── artifact_schema.yaml
│   ├── decision_schema.yaml
│   ├── reflex_schema.yaml
│   └── task_schema.yaml
├── inbox/{general,yac,lakshmi,fcs,casatao}/
├── workspace/{general,yac,lakshmi,fcs,casatao}/
├── outbox/general/
└── archive/{general,yac,lakshmi,fcs,casatao}/
```

Integrate the substance, not necessarily the exact old repo layout.

The old BUS concepts to preserve:

```text
- inbox -> workspace -> outbox -> archive
- domains
- schemas
- task/artifact/decision/reflex model
- cognitive commit convention
- GitHub Actions/reflex concept
- agent handoff rules
- BUS as shared operational memory and inter-agent bus
```

Update doctrine:

```text
GitHub-native BUS remains valid as durable/auditable backend.
Direct file runtime is required for fast non-versioned transport.
```

## 4. Target BUS structure

Create:

```text
01_BACKBONE/BUS/
├── README.md
├── bus_manifest.yaml
├── 00_PROTOCOLS/
│   ├── bus-canonical-doctrine.md
│   ├── bus-lifecycle-protocol.md
│   ├── bus-runtime-backend-protocol.md
│   ├── bus-agent-handoff-protocol.md
│   ├── bus-cognitive-commit-convention.md
│   ├── bus-reflex-architecture.md
│   └── bus-mpm-bridge-protocol.md
├── 01_SCHEMAS/
│   ├── bus_packet.schema.json
│   ├── bus_task.schema.json
│   ├── bus_artifact.schema.json
│   ├── bus_decision.schema.json
│   ├── bus_reflex.schema.json
│   └── mpm_bus_packet.schema.json
├── 02_ADAPTERS/
│   ├── direct-file-adapter.md
│   ├── git-adapter.md
│   ├── manus-cloud-adapter.md
│   ├── google-drive-adapter.md
│   ├── nas-adapter.md
│   └── blob-payload-adapter.md
├── 03_TEMPLATES/
│   ├── bus-packet-template.md
│   ├── bus-task-template.md
│   ├── bus-artifact-template.md
│   └── mpm-bus-packet-template.md
├── 04_DOMAINS/
│   ├── README.md
│   ├── general/
│   │   ├── README.md
│   │   └── .gitkeep
│   ├── mpm/
│   │   ├── README.md
│   │   ├── inbox/.gitkeep
│   │   ├── workspace/.gitkeep
│   │   ├── outbox/.gitkeep
│   │   └── archive/.gitkeep
│   ├── kap/
│   │   ├── README.md
│   │   └── .gitkeep
│   ├── casatao/
│   │   ├── README.md
│   │   └── .gitkeep
│   ├── kosmos/
│   │   ├── README.md
│   │   └── .gitkeep
│   └── yworld/
│       ├── README.md
│       └── .gitkeep
├── 05_RUNTIME/
│   ├── runtime-registry.json
│   ├── direct-file/README.md
│   ├── git/README.md
│   ├── manus-cloud/README.md
│   ├── google-drive/README.md
│   ├── nas/README.md
│   └── blob-payload/README.md
├── 06_INDEXES/
│   ├── latest-bus-event.json
│   ├── latest-bus-event.md
│   └── bus-domain-index.md
├── 08_TOOLS/
│   ├── README.md
│   └── bus.py
└── 99_ARCHIVE/
    └── legacy-yos-bus-import-notes.md
```

If a folder already exists, patch it rather than duplicating.

## 5. BUS doctrine to document

In `bus-canonical-doctrine.md`, define:

```text
BUS = universal transport, operational memory, and inter-agent exchange layer.
MPM = specialized orchestration layer for Mega Prompts.
KAP = knowledge assimilation pipeline.
Git = durable/auditable memory and versioning backend.
Direct file runtime = fast non-versioned transport backend.
```

Mandatory principles:

```text
1. BUS is universal.
2. MPM is a BUS domain/stream, not a separate transport architecture.
3. GitHub/Git may be a backend, but Git is not required for fast handoff.
4. Direct file transport must support non-versioned message passing.
5. All accepted/executed durable outputs eventually land in canonical YOS Git.
6. Runtime messages may be temporary and non-versioned.
7. Source of truth depends on lifecycle phase:
   - transport phase: runtime BUS
   - execution phase: MPM/KAP/etc. runtime
   - durable phase: YOS Git canonical artifacts
```

## 6. BUS lifecycle

In `bus-lifecycle-protocol.md`, define universal flow:

```text
inbox -> workspace -> outbox -> archive
```

Semantics:

```text
inbox = new message/task/artifact awaiting claim
workspace = claimed/active work zone
outbox = completed result/report/pointer awaiting consumption
archive = historical/completed/deprecated storage
dead-letter = failed/unprocessable messages, if runtime supports it
ack = acknowledgements, if runtime supports it
locks = claim locks, if runtime supports it
```

Important distinction:

```text
Git-tracked BUS folders define canonical structure and durable records.
Runtime BUS folders may live outside Git and carry ephemeral messages.
```

## 7. Runtime backend architecture

In `runtime-registry.json`, define backend classes:

```json
{
  "$schema": "yos-bus-runtime-registry-v1.0.0",
  "module": "YOS BUS",
  "canonical_path": "01_BACKBONE/BUS/",
  "runtime_root_env": "YOS_BUS_RUNTIME_ROOT",
  "default_domain": "general",
  "domains": ["general", "mpm", "kap", "casatao", "kosmos", "yworld"],
  "backend_priority": ["direct_file", "manus_cloud", "git", "google_drive", "nas", "blob_payload"],
  "backends": {
    "direct_file": {
      "status": "preferred",
      "versioned": false,
      "requires_git_commit_for_transport": false,
      "description": "Fast filesystem-based inbox/workspace/outbox/archive runtime."
    },
    "manus_cloud": {
      "status": "probe_required",
      "versioned": false,
      "requires_git_commit_for_transport": false,
      "description": "Manus online workspace/server-like runtime if stable and addressable."
    },
    "git": {
      "status": "fallback",
      "versioned": true,
      "requires_git_commit_for_transport": true,
      "description": "Durable/auditable fallback transport through canonical YOS Git."
    },
    "google_drive": {
      "status": "fallback",
      "versioned": false,
      "requires_git_commit_for_transport": false,
      "description": "Cloud synced folder transport."
    },
    "nas": {
      "status": "optional",
      "versioned": false,
      "requires_git_commit_for_transport": false,
      "description": "NAS/N100/local network filesystem transport."
    },
    "blob_payload": {
      "status": "experimental_payload_only",
      "versioned": "object",
      "requires_pointer": true,
      "description": "Git blob can store payload content but is not a discoverable queue without a pointer."
    }
  }
}
```

## 8. Direct file runtime

In `05_RUNTIME/direct-file/README.md`, define expected external runtime root:

```text
$YOS_BUS_RUNTIME_ROOT/
├── inbox/{general,mpm,kap,casatao,kosmos,yworld}/
├── workspace/{general,mpm,kap,casatao,kosmos,yworld}/
├── outbox/{general,mpm,kap,casatao,kosmos,yworld}/
├── archive/{general,mpm,kap,casatao,kosmos,yworld}/
├── ack/
├── locks/
└── dead-letter/
```

Rules:

```text
- This runtime root is not Git-tracked by default.
- It is used for ultra-fast handoff.
- File writes are direct filesystem writes.
- Claim should be atomic where possible: rename/move inbox -> workspace.
- Processed messages may later be persisted into YOS Git.
- Runtime root can be Manus cloud workspace, NAS, Google Drive synced folder, Dropbox, iCloud, local disk, mounted volume, etc.
```

## 9. Manus cloud runtime probe

In `05_RUNTIME/manus-cloud/README.md`, document that this backend is promising but requires probing.

Define required probe questions:

```text
1. Does Manus have a stable persistent workspace across sessions?
2. Can Manus read/write a known inbox path without Git?
3. Can ChatGPT or another bridge write into that Manus-accessible path?
4. Can the same conversation or future Manus task access the same path?
5. Is file latency substantially faster than Git commit/push?
6. What are the reliability and access boundaries?
```

Do not assert this backend is production-ready unless tested.

Mark: `status: probe_required`.

## 10. Git backend

In `05_RUNTIME/git/README.md`, define:

```text
Git backend = durable fallback transport.
It is reliable and auditable but slower.
It requires commits for path-addressable file writes.
It may trigger ChatGPT/GitHub action confirmations.
It must not be the preferred fast transport if direct_file or manus_cloud is available.
```

Also define:

```text
Git contents API create/update file = versioned commit.
Git blob = payload object, not discoverable queue.
Blob requires pointer; therefore blob alone is not BUS.
```

## 11. MPM stream/domain

Create `01_BACKBONE/BUS/04_DOMAINS/mpm/README.md`.

Define:

```text
BUS domain: mpm
Purpose: fast and/or durable transport of MPM packets, MPR pointers, execution requests, and status messages.
```

MPM BUS flow:

```text
BUS inbox/mpm
-> BUS workspace/mpm
-> MPM execution runtime
-> MPM MPR/report/ledger/latest pointers
-> BUS outbox/mpm
-> BUS archive/mpm
```

Critical rule:

```text
BUS transports MPM packets.
MPM executes them.
MPM remains the canonical execution ledger/report owner.
```

Do not move canonical MPRs out of `01_BACKBONE/MPM/06_REPORTS/`.
Do not move canonical ledger out of `01_BACKBONE/MPM/05_LEDGER/`.
Do not remove `01_BACKBONE/MPM/04_QUEUE/`.

Priority:

```text
1. BUS runtime inbox/mpm = preferred fast transport if configured.
2. MPM/04_QUEUE/ready = canonical Git fallback queue.
3. Git BUS domain inbox/mpm = durable fallback transport.
```

## 12. MPM adapter patch

Patch/create `01_BACKBONE/MPM/02_ADAPTERS/mpm-bus-adapter.md`.

Define how Manus `MP` should resolve input:

```text
MP command resolution order:

1. If YOS_BUS_RUNTIME_ROOT exists:
   read $YOS_BUS_RUNTIME_ROOT/inbox/mpm/

2. If exactly one valid MPM packet exists:
   claim it by moving to $YOS_BUS_RUNTIME_ROOT/workspace/mpm/
   materialize/record it into MPM execution context
   execute it

3. Else fallback to:
   01_BACKBONE/MPM/04_QUEUE/ready/*.md

4. Else fallback to Git BUS domain:
   01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/

5. If none: report no ready MP.
6. If multiple or risk_flags not empty: show micro-menu/manual selection.
```

Important:

```text
No broad repository search.
No legacy kap-control-plane runtime unless explicit fallback override.
No source corpus scan.
```

## 13. Patch MPM command protocol

Patch:

```text
01_BACKBONE/MPM/00_PROTOCOLS/mpm-manus-fetch-and-run-protocol.md
01_BACKBONE/MPM/00_PROTOCOLS/mpm-command-taxonomy.md
```

Add:

```text
MP now supports BUS-first input resolution.
MPR still uses latest-mpr.json fast path.
MPM/04_QUEUE/ready remains fallback canonical Git queue.
```

Preserve current tested behavior:

```text
ChatGPT MPR:
always read 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
then latest_mpr_path
then A&G review.
```

## 14. BUS tool

Create `01_BACKBONE/BUS/08_TOOLS/bus.py`.

Requirements:

```text
- Python 3 stdlib only
- no external dependencies
- no arbitrary command execution
- safe path handling
- can operate against external runtime root
```

Commands to implement minimally:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py status
python 01_BACKBONE/BUS/08_TOOLS/bus.py domains
python 01_BACKBONE/BUS/08_TOOLS/bus.py inbox --domain mpm
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --dry-run
python 01_BACKBONE/BUS/08_TOOLS/bus.py validate
python 01_BACKBONE/BUS/08_TOOLS/bus.py runtime-paths
```

Optional if safe:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root <path>
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --apply
python 01_BACKBONE/BUS/08_TOOLS/bus.py outbox --domain mpm
```

`claim --dry-run` must only show what would be claimed.
`claim --apply` may move one file from inbox/domain to workspace/domain if exactly one candidate and no ambiguity.
Do not execute MPM content from `bus.py`.

## 15. BUS packet schema

Create `bus_packet.schema.json` with at least:

```json
{
  "$schema": "yos-bus-packet-schema-v1.0.0",
  "required_fields": ["bus_packet_id", "domain", "type", "status", "created_by", "created_at", "payload"],
  "fields": {
    "bus_packet_id": "string",
    "domain": "string",
    "type": "task|artifact|decision|mpm_packet|mpr_pointer|event",
    "status": "inbox|workspace|outbox|archive|failed",
    "created_by": "string",
    "created_at": "iso8601",
    "claimed_by": "string|null",
    "claimed_at": "iso8601|null",
    "payload_kind": "inline|path|url|blob_sha|external_pointer",
    "payload": "object|string",
    "risk_flags": "array",
    "canonicalization_target": "string|null"
  }
}
```

Create `mpm_bus_packet.schema.json` with fields:

```json
{
  "$schema": "yos-mpm-bus-packet-schema-v1.0.0",
  "bus_domain": "mpm",
  "packet_kind": "mpm_packet",
  "mp_id": "string",
  "mode": "sprint|run|marathon",
  "status": "inbox|workspace|outbox|archive|failed",
  "risk_flags": "array",
  "mpm_payload_kind": "inline_markdown|path|url|blob_sha",
  "canonical_mp_path": "string|null",
  "expected_mpr_path": "string|null"
}
```

## 16. Domain mapping

Add BUS domains:

```text
general
mpm
kap
casatao
kosmos
yworld
```

Map old domains:

```text
yac -> yworld or archive as legacy alias
lakshmi -> decide later; for now record as legacy domain alias in import notes
fcs -> archive/legacy alias unless current canonical domain exists
casatao -> casatao
general -> general
```

Do not migrate actual old tasks if none exist.

Create `legacy-yos-bus-import-notes.md` documenting:

```text
- old repo: yj000018/yos-bus
- old HEAD: 245818d
- imported concepts
- domains mapped
- old repo status: legacy/dormant
- no destructive deletion
```

## 17. BUS indexes

Create:

```text
01_BACKBONE/BUS/06_INDEXES/latest-bus-event.json
01_BACKBONE/BUS/06_INDEXES/latest-bus-event.md
01_BACKBONE/BUS/06_INDEXES/bus-domain-index.md
```

Initial latest bus event:

```json
{
  "$schema": "yos-bus-latest-event-v1.0.0",
  "event_id": "BUS-20260705-MPM-FUSION-GATE",
  "event_type": "architecture_integration",
  "domain": "mpm",
  "status": "implemented_awaiting_a_g_review",
  "canonical_report_path": "01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT.md",
  "updated_at": "2026-07-05T00:00:00Z"
}
```

## 18. Validation

Run, if possible:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py validate
python 01_BACKBONE/BUS/08_TOOLS/bus.py status
python 01_BACKBONE/BUS/08_TOOLS/bus.py domains
python 01_BACKBONE/BUS/08_TOOLS/bus.py runtime-paths
python 01_BACKBONE/BUS/08_TOOLS/bus.py inbox --domain mpm
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --dry-run
```

Also run existing MPM validation:

```bash
python 01_BACKBONE/MPM/08_TOOLS/mpm.py validate
python 01_BACKBONE/MPM/08_TOOLS/mpm.py latest-report
python 01_BACKBONE/MPM/08_TOOLS/mpm.py queue
```

Expected:

```text
BUS validate: PASS or PASS_WITH_WARNINGS if runtime root not configured
MPM validate: PASS
MPM latest-report: resolves
MPM queue: no unexpected ready MPs after execution
```

## 19. Required MPR

Create:

```text
01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT.md
```

Create pointer:

```text
08_LOGS/mpm-reports/MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT-POINTER.md
```

Update:

```text
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.md
01_BACKBONE/MPM/05_LEDGER/latest-executed-mp.json
01_BACKBONE/MPM/05_LEDGER/mp-ledger.json
```

Move this MP from `01_BACKBONE/MPM/04_QUEUE/ready/` to `01_BACKBONE/MPM/04_QUEUE/executed/`.

## 20. MPR required fields

The report must include:

```text
STATUS:
MODE:
BRANCH:
COMMIT:
BUS MODULE CREATED: yes/no
BUS CANONICAL PATH:
LEGACY YOS-BUS INTEGRATED: yes/no/partial
BUS DOMAINS CREATED:
MPM DOMAIN CREATED: yes/no
DIRECT FILE RUNTIME DEFINED: yes/no
MANUS CLOUD RUNTIME PROBE DOC CREATED: yes/no
GIT BACKEND DEFINED AS FALLBACK: yes/no
BLOB PAYLOAD STATUS:
BUS TOOL CREATED: yes/no
BUS TOOL PATH:
BUS TOOL COMMANDS IMPLEMENTED:
MPM BUS ADAPTER CREATED/PATCHED: yes/no
MP COMMAND BUS-FIRST POLICY PATCHED: yes/no
MPR FAST PATH PRESERVED: yes/no
SCHEMAS CREATED:
PROTOCOLS CREATED/PATCHED:
VALIDATION COMMANDS RUN:
BUS VALIDATION STATUS:
MPM VALIDATION STATUS:
SOURCE CORPUS TOUCHED: yes/no
EXTERNAL REPOS TOUCHED: yes/no
READY QUEUE CLEAN: yes/no
READY FOR A&G REVIEW: yes/no
```

## 21. Boundaries

```text
Do not touch source corpus.
Do not migrate knowledge content.
Do not create external repos.
Do not delete or archive the old yos-bus remote repo.
Do not activate GitHub Actions yet.
Do not create background automation.
Do not depend on NAS/N100.
Do not claim Manus cloud runtime is working until probed.
Do not implement arbitrary execution from BUS packets.
Do not replace MPM ledger/report canonical paths.
Do not run the next transport test yet.
```

## 22. Commit strategy

Use one commit if possible.

Commit message:

```text
Integrate YOS BUS with MPM stream runtime
```

Use cognitive commit convention if already installed safely, but do not overcomplicate.

## 23. Final response to user

Return only:

```text
STATUS:
MODE:
COMMIT:
BUS MODULE CREATED:
BUS CANONICAL PATH:
MPM DOMAIN CREATED:
DIRECT FILE RUNTIME DEFINED:
MANUS CLOUD RUNTIME DOC:
MPM BUS ADAPTER:
MP COMMAND BUS-FIRST POLICY:
BUS TOOL:
VALIDATION STATUS:
READY QUEUE CLEAN:
MPR PATH:
READY FOR A&G REVIEW:
```

## 24. Stop condition

Stop after implementation, validation, commit, and MPR.

Do not run the BUS/MPM transport test yet.
Do not create the next MP automatically.
