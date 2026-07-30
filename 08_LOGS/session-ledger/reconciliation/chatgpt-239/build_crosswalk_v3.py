#!/usr/bin/env python3
"""Run the full curated ChatGPT-239 overlay against the ChatGPT ledger.

The repository contains two distinct ledgers:
- data/master_ledger.csv: ChatGPT account ledger (3,060 rows at the frozen base)
- 08_LOGS/session-ledger/data/master_ledger.csv: legacy Manus ledger

Unlike the previous identity-only wrapper, this entrypoint preserves every
curated classification and preservation field already embedded in
source/curated239.part01.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
EXPECTED_ROWS = 239
EXPECTED_KNOWN_IDS = 236
EXPECTED_SOURCE_CSV_SHA256 = "b98e511952d2279cfa3c8bf6d7a5c6aad6fedac18c1a22b46d801fcc332bcbeb"
CHATGPT_LEDGER = ROOT / "data/master_ledger.csv"
MANUS_LEDGER = ROOT / "08_LOGS/session-ledger/data/master_ledger.csv"
REQUIRED_NONBLANK = (
    "title",
    "batch_id",
    "primary_project",
    "raw_preservation_status",
    "verbatim_preservation_status",
    "fact_sheet_status",
)


def main() -> int:
    if not CHATGPT_LEDGER.exists():
        raise RuntimeError(f"missing ChatGPT ledger: {CHATGPT_LEDGER}")
    if CHATGPT_LEDGER.resolve() == MANUS_LEDGER.resolve():
        raise RuntimeError("ChatGPT and Manus ledgers must remain separate")

    spec = importlib.util.spec_from_file_location(
        "chatgpt239_crosswalk_core", HERE / "build_crosswalk.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load crosswalk core")
    core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(core)

    original_load_registry = core.load_registry

    def load_validated_registry():
        rows, raw = original_load_registry()
        if len(rows) != EXPECTED_ROWS:
            raise RuntimeError(f"row count mismatch: {len(rows)}")
        known = sum(bool((row.get("session_id_from_url") or "").strip()) for row in rows)
        if known != EXPECTED_KNOWN_IDS:
            raise RuntimeError(f"known UUID count mismatch: {known}")
        missing = {
            field: [index for index, row in enumerate(rows, 1) if not (row.get(field) or "").strip()]
            for field in REQUIRED_NONBLANK
        }
        missing = {field: values for field, values in missing.items() if values}
        if missing:
            raise RuntimeError(f"required overlay fields missing: {missing}")
        return rows, raw

    core.load_registry = load_validated_registry
    core.LEDGER = CHATGPT_LEDGER
    rows, raw = load_validated_registry()
    required_counts = {
        field: sum(bool((row.get(field) or "").strip()) for row in rows)
        for field in REQUIRED_NONBLANK
    }
    optional_blank = {
        "provisional_category": sum(not bool((row.get("provisional_category") or "").strip()) for row in rows)
    }
    status = int(core.main())

    validation_path = HERE / "generated" / "CHATGPT-239-CROSSWALK-VALIDATION.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    ledger_usable = validation.get("ledger_chatgpt_rows", 0) >= EXPECTED_KNOWN_IDS
    overlay_complete = all(required_counts[field] == EXPECTED_ROWS for field in REQUIRED_NONBLANK)
    validation.update({
        "chatgpt_ledger_path": CHATGPT_LEDGER.relative_to(ROOT).as_posix(),
        "manus_ledger_path_kept_separate": MANUS_LEDGER.relative_to(ROOT).as_posix(),
        "overlay_source_csv_sha256": EXPECTED_SOURCE_CSV_SHA256,
        "overlay_source_bytes": len(raw),
        "overlay_required_nonblank": required_counts,
        "overlay_optional_blank": optional_blank,
        "overlay_complete": overlay_complete,
        "ledger_usable_for_239_crosswalk": ledger_usable,
        "crosswalk_gate_status": "pass" if ledger_usable and overlay_complete and status == 0 else "blocked",
    })
    validation_path.write_text(
        json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0 if status == 0 and ledger_usable and overlay_complete else 4


if __name__ == "__main__":
    raise SystemExit(main())
