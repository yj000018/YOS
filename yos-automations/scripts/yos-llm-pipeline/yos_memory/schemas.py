from typing import Dict, Any, List

REQUIRED_FRONTMATTER_FIELDS = [
    "schema_version",
    "memory_id",
    "memory_type",
    "status",
    "source",
    "source_id",
    "created_at",
    "updated_at",
    "content_hash",
    "canonical_path",
    "mem0"
]

ALLOWED_MEMORY_TYPES = ["session", "synthesis", "project", "memory", "preference", "knowledge", "fusion"]

def validate_frontmatter(metadata: Dict[str, Any]) -> bool:
    """
    Validate that the metadata dictionary contains all required fields 
    and conforms to the yos-memory schema.
    """
    missing = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in metadata]
    if missing:
        raise ValueError(f"Missing required frontmatter fields: {missing}")
        
    if metadata.get("schema_version") not in ["1.0", "yos-memory/v1"]:
        raise ValueError(f"Invalid schema_version: {metadata.get('schema_version')}")
        
    if metadata.get("memory_type") not in ALLOWED_MEMORY_TYPES:
        raise ValueError(f"Invalid memory_type: {metadata.get('memory_type')}")
        
    if not isinstance(metadata.get("mem0"), dict):
        raise ValueError("mem0 field must be a dictionary")
        
    if "status" not in metadata["mem0"]:
        raise ValueError("mem0 dictionary must contain 'status' field")
        
    return True

def create_base_frontmatter(
    memory_type: str, 
    source: str, 
    source_id: str, 
    memory_id: str,
    content_hash: str,
    canonical_path: str,
    created_at: str,
    updated_at: str
) -> Dict[str, Any]:
    """Create a baseline valid frontmatter dictionary."""
    return {
        "schema_version": "yos-memory/v1",
        "memory_id": memory_id,
        "memory_type": memory_type,
        "status": "active",
        "source": source,
        "source_id": source_id,
        "created_at": created_at,
        "updated_at": updated_at,
        "project_ids": [],
        "tags": [],
        "confidence": "high",
        "content_hash": content_hash,
        "canonical_path": canonical_path,
        "legacy_notion_url": None,
        "mem0": {
            "eligible": True,
            "status": "pending",
            "memory_ids": [],
            "projection_hash": None
        }
    }
