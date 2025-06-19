# Tools/crm_tools/monday_tool.py

import json
import requests
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)

class MondayTool:
    def __init__(self):
        self.url = settings.MONDAY_API_URL
        self.headers = {
            "Authorization": settings.MONDAY_API_TOKEN,
            "Content-Type": "application/json"
        }

    def create_item(self, board_id: int, item_name: str, column_values: dict = None) -> dict:
        query = """
        mutation ($boardId: Int!, $itemName: String!, $columnValues: JSON) {
          create_item(board_id: $boardId, item_name: $itemName, column_values: $columnValues) {
            id
          }
        }
        """
        vars = {
            "boardId": board_id,
            "itemName": item_name,
            "columnValues": json.dumps(column_values or {})
        }
        resp = requests.post(self.url, json={"query": query, "variables": vars}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()["data"]["create_item"]

    def get_item(self, item_id: int) -> dict:
        query = """
        query ($itemId: Int!) {
          items(ids: [$itemId]) {
            id
            name
            column_values { id text }
          }
        }
        """
        vars = {"itemId": item_id}
        resp = requests.post(self.url, json={"query": query, "variables": vars}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()["data"]["items"][0]

    def update_item(self, item_id: int, column_values: dict) -> dict:
        query = """
        mutation ($itemId: Int!, $columnValues: JSON!) {
          change_multiple_column_values(item_id: $itemId, column_values: $columnValues) {
            id
          }
        }
        """
        vars = {"itemId": item_id, "columnValues": json.dumps(column_values)}
        resp = requests.post(self.url, json={"query": query, "variables": vars}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()["data"]["change_multiple_column_values"]

