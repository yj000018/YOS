#!/usr/bin/env python3
"""
context_pack_checksum_verifier.py — yOS Continuity Core Phase 1
Compute and verify Context Pack SHA-256 checksum.

IMPORTANT: Runtime/script verification is AUTHORITATIVE.
LLM self-reporting of checksum validity is declarative only and NOT authoritative.

Usage:
  python3 context_pack_checksum_verifier.py --pack PATH [--compute-only]
  python3 context_pack_checksum_verifier.py --pack PATH --verify
"""

import re
import sys
import json
import hashlib
import argparse
from pathlib import Path


CHECKSUM_FIELD = "pack_checksum"
CHECKSUM_EXCLUDE_PATTERN = re.compile(r"^pack_checksum:.*$", re.MULTILINE)


def canonicalize_pack_content(content: str) -> str:
    """
    Produce canonical serialization for checksum computation.
    Strips the pack_checksum field itself to avoid circular dependency.
    Normalizes line endings.
    """
    # Remove existing checksum field line
    canonical = CHECKSUM_EXCLUDE_PATTERN.sub("pack_checksum: <EXCLUDED_FOR_CHECKSUM>", content)
    # Normalize line endings
    canonical = canonical.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing whitespace per line
    canonical = "\n".join(line.rstrip() for line in canonical.split("\n"))
    return canonical


def compute_pack_checksum(pack_path: Path) -> str:
    """Compute SHA-256 checksum of canonical pack content."""
    content = pack_path.read_text(encoding="utf-8")
    canonical = canonicalize_pack_content(content)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compute_checksum_from_string(content: str) -> str:
    """Compute SHA-256 checksum from string content."""
    canonical = canonicalize_pack_content(content)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_pack_checksum(pack_path: Path) -> dict:
    """
    Verify pack checksum against stored pack_checksum field.
    Returns verification result dict.
    Runtime/script result is AUTHORITATIVE.
    """
    content = pack_path.read_text(encoding="utf-8")

    # Extract stored checksum
    stored_match = re.search(r"pack_checksum:\s*['\"]?([a-f0-9]{64})['\"]?", content)
    if not stored_match:
        return {
            "verified": False,
            "severity": "blocking",
            "action": "blocking",
            "computed_checksum": compute_pack_checksum(pack_path),
            "stored_checksum": None,
            "authoritative": True,
            "message": "pack_checksum field missing or malformed — cannot verify integrity"
        }

    stored_checksum = stored_match.group(1).strip()
    computed_checksum = compute_pack_checksum(pack_path)
    match = computed_checksum == stored_checksum

    return {
        "verified": match,
        "severity": "ok" if match else "blocking",
        "action": "proceed" if match else "blocking",
        "computed_checksum": computed_checksum,
        "stored_checksum": stored_checksum,
        "authoritative": True,
        "message": (
            "Checksum verified — pack integrity confirmed. (Runtime/script verification is authoritative.)"
            if match else
            f"CHECKSUM MISMATCH — pack may have been modified. "
            f"Computed: {computed_checksum[:16]}... Stored: {stored_checksum[:16]}... "
            "(Runtime/script verification is authoritative — LLM acknowledgment is declarative only.)"
        )
    }


def main():
    parser = argparse.ArgumentParser(description="yOS Context Pack Checksum Verifier")
    parser.add_argument("--pack", type=Path, required=True, help="Path to context pack file")
    parser.add_argument("--compute-only", action="store_true", help="Only compute and print checksum")
    parser.add_argument("--verify", action="store_true", help="Verify stored checksum")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.pack.exists():
        print(f"[ERROR] Pack file not found: {args.pack}", file=sys.stderr)
        sys.exit(1)

    if args.compute_only:
        checksum = compute_pack_checksum(args.pack)
        if args.json:
            print(json.dumps({"computed_checksum": checksum}))
        else:
            print(f"Computed SHA-256: {checksum}")
        return

    result = verify_pack_checksum(args.pack)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Verified:         {result['verified']}")
        print(f"Severity:         {result['severity']}")
        print(f"Action:           {result['action']}")
        print(f"Computed:         {result['computed_checksum']}")
        print(f"Stored:           {result['stored_checksum']}")
        print(f"Authoritative:    {result['authoritative']} (runtime/script — not LLM)")
        print(f"Message:          {result['message']}")

    if not result["verified"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
