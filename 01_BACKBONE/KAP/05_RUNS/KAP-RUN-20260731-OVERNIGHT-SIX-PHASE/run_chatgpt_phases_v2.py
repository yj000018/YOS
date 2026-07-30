#!/usr/bin/env python3
"""Repository-root-safe entrypoint for ChatGPT overnight phases 1-2."""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
CORE = HERE / "run_chatgpt_phases.py"

spec = importlib.util.spec_from_file_location("fusion_chatgpt_phases_core", CORE)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load ChatGPT overnight phase core")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.ROOT = ROOT
module.LEDGER = ROOT / "data/master_ledger.csv"
module.CROSSWALK = ROOT / "08_LOGS/session-ledger/reconciliation/chatgpt-239/generated/CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv"
raise SystemExit(module.main())
