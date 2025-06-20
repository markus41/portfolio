# ReactFlow Workflow Editor

This folder contains a minimal React application powered by [ReactFlow](https://reactflow.dev/).
It provides a drag-and-drop editor for connecting agents and tools into an executable workflow.

## Development

```bash
npm install
npm run dev
```

The application persists workflows by sending them to the backend via the
`/workflows` API endpoint.

## Configuration

The editor requires an API key when communicating with the backend service.
Create an `.env` file in this directory and define `VITE_API_KEY`:

```bash
cp .env.example .env
echo "VITE_API_KEY=mysecret" >> .env
```

When running `npm run dev` or building the project with `vite`, the value of
`VITE_API_KEY` is injected and included as the `X-API-Key` header on every
workflow save request. For production deployments you may also inject a
runtime configuration object named `window.APP_CONFIG` before loading the
bundle:

```html
<script>
  window.APP_CONFIG = { apiKey: 'mysecret' };
</script>
```

This fallback enables dynamic key assignment without rebuilding the frontend.

## Live History Streaming

`HistoryViewer` now streams real-time activity using Server-Sent Events (SSE).
It connects to the `/teams/<name>/stream` endpoint via `EventSource` and
appends incoming `activity` messages to the list. By default the component
listens to the `sales` team, but any team name can be provided:

```jsx
<HistoryViewer team="demo" />
```

When the page loads it fetches the latest history snapshot and then establishes
the streaming connection. The API key configured through `VITE_API_KEY` or
`window.APP_CONFIG.apiKey` is automatically included as the `api_key` query
parameter.
