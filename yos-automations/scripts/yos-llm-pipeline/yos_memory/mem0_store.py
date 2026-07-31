from typing import Dict, Any, List
from .config import config

class Mem0Store:
    """
    Mem0 projection store using the official mem0ai SDK.
    Requires: pip install mem0ai
    Auth: MEM0_API_KEY env var (via config.mem0_api_key)
    """

    def __init__(self):
        self.api_key = config.mem0_api_key
        self.user_id = config.mem0_user_id
        self._client = None

    def _get_client(self):
        """Lazy-init Mem0 client."""
        if self._client is None:
            try:
                from mem0 import MemoryClient
                self._client = MemoryClient(api_key=self.api_key)
            except ImportError:
                raise RuntimeError("mem0ai SDK not installed. Run: pip install mem0ai")
        return self._client

    def push_projection(self, projection_text: str, metadata: Dict[str, Any]) -> List[str]:
        """
        Push a compact semantic projection to Mem0.
        Returns a list of created memory IDs (or event_ids for async ops).

        Security guard: rejects any projection containing JWT tokens or API keys.
        """
        if not self.api_key:
            # Mock mode — no API key configured
            return ["mock_mem0_id_no_key"]

        # SECURITY GUARD: never push credentials to Mem0
        if "eyJhbGci" in projection_text or "sk-ant" in projection_text or "sk-" in projection_text:
            raise ValueError("SECURITY VIOLATION: Attempted to push credentials to Mem0")

        client = self._get_client()

        # Ensure user_id is not in metadata (it's a top-level param)
        clean_metadata = {k: v for k, v in metadata.items() if k != "user_id"}

        result = client.add(
            messages=[{"role": "user", "content": projection_text}],
            user_id=self.user_id,
            metadata=clean_metadata
        )

        # Handle Mem0 async response format: {'event_id': '...', 'status': 'PENDING'}
        if isinstance(result, dict):
            if "event_id" in result:
                return [result["event_id"]]
            elif "id" in result:
                return [result["id"]]
            elif "results" in result:
                return [m.get("id") for m in result["results"] if "id" in m]
        elif isinstance(result, list):
            return [m.get("id") for m in result if isinstance(m, dict) and "id" in m]

        return ["unknown_mem0_id"]

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Mem0 for semantic recall."""
        if not self.api_key:
            return []

        client = self._get_client()
        try:
            results = client.search(query, user_id=self.user_id, limit=limit)
            if isinstance(results, list):
                return results
            elif isinstance(results, dict) and "results" in results:
                return results["results"]
            return []
        except Exception:
            return []
