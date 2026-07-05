# YARP Message Types

> **Version:** v1.0.0
> **Status:** candidate

---

## Message Families

| Family | Types |
|---|---|
| Control | PING, HEARTBEAT, CANCEL, FINALIZE |
| Capability | CAPABILITY_QUERY, CAPABILITY_RESPONSE |
| Execution | EXECUTE_MP, ACK, NACK, PROGRESS, REQUEST_INFO, RESULT, ERROR |

---

## 1. PING

**Purpose:** Verify agent liveness and measure round-trip latency.

| Field | Required | Description |
|---|---|---|
| ping_id | yes | Unique ping identifier |
| sent_at | yes | ISO8601 timestamp |

**Optional fields:** none

**Valid sender:** any agent
**Valid receiver:** any agent
**Expected response:** PONG (embedded in ACK with ping_id echo)
**Timeout:** 30s
**Retry:** 3x with 5s backoff
**Idempotency:** yes (ping_id deduplication)
**Failure modes:** timeout → agent considered unreachable

---

## 2. HEARTBEAT

**Purpose:** Periodic liveness signal during long-running execution.

| Field | Required | Description |
|---|---|---|
| task_id | yes | Current task being executed |
| progress_pct | no | 0-100 integer |
| current_phase | no | Human-readable phase name |
| eta_seconds | no | Estimated seconds to completion |

**Valid sender:** executor
**Valid receiver:** orchestrator
**Expected response:** none (fire-and-forget)
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** missing heartbeat after 5min → orchestrator may CANCEL

---

## 3. CANCEL

**Purpose:** Request cancellation of an in-progress execution.

| Field | Required | Description |
|---|---|---|
| correlation_id | yes | Correlation ID of the EXECUTE_MP to cancel |
| reason | yes | Human-readable cancellation reason |

**Valid sender:** orchestrator, operator
**Valid receiver:** executor
**Expected response:** ACK (if cancellation accepted) or NACK (if too late)
**Timeout:** 30s
**Retry:** 1x
**Idempotency:** yes (correlation_id deduplication)
**Failure modes:** NACK → execution already completed, CANCEL ignored

---

## 4. FINALIZE

**Purpose:** Signal that a conversation/session is complete and can be archived.

| Field | Required | Description |
|---|---|---|
| conversation_id | yes | Conversation to finalize |
| archive_path | no | Suggested archive path |

**Valid sender:** orchestrator
**Valid receiver:** executor
**Expected response:** ACK
**Timeout:** 60s
**Retry:** 2x
**Idempotency:** yes
**Failure modes:** timeout → session remains open

---

## 5. CAPABILITY_QUERY

**Purpose:** Query an agent's supported message types, transports, and skills.

| Field | Required | Description |
|---|---|---|
| query_id | yes | Unique query identifier |
| requested_capabilities | no | Specific capabilities to query |

**Valid sender:** any agent
**Valid receiver:** any agent
**Expected response:** CAPABILITY_RESPONSE
**Timeout:** 30s
**Retry:** 2x
**Idempotency:** yes
**Failure modes:** timeout → assume minimal capabilities

---

## 6. CAPABILITY_RESPONSE

**Purpose:** Declare an agent's capabilities in response to CAPABILITY_QUERY.

| Field | Required | Description |
|---|---|---|
| query_id | yes | Echo of CAPABILITY_QUERY.query_id |
| agent_id | yes | Responding agent ID |
| yarp_version | yes | Supported YARP version |
| supported_message_types | yes | Array of message type strings |
| supported_transports | yes | Array of transport IDs |
| supported_artifact_types | yes | Array of artifact type strings |
| agent_profile | no | e.g. "manus-1.6", "gpt-4o", "claude-opus-4" |

**Valid sender:** any agent
**Valid receiver:** any agent
**Expected response:** none
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A

---

## 7. EXECUTE_MP

**Purpose:** Instruct an executor agent to execute a Mega Prompt packet.

| Field | Required | Description |
|---|---|---|
| mp_id | yes | Canonical MP identifier |
| mp_content | yes | Full MP content (string or artifact pointer) |
| mp_mode | yes | sprint / run / marathon |
| correlation_id | yes | Unique correlation ID for this execution |
| requested_executor | no | Target agent ID |
| structured_output_schema | no | JSON Schema for structured RESULT |
| priority | no | low / normal / high |
| deadline_at | no | ISO8601 deadline |

**Valid sender:** orchestrator, operator
**Valid receiver:** executor
**Expected response:** ACK (immediate) + RESULT (async)
**Timeout:** ACK: 60s; RESULT: mode-dependent (sprint: 5min, run: 15min, marathon: 60min)
**Retry:** 3x with exponential backoff; idempotent by mp_id
**Idempotency:** yes — executor must deduplicate by mp_id
**Failure modes:** ACK timeout → retry; RESULT timeout → ERROR; duplicate mp_id → ACK with existing task_id

---

## 8. ACK

**Purpose:** Acknowledge receipt and acceptance of a message.

| Field | Required | Description |
|---|---|---|
| ack_for_message_id | yes | envelope_id of acknowledged message |
| ack_for_type | yes | Message type being acknowledged |
| task_id | no | Assigned task ID (for EXECUTE_MP ACK) |
| accepted | yes | boolean |
| reason | no | If accepted=false, reason string |

**Valid sender:** executor, reviewer
**Valid receiver:** orchestrator
**Expected response:** none
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A

---

## 9. NACK

**Purpose:** Reject a message with reason.

| Field | Required | Description |
|---|---|---|
| nack_for_message_id | yes | envelope_id of rejected message |
| nack_for_type | yes | Message type being rejected |
| error_code | yes | YARP error code (see YARP-ERROR-CATALOGUE.md) |
| reason | yes | Human-readable rejection reason |
| retry_eligible | yes | boolean — can sender retry? |
| retry_after_seconds | no | Suggested retry delay |

**Valid sender:** executor, reviewer
**Valid receiver:** orchestrator
**Expected response:** none
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A

---

## 10. PROGRESS

**Purpose:** Report incremental progress during MP execution.

| Field | Required | Description |
|---|---|---|
| correlation_id | yes | Correlation ID of the EXECUTE_MP |
| task_id | yes | Current task ID |
| phase | yes | Current execution phase |
| progress_pct | no | 0-100 integer |
| message | no | Human-readable progress note |
| files_created | no | Array of file paths created so far |

**Valid sender:** executor
**Valid receiver:** orchestrator
**Expected response:** none (fire-and-forget)
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A

---

## 11. REQUEST_INFO

**Purpose:** Request additional information from orchestrator during execution.

| Field | Required | Description |
|---|---|---|
| correlation_id | yes | Correlation ID of the EXECUTE_MP |
| task_id | yes | Current task ID |
| question | yes | Human-readable question |
| required_fields | yes | Array of field names needed |
| timeout_seconds | no | How long executor will wait (default: 300) |

**Valid sender:** executor
**Valid receiver:** orchestrator, operator
**Expected response:** EXECUTE_MP continuation (sendMessage with answers)
**Timeout:** 300s default
**Retry:** N/A (executor waits)
**Idempotency:** N/A
**Failure modes:** timeout → executor proceeds with best-effort or returns ERROR

---

## 12. RESULT

**Purpose:** Return the result of an MP execution.

| Field | Required | Description |
|---|---|---|
| correlation_id | yes | Correlation ID of the EXECUTE_MP |
| mp_id | yes | MP identifier |
| task_id | yes | Manus task ID |
| status | yes | completed / failed / partial / blocked |
| commit | yes | Git commit hash |
| mpr_path | yes | Path to MPR in repo |
| artifacts | yes | Array of artifact pointers |
| validation | yes | {bus: string, mpm: string} |
| errors | yes | Array of error objects (empty if success) |
| structured_output | no | JSON result if structured_output_schema was set |

**Valid sender:** executor
**Valid receiver:** orchestrator, reviewer
**Expected response:** ACK
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A

---

## 13. ERROR

**Purpose:** Report an unrecoverable error during execution.

| Field | Required | Description |
|---|---|---|
| correlation_id | yes | Correlation ID of the EXECUTE_MP |
| task_id | no | Task ID if assigned |
| error_code | yes | YARP error code |
| error_message | yes | Human-readable error description |
| recoverable | yes | boolean |
| partial_artifacts | no | Any artifacts produced before failure |
| retry_eligible | yes | boolean |

**Valid sender:** executor
**Valid receiver:** orchestrator
**Expected response:** ACK
**Timeout:** N/A
**Retry:** N/A
**Idempotency:** N/A
**Failure modes:** N/A
