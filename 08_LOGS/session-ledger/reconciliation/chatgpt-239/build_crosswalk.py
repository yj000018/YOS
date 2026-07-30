#!/usr/bin/env python3
"""Crosswalk the frozen curated ChatGPT-239 registry to the YOS session ledger.

Identity rules:
- Native key is ChatGPT conversation UUID (ledger Source_ID).
- Known UUIDs are joined exactly only.
- Blank legacy UUIDs may be recovered only when title and timestamps provide a
  unique deterministic match. We never assign a fuzzy-only candidate.
- FUSION lineage is inventoried separately.
- No row is promoted to Canon.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import unicodedata
import zlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SOURCE_PART = HERE / "source" / "curated239.part01"
LEDGER = ROOT / "08_LOGS" / "session-ledger" / "data" / "master_ledger.csv"
OUT = HERE / "generated"
EXPECTED_REGISTRY_ROWS = 239
EXPECTED_KNOWN_UUIDS = 236
EXPECTED_SOURCE_SHA256 = "b98e511952d2279cfa3c8bf6d7a5c6aad6fedac18c1a22b46d801fcc332bcbeb"
FUSION_KNOWN = {
    "ONE FUSION": "6a5de467-6844-83eb-9a4f-849597c24605",
    "FUSION 1": "6a62566a-9b14-83eb-90a9-83c700b9f331",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def parse_time(value: str) -> datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def seconds_apart(a: str, b: str) -> float | None:
    da, db = parse_time(a), parse_time(b)
    if da is None or db is None:
        return None
    return abs((da - db).total_seconds())


def load_registry() -> tuple[list[dict[str, str]], bytes]:
    encoded = SOURCE_PART.read_text(encoding="utf-8").strip()
    raw = zlib.decompress(base64.b64decode(encoded))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"registry SHA mismatch: {digest}")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    return rows, raw


def load_ledger() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_write(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def json_write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def recover_blank_id(
    curated: dict[str, str],
    chatgpt_rows: list[dict[str, str]],
    title_index: dict[str, list[dict[str, str]]],
) -> dict[str, Any]:
    title_key = normalize_title(curated.get("title", ""))
    candidates = title_index.get(title_key, [])
    scored: list[dict[str, Any]] = []
    for row in candidates:
        created_delta = seconds_apart(curated.get("created_at", ""), row.get("Created_At", ""))
        updated_delta = seconds_apart(curated.get("updated_at", ""), row.get("Updated_At", ""))
        scored.append({
            "row": row,
            "created_delta_seconds": created_delta,
            "updated_delta_seconds": updated_delta,
        })

    exact_both = [
        item for item in scored
        if item["created_delta_seconds"] is not None
        and item["created_delta_seconds"] <= 1.0
        and item["updated_delta_seconds"] is not None
        and item["updated_delta_seconds"] <= 1.0
    ]
    if len(exact_both) == 1:
        item = exact_both[0]
        return {
            "recovered_id": item["row"].get("Source_ID", ""),
            "ledger_row": item["row"],
            "method": "title_created_updated_exact",
            "confidence": 1.0,
            "review_status": "verified_recovered",
            "candidate_count": len(candidates),
            "created_delta_seconds": item["created_delta_seconds"],
            "updated_delta_seconds": item["updated_delta_seconds"],
        }

    exact_created = [
        item for item in scored
        if item["created_delta_seconds"] is not None
        and item["created_delta_seconds"] <= 1.0
    ]
    if len(exact_created) == 1:
        item = exact_created[0]
        return {
            "recovered_id": item["row"].get("Source_ID", ""),
            "ledger_row": item["row"],
            "method": "title_created_exact",
            "confidence": 0.995,
            "review_status": "verified_recovered",
            "candidate_count": len(candidates),
            "created_delta_seconds": item["created_delta_seconds"],
            "updated_delta_seconds": item["updated_delta_seconds"],
        }

    # Unique title alone is recorded as a candidate, never assigned as native identity.
    if len(candidates) == 1:
        item = scored[0]
        return {
            "recovered_id": "",
            "candidate_id": item["row"].get("Source_ID", ""),
            "ledger_row": item["row"],
            "method": "unique_title_candidate_only",
            "confidence": 0.80,
            "review_status": "needs_review",
            "candidate_count": 1,
            "created_delta_seconds": item["created_delta_seconds"],
            "updated_delta_seconds": item["updated_delta_seconds"],
        }

    return {
        "recovered_id": "",
        "candidate_id": "",
        "ledger_row": {},
        "method": "no_deterministic_match" if not candidates else "ambiguous_title_candidates",
        "confidence": 0.0,
        "review_status": "unresolved",
        "candidate_count": len(candidates),
        "created_delta_seconds": None,
        "updated_delta_seconds": None,
    }


def fusion_candidates(chatgpt_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in chatgpt_rows:
        key = normalize_title(row.get("Title", ""))
        if "fusion" not in key:
            continue
        rows.append({
            "source_id": row.get("Source_ID", ""),
            "title": row.get("Title", ""),
            "normalized_title": key,
            "created_at": row.get("Created_At", ""),
            "updated_at": row.get("Updated_At", ""),
            "ledger_global_uid": row.get("Global_UID", ""),
        })
    return sorted(rows, key=lambda row: (row["created_at"], row["source_id"]))


def main() -> int:
    generated = now_utc()
    curated, raw = load_registry()
    ledger = load_ledger()
    chatgpt = [row for row in ledger if (row.get("Source") or "").strip().lower() == "chatgpt"]

    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_title: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in chatgpt:
        by_id[(row.get("Source_ID") or "").strip()].append(row)
        by_title[normalize_title(row.get("Title", ""))].append(row)

    known_ids = [(row.get("session_id_from_url") or "").strip() for row in curated]
    known_nonblank = [value for value in known_ids if value]
    missing_rows = [row for row in curated if not (row.get("session_id_from_url") or "").strip()]

    crosswalk: list[dict[str, Any]] = []
    recovered: list[dict[str, Any]] = []
    for index, row in enumerate(curated, 1):
        source_id = (row.get("session_id_from_url") or "").strip()
        ledger_row: dict[str, str] = {}
        candidate_id = ""
        method = ""
        confidence = 0.0
        review_status = ""
        candidate_count = 0
        created_delta: float | None = None
        updated_delta: float | None = None

        if source_id:
            matches = by_id.get(source_id, [])
            candidate_count = len(matches)
            if len(matches) == 1:
                ledger_row = matches[0]
                method = "uuid_exact"
                confidence = 1.0
                review_status = "verified_exact"
            elif len(matches) == 0:
                method = "uuid_absent_from_ledger"
                review_status = "unresolved"
            else:
                ledger_row = matches[0]
                method = "uuid_duplicate_in_ledger"
                review_status = "needs_review"
        else:
            result = recover_blank_id(row, chatgpt, by_title)
            source_id = result.get("recovered_id", "")
            candidate_id = result.get("candidate_id", "")
            ledger_row = result.get("ledger_row", {})
            method = result["method"]
            confidence = result["confidence"]
            review_status = result["review_status"]
            candidate_count = result["candidate_count"]
            created_delta = result["created_delta_seconds"]
            updated_delta = result["updated_delta_seconds"]
            recovered.append({
                "title": row.get("title", ""),
                "recovered_id": source_id,
                "candidate_id": candidate_id,
                "method": method,
                "confidence": confidence,
                "review_status": review_status,
                "candidate_count": candidate_count,
                "created_delta_seconds": created_delta,
                "updated_delta_seconds": updated_delta,
            })

        crosswalk.append({
            "curated_row": index,
            "title": row.get("title", ""),
            "curated_uuid_original": row.get("session_id_from_url", ""),
            "resolved_uuid": source_id,
            "candidate_uuid": candidate_id,
            "relationship": "same_native_conversation" if source_id and review_status.startswith("verified") else "unresolved",
            "match_method": method,
            "match_confidence": confidence,
            "review_status": review_status,
            "candidate_count": candidate_count,
            "curated_created_at": row.get("created_at", ""),
            "ledger_created_at": ledger_row.get("Created_At", ""),
            "created_delta_seconds": created_delta,
            "curated_updated_at": row.get("updated_at", ""),
            "ledger_updated_at": ledger_row.get("Updated_At", ""),
            "updated_delta_seconds": updated_delta,
            "ledger_title": ledger_row.get("Title", ""),
            "ledger_global_uid": ledger_row.get("Global_UID", ""),
            "baseline_batch_id": row.get("batch_id", ""),
            "baseline_primary_project": row.get("primary_project", ""),
            "baseline_provisional_category": row.get("provisional_category", ""),
            "baseline_fact_sheet_status": row.get("fact_sheet_status", ""),
            "baseline_verbatim_preservation_status": row.get("verbatim_preservation_status", ""),
            "canon_promoted": False,
        })

    fusions = fusion_candidates(chatgpt)
    fusion2_exact = [row for row in fusions if row["normalized_title"] == "fusion 2"]
    fusion2_resolution = {
        "native_id": fusion2_exact[0]["source_id"] if len(fusion2_exact) == 1 else "",
        "status": "verified_unique_exact_title_in_ledger" if len(fusion2_exact) == 1 else (
            "not_found" if len(fusion2_exact) == 0 else "ambiguous"
        ),
        "candidate_count": len(fusion2_exact),
    }

    fusion_rows: list[dict[str, Any]] = []
    for label, native_id in FUSION_KNOWN.items():
        matches = by_id.get(native_id, [])
        fusion_rows.append({
            "lineage_node": label,
            "native_id": native_id,
            "ledger_present": len(matches) == 1,
            "ledger_title": matches[0].get("Title", "") if matches else "",
            "created_at": matches[0].get("Created_At", "") if matches else "",
            "updated_at": matches[0].get("Updated_At", "") if matches else "",
            "identity_method": "known_uuid_exact",
            "review_status": "verified_exact" if len(matches) == 1 else "unresolved",
        })
    fusion_rows.append({
        "lineage_node": "FUSION 2",
        "native_id": fusion2_resolution["native_id"],
        "ledger_present": bool(fusion2_resolution["native_id"]),
        "ledger_title": fusion2_exact[0]["title"] if len(fusion2_exact) == 1 else "",
        "created_at": fusion2_exact[0]["created_at"] if len(fusion2_exact) == 1 else "",
        "updated_at": fusion2_exact[0]["updated_at"] if len(fusion2_exact) == 1 else "",
        "identity_method": "unique_exact_normalized_title_in_ledger" if len(fusion2_exact) == 1 else fusion2_resolution["status"],
        "review_status": "verified_ledger_identity" if len(fusion2_exact) == 1 else "unresolved",
    })

    stats = {
        "generated_at": generated,
        "source_registry_sha256": hashlib.sha256(raw).hexdigest(),
        "source_registry_rows": len(curated),
        "source_registry_rows_valid": len(curated) == EXPECTED_REGISTRY_ROWS,
        "source_registry_known_uuid_count": len(known_nonblank),
        "source_registry_known_uuid_count_valid": len(known_nonblank) == EXPECTED_KNOWN_UUIDS,
        "source_registry_unique_known_uuid_count": len(set(known_nonblank)),
        "source_registry_blank_uuid_count": len(missing_rows),
        "ledger_blob_sha256": hashlib.sha256(LEDGER.read_bytes()).hexdigest(),
        "ledger_commit": git("log", "-1", "--format=%H", "--", LEDGER.relative_to(ROOT).as_posix()),
        "ledger_total_rows": len(ledger),
        "ledger_chatgpt_rows": len(chatgpt),
        "ledger_chatgpt_unique_ids": len({row.get("Source_ID", "") for row in chatgpt if row.get("Source_ID")}),
        "ledger_chatgpt_duplicate_ids": sorted(
            source_id for source_id, count in Counter(
                row.get("Source_ID", "") for row in chatgpt if row.get("Source_ID")
            ).items() if count > 1
        ),
        "known_uuid_exact_matches": sum(row["match_method"] == "uuid_exact" for row in crosswalk),
        "known_uuid_absent": sum(row["match_method"] == "uuid_absent_from_ledger" for row in crosswalk),
        "blank_uuid_recovered": sum(bool(row["recovered_id"]) for row in recovered),
        "blank_uuid_unresolved": sum(not bool(row["recovered_id"]) for row in recovered),
        "resolved_crosswalk_rows": sum(row["relationship"] == "same_native_conversation" for row in crosswalk),
        "unresolved_crosswalk_rows": sum(row["relationship"] != "same_native_conversation" for row in crosswalk),
        "fusion2": fusion2_resolution,
        "fusion_title_candidates": fusions,
        "canon_promotions": 0,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    csv_write(OUT / "CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv", crosswalk, list(crosswalk[0]))
    csv_write(OUT / "CHATGPT-FUSION-LINEAGE.csv", fusion_rows, list(fusion_rows[0]))
    json_write(OUT / "CHATGPT-239-CROSSWALK-VALIDATION.json", {**stats, "blank_uuid_recovery": recovered})

    summary = [
        "---",
        "document_id: CHATGPT-239-YOS-LEDGER-CROSSWALK-SUMMARY-v1.0",
        "document_type: evidence_summary",
        "status: active_evidence_not_canon",
        f"generated_at: {generated}",
        "canon_promotions: 0",
        "---",
        "",
        "# ChatGPT 239 → YOS ledger crosswalk",
        "",
        "## Result",
        "",
        "| Metric | Count / value |",
        "|---|---:|",
        f"| Frozen curated rows | {len(curated)} |",
        f"| Known UUIDs in baseline | {len(known_nonblank)} |",
        f"| ChatGPT rows in current ledger | {len(chatgpt)} |",
        f"| Exact UUID matches | {stats['known_uuid_exact_matches']} |",
        f"| Blank UUIDs deterministically recovered | {stats['blank_uuid_recovered']} |",
        f"| Total resolved crosswalk rows | {stats['resolved_crosswalk_rows']} |",
        f"| Unresolved rows | {stats['unresolved_crosswalk_rows']} |",
        f"| FUSION 2 native ID | `{fusion2_resolution['native_id'] or 'unresolved'}` |",
        "",
        "## Blank-ID recovery",
        "",
        "| Title | Recovered UUID | Candidate UUID | Method | Status |",
        "|---|---|---|---|---|",
    ]
    for row in recovered:
        summary.append(
            f"| {row['title']} | `{row['recovered_id']}` | `{row['candidate_id']}` | "
            f"`{row['method']}` | `{row['review_status']}` |"
        )
    summary += [
        "",
        "## FUSION lineage",
        "",
        "| Node | Native ID | Ledger title | Method | Status |",
        "|---|---|---|---|---|",
    ]
    for row in fusion_rows:
        summary.append(
            f"| {row['lineage_node']} | `{row['native_id']}` | {row['ledger_title']} | "
            f"`{row['identity_method']}` | `{row['review_status']}` |"
        )
    summary += [
        "",
        "The curated classifications remain attached to the frozen 239 cohort. The ledger adds native acquisition provenance only.",
        "No fuzzy-only match is promoted to native identity or Canon.",
    ]
    (OUT / "CHATGPT-239-CROSSWALK-SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    hard_valid = (
        stats["source_registry_rows_valid"]
        and stats["source_registry_known_uuid_count_valid"]
        and not stats["ledger_chatgpt_duplicate_ids"]
    )
    return 0 if hard_valid else 3


if __name__ == "__main__":
    raise SystemExit(main())
