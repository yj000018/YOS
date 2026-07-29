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

## 2. ChatGPT (Manual Export — Semi-Automatic)

**Method**: Manual data export from OpenAI, then automated ingestion script.
**Frequency**: Monthly or on demand.

### Steps
1. Go to https://chatgpt.com → Settings → Data controls → **Export data**
2. Wait for email from OpenAI (usually 5-30 minutes)
3. Download the ZIP file
4. Run ingestion:
```bash
python3 scripts/ingest_chatgpt.py /path/to/chatgpt_export.zip
# OR with extracted JSON:
python3 scripts/ingest_chatgpt.py /path/to/conversations.json
```

### Data Format
The `conversations.json` file contains an array of conversation objects:
```json
[
  {
    "id": "conv_abc123",
    "title": "My Conversation",
    "create_time": 1720000000.0,
    "update_time": 1720001000.0,
    "mapping": { ... }  // Full message tree (not used in Ledger)
  }
]
```

### Notes
- No API access for manually created conversations (only API-created ones have IDs)
- The `mapping` field contains the full verbatim — used in Phase 2 (LMP processing)
- Drop the ZIP in `ingestion/` folder (gitignored) before running the script

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
