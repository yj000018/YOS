"""
Pipeline Adapter — yos_memory Phase 2
Non-destructive adapt layer for llm_distillation_pipeline.py.

Strategy:
  - llm_distillation_pipeline.py continues to use Notion as primary store (unchanged)
  - This adapter intercepts key events and mirrors them to Git + Mem0
  - Zero changes to the existing pipeline logic
  - Activated by setting YOS_MEMORY_ADAPTER=1 environment variable

Usage in llm_distillation_pipeline.py:
  from yos_memory.pipeline_adapter import PipelineAdapter
  adapter = PipelineAdapter()
  adapter.on_session_processed(session_result, distilled_data)
  adapter.on_knowledge_created(canonical_key, content, project)
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .config import config
from .ids import generate_global_uid, generate_content_hash
from .schemas import create_base_frontmatter, validate_frontmatter
from .frontmatter import write_markdown
from .git_store import write_canonical_file
from .dedup import DedupState
from .ledger import SessionLedger
from .mem0_store import Mem0Store

log = logging.getLogger("yos_memory.adapter")

ADAPTER_ENABLED = os.environ.get("YOS_MEMORY_ADAPTER", "0") == "1"


class PipelineAdapter:
    """
    Intercepts pipeline events and mirrors them to Git + Mem0.
    Does NOT modify Notion operations — purely additive.
    """

    def __init__(self):
        self.enabled = ADAPTER_ENABLED
        if not self.enabled:
            log.debug("PipelineAdapter disabled (set YOS_MEMORY_ADAPTER=1 to enable)")
            return
        self.dedup = DedupState()
        self.ledger = SessionLedger()
        self.mem0 = Mem0Store()
        log.info("PipelineAdapter initialized — Git+Mem0 mirroring active")

    def on_session_processed(
        self,
        session_result: Dict[str, Any],
        distilled: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Called after a session is processed by the pipeline.
        Mirrors the session synthesis to Git and Mem0.
        Returns the canonical Git path or None if skipped.
        """
        if not self.enabled:
            return None

        try:
            source_id = session_result.get("uid") or session_result.get("Source_ID", "")
            title = session_result.get("title") or session_result.get("Title", "Untitled")
            created_at = session_result.get("timestamp") or session_result.get("Created_At", "")
            project = (distilled or {}).get("project", "Unknown")

            if not source_id:
                log.warning("on_session_processed: no source_id, skipping")
                return None

            global_uid = generate_global_uid("Manus", source_id)

            # Build body from distilled data
            body_parts = [f"# {title}\n"]
            if distilled:
                if distilled.get("short_summary"):
                    body_parts.append(f"**Summary:** {distilled['short_summary']}\n")
                if distilled.get("project"):
                    body_parts.append(f"**Project:** {distilled['project']}\n")
                if distilled.get("keywords"):
                    body_parts.append(f"**Keywords:** {', '.join(distilled.get('keywords', []))}\n")
                if distilled.get("knowledge_items"):
                    body_parts.append("\n## Knowledge Items\n")
                    for item in distilled.get("knowledge_items", [])[:10]:
                        body_parts.append(f"- **{item.get('canonical_key', '?')}**: {item.get('content', '')[:200]}\n")

            body = "\n".join(body_parts)

            # Determine canonical path
            year = created_at[:4] if created_at and len(created_at) >= 4 else datetime.utcnow().strftime("%Y")
            rel_path = Path("08_LOGS") / "session-ledger" / "sessions" / "manus" / year / f"{global_uid}.md"
            abs_path = config.yos_repo_path / rel_path

            now = datetime.utcnow().isoformat() + "Z"
            metadata = create_base_frontmatter(
                memory_type="session",
                source="Manus",
                source_id=source_id,
                memory_id=global_uid,
                content_hash="",
                canonical_path=str(rel_path),
                created_at=created_at or now,
                updated_at=now
            )
            metadata["title"] = title
            metadata["project_ids"] = [project] if project else []
            metadata["pipeline"] = "llm_distillation_pipeline"

            # Dedup check using stable body_hash (excludes frontmatter)
            body_hash = generate_content_hash(body)
            if self.dedup.is_processed(global_uid, body_hash):
                log.debug(f"Skipping duplicate: {global_uid}")
                return None

            metadata["content_hash"] = body_hash
            validate_frontmatter(metadata)
            final_content = write_markdown(metadata, body)

            _, final_hash = write_canonical_file(abs_path, final_content)
            self.dedup.update_git_state(global_uid, body_hash, str(rel_path))
            self.ledger.update_session(global_uid, {
                "Title": title,
                "Source": "Manus",
                "Source_ID": source_id,
                "Project_ID": project,
                "Processing_Status": "processed",
                "Git_Path": str(rel_path),
                "Content_Hash": final_hash,
                "Archive_Status": "Archived",
                "Schema_Version": "yos-memory/v1",
            })

            # Mem0 projection
            try:
                projection = f"Session: {title}\nProject: {project}\n\n{body[:800]}"
                mem0_ids = self.mem0.push_projection(projection, {
                    "memory_type": "session",
                    "global_uid": global_uid,
                    "git_path": str(rel_path),
                })
                self.dedup.update_mem0_state(global_uid, "synced", mem0_ids)
                self.ledger.update_session(global_uid, {
                    "Mem0_Status": "synced",
                    "Mem0_Memory_IDs": ",".join(mem0_ids),
                })
                log.info(f"  [adapter] Mirrored to Git+Mem0: {global_uid}")
            except Exception as e:
                log.warning(f"  [adapter] Mem0 sync failed for {global_uid}: {e}")
                self.dedup.update_mem0_state(global_uid, "failed")

            return str(rel_path)

        except Exception as e:
            log.error(f"PipelineAdapter.on_session_processed error: {e}")
            return None

    def on_knowledge_created(
        self,
        canonical_key: str,
        content: str,
        project: str,
        notion_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Called after a Knowledge item is created in Notion.
        Mirrors it to Git as a knowledge file.
        """
        if not self.enabled:
            return None

        try:
            global_uid = generate_global_uid("knowledge", canonical_key)
            year = datetime.utcnow().strftime("%Y")
            rel_path = Path("05_KNOWLEDGE_DOMAINS") / project.lower().replace(" ", "_") / year / f"{global_uid}.md"
            abs_path = config.yos_repo_path / rel_path

            now = datetime.utcnow().isoformat() + "Z"
            metadata = create_base_frontmatter(
                memory_type="knowledge",
                source="llm_distillation_pipeline",
                source_id=canonical_key,
                memory_id=global_uid,
                content_hash="",
                canonical_path=str(rel_path),
                created_at=now,
                updated_at=now
            )
            metadata["title"] = canonical_key
            metadata["project_ids"] = [project]
            if notion_url:
                metadata["legacy_notion_url"] = notion_url

            body = f"# {canonical_key}\n\n{content}"
            # Dedup check using stable body_hash
            body_hash = generate_content_hash(body)
            if self.dedup.is_processed(global_uid, body_hash):
                return None

            metadata["content_hash"] = body_hash
            validate_frontmatter(metadata)
            final_content = write_markdown(metadata, body)
            _, final_hash = write_canonical_file(abs_path, final_content)
            self.dedup.update_git_state(global_uid, body_hash, str(rel_path))

            log.debug(f"  [adapter] Knowledge mirrored: {canonical_key}")
            return str(rel_path)

        except Exception as e:
            log.error(f"PipelineAdapter.on_knowledge_created error: {e}")
            return None
