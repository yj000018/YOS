import os
from pathlib import Path

class Config:
    def __init__(self):
        # Base paths
        self.yos_repo_path = Path(os.environ.get("YOS_REPO_PATH", "/tmp/yos_audit_clone"))
        
        # Canonical paths relative to YOS_REPO_PATH
        self.ledger_dir = self.yos_repo_path / "08_LOGS" / "session-ledger"
        self.sessions_dir = self.ledger_dir / "sessions"
        self.syntheses_dir = self.ledger_dir / "syntheses"
        self.fusions_dir = self.ledger_dir / "fusions"
        self.state_dir = self.ledger_dir / "state"
        
        self.projects_dir = self.yos_repo_path / "00_META" / "PROJECTS"
        self.memory_inbox_dir = self.yos_repo_path / "07_SOURCE_CORPUS" / "memory-inbox"
        self.preferences_dir = self.yos_repo_path / "00_META" / "USER_PROFILE" / "preferences"
        self.knowledge_dir = self.yos_repo_path / "05_KNOWLEDGE_DOMAINS"
        
        # State files
        self.master_ledger_csv = self.ledger_dir / "data" / "master_ledger.csv"
        self.processed_uids_json = self.state_dir / "processed_uids.json"
        
        # Ensure base directories exist
        self._ensure_dirs()
        
        # API Keys (no Notion required for writes)
        self.mem0_api_key = os.environ.get("MEM0_API_KEY", "")
        self.mem0_user_id = os.environ.get("MEM0_USER_ID", "yannick")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.manus_jwt_token = os.environ.get("MANUS_JWT_TOKEN", "")
        
        # Legacy read-only
        self.notion_api_key = os.environ.get("NOTION_API_KEY", "")

    def _ensure_dirs(self):
        """Ensure canonical directories exist."""
        dirs = [
            self.sessions_dir,
            self.syntheses_dir,
            self.fusions_dir,
            self.state_dir,
            self.projects_dir,
            self.memory_inbox_dir,
            self.preferences_dir,
            self.ledger_dir / "data"
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

config = Config()
