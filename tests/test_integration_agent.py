import json
from pathlib import Path

import json
from pathlib import Path

import pytest

from src.agents.integration_agent import IntegrationAgent


class StubConnector:
    def __init__(self, subtype, creds):
        self.data = [{"id": 1}]
        self.sent = []
        self.fetch_calls = 0

    def fetch_data(self, obj):
        self.fetch_calls += 1
        return list(self.data)

    def send_data(self, obj, data):
        self.sent.append(data)
        return True

    def count_data(self, obj):
        return len(self.sent if self.sent else self.data)


class FailingConnector(StubConnector):
    def fetch_data(self, obj):
        self.fetch_calls += 1
        if self.fetch_calls < 3:
            raise RuntimeError("server error")
        return list(self.data)


def _write_config(tmp_path: Path) -> Path:
    cfg = {
        "systems": {
            "crm": {"type": "crm", "subtype": "stub", "credentials": {}},
            "erp": {"type": "erp", "subtype": "stub", "credentials": {}},
        },
        "integrations": [
            {
                "name": "CRM_to_ERP_Contacts",
                "source": "crm",
                "target": "erp",
                "objects": ["contacts"],
                "sync_mode": "one_way",
                "field_mappings": {},
            }
        ],
    }
    path = tmp_path / "cfg.yaml"
    path.write_text(json.dumps(cfg))
    return path


def test_plan_and_execute(monkeypatch, tmp_path):
    path = _write_config(tmp_path)
    monkeypatch.setattr(
        "src.agents.integration_agent.CRMConnector", StubConnector
    )
    monkeypatch.setattr(
        "src.agents.integration_agent.ERPConnector", StubConnector
    )
    agent = IntegrationAgent(str(path))
    plan = agent.plan_integrations()[0]
    agent.execute_integration(plan)
    src = agent.systems["crm"]
    tgt = agent.systems["erp"]
    assert tgt.sent == src.data


def test_retry_logic(monkeypatch, tmp_path):
    path = _write_config(tmp_path)
    monkeypatch.setattr(
        "src.agents.integration_agent.CRMConnector", FailingConnector
    )
    monkeypatch.setattr(
        "src.agents.integration_agent.ERPConnector", StubConnector
    )
    monkeypatch.setattr("time.sleep", lambda x: None)
    agent = IntegrationAgent(str(path))
    plan = agent.plan_integrations()[0]
    agent.execute_integration(plan)
    src = agent.systems["crm"]
    assert src.fetch_calls == 3
