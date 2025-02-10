from pathlib import Path

import pytest

from src.football_pipeline.io import read_yaml

current_file_path = Path(__file__)

MOCK_DATA_DIR = current_file_path.parent / "mock_data" / "mock_yamls"

valid_yaml_path = MOCK_DATA_DIR / "valid.yaml"
invalid_yaml_path = MOCK_DATA_DIR / "invalid.yaml"


@pytest.mark.parametrize(
    "test_file, expected_result",
    [
        (
            valid_yaml_path,
            {
                "league": {
                    "backseries": False,
                    "players": ["some player", "some other player"],
                }
            },
        ),
        (invalid_yaml_path, {}),
    ],
)
def test_read_yaml(test_file, expected_result):
    """Tests the read_yaml function using a sample file."""
    result = read_yaml(test_file)
    print(f"Result for {test_file}: {result}")
    assert result == expected_result
