#!/usr/bin/env python3
"""Generate a reconciled ChatGPT raw/verbatim/fact-sheet coverage audit."""
from __future__ import annotations
import csv, hashlib, importlib.util, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
LEDGER = ROOT / "data/master_ledger.csv"
CROSSWALK = HERE / "generated/CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv"
OUT = HERE / "generated"
EXPECTED = {"ledger": 3060, "overlay": 239, "resolved": 237, "absent": 2}
REQUIRED = ("title", "batch_id", "primary_project", "raw_preservation_status",
            "verbatim_preservation_status", "fact_sheet_status")


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_overlay():
    spec = importlib.util.spec_from_file_location("crosswalk_core", HERE / "build_crosswalk.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load crosswalk core")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)
    rows, raw = core.load_registry()
    return [{"row": i, **row} for i, row in enumerate(rows, 1)], raw


def main():
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    overlay, overlay_raw = load_overlay()
    ledger_all = read_csv(LEDGER)
    ledger = [r for r in ledger_all if (r.get("Source") or "").lower() == "chatgpt"]
    crosswalk = read_csv(CROSSWALK)
    ledger_ids = [(r.get("Source_ID") or "").strip() for r in ledger]
    duplicate_ids = sorted(k for k, n in Counter(ledger_ids).items() if k and n > 1)
    by_row = {int(r["curated_row"]): r for r in crosswalk}
    resolved = sum(r.get("relationship") == "same_native_conversation" for r in crosswalk)
    absent = sum(r.get("match_method") == "uuid_absent_from_ledger" for r in crosswalk)
    required = {f: sum(bool((r.get(f) or "").strip()) for r in overlay) for f in REQUIRED}
    counts = {
        "raw": dict(Counter(r.get("raw_preservation_status", "") for r in overlay)),
        "verbatim": dict(Counter(r.get("verbatim_preservation_status", "") for r in overlay)),
        "fact_sheet": dict(Counter(r.get("fact_sheet_status", "") for r in overlay)),
    }

    rows, resolved_ids = [], set()
    for source in overlay:
        match = by_row[source["row"]]
        sid = match.get("resolved_uuid") or source.get("session_id_from_url", "")
        if match.get("resolved_uuid"):
            resolved_ids.add(match["resolved_uuid"])
        rows.append({
            "scope": "curated_overlay", "curated_row": source["row"], "source_id": sid,
            "title": source.get("title", ""),
            "ledger_presence": "present" if match.get("relationship") == "same_native_conversation" else "absent_exception",
            "raw_status": source.get("raw_preservation_status", ""),
            "verbatim_status": source.get("verbatim_preservation_status", ""),
            "fact_sheet_status": source.get("fact_sheet_status", ""),
            "durable_git_verification": "not_verified_by_this_audit",
        })
    for source in ledger:
        sid = (source.get("Source_ID") or "").strip()
        if sid not in resolved_ids:
            rows.append({
                "scope": "ledger_non_curated", "curated_row": "", "source_id": sid,
                "title": source.get("Title", ""), "ledger_presence": "present",
                "raw_status": "unknown_no_curated_evidence",
                "verbatim_status": "unknown_no_curated_evidence",
                "fact_sheet_status": "unknown_no_curated_evidence",
                "durable_git_verification": "not_verified_by_this_audit",
            })

    checks = {
        "ledger_rows_exact": len(ledger) == EXPECTED["ledger"],
        "ledger_ids_unique": len(set(ledger_ids)) == len(ledger_ids) and not duplicate_ids,
        "overlay_rows_exact": len(overlay) == EXPECTED["overlay"],
        "crosswalk_rows_exact": len(crosswalk) == EXPECTED["overlay"],
        "resolved_exact": resolved == EXPECTED["resolved"],
        "absent_exact": absent == EXPECTED["absent"],
        "required_fields_complete": all(required[f] == EXPECTED["overlay"] for f in REQUIRED),
        "output_reconciles": len(rows) == len(ledger) + EXPECTED["absent"],
    }
    execution_gate = "pass" if all(checks.values()) else "blocked"
    validation = {
        "generated_at": generated,
        "ledger_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "ledger_chatgpt_rows": len(ledger), "ledger_unique_ids": len(set(ledger_ids)),
        "ledger_duplicate_ids": duplicate_ids,
        "overlay_sha256": hashlib.sha256(overlay_raw).hexdigest(),
        "overlay_rows": len(overlay), "resolved": resolved, "absent_exceptions": absent,
        "required_nonblank": required, "attested_status_counts": counts,
        "ledger_rows_without_curated_evidence": len(ledger) - resolved,
        "audit_output_rows": len(rows), "execution_checks": checks,
        "audit_execution_gate": execution_gate,
        "durable_completeness_gate": "blocked",
        "durable_blockers": [
            "2823 ledger rows have no curated coverage evidence (including 2 documented absences)",
            "239 curated Fact Sheet statuses are pending in the frozen registry",
            "raw, verbatim, and Fact Sheet files are not yet hash/path verified in Git",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "CHATGPT-COVERAGE-AUDIT.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    (OUT / "CHATGPT-COVERAGE-VALIDATION.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = ["# ChatGPT coverage audit", "", f"- Audit execution gate: **{execution_gate}**",
              "- Durable completeness gate: **blocked**", "", "## Counts",
              f"- Ledger: {len(ledger)}", f"- Overlay: {len(overlay)}",
              f"- Resolved: {resolved}", f"- Documented absences: {absent}",
              f"- Audit rows: {len(rows)}", "", "## Attested statuses",
              f"- Raw: {counts['raw']}", f"- Verbatim: {counts['verbatim']}",
              f"- Fact Sheet: {counts['fact_sheet']}", "", "## Interpretation",
              "The audit reconciles identities and source attestations without treating historical generation claims as durable Git proof."]
    (OUT / "CHATGPT-COVERAGE-REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if execution_gate == "pass" else 5


if __name__ == "__main__":
    raise SystemExit(main())
