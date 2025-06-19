# Tools/crm_tools/salesforce_tool.py

from simple_salesforce import Salesforce
from ...config import settings
from ...utils.logger import get_logger
from ...utils import retry_tool

logger = get_logger(__name__)

class SalesforceTool:
    def __init__(self):
        logger.info("Authenticating to Salesforce")
        self.sf = Salesforce(
            username=settings.SF_USERNAME,
            password=settings.SF_PASSWORD,
            security_token=settings.SF_SECURITY_TOKEN,
            client_id=settings.SF_CLIENT_ID,
            domain=settings.SF_DOMAIN  # use "test" for sandbox
        )

    @retry_tool()
    def create_contact(self, data: dict) -> dict:
        logger.info(f"Creating Salesforce Contact: {data}")
        return self.sf.Contact.create(data)

    @retry_tool()
    def get_contact_by_email(self, email: str) -> dict | None:
        logger.info(f"Querying Salesforce for email={email}")
        soql = f"SELECT Id, FirstName, LastName, Email FROM Contact WHERE Email = '{email}' LIMIT 1"
        res = self.sf.query(soql)
        records = res.get("records", [])
        return records[0] if records else None

    @retry_tool()
    def update_contact(self, contact_id: str, data: dict) -> dict:
        logger.info(f"Updating Salesforce Contact {contact_id}: {data}")
        return self.sf.Contact.update(contact_id, data)
