# Metrics Collection

Brookside exposes basic Prometheus metrics when the `PROMETHEUS_PUSHGATEWAY`
environment variable is configured. A lightweight middleware records the total
number of requests and their latencies and pushes two gauges to the configured
Pushgateway:

- `api_request_count` – incremented for every request
- `api_request_latency_seconds` – time taken to handle the request

The middleware is automatically enabled when `PROMETHEUS_PUSHGATEWAY` is a non
-empty value. When unset, no metrics are pushed and the overhead is zero.

```bash
export PROMETHEUS_PUSHGATEWAY="http://localhost:9091"
python -m src.api
```

Both metrics include the request path and method as labels so you can aggregate
by endpoint in Prometheus. See the environment variable reference in
[docs/environment.md](environment.md) for related settings.

## Orchestrator Event Metrics

`SolutionOrchestrator` now assigns a unique `event_id` to every incoming event.
When metrics are enabled, an additional gauge `orchestrator_events_total` is
pushed for each processed event:

```python
labels = {"team": team, "event_type": event_type, "event_id": event_id}
pusher.push_metric("orchestrator_events_total", 1, labels)
```

Including the `event_id` label makes it trivial to correlate Prometheus data
with structured logs or SSE streams.

## Grafana/Loki Example

To visualise activity logs in Grafana you can run Loki and Promtail alongside
Prometheus. Below is a minimal `promtail` configuration that tails the JSONL log
file and parses the structured fields:

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: brookside
    static_configs:
      - targets: [localhost]
        labels:
          job: brookside
          __path__: /var/log/brookside/activity.jsonl
    pipeline_stages:
      - json:
          expressions:
            timestamp: timestamp
            agent_id: agent_id
            event_id: event_id
            summary: summary
      - timestamp:
          source: timestamp
          format: RFC3339Nano
```

Import the Loki data source into Grafana and build dashboards by querying
`{job="brookside"}`. Combined with the Prometheus metrics above you can easily
graph event throughput and drill into individual events using their `event_id`.
