# YOS BUS — Google Drive Entry Adapter

**Status:** candidate
**Backend ID:** google_drive
**Versioned:** no
**Transport commit required:** no

---

## Role

Cloud folder transport candidate. ChatGPT writes to a shared Google Drive folder; Manus reads from it.

---

## Status

Not yet probed. Candidate for future gate: `MPM-{DATE}-YOS-BUS-GDRIVE-ENTRY-PROBE-GATE`.

---

## Requirements (when implemented)

- Shared Google Drive folder accessible by both ChatGPT (via API/plugin) and Manus
- `YOS_BUS_GDRIVE_FOLDER_ID` environment variable
- Google Drive API credentials

---

## Target Write Path

```
Google Drive: yos-bus-inbox/mpm/{packet_filename}
```

---

## Notes

Do not use until probed and validated.
