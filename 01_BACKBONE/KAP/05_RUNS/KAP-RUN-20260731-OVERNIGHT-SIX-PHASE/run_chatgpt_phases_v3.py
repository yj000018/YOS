#!/usr/bin/env python3
"""Root-safe and multipart-safe entrypoint for ChatGPT phases 1-2."""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
CORE = HERE / "run_chatgpt_phases.py"
PARTS = [HERE / "source" / f"chatgpt239.overlay-source.part{i:02d}.b64" for i in range(4)]
EXPECTED_SHA256 = "7fa0caaee1f0a255834ec4c32cb6a33544137b2b16d5b19b777f56e31b192b02"


def load_enriched_source() -> tuple[list[dict], str]:
    missing = [path.name for path in PARTS if not path.exists()]
    if missing:
        raise RuntimeError(f"Missing overlay source parts: {missing}")
    encoded = "".join(path.read_text(encoding="utf-8").strip() for path in PARTS)
    raw = zlib.decompress(base64.b64decode(encoded))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"Enriched source SHA mismatch: {digest}")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != 239:
        raise RuntimeError(f"Enriched source row count mismatch: {len(rows)}")
    return rows, digest


spec = importlib.util.spec_from_file_location("fusion_chatgpt_phases_core", CORE)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load ChatGPT overnight phase core")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.ROOT = ROOT
module.LEDGER = ROOT / "data/master_ledger.csv"
module.CROSSWALK = ROOT / "08_LOGS/session-ledger/reconciliation/chatgpt-239/generated/CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv"
module.load_enriched_source = load_enriched_source
raise SystemExit(module.main())
