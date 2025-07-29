from string import punctuation

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.football_pipeline.domain.transform import add_ingestion_columns, sanitize_url


@pytest.mark.parametrize(
    "fixture_name, batch_guid, date_time, column, expected_unique_values",
    [
        pytest.param(
            "get_mock_df_001",
            "test-batch-123",
            "2024-02-17T12:00:00",
            "source_guid",
            6,
            id="Ensure unique source_guid for all rows",
        ),
        pytest.param(
            "get_mock_df_001",
            "test-batch-123",
            "2024-02-17T12:00:00",
            "batch_guid",
            1,
            id="Ensure same batch_guid for all rows",
        ),
        pytest.param(
            "get_mock_df_001",
            "test-batch-123",
            "2024-02-17T12:00:00",
            "ingestion_datetime",
            1,
            id="Ensure same datetime for all rows",
        ),
    ],
)
def test_add_ingestion_columns(
    request, fixture_name, batch_guid, date_time, column, expected_unique_values
):
    inp_df = request.getfixturevalue(fixture_name)
    result = add_ingestion_columns(inp_df, batch_guid, date_time)
    assert all(inp_df.eq(result[inp_df.columns]))  # the given data is unchanged
    assert result[column].nunique() == expected_unique_values
    assert (result["batch_guid"] == batch_guid).all()
    assert (result["ingestion_datetime"] == date_time).all()


@given(st.text())
def test_sanitize_url(input_url):
    result = sanitize_url(input_url)
    invalid_substrings = [
        "https://",
        "http://",
        "www.",
    ] + [character for character in punctuation if character != "_"]
    assert all([substring not in result for substring in invalid_substrings])
