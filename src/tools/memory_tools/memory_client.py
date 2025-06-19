import requests


class MemoryClient:
    """HTTP client for interacting with an external memory service."""

    def __init__(self, base_url: str, token: str):
        self.base = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def store(self, blob_uri: str, metadata: dict):
        payload = {"blob_uri": blob_uri, "metadata": metadata}
        return requests.post(f"{self.base}/store", json=payload, headers=self.headers)

    def retrieve(self, query: str, k: int = 6, filters: dict | None = None):
        params = {"query": query, "k": k, "filters": filters or {}}
        resp = requests.get(
            f"{self.base}/retrieve", params=params, headers=self.headers
        )
        return resp.json()

    def forget(self, doc_id: str):
        return requests.post(
            f"{self.base}/forget", json={"doc_id": doc_id}, headers=self.headers
        )

    def push_fact(self, fact_json: dict):
        return requests.post(
            f"{self.base}/push_fact", json=fact_json, headers=self.headers
        )
