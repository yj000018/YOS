from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from .config import config
from .ids import generate_random_id, generate_content_hash
from .schemas import create_base_frontmatter, validate_frontmatter
from .frontmatter import write_markdown
from .git_store import write_canonical_file
from .mem0_store import Mem0Store

class MemoryIntake:
    def __init__(self):
        self.mem0 = Mem0Store()
        
    def ingest(self, title: str, content: str, source: str = "manual", tags: list = None) -> Dict[str, Any]:
        """
        Ingest generic memory into the Git Memory Inbox.
        """
        now = datetime.utcnow()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        memory_id = generate_random_id("mem")
        
        rel_path = Path("07_SOURCE_CORPUS") / "memory-inbox" / year / month / f"{memory_id}.md"
        abs_path = config.yos_repo_path / rel_path
        
        metadata = create_base_frontmatter(
            memory_type="memory",
            source=source,
            source_id=memory_id,
            memory_id=memory_id,
            content_hash="",
            canonical_path=str(rel_path),
            created_at=now.isoformat() + "Z",
            updated_at=now.isoformat() + "Z"
        )
        
        metadata["title"] = title
        if tags:
            metadata["tags"] = tags
            
        temp_content = write_markdown(metadata, content)
        content_hash = generate_content_hash(temp_content)
        metadata["content_hash"] = content_hash
        
        validate_frontmatter(metadata)
        final_content = write_markdown(metadata, content)
        
        _, final_hash = write_canonical_file(abs_path, final_content)
        
        # Mem0 Projection
        mem0_status = "pending"
        try:
            self.mem0.push_projection(f"Memory: {title}\n\n{content}", {
                "memory_type": "memory",
                "memory_id": memory_id,
                "git_path": str(rel_path)
            })
            mem0_status = "synced"
        except Exception:
            mem0_status = "failed"
            
        return {
            "status": "success",
            "memory_id": memory_id,
            "path": str(rel_path),
            "mem0_status": mem0_status
        }
