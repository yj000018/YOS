#!/usr/bin/env python3
"""Run phases 1-2 of the overnight YOS corpus operation.

Phase 1: attach the frozen enriched ChatGPT-239 classifications as a separate
overlay on the 3,060-row native ledger.
Phase 2: audit committed Git evidence for raw bodies, verbatim, Fact Sheets and
summaries for every ledger UUID.

The native ledger is never modified and nothing is promoted to Canon.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import json
import re
import subprocess
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
SOURCE = HERE / "source/chatgpt239.overlay-source.zlib.b64"
LEDGER = ROOT / "data/master_ledger.csv"
CROSSWALK = ROOT / "08_LOGS/session-ledger/reconciliation/chatgpt-239/generated/CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv"
OUT = HERE / "generated/chatgpt"
EXPECTED_LEDGER_ROWS = 3060
EXPECTED_CURATED_ROWS = 239
EXPECTED_SOURCE_SHA256 = "7fa0caaee1f0a255834ec4c32cb6a33544137b2b16d5b19b777f56e31b192b02"
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
ROLE_RE = re.compile(r"(?:^|\n)\s*(?:\*\*)?(USER|ASSISTANT|CHATGPT|MANUS|You)(?:\*\*)?\s*[:—-]", re.I)
SUMMARY_RE = re.compile(r"(?:executive summary|résumé exécutif|session card|what was done|ce qui a été fait|key insights|next steps)", re.I)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".csv", ".html", ".htm", ".yaml", ".yml"}
CONTROL_PATH_MARKERS = (
    "data/master_ledger.csv",
    "chatgpt-239-to-yos-ledger-crosswalk.csv",
    "identity.rows.",
    "overlay-source",
    "generated/chatgpt",
)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_enriched_source() -> tuple[list[dict[str, Any]], str]:
    encoded = SOURCE.read_text(encoding="utf-8").strip()
    raw = zlib.decompress(base64.b64decode(encoded))
    digest = sha256_bytes(raw)
    if digest != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"enriched source SHA mismatch: {digest}")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != EXPECTED_CURATED_ROWS:
        raise RuntimeError(f"enriched source rows: {len(rows)} != {EXPECTED_CURATED_ROWS}")
    return rows, digest


def git_files() -> list[Path]:
    output = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"])
    result = []
    for raw in output.split(b"\0"):
        if raw:
            result.append(ROOT / raw.decode("utf-8", errors="replace"))
    return result


def classify_evidence(path: Path, text: str) -> set[str]:
    rel = path.relative_to(ROOT).as_posix().lower()
    kinds: set[str] = set()
    if "factsheet" in rel or "session_card" in rel or "session-card" in rel:
        kinds.add("fact_sheet")
    if "verbatim" in rel or "transcript" in rel or len(ROLE_RE.findall(text)) >= 2:
        kinds.add("verbatim")
    raw_path = any(token in rel for token in ("/raw", "raw_", "conversation", "export", "archive"))
    if raw_path or (path.suffix.lower() == ".json" and len(text) >= 1000):
        kinds.add("raw_body")
    if "summary" in rel or "synthesis" in rel or SUMMARY_RE.search(text):
        kinds.add("summary")
    return kinds


def audit_evidence(ledger_ids: set[str]) -> tuple[dict[str, dict[str, set[str]]], dict[str, Any]]:
    evidence: dict[str, dict[str, set[str]]] = {
        uid: {"raw_body": set(), "verbatim": set(), "fact_sheet": set(), "summary": set()}
        for uid in ledger_ids
    }
    scanned = 0
    skipped_large = 0
    errors: list[str] = []
    for path in git_files():
        rel = path.relative_to(ROOT).as_posix()
        low = rel.lower()
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(marker in low for marker in CONTROL_PATH_MARKERS):
            continue
        try:
            size = path.stat().st_size
            if size > 20_000_000:
                skipped_large += 1
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"{rel}: {exc}")
            continue
        ids = {match.lower() for match in UUID_RE.findall(text)} & ledger_ids
        if not ids:
            continue
        scanned += 1
        kinds = classify_evidence(path, text)
        if not kinds:
            continue
        for uid in ids:
            for kind in kinds:
                evidence[uid][kind].add(rel)
    meta = {
        "evidence_files_with_ledger_ids": scanned,
        "skipped_large_files": skipped_large,
        "read_errors": errors[:100],
        "scope": "committed_git_evidence_only",
    }
    return evidence, meta


def main() -> int:
    generated_at = now_utc()
    ledger = load_csv(LEDGER)
    crosswalk = load_csv(CROSSWALK)
    enriched, source_sha = load_enriched_source()

    if len(ledger) != EXPECTED_LEDGER_ROWS:
        raise RuntimeError(f"ledger rows: {len(ledger)} != {EXPECTED_LEDGER_ROWS}")
    ids = [(row.get("Source_ID") or "").strip().lower() for row in ledger]
    if len(set(ids)) != EXPECTED_LEDGER_ROWS or "" in ids:
        raise RuntimeError("ledger UUID uniqueness/blank invariant failed")
    if len(crosswalk) != EXPECTED_CURATED_ROWS:
        raise RuntimeError(f"crosswalk rows: {len(crosswalk)} != {EXPECTED_CURATED_ROWS}")

    by_curated_row = {int(row["curated_row"]): row for row in crosswalk}
    enriched_by_id: dict[str, dict[str, Any]] = {}
    overlay_source_rows: list[dict[str, Any]] = []
    for index, record in enumerate(enriched, 1):
        cross = by_curated_row[index]
        resolved = (cross.get("resolved_uuid") or record.get("session_id_from_url") or "").strip().lower()
        if not resolved:
            raise RuntimeError(f"curated row {index} has no resolved UUID")
        combined = dict(record)
        combined["curated_row"] = index
        combined["resolved_uuid"] = resolved
        combined["crosswalk_relationship"] = cross.get("relationship", "")
        combined["crosswalk_review_status"] = cross.get("review_status", "")
        combined["crosswalk_match_method"] = cross.get("match_method", "")
        enriched_by_id[resolved] = combined
        overlay_source_rows.append(combined)

    if len(enriched_by_id) != EXPECTED_CURATED_ROWS:
        raise RuntimeError("curated resolved UUIDs are not unique")

    ledger_ids = set(ids)
    evidence, evidence_meta = audit_evidence(ledger_ids)
    overlay_rows: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
    coverage_counts = Counter()

    curated_fields = [
        "curated_row", "title", "batch_id", "provisional_category", "project_tags",
        "primary_project", "related_projects", "relation_to_yos", "classification_confidence",
        "main_subject", "raw_preservation_status", "verbatim_preservation_status",
        "fact_sheet_status", "open_tasks_status", "issues_status", "decisions_status",
        "artifact_links_status", "commit_verification_status", "canon_status",
        "crosswalk_relationship", "crosswalk_review_status", "crosswalk_match_method",
    ]

    for row in ledger:
        uid = row["Source_ID"].strip().lower()
        curated = enriched_by_id.get(uid)
        out = dict(row)
        out["curated_239_member"] = bool(curated)
        for field in curated_fields:
            value = curated.get(field, "") if curated else ""
            if isinstance(value, list):
                value = "; ".join(str(item) for item in value)
            out[f"curated_{field}"] = value
        out["canon_promoted"] = False
        overlay_rows.append(out)

        ev = evidence[uid]
        flags = {kind: bool(paths) for kind, paths in ev.items()}
        for kind, present in flags.items():
            if present:
                coverage_counts[kind] += 1
        strict = all(flags.values())
        if strict:
            coverage_counts["strict_complete"] += 1
        coverage_rows.append({
            "source_id": uid,
            "title": row.get("Title", ""),
            "curated_239_member": bool(curated),
            "raw_body_present": flags["raw_body"],
            "verbatim_present": flags["verbatim"],
            "fact_sheet_present": flags["fact_sheet"],
            "summary_present": flags["summary"],
            "strict_complete_committed_git": strict,
            "raw_body_paths": "; ".join(sorted(ev["raw_body"])[:10]),
            "verbatim_paths": "; ".join(sorted(ev["verbatim"])[:10]),
            "fact_sheet_paths": "; ".join(sorted(ev["fact_sheet"])[:10]),
            "summary_paths": "; ".join(sorted(ev["summary"])[:10]),
            "canon_promoted": False,
        })

    overlay_fields = list(ledger[0].keys()) + ["curated_239_member"] + [f"curated_{f}" for f in curated_fields] + ["canon_promoted"]
    coverage_fields = list(coverage_rows[0].keys())
    write_csv(OUT / "CHATGPT-3060-CURATED-239-OVERLAY.csv", overlay_rows, overlay_fields)
    write_csv(OUT / "CHATGPT-3060-CONTENT-COVERAGE.csv", coverage_rows, coverage_fields)
    write_json(OUT / "CHATGPT-239-ENRICHED-RESOLVED.json", overlay_source_rows)

    ledger_sha = sha256_bytes(LEDGER.read_bytes())
    validation = {
        "generated_at": generated_at,
        "status": "complete_audit_with_external_sources_out_of_scope",
        "ledger_rows": len(ledger),
        "ledger_unique_ids": len(ledger_ids),
        "ledger_sha256": ledger_sha,
        "curated_source_rows": len(enriched),
        "curated_resolved_unique_ids": len(enriched_by_id),
        "curated_ids_present_in_ledger": len(set(enriched_by_id) & ledger_ids),
        "curated_ids_absent_from_ledger": sorted(set(enriched_by_id) - ledger_ids),
        "enriched_source_sha256": source_sha,
        "coverage_counts": dict(coverage_counts),
        "coverage_scope": evidence_meta,
        "canon_promotions": 0,
        "validation_passed": len(ledger) == 3060 and len(enriched_by_id) == 239,
    }
    write_json(OUT / "CHATGPT-OVERNIGHT-PHASES-1-2-VALIDATION.json", validation)

    status = f"""---
document_id: CHATGPT-OVERNIGHT-PHASES-1-2-STATUS
status: complete_with_scope_boundary
generated_at: {generated_at}
canon_promotions: 0
---

# ChatGPT overnight phases 1-2

## Phase 1 — curated overlay

- Native ledger rows: **{len(ledger)}**
- Enriched curated identities: **{len(enriched_by_id)}**
- Curated identities present in ledger: **{len(set(enriched_by_id) & ledger_ids)}**
- Known curated ledger absences: **{len(set(enriched_by_id) - ledger_ids)}**
- Native ledger rewritten: **no**

## Phase 2 — content coverage audit

This audit grades every one of the 3,060 ledger identities against **committed Git evidence**.
Library, Drive and live ChatGPT bodies are not silently counted as acquired when their bytes are not committed.

| Evidence layer | IDs with evidence |
|---|---:|
| Raw body | {coverage_counts['raw_body']} |
| Verbatim | {coverage_counts['verbatim']} |
| Fact Sheet | {coverage_counts['fact_sheet']} |
| Summary | {coverage_counts['summary']} |
| Strict complete in committed Git | {coverage_counts['strict_complete']} |

The detailed 3,060-row matrix is `CHATGPT-3060-CONTENT-COVERAGE.csv`.
No automated result is Canon.
"""
    (OUT / "CHATGPT-OVERNIGHT-PHASES-1-2-STATUS.md").write_text(status, encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0 if validation["validation_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
