import sys
import types
import src.api as api


def test_main_uses_api_host(monkeypatch):
    """The entrypoint should pass API_HOST to uvicorn."""
    captured = {}

    def fake_run(app, host=None, port=None):
        captured['host'] = host
        captured['port'] = port

    monkeypatch.setitem(sys.modules, 'uvicorn', types.SimpleNamespace(run=fake_run))
    monkeypatch.setenv('API_HOST', '127.0.0.1')
    monkeypatch.setenv('PORT', '12345')
    api.settings.API_HOST = '127.0.0.1'
    monkeypatch.setattr(api, 'create_app', lambda *a, **k: 'app')
    monkeypatch.setattr(api, 'SolutionOrchestrator', lambda *a, **k: 'orch')
    monkeypatch.setattr(api, 'setup_logging', lambda: None)

    api.main([])

    assert captured['host'] == '127.0.0.1'
    assert captured['port'] == 12345

