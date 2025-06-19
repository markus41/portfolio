# src/agents/contract_sign_monitor_agent.py

from ..base_agent import BaseAgent
from ...tools.docusign_tool import DocuSignTool
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ContractSignMonitorAgent(BaseAgent):
    def __init__(self):
        self.docusign = DocuSignTool(settings.DOCUSIGN_ACCESS_TOKEN)

    def run(self, payload):
        """
        payload: {
          "envelope_id": str
        }
        """
        env_id = payload["envelope_id"]
        status = self.docusign.get_envelope_status(env_id).get("status")
        logger.info(f"ContractSignMonitorAgent → envelope {env_id} is {status}")
        return {"status": status}
