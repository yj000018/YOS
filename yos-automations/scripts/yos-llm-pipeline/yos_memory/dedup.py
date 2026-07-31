import json
from pathlib import Path
from typing import Dict, Any, Optional
from .config import config

class DedupState:
    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or config.processed_uids_json
        self.state: Dict[str, Dict[str, Any]] = {}
        self.load()
        
    def load(self):
        """Load the deduplication state from JSON."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
            except json.JSONDecodeError:
                self.state = {}
        else:
            self.state = {}
            
    def save(self):
        """Save the deduplication state to JSON."""
        # Ensure directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Atomic write
        temp_file = self.state_file.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, sort_keys=True)
        temp_file.replace(self.state_file)
        
    def get_record(self, global_uid: str) -> Optional[Dict[str, Any]]:
        """Get the state record for a global UID."""
        return self.state.get(global_uid)
        
    def is_processed(self, global_uid: str, content_hash: Optional[str] = None) -> bool:
        """
        Check if a UID has been processed.
        If content_hash is provided, checks if the content has changed.
        """
        record = self.state.get(global_uid)
        if not record:
            return False
            
        if content_hash and record.get("content_hash") != content_hash:
            return False # Processed but content changed
            
        return record.get("git_status") == "written"
        
    def update_git_state(self, global_uid: str, content_hash: str, git_path: str):
        """Update the Git writing state for a UID."""
        if global_uid not in self.state:
            self.state[global_uid] = {}
            
        self.state[global_uid].update({
            "content_hash": content_hash,
            "git_path": str(git_path),
            "git_status": "written"
        })
        
        # If content changed, reset mem0 status to pending
        if self.state[global_uid].get("content_hash") != content_hash:
            self.state[global_uid]["mem0_status"] = "pending"
            
        self.save()
        
    def update_mem0_state(self, global_uid: str, status: str, memory_ids: list = None):
        """Update the Mem0 sync state for a UID."""
        if global_uid not in self.state:
            self.state[global_uid] = {}
            
        update_data = {"mem0_status": status}
        if memory_ids is not None:
            update_data["mem0_memory_ids"] = memory_ids
            
        self.state[global_uid].update(update_data)
        self.save()
