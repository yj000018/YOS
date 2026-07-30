#!/usr/bin/env python3
"""Transport-safe entrypoint for the ChatGPT-239 ledger crosswalk."""
from __future__ import annotations

import base64
import importlib.util
import json
import hashlib
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_COMPACT_SHA256 = "b77b14264d84cb5c7117aba93378dde26d798bc24870a993aaff7feaa9bb2564"


def load_compact_registry() -> tuple[list[dict[str, str]], bytes]:
    parts = sorted((HERE / "source").glob("compactjson.part*"))
    expected_names = [f"compactjson.part{i:02d}" for i in range(5)]
    if [path.name for path in parts] != expected_names:
        raise RuntimeError(
            f"multipart source mismatch: {[path.name for path in parts]} != {expected_names}"
        )
    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in parts)
    raw = zlib.decompress(base64.b64decode(encoded))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_COMPACT_SHA256:
        raise RuntimeError(f"compact registry SHA mismatch: {digest}")
    payload = json.loads(raw.decode("utf-8"))
    fields = payload["fields"]
    rows = [dict(zip(fields, values, strict=True)) for values in payload["rows"]]
    return rows, raw


def main() -> int:
    spec = importlib.util.spec_from_file_location("chatgpt239_crosswalk_core", HERE / "build_crosswalk.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load crosswalk core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.load_registry = load_compact_registry
    return int(module.main())


if __name__ == "__main__":
    raise SystemExit(main())
