import json
from pathlib import Path



from src.solution_orchestrator import SolutionOrchestrator

TEMPLATE_DIR = Path('workflows/templates')


def test_blog_post_workflow(tmp_path):
    team_file = TEMPLATE_DIR / 'writer_team.json'
    plan_file = TEMPLATE_DIR / 'blog_post.json'
    plans = json.loads(plan_file.read_text())

    # create orchestrator and run goal
    orch = SolutionOrchestrator({'writer': str(team_file)}, planner_plans=plans)
    result = orch.execute_goal('blog_post')
    assert result['status'] == 'complete'
    assert len(result['results']) == 3


def test_template_files_parse():
    for name in ['writer_team.json', 'analysis_team.json']:
        data = json.loads((TEMPLATE_DIR / name).read_text())
        assert 'config' in data

    for name in ['blog_post.json', 'document_summary.json', 'sales_outreach.json']:
        data = json.loads((TEMPLATE_DIR / name).read_text())
        assert isinstance(data, dict)
