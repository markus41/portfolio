from configparser import ConfigParser
from pathlib import Path

import src


def test_version_matches_setup_cfg():
    cfg_path = Path(__file__).resolve().parents[1] / "setup.cfg"
    parser = ConfigParser()
    parser.read(cfg_path)
    expected = parser["metadata"]["version"]
    assert src.__version__ == expected
    assert src.get_version() == expected
