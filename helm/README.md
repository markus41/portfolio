# Helm Chart

This directory contains a lightweight Helm chart for deploying the Brookside BI orchestrator.

To install the chart locally:

```bash
helm install brookside ./helm/brookside \
  --set image.tag=<release>
```

Replace `<release>` with the desired image tag, e.g. `v1.0.0`.
