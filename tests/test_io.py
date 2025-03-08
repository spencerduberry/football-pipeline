import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.football_pipeline.io import extract_data, read_yaml, write_to_parquet


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


@pytest.mark.parametrize(
    "response_fixture_name, keys, expected_result",
    [
        (
            "response_dict",
            ["key_a", "key_c"],
            {
                "key_a": [{"col": 1}, {"col": 2}, {"col": 3}],
                "key_c": [{"col": 7}, {"col": 8}, {"col": 9}],
            },
        ),
        (
            "response_list",
            None,
            {"mock_path": [{"col": 1}, {"col": 2}, {"col": 3}]},
        ),
    ],
)
def test_extract_data(request, response_fixture_name, keys, expected_result):
    response_json = request.getfixturevalue(response_fixture_name)

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(response_json).encode("utf-8")
    mock_response.__enter__.return_value = mock_response
    mock_response.status = 200

    with (
        patch("urllib.request.Request"),
        patch("urllib.request.urlopen", return_value=mock_response),
    ):
        result = extract_data("http://mock.path", keys)
        assert {
            k: v.to_dict(orient="records") for k, v in result.items()
        } == expected_result


@pytest.mark.parametrize(
    "response_fixture_name, keys, expected_result",
    [
        (
            "response_dict",
            ["key_a", "key_c"],
            [
                {"err": Exception(), "key": "key_a"},
                {"err": Exception(), "key": "key_c"},
            ],
        ),
        (
            "response_list",
            None,
            [
                {"err": Exception(), "key": "mock_path"},
            ],
        ),
    ],
)
def test_extract_data_with_dataframe_exceptions(
    request, response_fixture_name, keys, expected_result
):
    response_json = request.getfixturevalue(response_fixture_name)

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(response_json).encode("utf-8")
    mock_response.__enter__.return_value = mock_response
    mock_response.status = 200

    with (
        patch("urllib.request.Request"),
        patch("urllib.request.urlopen", return_value=mock_response),
        patch("src.football_pipeline.io.pd.DataFrame", side_effect=Exception()),
    ):
        result = extract_data("http://mock.path", keys)
        mismatch = []
        for idx, expected_dict in enumerate(expected_result):
            result_dict = result[idx]
            if not all(
                (
                    result_dict.keys() == expected_dict.keys(),
                    result_dict["key"] == expected_dict["key"],
                )
            ):
                mismatch.append((result_dict, expected_dict))
        assert mismatch == []


def test_extract_data_invalid_url():
    with patch("urllib.request.urlopen", side_effect=ValueError()):
        response = extract_data("invalid_url")
        assert all(
            (
                "err" in response[0].keys(),
                "path" in response[0].keys(),
            )
        )
