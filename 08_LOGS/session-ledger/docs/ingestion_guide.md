# Y-OS Ledger — Ingestion Guide (Multi-LLM)

This guide documents how to ingest sessions from each supported LLM platform into the Y-OS Master Ledger.

---

## 1. Manus (API — Automatic)

**Method**: REST/gRPC API via Python script on the Cloud Computer.
**Frequency**: Run on demand or schedule via cron.

### Prerequisites
- JWT token (expires ~30 days after login — renew via DevTools Network)
- Cloud Computer access (34.148.90.222)

### Steps
```bash
ssh ubuntu@34.148.90.222
cd /home/ubuntu/yos/ledger
python3 delta_sync.py           # Delta sync (recommended)
python3 delta_sync.py --full    # Full rebuild
```

### API Details
- Endpoint: `POST https://api.manus.im/session.v1.SessionService/ListSessions`
- Pagination: `{"limit": 100, "offset": 0}` — increment offset until `hasNext: false`
- Total sessions: 537 (as of 2026-07-30) — no archived sessions endpoint found
- See full API docs: `docs/manus_api_v1.md`

### JWT Renewal
1. Open Manus in browser → DevTools (F12) → Network tab
2. Click any session to trigger API call
3. Find request to `api.manus.im` → Right-click → Copy as cURL
4. Extract `authorization: Bearer eyJ...` value
5. Update `HEADERS["authorization"]` in `scripts/delta_sync.py`

---

## 2. ChatGPT (Cookie-Editor + requests — Semi-Automatic)

**Method**: Export session cookies from browser via Cookie-Editor extension, then Python `requests` script calls ChatGPT's internal API. **No ZIP export, no Playwright, works with Team/Business accounts.**
**Frequency**: Monthly or on demand (re-export cookies when they expire ~30 days).

### Why not the ZIP export?
ChatGPT Team and Business accounts do not have the "Export data" option available in Settings. The Cookie-Editor approach is the only reliable method for these account types.

### Why not Playwright?
Playwright requires a full Chromium headless browser (~300MB RAM, slow startup). A Python `requests` script using the same cookies achieves identical results at 10x lower resource cost.

### Setup (one-time, ~5 minutes)
1. Install [Cookie-Editor](https://cookie-editor.com) in Chrome/Brave:
   - Chrome: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
2. Go to `https://chatgpt.com` (must be logged in)
3. Click the Cookie-Editor icon in the toolbar
4. Click **Export** → **Export as JSON**
5. Save the JSON to the Cloud Computer: `~/yos/ledger/chatgpt_cookies.json`
   (This file is gitignored — never commit cookies to Git)

### Usage
```bash
# Delta sync (recommended — only fetches new conversations)
python3 scripts/ingest_chatgpt_cookies.py

# Full rebuild (replaces all ChatGPT entries)
python3 scripts/ingest_chatgpt_cookies.py --full

# Preview without writing
python3 scripts/ingest_chatgpt_cookies.py --dry-run

# Custom cookie file path
python3 scripts/ingest_chatgpt_cookies.py --cookies /path/to/cookies.json
```

### Cookie Renewal
Cookies expire after ~30 days of inactivity. Signs of expiry: HTTP 401 error.
Renewal: repeat the Cookie-Editor export steps above and overwrite `chatgpt_cookies.json`.

### API Details (internal — may change)
- Endpoint: `GET https://chatgpt.com/backend-api/conversations?offset=0&limit=100&order=updated`
- Pagination: offset-based (same pattern as Manus)
- Key cookie: `__Secure-next-auth.session-token` (the main auth token)
- Rate limit: 1 req/0.5s is safe

### Reusable Pattern
This "Cookie-Editor + requests" pattern works for **any web app without a public API**:
Perplexity, Claude web, Gemini, Notion (as fallback), etc.
Always check for an `Authorization` header or session cookie in DevTools Network first.

---

## 3. Claude (Manual Export — Semi-Automatic)

**Method**: Manual data export from Anthropic, then automated ingestion script.
**Status**: Script planned (not yet built)

### Steps
1. Go to https://claude.ai → Settings → **Export data**
2. Download the ZIP file
3. Run (once script is built):
```bash
python3 scripts/ingest_claude.py /path/to/claude_export.zip
```

### Data Format (expected)
Claude exports conversations as JSON with similar structure to ChatGPT.
Script will be built once an export file is available for analysis.

---

## 4. Gemini (Google Takeout — Manual)

**Method**: Google Takeout export, then automated ingestion.
**Status**: Planned

### Steps
1. Go to https://takeout.google.com
2. Select **Gemini Apps Activity**
3. Download and extract
4. Run (once script is built):
```bash
python3 scripts/ingest_gemini.py /path/to/takeout/
```

---

## 5. Perplexity (No Export — Manual)

**Method**: No official export. Options:
- Manual copy-paste of conversation titles into a CSV
- Browser extension to scrape conversation list
- API (if Pro account — check https://docs.perplexity.ai)

**Status**: Limited — low priority given no bulk export

---

## 6. Future LLMs

To add a new LLM source:
1. Create `scripts/ingest_<llm_name>.py` following the same pattern as `ingest_chatgpt.py`
2. Map native fields to the Ledger schema (`Global_UID`, `Source`, `Source_ID`, `Title`, etc.)
3. Add the LLM to the coverage table in `README.md`
4. Document the export process in this guide

---

## Delta Detection Logic

All ingestion scripts use the same delta detection:
1. Load existing Ledger → extract all `Source_ID` values into a set
2. Parse new export → filter out sessions whose `Source_ID` is already in the set
3. Prepend new sessions to the Ledger (newest first)
4. Save updated Ledger

This ensures idempotency — running the same ingestion twice never creates duplicates.
