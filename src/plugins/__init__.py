"""Plugin stubs providing tool integrations."""

from .base_plugin import BaseToolPlugin
from .email_plugin import EmailPlugin
from .crm_plugin import CRMPlugin
from .scraping_plugin import ScrapingPlugin
from .cloud_docs_plugin import CloudDocsPlugin

__all__ = [
    "BaseToolPlugin",
    "EmailPlugin",
    "CRMPlugin",
    "ScrapingPlugin",
    "CloudDocsPlugin",
]
