from src.user_settings import (
    init_db,
    upsert_settings,
    get_settings,
    UserSettingsData,
    create_engine,
)
import pytest


@pytest.mark.skipif(create_engine is None, reason="SQLAlchemy not installed")
def test_roundtrip(tmp_path):
    db = tmp_path / "test.db"
    init_db(f"sqlite:///{db}")
    data = UserSettingsData(
        api_key="k1",
        organization="Acme",
        crm_api_url="http://c",
        crm_api_key="key",
        disabled_teams=["sales"],
    )
    upsert_settings("k1", data)
    loaded = get_settings("k1")
    assert loaded.crm_api_url == "http://c"
    assert loaded.disabled_teams == ["sales"]
