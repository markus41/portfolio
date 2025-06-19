"""Centralised project configuration using pydantic settings.

``Settings`` aggregates configuration previously scattered across
``constants.py``.  Values are loaded from environment variables and an
``.env`` file whose location depends on the running environment.  The
file selection logic is controlled by the ``ENV`` and ``ENV_FILE``
variables:

``ENV_FILE``
    When set, provides an explicit path to the dotenv file.

``ENV``
    Chooses a file named ``.env.<ENV>``.  ``ENV=prod`` loads ``.env`` to
    mimic typical production deployments.  The default is ``dev`` which
    reads ``.env.dev`` if present.

Instances validate a few fields (like AWS regions) to catch
misconfiguration early in application startup.
"""
from __future__ import annotations

from typing import Literal, Optional
import os

from pydantic import BaseSettings, Field, validator


def _choose_env_file() -> str:
    """Determine which ``.env`` file to load based on environment vars."""
    explicit = os.getenv("ENV_FILE")
    if explicit:
        return explicit
    env = os.getenv("ENV", "dev")
    return ".env" if env == "prod" else f".env.{env}"


_DEFAULT_ENV_FILE = _choose_env_file()


def _load_env_file(path: str) -> dict[str, str]:
    """Return key-value pairs parsed from ``path`` if it exists."""
    data: dict[str, str] = {}
    if not os.path.exists(path):
        return data
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key] = value
    return data


def update_env_file(path: str, values: dict[str, str]) -> None:
    """Merge ``values`` with existing ``path`` contents and persist."""
    env = _load_env_file(path)
    env.update({str(k): str(v) for k, v in values.items()})
    with open(path, "w") as f:
        for key, val in env.items():
            f.write(f"{key}={val}\n")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI Providers
    OPENAI_API_KEY: Optional[str] = None

    # CRM & Marketing Platforms
    CRM_API_URL: Optional[str] = None
    CRM_API_KEY: Optional[str] = None
    MONDAY_API_TOKEN: Optional[str] = None
    MONDAY_API_URL: str = "https://api.monday.com/v2"
    HUBSPOT_API_KEY: Optional[str] = None
    DYNAMICS_TENANT_ID: Optional[str] = None
    DYNAMICS_CLIENT_ID: Optional[str] = None
    DYNAMICS_CLIENT_SECRET: Optional[str] = None
    DYNAMICS_API_URL: Optional[str] = None
    SF_CLIENT_ID: Optional[str] = None
    SF_CLIENT_SECRET: Optional[str] = None
    SF_USERNAME: Optional[str] = None
    SF_PASSWORD: Optional[str] = None
    SF_SECURITY_TOKEN: Optional[str] = None
    SF_DOMAIN: str = "login.salesforce.com"

    # Advertising & Social Platforms
    FACEBOOK_ACCESS_TOKEN: str = ""
    GOOGLE_ADS_API_KEY: str = ""

    # Real Estate APIs
    MLS_API_URL: Optional[str] = None
    MLS_API_KEY: Optional[str] = None
    RE_LEADS_API_URL: Optional[str] = None
    RE_LEADS_API_KEY: Optional[str] = None
    LISTING_POST_API_URL: Optional[str] = None
    LISTING_POST_API_KEY: Optional[str] = None

    # Document Signing
    DOCUSIGN_ACCESS_TOKEN: Optional[str] = None
    DOCUSIGN_INTEGRATOR_KEY: Optional[str] = None
    DOCUSIGN_USER_ID: Optional[str] = None
    DOCUSIGN_ACCOUNT_ID: Optional[str] = None
    DOCUSIGN_BASE_URL: Optional[str] = None

    # Storage & Infrastructure
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_SNS_TOPIC_ARN: Optional[str] = None
    AWS_SES_REGION: str = "us-east-1"
    AZURE_BLOB_CONNECTION_STR: Optional[str] = None
    AZURE_BLOB_CONTAINER: Optional[str] = None
    GCS_BUCKET_NAME: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    REDIS_URL: Optional[str] = None
    DB_CONNECTION_STRING: Optional[str] = None
    KAFKA_BOOTSTRAP_SERVERS: Optional[str] = None
    RABBITMQ_URL: Optional[str] = None

    # Messaging & Notifications
    SENDGRID_API_KEY: Optional[str] = None
    SLACK_WEBHOOK_URL: Optional[str] = None
    TEAMS_WEBHOOK_URL: Optional[str] = None
    FCM_SERVER_KEY: Optional[str] = None
    PUSHOVER_USER_KEY: Optional[str] = None
    PUSHOVER_API_TOKEN: Optional[str] = None
    DISCORD_WEBHOOK_URL: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM_PHONE: Optional[str] = None

    # Monitoring & Analytics
    PROMETHEUS_PUSHGATEWAY: Optional[str] = None
    GA4_MEASUREMENT_ID: Optional[str] = None
    GA4_API_SECRET: Optional[str] = None
    MIXPANEL_TOKEN: Optional[str] = None
    SEGMENT_WRITE_KEY: Optional[str] = None
    AMPLITUDE_API_KEY: Optional[str] = None
    IPINFO_TOKEN: Optional[str] = None
    UA_PARSER_REGEX_PATH: str = ""

    # Data Enrichment
    CLEARBIT_API_KEY: Optional[str] = None
    PEOPLE_DATA_LABS_API_KEY: Optional[str] = None
    HUNTER_API_KEY: Optional[str] = None
    FULLCONTACT_API_KEY: Optional[str] = None
    ZOOMINFO_API_KEY: Optional[str] = None
    PIPL_API_KEY: Optional[str] = None
    SNOVIO_API_KEY: Optional[str] = None

    # Payment Gateways
    STRIPE_API_KEY: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    SQUARE_ACCESS_TOKEN: Optional[str] = None
    SQUARE_ENVIRONMENT: Literal["sandbox", "production"] = "sandbox"
    BRAINTREE_MERCHANT_ID: Optional[str] = None
    BRAINTREE_PUBLIC_KEY: Optional[str] = None
    BRAINTREE_PRIVATE_KEY: Optional[str] = None
    AUTHORIZE_NET_API_LOGIN_ID: Optional[str] = None
    AUTHORIZE_NET_TRANSACTION_KEY: Optional[str] = None
    ADYEN_API_KEY: Optional[str] = None
    ADYEN_MERCHANT_ACCOUNT: Optional[str] = None
    ADYEN_ENVIRONMENT: Literal["TEST", "LIVE"] = "TEST"
    PLAID_CLIENT_ID: Optional[str] = None
    PLAID_SECRET: Optional[str] = None
    PLAID_ENVIRONMENT: Literal["sandbox", "development", "production"] = "sandbox"

    # Utility Services
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = None
    CONFIG_PATH: str = "config/playbook.yaml"
    API_AUTH_KEY: Optional[str] = None

    # Memory Service
    MEMORY_BACKEND: Literal["rest", "file"] = "rest"
    MEMORY_ENDPOINT: str = "http://localhost:8000"
    MEMORY_FILE_PATH: str = "memory.jsonl"

    # Logistics & E-commerce
    TMS_API_URL: Optional[str] = None
    TMS_API_KEY: Optional[str] = None
    INVENTORY_API_URL: Optional[str] = None
    INVENTORY_API_KEY: Optional[str] = None
    ECOMMERCE_API_URL: Optional[str] = None
    ECOMMERCE_API_KEY: Optional[str] = None

    class Config:
        case_sensitive = False

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Insert dotenv loading without requiring ``python-dotenv``."""

            def dotenv_settings(settings):
                return _load_env_file(_DEFAULT_ENV_FILE)

            return init_settings, env_settings, dotenv_settings, file_secret_settings

    @validator("AWS_REGION", allow_reuse=True)
    def validate_region(cls, value: str) -> str:
        valid = {
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-central-1",
            "ap-southeast-1",
            "ap-northeast-1",
        }
        if value not in valid:
            raise ValueError("Invalid AWS region")
        return value


# Instantiate a single global settings object used across the project
settings = Settings()
