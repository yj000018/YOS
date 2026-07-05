# YARP Migration Plan

> **Version:** v1.0.0
> **Status:** candidate

---

## Migration Overview

```
Phase 0 — Current manual bridge (operational)
Phase 1 — BUS direct-file / manual ingest (operational)
Phase 2 — Manus API async relay (production_candidate)
Phase 3 — Webhook / push last-mile (production_candidate)
Phase 4 — Multi-agent YARP (future)
```

---

## Phase 0 — Current Manual Bridge

**Status:** operational (current state as of 2026-07-05)

**Description:**
```
ChatGPT creates MP file
User uploads to Manus (manual)
Manus executes
User returns MPR to ChatGPT (manual)
```

**YARP compliance:** none (pre-YARP)

**Actors:**
- ChatGPT (A&G): creates MP Markdown file
- Human operator: uploads file to Manus session
- Manus: executes MP, writes MPR
- Human operator: copies MPR back to ChatGPT

**Limitations:**
- Requires human relay for every MP
- No ACK/RESULT protocol
- No correlation tracking
- No idempotency
- Latency: minutes (human-dependent)

**Deprecation target:** Phase 2

---

## Phase 1 — BUS Direct-file / Manual Ingest

**Status:** operational (BUS module created 2026-07-05)

**Description:**
```
ChatGPT creates MP file
User uploads to Manus (manual)
Manus agent uses bus.py to ingest MP into BUS inbox
Manus executes via MPM
Manus writes MPR to BUS outbox
User returns MPR to ChatGPT (manual)
```

**YARP compliance:** partial (BUS transport layer, no YARP envelope)

**Improvements over Phase 0:**
- BUS lifecycle (inbox → workspace → outbox → archive)
- `bus.py claim` for idempotent packet claiming
- `bus.py validate` for transport health checks
- `latest-mpr.json` fixed pointer for MPR retrieval
- Git-committed audit trail

**Remaining gaps:**
- No YARP envelope
- No ACK/RESULT protocol
- Human relay still required for delivery
- No structured output

**Deprecation target:** Phase 2 (human relay eliminated)

---

## Phase 2 — Manus API Async Relay

**Status:** production_candidate (API verified, not yet live)

**Description:**
```
ChatGPT emits EXECUTE_MP via Manus API task.sendMessage
Manus agent receives, writes to BUS inbox
Manus executes via MPM
Manus returns RESULT JSON via structured_output
ChatGPT reads RESULT via task.listMessages polling
MPR Markdown generated for audit
```

**YARP compliance:** high (EXECUTE_MP + ACK + RESULT, JSON-first)

**Implementation steps:**
1. Generate Manus API key (5min)
2. Test task.sendMessage with MP packet (30min)
3. Add structured_output_schema for MPR as JSON (1h)
4. Train Manus agent via project instruction to recognize MP packets (1h)
5. Validate end-to-end: ChatGPT → Manus → MPR → ChatGPT (2h)

**Estimated effort:** ~4h
**Unblocks:** elimination of human relay for MP delivery

**Remaining gaps:**
- Polling required (no push)
- Human relay still needed for MPR review (A&G review step)

---

## Phase 3 — Webhook / Push Last-mile

**Status:** production_candidate (API verified, not yet live)

**Description:**
```
ChatGPT emits EXECUTE_MP via Manus API
Manus ACKs immediately
Manus executes
Manus pushes RESULT to ChatGPT webhook endpoint
ChatGPT receives RESULT JSON push notification
No polling required
```

**YARP compliance:** full (EXECUTE_MP + ACK + RESULT push, JSON-first)

**Implementation steps:**
1. Deploy webhook receiver endpoint (HTTPS) (2h)
2. Register webhook via POST /v2/webhook.create (30min)
3. Handle task_stopped event with structured_output (1h)
4. Validate end-to-end push flow (1h)

**Estimated effort:** ~4-5h
**Unblocks:** real-time MPR delivery, eliminates polling

---

## Phase 4 — Multi-agent YARP

**Status:** future

**Description:**
```
ChatGPT emits EXECUTE_MP via YARP envelope
Transport adapter selected automatically (API → BUS → Git fallback)
Manus ACKs via YARP ACK
Manus executes
Manus returns YARP RESULT
Claude reviews MPR via YARP RESULT → ACK/NACK
n8n automation triggers on YARP events
All agents speak YARP natively
```

**YARP compliance:** full (all 13 message types, all 5 layers)

**Implementation steps:**
1. YARP envelope wrapper library (Python + Node.js) (2 days)
2. YARP session manager (handshake, version negotiation) (1 day)
3. YARP state machine runtime (1 day)
4. MCP server for YARP transport (2 days)
5. Multi-agent routing (ChatGPT → Claude → Manus → n8n) (3 days)

**Estimated effort:** ~2 weeks
**Unblocks:** full multi-agent yOS cognitive OS

---

## Migration Checklist

| Phase | Status | Blocker | Next Action |
|---|---|---|---|
| Phase 0 | ✅ operational | none | deprecate after Phase 2 |
| Phase 1 | ✅ operational | none | use as fallback |
| Phase 2 | 🔶 candidate | API key not generated | generate Manus API key |
| Phase 3 | 🔶 candidate | no webhook endpoint | deploy webhook receiver |
| Phase 4 | ⬜ future | Phase 2+3 must be live | N/A |

---

## BUS / MPM Integration Points

| YARP Component | BUS Integration | MPM Integration |
|---|---|---|
| EXECUTE_MP delivery | BUS inbox/mpm/ | MPM ready queue |
| ACK | BUS claim (bus.py claim) | MPM ledger status: running |
| RESULT | BUS outbox/mpm/ | MPM ledger status: executed |
| FINALIZE | BUS archive/mpm/ | MPM ledger status: archived |
| Correlation | latest-bus-event.json | mp-ledger.json |
| Fast-path pointer | latest-bus-event.json | latest-mpr.json |
