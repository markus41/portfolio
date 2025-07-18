from pathlib import Path
import yaml


def test_chart_yaml_loads() -> None:
    chart = Path('helm/brookside/Chart.yaml')
    data = yaml.safe_load(chart.read_text())
    assert data["apiVersion"] == "v2"
    assert "version" in data


def test_values_yaml_loads() -> None:
    values = Path('helm/brookside/values.yaml')
    data = yaml.safe_load(values.read_text())
    assert "image" in data
    assert "repository" in data["image"]
