# Manus API Capability Matrix

> **Source:** `openapi_v2.json` + official Manus API docs (`skills/manus-api/docs/v2/`)
> **Gate:** `MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE`
> **Verified:** 2026-07-05

---

## Capability Summary

| # | Question | Classification | Endpoint |
|---|---|---|---|
| 1 | Can external client create a task? | **proven** | `POST /v2/task.create` |
| 2 | Can external client send message to existing task? | **proven** | `POST /v2/task.sendMessage` |
| 3 | Can external client upload + attach a file? | **proven** | `POST /v2/file.upload` + ContentPart |
| 4 | Can external client write to persistent workspace? | **unsupported** (indirect: supported) | — |
| 5 | Can external client read from persistent workspace? | **unsupported** (indirect: supported) | — |
| 6 | Can API trigger/continue work in existing conversation? | **proven** | `POST /v2/task.sendMessage` |
| 7 | What authentication model is required? | **proven** | `x-manus-api-key` header |
| 8 | Which operations are officially documented vs inferred? | see below | — |

---

## Documentation Status

| Capability | Status |
|---|---|
| task.create | officially documented |
| task.sendMessage | officially documented |
| file.upload | officially documented |
| task.listMessages | officially documented |
| task.confirmAction | officially documented |
| webhooks | officially documented |
| structured_output | officially documented |
| agent-default-main_task shortcut | officially documented |
| workspace write via task instruction | **inferred** (not documented, but proven by sandbox behavior) |
| workspace read via task instruction | **inferred** (not documented, but proven by sandbox behavior) |

---

## Authentication Model

```
Method 1: API Key (recommended for BUS)
  Header: x-manus-api-key: <key>
  Scope: full account access
  Rate limit: 10 req/min (task.create)
  Notes: No expiry. Server-to-server. Simplest.

Method 2: OAuth2
  Grant types: authorization_code, client_credentials
  Scopes:
    create_task       → create tasks, send messages, upload files (scoped to OAuth app)
    manage_all_tasks  → full access to all user tasks
  Notes: For third-party apps. create_task scope isolates tasks per OAuth app.
```

---

## Sequence Diagrams

### 1. task.create

```
ChatGPT                    Manus API                  Manus Agent
   |                           |                           |
   |-- POST /v2/task.create -->|                           |
   |   {message: {content},    |                           |
   |    hide_in_task_list: true,|                          |
   |    structured_output_schema}|                         |
   |                           |-- spawn agent task ------>|
   |<-- {task_id, task_url} ---|                           |
   |                           |                           |-- executes task
   |                           |                           |-- writes to workspace
   |                           |<-- task_stopped event ----|
   |-- GET /v2/task.listMessages?task_id=<id> ------------>|
   |<-- {messages: [..., structured_output_result]} -------|
```

### 2. task.sendMessage (BUS relay pattern)

```
ChatGPT                    Manus API                  Manus Agent (IM)
   |                           |                           |
   |-- POST /v2/task.sendMessage -->|                      |
   |   {task_id: "agent-default-main_task",                |
   |    message: {content: "<MP packet>"}}                 |
   |                           |-- relay to IM agent ----->|
   |<-- {ok: true, task_id} ---|                           |
   |                           |                           |-- parses MP packet
   |                           |                           |-- writes to BUS inbox
   |                           |                           |-- executes MP
   |                           |                           |-- writes MPR to outbox
   |                           |<-- task_stopped ----------|
   |-- GET /v2/task.listMessages?task_id=agent-default-main_task
   |<-- {assistant_message: {content: "<MPR>"}} -----------|
```

### 3. file.upload + attachment flow

```
ChatGPT                    Manus API                  S3 CDN
   |                           |                           |
   |-- POST /v2/file.upload -->|                           |
   |   {filename: "mp.md"}     |                           |
   |<-- {file_id, upload_url} -|                           |
   |                           |                           |
   |-- PUT upload_url (file bytes) ------------------->    |
   |<-- 200 OK ----------------------------------------    |
   |                           |                           |
   |-- POST /v2/task.create -->|                           |
   |   {message: {content: [{type: "file", file_id: "..."}]}}
   |<-- {task_id} -------------|                           |
   |                           |-- agent fetches file ---->|
   |                           |<-- file content ----------|
   |                           |-- agent processes ------->|
```

### 4. Structured Output (MPR as JSON)

```
ChatGPT                    Manus API                  Manus Agent
   |                           |                           |
   |-- POST /v2/task.create -->|                           |
   |   {message: {content: "Execute MP..."},               |
   |    structured_output_schema: {                        |
   |      type: "object",                                  |
   |      properties: {status: {type: "string"},           |
   |                   commit: {type: "string"},           |
   |                   ...},                               |
   |      required: ["status", "commit", ...],             |
   |      additionalProperties: false}}                    |
   |<-- {task_id} -------------|                           |
   |                           |                           |-- executes MP
   |                           |                           |-- formats MPR as JSON
   |                           |<-- task_stopped ----------|
   |-- GET /v2/task.listMessages?task_id=<id> ------------>|
   |<-- {structured_output_result: {success: true,         |
   |      value: {status: "EXECUTED", commit: "abc123", ...}}}
```

---

## Blocking Limitations

| ID | Severity | Description | Workaround |
|---|---|---|---|
| BL-01 | **critical** | No direct workspace write API | task instruction → Manus agent writes (async ~30-120s) |
| BL-02 | **critical** | No direct workspace read API | task instruction → Manus agent reads + returns (async) |
| BL-03 | medium | file.upload → S3 CDN, not workspace | Combine file_id with task instruction to write to workspace |
| BL-04 | low | Rate limit: 10 task.create/min | Queue MPs, 6s spacing |

---

## Recommended BUS Integration Pattern

### Async Task Relay Pattern

```
Name:     Async Task Relay Pattern
Auth:     x-manus-api-key
Latency:  30-120s (async task execution)
Eliminates: manual file upload bridge
Requires: Manus agent trained to recognize MP packets
```

**Step-by-step:**

1. ChatGPT sends MP packet as message:
   ```json
   POST /v2/task.sendMessage
   {
     "task_id": "agent-default-main_task",
     "message": {"content": "<full MP packet content>"},
     "structured_output_schema": {
       "type": "object",
       "properties": {
         "status": {"type": "string"},
         "commit": {"type": "string"},
         "mpr_path": {"type": "string"}
       },
       "required": ["status", "commit", "mpr_path"],
       "additionalProperties": false
     }
   }
   ```

2. Manus agent receives, writes to `/home/ubuntu/yos-bus-runtime/inbox/mpm/<packet>.md`

3. Manus agent executes MP, writes MPR to `/home/ubuntu/yos-bus-runtime/outbox/mpm/<mpr>.md`

4. ChatGPT receives structured output:
   ```json
   {
     "status": "EXECUTED_AWAITING_A_G_REVIEW",
     "commit": "abc1234",
     "mpr_path": "01_BACKBONE/MPM/06_REPORTS/awaiting-review/..."
   }
   ```

**Alternative (webhook):**
- Register webhook on `task_stopped` event
- Receive push notification with `task_detail.structured_output`
- No polling required

---

## Minimal Implementation Roadmap

| Phase | Action | Effort | Unblocks |
|---|---|---|---|
| 1 | Generate Manus API key | 5min | all API calls |
| 2 | Test task.sendMessage with MP packet | 30min | BUS first-mile relay |
| 3 | Add structured_output_schema to sendMessage | 1h | MPR as JSON result |
| 4 | Register webhook endpoint | 2h | push last-mile |
| 5 | Train Manus agent via project instruction | 1h | autonomous BUS write |
