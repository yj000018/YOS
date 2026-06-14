#!/usr/bin/env python3
"""
Live Worker Executor v1 — Y-OS
ADR-0044

Executes real provider API calls from compiled Context Packs.
Never exposes secrets in logs or outputs.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import os
import time
import re


# ─── Execution Result ─────────────────────────────────────────────────────────

@dataclass
class WorkerExecutionResult:
    worker: str
    capability: str
    mission_id: str
    provider: str
    model: str
    status: str                    # SUCCESS | FAILED | SKIPPED_MISSING_SECRET | FALLBACK
    content: str = ""              # Worker output (never contains secrets)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    error_type: str = ""
    error_message_redacted: str = ""
    context_pack_id: str = ""
    selected_mode: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def success(self) -> bool:
        return self.status == "SUCCESS"


def _redact_secrets(text: str) -> str:
    """Remove any potential secret values from error messages."""
    patterns = [
        (r"sk-[A-Za-z0-9]{20,}", "[REDACTED_OPENAI_KEY]"),
        (r"sk-ant-[A-Za-z0-9\-]{20,}", "[REDACTED_ANTHROPIC_KEY]"),
        (r"ghp_[A-Za-z0-9]{36}", "[REDACTED_GITHUB_PAT]"),
        (r"Bearer [A-Za-z0-9\-._~+/]{20,}", "Bearer [REDACTED]"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text


# ─── Executor ─────────────────────────────────────────────────────────────────

class LiveWorkerExecutor:
    """Executes real LLM API calls from Context Pack payloads."""

    def execute_openai(
        self,
        worker: str,
        capability: str,
        mission_id: str,
        system_prompt: str,
        user_content: str,
        model: str = "gpt-4o",
        context_pack_id: str = "",
        selected_mode: str = "",
    ) -> WorkerExecutionResult:
        """Execute via OpenAI API."""
        api_key = os.environ.get("OPENAI_API_KEY", "")
        api_base = os.environ.get("OPENAI_API_BASE", "")

        if not api_key:
            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="openai",
                model=model,
                status="SKIPPED_MISSING_SECRET",
                error_type="MISSING_API_KEY",
                error_message_redacted="OPENAI_API_KEY not set in environment.",
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

        try:
            import openai
            client_kwargs = {"api_key": api_key}
            if api_base:
                client_kwargs["base_url"] = api_base
            client = openai.OpenAI(**client_kwargs)

            start = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=1500,
                temperature=0.2,
            )
            latency_ms = (time.time() - start) * 1000

            content = response.choices[0].message.content or ""
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            actual_model = response.model or model

            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="openai",
                model=actual_model,
                status="SUCCESS",
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                latency_ms=round(latency_ms, 1),
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

        except Exception as e:
            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="openai",
                model=model,
                status="FAILED",
                error_type=type(e).__name__,
                error_message_redacted=_redact_secrets(str(e)[:200]),
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

    def execute_anthropic(
        self,
        worker: str,
        capability: str,
        mission_id: str,
        system_prompt: str,
        user_content: str,
        model: str = "claude-opus-4-5",
        context_pack_id: str = "",
        selected_mode: str = "",
    ) -> WorkerExecutionResult:
        """Execute via Anthropic API."""
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")

        if not api_key:
            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="anthropic",
                model=model,
                status="SKIPPED_MISSING_SECRET",
                error_type="MISSING_API_KEY",
                error_message_redacted="ANTHROPIC_API_KEY not set in environment.",
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)

            start = time.time()
            response = client.messages.create(
                model=model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_content}],
                max_tokens=1500,
            )
            latency_ms = (time.time() - start) * 1000

            content = response.content[0].text if response.content else ""
            usage = response.usage
            prompt_tokens = usage.input_tokens if usage else 0
            completion_tokens = usage.output_tokens if usage else 0
            actual_model = response.model or model

            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="anthropic",
                model=actual_model,
                status="SUCCESS",
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
                latency_ms=round(latency_ms, 1),
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

        except Exception as e:
            return WorkerExecutionResult(
                worker=worker,
                capability=capability,
                mission_id=mission_id,
                provider="anthropic",
                model=model,
                status="FAILED",
                error_type=type(e).__name__,
                error_message_redacted=_redact_secrets(str(e)[:200]),
                context_pack_id=context_pack_id,
                selected_mode=selected_mode,
            )

    def execute_with_fallback(
        self,
        worker: str,
        capability: str,
        mission_id: str,
        system_prompt: str,
        user_content: str,
        primary_provider: str = "anthropic",
        primary_model: str = "claude-opus-4-5",
        fallback_provider: str = "openai",
        fallback_model: str = "gpt-4o",
        context_pack_id: str = "",
        selected_mode: str = "",
    ) -> WorkerExecutionResult:
        """Try primary provider, fallback to secondary if needed."""
        # Try primary
        if primary_provider == "anthropic":
            result = self.execute_anthropic(
                worker, capability, mission_id, system_prompt, user_content,
                primary_model, context_pack_id, selected_mode
            )
        else:
            result = self.execute_openai(
                worker, capability, mission_id, system_prompt, user_content,
                primary_model, context_pack_id, selected_mode
            )

        if result.success:
            return result

        # Fallback
        print(f"  [FALLBACK] {primary_provider} failed ({result.status}) → trying {fallback_provider}")
        if fallback_provider == "openai":
            fallback_result = self.execute_openai(
                worker, capability, mission_id, system_prompt, user_content,
                fallback_model, context_pack_id, selected_mode
            )
        else:
            fallback_result = self.execute_anthropic(
                worker, capability, mission_id, system_prompt, user_content,
                fallback_model, context_pack_id, selected_mode
            )

        if fallback_result.success:
            fallback_result.status = "FALLBACK"
        return fallback_result
