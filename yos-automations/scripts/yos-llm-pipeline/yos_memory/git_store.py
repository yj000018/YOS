import os
import shutil
from pathlib import Path
from typing import Tuple

def write_canonical_file(target_path: Path, content: str) -> Tuple[Path, str]:
    """
    Write content to target_path atomically.
    Returns the canonical path and the content hash.
    
    1. Write to a temporary file.
    2. Atomically rename (move) it to the target path.
    """
    from .ids import generate_content_hash
    
    # Ensure parent directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create temporary path
    temp_path = target_path.with_suffix('.tmp')
    
    try:
        # Write to temp file
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Atomic rename (POSIX)
        os.replace(temp_path, target_path)
        
        # Calculate hash of written content
        content_hash = generate_content_hash(content)
        
        return target_path, content_hash
        
    except Exception as e:
        # Cleanup temp file on failure
        if temp_path.exists():
            try:
                temp_path.unlink()
            except:
                pass
        raise e
