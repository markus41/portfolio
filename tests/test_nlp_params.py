from src.utils.nlp_params import parse_parameters


def test_parse_parameters_basic():
    text = "Launch a campaign for small businesses on 2024-05-01 with a budget of $500"
    params = parse_parameters(text)
    assert params["budget"] == 500
    assert "2024-05-01" in params["dates"]
    assert params["target_audience"] == "small businesses"
