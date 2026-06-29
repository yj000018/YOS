#!/usr/bin/env python3
"""
cap_validator.py — yOS Continuity Core Phase 1
Constraint Acknowledgment Protocol (CAP) validator.

CAP is a handoff validation rule:
  - LLM acknowledgment is DECLARATIVE only (not authoritative)
  - Runtime/script verification is AUTHORITATIVE
  - Blocking enforcement: missing CAP = hard_stop before execution

CAP Fields required in a Context Pack:
  cap_acknowledged: true
  cap_acknowledged_by: <llm_id>
  cap_acknowledged_at: <ISO8601>
  cap_constraints_hash: <sha256 of constraints block>

Usage:
  python3 cap_validator.py --pack PATH
  python3 cap_validator.py --pack PATH --constraints-path PATH
"""

import re
import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

CAP_REQUIRED_FIELDS = [
    "cap_acknowledged",
    "cap_acknowledged_by",
    "cap_acknowledged_at",
    "cap_constraints_hash"
]

CAP_MAX_AGE_HOURS = 24  # CAP acknowledgment expires after 24h


def extract_cap_fields(content: str) -> dict:
    """Extract CAP fields from pack content."""
    fields = {}
    for field in CAP_REQUIRED_FIELDS:
        match = re.search(rf"{field}:\s*['\"]?([^\n'\"]+)['\"]?", content)
        if match:
            fields[field] = match.group(1).strip()
    return fields


def compute_constraints_hash(constraints_text: str) -> str:
    """Compute SHA-256 of constraints block."""
    normalized = constraints_text.strip().replace("\r\n", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate_cap(pack_path: Path, constraints_path: Path = None) -> dict:
    """
    Validate CAP fields in a Context Pack.
    Returns validation result dict.
    Runtime/script result is AUTHORITATIVE.
    LLM cap_acknowledged is DECLARATIVE only.
    """
    content = pack_path.read_text(encoding="utf-8")
    cap_fields = extract_cap_fields(content)

    result = {
        "cap_valid": False,
        "severity": None,
        "action": None,
        "missing_fields": [],
        "cap_acknowledged": False,
        "cap_acknowledged_by": None,
        "cap_acknowledged_at": None,
        "cap_age_hours": None,
        "cap_expired": False,
        "constraints_hash_match": None,
        "authoritative": True,
        "note": "Runtime/script verification is authoritative. LLM acknowledgment is declarative only.",
        "violations": []
    }

    # Check missing fields
    missing = [f for f in CAP_REQUIRED_FIELDS if f not in cap_fields]
    result["missing_fields"] = missing

    if missing:
        result["severity"] = "hard_stop"
        result["action"] = "hard_stop"
        result["violations"].append(f"Missing CAP fields: {missing}")
        return result

    # Check cap_acknowledged = true
    ack_val = cap_fields.get("cap_acknowledged", "").lower()
    if ack_val not in ("true", "yes", "1"):
        result["cap_acknowledged"] = False
        result["severity"] = "hard_stop"
        result["action"] = "hard_stop"
        result["violations"].append(f"cap_acknowledged='{ack_val}' — must be true")
        return result

    result["cap_acknowledged"] = True
    result["cap_acknowledged_by"] = cap_fields.get("cap_acknowledged_by")

    # Check CAP age
    ack_at = cap_fields.get("cap_acknowledged_at", "")
    try:
        ts = datetime.fromisoformat(ack_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_hours = (now - ts).total_seconds() / 3600
        result["cap_acknowledged_at"] = ack_at
        result["cap_age_hours"] = round(age_hours, 2)
        if age_hours > CAP_MAX_AGE_HOURS:
            result["cap_expired"] = True
            result["severity"] = "blocking"
            result["action"] = "blocking"
            result["violations"].append(
                f"CAP acknowledgment expired: {round(age_hours, 1)}h old (max {CAP_MAX_AGE_HOURS}h)"
            )
    except (ValueError, AttributeError):
        result["violations"].append(f"Cannot parse cap_acknowledged_at: '{ack_at}'")
        result["severity"] = "blocking"
        result["action"] = "blocking"

    # Verify constraints hash if constraints_path provided
    if constraints_path and constraints_path.exists():
        constraints_text = constraints_path.read_text(encoding="utf-8")
        computed_hash = compute_constraints_hash(constraints_text)
        stored_hash = cap_fields.get("cap_constraints_hash", "")
        hash_match = computed_hash == stored_hash
        result["constraints_hash_match"] = hash_match
        if not hash_match:
            result["violations"].append(
                f"Constraints hash mismatch — constraints may have changed since CAP was issued. "
                f"Computed: {computed_hash[:16]}... Stored: {stored_hash[:16]}..."
            )
            if result["severity"] not in ("hard_stop",):
                result["severity"] = "blocking"
                result["action"] = "blocking"
    else:
        result["constraints_hash_match"] = None  # Cannot verify without constraints file

    if not result["violations"] and not result.get("cap_expired"):
        result["cap_valid"] = True
        result["severity"] = "ok"
        result["action"] = "proceed"

    return result


def main():
    parser = argparse.ArgumentParser(description="yOS CAP Validator")
    parser.add_argument("--pack", type=Path, required=True)
    parser.add_argument("--constraints-path", type=Path, help="Path to constraints file for hash verification")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.pack.exists():
        print(f"[ERROR] Pack not found: {args.pack}", file=sys.stderr)
        sys.exit(1)

    result = validate_cap(args.pack, args.constraints_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"CAP Valid:              {result['cap_valid']}")
        print(f"Severity:               {result['severity']}")
        print(f"Action:                 {result['action']}")
        print(f"Acknowledged:           {result['cap_acknowledged']}")
        print(f"Acknowledged By:        {result['cap_acknowledged_by']}")
        print(f"CAP Age (hours):        {result['cap_age_hours']}")
        print(f"CAP Expired:            {result['cap_expired']}")
        print(f"Constraints Hash Match: {result['constraints_hash_match']}")
        print(f"Note:                   {result['note']}")
        if result["violations"]:
            print("Violations:")
            for v in result["violations"]:
                print(f"  - {v}")

    if not result["cap_valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
