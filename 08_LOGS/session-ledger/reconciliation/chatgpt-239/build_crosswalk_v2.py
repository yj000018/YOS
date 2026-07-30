#!/usr/bin/env python3
"""Transport-safe entrypoint for the ChatGPT-239 ledger crosswalk."""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_IDENTITY_SHA256 = "e94e9edbcbeef9b0078cc52e63c21c8a55d3a8276e8fd317c76c65c073d8ba34"


def load_identity_registry() -> tuple[list[dict[str, str]], bytes]:
    parts = sorted((HERE / "source").glob("idonly.part*"))
    expected_names = ["idonly.part00", "idonly.part01"]
    if [path.name for path in parts] != expected_names:
        raise RuntimeError(
            f"identity source mismatch: {[path.name for path in parts]} != {expected_names}"
        )
    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in parts)
    raw = zlib.decompress(base64.b64decode(encoded))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_IDENTITY_SHA256:
        raise RuntimeError(f"identity registry SHA mismatch: {digest}")
    payload = json.loads(raw.decode("utf-8"))
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
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
