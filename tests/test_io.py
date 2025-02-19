import os
from pathlib import Path

import pytest

from src.football_pipeline.io import read_yaml, write_to_parquet


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


@pytest.mark.parametrize(
    "df_fixture_name, path, expected_output",
    [
        pytest.param(
            "get_mock_df_001",
            "test.parquet",
            True,
            id="Return True for successful .parquet writes",
        ),
        pytest.param(
            "get_mock_df_001",
            "test.invalid_ext",
            False,
            id="Return False for invalid file extensions",
        ),
        pytest.param(
            "get_mock_df_001",
            "when_they_dont_score_they_hardly_win/test.parquet",
            False,
            id="Return False for invalid directory",
        ),
    ],
)
def test_write_to_parquet(request, df_fixture_name, path, expected_output):
    input_df = request.getfixturevalue(df_fixture_name)
    try:
        result = write_to_parquet(input_df, path)
        assert result == expected_output
        assert os.path.exists(path) == expected_output
    finally:
        if os.path.exists(path):
            os.remove(path)
