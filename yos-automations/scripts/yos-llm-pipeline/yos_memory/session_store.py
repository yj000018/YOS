from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from .config import config
from .ids import generate_global_uid
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
        """
        global_uid = generate_global_uid(source, source_id)
        
        # 1. Determine canonical path
        year = created_at[:4] if created_at else datetime.utcnow().strftime("%Y")
        rel_path = Path("08_LOGS") / "session-ledger" / "sessions" / source.lower() / year / f"{global_uid}.md"
        abs_path = config.yos_repo_path / rel_path
        
        # 2. Build frontmatter
        now = datetime.utcnow().isoformat() + "Z"
        metadata = create_base_frontmatter(
            memory_type="session",
            source=source,
            source_id=source_id,
            memory_id=global_uid,
            content_hash="", # Placeholder
            canonical_path=str(rel_path),
            created_at=created_at or now,
            updated_at=now
        )
        
        metadata["title"] = title
        if project_id:
            metadata["project_ids"] = [project_id]
        if tags:
            metadata["tags"] = tags
            
        # 3. Generate Markdown and Hash
        # Temporary hash to check dedup before writing
        from .ids import generate_content_hash
        temp_content = write_markdown(metadata, body_markdown)
        content_hash = generate_content_hash(temp_content)
        
        # Check deduplication
        if self.dedup.is_processed(global_uid, content_hash):
            return {"status": "skipped_duplicate", "global_uid": global_uid, "path": str(rel_path)}
            
        # Update hash in metadata and generate final content
        metadata["content_hash"] = content_hash
        validate_frontmatter(metadata)
        final_content = write_markdown(metadata, body_markdown)
        
        # 4. Write Canonical Git File
        _, final_hash = write_canonical_file(abs_path, final_content)
        
        # 5. Update Dedup State and Ledger
        self.dedup.update_git_state(global_uid, final_hash, str(rel_path))
        self.ledger.update_session(global_uid, {
            "Title": title,
            "Source": source,
            "Source_ID": source_id,
            "Project_ID": project_id or "",
            "Processing_Status": "processed",
            "Git_Path": str(rel_path),
            "Content_Hash": final_hash,
            "Archive_Status": "Archived" # Legacy compat
        })
        
        # 6. Mem0 Projection
        mem0_status = "pending"
        mem0_ids = []
        
        try:
            # Build compact projection
            projection = f"Session: {title}\nProject: {project_id or 'None'}\n\n{body_markdown[:1000]}..."
            mem0_ids = self.mem0.push_projection(projection, {
                "memory_type": "session",
                "global_uid": global_uid,
                "git_path": str(rel_path),
                "content_hash": final_hash
            })
            mem0_status = "synced"
        except Exception as e:
            print(f"Mem0 sync failed for {global_uid}: {e}")
            mem0_status = "failed"
            
        # 7. Update state with Mem0 result
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
            "mem0_status": mem0_status
        }
