---
mp_id: MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
packet_code: MPM
packet_type: Mega Prompt Manus
title: YOS KAP Knowledge Adapter Census and Probe Gate
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
canonical_mp_path: 01_BACKBONE/MPM/04_QUEUE/ready/MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE.md
canonical_mpr_path: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE-REPORT.md
log_pointer_path: 08_LOGS/mpm-reports/MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE-REPORT-POINTER.md
---

# MPM marathon — YOS KAP Knowledge Adapter Census and Probe Gate

## Mission

Design, inventory, and probe the KAP Knowledge Adapter layer.

KAP must never talk directly to a provider brand or consumer app. KAP talks only to a normalized Knowledge Adapter contract.

Each adapter must be evaluated for:

```text
Historical Backfill
Continuous Capture
Checkpointing
Finalization
Coverage Reporting
```

Do not deploy production automation yet.

## Core doctrine

```text
KAP does not speak to LLMs.
KAP speaks to Knowledge Adapters.
Knowledge Adapters speak to provider APIs, workspaces, repositories, memories, files, and research systems.
```

Classify environments by runtime type:

```text
Class A — API Runtime
Class B — Workspace Runtime
Class C — Consumer UI
```

Class C is descriptive only. Prefer Class A and B.

## Canonical adapter contract

```text
discover_sources()
list_sessions()
retrieve_session()
retrieve_history()
retrieve_delta(cursor)
fetch_attachments()
checkpoint()
detect_finalization()
finalize()
resume(cursor)
report_coverage()
health_check()
```

Each method status:

```text
proven
candidate
unsupported
unknown
not_applicable
```

## Environments to census

Probe and classify at least:

```text
OpenAI API
Anthropic API
Gemini API
xAI API
Perplexity API
Manus workspace/API
Claude Code workspace
Codex workspace/runtime
Gemini CLI workspace
Git repository
Notion
Mem0
Google Drive / local export corpus
```

Consumer UIs may be listed for completeness:

```text
ChatGPT App
Claude.ai
Gemini App
Grok App
Perplexity App
```

but must not be preferred architecture.

## Required adapter taxonomy

```text
Conversation Adapter
Workspace Adapter
Research Adapter
Repository Adapter
Memory Adapter
File Adapter
Evidence Adapter
```

Examples:

```text
OpenAI API Adapter = Conversation Adapter
Claude Code Adapter = Workspace Adapter
Perplexity Adapter = Research + Evidence Adapter
Git Adapter = Repository Adapter
Mem0 Adapter = Memory Adapter
Google Drive Adapter = File Adapter
```

## Required canonical files

Create or patch:

```text
01_BACKBONE/KAP/00_PROTOCOLS/knowledge-adapter-doctrine.md
01_BACKBONE/KAP/00_PROTOCOLS/knowledge-adapter-contract.md
01_BACKBONE/KAP/00_PROTOCOLS/historical-backfill-protocol.md
01_BACKBONE/KAP/00_PROTOCOLS/continuous-capture-protocol.md
01_BACKBONE/KAP/00_PROTOCOLS/checkpoint-and-finalization-protocol.md

01_BACKBONE/KAP/01_SCHEMAS/knowledge_adapter.schema.json
01_BACKBONE/KAP/01_SCHEMAS/kap_session_record.schema.json
01_BACKBONE/KAP/01_SCHEMAS/kap_checkpoint.schema.json
01_BACKBONE/KAP/01_SCHEMAS/kap_coverage_report.schema.json

01_BACKBONE/KAP/04_REGISTRIES/knowledge-adapters.json
01_BACKBONE/KAP/04_REGISTRIES/knowledge-adapter-capability-matrix.json

01_BACKBONE/KAP/06_REPORTS/knowledge-adapter-census.md
01_BACKBONE/KAP/06_REPORTS/knowledge-adapter-probe-results.md
```

If KAP numbering differs, adapt safely and report actual paths.

## Probe strategy

### Phase A — Documentation / capability census

For each environment identify:

```text
available APIs
workspace/file access
history access
streaming or polling
webhooks/events
attachments support
rate limits
auth model
known limitations
```

Use official documentation where possible.

### Phase B — Local/runtime probes

Where accessible in Manus environment, test:

```text
filesystem visibility
persistent paths
task history
CLI availability
API client availability
event hooks
sample delta capture
```

### Phase C — Minimal synthetic tests

Where safe and cheap, test:

```text
historical retrieve of one known record
new session/task capture
checkpoint/resume
finalization signal
coverage report
```

Do not run large migrations or enumerate full histories blindly.

## Required matrix

Create a matrix with:

```text
adapter_id
provider_or_runtime
adapter_type
runtime_class
historical_backfill
continuous_capture
checkpoint
finalization
attachments
resume
coverage_reporting
consumer_app_history_access
provider_api_history_access
workspace_history_access
auth_model
status
confidence
limitations
recommended_role
```

Statuses:

```text
production_ready
production_candidate
candidate
probe_required
unsupported
```

## Required normalized KAP session model

```json
{
  "source_id": "string",
  "adapter_id": "string",
  "session_id": "string",
  "external_session_id": "string|null",
  "status": "active|checkpointed|finalized|archived|unknown",
  "created_at": "iso8601|null",
  "updated_at": "iso8601|null",
  "finalized_at": "iso8601|null",
  "checkpoint_cursor": "string|null",
  "messages": [],
  "attachments": [],
  "coverage": {
    "level": "minimal|partial|broad|near_exhaustive|exhaustive",
    "known_gaps": []
  }
}
```

## Trigger model

Define normalized events:

```text
source_discovered
session_created
session_delta_available
checkpoint_due
session_idle
session_finalized
historical_batch_ready
attachment_available
adapter_error
```

Preferred signal order:

```text
1. native message event
2. native completion/archive event
3. API polling cursor
4. filesystem watcher
5. scheduled delta import
6. manual finalize marker
```

Doctrine:

```text
Best available signal wins.
```

## Finalization model

Allow:

```text
native completion event
explicit SESSION_FINALIZE event
workspace marker
task completion
commit marker
idle timeout
full export import
manual finalize
```

Document risk and confidence for each.

## Historical vs consumer-app distinction

Every adapter must distinguish:

```text
provider_api_history
consumer_app_history
workspace_history
exported_history
```

Never imply API access automatically includes consumer app history.

## Required recommendations

Produce:

```text
best adapters for historical backfill
best adapters for continuous capture
best adapters for workspace execution
best adapters for research/evidence
best fallback adapters
adapters to avoid for production
recommended rollout order
```

## Validation

Validate all created JSON files with `python -m json.tool`.

Run if available:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py validate
python 01_BACKBONE/MPM/08_TOOLS/mpm.py validate
```

## Required MPR

Create:

```text
01_BACKBONE/MPM/06_REPORTS/awaiting-review/MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE-REPORT.md
```

Create pointer and update latest MPR / ledger files.

Move this MP to executed if queued.

## MPR required fields

```text
STATUS:
MODE:
BRANCH:
COMMIT:
ADAPTER_DOCTRINE_CREATED:
ADAPTER_CONTRACT_CREATED:
HISTORICAL_BACKFILL_PROTOCOL_CREATED:
CONTINUOUS_CAPTURE_PROTOCOL_CREATED:
CHECKPOINT_FINALIZATION_PROTOCOL_CREATED:
ADAPTERS_CENSUSED:
ADAPTERS_PROBED:
PRODUCTION_READY_ADAPTERS:
PRODUCTION_CANDIDATE_ADAPTERS:
PROBE_REQUIRED_ADAPTERS:
UNSUPPORTED_ADAPTERS:
NORMALIZED_SESSION_MODEL_CREATED:
TRIGGER_MODEL_CREATED:
FINALIZATION_MODEL_CREATED:
CAPABILITY_MATRIX_CREATED:
REGISTRY_CREATED:
JSON_VALIDATION_STATUS:
BUS_VALIDATION_STATUS:
MPM_VALIDATION_STATUS:
SOURCE_CORPUS_TOUCHED:
EXTERNAL_REPOS_TOUCHED:
READY_FOR_A&G_REVIEW:
```

## Boundaries

```text
Do not deploy production automation.
Do not import full historical corpora.
Do not enumerate thousands of sessions blindly.
Do not expose secrets.
Do not mutate source corpus.
Do not assume consumer app history is accessible through provider APIs.
Do not create next MP.
```

## Commit message

```text
Define and probe KAP Knowledge Adapters
```

## Final response to user

Return only:

```text
STATUS:
COMMIT:
ADAPTERS_CENSUSED:
ADAPTERS_PROBED:
PRODUCTION_READY_ADAPTERS:
PRODUCTION_CANDIDATE_ADAPTERS:
PROBE_REQUIRED_ADAPTERS:
CAPABILITY_MATRIX_CREATED:
NORMALIZED_SESSION_MODEL_CREATED:
MPR PATH:
READY FOR A&G REVIEW:
```
