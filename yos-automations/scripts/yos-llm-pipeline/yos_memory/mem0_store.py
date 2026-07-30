import requests
from typing import Dict, Any, List, Optional
from .config import config

class Mem0Store:
    def __init__(self):
        self.api_key = config.mem0_api_key
        self.user_id = config.mem0_user_id
        self.base_url = "https://api.mem0.ai/v1/memories"
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def push_projection(self, projection_text: str, metadata: Dict[str, Any]) -> List[str]:
        """
        Push a compact semantic projection to Mem0.
        Returns a list of created memory IDs.
        """
        if not self.api_key:
            # Mock mode or pending state if key is absent
            return ["mock_mem0_id_123"]
            
        # Ensure user_id is set
        metadata["user_id"] = self.user_id
        
        # NEVER send credentials in projection text
        if "eyJhbGci" in projection_text or "sk-ant" in projection_text:
            raise ValueError("SECURITY VIOLATION: Attempted to push secrets to Mem0")
            
        payload = {
            "messages": [{"role": "user", "content": projection_text}],
            "user_id": self.user_id,
            "metadata": metadata
        }
        
        response = requests.post(self.base_url, headers=self._get_headers(), json=payload)
        
        if response.status_code in (200, 201):
            data = response.json()
            # Handle different response formats from Mem0 API
            if isinstance(data, list):
                return [m.get("id") for m in data if "id" in m]
            elif isinstance(data, dict) and "id" in data:
                return [data["id"]]
            elif isinstance(data, dict) and "results" in data:
                return [m.get("id") for m in data["results"] if "id" in m]
            return ["unknown_mem0_id"]
        else:
            raise Exception(f"Mem0 API error ({response.status_code}): {response.text}")
            
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Mem0 for semantic recall."""
        if not self.api_key:
            return []
            
        payload = {
            "query": query,
            "user_id": self.user_id,
            "limit": limit
        }
        
        response = requests.post(f"{self.base_url}/search", headers=self._get_headers(), json=payload)
        if response.status_code == 200:
            return response.json()
        return []
