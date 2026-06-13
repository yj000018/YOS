#!/usr/bin/env python3
"""
Lakshmi Context Review v1 — Y-OS
ADR-0033 / ADR-0043

Evaluates every compiled Context Pack for governance compliance.
PASS if: verdict in APPROVE/APPROVE_WITH_WARNING AND score <= 55 AND blocking = 0.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import json


# ─── Review Criteria ──────────────────────────────────────────────────────────

@dataclass
class ReviewCriteria:
    source_artifact_coverage: float    # 0.0–1.0
    missing_context_risk: int          # 0–100
    omitted_context_risk: int          # 0–100
    constitutional_compliance: bool
    token_compression_risk: int        # 0–100 (high if budget exceeded)
    stale_context_risk: int            # 0–100
    lineage_integrity: bool
    raw_session_history_tokens: int    # MUST be 0


# ─── Review Result ────────────────────────────────────────────────────────────

@dataclass
class GovernanceReview:
    mission_id: str
    worker: str
    mode: str
    verdict: str                       # APPROVE | APPROVE_WITH_WARNING | REJECT
    risk_score: int                    # 0–100
    blocking_reasons: list[str]
    warnings: list[str]
    article_checks: dict[str, str]     # Article I–V → PASS/FAIL
    lineage_integrity_score: float     # 0.0–1.0
    raw_session_history_used: int      # MUST be 0
    passed: bool
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def to_markdown(self) -> str:
        verdict_emoji = {"APPROVE": "✅", "APPROVE_WITH_WARNING": "⚠️", "REJECT": "❌"}.get(self.verdict, "?")
        lines = [
            f"---",
            f"id: yos-gov-review-{self.mission_id.lower().replace('-','_')}-{self.worker.lower()}",
            f"title: Governance Review — {self.mission_id} / {self.worker}",
            f"type: governance_review",
            f"mission_id: {self.mission_id}",
            f"worker: {self.worker}",
            f"mode: {self.mode}",
            f"verdict: {self.verdict}",
            f"risk_score: {self.risk_score}",
            f"passed: {str(self.passed).lower()}",
            f"raw_session_history_used: {self.raw_session_history_used}",
            f"timestamp: '{self.timestamp}'",
            f"tags: ['#governance', '#lakshmi', '#yos']",
            f"---",
            f"",
            f"# Governance Review — {self.mission_id} / {self.worker}",
            f"",
            f"**Verdict:** {verdict_emoji} {self.verdict}  ",
            f"**Risk Score:** {self.risk_score}/100  ",
            f"**Passed:** {'YES' if self.passed else 'NO'}  ",
            f"**Raw Session History:** {self.raw_session_history_used} tokens (BLOCKED)",
            f"",
            f"---",
            f"",
            f"## Constitutional Article Checks",
            f"",
        ]
        for article, result in self.article_checks.items():
            emoji = "✅" if result == "PASS" else "❌"
            lines.append(f"- {emoji} **{article}:** {result}")
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

        lines += [
            f"## Lineage Integrity",
            f"",
            f"Score: {self.lineage_integrity_score:.1%}",
            f"",
            f"---",
            f"*Reviewed by Lakshmi Context Review v1 — Y-OS*",
        ]
        return "\n".join(lines)


# ─── Reviewer ─────────────────────────────────────────────────────────────────

class LakshmiContextReviewer:
    """Evaluates Context Packs for governance compliance (ADR-0033)."""

    def review(self, pack) -> GovernanceReview:
        """Review a compiled Context Pack."""
        blocking = []
        warnings = []
        score = 0

        # ── Hard constraint: no raw session history ──────────────────────────
        if pack.raw_session_history_tokens > 0:
            blocking.append(
                f"CRITICAL: raw_session_history_tokens={pack.raw_session_history_tokens} > 0. "
                f"Article I violation — raw history must never be injected."
            )
            score += 50

        # ── Article I: Artifact Primacy ──────────────────────────────────────
        art1 = "PASS"
        if not pack.source_manifest:
            art1 = "FAIL"
            blocking.append("Article I: No source artifacts in manifest.")
            score += 20
        elif len(pack.source_manifest) < 2:
            warnings.append("Article I: Only 1 source artifact — consider enriching context.")
            score += 5

        # ── Article II: Preservation Principle ──────────────────────────────
        art2 = "PASS"
        if pack.raw_session_history_tokens > 0:
            art2 = "FAIL"
            score += 20
        elif pack.omitted_context:
            warnings.append(f"Article II: {len(pack.omitted_context)} context items omitted — check budget.")
            score += 3

        # ── Article III: Derivation Transparency ────────────────────────────
        art3 = "PASS"
        if not pack.lineage:
            art3 = "FAIL"
            blocking.append("Article III: No lineage recorded — derivation not transparent.")
            score += 15
        elif len(pack.lineage) < 2:
            warnings.append("Article III: Lineage sparse — add more derivation steps.")
            score += 5

        # ── Article IV: Human Override ───────────────────────────────────────
        art4 = "PASS"
        # Always passes unless explicitly overridden
        if pack.mode == "MODE-E" and not pack.missing_context:
            pass  # Full context available — human override not needed
        elif pack.missing_context:
            warnings.append(f"Article IV: {len(pack.missing_context)} missing context items — human review recommended.")
            score += 5

        # ── Article V: Governance Before Autonomy ────────────────────────────
        art5 = "PASS"
        if pack.mode in ("MODE-D", "MODE-E") and not pack.lineage:
            art5 = "FAIL"
            blocking.append("Article V: MODE-D/E requires governance lineage.")
            score += 10

        # ── Missing context risk ─────────────────────────────────────────────
        if pack.missing_context:
            missing_risk = min(len(pack.missing_context) * 10, 30)
            score += missing_risk
            if missing_risk > 20:
                warnings.append(f"Missing context risk: {missing_risk}/30 — {len(pack.missing_context)} items missing.")

        # ── Token compression risk ───────────────────────────────────────────
        if pack.compression_mode == "aggressive":
            score += 8
            warnings.append("Token compression: aggressive mode — context may be incomplete.")

        # ── Lineage integrity score ──────────────────────────────────────────
        lineage_score = min(len(pack.lineage) / 5.0, 1.0)

        # ── Verdict ──────────────────────────────────────────────────────────
        if blocking:
            verdict = "REJECT"
            passed = False
        elif score <= 35:
            verdict = "APPROVE"
            passed = True
        elif score <= 55:
            verdict = "APPROVE_WITH_WARNING"
            passed = True
        else:
            verdict = "REJECT"
            passed = False

        return GovernanceReview(
            mission_id=pack.mission_id,
            worker=pack.worker,
            mode=pack.mode,
            verdict=verdict,
            risk_score=score,
            blocking_reasons=blocking,
            warnings=warnings,
            article_checks={
                "Article I — Artifact Primacy": art1,
                "Article II — Preservation Principle": art2,
                "Article III — Derivation Transparency": art3,
                "Article IV — Human Override": art4,
                "Article V — Governance Before Autonomy": art5,
            },
            lineage_integrity_score=lineage_score,
            raw_session_history_used=pack.raw_session_history_tokens,
            passed=passed,
        )


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from context_compiler_v2 import ContextCompilerV2, CompilationRequest

    compiler = ContextCompilerV2()
    reviewer = LakshmiContextReviewer()

    req = CompilationRequest(
        mission_id="MISSION-016-TEST",
        worker="Brahma",
        capability="architecture",
        mode="MODE-D",
        relevant_adrs=["ADR-0037"],
        canonical_memory="Y-OS canonical memory: CCR Runtime v2 with MODE-B/D/E.",
    )
    pack = compiler.compile(req)
    review = reviewer.review(pack)
    print(f"Verdict: {review.verdict} | Score: {review.risk_score} | Passed: {review.passed}")
