# Environment Variable Reference

This document describes every environment variable consumed in the project. The
values live in [src/config.py](../src/config.py) and are provided by a Pydantic
`BaseSettings` class. They can be loaded from environment variables or a local
`.env` file.  Which file is used depends on the ``ENV`` and ``ENV_FILE``
variables documented below.

## Environment Selection

- `ENV` – Defines the runtime environment. ``prod`` loads ``.env`` while any
  other value loads ``.env.<ENV>`` (for example ``ENV=dev`` loads ``.env.dev``).
  Defaults to ``dev``.
- `ENV_FILE` – Explicit path to a dotenv file. When set this overrides the
  ``ENV`` based behaviour.

## AI Providers
- `OPENAI_API_KEY` – API key for OpenAI models.

## CRM & Marketing Platforms
- `CRM_API_URL` – Base URL for the CRM system.
- `CRM_API_KEY` – Authentication key for the CRM.
- `MONDAY_API_TOKEN` – Monday.com API token.
- `MONDAY_API_URL` – Monday.com GraphQL endpoint, default `https://api.monday.com/v2`.
- `HUBSPOT_API_KEY` – HubSpot API key.
- `DYNAMICS_TENANT_ID` – Microsoft Dynamics tenant ID.
- `DYNAMICS_CLIENT_ID` – Microsoft Dynamics client ID.
- `DYNAMICS_CLIENT_SECRET` – Microsoft Dynamics client secret.
- `DYNAMICS_API_URL` – Dynamics API URL.
- `SF_CLIENT_ID` – Salesforce client ID.
- `SF_CLIENT_SECRET` – Salesforce client secret.
- `SF_USERNAME` – Salesforce username.
- `SF_PASSWORD` – Salesforce password.
- `SF_SECURITY_TOKEN` – Salesforce security token.
- `SF_DOMAIN` – Salesforce domain, defaults to `login.salesforce.com`.

## Advertising & Social Platforms
- `FACEBOOK_ACCESS_TOKEN` – Access token for Facebook APIs used by `AdTool`.
- `GOOGLE_ADS_API_KEY` – Google Ads API key used by `AdTool`.

## Real Estate APIs
- `MLS_API_URL` – Base URL for the MLS data feed.
- `MLS_API_KEY` – Key for MLS integration.
- `RE_LEADS_API_URL` – Lead source API URL.
- `RE_LEADS_API_KEY` – Lead source API key.
- `LISTING_POST_API_URL` – Endpoint for posting listings.
- `LISTING_POST_API_KEY` – Key for listing posts.

## Document Signing
- `DOCUSIGN_ACCESS_TOKEN` – DocuSign OAuth token.
- `DOCUSIGN_INTEGRATOR_KEY` – DocuSign integrator key.
- `DOCUSIGN_USER_ID` – DocuSign user ID.
- `DOCUSIGN_ACCOUNT_ID` – DocuSign account ID.
- `DOCUSIGN_BASE_URL` – DocuSign base URL.

## Storage & Infrastructure
- `AWS_ACCESS_KEY_ID` – AWS access key.
- `AWS_SECRET_ACCESS_KEY` – AWS secret key.
- `AWS_S3_BUCKET` – S3 bucket name.
- `AWS_REGION` – AWS region, default `us-east-1`.
- `AWS_SNS_TOPIC_ARN` – SNS topic ARN.
- `AWS_SES_REGION` – SES region, default `us-east-1`.
- `AZURE_BLOB_CONNECTION_STR` – Azure blob storage connection string.
- `AZURE_BLOB_CONTAINER` – Azure blob container name.
- `GCS_BUCKET_NAME` – Google Cloud Storage bucket.
- `GOOGLE_APPLICATION_CREDENTIALS` – Path to Google service account JSON.
- `REDIS_URL` – Redis connection string.
- `DB_CONNECTION_STRING` – Database URL.
- The `GET /history` endpoint reads from this database and supports
  `team` and `event_type` query parameters in addition to `limit` and
  `offset` for filtering stored events.
- `KAFKA_BOOTSTRAP_SERVERS` – Kafka broker list.
- `RABBITMQ_URL` – RabbitMQ connection string.
- `CLOUD_DOCS_API_URL` – Base URL for the cloud document service.
- `CLOUD_DOCS_API_KEY` – Authentication token for the cloud docs API.

## Memory Service
- `MEMORY_BACKEND` – Choose the persistence layer (`rest`, `rest_async`, `file`, `redis`, `embedding`).
- `MEMORY_ENDPOINT` – URL for the REST backend when `MEMORY_BACKEND=rest`.
- `MEMORY_FILE_PATH` – File path when `MEMORY_BACKEND=file`.
- `MEMORY_REDIS_URL` – Redis URL when `MEMORY_BACKEND=redis`.
- `MEMORY_EMBED_FIELD` – Payload field containing text when `MEMORY_BACKEND=embedding`.

## Messaging & Notifications
- `SENDGRID_API_KEY` – SendGrid API key.
- `DEFAULT_FROM_EMAIL` – Address used as the sender when none is provided.
- `SLACK_WEBHOOK_URL` – Slack webhook for notifications.
- `TEAMS_WEBHOOK_URL` – Microsoft Teams webhook.
- `TWILIO_ACCOUNT_SID` – Twilio account SID.
- `TWILIO_AUTH_TOKEN` – Twilio auth token.
- `TWILIO_FROM_PHONE` – Twilio sender phone number.
- `ORCHESTRATOR_CONFIDENCE_THRESHOLD` – Minimum confidence before auto actions are accepted. Default `0.7`.
- `ORCHESTRATOR_MAX_RETRIES` – How many times the orchestrator retries a failed step before escalation. Default `3`.
- `FCM_SERVER_KEY` – Firebase Cloud Messaging server key.
- `PUSHOVER_USER_KEY` – Pushover user key.
- `PUSHOVER_API_TOKEN` – Pushover API token.
- `DISCORD_WEBHOOK_URL` – Discord webhook.

## Monitoring & Analytics
- `PROMETHEUS_PUSHGATEWAY` – Prometheus Pushgateway URL. When defined the API
  emits request metrics as described in [metrics.md](metrics.md).
- `GA4_MEASUREMENT_ID` – Google Analytics 4 measurement ID.
- `GA4_API_SECRET` – Google Analytics API secret.
- `MIXPANEL_TOKEN` – Mixpanel project token.
- `SEGMENT_WRITE_KEY` – Segment write key.
- `AMPLITUDE_API_KEY` – Amplitude API key.
- `VISITOR_ANALYTICS_URL` – HTTP endpoint for storing visitor events.
- `VISITOR_ANALYTICS_KEY` – Bearer token for the analytics service.
- `IPINFO_TOKEN` – ipinfo.io token.
- `UA_PARSER_REGEX_PATH` – Optional path to UA parser regexes.

## Data Enrichment
- `CLEARBIT_API_KEY` – Clearbit enrichment key.
- `PEOPLE_DATA_LABS_API_KEY` – People Data Labs API key.
- `HUNTER_API_KEY` – Hunter.io key.
- `FULLCONTACT_API_KEY` – FullContact key.
- `ZOOMINFO_API_KEY` – ZoomInfo key.
- `PIPL_API_KEY` – Pipl key.
- `SNOVIO_API_KEY` – Snov.io key.

## Payment Gateways
- `STRIPE_API_KEY` – Stripe API key.
- `PAYPAL_CLIENT_ID` – PayPal client ID.
- `PAYPAL_CLIENT_SECRET` – PayPal secret.
- `SQUARE_ACCESS_TOKEN` – Square access token.
- `SQUARE_ENVIRONMENT` – Square environment (`sandbox` or `production`).
- `BRAINTREE_MERCHANT_ID` – Braintree merchant ID.
- `BRAINTREE_PUBLIC_KEY` – Braintree public key.
- `BRAINTREE_PRIVATE_KEY` – Braintree private key.
- `AUTHORIZE_NET_API_LOGIN_ID` – Authorize.Net login ID.
- `AUTHORIZE_NET_TRANSACTION_KEY` – Authorize.Net transaction key.
- `ADYEN_API_KEY` – Adyen API key.
- `ADYEN_MERCHANT_ACCOUNT` – Adyen merchant account.
- `ADYEN_ENVIRONMENT` – Adyen environment (`TEST` or `LIVE`).
- `PLAID_CLIENT_ID` – Plaid client ID.
- `PLAID_SECRET` – Plaid secret.
- `PLAID_ENVIRONMENT` – Plaid environment (`sandbox`, `development`, or `production`).

## Logistics & E-commerce
- `TMS_API_URL` – Transportation management system endpoint.
- `TMS_API_KEY` – Key for the TMS.
- `INVENTORY_API_URL` – Inventory service endpoint.
- `INVENTORY_API_KEY` – Key for the inventory service.
- `ECOMMERCE_API_URL` – E‑commerce API URL.
- `ECOMMERCE_API_KEY` – E‑commerce API key.

## Utility Services
- `GOOGLE_TRANSLATE_API_KEY` – Google Translate API key.
- `CONFIG_PATH` – Path to the orchestrator configuration, defaults to `config/playbook.yaml`.
- `API_AUTH_KEY` – Token required by the FastAPI server for requests.
- `ALLOWED_ORIGINS` – Comma separated list of domains allowed for CORS requests.
- `SCRAPER_USER_AGENT` – HTTP User-Agent string used by `ScrapingPlugin`.
