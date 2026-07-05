# YARP Transport Adapters

> **Version:** v1.0.0
> **Status:** candidate

---

## Transport Adapter Matrix

| Transport | supports_write | supports_read | supports_ack | supports_push | supports_persistence | supports_large_payloads | supports_structured_output | latency | security | status |
|---|---|---|---|---|---|---|---|---|---|---|
| Manus API (task.sendMessage) | indirect | indirect | yes | via webhook | cross-session | 512MB (file_id) | yes (structured_output_schema) | 30-120s | API key / OAuth2 | **production_ready** |
| Manus Workspace Filesystem | yes | yes | no (manual) | no | cross-session | unlimited | no | <1s | sandbox isolation | **production_ready** |
| Direct-file BUS | yes | yes | no (manual) | no | cross-session | unlimited | no | <1s | filesystem | **production_ready** |
| Git BUS fallback | yes | yes | no (manual) | no | permanent | unlimited | no | 5-30s | GitHub PAT | **production_ready** |
| Manual Upload | yes (human) | no | no | no | session-only | 20MB | no | minutes | human relay | **operational_bridge** |
| Webhooks | no | no | no | yes | no | 10MB | yes (JSON body) | <5s | HTTPS + secret | **production_candidate** |
| MCP Bridge | yes | yes | yes | yes | depends | depends | yes | <1s | MCP auth | **candidate** |
| Google Drive | yes | yes | no | no | permanent | 5TB | no | 2-10s | OAuth2 | **candidate** |
| Future adapters | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | future |

---

## 1. Manus API — task.sendMessage

**Status:** production_ready
**YARP Role:** primary first-mile (EXECUTE_MP delivery) + last-mile (RESULT retrieval)

```
supports_write:              indirect (via task instruction → agent writes to workspace)
supports_read:               indirect (via task instruction → agent reads and returns)
supports_ack:                yes (task.sendMessage returns {ok: true, task_id})
supports_push:               yes (via webhook on task_stopped)
supports_persistence:        cross-session (workspace persists)
supports_large_payloads:     yes (512MB via file_id, 20MB via file_url or file_data)
supports_structured_output:  yes (structured_output_schema + structured_output_result event)
latency:                     30-120s (async agent execution)
security:                    x-manus-api-key header (server-to-server) or OAuth2
failure_modes:               rate limit (10/min), agent timeout, task error
```

**YARP Message Mapping:**

| YARP Message | Manus API Call |
|---|---|
| EXECUTE_MP | POST /v2/task.sendMessage {task_id: "agent-default-main_task", message: {content: "<MP>"}} |
| ACK | {ok: true, task_id: "..."} in response |
| RESULT | GET /v2/task.listMessages → structured_output_result event |
| RESULT (push) | POST webhook on task_stopped with structured_output |
| HEARTBEAT | task.listMessages polling |
| CANCEL | task.stop (if available) |

---

## 2. Manus Workspace Filesystem

**Status:** production_ready
**YARP Role:** BUS runtime substrate (direct-file backend)

```
supports_write:              yes (/home/ubuntu/yos-bus-runtime/)
supports_read:               yes
supports_ack:                no (filesystem has no ACK mechanism)
supports_push:               no
supports_persistence:        cross-session (sandbox persists between hibernation cycles)
supports_large_payloads:     yes (limited by disk: ~30GB available)
supports_structured_output:  no (plain files only)
latency:                     <1s
security:                    sandbox isolation (no external access without Manus agent)
failure_modes:               sandbox hibernation (files persist), disk full
```

**YARP Message Mapping:**

| YARP Message | Filesystem Operation |
|---|---|
| EXECUTE_MP | Write to /home/ubuntu/yos-bus-runtime/inbox/mpm/<mp_id>.md |
| ACK | bus.py claim → move to workspace/ |
| RESULT | Write to /home/ubuntu/yos-bus-runtime/outbox/mpm/<mpr_id>.md |
| FINALIZE | bus.py archive → move to archive/ |

---

## 3. Direct-file BUS

**Status:** production_ready
**YARP Role:** Git-committed BUS transport (fallback when workspace not available)

```
supports_write:              yes (01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/)
supports_read:               yes
supports_ack:                no
supports_push:               no
supports_persistence:        permanent (Git)
supports_large_payloads:     yes (Git LFS for >100MB)
supports_structured_output:  no
latency:                     <1s (local) + 5-30s (git push)
security:                    GitHub PAT
failure_modes:               merge conflicts, git push failure
```

---

## 4. Git BUS Fallback

**Status:** production_ready
**YARP Role:** Durable audit trail + fallback transport

```
supports_write:              yes (git commit + push)
supports_read:               yes (git pull + read)
supports_ack:                no
supports_push:               no
supports_persistence:        permanent
supports_large_payloads:     yes (Git LFS)
supports_structured_output:  no
latency:                     5-30s
security:                    GitHub PAT
failure_modes:               network failure, rate limits
```

---

## 5. Manual Upload (Operational Bridge)

**Status:** operational_bridge
**YARP Role:** Phase 0 bridge — human relay

```
supports_write:              yes (human uploads file to Manus)
supports_read:               no (human copies MPR from Manus)
supports_ack:                no
supports_push:               no
supports_persistence:        session-only (upload cleared after session)
supports_large_payloads:     20MB limit
supports_structured_output:  no
latency:                     minutes (human-dependent)
security:                    human relay
failure_modes:               human error, session expiry
```

**Deprecation target:** Phase 2 (Manus API async relay)

---

## 6. Webhooks

**Status:** production_candidate
**YARP Role:** last-mile push (RESULT delivery to orchestrator)

```
supports_write:              no
supports_read:               no
supports_ack:                no
supports_push:               yes (POST to external HTTPS endpoint)
supports_persistence:        no (fire-and-forget)
supports_large_payloads:     10MB JSON body
supports_structured_output:  yes (JSON body with structured_output)
latency:                     <5s
security:                    HTTPS + webhook secret header
failure_modes:               endpoint unreachable, timeout, no retry by default
```

**Setup:** POST /v2/webhook.create {url, events: ["task_stopped"]}

---

## 7. MCP Bridge

**Status:** candidate
**YARP Role:** future bidirectional transport

```
supports_write:              yes (MCP filesystem tools)
supports_read:               yes
supports_ack:                yes (MCP tool response)
supports_push:               yes (MCP notifications)
supports_persistence:        depends on MCP server
supports_large_payloads:     depends
supports_structured_output:  yes
latency:                     <1s
security:                    MCP auth (varies)
failure_modes:               MCP server unavailable, no servers configured (current state)
```

**Blocker:** No MCP servers configured in current yOS session.

---

## 8. Google Drive

**Status:** candidate
**YARP Role:** future cross-platform transport

```
supports_write:              yes (Drive API)
supports_read:               yes
supports_ack:                no
supports_push:               no (polling required)
supports_persistence:        permanent
supports_large_payloads:     5TB
supports_structured_output:  no
latency:                     2-10s
security:                    OAuth2
failure_modes:               auth expiry, quota limits
```

---

## Transport Selection Policy

```
Priority order (EXECUTE_MP delivery):
1. Manus API task.sendMessage (if API key available)
2. Workspace Filesystem direct-file BUS (if YOS_BUS_RUNTIME_ROOT set)
3. Git BUS fallback (always available)
4. Manual upload (operational bridge — Phase 0 only)

Priority order (RESULT retrieval):
1. Webhook push (if endpoint registered)
2. Manus API task.listMessages polling
3. Git BUS outbox polling
4. Manual copy (operational bridge — Phase 0 only)
```
