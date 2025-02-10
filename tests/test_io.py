from pathlib import Path

import pytest

from src.football_pipeline.io import read_yaml


@pytest.mark.parametrize(
    "test_file, expected_result",
    [
        (
            "valid.yaml",
            {
                "league": {
                    "backseries": False,
                    "players": ["some player", "some other player"],
                }
            },
        ),
        ("invalid.yaml", {}),
        ("blank.yaml", {}),
    ],
)
def test_read_yaml(test_file, expected_result):
    """Tests the read_yaml function using a sample file."""
    file_path = Path(__file__).parent / "mock_data/mock_yamls" / test_file
    result = read_yaml(file_path)
    assert result == expected_result
