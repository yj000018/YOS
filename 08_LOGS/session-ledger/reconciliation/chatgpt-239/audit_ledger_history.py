#!/usr/bin/env python3
"""Audit every Git-reachable version of the YOS master session ledger.

The 3,060 ChatGPT ingestion was reported operationally. This script proves
whether any corresponding ledger blob was durably committed to Git. It scans
all blob versions reachable from all refs, counts source rows, and records
commits/refs containing each blob. No data mutation or Canon promotion.
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "generated"
LEDGER_PATH = "08_LOGS/session-ledger/data/master_ledger.csv"
CLAIM_COMMIT = "ac472da1864f338c9ac36209ed02becd1d96d4f5"


def git(*args: str, binary: bool = False):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args],
        stderr=subprocess.DEVNULL,
        text=not binary,
    )


def commits_for_blob(blob: str) -> list[str]:
    commits: list[str] = []
    for commit in git("rev-list", "--all", "--", LEDGER_PATH).splitlines():
        try:
            current = git("rev-parse", f"{commit}:{LEDGER_PATH}").strip()
        except subprocess.CalledProcessError:
            continue
        if current == blob:
            commits.append(commit)
    return commits


def refs_containing(commit: str) -> list[str]:
    if not commit:
        return []
    output = git("for-each-ref", "--format=%(refname:short)", "--contains", commit)
    return sorted(line for line in output.splitlines() if line)


def main() -> int:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    object_lines = git("rev-list", "--all", "--objects", "--", LEDGER_PATH).splitlines()
    blobs: set[str] = set()
    for line in object_lines:
        parts = line.split(" ", 1)
        if len(parts) == 2 and parts[1] == LEDGER_PATH:
            obj = parts[0]
            try:
                kind = git("cat-file", "-t", obj).strip()
            except subprocess.CalledProcessError:
                continue
            if kind == "blob":
                blobs.add(obj)

    versions = []
    for blob in sorted(blobs):
        raw = git("cat-file", "blob", blob, binary=True)
        text = raw.decode("utf-8-sig", errors="replace")
        rows = list(csv.DictReader(io.StringIO(text)))
        sources = Counter((row.get("Source") or "").strip() or "<blank>" for row in rows)
        chatgpt_ids = [
            (row.get("Source_ID") or "").strip()
            for row in rows
            if (row.get("Source") or "").strip().lower() == "chatgpt"
        ]
        commits = commits_for_blob(blob)
        versions.append({
            "blob_sha": blob,
            "byte_count": len(raw),
            "row_count": len(rows),
            "source_counts": dict(sorted(sources.items())),
            "chatgpt_rows": len(chatgpt_ids),
            "chatgpt_unique_ids": len({value for value in chatgpt_ids if value}),
            "first_commit": commits[-1] if commits else "",
            "latest_commit": commits[0] if commits else "",
            "commit_count": len(commits),
            "refs_containing_latest_commit": refs_containing(commits[0]) if commits else [],
        })

    versions.sort(key=lambda item: (item["row_count"], item["blob_sha"]))
    max_chatgpt = max((item["chatgpt_rows"] for item in versions), default=0)
    max_rows = max((item["row_count"] for item in versions), default=0)
    claim_parent = git("rev-parse", f"{CLAIM_COMMIT}^").strip()
    claim_blob = ""
    parent_blob = ""
    for commit, key in ((CLAIM_COMMIT, "claim"), (claim_parent, "parent")):
        try:
            value = git("rev-parse", f"{commit}:{LEDGER_PATH}").strip()
        except subprocess.CalledProcessError:
            value = ""
        if key == "claim":
            claim_blob = value
        else:
            parent_blob = value

    report = {
        "generated_at": generated,
        "ledger_path": LEDGER_PATH,
        "reachable_blob_versions": len(versions),
        "maximum_total_rows_in_any_git_blob": max_rows,
        "maximum_chatgpt_rows_in_any_git_blob": max_chatgpt,
        "durable_3060_chatgpt_ledger_present": max_chatgpt >= 3060,
        "ingestion_claim_commit": CLAIM_COMMIT,
        "ingestion_claim_parent": claim_parent,
        "claim_commit_ledger_blob": claim_blob,
        "parent_commit_ledger_blob": parent_blob,
        "claim_commit_changed_ledger_blob": bool(claim_blob and parent_blob and claim_blob != parent_blob),
        "versions": versions,
        "canon_promotions": 0,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "CHATGPT-LEDGER-GIT-HISTORY-AUDIT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "---",
        "document_id: CHATGPT-LEDGER-GIT-HISTORY-AUDIT-v1.0",
        "document_type: evidence_audit",
        "status: active_evidence_not_canon",
        f"generated_at: {generated}",
        "canon_promotions: 0",
        "---",
        "",
        "# ChatGPT ledger Git-history audit",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Reachable ledger blob versions | {len(versions)} |",
        f"| Maximum total rows | {max_rows} |",
        f"| Maximum ChatGPT rows | {max_chatgpt} |",
        f"| Durable 3,060-row ChatGPT ledger present | {str(max_chatgpt >= 3060).lower()} |",
        f"| Claim commit changed ledger blob | {str(report['claim_commit_changed_ledger_blob']).lower()} |",
        "",
        "## Versions",
        "",
        "| Blob | Rows | ChatGPT | Sources | Latest commit |",
        "|---|---:|---:|---|---|",
    ]
    for item in versions:
        sources = ", ".join(f"{key}={value}" for key, value in item["source_counts"].items())
        lines.append(
            f"| `{item['blob_sha']}` | {item['row_count']} | {item['chatgpt_rows']} | "
            f"{sources} | `{item['latest_commit']}` |"
        )
    lines += [
        "",
        "The ingestion commit message is operational evidence, not proof that the generated ledger was committed.",
        "No missing rows are fabricated and no automated evidence is promoted to Canon.",
    ]
    (OUT / "CHATGPT-LEDGER-GIT-HISTORY-AUDIT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
