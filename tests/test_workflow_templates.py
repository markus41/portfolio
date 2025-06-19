import json
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")


from src.solution_orchestrator import SolutionOrchestrator

TEMPLATE_DIR = Path('workflows/templates')


def test_blog_post_workflow(tmp_path):
    for ext in ("json", "yaml"):
        team_file = TEMPLATE_DIR / f"writer_team.{ext}"
        plan_file = TEMPLATE_DIR / f"blog_post.{ext}"
        if ext == "json":
            plans = json.loads(plan_file.read_text())
        else:
            plans = yaml.safe_load(plan_file.read_text())

        orch = SolutionOrchestrator({"writer": str(team_file)}, planner_plans=plans)
        result = orch.execute_goal("blog_post")
        assert result["status"] == "complete"
        assert len(result["results"]) == 3


def test_template_files_parse():
    for base in ['writer_team', 'analysis_team']:
        for ext in ("json", "yaml"):
            data = (TEMPLATE_DIR / f"{base}.{ext}").read_text()
            parsed = json.loads(data) if ext == "json" else yaml.safe_load(data)
            assert 'config' in parsed

    for base in ['blog_post', 'document_summary', 'sales_outreach']:
        for ext in ("json", "yaml"):
            data = (TEMPLATE_DIR / f"{base}.{ext}").read_text()
            parsed = json.loads(data) if ext == "json" else yaml.safe_load(data)
            assert isinstance(parsed, dict)
