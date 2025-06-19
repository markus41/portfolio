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
