import re
from ...utils.logger import get_logger

logger = get_logger(__name__)


def normalize_form(form_data: dict) -> dict:
    """Normalize raw form submission data."""
    email = form_data.get("Email") or form_data.get("email") or ""
    name = form_data.get("Name") or form_data.get("name") or ""
    phone = re.sub(r"\D", "", form_data.get("Phone", ""))
    return {"email": email.lower(), "name": name.strip(), "phone": phone}
