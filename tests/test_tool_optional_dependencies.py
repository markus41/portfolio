import importlib
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools import chat_tool, crm_tool, scheduler_tool


def test_chat_tool_requires_openai():
    chat_tool.openai = None
    importlib.reload(chat_tool)
    with pytest.raises(RuntimeError):
        chat_tool.ChatTool().chat([])


def test_crm_tool_requires_requests():
    crm_tool.requests = None
    importlib.reload(crm_tool)
    with pytest.raises(RuntimeError):
        crm_tool.CRMTool.create_contact({})


def test_scheduler_tool_requires_google_client():
    scheduler_tool.service_account = None
    scheduler_tool.build = None
    importlib.reload(scheduler_tool)
    with pytest.raises(RuntimeError):
        scheduler_tool.SchedulerTool()
