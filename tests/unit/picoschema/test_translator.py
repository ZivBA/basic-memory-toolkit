"""Tests for picoschema-to-JSON-Schema translator."""
from pathlib import Path

import yaml
import pytest

# Will fail import until translator exists — that's the point
from scripts.picoschema_to_jsonschema import translate_schema_file


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> tuple[Path, dict]:
    """Return (input_path, expected_dict) for a named fixture."""
    input_path = FIXTURES_DIR / name / "input.md"
    expected_path = FIXTURES_DIR / name / "expected.yaml"
    expected = yaml.safe_load(expected_path.read_text())
    return input_path, expected


def test_simple_required():
    input_path, expected = load_fixture("simple_required")
    result = translate_schema_file(input_path)
    assert result == expected
