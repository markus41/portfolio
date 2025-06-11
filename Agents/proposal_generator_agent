# src/agents/proposal_generator_agent.py

from .base_agent import BaseAgent
from ..tools.docgen_tool import DocGenTool
from ..utils.logger import get_logger
import uuid

logger = get_logger(__name__)

class ProposalGeneratorAgent(BaseAgent):
    def __init__(self, template_path: str = "templates/proposal.docx"):
        self.doc_tool = DocGenTool(template_path)

    def run(self, payload):
        """
        payload: {
          "client_name": str,
          "project_scope": str,
          "pricing": dict,  # e.g. {"Service A":1000, "Service B":2000}
          "valid_until": "2025-07-31"
        }
        """
        filename = f"output/proposal_{uuid.uuid4().hex}.docx"
        context = {
            "client_name": payload["client_name"],
            "project_scope": payload["project_scope"],
            "pricing_table": payload["pricing"].items(),
            "valid_until": payload["valid_until"],
        }
        path = self.doc_tool.generate(context, filename)
        logger.info(f"Proposal generated at {path}")
        return {"path": path, "status": "generated"}
