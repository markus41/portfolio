
"""Configuration constants populated from environment variables.

This module exposes a flat list of API keys, URLs and other settings used
by the various agent and tool classes throughout the repository.  Each
constant simply reads the value from ``os.getenv`` which means tests can
easily override them by modifying ``os.environ``.
"""

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CRM_API_URL     = os.getenv("CRM_API_URL")
CRM_API_KEY     = os.getenv("CRM_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
GOOGLE_ADS_API_KEY = os.getenv("GOOGLE_ADS_API_KEY", "")
REDIS_URL                 = os.getenv("REDIS_URL")
SLACK_WEBHOOK_URL         = os.getenv("SLACK_WEBHOOK_URL")
TEAMS_WEBHOOK_URL         = os.getenv("TEAMS_WEBHOOK_URL")
PROMETHEUS_PUSHGATEWAY    = os.getenv("PROMETHEUS_PUSHGATEWAY")
MLS_API_URL              = os.getenv("MLS_API_URL")
MLS_API_KEY              = os.getenv("MLS_API_KEY")
RE_LEADS_API_URL         = os.getenv("RE_LEADS_API_URL")
RE_LEADS_API_KEY         = os.getenv("RE_LEADS_API_KEY")
LISTING_POST_API_URL     = os.getenv("LISTING_POST_API_URL")
LISTING_POST_API_KEY     = os.getenv("LISTING_POST_API_KEY")
CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY")
DOCUSIGN_ACCESS_TOKEN = os.getenv("DOCUSIGN_ACCESS_TOKEN")
DOCUSIGN_INTEGRATOR_KEY = os.getenv("DOCUSIGN_INTEGRATOR_KEY")
DOCUSIGN_USER_ID = os.getenv("DOCUSIGN_USER_ID")
DOCUSIGN_ACCOUNT_ID = os.getenv("DOCUSIGN_ACCOUNT_ID")
DOCUSIGN_BASE_URL = os.getenv("DOCUSIGN_BASE_URL")
STRIPE_API_KEY            = os.getenv("STRIPE_API_KEY")
AWS_ACCESS_KEY_ID         = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY     = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET             = os.getenv("AWS_S3_BUCKET")
GOOGLE_TRANSLATE_API_KEY  = os.getenv("GOOGLE_TRANSLATE_API_KEY")
DB_CONNECTION_STRING        = os.getenv("DB_CONNECTION_STRING")        # e.g. "postgresql://user:pass@host:port/dbname"
KAFKA_BOOTSTRAP_SERVERS     = os.getenv("KAFKA_BOOTSTRAP_SERVERS")     # CSV list, e.g. "broker1:9092,broker2:9092"
RABBITMQ_URL                = os.getenv("RABBITMQ_URL")                # e.g. "amqps://user:pass@host:5671/vhost"
AZURE_BLOB_CONNECTION_STR   = os.getenv("AZURE_BLOB_CONNECTION_STR")   # for azure-storage-blob
AZURE_BLOB_CONTAINER        = os.getenv("AZURE_BLOB_CONTAINER")        # name of  container
GCS_BUCKET_NAME             = os.getenv("GCS_BUCKET_NAME")             # Google Cloud Storage bucket
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # path to credentials JSON
MONDAY_API_TOKEN        = os.getenv("MONDAY_API_TOKEN")
MONDAY_API_URL          = os.getenv("MONDAY_API_URL", "https://api.monday.com/v2")
HUBSPOT_API_KEY         = os.getenv("HUBSPOT_API_KEY")
DYNAMICS_TENANT_ID      = os.getenv("DYNAMICS_TENANT_ID")
DYNAMICS_CLIENT_ID      = os.getenv("DYNAMICS_CLIENT_ID")
DYNAMICS_CLIENT_SECRET  = os.getenv("DYNAMICS_CLIENT_SECRET")
DYNAMICS_API_URL        = os.getenv("DYNAMICS_API_URL") 
SF_CLIENT_ID            = os.getenv("SF_CLIENT_ID")
SF_CLIENT_SECRET        = os.getenv("SF_CLIENT_SECRET")
SF_USERNAME             = os.getenv("SF_USERNAME")
SF_PASSWORD             = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN       = os.getenv("SF_SECURITY_TOKEN")
SF_DOMAIN               = os.getenv("SF_DOMAIN", "login.salesforce.com")
GA4_MEASUREMENT_ID    = os.getenv("GA4_MEASUREMENT_ID")
GA4_API_SECRET        = os.getenv("GA4_API_SECRET")
MIXPANEL_TOKEN        = os.getenv("MIXPANEL_TOKEN")
SEGMENT_WRITE_KEY     = os.getenv("SEGMENT_WRITE_KEY")
AMPLITUDE_API_KEY     = os.getenv("AMPLITUDE_API_KEY")
IPINFO_TOKEN          = os.getenv("IPINFO_TOKEN")
UA_PARSER_REGEX_PATH  = os.getenv("UA_PARSER_REGEX_PATH", "")  # optional path to ua_parser regexes
PEOPLE_DATA_LABS_API_KEY   = os.getenv("PEOPLE_DATA_LABS_API_KEY")
HUNTER_API_KEY             = os.getenv("HUNTER_API_KEY")
FULLCONTACT_API_KEY        = os.getenv("FULLCONTACT_API_KEY")
ZOOMINFO_API_KEY           = os.getenv("ZOOMINFO_API_KEY")
PIPL_API_KEY               = os.getenv("PIPL_API_KEY")
SNOVIO_API_KEY             = os.getenv("SNOVIO_API_KEY")
PAYPAL_CLIENT_ID             = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET         = os.getenv("PAYPAL_CLIENT_SECRET")
SQUARE_ACCESS_TOKEN          = os.getenv("SQUARE_ACCESS_TOKEN")
SQUARE_ENVIRONMENT           = os.getenv("SQUARE_ENVIRONMENT", "sandbox")  # or "production"
BRAINTREE_MERCHANT_ID        = os.getenv("BRAINTREE_MERCHANT_ID")
BRAINTREE_PUBLIC_KEY         = os.getenv("BRAINTREE_PUBLIC_KEY")
BRAINTREE_PRIVATE_KEY        = os.getenv("BRAINTREE_PRIVATE_KEY")
AUTHORIZE_NET_API_LOGIN_ID   = os.getenv("AUTHORIZE_NET_API_LOGIN_ID")
AUTHORIZE_NET_TRANSACTION_KEY= os.getenv("AUTHORIZE_NET_TRANSACTION_KEY")
ADYEN_API_KEY                = os.getenv("ADYEN_API_KEY")
ADYEN_MERCHANT_ACCOUNT       = os.getenv("ADYEN_MERCHANT_ACCOUNT")
ADYEN_ENVIRONMENT            = os.getenv("ADYEN_ENVIRONMENT", "TEST")        # or "LIVE"
PLAID_CLIENT_ID              = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET                 = os.getenv("PLAID_SECRET")
PLAID_ENVIRONMENT            = os.getenv("PLAID_ENVIRONMENT", "sandbox")    # or "development"/"production"
TWILIO_ACCOUNT_SID        = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN         = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE         = os.getenv("TWILIO_FROM_PHONE")
AWS_SNS_TOPIC_ARN         = os.getenv("AWS_SNS_TOPIC_ARN")
AWS_REGION                = os.getenv("AWS_REGION", "us-east-1")
FCM_SERVER_KEY            = os.getenv("FCM_SERVER_KEY")
PUSHOVER_USER_KEY         = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN        = os.getenv("PUSHOVER_API_TOKEN")
DISCORD_WEBHOOK_URL       = os.getenv("DISCORD_WEBHOOK_URL")
AWS_SES_REGION            = os.getenv("AWS_SES_REGION", "us-east-1")
CONFIG_PATH               = os.getenv("CONFIG_PATH", "config/playbook.yaml")

# Logistics & e-commerce APIs
TMS_API_URL           = os.getenv("TMS_API_URL")
TMS_API_KEY           = os.getenv("TMS_API_KEY")
INVENTORY_API_URL     = os.getenv("INVENTORY_API_URL")
INVENTORY_API_KEY     = os.getenv("INVENTORY_API_KEY")
ECOMMERCE_API_URL     = os.getenv("ECOMMERCE_API_URL")
ECOMMERCE_API_KEY     = os.getenv("ECOMMERCE_API_KEY")
