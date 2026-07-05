#!/usr/bin/env python3
"""
Basic tests for mpm.py CLI.
Run from repo root: python 01_BACKBONE/MPM/08_TOOLS/tests/test_mpm_cli.py
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add tools dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from mpm import _parse_frontmatter, _resolve_queue, _load_json, _save_json

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
results = []


def test(name, fn):
    try:
        fn()
        print(f"  {PASS}  {name}")
        results.append(True)
    except Exception as e:
        print(f"  {FAIL}  {name}: {e}")
        results.append(False)


def make_test_repo(tmp: Path):
    """Create minimal fake MPM repo structure."""
    ready = tmp / "01_BACKBONE/MPM/04_QUEUE/ready"
    executed = tmp / "01_BACKBONE/MPM/04_QUEUE/executed"
    ledger_dir = tmp / "01_BACKBONE/MPM/05_LEDGER"
    ready.mkdir(parents=True)
    executed.mkdir(parents=True)
    ledger_dir.mkdir(parents=True)
    (tmp / ".git").mkdir()  # fake git root

    ledger = {
        "$schema": "yos-mpm-ledger-v1.0.0",
        "system": "yOS MPM",
        "version": "1.0.0",
        "last_updated": "2026-07-05T00:00:00Z",
        "description": "test ledger",
        "entries": []
    }
    _save_json(ledger_dir / "mp-ledger.json", ledger)
    return tmp


def test_parse_frontmatter():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("---\nmp_id: TEST-001\ntitle: Test\nrisk_flags: []\n---\n# Body\n")
        fname = f.name
    try:
        meta = _parse_frontmatter(Path(fname))
        assert meta.get("mp_id") == "TEST-001", f"Expected TEST-001, got {meta.get('mp_id')}"
        assert meta.get("title") == "Test"
    finally:
        os.unlink(fname)


def test_queue_empty():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_test_repo(Path(tmp))
        q = _resolve_queue(root)
        assert q["queue_condition"] == "none"
        assert q["ready_count"] == 0


def test_queue_exactly_one():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_test_repo(Path(tmp))
        mp_file = root / "01_BACKBONE/MPM/04_QUEUE/ready/MPM-TEST-001.md"
        mp_file.write_text("---\nmp_id: MPM-TEST-001\ntitle: Test\nrisk_flags: []\n---\n# Body\n")
        q = _resolve_queue(root)
        assert q["queue_condition"] == "exactly_one_ready", f"Got: {q['queue_condition']}"
        assert q["ready_count"] == 1
        assert q["selected_mp"]["mp_id"] == "MPM-TEST-001"


def test_queue_multiple():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_test_repo(Path(tmp))
        for i in range(2):
            mp_file = root / f"01_BACKBONE/MPM/04_QUEUE/ready/MPM-TEST-00{i}.md"
            mp_file.write_text(f"---\nmp_id: MPM-TEST-00{i}\ntitle: Test {i}\nrisk_flags: []\n---\n")
        q = _resolve_queue(root)
        assert q["queue_condition"] == "multiple_ready"
        assert q["ready_count"] == 2


def test_queue_risk_flagged():
    with tempfile.TemporaryDirectory() as tmp:
        root = make_test_repo(Path(tmp))
        mp_file = root / "01_BACKBONE/MPM/04_QUEUE/ready/MPM-TEST-RISKY.md"
        mp_file.write_text("---\nmp_id: MPM-TEST-RISKY\ntitle: Risky\nrisk_flags: [source_mutation]\n---\n")
        q = _resolve_queue(root)
        assert q["queue_condition"] == "risk_flagged"


def test_save_load_json():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "sub" / "test.json"
        data = {"key": "value", "num": 42}
        _save_json(p, data)
        loaded = _load_json(p)
        assert loaded == data


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print("  yOS MPM CLI — Tests")
    print(f"{'='*50}\n")

    test("parse_frontmatter", test_parse_frontmatter)
    test("queue_empty", test_queue_empty)
    test("queue_exactly_one", test_queue_exactly_one)
    test("queue_multiple", test_queue_multiple)
    test("queue_risk_flagged", test_queue_risk_flagged)
    test("save_load_json", test_save_load_json)

    passed = sum(results)
    total = len(results)
    print(f"\n  {passed}/{total} tests passed")
    sys.exit(0 if passed == total else 1)
