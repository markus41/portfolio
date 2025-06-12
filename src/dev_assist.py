"""Simple developer helper for generating boilerplate files."""

import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python dev_assist.py 'Describe component'")
        return
    desc = sys.argv[1]
    name = desc.lower().replace(" ", "_")
    code_file = Path(f"src/{name}.py")
    test_file = Path(f"tests/test_{name}.py")

    if not code_file.exists():
        code_file.write_text(f'"""TODO: {desc}."""\n')
    if not test_file.exists():
        test_file.write_text(
            '"""Tests for {name}"""\n\n\n' 'def test_placeholder():\n    assert True\n'
        )
    print(f"Created {code_file} and {test_file}")


if __name__ == "__main__":  # pragma: no cover - manual utility
    main()
