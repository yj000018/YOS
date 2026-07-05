---
mp_id: MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE
packet_code: MPM
packet_type: Mega Prompt Manus
title: YOS BUS First/Last Mile Integration Gate
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
canonical_mp_path: 01_BACKBONE/MPM/04_QUEUE/ready/MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE.md
canonical_mpr_path: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT.md
log_pointer_path: 08_LOGS/mpm-reports/MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT-POINTER.md
---

# MPM marathon - YOS BUS First/Last Mile Integration Gate

## 0. Mission

Implement the missing first-mile and last-mile integration layer around the now-validated YOS BUS direct-file runtime.

Previous gates validated:

```text
BUS universal architecture = accepted
BUS mpm stream = accepted
Git BUS fallback = operational
Direct-file runtime = operational
Direct-file claim latency = ~43ms
Runtime packet not committed to Git = validated
```

Remaining problem:

```text
ChatGPT -> BUS still requires manual download/upload.
MPR -> ChatGPT is conceptually fast-path but needs a clean last-mile contract.
```

Goal:

```text
Create a clean, backend-agnostic BUS Entry Adapter and BUS Report Adapter design + implementation scaffold so the workflow can become:

ChatGPT: MPM
-> BUS inbox/mpm via selected entry backend
Manus: MP
-> BUS-first execution
ChatGPT: MPR
-> latest report fast-path / outbox report pointer

without Git being used as the transport bus except as fallback.
```

This is an integration/scaffold marathon, not a full cloud deployment. Do not activate background automation.

## 1. Canonical architecture

Preserve:

```text
Repo: yj000018/YOS
Branch: main
BUS canonical path: 01_BACKBONE/BUS/
MPM canonical path: 01_BACKBONE/MPM/
Git = durable memory / audit / final persistence
BUS Runtime Backend = transport abstraction
direct_file = validated fast local/runtime backend
git = fallback transport only
```

Do not create a new repo.
Do not move MPM out of `01_BACKBONE/MPM/`.
Do not move BUS out of `01_BACKBONE/BUS/`.

## 2. Core design decision

Implement this doctrine:

```text
BUS.write(packet) is the canonical first-mile abstraction.
BUS.read_latest_report() is the canonical last-mile abstraction.
```

Backend-specific details must be behind adapters:

```text
direct_file
manus_workspace
google_drive
nas
git
blob_payload
manual_upload
```

Do not hardcode one environment path as universal.

Use:

```text
YOS_BUS_RUNTIME_ROOT
YOS_BUS_ENTRY_BACKEND
YOS_BUS_REPORT_BACKEND
```

## 3. First-mile problem to solve

Current unwanted workflow:

```text
ChatGPT creates file
user downloads
user uploads to Manus
Manus runs MP
```

Target workflows:

### Preferred future

```text
ChatGPT/MPM
-> BUS entry backend
-> BUS inbox/mpm
-> Manus MP
```

### Current safe fallback

```text
ChatGPT creates downloadable packet
-> user uploads to Manus
-> Manus uses bus.py ingest/enqueue to place it into BUS runtime inbox/mpm
-> MP executes
```

### Git fallback

```text
ChatGPT writes Git BUS inbox/mpm or MPM/ready
-> Manus MP
```

Git fallback remains valid but must not be preferred.

## 4. Last-mile problem to solve

Current working behavior:

```text
ChatGPT MPR
-> read 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
-> read latest_mpr_path
-> A&G review
```

Target:

```text
MPR
-> latest-mpr.json fast path
-> optional BUS outbox/mpm latest-report pointer
-> A&G review
```

The last-mile must remain path-fixed and non-search based.

## 5. Required files to create/patch

Create or patch under BUS:

```text
01_BACKBONE/BUS/00_PROTOCOLS/bus-first-last-mile-protocol.md
01_BACKBONE/BUS/00_PROTOCOLS/bus-entry-adapter-protocol.md
01_BACKBONE/BUS/00_PROTOCOLS/bus-report-adapter-protocol.md

01_BACKBONE/BUS/02_ADAPTERS/manual-upload-entry-adapter.md
01_BACKBONE/BUS/02_ADAPTERS/direct-file-entry-adapter.md
01_BACKBONE/BUS/02_ADAPTERS/git-entry-adapter.md
01_BACKBONE/BUS/02_ADAPTERS/google-drive-entry-adapter.md
01_BACKBONE/BUS/02_ADAPTERS/manus-workspace-entry-adapter.md
01_BACKBONE/BUS/02_ADAPTERS/report-fast-path-adapter.md

01_BACKBONE/BUS/03_TEMPLATES/mpm-entry-packet-template.md
01_BACKBONE/BUS/03_TEMPLATES/mpr-report-pointer-template.md

01_BACKBONE/BUS/05_RUNTIME/entry-backend-registry.json
01_BACKBONE/BUS/05_RUNTIME/report-backend-registry.json

01_BACKBONE/BUS/06_INDEXES/latest-entry-event.json
01_BACKBONE/BUS/06_INDEXES/latest-report-event.json
```

Patch:

```text
01_BACKBONE/BUS/08_TOOLS/bus.py
01_BACKBONE/BUS/08_TOOLS/README.md
01_BACKBONE/MPM/02_ADAPTERS/mpm-bus-adapter.md
01_BACKBONE/MPM/00_PROTOCOLS/mpm-command-taxonomy.md
01_BACKBONE/MPM/00_PROTOCOLS/mpm-manus-fetch-and-run-protocol.md
```

## 6. bus.py required new commands

Patch `bus.py` to support:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py write --domain mpm --file <path> --backend direct_file
python 01_BACKBONE/BUS/08_TOOLS/bus.py ingest --domain mpm --file <path>
python 01_BACKBONE/BUS/08_TOOLS/bus.py latest-report
python 01_BACKBONE/BUS/08_TOOLS/bus.py report-pointer --domain mpm
python 01_BACKBONE/BUS/08_TOOLS/bus.py entry-backends
python 01_BACKBONE/BUS/08_TOOLS/bus.py report-backends
```

If exact command names need adjustment, keep behavior equivalent and document final names.

### Command semantics

#### ingest

```text
ingest = accept a local file and place it into selected BUS inbox/domain.
```

Use case:

```text
User uploads MPM file to Manus.
Manus runs bus.py ingest --domain mpm --file <uploaded_file>.
The packet lands in BUS runtime inbox/mpm or Git fallback inbox/mpm depending config.
```

#### write

```text
write = programmatic first-mile write into selected BUS backend.
```

It should support at least direct_file and git fallback if already practical.

#### latest-report

```text
latest-report = print latest MPR pointer using canonical MPM latest-mpr.json.
```

It must read:

```text
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
```

No search.

#### report-pointer

```text
report-pointer --domain mpm = emit BUS-friendly report pointer to latest MPR.
```

## 7. Backend registries

Create `entry-backend-registry.json`:

```json
{
  "$schema": "yos-bus-entry-backend-registry-v1.0.0",
  "canonical_module": "YOS BUS",
  "entry_abstraction": "BUS.write(packet)",
  "env": {
    "backend": "YOS_BUS_ENTRY_BACKEND",
    "runtime_root": "YOS_BUS_RUNTIME_ROOT"
  },
  "preferred_order": [
    "direct_file",
    "manus_workspace",
    "google_drive",
    "nas",
    "git",
    "manual_upload",
    "blob_payload"
  ],
  "backends": {
    "direct_file": {
      "status": "validated_local_runtime",
      "versioned": false,
      "transport_commit_required": false,
      "notes": "Validated in direct-file runtime probe. Requires accessible runtime root."
    },
    "manus_workspace": {
      "status": "probe_required",
      "versioned": false,
      "transport_commit_required": false,
      "notes": "Potential online Manus server/workspace transport. Must be probed."
    },
    "google_drive": {
      "status": "candidate",
      "versioned": false,
      "transport_commit_required": false,
      "notes": "Cloud folder transport candidate."
    },
    "nas": {
      "status": "optional",
      "versioned": false,
      "transport_commit_required": false,
      "notes": "Works if NAS/N100 is online; must not be mandatory."
    },
    "git": {
      "status": "fallback",
      "versioned": true,
      "transport_commit_required": true,
      "notes": "Reliable but slow and may trigger ChatGPT/GitHub confirmations."
    },
    "manual_upload": {
      "status": "fallback",
      "versioned": false,
      "transport_commit_required": false,
      "notes": "Human uploads packet to Manus; bus.py ingest places it into BUS."
    },
    "blob_payload": {
      "status": "experimental_payload_only",
      "requires_pointer": true,
      "notes": "Blob can hold payload but is not a discoverable queue by itself."
    }
  }
}
```

Create `report-backend-registry.json`:

```json
{
  "$schema": "yos-bus-report-backend-registry-v1.0.0",
  "canonical_last_mile": "MPR fast path",
  "fixed_latest_mpr_path": "01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json",
  "preferred_order": [
    "latest_mpr_json",
    "bus_outbox_pointer",
    "git_fetch_direct",
    "manual_paste"
  ],
  "rules": [
    "No search by default.",
    "Read latest-mpr.json first.",
    "Then read latest_mpr_path.",
    "Only search if latest pointer is missing or corrupt."
  ]
}
```

## 8. MPM command doctrine patch

Patch MPM docs with explicit commands:

### ChatGPT side

```text
MPM = generate next MP packet.
MPR = read fixed latest-mpr.json fast path and A&G review.
```

### Manus side

```text
MP = resolve BUS-first:
1. YOS_BUS_RUNTIME_ROOT/inbox/mpm
2. MPM/04_QUEUE/ready
3. BUS Git domain inbox/mpm
4. micro-menu if ambiguous
```

### Current manual bridge fallback

```text
If MP is attached/uploaded manually, Manus should ingest it into BUS first when possible:
bus.py ingest --domain mpm --file <uploaded_mpm_file>
then continue with MP execution.
```

## 9. Direct-file first-mile self-test

If possible, perform a local self-test without needing ChatGPT direct write.

Create a minimal synthetic packet file in a temp location:

```text
/tmp/yos-bus-entry-selftest/MPM-BUS-ENTRY-SELFTEST.md
```

Then run:

```bash
export YOS_BUS_RUNTIME_ROOT=/tmp/yos-bus-runtime
python 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root "$YOS_BUS_RUNTIME_ROOT"
python 01_BACKBONE/BUS/08_TOOLS/bus.py ingest --domain mpm --file /tmp/yos-bus-entry-selftest/MPM-BUS-ENTRY-SELFTEST.md
python 01_BACKBONE/BUS/08_TOOLS/bus.py inbox --domain mpm
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --dry-run
```

Expected:

```text
ingest: packet copied/moved into direct-file runtime inbox/mpm
inbox: detects packet
claim dry-run: identifies packet
```

Then clean up the synthetic packet to avoid stale active runtime state.

Do not commit runtime packet.

## 10. Last-mile self-test

Run:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py latest-report
python 01_BACKBONE/BUS/08_TOOLS/bus.py report-pointer --domain mpm
```

Expected:

```text
latest-report reads fixed latest-mpr.json.
report-pointer emits domain mpm report pointer without searching.
```

## 11. Validation commands

Run:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py validate
python 01_BACKBONE/BUS/08_TOOLS/bus.py status
python 01_BACKBONE/BUS/08_TOOLS/bus.py entry-backends
python 01_BACKBONE/BUS/08_TOOLS/bus.py report-backends
python 01_BACKBONE/BUS/08_TOOLS/bus.py latest-report
python 01_BACKBONE/MPM/08_TOOLS/mpm.py validate
python 01_BACKBONE/MPM/08_TOOLS/mpm.py latest-report
python 01_BACKBONE/MPM/08_TOOLS/mpm.py queue
```

Expected:

```text
BUS validate: PASS or PASS_WITH_WARNINGS only if runtime root not set for non-test context
MPM validate: PASS or PASS_WITH_WARNINGS with non-blocking documented warning
latest-report: resolves
queue: clean after execution
```

## 12. Required MPR

Create:

```text
01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT.md
```

Create pointer:

```text
08_LOGS/mpm-reports/MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT-POINTER.md
```

Update:

```text
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.md
01_BACKBONE/MPM/05_LEDGER/latest-executed-mp.json
01_BACKBONE/MPM/05_LEDGER/mp-ledger.json
01_BACKBONE/BUS/06_INDEXES/latest-bus-event.json
01_BACKBONE/BUS/06_INDEXES/latest-bus-event.md
01_BACKBONE/BUS/06_INDEXES/latest-entry-event.json
01_BACKBONE/BUS/06_INDEXES/latest-report-event.json
```

Move this MP from:

```text
01_BACKBONE/MPM/04_QUEUE/ready/
```

to:

```text
01_BACKBONE/MPM/04_QUEUE/executed/
```

## 13. MPR required fields

The report must include:

```text
STATUS:
MODE:
BRANCH:
COMMIT:
FIRST_MILE_PROTOCOL_CREATED: yes/no
LAST_MILE_PROTOCOL_CREATED: yes/no
ENTRY_BACKEND_REGISTRY_CREATED: yes/no
REPORT_BACKEND_REGISTRY_CREATED: yes/no
BUS_INGEST_COMMAND_IMPLEMENTED: yes/no
BUS_WRITE_COMMAND_IMPLEMENTED: yes/no/partial
BUS_LATEST_REPORT_COMMAND_IMPLEMENTED: yes/no
BUS_REPORT_POINTER_COMMAND_IMPLEMENTED: yes/no
MANUAL_UPLOAD_FALLBACK_DEFINED: yes/no
DIRECT_FILE_ENTRY_SELFTEST_STATUS:
LAST_MILE_SELFTEST_STATUS:
MPM_COMMAND_DOCTRINE_PATCHED: yes/no
MPR_FIXED_PATH_DOCTRINE_CONFIRMED: yes/no
RUNTIME_PACKET_COMMITTED_TO_GIT: yes/no
BUS_VALIDATION_STATUS:
MPM_VALIDATION_STATUS:
READY_QUEUE_CLEAN: yes/no
SOURCE_CORPUS_TOUCHED: yes/no
EXTERNAL_REPOS_TOUCHED: yes/no
READY_FOR_A&G_REVIEW: yes/no
```

## 14. Boundaries

```text
Do not touch source corpus.
Do not migrate knowledge content.
Do not create external repos.
Do not activate GitHub Actions.
Do not create background automation.
Do not depend on NAS/N100.
Do not claim Manus cloud write access works unless actually probed.
Do not claim ChatGPT can directly write to runtime unless implemented.
Do not execute arbitrary BUS packet content.
Do not commit runtime transport packet files.
Do not create next MP automatically.
```

## 15. Commit strategy

Use one commit if possible.

Commit message:

```text
Integrate YOS BUS first and last mile adapters
```

## 16. Final response to user

Return only:

```text
STATUS:
MODE:
COMMIT:
FIRST_MILE_PROTOCOL:
LAST_MILE_PROTOCOL:
BUS_INGEST_COMMAND:
BUS_WRITE_COMMAND:
BUS_LATEST_REPORT_COMMAND:
DIRECT_FILE_ENTRY_SELFTEST:
LAST_MILE_SELFTEST:
MPR_FIXED_PATH:
VALIDATION STATUS:
READY QUEUE CLEAN:
MPR PATH:
READY FOR A&G REVIEW:
```

## 17. Stop condition

Stop after implementation, self-tests, cleanup, commit, and MPR.

Do not start full automation.
Do not start Manus cloud API/MCP probe unless explicitly requested in a separate gate.
