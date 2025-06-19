# src/agents/contract_agent.py

from ..base_agent import BaseAgent
from ...tools.docusign_tool import DocuSignTool
from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)

class ContractAgent(BaseAgent):
    def __init__(self):
        self.docusign = DocuSignTool(settings.DOCUSIGN_ACCESS_TOKEN)

    def run(self, payload):
        """
        payload: envelope_definition dict for DocuSign
        """
        envelope = self.docusign.send_envelope(payload)
        return {"envelope_id": envelope["envelopeId"], "status": envelope["status"]}
