#!/usr/bin/env python3
"""Transport-safe entrypoint for the ChatGPT-239 ledger crosswalk."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_JSONL_SHA256 = "aeb05f4aad05e039b14c694de893baa1b0a58fa8d279d5bc3d0462678e256b7c"
EXPECTED_ROWS = 239
EXPECTED_KNOWN_IDS = 236


def load_identity_registry() -> tuple[list[dict[str, str]], bytes]:
    parts = sorted((HERE / "source").glob("identity.rows.*.jsonl"))
    expected_names = [f"identity.rows.{i:02d}.jsonl" for i in range(6)]
    if [path.name for path in parts] != expected_names:
        raise RuntimeError(
            f"JSONL source mismatch: {[path.name for path in parts]} != {expected_names}"
        )
    raw = b"".join(path.read_bytes() for path in parts)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_JSONL_SHA256:
        raise RuntimeError(f"JSONL registry SHA mismatch: {digest}")
    payload = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line]
    if len(payload) != EXPECTED_ROWS:
        raise RuntimeError(f"row count mismatch: {len(payload)}")
    if [item["row"] for item in payload] != list(range(1, EXPECTED_ROWS + 1)):
        raise RuntimeError("row sequence mismatch")
    if sum(bool(item.get("id")) for item in payload) != EXPECTED_KNOWN_IDS:
        raise RuntimeError("known UUID count mismatch")

    rows: list[dict[str, str]] = []
    for item in payload:
        rows.append({
            "title": item.get("title", ""),
            "session_id_from_url": item.get("id", ""),
            "created_at": item.get("created_at", ""),
            "updated_at": item.get("updated_at", ""),
            "batch_id": item.get("batch_id", ""),
            "primary_project": "",
            "provisional_category": "",
            "fact_sheet_status": "",
            "verbatim_preservation_status": "",
        })
    return rows, raw


def main() -> int:
    spec = importlib.util.spec_from_file_location(
        "chatgpt239_crosswalk_core", HERE / "build_crosswalk.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load crosswalk core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.load_registry = load_identity_registry
    core_status = int(module.main())
    validation_path = HERE / "generated" / "CHATGPT-239-CROSSWALK-VALIDATION.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    # A ledger with fewer than the 236 already-known UUIDs cannot be the intended
    # ChatGPT corpus and must not yield a green identity crosswalk.
    ledger_usable = validation.get("ledger_chatgpt_rows", 0) >= EXPECTED_KNOWN_IDS
    validation["ledger_usable_for_239_crosswalk"] = ledger_usable
    validation["crosswalk_gate_status"] = "pass" if ledger_usable and core_status == 0 else "blocked_missing_durable_ledger"
    validation_path.write_text(
        json.dumps(validation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0 if core_status == 0 and ledger_usable else 4


if __name__ == "__main__":
    raise SystemExit(main())
