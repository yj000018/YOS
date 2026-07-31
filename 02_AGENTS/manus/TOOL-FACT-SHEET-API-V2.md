# Tool Fact Sheet: Manus API v2 (task.listMessages)

**Status:** Validated (2026-07-30)
**Purpose:** Extract full verbatim (user + assistant messages) from any Manus session.
**Alternative to:** Playwright scraping (which is slow, fragile, and requires DOM parsing).

## Authentication
- **Header:** `x-manus-api-key: <TOKEN>`
- **Token Format:** `sk-...`
- **Storage:** 1Password (Vault "MAIN VAULT", item "Manus API Key")

## Endpoint
`GET https://api.manus.im/v2/task.listMessages`

### Parameters
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | Yes | The session ID (e.g., `sFS6j73tgStr66oeGLvkxR`) |
| `limit` | int | No | Max messages per page (Default: ?, Max tested: 200) |
| `cursor` | string | No | Pagination cursor (from `next_cursor` in previous response) |

### Response Structure
```json
{
  "ok": true,
  "messages": [
    {
      "id": "msg_...",
      "timestamp": "2026-07-30T12:00:00.000Z",
      "user_message": {
        "content": "Text string or array of parts"
      }
    },
    {
      "id": "msg_...",
      "timestamp": "2026-07-30T12:00:05.000Z",
      "assistant_message": {
        "content": "Text string"
      }
    }
  ],
  "has_more": true,
  "next_cursor": "cursor_string"
}
```

## Known Limitations & Lessons Learned (LL)
1. **Rate Limiting:** The API strictly enforces rate limits. Exceeding them returns HTTP 429 (`resource_exhausted`).
   - *Mitigation:* Add a `0.5s` delay between requests, and a `3.0s` backoff on 429 errors.
2. **Content Format:** `user_message.content` can sometimes be an array of objects (e.g., `[{"type": "text", "text": "..."}]`) instead of a flat string, especially if the user uploaded files or images. The parser must handle both types.
3. **Completeness:** This API returns the *raw* verbatim, bypassing UI truncations. It is the definitive source of truth for session history.

## Python Example
```python
import urllib.request
import json

def fetch_messages(task_id, api_key):
    url = f"https://api.manus.im/v2/task.listMessages?task_id={task_id}&limit=200"
    headers = {"accept": "application/json", "x-manus-api-key": api_key}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())
```
