#!/usr/bin/env python3
"""
Output Validator v1 — Y-OS
ADR-0044

Validates worker output artifacts before registration.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import re
import json

# Patterns that indicate secret leakage
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",           # OpenAI key
    r"sk-ant-[A-Za-z0-9\-]{20,}",     # Anthropic key
    r"ghp_[A-Za-z0-9]{36}",           # GitHub PAT
    r"AKIA[A-Z0-9]{16}",              # AWS key
    r"Bearer [A-Za-z0-9\-._~+/]{20,}",# Bearer token
]

# Patterns that indicate raw session history injection
SESSION_HISTORY_PATTERNS = [
    r"<compacted_history>",
    r"<shell action=",
    r"<file action=",
    r"\[TOOL_RESULT_RECEIVED\]",
    r"__TOOL_RESULT_RECEIVED__",
]


@dataclass
class ValidationResult:
    artifact_id: str
    verdict: str           # VALID | VALID_WITH_WARNING | INVALID_RETRYABLE | INVALID_BLOCKED
    passed: bool
    checks: dict[str, str]  # check_name → PASS/FAIL/WARN
    warnings: list[str]
    blocking_reasons: list[str]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_markdown(self) -> str:
        verdict_emoji = {
            "VALID": "✅",
            "VALID_WITH_WARNING": "⚠️",
            "INVALID_RETRYABLE": "🔄",
            "INVALID_BLOCKED": "❌",
        }.get(self.verdict, "?")
        lines = [
            f"---",
            f"id: yos-validation-{self.artifact_id.lower()}",
            f"title: Validation — {self.artifact_id}",
            f"type: validation_report",
            f"artifact_id: {self.artifact_id}",
            f"verdict: {self.verdict}",
            f"passed: {str(self.passed).lower()}",
            f"timestamp: '{self.timestamp}'",
            f"tags: ['#validation', '#yos']",
            f"---",
            f"",
            f"# Validation Report — {self.artifact_id}",
            f"",
            f"**Verdict:** {verdict_emoji} {self.verdict}  ",
            f"**Passed:** {'YES' if self.passed else 'NO'}",
            f"",
            f"## Checks",
            f"",
        ]
        for check, result in self.checks.items():
            emoji = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}.get(result, "?")
            lines.append(f"- {emoji} **{check}:** {result}")
        lines.append("")
        if self.blocking_reasons:
            lines.append("## ❌ Blocking Reasons")
            lines.append("")
            for r in self.blocking_reasons:
                lines.append(f"- {r}")
            lines.append("")
        if self.warnings:
            lines.append("## ⚠️ Warnings")
            lines.append("")
            for w in self.warnings:
                lines.append(f"- {w}")
            lines.append("")
        lines.append("---")
        lines.append("*Output Validator v1 — Y-OS*")
        return "\n".join(lines)


class OutputValidator:
    """Validates worker output artifacts."""

    def validate(
        self,
        artifact_id: str,
        content: str,
        artifact_type: str,
        lineage: Optional[dict] = None,
        provider: str = "",
        model: str = "",
        context_pack_id: str = "",
    ) -> ValidationResult:
        checks = {}
        warnings = []
        blocking = []

        # 1. Non-empty output
        if content and len(content.strip()) > 50:
            checks["non_empty_output"] = "PASS"
        elif content and len(content.strip()) > 0:
            checks["non_empty_output"] = "WARN"
            warnings.append("Output is very short (< 50 chars) — may be incomplete.")
        else:
            checks["non_empty_output"] = "FAIL"
            blocking.append("Output is empty.")

        # 2. Artifact type matches expected
        valid_types = {
            "Worker Output", "Governance Review", "Learning Report",
            "CEO Briefing", "Execution Trace", "Architecture Note",
            "Implementation Checklist", "Learning Synthesis",
        }
        if artifact_type in valid_types:
            checks["artifact_type_valid"] = "PASS"
        else:
            checks["artifact_type_valid"] = "WARN"
            warnings.append(f"Artifact type '{artifact_type}' not in standard set.")

        # 3. Lineage exists
        if lineage and lineage.get("source_context_pack"):
            checks["lineage_exists"] = "PASS"
        elif lineage:
            checks["lineage_exists"] = "WARN"
            warnings.append("Lineage exists but source_context_pack missing.")
        else:
            checks["lineage_exists"] = "FAIL"
            blocking.append("No lineage recorded — Article III violation.")

        # 4. No secret leakage
        secret_found = False
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, content):
                secret_found = True
                break
        if not secret_found:
            checks["no_secret_leakage"] = "PASS"
        else:
            checks["no_secret_leakage"] = "FAIL"
            blocking.append("CRITICAL: Secret pattern detected in output — BLOCKED.")

        # 5. No raw session history
        history_found = False
        for pattern in SESSION_HISTORY_PATTERNS:
            if re.search(pattern, content):
                history_found = True
                break
        if not history_found:
            checks["no_raw_session_history"] = "PASS"
        else:
            checks["no_raw_session_history"] = "FAIL"
            blocking.append("CRITICAL: Raw session history pattern detected — Article II violation.")

        # 6. Provider/model metadata
        if provider and model:
            checks["provider_model_metadata"] = "PASS"
        elif provider or model:
            checks["provider_model_metadata"] = "WARN"
            warnings.append("Partial provider/model metadata.")
        else:
            checks["provider_model_metadata"] = "FAIL"
            blocking.append("No provider/model metadata — traceability missing.")

        # 7. Constitutional compliance basics
        # Check for artifact-like structure (has a title or heading)
        if re.search(r"^#\s+.+", content, re.MULTILINE) or re.search(r"^title:", content, re.MULTILINE):
            checks["artifact_structure"] = "PASS"
        else:
            checks["artifact_structure"] = "WARN"
            warnings.append("Output lacks artifact structure (no title/heading).")

        # 8. Context pack reference
        if context_pack_id and context_pack_id in content:
            checks["context_pack_reference"] = "PASS"
        elif context_pack_id:
            checks["context_pack_reference"] = "WARN"
            warnings.append(f"Context Pack ID '{context_pack_id}' not found in output.")
        else:
            checks["context_pack_reference"] = "WARN"
            warnings.append("No context_pack_id provided for reference check.")

        # Verdict
        if blocking:
            if any("CRITICAL" in r for r in blocking):
                verdict = "INVALID_BLOCKED"
                passed = False
            else:
                verdict = "INVALID_RETRYABLE"
                passed = False
        elif warnings:
            verdict = "VALID_WITH_WARNING"
            passed = True
        else:
            verdict = "VALID"
            passed = True

        return ValidationResult(
            artifact_id=artifact_id,
            verdict=verdict,
            passed=passed,
            checks=checks,
            warnings=warnings,
            blocking_reasons=blocking,
        )
