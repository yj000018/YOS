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

class SessionStore:
    def __init__(self):
        self.dedup = DedupState()
        self.ledger = SessionLedger()
        self.mem0 = Mem0Store()

    def archive_session(self,
                        source: str,
                        source_id: str,
                        title: str,
                        body_markdown: str,
                        created_at: str,
                        project_id: Optional[str] = None,
                        tags: list = None) -> Dict[str, Any]:
        """
        Archive a session to Git and optionally Mem0.
        Returns the result metadata.

        Dedup strategy: body_hash = sha256(body_markdown only).
        This is stable across runs because it excludes the frontmatter
        content_hash field (which would otherwise create a circular dependency
        where the hash changes every time it is embedded).
        """
        global_uid = generate_global_uid(source, source_id)

        # 1. Determine canonical path
        year = created_at[:4] if created_at else datetime.utcnow().strftime("%Y")
        rel_path = Path("08_LOGS") / "session-ledger" / "sessions" / source.lower() / year / f"{global_uid}.md"
        abs_path = config.yos_repo_path / rel_path

        # 2. Compute stable body hash for dedup (body only, not frontmatter)
        body_hash = generate_content_hash(body_markdown)

        # 3. Check deduplication using stable body_hash
        if self.dedup.is_processed(global_uid, body_hash):
            return {"status": "skipped_duplicate", "global_uid": global_uid, "path": str(rel_path)}

        # 4. Build frontmatter with body_hash embedded
        now = datetime.utcnow().isoformat() + "Z"
        metadata = create_base_frontmatter(
            memory_type="session",
            source=source,
            source_id=source_id,
            memory_id=global_uid,
            content_hash=body_hash,
            canonical_path=str(rel_path),
            created_at=created_at or now,
            updated_at=now
        )
        metadata["title"] = title
        if project_id:
            metadata["project_ids"] = [project_id]
        if tags:
            metadata["tags"] = tags

        # 5. Validate and generate final content
        validate_frontmatter(metadata)
        final_content = write_markdown(metadata, body_markdown)

        # 6. Write Canonical Git File (atomic)
        _, final_hash = write_canonical_file(abs_path, final_content)

        # 7. Update Dedup State and Ledger (use body_hash for dedup key)
        self.dedup.update_git_state(global_uid, body_hash, str(rel_path))
        self.ledger.update_session(global_uid, {
            "Title": title,
            "Source": source,
            "Source_ID": source_id,
            "Project_ID": project_id or "",
            "Processing_Status": "processed",
            "Git_Path": str(rel_path),
            "Content_Hash": body_hash,
            "Archive_Status": "Archived"  # Legacy compat
        })

        # 8. Mem0 Projection (graceful failure)
        mem0_status = "pending"
        mem0_ids = []
        try:
            projection = f"Session: {title}\nProject: {project_id or 'None'}\n\n{body_markdown[:1000]}..."
            mem0_ids = self.mem0.push_projection(projection, {
                "memory_type": "session",
                "global_uid": global_uid,
                "git_path": str(rel_path),
                "content_hash": body_hash
            })
            mem0_status = "synced"
        except Exception as e:
            print(f"Mem0 sync failed for {global_uid}: {e}")
            mem0_status = "failed"

        # 9. Update state with Mem0 result
        self.dedup.update_mem0_state(global_uid, mem0_status, mem0_ids)
        self.ledger.update_session(global_uid, {
            "Mem0_Status": mem0_status,
            "Mem0_Memory_IDs": ",".join(mem0_ids)
        })

        return {
            "status": "success",
            "global_uid": global_uid,
            "path": str(rel_path),
            "hash": final_hash,
            "body_hash": body_hash,
            "mem0_status": mem0_status
        }
