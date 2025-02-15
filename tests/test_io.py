import os
from pathlib import Path

import pandas as pd
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


@pytest.fixture
def get_mock_df_002():
    return pd.DataFrame(
        {"column1": [1, 2, 3, 4, 5, 6], "column2": ["A", "B", "C", "D", "E", "F"]}
    )


@pytest.mark.parametrize(
    "df, path, expected_output",
    [
        pytest.param(
            "get_mock_df_002",
            "test.parquet",
            True,
            id="Return True for successful .parquet writes",
        ),
        pytest.param(
            "get_mock_df_002",
            "test.invalid_ext",
            False,
            id="Return False for invalid file extensions",
        ),
        pytest.param(
            "get_mock_df_002",
            "when_they_dont_score_they_hardly_win/test.parquet",
            False,
            id="Return False for invalid directory",
        ),
    ],
)
def test_write_to_parquet(request, df, path, expected_output):
    input_df = request.getfixturevalue(df)
    result = write_to_parquet(path, input_df)
    assert result == expected_output
    if expected_output:
        assert os.path.exists(path)
        os.remove(path)
    else:
        assert not os.path.exists(path)
