# Y-OS Session Ledger

**Status**: Active | **Last Sync**: 2026-07-30 | **Total Sessions**: 537 (Manus)

The Y-OS Session Ledger is the **Master Table of Contents** for all LLM sessions across all platforms. It is a lightweight index — not an archive. Its purpose is to track what exists, where it lives, and whether it has been processed by the LLM Memory Pipeline (LMP).

---

## Architecture

```
session-ledger/
├── README.md              ← This file
├── data/
│   ├── master_ledger.csv  ← The Ledger (all sessions, all LLMs)
│   └── manus_raw.json     ← Raw API dump (Manus only, last full sync)
├── scripts/
│   ├── delta_sync.py      ← Manus API Delta-Sync (run on Cloud Computer)
│   ├── ingest_chatgpt.py  ← ChatGPT conversations.json ingestion
│   ├── ingest_claude.py   ← Claude export ingestion (future)
│   └── process_ledger.py  ← LMP Phase 2: enrich + mark as Archived
├── docs/
│   ├── manus_api_v1.md    ← Manus API exhaustive documentation
│   └── ingestion_guide.md ← How to ingest each LLM's sessions
└── ingestion/
    └── .gitkeep           ← Drop raw export files here (not committed)
```

---

## Ledger Schema

| Column | Type | Description |
|---|---|---|
| `Global_UID` | string | Y-OS unique ID (`manus_<uid>`, `chatgpt_<id>`, etc.) |
| `Source` | string | LLM platform: `Manus`, `ChatGPT`, `Claude`, `Gemini`, etc. |
| `Source_ID` | string | Native session/conversation ID from the source platform |
| `Title` | string | Session title (native, may include `[✓]` prefix if LMP-processed) |
| `Project_ID` | string | Manus project UID (if classified) |
| `Created_At` | datetime | Session creation timestamp (ISO 8601) |
| `Updated_At` | datetime | Last update timestamp |
| `Archive_Status` | enum | `Pending` (not processed) / `Archived` (LMP done) |
| `Archive_Link` | url | Notion page URL containing verbatim + synthesis |
| `Topic_Summary` | string | 1-2 sentence LLM-generated summary (filled during LMP) |
| `Project_Tag` | string | Y-OS project label (filled during LMP) |

---

## Workflow

### Phase 1 — Fast Sync (Ledger Update)
Adds new sessions to the Ledger without opening them. Runs in seconds.

```bash
# On Cloud Computer (34.148.90.222)
cd /home/ubuntu/yos/ledger
python3 delta_sync.py           # Delta: adds only new sessions
python3 delta_sync.py --full    # Full rebuild from scratch
```

### Phase 2 — Deep Processing (LMP)
Opens each `Pending` session, generates synthesis, pushes to Notion.
Marks session as `Archived` and optionally renames it with `[✓]` prefix.

```bash
python3 process_ledger.py --limit 10   # Process 10 pending sessions
```

### Phase 3 — State Sync
Updates `Archive_Status` in the Ledger and optionally renames the session in the source platform.

---

## LLM Coverage

| LLM | Ingestion Method | Status | Sessions |
|---|---|---|---|
| **Manus** | API (`ListSessions` + pagination) | ✅ Active | 537 |
| **ChatGPT** | Manual export (`conversations.json` ZIP) | 🔧 Script ready | TBD |
| **Claude** | Manual export (claude.ai Settings > Export) | 📋 Planned | TBD |
| **Gemini** | Manual export (Google Takeout) | 📋 Planned | TBD |
| **Perplexity** | No export available (manual copy) | ⚠️ Limited | TBD |

---

## JWT Token Management

The Manus API requires a JWT Bearer token. Current token expires: **2026-08-26**.

To renew:
1. Open Manus in browser
2. DevTools (F12) → Network tab
3. Click any session to trigger an API call
4. Find a request to `api.manus.im`
5. Right-click → Copy as cURL
6. Extract the `authorization: Bearer eyJ...` value
7. Update `HEADERS["authorization"]` in `scripts/delta_sync.py`

---

## Notes

- The `ingestion/` folder is gitignored — drop raw export files there, never commit them (they contain private conversation data)
- The `data/manus_raw.json` file contains full API responses — commit only if needed for debugging
- The `data/master_ledger.csv` is the canonical source of truth — always commit after a sync
