import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from .config import config

class SessionLedger:
    def __init__(self, ledger_file: Optional[Path] = None):
        self.ledger_file = ledger_file or config.master_ledger_csv
        self.fieldnames = [
            "Global_UID", "Source", "Source_ID", "Title", "Project_ID",
            "Created_At", "Updated_At", "Processing_Status", "Git_Path",
            "Content_Hash", "Mem0_Status", "Mem0_Memory_IDs", "Schema_Version",
            "Last_Processed_At", "Legacy_Notion_URL", "Archive_Status", "Archive_Link"
        ]
        
    def read_all(self) -> List[Dict[str, str]]:
        """Read all rows from the ledger."""
        if not self.ledger_file.exists():
            return []
            
        with open(self.ledger_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
            
    def write_all(self, rows: List[Dict[str, str]]):
        """Write all rows to the ledger atomically."""
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure all rows have all fields
        for row in rows:
            for field in self.fieldnames:
                if field not in row:
                    row[field] = ""
                    
        temp_file = self.ledger_file.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
        temp_file.replace(self.ledger_file)
        
    def update_session(self, global_uid: str, updates: Dict[str, str]):
        """Update a specific session in the ledger."""
        rows = self.read_all()
        found = False
        
        for row in rows:
            if row.get("Global_UID") == global_uid:
                row.update(updates)
                row["Last_Processed_At"] = datetime.utcnow().isoformat() + "Z"
                found = True
                break
                
        if not found:
            # Create new row
            new_row = {"Global_UID": global_uid}
            new_row.update(updates)
            new_row["Last_Processed_At"] = datetime.utcnow().isoformat() + "Z"
            rows.append(new_row)
            
        self.write_all(rows)
        
    def get_pending_sessions(self) -> List[Dict[str, str]]:
        """Get sessions that need processing (Pending or legacy Archive_Status)."""
        rows = self.read_all()
        pending = []
        for row in rows:
            if row.get("Processing_Status") != "processed" and row.get("Archive_Status") != "Archived":
                pending.append(row)
        return pending
