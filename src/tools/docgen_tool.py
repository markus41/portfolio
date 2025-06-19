from docxtpl import DocxTemplate
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DocGenTool:
    """Generate documents based on a Docx template."""

    def __init__(self, template_path: str):
        self.template = DocxTemplate(template_path)

    def generate(self, context: dict, output_path: str) -> str:
        logger.info(f"Generating document to {output_path}")
        self.template.render(context)
        self.template.save(output_path)
        return output_path
