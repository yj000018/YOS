#!/usr/bin/env python3
"""Analyze curated UUIDs absent from the committed ChatGPT ledger.

A curated URL UUID remains authoritative unless exact title+timestamp evidence
proves a unique alternate ledger row. Alternate IDs are reported as candidates,
not silently substituted. No Canon promotion.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
LEDGER = ROOT / "data/master_ledger.csv"
SOURCE = HERE / "source/known_absent_metadata.jsonl"
OUT = HERE / "generated/CHATGPT-KNOWN-UUID-ABSENCE-ANALYSIS.json"


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value).split())


def parse_time(value: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        result = datetime.fromisoformat(value)
    except ValueError:
        return None
    if result.tzinfo is None:
        result = result.replace(tzinfo=timezone.utc)
    return result.astimezone(timezone.utc)


def delta(a: str, b: str) -> float | None:
    da, db = parse_time(a), parse_time(b)
    return abs((da - db).total_seconds()) if da and db else None


def main() -> int:
    with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    source_rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line]
    results = []
    for source in source_rows:
        title_key = normalize(source["title"])
        candidates = []
        for row in rows:
            title_score_exact = normalize(row.get("Title", "")) == title_key
            if not title_score_exact:
                continue
            created_delta = delta(source["created_at"], row.get("Created_At", ""))
            updated_delta = delta(source["updated_at"], row.get("Updated_At", ""))
            candidates.append({
                "source_id": row.get("Source_ID", ""),
                "title": row.get("Title", ""),
                "created_at": row.get("Created_At", ""),
                "updated_at": row.get("Updated_At", ""),
                "created_delta_seconds": created_delta,
                "updated_delta_seconds": updated_delta,
            })
        exact_created = [c for c in candidates if c["created_delta_seconds"] is not None and c["created_delta_seconds"] <= 1.0]
        exact_both = [
            c for c in exact_created
            if c["updated_delta_seconds"] is not None and c["updated_delta_seconds"] <= 1.0
        ]
        if len(exact_both) == 1:
            status = "unique_title_created_updated_alternate_candidate"
            alternate = exact_both[0]["source_id"]
            confidence = 1.0
        elif len(exact_created) == 1:
            status = "unique_title_created_alternate_candidate"
            alternate = exact_created[0]["source_id"]
            confidence = 0.995
        elif len(candidates) == 1:
            status = "unique_title_candidate_needs_review"
            alternate = candidates[0]["source_id"]
            confidence = 0.8
        elif not candidates:
            status = "no_title_candidate_in_ledger"
            alternate = ""
            confidence = 0.0
        else:
            status = "ambiguous_title_candidates"
            alternate = ""
            confidence = 0.0
        results.append({
            **source,
            "status": status,
            "alternate_ledger_uuid": alternate,
            "confidence": confidence,
            "candidate_count": len(candidates),
            "candidates": candidates,
            "curated_uuid_preserved_as_authoritative": True,
            "automatic_substitution": False,
        })

    report = {
        "ledger_path": LEDGER.relative_to(ROOT).as_posix(),
        "rows_analyzed": len(results),
        "results": results,
        "canon_promotions": 0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
