# YARP Error Catalogue

> **Version:** v1.0.0
> **Status:** candidate

---

## Error Code Format

```
YARP-E{category}{code}
  E1xx — Transport errors
  E2xx — Session errors
  E3xx — Message errors
  E4xx — Execution errors
  E5xx — Governance errors
  E9xx — Unknown/internal errors
```

---

## E1xx — Transport Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E101 | TRANSPORT_UNAVAILABLE | Transport backend unreachable | yes | yes |
| E102 | TRANSPORT_TIMEOUT | No response within transport timeout | yes | yes |
| E103 | TRANSPORT_AUTH_FAILED | Authentication rejected by transport | no | no |
| E104 | TRANSPORT_RATE_LIMITED | Rate limit exceeded | yes | yes (after retry_after_seconds) |
| E105 | TRANSPORT_PAYLOAD_TOO_LARGE | Payload exceeds transport size limit | no | no (split payload) |
| E106 | TRANSPORT_WRITE_FAILED | Write to transport backend failed | yes | yes |
| E107 | TRANSPORT_READ_FAILED | Read from transport backend failed | yes | yes |
| E108 | TRANSPORT_PUSH_FAILED | Webhook push failed | yes | yes |

---

## E2xx — Session Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E201 | SESSION_VERSION_MISMATCH | Incompatible YARP MAJOR version | no | no (upgrade required) |
| E202 | SESSION_IDENTITY_UNKNOWN | Sender agent_id not recognized | no | no |
| E203 | SESSION_EXPIRED | Session TTL exceeded | yes | yes (new session) |
| E204 | SESSION_CAPABILITY_MISMATCH | Receiver lacks required capability | no | no |
| E205 | SESSION_HANDSHAKE_FAILED | Session negotiation failed | yes | yes |

---

## E3xx — Message Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E301 | MESSAGE_SCHEMA_INVALID | Message does not match YARP schema | no | no (fix message) |
| E302 | MESSAGE_MISSING_REQUIRED_FIELD | Required field absent | no | no (fix message) |
| E303 | MESSAGE_TYPE_UNKNOWN | Unrecognized message_type | no | no |
| E304 | MESSAGE_DUPLICATE | Duplicate envelope_id received | no | no (idempotent) |
| E305 | MESSAGE_EXPIRED | Message TTL (ttl_seconds) exceeded | yes | yes (new message) |
| E306 | MESSAGE_CORRELATION_NOT_FOUND | correlation_id not in state registry | no | no |

---

## E4xx — Execution Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E401 | EXECUTION_MP_NOT_FOUND | mp_id not found in BUS inbox or queue | yes | yes (re-deliver) |
| E402 | EXECUTION_MP_INVALID | MP packet malformed or missing required sections | no | no (fix MP) |
| E403 | EXECUTION_TIMEOUT | Execution exceeded mode timeout | yes | yes |
| E404 | EXECUTION_FAILED | Execution returned error | yes | yes |
| E405 | EXECUTION_CANCELLED | Execution cancelled by orchestrator | no | no |
| E406 | EXECUTION_DUPLICATE | mp_id already in completed state | no | no (return existing RESULT) |
| E407 | EXECUTION_PARTIAL | Execution partially completed | yes | yes (idempotent retry) |
| E408 | EXECUTION_BLOCKED | Execution blocked on external dependency | yes | yes (after unblock) |
| E409 | EXECUTION_VALIDATION_FAILED | BUS or MPM validation failed post-execution | yes | yes |
| E410 | EXECUTION_COMMIT_FAILED | Git commit or push failed | yes | yes |

---

## E5xx — Governance Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E501 | GOVERNANCE_ID_COLLISION | Duplicate yarp_message_id or correlation_id | no | no |
| E502 | GOVERNANCE_IDEMPOTENCY_VIOLATED | Non-idempotent operation attempted twice | no | no |
| E503 | GOVERNANCE_AUDIT_WRITE_FAILED | Audit log write failed | yes | yes |
| E504 | GOVERNANCE_STATE_INVALID | Invalid state transition attempted | no | no |
| E505 | GOVERNANCE_SIGNATURE_INVALID | Message signature/checksum mismatch | no | no |

---

## E9xx — Unknown/Internal Errors

| Code | Name | Description | Recoverable | Retry |
|---|---|---|---|---|
| E901 | INTERNAL_ERROR | Unclassified internal error | yes | yes |
| E902 | UNKNOWN_ERROR | Error type not recognized | yes | yes |

---

## Error Object Schema

```json
{
  "error_code": "YARP-E4xx",
  "error_name": "string",
  "error_message": "string",
  "recoverable": true,
  "retry_eligible": true,
  "retry_after_seconds": 30,
  "context": {
    "correlation_id": "...",
    "mp_id": "...",
    "task_id": "...",
    "phase": "..."
  }
}
```

---

## Recovery Playbook

| Scenario | Error Code | Recovery Action |
|---|---|---|
| Manus API rate limit | E104 | Wait retry_after_seconds (default: 60s), retry |
| Transport timeout | E102 | Retry ×3 with exponential backoff |
| MP not found in inbox | E401 | Re-deliver via BUS or Git fallback |
| Execution timeout (sprint) | E403 | Re-queue with new attempt_id, retry ×2 |
| Git push failed | E410 | Retry ×3, check GitHub PAT |
| Duplicate mp_id | E406 | Return existing RESULT (idempotent) |
| Version mismatch | E201 | Upgrade YARP version on sender or receiver |
| Validation failed | E409 | Run bus.py validate + mpm.py validate, fix issues, retry |
