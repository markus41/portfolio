# Metrics Collection

Brookside exposes basic Prometheus metrics when the `PROMETHEUS_PUSHGATEWAY`
environment variable is configured. A lightweight middleware records the total
number of requests and their latencies and pushes two gauges to the configured
Pushgateway:

- `api_request_count` – incremented for every request
- `api_request_latency_seconds` – time taken to handle the request
- `agent_tokens_used` – tokens consumed by an agent execution
- `agent_loop_count` – number of times an agent was invoked

The middleware is automatically enabled when `PROMETHEUS_PUSHGATEWAY` is a non
-empty value. When unset, no metrics are pushed and the overhead is zero.

```bash
export PROMETHEUS_PUSHGATEWAY="http://localhost:9091"
python -m src.api
```

Both metrics include the request path and method as labels so you can aggregate
by endpoint in Prometheus. See the environment variable reference in
[docs/environment.md](environment.md) for related settings.
