import requests
from typing import Dict, Any, Optional
from .config import config

class LegacyNotionReader:
    """
    Read-only adapter for historical Notion data.
    MUST NOT contain any create, update, or delete operations.
    """
    def __init__(self):
        self.api_key = config.notion_api_key
        self.base_url = "https://api.notion.com/v1"
        
    def _get_headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise ValueError("NOTION_API_KEY is required for legacy reads")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
    def fetch_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a page by ID (read-only)."""
        if not self.api_key:
            return None
        response = requests.get(f"{self.base_url}/pages/{page_id}", headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        return None
        
    def query_database(self, database_id: str, filter_params: dict = None) -> list:
        """Query a database (read-only)."""
        if not self.api_key:
            return []
        payload = {}
        if filter_params:
            payload["filter"] = filter_params
            
        response = requests.post(f"{self.base_url}/databases/{database_id}/query", 
                                 headers=self._get_headers(), json=payload)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
