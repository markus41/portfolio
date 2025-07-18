# Helm Deployment

A lightweight Helm chart is provided under `helm/` to simplify Kubernetes deployments.

Install the chart from the repository root:

```bash
helm install brookside ./helm/brookside \
  --set image.tag=<version>
```

Set `image.tag` to a version published on GitHub Container Registry. The chart
deploys a single orchestrator pod exposing port `8000`.
