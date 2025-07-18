from src.utils.team_mapping import parse_team_mapping
import pytest


def test_parse_team_mapping_basic():
    pairs = ["sales=teams/sales.json", "ops=teams/ops.json"]
    result = parse_team_mapping(pairs)
    assert result == {
        "sales": "teams/sales.json",
        "ops": "teams/ops.json",
    }


def test_parse_team_mapping_allows_overrides():
    pairs = ["demo=one.json", "demo=two.json"]
    result = parse_team_mapping(pairs)
    assert result == {"demo": "two.json"}


@pytest.mark.parametrize("spec", ["foo"])
def test_parse_team_mapping_invalid(spec):
    with pytest.raises(ValueError):
        parse_team_mapping([spec])
