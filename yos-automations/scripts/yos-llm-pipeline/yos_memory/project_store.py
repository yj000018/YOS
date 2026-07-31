from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from .config import config
from .schemas import create_base_frontmatter, validate_frontmatter
from .frontmatter import write_markdown, read_markdown
from .git_store import write_canonical_file
from .ids import generate_content_hash
from .mem0_store import Mem0Store

class ProjectStore:
    def __init__(self):
        self.mem0 = Mem0Store()
        
    def write_project_card(self, slug: str, title: str, body_markdown: str, session_uids: List[str] = None) -> Dict[str, Any]:
        """
        Write or update a living project card in Git.
        """
        rel_path = Path("00_META") / "PROJECTS" / slug / "PROJECT.md"
        abs_path = config.yos_repo_path / rel_path
        
        now = datetime.utcnow().isoformat() + "Z"
        created_at = now
        
        # Read existing to preserve creation date
        if abs_path.exists():
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    existing_meta, _ = read_markdown(f.read())
                    if "created_at" in existing_meta:
                        created_at = existing_meta["created_at"]
            except Exception:
                pass
                
        metadata = create_base_frontmatter(
            memory_type="project",
            source="yos_pipeline",
            source_id=slug,
            memory_id=f"project_{slug}",
            content_hash="",
            canonical_path=str(rel_path),
            created_at=created_at,
            updated_at=now
        )
        
        metadata["title"] = title
        metadata["project_ids"] = [slug]
        if session_uids:
            metadata["last_session_ids"] = session_uids
            
        temp_content = write_markdown(metadata, body_markdown)
        content_hash = generate_content_hash(temp_content)
        metadata["content_hash"] = content_hash
        
        validate_frontmatter(metadata)
        final_content = write_markdown(metadata, body_markdown)
        
        _, final_hash = write_canonical_file(abs_path, final_content)
        
        # Mem0 Projection
        mem0_status = "pending"
        try:
            projection = f"Project: {title}\nStatus: Active\n\n{body_markdown[:1000]}"
            self.mem0.push_projection(projection, {
                "memory_type": "project",
                "project_id": slug,
                "git_path": str(rel_path)
            })
            mem0_status = "synced"
        except Exception as e:
            print(f"Mem0 sync failed for project {slug}: {e}")
            mem0_status = "failed"
            
        return {
            "status": "success",
            "project": slug,
            "path": str(rel_path),
            "mem0_status": mem0_status
        }
