# src/memory_service.py

from typing import List, Dict, Any
import requests
from .utils.logger import get_logger

logger = get_logger(__name__)

class MemoryService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def store(self, key: str, payload: Dict[str, Any]) -> bool:
        logger.info(f"Storing memory for key={key}")
        # implement your vector DB or search-engine call here
        response = requests.post(f"{self.endpoint}/store", json={"key": key, "data": payload})
        return response.ok

    def fetch(self, key: str, top_k: int = 5) -> List[Dict[str, Any]]:
        logger.info(f"Fetching top {top_k} memories for key={key}")
        response = requests.get(f"{self.endpoint}/fetch", params={"key": key, "top_k": top_k})
        return response.json() if response.ok else []
