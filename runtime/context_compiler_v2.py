#!/usr/bin/env python3
"""
Context Compiler v2 — Y-OS
ADR-0043

Compiles a Context Pack artifact from structured sources.
No raw session history is ever included.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json
import re


# ─── Compilation Request ──────────────────────────────────────────────────────

@dataclass
class CompilationRequest:
    mission_id: str
    worker: str
    capability: str
    mode: str                            # MODE-B | MODE-D | MODE-E
    parent_artifacts: list[str] = field(default_factory=list)
    relevant_adrs: list[str] = field(default_factory=list)
    relevant_concepts: list[str] = field(default_factory=list)
    relevant_missions: list[str] = field(default_factory=list)
    session_delta: Optional[str] = None  # Only for MODE-E
    canonical_memory: Optional[str] = None  # For MODE-D/E
    token_budget: int = 8000


# ─── Context Pack Artifact ────────────────────────────────────────────────────

@dataclass
class ContextPack:
    mission_id: str
    worker: str
    capability: str
    mode: str
    content: str
    source_manifest: list[str]
    omitted_context: list[str]
    missing_context: list[str]
    compression_mode: str
    lineage: list[str]
    token_estimate: int
    raw_session_history_tokens: int = 0  # MUST always be 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_markdown(self) -> str:
        lines = [
            f"---",
            f"id: yos-context-pack-{self.mission_id.lower().replace('-','_')}-{self.worker.lower()}",
            f"title: Context Pack — {self.mission_id} / {self.worker}",
            f"type: context_pack",
            f"mission_id: {self.mission_id}",
            f"worker: {self.worker}",
            f"capability: {self.capability}",
            f"mode: {self.mode}",
            f"token_estimate: {self.token_estimate}",
            f"raw_session_history_tokens: {self.raw_session_history_tokens}",
            f"timestamp: '{self.timestamp}'",
            f"tags: ['#context-pack', '#yos', '#{self.mode.lower()}']",
            f"---",
            f"",
            f"# Context Pack — {self.mission_id} / {self.worker} ({self.mode})",
            f"",
            f"**Worker:** {self.worker}  ",
            f"**Capability:** {self.capability}  ",
            f"**Mode:** {self.mode}  ",
            f"**Token Estimate:** {self.token_estimate}  ",
            f"**Raw Session History:** {self.raw_session_history_tokens} tokens (BLOCKED)",
            f"",
            f"---",
            f"",
            f"## Context Content",
            f"",
            self.content,
            f"",
            f"---",
            f"",
            f"## Source Manifest",
            f"",
        ]
        for src in self.source_manifest:
            lines.append(f"- {src}")
        lines.append("")

        if self.omitted_context:
            lines.append("## Omitted Context")
            lines.append("")
            for item in self.omitted_context:
                lines.append(f"- {item}")
            lines.append("")

        if self.missing_context:
            lines.append("## Missing Context Disclosure")
            lines.append("")
            for item in self.missing_context:
                lines.append(f"- ⚠️ {item}")
            lines.append("")

        lines += [
            f"## Lineage",
            f"",
        ]
        for l in self.lineage:
            lines.append(f"- {l}")
        lines.append("")
        lines.append(f"---")
        lines.append(f"*Compiled by Context Compiler v2 — Y-OS*")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ─── Context Compiler ─────────────────────────────────────────────────────────

class ContextCompilerV2:
    """Compiles Context Packs from structured sources."""

    CORPUS_ROOT = Path("/home/ubuntu/yreg")

    def compile(self, req: CompilationRequest) -> ContextPack:
        """Compile a Context Pack for the given request."""
        sections = []
        source_manifest = []
        omitted = []
        missing = []
        lineage = [
            f"Compiled by ContextCompilerV2 at {datetime.now(timezone.utc).isoformat()}",
            f"Mission: {req.mission_id}",
            f"Worker: {req.worker} / {req.capability}",
            f"Mode: {req.mode}",
            f"ADR-0043: CCR Runtime v2 Implementation",
        ]

        token_used = 0
        token_budget = req.token_budget

        # ── Worker Identity ──────────────────────────────────────────────────
        worker_identity = self._get_worker_identity(req.worker)
        sections.append(f"## Worker Identity\n\n{worker_identity}")
        token_used += len(worker_identity) // 4
        source_manifest.append(f"Worker identity: {req.worker} (built-in)")

        # ── Mission Context ──────────────────────────────────────────────────
        mission_ctx = f"**Mission:** {req.mission_id}\n**Capability:** {req.capability}\n**Mode:** {req.mode}"
        sections.append(f"## Mission Context\n\n{mission_ctx}")
        token_used += len(mission_ctx) // 4
        source_manifest.append(f"Mission context: {req.mission_id}")

        # ── Relevant ADRs ────────────────────────────────────────────────────
        if req.relevant_adrs:
            adr_content = self._load_adrs(req.relevant_adrs, token_budget - token_used)
            if adr_content["loaded"]:
                sections.append(f"## Relevant ADRs\n\n{adr_content['content']}")
                token_used += adr_content["tokens"]
                source_manifest.extend(adr_content["sources"])
            if adr_content["omitted"]:
                omitted.extend(adr_content["omitted"])

        # ── Relevant Concepts ────────────────────────────────────────────────
        if req.relevant_concepts:
            concept_content = self._load_concepts(req.relevant_concepts, token_budget - token_used)
            if concept_content["loaded"]:
                sections.append(f"## Relevant Concepts\n\n{concept_content['content']}")
                token_used += concept_content["tokens"]
                source_manifest.extend(concept_content["sources"])
            if concept_content["omitted"]:
                omitted.extend(concept_content["omitted"])

        # ── Relevant Missions ────────────────────────────────────────────────
        if req.relevant_missions:
            mission_refs = "\n".join(f"- [[{m}]]" for m in req.relevant_missions)
            sections.append(f"## Related Missions\n\n{mission_refs}")
            token_used += len(mission_refs) // 4
            source_manifest.append(f"Mission references: {', '.join(req.relevant_missions)}")

        # ── Canonical Memory (MODE-D/E) ──────────────────────────────────────
        if req.mode in ("MODE-D", "MODE-E") and req.canonical_memory:
            budget_remaining = token_budget - token_used
            canon_truncated = req.canonical_memory[:budget_remaining * 4]
            sections.append(f"## Canonical Memory\n\n{canon_truncated}")
            token_used += len(canon_truncated) // 4
            source_manifest.append("Canonical Memory (LMP stage 6)")
            lineage.append("Canonical Memory included (MODE-D/E)")
        elif req.mode in ("MODE-D", "MODE-E") and not req.canonical_memory:
            missing.append("Canonical Memory not provided — MODE-D/E requires it")

        # ── Session Delta (MODE-E only) ──────────────────────────────────────
        if req.mode == "MODE-E" and req.session_delta:
            budget_remaining = token_budget - token_used
            delta_truncated = req.session_delta[:budget_remaining * 4]
            sections.append(f"## Session Delta\n\n{delta_truncated}")
            token_used += len(delta_truncated) // 4
            source_manifest.append("Session Delta (LMP stage 3)")
            lineage.append("Session Delta included (MODE-E)")
        elif req.mode == "MODE-E" and not req.session_delta:
            missing.append("Session Delta not provided — MODE-E requires it")

        # ── Parent Artifacts ─────────────────────────────────────────────────
        if req.parent_artifacts:
            parent_refs = "\n".join(f"- {a}" for a in req.parent_artifacts)
            sections.append(f"## Parent Artifacts\n\n{parent_refs}")
            source_manifest.extend(req.parent_artifacts)

        # ── Assemble ─────────────────────────────────────────────────────────
        content = "\n\n".join(sections)
        final_tokens = len(content) // 4

        return ContextPack(
            mission_id=req.mission_id,
            worker=req.worker,
            capability=req.capability,
            mode=req.mode,
            content=content,
            source_manifest=source_manifest,
            omitted_context=omitted,
            missing_context=missing,
            compression_mode="structural" if final_tokens < token_budget else "aggressive",
            lineage=lineage,
            token_estimate=final_tokens,
            raw_session_history_tokens=0,  # ALWAYS 0
        )

    def _get_worker_identity(self, worker: str) -> str:
        identities = {
            "Brahma": "Brahma — CTO. Responsible for architecture, technical design, ADRs, and system evolution. Works in MODE-D by default.",
            "Ganesha": "Ganesha — CEO. Responsible for strategy, decisions, governance, and constitutional oversight. Works in MODE-D.",
            "Lakshmi": "Lakshmi — CLO (Risk). Responsible for governance reviews, risk scoring, and constitutional compliance.",
            "Hanuman": "Hanuman — COO. Responsible for execution, build, deploy, and operational tasks. Works in MODE-B by default.",
            "Saraswati": "Saraswati — CLO (Learning). Responsible for knowledge synthesis, learning, and documentation.",
            "Krishna": "Krishna — CPO. Responsible for product strategy, features, and user experience.",
        }
        return identities.get(worker, f"{worker} — Y-OS worker. Role not defined in registry.")

    def _load_adrs(self, adr_ids: list[str], token_budget: int) -> dict:
        loaded = []
        sources = []
        omitted = []
        tokens = 0

        for adr_id in adr_ids:
            # Try to find the ADR file
            matches = list(self.CORPUS_ROOT.rglob(f"*{adr_id}*.md"))
            if not matches:
                omitted.append(f"{adr_id} — file not found in corpus")
                continue

            path = matches[0]
            content = path.read_text(errors="ignore")
            # Extract title and status only (not full content — token budget)
            title_match = re.search(r'^title:\s*[\'"]?(.+?)[\'"]?\s*$', content, re.MULTILINE)
            status_match = re.search(r'^status:\s*(\w+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else adr_id
            status = status_match.group(1) if status_match else "UNKNOWN"

            snippet = f"**[[{adr_id}]]** — {title} ({status})"
            snippet_tokens = len(snippet) // 4

            if tokens + snippet_tokens > token_budget:
                omitted.append(f"{adr_id} — omitted (token budget)")
                continue

            loaded.append(snippet)
            sources.append(f"{adr_id}: {path.relative_to(self.CORPUS_ROOT)}")
            tokens += snippet_tokens

        return {
            "loaded": loaded,
            "content": "\n".join(loaded),
            "sources": sources,
            "omitted": omitted,
            "tokens": tokens,
        }

    def _load_concepts(self, concept_ids: list[str], token_budget: int) -> dict:
        loaded = []
        sources = []
        omitted = []
        tokens = 0

        concepts_dir = self.CORPUS_ROOT / "concepts"
        for concept_id in concept_ids:
            path = concepts_dir / f"{concept_id}.md"
            if not path.exists():
                # Try fuzzy match
                matches = list(concepts_dir.glob(f"*{concept_id}*"))
                if not matches:
                    omitted.append(f"{concept_id} — concept file not found")
                    continue
                path = matches[0]

            content = path.read_text(errors="ignore")
            title_match = re.search(r'^title:\s*[\'"]?(.+?)[\'"]?\s*$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else concept_id

            snippet = f"**[[{concept_id}]]** — {title}"
            snippet_tokens = len(snippet) // 4

            if tokens + snippet_tokens > token_budget:
                omitted.append(f"{concept_id} — omitted (token budget)")
                continue

            loaded.append(snippet)
            sources.append(f"concepts/{path.name}")
            tokens += snippet_tokens

        return {
            "loaded": loaded,
            "content": "\n".join(loaded),
            "sources": sources,
            "omitted": omitted,
            "tokens": tokens,
        }


if __name__ == "__main__":
    compiler = ContextCompilerV2()
    req = CompilationRequest(
        mission_id="MISSION-016-TEST",
        worker="Brahma",
        capability="architecture",
        mode="MODE-D",
        relevant_adrs=["ADR-0037", "ADR-0043"],
        relevant_concepts=["CCR_Runtime", "Artifact_Primacy"],
        canonical_memory="Y-OS canonical memory: ADR-0037 defines CCR Runtime v2 with MODE-B/D/E.",
    )
    pack = compiler.compile(req)
    print(f"Context Pack compiled: {pack.token_estimate} tokens, mode={pack.mode}")
    print(f"Raw session history: {pack.raw_session_history_tokens}")
    print(f"Sources: {len(pack.source_manifest)}")
