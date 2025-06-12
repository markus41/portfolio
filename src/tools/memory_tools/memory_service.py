from typing import Any, Dict, List
import requests
from ...utils.logger import get_logger

logger = get_logger(__name__)

class MemoryService:
    """Thin client for storing and fetching structured memories."""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        logger.info(f"Storing memory for key={key}")
        resp = requests.post(f"{self.endpoint}/store", json={"key": key, "data": payload})
        return resp.ok

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Fetching top {top_k} memories for key={key}")
        resp = requests.get(f"{self.endpoint}/fetch", params={"key": key, "top_k": top_k})
        return resp.json() if resp.ok else []
