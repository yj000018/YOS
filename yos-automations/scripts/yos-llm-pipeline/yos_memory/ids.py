import hashlib
import uuid
import re

def generate_global_uid(source: str, native_id: str) -> str:
    """Generate a stable global UID from source and native ID."""
    source_clean = re.sub(r'[^a-zA-Z0-9]', '', str(source).lower())
    native_clean = re.sub(r'[^a-zA-Z0-9_-]', '', str(native_id))
    if not source_clean or not native_clean:
        raise ValueError(f"Invalid source or native_id: {source}, {native_id}")
    return f"{source_clean}_{native_clean}"

def generate_content_hash(content: str) -> str:
    """Generate SHA256 hash of normalized content."""
    # Normalize line endings to ensure consistent hashing across platforms
    normalized_content = content.replace('\r\n', '\n').strip()
    return f"sha256:{hashlib.sha256(normalized_content.encode('utf-8')).hexdigest()}"

def generate_memory_key(memory_type: str, global_uid: str, content_hash: str) -> str:
    """Generate a unique key for deduplication."""
    return f"{memory_type}:{global_uid}:{content_hash}"

def generate_random_id(prefix: str = "") -> str:
    """Generate a random ID with an optional prefix."""
    random_str = uuid.uuid4().hex[:12]
    return f"{prefix}_{random_str}" if prefix else random_str
