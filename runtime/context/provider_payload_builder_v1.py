#!/usr/bin/env python3
"""
Provider Payload Builder v1 — Y-OS
ADR-0043

Converts a Context Pack into provider-ready payloads.
Supports: OpenAI, Anthropic, Manus Runtime.
Does NOT call providers — compilation only.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import json

# Import ContextPack type (avoid circular)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from context_compiler_v2 import ContextPack


# ─── Payload Schemas ──────────────────────────────────────────────────────────

@dataclass
class OpenAIPayload:
    model: str
    messages: list[dict]
    max_tokens: int
    temperature: float = 0.2
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "metadata": self.metadata,
        }


@dataclass
class AnthropicPayload:
    model: str
    system: str
    messages: list[dict]
    max_tokens: int
    temperature: float = 0.2
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "system": self.system,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "metadata": self.metadata,
        }


@dataclass
class ManusPayload:
    worker: str
    capability: str
    mode: str
    context_pack_id: str
    context_content: str
    token_budget: int
    governance_required: bool
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CompiledPayload:
    mission_id: str
    worker: str
    mode: str
    provider: str
    payload: dict
    token_estimate: int
    raw_session_history_tokens: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_markdown(self) -> str:
        payload_json = json.dumps(self.payload, indent=2, ensure_ascii=False)
        return (
            f"---\n"
            f"id: yos-payload-{self.mission_id.lower().replace('-','_')}-{self.provider.lower()}\n"
            f"title: Provider Payload — {self.mission_id} / {self.provider}\n"
            f"type: compiled_payload\n"
            f"mission_id: {self.mission_id}\n"
            f"worker: {self.worker}\n"
            f"mode: {self.mode}\n"
            f"provider: {self.provider}\n"
            f"token_estimate: {self.token_estimate}\n"
            f"raw_session_history_tokens: {self.raw_session_history_tokens}\n"
            f"timestamp: '{self.timestamp}'\n"
            f"tags: ['#payload', '#yos', '#{self.provider.lower()}']\n"
            f"---\n\n"
            f"# Provider Payload — {self.mission_id} / {self.provider}\n\n"
            f"**Worker:** {self.worker}  \n"
            f"**Mode:** {self.mode}  \n"
            f"**Provider:** {self.provider}  \n"
            f"**Token Estimate:** {self.token_estimate}  \n"
            f"**Raw Session History:** {self.raw_session_history_tokens} (BLOCKED)\n\n"
            f"---\n\n"
            f"## Payload\n\n"
            f"```json\n{payload_json}\n```\n\n"
            f"---\n"
            f"*Built by Provider Payload Builder v1 — Y-OS*\n"
        )

    def to_json(self) -> str:
        return json.dumps({
            "mission_id": self.mission_id,
            "worker": self.worker,
            "mode": self.mode,
            "provider": self.provider,
            "token_estimate": self.token_estimate,
            "raw_session_history_tokens": self.raw_session_history_tokens,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }, indent=2, ensure_ascii=False)


# ─── Builder ──────────────────────────────────────────────────────────────────

# Worker → model mapping
WORKER_MODELS = {
    "Brahma":    {"openai": "gpt-4o", "anthropic": "claude-opus-4-5"},
    "Ganesha":   {"openai": "gpt-4o", "anthropic": "claude-opus-4-5"},
    "Lakshmi":   {"openai": "gpt-4o", "anthropic": "claude-opus-4-5"},
    "Hanuman":   {"openai": "gpt-4o-mini", "anthropic": "claude-haiku-3-5"},
    "Saraswati": {"openai": "gpt-4o", "anthropic": "claude-sonnet-4-5"},
    "Krishna":   {"openai": "gpt-4o", "anthropic": "claude-sonnet-4-5"},
}

SYSTEM_PROMPT_TEMPLATE = (
    "You are {worker}, a Y-OS worker with capability: {capability}. "
    "You operate under the Y-OS Constitution (Article I: Artifact Primacy). "
    "All outputs must be artifacts. No raw session history is available. "
    "Context mode: {mode}."
)


class ProviderPayloadBuilder:
    """Converts a Context Pack into provider-ready payloads."""

    def build_openai(self, pack) -> CompiledPayload:
        worker = pack.worker
        models = WORKER_MODELS.get(worker, {"openai": "gpt-4o"})
        system = SYSTEM_PROMPT_TEMPLATE.format(
            worker=worker, capability=pack.capability, mode=pack.mode
        )
        payload = OpenAIPayload(
            model=models["openai"],
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": pack.content},
            ],
            max_tokens=min(pack.token_estimate, 4096),
            metadata={
                "mission_id": pack.mission_id,
                "mode": pack.mode,
                "raw_session_history": 0,
            },
        )
        return CompiledPayload(
            mission_id=pack.mission_id,
            worker=worker,
            mode=pack.mode,
            provider="openai",
            payload=payload.to_dict(),
            token_estimate=pack.token_estimate,
            raw_session_history_tokens=0,
        )

    def build_anthropic(self, pack) -> CompiledPayload:
        worker = pack.worker
        models = WORKER_MODELS.get(worker, {"anthropic": "claude-sonnet-4-5"})
        system = SYSTEM_PROMPT_TEMPLATE.format(
            worker=worker, capability=pack.capability, mode=pack.mode
        )
        payload = AnthropicPayload(
            model=models["anthropic"],
            system=system,
            messages=[{"role": "user", "content": pack.content}],
            max_tokens=min(pack.token_estimate, 4096),
            metadata={
                "mission_id": pack.mission_id,
                "mode": pack.mode,
                "raw_session_history": 0,
            },
        )
        return CompiledPayload(
            mission_id=pack.mission_id,
            worker=worker,
            mode=pack.mode,
            provider="anthropic",
            payload=payload.to_dict(),
            token_estimate=pack.token_estimate,
            raw_session_history_tokens=0,
        )

    def build_manus(self, pack) -> CompiledPayload:
        payload = ManusPayload(
            worker=pack.worker,
            capability=pack.capability,
            mode=pack.mode,
            context_pack_id=f"context_pack_{pack.mission_id}_{pack.worker}",
            context_content=pack.content[:2000],  # Manus runtime truncation
            token_budget=pack.token_estimate,
            governance_required=(pack.mode in ("MODE-D", "MODE-E")),
            metadata={
                "mission_id": pack.mission_id,
                "raw_session_history": 0,
                "source_count": len(pack.source_manifest),
            },
        )
        return CompiledPayload(
            mission_id=pack.mission_id,
            worker=pack.worker,
            mode=pack.mode,
            provider="manus",
            payload=payload.to_dict(),
            token_estimate=pack.token_estimate,
            raw_session_history_tokens=0,
        )

    def build_all(self, pack) -> list[CompiledPayload]:
        """Build payloads for all three providers."""
        return [
            self.build_openai(pack),
            self.build_anthropic(pack),
            self.build_manus(pack),
        ]


if __name__ == "__main__":
    # Quick test
    import sys
    sys.path.insert(0, str(__file__).replace("provider_payload_builder_v1.py", ""))
    from context_compiler_v2 import ContextCompilerV2, CompilationRequest

    compiler = ContextCompilerV2()
    req = CompilationRequest(
        mission_id="MISSION-016-TEST",
        worker="Hanuman",
        capability="build",
        mode="MODE-B",
        relevant_adrs=["ADR-0037"],
    )
    pack = compiler.compile(req)
    builder = ProviderPayloadBuilder()
    payloads = builder.build_all(pack)
    for p in payloads:
        print(f"  {p.provider}: {p.token_estimate} tokens, raw_history={p.raw_session_history_tokens}")
