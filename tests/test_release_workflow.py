import pytest

yaml = pytest.importorskip("yaml")

from pathlib import Path


def test_release_workflow_structure():
    """Ensure the release workflow parses and contains expected steps."""
    wf_file = Path('.github/workflows/release.yml')
    assert wf_file.exists(), 'release.yml missing'
    data = yaml.safe_load(wf_file.read_text())

    # Trigger
    push = data.get('on', {}).get('push', {})
    assert 'tags' in push and 'v*.*.*' in push['tags']

    # Build job must run python -m build
    build_steps = data['jobs']['build']['steps']
    assert any('python -m build' in (step.get('run') or '') for step in build_steps)

    # Docker job must build multi-arch images
    docker_steps = data['jobs']['docker']['steps']
    build_push = [s for s in docker_steps if s.get('uses', '').startswith('docker/build-push-action')]
    assert build_push, 'docker build step missing'
    assert 'linux/amd64,linux/arm64' in build_push[0]['with']['platforms']
