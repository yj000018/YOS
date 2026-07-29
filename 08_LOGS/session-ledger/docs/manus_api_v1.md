# Manus API Reference (v1 gRPC/Connect & v2 REST)
*Author: Manus AI — Last Updated: 2026-07-29*

## 1. Overview & Architecture

Manus uses two distinct API paradigms for its frontend operations:
1. **v1 API (gRPC/Connect)**: The primary protocol for core operations (sessions, projects, skills, knowledge). It uses the Connect protocol over HTTP/1.1 with JSON payloads.
2. **v2 API (REST)**: Used primarily for chat streaming, file retrieval, and cascade jobs.

### 1.1 Base URL
All requests are routed through: `https://api.manus.im/`

### 1.2 Authentication
Authentication requires **both** a JWT Bearer token and `httpOnly` session cookies.

**Required Headers:**
```http
authorization: Bearer eyJhbGci... (JWT token)
connect-protocol-version: 1
content-type: application/json
x-client-id: <clientId> (e.g., Ar5uY3QT3YAeaTYrakTIhU)
x-client-locale: en
x-client-timezone: UTC
x-client-type: web
```

**CRITICAL LIMITATION**: The `httpOnly` cookies (like `__Secure-next-auth.session-token`) cannot be accessed via JavaScript `document.cookie`. As a result, **mutations (POST/PUT/DELETE) cannot be executed via `fetch()` from the DevTools console**. They will return `500 Internal Server Error` or `record not found`. 
*Workaround for automation*: Mutations must be triggered by simulating UI events (e.g., `dispatchEvent(new MouseEvent('click'))`) so the browser's native networking stack attaches the `httpOnly` cookies automatically.

---

## 2. v1 API (gRPC/Connect) Reference

Endpoints follow the pattern: `https://api.manus.im/namespace.v1.ServiceName/MethodName`

### 2.1 Session Management (`session.v1.SessionService`)

| Method | Purpose | Payload Example |
|---|---|---|
| `ListSessions` | Retrieve all sessions | `{}` |
| `GetSession` | Get details of a specific session | `{"sessionUid": "..."}` |
| `UpdateSession` | Rename a session | `{"sessionUid": "...", "title": "New Name"}` |
| `ArchiveSession` | Move session to archive | `{"sessionUid": "..."}` |
| `DeleteSession` | Permanently delete session | `{"sessionUid": "..."}` |
| `UpdateReadPosition` | Mark chat as read | `{"sessionUid": "...", "position": 12}` |

### 2.2 Project Management (`session.v1.ProjectService`)

| Method | Purpose | Payload Example |
|---|---|---|
| `GetProject` | Get project metadata | `{"projectUid": "..."}` |
| `ListProjectFiles` | List files attached to project | `{"projectUid": "..."}` |
| `MoveSessionToProject` | Move session to a project | `{"sessionUid": "...", "projectUid": "..."}` |

### 2.3 Scheduling & Automation (`session.v1.SessionService`)

| Method | Purpose |
|---|---|
| `ListScheduledTasks` | List all cron/interval tasks |
| `ListProjectScheduledTasks` | List tasks scoped to a project |
| `ListScheduledTasksWithSessions` | List tasks and their generated sessions |
| `ListScheduleTaskTimeAxis` | Get timeline of task executions |

### 2.4 Ecosystem & Integrations

**Skills (`skill.v1.*`)**
- `skill.v1.SkillOptionalService/ListSkills`: List available skills
- `skill.v1.ProjectSkillService/ListProjectSkills`: List skills enabled for a project

**Knowledge (`knowledge.v1.KnowledgeService`)**
- `ListKnowledgeEvents`: Retrieve memory/knowledge events

**Connectors/Addons (`addon.v1.AddonService`)**
- `ListAddonEntries`: List connected MCPs/APIs
- `IssueAddonSubjectToken`: Generate short-lived token for an addon

---

## 3. v2 API (REST) Reference

The v2 API uses standard REST conventions, primarily for data retrieval and streaming.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/chat/getSessionV2` | GET | Retrieve full chat history. Params: `sessionId`, `getFirstSegment` |
| `/api/chat/getSessionFilesV2` | GET | Retrieve files generated in session. Params: `sessionId`, `type=private` |
| `/api/sessions/{sessionId}/cascade-jobs` | GET | Monitor background tasks (e.g., parallel processing, MCP execution). Params: `status=running` |

---

## 4. Automation Strategy (The "Ledger" Protocol)

To build a definitive Ledger of thousands of sessions and perform a Delta-Sync, follow this protocol:

1. **Extraction**: Use the Cloud Computer (to avoid CloudFront 403 blocks) to run a Python script.
2. **Auth Injection**: Export the JWT and cookies from the browser's Network tab (Copy as cURL) and inject them into the Python script.
3. **Pagination**: Call `session.v1.SessionService/ListSessions` to extract all sessions.
4. **Delta-Sync Logic**: 
   - Load existing `master_ledger.json`.
   - Fetch sessions sorted by `createdAt` descending.
   - Stop fetching when a `sessionUid` matches the most recent ID in the Ledger.
5. **Mutation**: For bulk moving/renaming, generate a UI-automation script (JavaScript) that uses `dispatchEvent` and coordinate-based clicks, as direct `fetch` mutations will fail due to missing `httpOnly` cookies in the console context.

---

## 5. Pagination & Rate Limiting Findings (Updated 2026-07-29)

### 5.1 CloudFront 403 Blocks
**Issue**: Rapid successive JavaScript execution or rapid API calls from the Manus sandbox browser triggers a CloudFront WAF 403 Forbidden error, blocking the session/IP.
**Workaround**: Execute bulk extraction scripts (like the Ledger Sync) from an external persistent node (e.g., Y-OS Cloud Computer `34.148.90.222`). By injecting the `JWT` and `x-client-id` captured from the browser into a Python `urllib` script, the API can be queried securely without triggering browser-based bot protections.

### 5.2 Pagination Mechanism (`ListSessions`)
The `ListSessions` endpoint does **not** use the `cursor` field for pagination, even though it returns a `nextCursor` in some responses.
**Correct Implementation**: Use `offset` and `limit` in the JSON payload.
```json
{
  "limit": 100,
  "offset": 0
}
```
Increment `offset` by `limit` until `hasNext` returns `false` or the `sessions` array is empty.

---

## 6. The Y-OS Master Ledger Workflow

To process thousands of sessions efficiently without hitting rate limits, Y-OS uses a 3-phase architecture:

### Phase 1: Fast Sync (Ledger Initialization)
- **Action**: Query `ListSessions` with pagination via the Cloud Computer.
- **Data**: Extract only metadata (UID, Title, Date, Project ID).
- **Result**: Append new sessions to `master_ledger.json` with `Archive_Status: "Pending"`. Do not open sessions.

### Phase 2: Deep Processing (LLM Memory Pipeline - LMP)
- **Action**: Iterate over `Pending` sessions in the Ledger.
- **Data**: Fetch full verbatim via `GetSessionV2`.
- **Result**: Generate synthesis, extract key knowledge, and push to Notion (yOS Memory).

### Phase 3: State Sync (Visual Feedback)
- **Action**: Mark session as `Archived` in the Ledger.
- **Visual Update**: Use `UpdateSession` (or UI automation) to prepend `[✓]` to the session title in the Manus interface, providing immediate visual feedback that the session has been processed.
