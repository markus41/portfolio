# Web Configuration Editor

A lightweight React page (`webui/index.html`) allows non-developers to adjust agent teams and environment settings without touching the source code.

## Running the API

Start the FastAPI server exposing the new configuration endpoints:

```bash
python -m src.api
```

Provide the `X-API-Key` header set to `API_AUTH_KEY` from your `.env` file.

## Using the Editor

Open `webui/index.html` in your browser. Enter the API key when prompted and the page will list available team configuration files from `src/teams/` and the current environment settings.

1. **Teams** – select a team to view and edit its JSON. Press **Save Team** to persist changes back to disk.
2. **Environment Settings** – modify key/value pairs in JSON form and click **Save Settings**. The values are written to the `.env` file used by the CLI and Python modules.

The CLI automatically reads these files, so updates made through the web UI take effect the next time the orchestrator or tests are run.
